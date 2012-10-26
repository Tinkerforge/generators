unit IPConnection;

{$ifdef FPC}{$mode OBJFPC}{$H+}{$endif}

interface

uses
  {$ifdef FPC}
   {$ifdef UNIX}CThreads, Errors, NetDB, BaseUnix, {$else}WinSock,{$endif}
  {$else}
   {$ifdef MSWINDOWS}Windows,{$endif}
  {$endif}
  Classes, Sockets, SyncObjs, SysUtils, Base58, LEConverter, BlockingQueue, Device;

const
  FUNCTION_GET_STACK_ID = 255;
  FUNCTION_ENUMERATE = 254;
  FUNCTION_ENUMERATE_CALLBACK = 253;
  BROADCAST_ADDRESS = 0;
  RESPONSE_TIMEOUT = 2500;

{$ifdef FPC}
 {$ifdef MSWINDOWS}
  ESysEINTR = WSAEINTR;
  ESysECONNRESET = WSAECONNRESET;
 {$endif}
{$else}
  ESysEINTR = 10004;
  ESysECONNRESET = 10054;
{$endif}

type
  { TWrapperThread }
  TThreadProcedure = procedure of object;
  TWrapperThread = class(TThread)
  private
      proc: TThreadProcedure;
  public
      constructor Create(const proc_: TThreadProcedure);
      procedure Execute; override;
  end;

  { TIPConnection }
  TIPConnectionNotifyEnumerate = procedure(const uid: string; const name: string; const stackID: byte; const isNew: boolean) of object;
  TIPConnection = class
  protected
    receiveThreadFlag: boolean;
    callbackThreadFlag: boolean;
    receiveThread: TWrapperThread;
    callbackThread: TWrapperThread;
  private
    pendingData: TByteArray;
    pendingAddDevice: TDevice;
    addDeviceMutex: TCriticalSection;
    devices: array [0..255] of TDevice;
{$ifdef FPC}
    address: TInetSockAddr;
    socket: TSocket;
{$else}
    remoteHost: TSocketHost;
    remotePort: TSocketPort;
    socket: TTcpClient;
    lastSocketError: integer;
{$endif}
    callbackQueue: TBlockingQueue;
    enumerateCallback: TIPConnectionNotifyEnumerate;

{$ifndef FPC}
    procedure SocketErrorOccurred(sender: TObject; socketError: integer);
{$endif}
    function Reconnect: boolean;
    procedure ReceiveLoop;
    procedure CallbackLoop;
    procedure HandleResponse(const packet: TByteArray);
    procedure HandleAddDevice(const packet: TByteArray);
    procedure HandleEnumerate(const packet: TByteArray);
  public
    constructor Create(const host: string; const port: word);
    destructor Destroy; override;
    procedure JoinThread;
    procedure AddDevice(device: TDevice);
    procedure Enumerate(const enumerateCallback_: TIPConnectionNotifyEnumerate);

    procedure Write(const data: TByteArray);
  end;

  function CreateRequestPacket(const stackID: byte; const functionID: byte; const len: word): TByteArray;
  function GetStackIDFromData(const data: TByteArray): byte;
  function GetFunctionIDFromData(const data: TByteArray): byte;
  function GetLengthFromData(const data: TByteArray): word;

implementation

{ TWrapperThread }
constructor TWrapperThread.Create(const proc_: TThreadProcedure);
begin
  proc := proc_;
  inherited Create(false);
end;

procedure TWrapperThread.Execute;
begin
  proc;
end;

{ TIPConnection }
constructor TIPConnection.Create(const host: string; const port: word);
{$ifdef FPC}
 {$ifdef MSWINDOWS}
var entry: PHostEnt;
 {$else}
var entry: THostEntry;
 {$endif}
    resolved: TInAddr;
{$endif}
begin
  receiveThreadFlag := true;
  callbackThreadFlag := true;
  addDeviceMutex := TCriticalSection.Create;
  callbackQueue := TBlockingQueue.Create;
{$ifdef FPC}
  socket := fpsocket(AF_INET, SOCK_STREAM, 0);
  if (socket < 0) then begin
    raise Exception.Create('Could not create socket: ' + {$ifdef UNIX}strerror(socketerror){$else}SysErrorMessage(socketerror){$endif});
  end;
  resolved := StrToHostAddr(host);
  if (HostAddrToStr(resolved) <> host) then begin
 {$ifdef MSWINDOWS}
    entry := gethostbyname(PChar(host));
    if (entry = nil) then begin
      raise Exception.Create('Could not resolve host: ' + host);
    end;
    resolved.s_addr := longint(pointer(entry^.h_addr_list^)^);
 {$else}
    entry.Name := '';
    if (not ResolveHostByName(host, entry)) then begin
      raise Exception.Create('Could not resolve host: ' + host);
    end;
    resolved := entry.Addr;
 {$endif}
  end
  else begin
    resolved := HostToNet(resolved);
  end;
  address.sin_family := AF_INET;
  address.sin_port := htons(port);
  address.sin_addr := resolved;
  if (fpconnect(socket, @address, sizeof(address)) < 0) then begin
    raise Exception.Create('Could not connect socket: ' + {$ifdef UNIX}strerror(socketerror){$else}SysErrorMessage(socketerror){$endif});
  end;
{$else}
  remoteHost := TSocketHost(host);
  remotePort := TSocketPort(IntToStr(port));
  socket := TTcpClient.Create(nil);
  socket.RemoteHost := remoteHost;
  socket.RemotePort := remotePort;
  socket.BlockMode := bmBlocking;
  socket.OnError := self.SocketErrorOccurred;
  socket.Open;
  if (not socket.Connected) then begin
    raise Exception.Create('Could not connect socket');
  end;
{$endif}
  receiveThread := TWrapperThread.Create({$ifdef FPC}@{$endif}self.ReceiveLoop);
  callbackThread := TWrapperThread.Create({$ifdef FPC}@{$endif}self.CallbackLoop);
end;

destructor TIPConnection.Destroy;
var packet: TByteArray;
begin
  { End callback thread }
  callbackThreadFlag := false;
  SetLength(packet, 0);
  callbackQueue.Enqueue(packet);
{$ifdef FPC}
  if (GetCurrentThreadId <> callbackThread.ThreadID) then begin
{$else}
  if (Windows.GetCurrentThreadId <> callbackThread.ThreadID) then begin
{$endif}
    callbackThread.WaitFor;
  end;
  callbackQueue.Destroy;
  { End receive thread }
  receiveThreadFlag := false;
{$ifdef FPC}
  if (socket >= 0) then begin
    fpshutdown(socket, 2);
    closesocket(socket);
    socket := -1;
  end;
{$else}
  socket.Close;
{$endif}
{$ifdef FPC}
  if (GetCurrentThreadId <> receiveThread.ThreadID) then begin
{$else}
  if (Windows.GetCurrentThreadId <> receiveThread.ThreadID) then begin
{$endif}
    receiveThread.WaitFor;
  end;
  addDeviceMutex.Destroy;
  inherited Destroy;
end;

procedure TIPConnection.JoinThread;
begin
  callbackThread.WaitFor;
  receiveThread.WaitFor;
end;

{$ifndef FPC}
procedure TIPConnection.SocketErrorOccurred(sender: TObject; socketError: integer);
begin
  lastSocketError := socketError;
end;
{$endif}

function TIPConnection.Reconnect: boolean;
begin
  result := false;
{$ifdef FPC}
  closesocket(socket);
  socket := -1;
{$else}
  socket.Close;
{$endif}
  while (receiveThreadFlag) do begin
{$ifdef FPC}
    socket := fpsocket(AF_INET, SOCK_STREAM, 0);
    if (socket < 0) then begin
      sleep(1000);
      continue;
    end;
    if (fpconnect(socket, @address, sizeof(address)) < 0) then begin
      closesocket(socket);
      socket := -1;
      sleep(1000);
      continue;
    end;
{$else}
    socket := TTcpClient.Create(nil);
    socket.RemoteHost := remoteHost;
    socket.RemotePort := remotePort;
    socket.BlockMode := bmBlocking;
    socket.OnError := self.SocketErrorOccurred;
    socket.Open;
    if (not socket.Connected) then begin
      socket.Close;
      sleep(1000);
      continue;
    end;
{$endif}
    result := true;
    break;
  end;
end;

procedure TIPConnection.ReceiveLoop;
var data: array [0..8191] of byte; len, pendingLen: longint; packet: TByteArray;
begin
  try
    while (receiveThreadFlag) and (not receiveThread.Terminated) do begin
{$ifdef FPC}
      len := fprecv(socket, @data[0], Length(data), 0);
{$else}
      lastSocketError := 0;
      len := socket.ReceiveBuf(data, Length(data));
{$endif}
      if (not receiveThreadFlag) then begin
        exit;
      end;
      if (len < 0) then begin
{$ifdef FPC}
        if (socketerror = ESysEINTR) then begin
          continue;
        end;
        if (socketerror = ESysECONNRESET) then begin
          if (not Reconnect) then begin
            exit;
          end;
          continue;
        end;
{$else}
        if (lastSocketError = ESysEINTR) then begin
          continue;
        end;
        if (lastSocketError = ESysECONNRESET) then begin
          if (not Reconnect) then begin
            exit;
          end;
          continue;
        end;
{$endif}
        if (receiveThreadFlag) then begin
          WriteLn(ErrOutput, 'A socket error occurred, destroying IPConnection');
        end;
        exit;
      end;
      if (len = 0) then begin
        if (receiveThreadFlag) then begin
          WriteLn(ErrOutput, 'Socket disconnected by Server, destroying IPConnection');
        end;
        exit;
      end;
      pendingLen := Length(pendingData);
      SetLength(pendingData, pendingLen + len);
      Move(data[0], pendingData[pendingLen], len);
      while (true) do begin
        if (Length(pendingData) < 4) then begin
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
        Move(pendingData[len], pendingData[0], Length(pendingData) - len);
        SetLength(pendingData, Length(pendingData) - len);
        HandleResponse(packet);
      end;
    end;
  except
  end;
end;

procedure TIPConnection.CallbackLoop;
var packet: TByteArray; functionID: byte; stackID: byte; device: TDevice; callbackWrapper: TCallbackWrapper;
begin
  while (callbackThreadFlag) and (not callbackThread.Terminated) do begin
    SetLength(packet, 0);
    if (not callbackQueue.Dequeue(packet, -1)) then begin
      exit;
    end;
    if (not callbackThreadFlag) then begin
      exit;
    end;
    functionID := GetFunctionIDFromData(packet);
    if (functionID = FUNCTION_ENUMERATE_CALLBACK) then begin
      if (Assigned(enumerateCallback)) then begin
        enumerateCallback(Base58Encode(LEConvertUInt64From(4, packet)),
                          LEConvertStringFrom(12, 40, packet),
                          packet[52],
                          LEConvertBooleanFrom(53, packet));
      end;
    end
    else begin
      stackID := GetStackIDFromData(packet);
      device := devices[stackID];
      callbackWrapper := device.callbackWrappers[functionID];
      if (Assigned(callbackWrapper)) then begin
        callbackWrapper(packet);
      end;
    end;
  end;
end;

procedure TIPConnection.HandleResponse(const packet: TByteArray);
var functionID, stackID: byte; device: TDevice; callbackWrapper: TCallbackWrapper;
begin
  functionID := GetFunctionIDFromData(packet);
  if (functionID = FUNCTION_GET_STACK_ID) then begin
    HandleAddDevice(packet);
    exit;
  end
  else if (functionID = FUNCTION_ENUMERATE_CALLBACK) then begin
    HandleEnumerate(packet);
    exit;
  end;
  stackID := GetStackIDFromData(packet);
  device := devices[stackID];
  if (device = nil) then begin
    { Response from an unknown device, ignoring it }
    exit;
  end;
  if (device.expectedResponseFunctionID = functionID) then begin
    device.responseQueue.Enqueue(packet);
    exit;
  end;
  callbackWrapper := device.callbackWrappers[functionID];
  if (Assigned(callbackWrapper)) then begin
    callbackQueue.Enqueue(packet);
  end;
end;

procedure TIPConnection.HandleAddDevice(const packet: TByteArray);
var uid: uint64; name, tmp1, tmp2: string; i: longint;
begin
  if (not Assigned(pendingAddDevice)) then begin
    exit;
  end;
  uid := LEConvertUInt64From(4, packet);
  if (pendingAddDevice.uid = uid) then begin
    name := LEConvertStringFrom(15, 40, packet);
    i := LastDelimiter(' ', name);
    if (i < 1) then begin
      exit;
    end;
    tmp1 := StringReplace(Copy(name, 0, i - 1), '-', ' ', [rfReplaceAll]);
    tmp2 := StringReplace(pendingAddDevice.expectedName, '-', ' ', [rfReplaceAll]);
    if (CompareStr(tmp1, tmp2) <> 0) then begin
      exit;
    end;
    pendingAddDevice.firmwareVersion[0] := packet[12];
    pendingAddDevice.firmwareVersion[1] := packet[13];
    pendingAddDevice.firmwareVersion[2] := packet[14];
    pendingAddDevice.name := name;
    pendingAddDevice.stackID := packet[55];
    devices[pendingAddDevice.stackID] := pendingAddDevice;
    pendingAddDevice.responseQueue.Enqueue(packet);
  end;
end;

procedure TIPConnection.HandleEnumerate(const packet: TByteArray);
begin
  if (Assigned(enumerateCallback)) then begin
    callbackQueue.Enqueue(packet);
  end
end;
procedure TIPConnection.Enumerate(const enumerateCallback_: TIPConnectionNotifyEnumerate);
var request: TByteArray;
begin
  enumerateCallback := enumerateCallback_;
  request := CreateRequestPacket(BROADCAST_ADDRESS, FUNCTION_ENUMERATE, 4);
  Write(request);end;

procedure TIPConnection.AddDevice(device: TDevice);
var request, response: TByteArray;
begin
  addDeviceMutex.Acquire;
  try
    request := CreateRequestPacket(BROADCAST_ADDRESS, FUNCTION_GET_STACK_ID, 12);
    LEConvertUInt64To(device.uid, 4, request);
    pendingAddDevice := device;
    Write(request);
    SetLength(response, 0);
    if (not device.responseQueue.Dequeue(response, RESPONSE_TIMEOUT)) then begin
      raise Exception.Create('Could not add device ' + Base58Encode(device.uid) + ', timeout');
    end;
    device.ipcon := self;
  finally
    pendingAddDevice := nil;
    addDeviceMutex.Release;
  end;
end;

procedure TIPConnection.Write(const data: TByteArray);
begin
{$ifdef FPC}
  fpsend(socket, @data[0], Length(data), 0);
{$else}
  socket.SendBuf(data[0], Length(data));
{$endif}
end;

function CreateRequestPacket(const stackID: byte; const functionID: byte; const len: word): TByteArray;
begin
  SetLength(result, len);
  FillChar(result[0], len, 0);
  result[0] := stackID;
  result[1] := functionID;
  LEConvertUInt16To(len, 2, result);
end;

function GetStackIDFromData(const data: TByteArray): byte;
begin
  result := data[0];
end;

function GetFunctionIDFromData(const data: TByteArray): byte;
begin
  result := data[1];
end;

function GetLengthFromData(const data: TByteArray): word;
begin
  result := LEConvertUInt16From(2, data);
end;

end.
