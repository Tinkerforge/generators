unit IPConnection;

{$ifdef FPC}{$mode OBJFPC}{$H+}{$endif}

interface

uses
  {$ifdef FPC}
   {$ifdef UNIX}CThreads, Errors, NetDB, BaseUnix, {$else}WinSock,{$endif}
  {$else}
   {$ifdef MSWINDOWS}Windows, WinSock,{$endif}
  {$endif}
  Classes, Sockets, SyncObjs, SysUtils, Base58, LEConverter, BlockingQueue, Device, TimedSemaphore;

const
  IPCON_FUNCTION_ENUMERATE = 254;

  IPCON_CALLBACK_ENUMERATE = 253;
  IPCON_CALLBACK_CONNECTED = 0;
  IPCON_CALLBACK_DISCONNECTED = 1;

  IPCON_QUEUE_KIND_EXIT = 0;
  IPCON_QUEUE_KIND_DESTROY_AND_EXIT = 1;
  IPCON_QUEUE_KIND_META = 2;
  IPCON_QUEUE_KIND_PACKET = 3;

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
  ESysEINTR = WSAEINTR;
{$endif}

type
  { TWrapperThread }
  TWrapperThread = class;
  TThreadProcedure = procedure(thread: TWrapperThread; opaque: TObject) of object;
  TWrapperThread = class(TThread)
  private
    proc: TThreadProcedure;
    opaque: TObject;
  public
    constructor Create(const proc_: TThreadProcedure; opaque_: TObject);
    procedure Execute; override;
    function IsCurrent: boolean;
  end;

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
    socketMutex: TCriticalSection;
    timeout: longint;
    devices: TDeviceTable;
  private
    host: string;
    port: word;
    autoReconnect: boolean;
    autoReconnectAllowed: boolean;
    autoReconnectPending: boolean;
    receiveFlag: boolean;
    receiveThread: TWrapperThread;
    callbackQueue: TBlockingQueue;
    callbackThread: TWrapperThread;
    sequenceNumberMutex: TCriticalSection;
    nextSequenceNumber: byte;
    pendingData: TByteArray;
    socket: TSocket;
    waiter: TTimedSemaphore;
    enumerateCallback: TIPConnectionNotifyEnumerate;
    connectedCallback: TIPConnectionNotifyConnected;
    disconnectedCallback: TIPConnectionNotifyDisconnected;

    procedure ConnectUnlocked(const isAutoReconnect: boolean);
    function GetLastSocketError: string;
    procedure ReceiveLoop(thread: TWrapperThread; opaque: TObject);
    procedure CallbackLoop(thread: TWrapperThread; opaque: TObject);
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
    function CreatePacket(const device: TDevice; const functionID: byte; const len: byte): TByteArray;
    procedure Send(const data: TByteArray);
  end;

  function GetUIDFromData(const data: TByteArray): longword;
  function GetLengthFromData(const data: TByteArray): byte;
  function GetFunctionIDFromData(const data: TByteArray): byte;
  function GetSequenceNumberFromData(const data: TByteArray): byte;
  function GetResponseExpectedFromData(const data: TByteArray): boolean;
  function GetErrorCodeFromData(const data: TByteArray): byte;

implementation

{ TWrapperThread }
constructor TWrapperThread.Create(const proc_: TThreadProcedure; opaque_: TObject);
begin
  proc := proc_;
  opaque := opaque_;
  inherited Create(false);
end;

procedure TWrapperThread.Execute;
begin
  proc(self, opaque);
end;

function TWrapperThread.IsCurrent: boolean;
begin
{$ifdef FPC}
  result := GetCurrentThreadId = ThreadID;
{$else}
  result := Windows.GetCurrentThreadId = ThreadID;
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
  callbackQueue := nil;
  callbackThread := nil;
  sequenceNumberMutex := TCriticalSection.Create;
  nextSequenceNumber := 0;
  SetLength(pendingData, 0);
  devices := TDeviceTable.Create;
  socketMutex := TCriticalSection.Create;
  socket := INVALID_SOCKET;
  waiter := TTimedSemaphore.Create;
end;

destructor TIPConnection.Destroy;
begin
  if (IsConnected) then begin
    Disconnect;
  end;
  sequenceNumberMutex.Destroy;
  devices.Destroy;
  socketMutex.Destroy;
  waiter.Destroy;
  inherited Destroy;
end;

procedure TIPConnection.Connect(const host_: string; const port_: word);
begin
  socketMutex.Acquire;
  try
    if (IsConnected) then begin
      raise Exception.Create('Already connected');
    end;
    host := host_;
    port := port_;
    ConnectUnlocked(false);
  finally
    socketMutex.Release;
  end;
end;

procedure TIPConnection.Disconnect;
var callbackQueue_: TBlockingQueue; callbackThread_: TWrapperThread; meta: TByteArray;
begin
  callbackQueue_ := nil;
  callbackThread_ := nil;
  socketMutex.Acquire;
  try
    autoReconnectAllowed := false;
    if (autoReconnectPending) then begin
      { Abort pending auto-reconnect }
      autoReconnectPending := false;
    end
    else begin
      if (not IsConnected) then begin
        raise Exception.Create('Not connected');
      end;
      { Destroy receive thread }
      receiveFlag := false;
{$ifdef FPC}
      fpshutdown(socket, 2);
{$else}
      shutdown(socket, SD_BOTH);
{$endif}
      if (not receiveThread.IsCurrent) then begin
        receiveThread.WaitFor;
      end;
      receiveThread.Destroy;
      receiveThread := nil;
      { Destroy socket }
      closesocket(socket);
      socket := INVALID_SOCKET;
    end;
    { Destroy callback thread }
    callbackQueue_ := callbackQueue;
    callbackThread_ := callbackThread;
    callbackQueue := nil;
    callbackThread := nil;
  finally
    socketMutex.Release;
  end;
  if ((callbackQueue_ <> nil) and (callbackThread_ <> nil)) then begin
    { Do this outside of socketMutex to allow calling (dis-)connect from
     the callbacks while blocking on the WaitFor call here }
    SetLength(meta, 2);
    meta[0] := IPCON_CALLBACK_DISCONNECTED;
    meta[1] := IPCON_DISCONNECT_REASON_REQUEST;
    callbackQueue_.Enqueue(IPCON_QUEUE_KIND_META, meta);
    if (not callbackThread_.IsCurrent) then begin
      callbackQueue_.Enqueue(IPCON_QUEUE_KIND_EXIT, nil);
      callbackThread_.WaitFor;
      callbackThread_.Destroy;
    end
    else begin
      callbackQueue_.Enqueue(IPCON_QUEUE_KIND_DESTROY_AND_EXIT, nil);
    end;
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
  socketMutex.Acquire;
  try
    request := CreatePacket(nil, IPCON_FUNCTION_ENUMERATE, 8);
    Send(request);
  finally
    socketMutex.Release;
  end;
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
    data: WSAData;
{$endif}
    nodelay: longint;
{$ifdef MSWINDOWS}
    entry: PHostEnt;
{$else}
    entry: THostEntry;
{$endif}
{$ifdef FPC}
    address: TInetSockAddr;
{$else}
    address: TSockAddrIn;
{$endif}
    resolved: TInAddr;
    connectReason: word;
    meta: TByteArray;
begin
  { Create callback queue and thread }
  if (callbackThread = nil) then begin
    callbackQueue := TBlockingQueue.Create;
    callbackThread := TWrapperThread.Create({$ifdef FPC}@{$endif}self.CallbackLoop,
                                            callbackQueue);
  end;
  { Create and connect socket }
{$ifndef FPC}
  if (WSAStartup(MakeWord(2, 2), data) <> 0) then begin
    raise Exception.Create('Could not initialize Windows Sockets 2.2: ' + GetLastSocketError);
  end;
{$endif}
{$ifdef FPC}
  socket := fpsocket(AF_INET, SOCK_STREAM, 0);
  if (socket < 0) then begin
{$else}
  socket := WinSock.socket(AF_INET, SOCK_STREAM, 0);
  if (socket = INVALID_SOCKET) then begin
{$endif}
    raise Exception.Create('Could not create socket: ' + GetLastSocketError);
  end;
  nodelay := 1;
{$ifdef FPC}
  if (fpsetsockopt(socket, IPPROTO_TCP, TCP_NODELAY, @nodelay, sizeof(nodelay)) < 0) then begin
{$else}
  if (setsockopt(socket, IPPROTO_TCP, TCP_NODELAY, @nodelay, sizeof(nodelay)) = SOCKET_ERROR) then begin
{$endif}
    raise Exception.Create('Could not set TCP_NODELAY socket option: ' + GetLastSocketError);
  end;
{$ifdef MSWINDOWS}
  entry := gethostbyname(PAnsiChar(AnsiString(host)));
  if (entry = nil) then begin
    closesocket(socket);
    socket := INVALID_SOCKET;
    raise Exception.Create('Could not resolve host: ' + host);
  end;
  resolved.s_addr := longint(pointer(entry^.h_addr_list^)^);
{$else}
  entry.Name := '';
  if (not ResolveHostByName(host, entry)) then begin
    closesocket(socket);
    socket := INVALID_SOCKET;
    raise Exception.Create('Could not resolve host: ' + host);
  end;
  resolved := entry.Addr;
{$endif}
  address.sin_family := AF_INET;
  address.sin_port := htons(port);
  address.sin_addr := resolved;
{$ifdef FPC}
  if (fpconnect(socket, @address, sizeof(address)) < 0) then begin
{$else}
  if (WinSock.connect(socket, address, sizeof(address)) = SOCKET_ERROR) then begin
{$endif}
    closesocket(socket);
    socket := INVALID_SOCKET;
    raise Exception.Create('Could not connect socket: ' + GetLastSocketError);
  end;
  { Create receive thread }
  receiveFlag := true;
  receiveThread := TWrapperThread.Create({$ifdef FPC}@{$endif}self.ReceiveLoop, nil);
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
  callbackQueue.Enqueue(IPCON_QUEUE_KIND_META, meta);
end;

function TIPConnection.GetLastSocketError: string;
begin
{$ifdef FPC}
 {$ifdef UNIX}
  result := strerror(socketerror);
 {$else}
  result := SysErrorMessage(socketerror);
 {$endif}
{$else}
  result := SysErrorMessage(WSAGetLastError);
{$endif}
end;

procedure TIPConnection.ReceiveLoop(thread: TWrapperThread; opaque: TObject);
var data: array [0..8191] of byte; len, pendingLen, remainingLen: longint; packet, meta: TByteArray;
begin
  while (receiveFlag) do begin
{$ifdef FPC}
    len := fprecv(socket, @data[0], Length(data), 0);
{$else}
    len := Recv(socket, data, Length(data), 0);
{$endif}
    if (not receiveFlag) then begin
      exit;
    end;
    if ((len < 0) or (len = 0)) then begin
      if ((len < 0) and ({$ifdef FPC}socketerror{$else}WSAGetLastError{$endif} = ESysEINTR)) then begin
        continue;
      end;
      autoReconnectAllowed := true;
      receiveFlag := false;
      SetLength(meta, 2);
      meta[0] := IPCON_CALLBACK_DISCONNECTED;
      if (len = 0) then begin
        meta[1] := IPCON_DISCONNECT_REASON_SHUTDOWN;
      end
      else begin
        meta[1] := IPCON_DISCONNECT_REASON_ERROR;
      end;
      callbackQueue.Enqueue(IPCON_QUEUE_KIND_META, meta);
      exit;
    end;
    pendingLen := Length(pendingData);
    SetLength(pendingData, pendingLen + len);
    Move(data[0], pendingData[pendingLen], len);
    while (true) do begin
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

procedure TIPConnection.CallbackLoop(thread: TWrapperThread; opaque: TObject);
var callbackQueue_: TBlockingQueue; kind: byte; data: TByteArray;
begin
  callbackQueue_ := opaque as TBlockingQueue;
  while (true) do begin
    SetLength(data, 0);
    if (not callbackQueue_.Dequeue(kind, data, -1)) then begin
      break;
    end;
    if (kind = IPCON_QUEUE_KIND_EXIT) then begin
      break;
    end
    else if (kind = IPCON_QUEUE_KIND_DESTROY_AND_EXIT) then begin
      thread.Destroy;
      break;
    end
    else if (kind = IPCON_QUEUE_KIND_META) then begin
      DispatchMeta(data);
    end
    else if (kind = IPCON_QUEUE_KIND_PACKET) then begin
      { Don't dispatch callbacks when the receive thread isn't running }
      if (receiveFlag) then begin
        DispatchPacket(data);
      end;
    end;
  end;
  callbackQueue_.Destroy;
end;

procedure TIPConnection.HandleResponse(const packet: TByteArray);
var sequenceNumber, functionID: byte; device: TDevice;
begin
  functionID := GetFunctionIDFromData(packet);
  sequenceNumber := GetSequenceNumberFromData(packet);
  if ((sequenceNumber = 0) and (functionID = IPCON_CALLBACK_ENUMERATE)) then begin
    if (Assigned(enumerateCallback)) then begin
      callbackQueue.Enqueue(IPCON_QUEUE_KIND_PACKET, packet);
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
      callbackQueue.Enqueue(IPCON_QUEUE_KIND_PACKET, packet);
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
    socketMutex.Acquire;
    try
      if (IsConnected) then begin
        closesocket(socket);
        socket := INVALID_SOCKET;
      end;
    finally
      socketMutex.Release;
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

function TIPConnection.CreatePacket(const device: TDevice; const functionID: byte; const len: byte): TByteArray;
var sequenceNumber, responseExpected: byte;
begin
  SetLength(result, len);
  FillChar(result[0], len, 0);
  sequenceNumberMutex.Acquire;
  try
    sequenceNumber := nextSequenceNumber + 1;
    nextSequenceNumber := (nextSequenceNumber + 1) mod 15;
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

{ NOTE: Assumes that socketMutex is locked }
procedure TIPConnection.Send(const data: TByteArray);
begin
{$ifdef FPC}
  fpsend(socket, @data[0], Length(data), 0);
{$else}
  WinSock.Send(socket, data[0], Length(data), 0);
{$endif}
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
