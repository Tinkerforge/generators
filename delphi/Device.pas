unit Device;

{$ifdef FPC}{$mode OBJFPC}{$H+}{$endif}

interface

uses
  {$ifdef UNIX}CThreads,{$endif} SyncObjs, SysUtils, Base58, BlockingQueue, LEConverter;

type
  { TDevice }
  TCallbackWrapper = procedure(const packet: TByteArray) of object;
  TVersionNumber = array [0..2] of byte;
  TDeviceVersion = record
    name: string;
    firmwareVersion: TVersionNumber;
    bindingVersion: TVersionNumber;
  end;
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
    procedure SendRequestNoResponse(const request: TByteArray);
    procedure SendRequestExpectResponse(const request: TByteArray; const functionID: byte; out response: TByteArray);
    function GetVersion: TDeviceVersion;
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

function TDevice.GetVersion: TDeviceVersion;
begin
  result.name := name;
  result.firmwareVersion := firmwareVersion;
  result.bindingVersion := bindingVersion;
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
