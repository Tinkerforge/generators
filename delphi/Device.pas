unit Device;

{$ifdef FPC}{$mode OBJFPC}{$H+}{$endif}

interface

uses
  {$ifdef UNIX}CThreads,{$endif} SyncObjs, SysUtils, Base58, BlockingQueue, LEConverter;

const
  RESPONSE_EXPECTED_INVALID_FUNCTION_ID = 0;
  RESPONSE_EXPECTED_ALWAYS_TRUE = 1; { Getter }
  RESPONSE_EXPECTED_ALWAYS_FALSE = 2; { Callback }
  RESPONSE_EXPECTED_TRUE = 3; { Setter }
  RESPONSE_EXPECTED_FALSE = 4; { Setter, default }

type
  { TimeoutException }
  TimeoutException = class(Exception)
  end;

  { NotSupportedException }
  NotSupportedException = class(Exception)
  end;

  { TDevice }
  TCallbackWrapper = procedure(const packet: TByteArray) of object;
  TVersionNumber = array [0..2] of byte;
  TDevice = class
  private
    requestMutex: TCriticalSection;
  public
    uid_: longword;
    ipcon: TObject;
    apiVersion: TVersionNumber;
    expectedResponseFunctionID: byte;
    expectedResponseSequenceNumber: byte;
    responseQueue: TBlockingQueue;
    responseExpected: array [0..255] of byte;
    callbackWrappers: array [0..255] of TCallbackWrapper;

    constructor Create(const uid__: string; ipcon_: TObject);
    destructor Destroy; override;

    /// <summary>
    ///  Returns the name (including the hardware version), the firmware
    ///  version and the binding version of the device. The firmware and
    ///  binding versions are given in arrays of size 3 with the syntax
    ///  [major, minor, revision].
    /// </summary>
    function GetAPIVersion: TVersionNumber;

    function GetResponseExpected(const functionID: byte): boolean;
    procedure SetResponseExpected(const functionID: byte; const responseExpected_: boolean);
    procedure SetResponseExpectedAll(const responseExpected_: boolean);

    { Internal }
    function SendRequest(const request: TByteArray): TByteArray;
  end;

  { TDeviceTable }
  TUIDArray = array of longword;
  TDeviceArray = array of TDevice;
  TDeviceTable = class
  private
    mutex: TCriticalSection;
    uids: TUIDArray;
    devices: TDeviceArray;
  public
    constructor Create();
    destructor Destroy; override;
    procedure Insert(const uid: longword; const device: TDevice);
    procedure Remove(const uid: longword);
    function Get(const uid: longword): TDevice;
  end;

implementation

uses
  IPConnection;

{ TDevice }
constructor TDevice.Create(const uid__: string; ipcon_: TObject);
var i: longint;
begin
  uid_ := Base58Decode(uid__);
  ipcon := ipcon_;
  apiVersion[0] := 0;
  apiVersion[1] := 0;
  apiVersion[2] := 0;
  expectedResponseFunctionID := 0;
  expectedResponseSequenceNumber := 0;
  requestMutex := TCriticalSection.Create;
  responseQueue := TBlockingQueue.Create;
  for i := 0 to Length(responseExpected) - 1 do begin
    responseExpected[i] := RESPONSE_EXPECTED_INVALID_FUNCTION_ID;
  end;
  (ipcon as TIPConnection).devices.Insert(uid_, self);
end;

destructor TDevice.Destroy;
begin
  requestMutex.Destroy;
  responseQueue.Destroy;
  inherited Destroy;
end;

function TDevice.GetAPIVersion: TVersionNumber;
begin
  result := apiVersion;
end;

function TDevice.GetResponseExpected(const functionID: byte): boolean;
begin
  if ((responseExpected[functionID] = RESPONSE_EXPECTED_ALWAYS_TRUE) or
      (responseExpected[functionID] = RESPONSE_EXPECTED_TRUE)) then begin
    result := true;
  end
  else if ((responseExpected[functionID] = RESPONSE_EXPECTED_ALWAYS_FALSE) or
           (responseExpected[functionID] = RESPONSE_EXPECTED_FALSE)) then begin
    result := false;
  end
  else begin
    raise Exception.Create('Invalid function ID');
  end;
end;

procedure TDevice.SetResponseExpected(const functionID: byte; const responseExpected_: boolean);
begin
  if ((responseExpected[functionID] <> RESPONSE_EXPECTED_TRUE) and
      (responseExpected[functionID] <> RESPONSE_EXPECTED_FALSE)) then begin
    raise Exception.Create('Invalid function ID');
  end
  else if (responseExpected_) then begin
    responseExpected[functionID] := RESPONSE_EXPECTED_TRUE;
  end
  else begin
    responseExpected[functionID] := RESPONSE_EXPECTED_FALSE;
  end;
end;

procedure TDevice.SetResponseExpectedAll(const responseExpected_: boolean);
var i: longint;
begin
  for i := 0 to Length(responseExpected) - 1 do begin
    if ((responseExpected[i] = RESPONSE_EXPECTED_TRUE) or
        (responseExpected[i] = RESPONSE_EXPECTED_FALSE)) then begin
      if (responseExpected_) then begin
        responseExpected[i] := RESPONSE_EXPECTED_TRUE;
      end
      else begin
        responseExpected[i] := RESPONSE_EXPECTED_FALSE;
      end;
    end;
  end;
end;

{ NOTE: Assumes that requestMutex is locked }
function TDevice.SendRequest(const request: TByteArray): TByteArray;
var ipcon_: TIPConnection; responseExpected_: boolean; kind, errorCode, functionID: byte;
begin
  SetLength(result, 0);
  ipcon_ := ipcon as TIPConnection;
  ipcon_.socketMutex.Acquire;
  try
    if (not ipcon_.IsConnected) then begin
      raise Exception.Create('Not connected');
    end;
    responseExpected_ := GetResponseExpectedFromData(request);
    if (responseExpected_) then begin
      expectedResponseFunctionID := GetFunctionIDFromData(request);
      expectedResponseSequenceNumber := GetSequenceNumberFromData(request);
    end;
    ipcon_.Send(request);
  finally
    ipcon_.socketMutex.Release;
  end;
  if (responseExpected_) then begin
    functionID := GetFunctionIDFromData(request);
    if (not responseQueue.Dequeue(kind, result, ipcon_.timeout)) then begin
      expectedResponseFunctionID := 0;
      expectedResponseSequenceNumber := 0;
      raise TimeoutException.Create('Did not receive response in time for function ID ' + IntToStr(functionID));
    end;
    expectedResponseFunctionID := 0;
    expectedResponseSequenceNumber := 0;
    errorCode := GetErrorCodeFromData(result);
    if (errorCode = 0) then begin
      { No error }
    end
    else begin
      if (errorCode = 1) then begin
        raise NotSupportedException.Create('Got invalid parameter for function ' + IntToStr(functionID));
      end
      else if (errorCode = 2) then begin
        raise NotSupportedException.Create('Function ' + IntToStr(functionID) + ' is not supported');
      end
      else begin
        raise NotSupportedException.Create('Function ' + IntToStr(functionID) + ' returned an unknown error');
      end;
    end;
  end;
end;


{ TDeviceTable }
constructor TDeviceTable.Create;
begin
  mutex := TCriticalSection.Create;
  SetLength(uids, 0);
  SetLength(devices, 0);
end;

destructor TDeviceTable.Destroy;
begin
  SetLength(uids, 0);
  SetLength(devices, 0);
  mutex.Destroy;
  inherited Destroy;
end;

procedure TDeviceTable.Insert(const uid: longword; const device: TDevice);
var len: longint; i: longint;
begin
  len := Length(uids);
  for i := 0 to len - 1 do begin
    if (uids[i] = uid) then begin
      devices[i] := device;
      exit;
    end;
  end;
  SetLength(uids, len + 1);
  SetLength(devices, len + 1);
  uids[len] := uid;
  devices[len] := device;
end;

procedure TDeviceTable.Remove(const uid: longword);
var len: longint; i: longint; k: longint;
begin
  len := Length(uids);
  for i := 0 to len - 1 do begin
    if (uids[i] = uid) then begin
      for k := i + 1 to len - 1 do begin
        uids[k - 1] := uids[k];
        devices[k - 1] := devices[k];
      end;
      SetLength(uids, len - 1);
      SetLength(devices, len - 1);
      exit;
    end;
  end;
end;

function TDeviceTable.Get(const uid: longword): TDevice;
var len: longint; i: longint;
begin
  result := nil;
  len := Length(uids);
  for i := 0 to len - 1 do begin
    if (uids[i] = uid) then begin
      result := devices[i];
      exit;
    end;
  end;
end;

end.
