unit Device;

{$ifdef FPC}{$mode OBJFPC}{$H+}{$endif}

interface

uses
  {$ifdef UNIX}CThreads,{$endif} SyncObjs, SysUtils, Base58, BlockingQueue, LEConverter;

type
  { TDevice }
  TCallbackWrapper = procedure(const packet: TByteArray) of object;
  TVersionNumber = array [0..2] of byte;
  TDevice = class
  private
    writeMutex: TCriticalSection;
  public
    uid: uint64;
    stackID: byte;
    expectedName: string;
    name: string;
    firmwareVersion: TVersionNumber;
    bindingVersion: TVersionNumber;
    expectedResponseFunctionID: byte;
    responseQueue: TBlockingQueue;
    ipcon: TObject;
    callbackWrappers: array [0..255] of TCallbackWrapper;

    constructor Create(const uid_: string);
    destructor Destroy; override;

    /// <summary>
    ///  Returns the name (including the hardware version), the firmware
    ///  version and the binding version of the device. The firmware and
    ///  binding versions are given in arrays of size 3 with the syntax
    ///  [major, minor, revision].
    /// </summary>
    procedure GetVersion(out name_: string; out firmwareVersion_: TVersionNumber; out bindingVersion_: TVersionNumber);

    procedure SendRequestNoResponse(const request: TByteArray);
    procedure SendRequestExpectResponse(const request: TByteArray; const functionID: byte; out response: TByteArray);
  end;

implementation

uses
  IPConnection;

{ TDevice }
constructor TDevice.Create(const uid_: string);
begin
  uid := Base58Decode(uid_);
  responseQueue := TBlockingQueue.Create;
  writeMutex := TCriticalSection.Create;
end;

destructor TDevice.Destroy;
begin
  writeMutex.Destroy;
  responseQueue.Destroy;
  inherited Destroy;
end;

procedure TDevice.GetVersion(out name_: string; out firmwareVersion_: TVersionNumber; out bindingVersion_: TVersionNumber);
begin
  name_ := name;
  firmwareVersion_ := firmwareVersion;
  bindingVersion_ := bindingVersion;
end;

procedure TDevice.SendRequestNoResponse(const request: TByteArray);
begin
  if ((not Assigned(ipcon)) or (not (ipcon is TIPConnection))) then begin
    raise Exception.Create('Not added to IPConnection');
  end;
  writeMutex.Acquire;
  try
    (ipcon as TIPConnection).Write(request);
  finally
    writeMutex.Release;
  end;
end;

procedure TDevice.SendRequestExpectResponse(const request: TByteArray; const functionID: byte; out response: TByteArray);
begin
  if ((not Assigned(ipcon)) or (not (ipcon is TIPConnection))) then begin
    raise Exception.Create('Not added to IPConnection');
  end;
  writeMutex.Acquire;
  try
    expectedResponseFunctionID := functionID;
    (ipcon as TIPConnection).Write(request);
    if (not responseQueue.Dequeue(response, RESPONSE_TIMEOUT)) then begin
      raise Exception.Create('Did not receive response in time');
    end;
  finally
    writeMutex.Release;
  end;
end;

end.
