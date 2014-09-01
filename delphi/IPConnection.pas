{
  Copyright (C) 2012-2014 Matthias Bolte <matthias@tinkerforge.com>

  Redistribution and use in source and binary forms of this file,
  with or without modification, are permitted. See the Creative
  Commons Zero (CC0 1.0) License for more details.
}

unit IPConnection;

{ FIXME: add TSocketWrapper to deal with the various socket implementations }

{$ifdef FPC}
 {$mode OBJFPC}{$H+}
{$else}
 {$ifdef MACOS}{$define DELPHI_MACOS}{$endif}
{$endif}

interface

uses
{$ifdef FPC}
 {$ifdef UNIX}CThreads, Errors, CNetDB, BaseUnix,{$else} Windows, WinSock,{$endif} Sockets,
{$else}
 {$ifdef MSWINDOWS}Windows, WinSock,{$endif}
{$endif}
{$ifdef DELPHI_MACOS}
  Posix.ArpaInet, Posix.Errno, Posix.NetDB, Posix.NetinetIn, Posix.NetinetTcp, Posix.String_, Posix.SysSocket, Posix.SysTypes, Posix.Unistd,
{$endif}
  Classes, SyncObjs, SysUtils, LEConverter, BlockingQueue, Device, TimedSemaphore, SHA1, BrickDaemon;

const
  IPCON_FUNCTION_DISCONNECT_PROBE = 128;
  IPCON_FUNCTION_ENUMERATE = 254;

  IPCON_CALLBACK_ENUMERATE = 253;
  IPCON_CALLBACK_CONNECTED = 0;
  IPCON_CALLBACK_DISCONNECTED = 1;

  IPCON_QUEUE_KIND_EXIT = 0;
  IPCON_QUEUE_KIND_DESTROY_AND_EXIT = 1;
  IPCON_QUEUE_KIND_META = 2;
  IPCON_QUEUE_KIND_PACKET = 3;

  IPCON_DISCONNECT_PROBE_INTERVAL = 5000;

  { enumerationType parameter of the TIPConnectionNotifyEnumerate }
  IPCON_ENUMERATION_TYPE_AVAILABLE = 0;
  IPCON_ENUMERATION_TYPE_CONNECTED = 1;
  IPCON_ENUMERATION_TYPE_DISCONNECTED = 2;

  { connectReason parameter of the TIPConnectionNotifyConnected }
  IPCON_CONNECT_REASON_REQUEST = 0;
  IPCON_CONNECT_REASON_AUTO_RECONNECT = 1;

  { disconnectReason parameter of the TIPConnectionNotifyDisconnected }
  IPCON_DISCONNECT_REASON_REQUEST = 0;
  IPCON_DISCONNECT_REASON_ERROR = 1;
  IPCON_DISCONNECT_REASON_SHUTDOWN = 2;

  { returned by GetConnectionState }
  IPCON_CONNECTION_STATE_DISCONNECTED = 0;
  IPCON_CONNECTION_STATE_CONNECTED = 1;
  IPCON_CONNECTION_STATE_PENDING = 2; { auto-reconnect in progress }

{$ifdef FPC}
  INVALID_SOCKET = -1;
 {$ifdef MSWINDOWS}
  ESysEINTR = WSAEINTR;
 {$endif}
{$else}
 {$ifdef DELPHI_MACOS}
  INVALID_SOCKET = -1;
  ESysEINTR = EINTR;
 {$else}
  ESysEINTR = WSAEINTR;
 {$endif}
{$endif}

type
  { ETinkerforgeException }
  ETinkerforgeException = class(Exception)
  end;

  { ETimeoutException }
  ETimeoutException = class(ETinkerforgeException)
  end;
  TimeoutException = ETimeoutException; { for backward compatibility }

  { EAlreadyConnectedException }
  EAlreadyConnectedException = class(ETinkerforgeException)
  end;

  { ENotConnectedException }
  ENotConnectedException = class(ETinkerforgeException)
  end;

  { ENotSupportedException }
  ENotSupportedException = class(ETinkerforgeException)
  end;
  NotSupportedException = ENotSupportedException; { for backward compatibility }

  { TThreadWrapper }
  TThreadWrapper = class;
  TThreadProcedure = procedure(thread: TThreadWrapper; opaque: pointer) of object;
  TThreadWrapper = class(TThread)
  private
    proc: TThreadProcedure;
    opaque: pointer;
  public
    constructor Create(const proc_: TThreadProcedure; opaque_: pointer);
    procedure Execute; override;
    function IsCurrent: boolean;
  end;

  type TCallbackContext = record
    queue: TBlockingQueue;
    mutex: TCriticalSection;
    packetDispatchAllowed: boolean;
    thread: TThreadWrapper;
  end;

  PCallbackContext = ^TCallbackContext;

  { TIPConnection }
  TIPConnection = class;
  TIPConnectionNotifyEnumerate = procedure(sender: TIPConnection; const uid: string; const connectedUid: string;
                                           const position: char; const hardwareVersion: TVersionNumber;
                                           const firmwareVersion: TVersionNumber; const deviceIdentifier: word;
                                           const enumerationType: byte) of object;
  TIPConnectionNotifyConnected = procedure(sender: TIPConnection; const connectReason: byte) of object;
  TIPConnectionNotifyDisconnected = procedure(sender: TIPConnection; const disconnectReason: byte) of object;
  TIPConnection = class
  public
    timeout: longint;
    devices: TDeviceTable;
  private
    host: string;
    port: word;
    autoReconnect: boolean;
    autoReconnectAllowed: boolean;
    autoReconnectPending: boolean;
    receiveFlag: boolean;
    receiveThread: TThreadWrapper;
    callback: PCallbackContext;
    disconnectProbeFlag: boolean;
    disconnectProbeQueue: TBlockingQueue;
    disconnectProbeThread: TThreadWrapper;
    sequenceNumberMutex: TCriticalSection;
    nextSequenceNumber: byte; { protected by sequenceNumberMutex }
    authenticationMutex: TCriticalSection; { protects authentication handshake }
    nextAuthenticationNonce: longword; { protected by authenticationMutex }
    pendingData: TByteArray;
    socketMutex: TCriticalSection;
    socketSendMutex: TCriticalSection;
{$ifdef DELPHI_MACOS}
    socket: longint; { protected by socketMutex }
{$else}
    socket: TSocket; { protected by socketMutex }
{$endif}
    socketID: longword; { protected by socketMutex }
    waiter: TTimedSemaphore;
    enumerateCallback: TIPConnectionNotifyEnumerate;
    connectedCallback: TIPConnectionNotifyConnected;
    disconnectedCallback: TIPConnectionNotifyDisconnected;
    brickd: TBrickDaemon;

    procedure ConnectUnlocked(const isAutoReconnect: boolean);
    procedure DisconnectUnlocked;
    function GetLastSocketErrorNumber: longint;
    function GetLastSocketErrorMessage: string;
    procedure ReceiveLoop(thread: TThreadWrapper; opaque: pointer);
    procedure CallbackLoop(thread: TThreadWrapper; opaque: pointer);
    procedure DisconnectProbeLoop(thread: TThreadWrapper; opaque: pointer);
    procedure HandleDisconnectByPeer(const disconnectReason: byte;
                                     const socketID_: longword;
                                     const disconnectImmediately: boolean);
    procedure HandleResponse(const packet: TByteArray);
    procedure DispatchMeta(const meta: TByteArray);
    procedure DispatchPacket(const packet: TByteArray);
  public
    /// <summary>
    ///  Creates an IP Connection object that can be used to enumerate the
    ///  available devices. It is also required for the constructor of Bricks
    ///  and Bricklets.
    /// </summary>
    constructor Create;

    /// <summary>
    ///  Destroys the IP Connection object. Calls Disconnect internally. The
    ///  connection to the Brick Daemon gets closed and the threads of the
    ///  IP Connection are terminated.
    /// </summary>
    destructor Destroy; override;

    /// <summary>
    ///  Creates a TCP/IP connection to the given *host* and *port*. The host
    ///  and port can point to a Brick Daemon or to a WIFI/Ethernet Extension.
    ///
    ///  Devices can only be controlled when the connection was established
    ///  successfully.
    ///
    ///  Blocks until the connection is established and throws an exception
    ///  if there is no Brick Daemon or WIFI/Ethernet Extension listening at
    ///  the given host and port.
    /// </summary>
    procedure Connect(const host_: string; const port_: word);

    /// <summary>
    ///  Disconnects the TCP/IP connection from the Brick Daemon or the
    ///  WIFI/Ethernet Extension.
    /// </summary>
    procedure Disconnect;

    /// <summary>
    ///  Performs an authentication handshake with the connected Brick Daemon or
    ///  WIFI/Ethernet Extension. If the handshake succeeds the connection switches
    ///  from non-authenticated to authenticated state and communication can
    ///  continue as normal. If the handshake fails then the connection gets closed.
    ///  Authentication can fail if the wrong secret was used or if authentication
    ///  is not enabled at all on the Brick Daemon or the WIFI/Ethernet Extension.
    ///
    ///  For more information about authentication see
    ///  http://www.tinkerforge.com/en/doc/Tutorials/Tutorial_Authentication/Tutorial.html
    /// </summary>
    procedure Authenticate(const secret: string);

    /// <summary>
    ///  Can return the following states:
    ///
    ///  - IPCON_CONNECTION_STATE_DISCONNECTED: No connection is established.
    ///  - IPCON_CONNECTION_STATE_CONNECTED: A connection to the Brick Daemon or
    ///    the WIFI/Ethernet Extension  is established.
    ///  - IPCON_CONNECTION_STATE_PENDING: IP Connection is currently trying to
    ///    connect.
    /// </summary>
    function GetConnectionState: byte;

    /// <summary>
    ///  Enables or disables auto-reconnect. If auto-reconnect is enabled,
    ///  the IP Connection will try to reconnect to the previously given
    ///  host and port, if the connection is lost.
    ///
    ///  Default value is *true*.
    /// </summary>
    procedure SetAutoReconnect(const autoReconnect_: boolean);

    /// <summary>
    ///  Returns *true* if auto-reconnect is enabled, *false* otherwise.
    /// </summary>
    function GetAutoReconnect: boolean;

    /// <summary>
    ///  Sets the timeout in milliseconds for getters and for setters for
    ///  which the response expected flag is activated.
    ///
    ///  Default timeout is 2500.
    /// </summary>
    procedure SetTimeout(const timeout_: longword);

    /// <summary>
    ///  Returns the timeout as set by SetTimeout.
    /// </summary>
    function GetTimeout: longword;

    /// <summary>
    ///  Broadcasts an enumerate request. All devices will respond with an
    ///  enumerate callback.
    /// </summary>
    procedure Enumerate;

    /// <summary>
    ///  Stops the current thread until Unwait is called.
    ///
    ///  This is useful if you rely solely on callbacks for events, if you want
    ///  to wait for a specific callback or if the IP Connection was created in
    ///  a thread.
    ///
    ///  Wait and Unwait act in the same way as "acquire" and "release" of a
    ///  semaphore.
    /// </summary>
    procedure Wait;

    /// <summary>
    ///  Unwaits the thread previously stopped by Wait.
    ///
    ///  Wait and Unwait act in the same way as "acquire" and "release" of
    ///  a semaphore.
    /// </summary>
    procedure Unwait;

    property OnEnumerate: TIPConnectionNotifyEnumerate read enumerateCallback write enumerateCallback;
    property OnConnected: TIPConnectionNotifyConnected read connectedCallback write connectedCallback;
    property OnDisconnected: TIPConnectionNotifyDisconnected read disconnectedCallback write disconnectedCallback;

    { Internal }
    function IsConnected: boolean;
    function CreateRequestPacket(const device: TDevice; const functionID: byte; const len: byte): TByteArray;
    procedure SendRequest(const request: TByteArray);
  end;

  function GetUIDFromData(const data: TByteArray): longword;
  function GetLengthFromData(const data: TByteArray): byte;
  function GetFunctionIDFromData(const data: TByteArray): byte;
  function GetSequenceNumberFromData(const data: TByteArray): byte;
  function GetResponseExpectedFromData(const data: TByteArray): boolean;
  function GetErrorCodeFromData(const data: TByteArray): byte;

implementation

{$ifdef MSWINDOWS}

function CryptAcquireContextA(phProv: pointer; pszContainer: LPCSTR; pszProvider: LPCSTR; dwProvType: DWORD; dwFlags: DWORD): BOOL; stdcall; external 'advapi32.dll' name 'CryptAcquireContextA';
function CryptReleaseContext(hProv: pointer; dwFlags: DWORD): BOOL; stdcall; external 'advapi32.dll' name 'CryptReleaseContext';
function CryptGenRandom(hProv: ULONG; dwLen: DWORD; pbBuffer: PBYTE): BOOL; stdcall; external 'advapi32.dll' name 'CryptGenRandom';

{$else}

function ReadUInt32(const filename: string): longword;
var fh: File; bytes: TByteArray; count: longint;
begin
  SetLength(bytes, 4);
  count := 0;
  AssignFile(fh, filename);
  try
    Reset(fh, 1);
    BlockRead(fh, bytes, 4, count);
  finally
    CloseFile(fh);
  end;
  if (count <> 4) then begin
    raise Exception.Create('Insufficent number of random bytes read');
  end;
  result := LEConvertUInt32From(0, bytes);
end;

{$endif}

function GetRandomUInt32: longword;
var success: boolean; days: double; seconds, microseconds, pid: longword;
{$ifdef MSWINDOWS}
    provider: ULONG; bytes: TByteArray;
{$endif}
begin
  result := 0;
  success := false;
{$ifdef MSWINDOWS}
  provider := 0;
  if (CryptAcquireContextA(@provider, nil, nil, 1, $F0000040)) then begin
    SetLength(bytes, 4);
    if (CryptGenRandom(provider, 4, @bytes[0])) then begin
      result := LEConvertUInt32From(0, bytes);
      success := true;
    end;
    CryptReleaseContext(@provider, 0);
  end;
{$else}
  try
    { Try the non-blocking /dev/urandom first, as there seems to be no direct
      way to do a non-blocking read from Delphi. }
    result := ReadUInt32('/dev/urandom');
    success := true;
  except
  end;
  if (not success) then begin
    try
      { If /dev/urandom is not available fallback to /dev/random which might
        block on read }
      result := ReadUInt32('/dev/random');
      success := true;
    except
    end;
  end;
{$endif}
  if (not success) then begin
    days := Now;
    seconds := Trunc(days * 86400);
    microseconds := Trunc(Frac(days * 86400) * 1000000);
{$ifdef FPC}
    pid := GetProcessID;
{$else}
 {$ifdef MSWINDOWS}
    pid := Windows.GetCurrentProcessId;
 {$else}
    { FIXME: no clue how to get PID }
    pid := 0;
 {$endif}
{$endif}
    result := ((seconds shl 26) or (seconds shr 6)) + microseconds + pid; { overflow is intended }
  end;
end;

function HMACSHA1(const secret: TByteArray; const data: TByteArray): TSHA1Digest;
var preparedSecret: TByteArray; sha1: TSHA1; i: longint;
    ipad, opad: array [0..63] of byte; digest: TSHA1Digest;
begin
  if Length(secret) > 64 then begin
    SHA1Init(sha1);
    SHA1Update(sha1, secret);
    digest := SHA1Final(sha1);
    SetLength(preparedSecret, 64);
    Move(digest, preparedSecret, 64);
  end
  else begin
    preparedSecret := secret;
  end;
  for i := 0 to 63 do begin
    ipad[i] := $36;
    opad[i] := $5C;
  end;
  for i := 0 to (Length(preparedSecret) - 1) do begin
    ipad[i] := preparedSecret[i] xor ipad[i];
    opad[i] := preparedSecret[i] xor opad[i];
  end;
  SHA1Init(sha1);
  SHA1Update(sha1, ipad);
  SHA1Update(sha1, data);
  digest := SHA1Final(sha1);
  SHA1Init(sha1);
  SHA1Update(sha1, opad);
  SHA1Update(sha1, digest);
  result := SHA1Final(sha1);
end;

{ TThreadWrapper }
constructor TThreadWrapper.Create(const proc_: TThreadProcedure; opaque_: pointer);
begin
  proc := proc_;
  opaque := opaque_;
  inherited Create(false);
end;

procedure TThreadWrapper.Execute;
begin
  proc(self, opaque);
end;

function TThreadWrapper.IsCurrent: boolean;
begin
{$ifdef FPC}
  result := GetCurrentThreadId = ThreadID;
{$else}
 {$ifdef MSWINDOWS}
  result := Windows.GetCurrentThreadId = ThreadID;
 {$else}
  result := CurrentThread.ThreadID = ThreadID;
 {$endif}
{$endif}
end;

{ TIPConnection }
constructor TIPConnection.Create;
begin
  host := '';
  port := 0;
  timeout := 2500;
  autoReconnect := true;
  autoReconnectAllowed := false;
  autoReconnectPending := false;
  receiveFlag := false;
  receiveThread := nil;
  callback := nil;
  disconnectProbeFlag := false;
  disconnectProbeQueue := nil;
  disconnectProbeThread := nil;
  sequenceNumberMutex := TCriticalSection.Create;
  nextSequenceNumber := 0;
  authenticationMutex := TCriticalSection.Create;
  nextAuthenticationNonce := 0;
  SetLength(pendingData, 0);
  devices := TDeviceTable.Create;
  socketMutex := TCriticalSection.Create;
  socketSendMutex := TCriticalSection.Create;
  socket := INVALID_SOCKET;
  waiter := TTimedSemaphore.Create;
  brickd := TBrickDaemon.Create('2', self);
end;

destructor TIPConnection.Destroy;
begin
  if (IsConnected) then begin
    Disconnect;
  end;
  authenticationMutex.Destroy;
  sequenceNumberMutex.Destroy;
  devices.Destroy;
  socketMutex.Destroy;
  socketSendMutex.Destroy;
  waiter.Destroy;
  inherited Destroy;
end;

procedure TIPConnection.Connect(const host_: string; const port_: word);
begin
  socketMutex.Acquire;
  try
    if (IsConnected) then begin
      raise EAlreadyConnectedException.Create('Already connected to ' + host + ':' + IntToStr(port));
    end;
    host := host_;
    port := port_;
    ConnectUnlocked(false);
  finally
    socketMutex.Release;
  end;
end;

procedure TIPConnection.Disconnect;
var callback_: PCallbackContext; meta: TByteArray;
begin
  callback_ := nil;
  socketMutex.Acquire;
  try
    autoReconnectAllowed := false;
    if (autoReconnectPending) then begin
      { Abort pending auto-reconnect }
      autoReconnectPending := false;
    end
    else begin
      if (not IsConnected) then begin
        raise ENotConnectedException.Create('Not connected');
      end;
      DisconnectUnlocked;
      SetLength(pendingData, 0);
    end;
    { Destroy callback thread }
    callback_ := callback;
    callback := nil;
  finally
    socketMutex.Release;
  end;
  if (callback_ <> nil) then begin
    { Do this outside of socketMutex to allow calling (dis-)connect from
      the callbacks while blocking on the WaitFor call here }
    SetLength(meta, 2);
    meta[0] := IPCON_CALLBACK_DISCONNECTED;
    meta[1] := IPCON_DISCONNECT_REASON_REQUEST;
    callback_^.queue.Enqueue(IPCON_QUEUE_KIND_META, meta);
    if (not callback_^.thread.IsCurrent) then begin
      callback_^.queue.Enqueue(IPCON_QUEUE_KIND_EXIT, nil);
      callback_^.thread.WaitFor;
      callback_^.thread.Destroy;
    end
    else begin
      callback_^.queue.Enqueue(IPCON_QUEUE_KIND_DESTROY_AND_EXIT, nil);
    end;
  end;
end;

procedure TIPConnection.Authenticate(const secret: string);
var serverNonce, clientNonce: TArray0To3OfUInt8; i: longint;
    secretBytes, clientNonceBytes, data: TByteArray;
    digest: TSHA1Digest;
begin
  authenticationMutex.Acquire;
  try
    if (nextAuthenticationNonce = 0) then begin
      nextAuthenticationNonce := GetRandomUInt32;
    end;
    serverNonce := brickd.GetAuthenticationNonce;
    SetLength(clientNonceBytes, 4);
    LEConvertUInt32To(nextAuthenticationNonce, 0, clientNonceBytes);
    Inc(nextAuthenticationNonce);
    SetLength(data, 8);
    for i := 0 to 3 do begin
      data[i] := serverNonce[i];
    end;
    for i := 0 to 3 do begin
      data[4 + i] := clientNonceBytes[i];
      clientNonce[i] := clientNonceBytes[i];
    end;
    SetLength(secretBytes, Length(secret));
    LEConvertStringTo(secret, 0, Length(secret), secretBytes);
    digest := HMACSHA1(secretBytes, data);
    brickd.Authenticate(clientNonce, TArray0To19OfUInt8(digest));
  finally
    authenticationMutex.Release;
  end;
end;

function TIPConnection.GetConnectionState: byte;
begin
  if (IsConnected) then begin
    result := IPCON_CONNECTION_STATE_CONNECTED;
  end
  else if (autoReconnectPending) then begin
    result := IPCON_CONNECTION_STATE_PENDING;
  end
  else begin
    result := IPCON_CONNECTION_STATE_DISCONNECTED;
  end;
end;

procedure TIPConnection.SetAutoReconnect(const autoReconnect_: boolean);
begin
  autoReconnect := autoReconnect_;
  if (not autoReconnect) then begin
    { Abort potentially pending auto-reconnect }
    autoReconnectAllowed := false;
  end;
end;

function TIPConnection.GetAutoReconnect: boolean;
begin
  result := autoReconnect;
end;

procedure TIPConnection.SetTimeout(const timeout_: longword);
begin
  timeout := timeout_;
end;

function TIPConnection.GetTimeout: longword;
begin
  result := timeout;
end;

procedure TIPConnection.Enumerate;
var request: TByteArray;
begin
  request := CreateRequestPacket(nil, IPCON_FUNCTION_ENUMERATE, 8);
  SendRequest(request);
end;

procedure TIPConnection.Wait;
begin
  waiter.Acquire(-1);
end;

procedure TIPConnection.Unwait;
begin
  waiter.Release;
end;

{ NOTE: Assumes that socketMutex is locked }
procedure TIPConnection.ConnectUnlocked(const isAutoReconnect: boolean);
var
{$ifndef FPC}
 {$ifdef MSWINDOWS}
    data: WSAData;
 {$endif}
{$endif}
    nodelay: longint;
{$ifdef DELPHI_MACOS}
    hints: addrinfo;
    entry: PAddrInfo;
    error: longint;
{$else}
    entry: PHostEnt;
{$endif}
{$ifdef FPC}
    address: TInetSockAddr;
{$else}
 {$ifdef DELPHI_MACOS}
    address: sockaddr_in;
 {$else}
    address: TSockAddrIn;
 {$endif}
{$endif}
{$ifdef DELPHI_MACOS}
    resolved: in_addr;
{$else}
    resolved: TInAddr;
{$endif}
    connectReason: word;
    meta: TByteArray;
begin
  { Create callback queue and thread }
  if (callback = nil) then begin
    New(callback);
    callback^.mutex := TCriticalSection.Create;
    callback^.packetDispatchAllowed := false;
    callback^.queue := TBlockingQueue.Create;
    callback^.thread := TThreadWrapper.Create({$ifdef FPC}@{$endif}self.CallbackLoop,
                                              callback);
  end;
  { Create and connect socket }
{$ifndef FPC}
 {$ifdef MSWINDOWS}
  if (WSAStartup(MakeWord(2, 2), data) <> 0) then begin
    raise Exception.Create('Could not initialize Windows Sockets 2.2: ' + GetLastSocketErrorMessage);
  end;
 {$endif}
{$endif}
{$ifdef FPC}
  socket := fpsocket(AF_INET, SOCK_STREAM, 0);
  if (socket < 0) then begin
{$else}
 {$ifdef DELPHI_MACOS}
  socket := Posix.SysSocket.socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
 {$else}
  socket := WinSock.socket(AF_INET, SOCK_STREAM, 0);
 {$endif}
  if (socket = INVALID_SOCKET) then begin
{$endif}
    raise Exception.Create('Could not create socket: ' + GetLastSocketErrorMessage);
  end;
  nodelay := 1;
{$ifdef FPC}
  if (fpsetsockopt(socket, IPPROTO_TCP, TCP_NODELAY, @nodelay, sizeof(nodelay)) < 0) then begin
{$else}
 {$ifdef DELPHI_MACOS}
  if (setsockopt(socket, IPPROTO_TCP, TCP_NODELAY, nodelay, sizeof(nodelay)) < 0) then begin
 {$else}
  if (setsockopt(socket, IPPROTO_TCP, TCP_NODELAY, @nodelay, sizeof(nodelay)) = SOCKET_ERROR) then begin
 {$endif}
{$endif}
    raise Exception.Create('Could not set TCP_NODELAY socket option: ' + GetLastSocketErrorMessage);
  end;
{$ifdef DELPHI_MACOS}
  FillChar(hints, SizeOf(hints), 0);
  hints.ai_flags := AI_PASSIVE;
  hints.ai_family := AF_UNSPEC;
  hints.ai_socktype := SOCK_STREAM;
  error := getaddrinfo(PAnsiChar(AnsiString(host)), nil, hints, entry);
  if (error <> 0) then begin
    Posix.Unistd.__close(socket);
    socket := INVALID_SOCKET;
    raise Exception.Create('Could not resolve host ' + host + ': ' + string(gai_strerror(error)));
  end;
  resolved := sockaddr_in(entry.ai_addr^).sin_addr;
  freeaddrinfo(entry^);
{$else}
  entry := gethostbyname(PAnsiChar(AnsiString(host)));
  if (entry = nil) then begin
    closesocket(socket);
    socket := INVALID_SOCKET;
    raise Exception.Create('Could not resolve host: ' + host);
  end;
  resolved.s_addr := longint(pointer(entry^.h_addr_list^)^);
{$endif}
  address.sin_family := AF_INET;
  address.sin_port := htons(port);
  address.sin_addr := resolved;
{$ifdef FPC}
  if (fpconnect(socket, @address, sizeof(address)) < 0) then begin
{$else}
 {$ifdef DELPHI_MACOS}
  if (Posix.SysSocket.connect(socket, sockaddr(address), sizeof(address)) < 0) then begin
 {$else}
  if (WinSock.connect(socket, address, sizeof(address)) = SOCKET_ERROR) then begin
 {$endif}
{$endif}
{$ifdef DELPHI_MACOS}
    Posix.Unistd.__close(socket);
{$else}
    closesocket(socket);
{$endif}
    socket := INVALID_SOCKET;
    raise Exception.Create('Could not connect socket: ' + GetLastSocketErrorMessage);
  end;
  socketID := socketID + 1;
  { Create disconnect probe thread }
  disconnectProbeFlag := true;
  disconnectProbeQueue := TBlockingQueue.Create;
  disconnectProbeThread := TThreadWrapper.Create({$ifdef FPC}@{$endif}self.DisconnectProbeLoop, nil);
  { Create receive thread }
  callback^.packetDispatchAllowed := true;
  receiveFlag := true;
  receiveThread := TThreadWrapper.Create({$ifdef FPC}@{$endif}self.ReceiveLoop, nil);
  autoReconnectAllowed := false;
  autoReconnectPending := false;
  { Trigger connected callback }
  if (isAutoReconnect) then begin
    connectReason := IPCON_CONNECT_REASON_AUTO_RECONNECT;
  end
  else begin
    connectReason := IPCON_CONNECT_REASON_REQUEST;
  end;
  SetLength(meta, 2);
  meta[0] := IPCON_CALLBACK_CONNECTED;
  meta[1] := connectReason;
  callback^.queue.Enqueue(IPCON_QUEUE_KIND_META, meta);
end;

{ NOTE: Assumes that socketMutex is locked }
procedure TIPConnection.DisconnectUnlocked;
begin
  { Destroy disconnect probe thread }
  disconnectProbeQueue.Enqueue(0, nil);
  disconnectProbeThread.WaitFor;
  disconnectProbeThread.Destroy;
  disconnectProbeThread := nil;
  disconnectProbeQueue.Destroy;
  disconnectProbeQueue := nil;
  { Stop dispatching packet callbacks before ending the receive
    thread to avoid timeout exceptions due to callback function
    trying to call getters }
  if (not callback^.thread.IsCurrent) then begin
    { FIXME: Cannot lock callback mutex here because this can
             deadlock due to an ordering problem with the socket mutex }
    //callback^.mutex.Acquire;
    //try
      callback^.packetDispatchAllowed := false;
    //finally
    //  callback^.mutex.Release;
    //end;
  end
  else begin
    callback^.packetDispatchAllowed := false;
  end;
  { Destroy receive thread }
  receiveFlag := false;
{$ifdef FPC}
  fpshutdown(socket, 2);
{$else}
 {$ifdef DELPHI_MACOS}
  shutdown(socket, SHUT_RDWR);
 {$else}
  shutdown(socket, SD_BOTH);
 {$endif}
{$endif}
  if (not receiveThread.IsCurrent) then begin
    receiveThread.WaitFor;
  end;
  receiveThread.Destroy;
  receiveThread := nil;
  { Destroy socket }
{$ifdef DELPHI_MACOS}
    Posix.Unistd.__close(socket);
{$else}
    closesocket(socket);
{$endif}
  socket := INVALID_SOCKET;
end;

function TIPConnection.GetLastSocketErrorNumber: longint;
begin
{$ifdef FPC}
  result := socketerror;
{$else}
 {$ifdef DELPHI_MACOS}
  result := errno;
 {$else}
  result := WSAGetLastError;
 {$endif}
{$endif}
end;

function TIPConnection.GetLastSocketErrorMessage: string;
begin
{$ifdef FPC}
 {$ifdef UNIX}
  result := strerror(socketerror);
 {$else}
  result := SysErrorMessage(socketerror);
 {$endif}
{$else}
 {$ifdef DELPHI_MACOS}
  result := string(strerror(errno));
 {$else}
  result := SysErrorMessage(WSAGetLastError);
 {$endif}
{$endif}
end;

procedure TIPConnection.ReceiveLoop(thread: TThreadWrapper; opaque: pointer);
var socketID_: longword; data: array [0..8191] of byte;
    len, pendingLen, remainingLen: longint; packet: TByteArray;
    disconnectReason: byte;
begin
  socketID_ := socketID;
  disconnectReason := IPCON_DISCONNECT_REASON_ERROR;
  while (receiveFlag) do begin
{$ifdef FPC}
    len := fprecv(socket, @data[0], Length(data), 0);
{$else}
 {$ifdef DELPHI_MACOS}
    len := recv(socket, data, Length(data), 0);
 {$else}
    len := WinSock.Recv(socket, data, Length(data), 0);
 {$endif}
{$endif}
    if (not receiveFlag) then begin
      exit;
    end;
    if ((len < 0) or (len = 0)) then begin
      if (len < 0) then begin
        if (GetLastSocketErrorNumber = ESysEINTR) then begin
          continue;
        end;
        disconnectReason := IPCON_DISCONNECT_REASON_ERROR;
      end
      else begin
        disconnectReason := IPCON_DISCONNECT_REASON_SHUTDOWN;
      end;
      HandleDisconnectByPeer(disconnectReason, socketID_, false);
      exit;
    end;
    pendingLen := Length(pendingData);
    SetLength(pendingData, pendingLen + len);
    Move(data[0], pendingData[pendingLen], len);
    while (receiveFlag) do begin
      if (Length(pendingData) < 8) then begin
        { Wait for complete header }
        break;
      end;
      len := GetLengthFromData(pendingData);
      if (Length(pendingData) < len) then begin
        { Wait for complete packet }
        break;
      end;
      SetLength(packet, len);
      Move(pendingData[0], packet[0], len);
      remainingLen := Length(pendingData) - len;
      if (remainingLen > 0) then begin
        { Don't call Move with remainingLen of 0, because in this case len is
          outside the bounds of pendingData. This would trigger an ERangeCheck
          error at runtime }
        Move(pendingData[len], pendingData[0], remainingLen);
      end;
      SetLength(pendingData, remainingLen);
      HandleResponse(packet);
    end;
  end;
end;

procedure TIPConnection.CallbackLoop(thread: TThreadWrapper; opaque: pointer);
var callback_: PCallbackContext; kind: byte; data: TByteArray;
begin
  callback_ := PCallbackContext(opaque);
  while (true) do begin
    SetLength(data, 0);
    if (not callback_^.queue.Dequeue(kind, data, -1)) then begin
      break;
    end;
    if (kind = IPCON_QUEUE_KIND_EXIT) then begin
      break;
    end
    else if (kind = IPCON_QUEUE_KIND_DESTROY_AND_EXIT) then begin
      thread.Destroy;
      break;
    end;
    { FIXME: Cannot lock callback mutex here because this can
             deadlock due to an ordering problem with the socket mutex }
    //callback_^.mutex.Acquire;
    //try
      if (kind = IPCON_QUEUE_KIND_META) then begin
        DispatchMeta(data);
      end
      else if (kind = IPCON_QUEUE_KIND_PACKET) then begin
        { Don't dispatch callbacks when the receive thread isn't running }
        if (callback_^.packetDispatchAllowed) then begin
          DispatchPacket(data);
        end;
      end;
    //finally
    //  callback_.mutex.Release;
    //end;
  end;
  callback_^.queue.Destroy;
  callback_^.mutex.Destroy;
  Dispose(callback_);
end;

{ NOTE: The disconnect probe loop is not allowed to hold the socketMutex at any
        time because it is created and joined while the socketMutex is locked }
procedure TIPConnection.DisconnectProbeLoop(thread: TThreadWrapper; opaque: pointer);
var kind: byte; data, request: TByteArray; error: boolean;
begin
  SetLength(data, 0);
  request := CreateRequestPacket(nil, IPCON_FUNCTION_DISCONNECT_PROBE, 8);
  while (not disconnectProbeQueue.Dequeue(kind, data, IPCON_DISCONNECT_PROBE_INTERVAL)) do begin
    if (disconnectProbeFlag) then begin
      socketSendMutex.Acquire;
      try
{$ifdef FPC}
        error := fpsend(socket, @request[0], Length(request), 0) < 0;
{$else}
 {$ifdef DELPHI_MACOS}
        error := send(socket, request[0], Length(request), 0) < 0;
 {$else}
        error := WinSock.Send(socket, request[0], Length(request), 0) = SOCKET_ERROR;
 {$endif}
{$endif}
      finally
        socketSendMutex.Release;
      end;
      if (error) then begin
        HandleDisconnectByPeer(IPCON_DISCONNECT_REASON_ERROR, socketID, false);
        break;
      end;
    end
    else begin
      disconnectProbeFlag := true;
    end;
  end;
end;

{ NOTE: Assumes that socketMutex is locked if disconnectImmediately is true }
procedure TIPConnection.HandleDisconnectByPeer(const disconnectReason: byte;
                                               const socketID_: longword;
                                               const disconnectImmediately: boolean);
var meta: TByteArray;
begin
  autoReconnectAllowed := true;
  if (disconnectImmediately) then begin
    DisconnectUnlocked;
  end;
  SetLength(meta, 6);
  meta[0] := IPCON_CALLBACK_DISCONNECTED;
  meta[1] := disconnectReason;
  LEConvertUInt32To(socketID_, 2, meta);
  callback^.queue.Enqueue(IPCON_QUEUE_KIND_META, meta);
end;

procedure TIPConnection.HandleResponse(const packet: TByteArray);
var sequenceNumber, functionID: byte; device: TDevice;
begin
  disconnectProbeFlag := false;
  functionID := GetFunctionIDFromData(packet);
  sequenceNumber := GetSequenceNumberFromData(packet);
  if ((sequenceNumber = 0) and (functionID = IPCON_CALLBACK_ENUMERATE)) then begin
    if (Assigned(enumerateCallback)) then begin
      callback^.queue.Enqueue(IPCON_QUEUE_KIND_PACKET, packet);
    end;
    exit;
  end;
  device := devices.Get(GetUIDFromData(packet));
  if (device = nil) then begin
    { Response from an unknown device, ignoring it }
    exit;
  end;
  if (sequenceNumber = 0) then begin
    if (Assigned(device.callbackWrappers[functionID])) then begin
      callback^.queue.Enqueue(IPCON_QUEUE_KIND_PACKET, packet);
    end;
    exit;
  end;
  if ((device.expectedResponseFunctionID = functionID) and
      (device.expectedResponseSequenceNumber = sequenceNumber)) then begin
    device.responseQueue.Enqueue(0, packet);
    exit;
  end;
end;

procedure TIPConnection.DispatchMeta(const meta: TByteArray);
var retry: boolean;
begin
  if (meta[0] = IPCON_CALLBACK_CONNECTED) then begin
    if (Assigned(connectedCallback)) then begin
      try
        connectedCallback(self, meta[1]);
      except
        { Ignore exceptions in user code }
      end;
    end;
  end
  else if (meta[0] = IPCON_CALLBACK_DISCONNECTED) then begin
    { Need to do this here, the receive loop is not allowed to hold the socket
      mutex because this could cause a deadlock with a concurrent call to the
      (dis-)connect function }
    if (meta[1] <> IPCON_DISCONNECT_REASON_REQUEST) then begin
      socketMutex.Acquire;
      try
        { Don't close the socket if it got disconnected or reconnected
          in the meantime }
        if (IsConnected and (socketID = LEConvertUInt32From(2, meta))) then begin
          { Destroy disconnect probe thread }
          disconnectProbeQueue.Enqueue(0, nil);
          disconnectProbeThread.WaitFor;
          disconnectProbeThread.Destroy;
          disconnectProbeThread := nil;
          disconnectProbeQueue.Destroy;
          disconnectProbeQueue := nil;
          { Destroy socket }
{$ifdef DELPHI_MACOS}
          Posix.Unistd.__close(socket);
{$else}
          closesocket(socket);
{$endif}
          socket := INVALID_SOCKET;
        end;
      finally
        socketMutex.Release;
      end;
    end;
    { FIXME: Wait a moment here, otherwise the next connect attempt will
      succeed, even if there is no open server socket. The first receive will
      then fail directly }
    Sleep(100);
    if (Assigned(disconnectedCallback)) then begin
      try
        disconnectedCallback(self, meta[1]);
      except
        { Ignore exceptions in user code }
      end;
    end;
    if ((meta[1] <> IPCON_DISCONNECT_REASON_REQUEST) and autoReconnect and
        autoReconnectAllowed) then begin
      autoReconnectPending := true;
      retry := true;
      { Block here until reconnect. this is okay, there is no callback to
        deliver when there is no connection }
      while (retry) do begin
        retry := false;
        socketMutex.Acquire;
        try
          if (autoReconnectAllowed and (not IsConnected)) then begin
            try
              ConnectUnlocked(true);
            except
              retry := true;
            end;
          end
          else begin
            autoReconnectPending := false;
          end;
        finally
          socketMutex.Release;
        end;
        if (retry) then begin
          { Wait a moment to give another thread a chance to interrupt the
            auto-reconnect }
          Sleep(100);
        end;
      end;
    end;
  end;
end;

procedure TIPConnection.DispatchPacket(const packet: TByteArray);
var functionID: byte; uid, connectedUid: string; position: char;
    hardwareVersion, firmwareVersion: TVersionNumber;
    deviceIdentifier: word; enumerationType: byte;
    device: TDevice; callbackWrapper: TCallbackWrapper;
begin
  functionID := GetFunctionIDFromData(packet);
  if (functionID = IPCON_CALLBACK_ENUMERATE) then begin
    if (Assigned(enumerateCallback)) then begin
      uid := LEConvertStringFrom(8, 8, packet);
      connectedUid := LEConvertStringFrom(16, 8, packet);
      position := LEConvertCharFrom(24, packet);
      hardwareVersion[0] := LEConvertUInt8From(25, packet);
      hardwareVersion[1] := LEConvertUInt8From(26, packet);
      hardwareVersion[2] := LEConvertUInt8From(27, packet);
      firmwareVersion[0] := LEConvertUInt8From(28, packet);
      firmwareVersion[1] := LEConvertUInt8From(29, packet);
      firmwareVersion[2] := LEConvertUInt8From(30, packet);
      deviceIdentifier := LEConvertUInt16From(31, packet);
      enumerationType := LEConvertUInt8From(33, packet);
      try
        enumerateCallback(self, uid, connectedUid, position,
                          hardwareVersion, firmwareVersion,
                          deviceIdentifier, enumerationType);
      except
        { Ignore exceptions in user code }
      end;
    end
  end
  else begin
    device := devices.Get(GetUIDFromData(packet));
    if (device = nil) then begin
      exit;
    end;
    callbackWrapper := device.callbackWrappers[functionID];
    if (Assigned(callbackWrapper)) then begin
      try
        callbackWrapper(packet);
      except
        { Ignore exceptions in user code }
      end;
    end;
  end;
end;

function TIPConnection.IsConnected: boolean;
begin
  result := socket <> INVALID_SOCKET;
end;

function TIPConnection.CreateRequestPacket(const device: TDevice; const functionID: byte; const len: byte): TByteArray;
var sequenceNumber, responseExpected: byte;
begin
  SetLength(result, len);
  FillChar(result[0], len, 0);
  sequenceNumberMutex.Acquire;
  try
    sequenceNumber := nextSequenceNumber + 1;
    nextSequenceNumber := sequenceNumber mod 15;
  finally
    sequenceNumberMutex.Release;
  end;
  responseExpected := 0;
  if (device <> nil) then begin
    LEConvertUInt32To(device.uid_, 0, result);
    if (device.GetResponseExpected(functionID)) then begin
      responseExpected := 1;
    end;
  end;
  result[4] := len;
  result[5] := functionID;
  result[6] := (sequenceNumber shl 4) or (responseExpected shl 3);
end;

procedure TIPConnection.SendRequest(const request: TByteArray);
var error: boolean;
begin
  socketMutex.Acquire;
  try
    if (not IsConnected) then begin
      raise ENotConnectedException.Create('Not connected');
    end;
    socketSendMutex.Acquire;
    try
{$ifdef FPC}
      error := fpsend(socket, @request[0], Length(request), 0) < 0;
{$else}
 {$ifdef DELPHI_MACOS}
      error := send(socket, request[0], Length(request), 0) < 0;
 {$else}
      error := WinSock.Send(socket, request[0], Length(request), 0) = SOCKET_ERROR;
 {$endif}
{$endif}
    finally
      socketSendMutex.Release;
    end;
    if (error) then begin
      HandleDisconnectByPeer(IPCON_DISCONNECT_REASON_ERROR, 0, true);
      raise ENotConnectedException.Create('Not connected');
    end;
    disconnectProbeFlag := false;
  finally
    socketMutex.Release;
  end;
end;

function GetUIDFromData(const data: TByteArray): longword;
begin
  result := LEConvertUInt32From(0, data);
end;

function GetLengthFromData(const data: TByteArray): byte;
begin
  result := data[4];
end;

function GetFunctionIDFromData(const data: TByteArray): byte;
begin
  result := data[5];
end;

function GetSequenceNumberFromData(const data: TByteArray): byte;
begin
  result := (data[6] shr 4) and $0F;
end;

function GetResponseExpectedFromData(const data: TByteArray): boolean;
begin
  if (((data[6] shr 3) and $01) = 1) then begin
    result := true;
  end
  else begin
    result := false;
  end;
end;

function GetErrorCodeFromData(const data: TByteArray): byte;
begin
  result := (data[7] shr 6) and $03;
end;

end.
