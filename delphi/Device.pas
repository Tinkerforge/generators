{
  Copyright (C) 2012-2013, 2019-2020 Matthias Bolte <matthias@tinkerforge.com>

  Redistribution and use in source and binary forms of this file,
  with or without modification, are permitted. See the Creative
  Commons Zero (CC0 1.0) License for more details.
}

unit Device;

{$ifdef FPC}{$mode OBJFPC}{$H+}{$endif}

interface

uses
  {$ifdef UNIX}CThreads,{$endif} SyncObjs, SysUtils, Base58, BlockingQueue,
  LEConverter, DeviceBase, DeviceDisplayNames;

const
  DEVICE_RESPONSE_EXPECTED_INVALID_FUNCTION_ID = 0;
  DEVICE_RESPONSE_EXPECTED_ALWAYS_TRUE = 1; { getter }
  DEVICE_RESPONSE_EXPECTED_TRUE = 2; { setter }
  DEVICE_RESPONSE_EXPECTED_FALSE = 3; { setter, default }

  DEVICE_IDENTIFIER_CHECK_PENDING = 0;
  DEVICE_IDENTIFIER_CHECK_MATCH = 1;
  DEVICE_IDENTIFIER_CHECK_MISMATCH = 2;

type
  { TDevice }
  TCallbackWrapper = procedure(const packet: TByteArray) of object;
  TVersionNumber = array [0..2] of byte;
  TDevice = class(TDeviceBase)
  private
    requestMutex: TCriticalSection;
    deviceIdentifier_: word;
    deviceDisplayName: string;
    deviceIdentifierMutex: TCriticalSection;
    deviceIdentifierCheck: byte; { protected by deviceIdentifierMutex }
    wrongDeviceDisplayName: string; { protected by deviceIdentifierMutex }
  public
    replaced: boolean;
    uidString: string;
    uidNumber: longword;
    uidValid: boolean;
    ipcon: TObject;
    apiVersion: TVersionNumber;
    expectedResponseFunctionID: byte; { protected by requestMutex }
    expectedResponseSequenceNumber: byte; { protected by requestMutex }
    responseQueue: TBlockingQueue;
    responseExpected: array [0..255] of byte;
    callbackWrappers: array [0..255] of TCallbackWrapper;

    /// <summary>
    ///  Creates the device object with the unique device ID *uid* and adds
    ///  it to the IPConnection *ipcon*.
    /// </summary>
    constructor Create(const uid: string; ipcon_: TObject; deviceIdentifier: word; deviceDisplayName_: string);

    /// <summary>
    ///  Removes the device object from its IPConnection and destroys it.
    ///  The device object cannot be used anymore afterwards.
    /// </summary>
    destructor Destroy; override;

    /// <summary>
    ///  Returns the API version (major, minor, revision) of the bindings for
    ///  this device.
    /// </summary>
    function GetAPIVersion: TVersionNumber; virtual;

    /// <summary>
    ///  Returns the response expected flag for the function specified by the
    ///  *functionId* parameter. It is *true* if the function is expected to
    ///  send a response, *false* otherwise.
    ///
    ///  For getter functions this is enabled by default and cannot be disabled,
    ///  because those functions will always send a response. For callback
    ///  configuration functions it is enabled by default too, but can be
    ///  disabled via the setResponseExpected function. For setter functions it
    ///  is disabled by default and can be enabled.
    ///
    ///  Enabling the response expected flag for a setter function allows to
    ///  detect timeouts and other error conditions calls of this setter as
    ///  well. The device will then send a response for this purpose. If this
    ///  flag is disabled for a setter function then no response is sent and
    ///  errors are silently ignored, because they cannot be detected.
    /// </summary>
    function GetResponseExpected(const functionId: byte): boolean; virtual;

    /// <summary>
    ///  Changes the response expected flag of the function specified by
    ///  the function ID parameter. This flag can only be changed for setter
    ///  (default value: *false*) and callback configuration functions
    ///  (default value: *true*). For getter functions it is always enabled.
    ///
    ///  Enabling the response expected flag for a setter function allows to
    ///  detect timeouts and other error conditions calls of this setter as
    ///  well. The device will then send a response for this purpose. If this
    ///  flag is disabled for a setter function then no response is sent and
    ///  errors are silently ignored, because they cannot be detected.
    /// </summary>
    procedure SetResponseExpected(const functionId: byte;
                                  const responseExpected_: boolean); virtual;

    /// <summary>
    ///  Changes the response expected flag for all setter and callback
    ///  configuration functions of this device at once.
    /// </summary>
    procedure SetResponseExpectedAll(const responseExpected_: boolean); virtual;

    procedure GetIdentity(out uid: string; out connectedUid: string; out position: char;
                          out hardwareVersion: TVersionNumber; out firmwareVersion: TVersionNumber;
                          out deviceIdentifier: word); virtual; abstract;

    { Internal }
    function SendRequest(const request: TByteArray; expectedResponseLength: byte): TByteArray;
    procedure CheckValidity;
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
    constructor Create;
    destructor Destroy; override;
    function Insert(const uid: longword; const device: TDevice; out replacedDevice: TDevice): boolean;
    procedure Remove(const uid: longword);
    function Get(const uid: longword): TDevice;
  end;

implementation

uses
  IPConnection;

{ TDevice }
constructor TDevice.Create(const uid: string; ipcon_: TObject; deviceIdentifier: word; deviceDisplayName_: string);
var longUidNumber: uint64; value1, value2, i: longint;
begin
  inherited Create;
  replaced := false;
  uidString := uid;
  uidValid := Base58Decode(uid, longUidNumber);
  if (uidValid and (longUidNumber > $FFFFFFFF)) then begin
    { Convert from 64bit to 32bit }
    value1 := longUidNumber and $FFFFFFFF;
    value2 := longword((longUidNumber shr 32) and $FFFFFFFF);
    longUidNumber := (value1 and $00000FFF);
    longUidNumber := longUidNumber or ((value1 and longword($0F000000)) shr 12);
    longUidNumber := longUidNumber or ((value2 and longword($0000003F)) shl 16);
    longUidNumber := longUidNumber or ((value2 and longword($000F0000)) shl 6);
    longUidNumber := longUidNumber or ((value2 and longword($3F000000)) shl 2);
  end;
  uidNumber := longUidNumber;
  if (uidNumber = 0) then begin
    uidValid := false; { broadcast UID is forbidden }
  end;
  uidString := uid;
  ipcon := ipcon_;
  apiVersion[0] := 0;
  apiVersion[1] := 0;
  apiVersion[2] := 0;
  deviceIdentifier_ := deviceIdentifier;
  deviceDisplayName := deviceDisplayName_;
  deviceIdentifierMutex := TCriticalSection.Create;
  deviceIdentifierCheck := DEVICE_IDENTIFIER_CHECK_PENDING;
  wrongDeviceDisplayName := '?';
  expectedResponseFunctionID := 0;
  expectedResponseSequenceNumber := 0;
  requestMutex := TCriticalSection.Create;
  responseQueue := TBlockingQueue.Create;
  for i := 0 to Length(responseExpected) - 1 do begin
    responseExpected[i] := DEVICE_RESPONSE_EXPECTED_INVALID_FUNCTION_ID;
  end;
end;

destructor TDevice.Destroy;
begin
  if (not replaced and uidValid) then begin
    (ipcon as TIPConnection).devices.Remove(uidNumber);
  end;
  responseQueue.Destroy;
  requestMutex.Destroy;
  deviceIdentifierMutex.Destroy;
  inherited Destroy;
end;

function TDevice.GetAPIVersion: TVersionNumber;
begin
  result := apiVersion;
end;

function TDevice.GetResponseExpected(const functionID: byte): boolean;
var flag: byte;
begin
  flag := responseExpected[functionID];
  if (flag = DEVICE_RESPONSE_EXPECTED_INVALID_FUNCTION_ID) then begin
    raise Exception.Create('Invalid function ID ' + IntToStr(functionID));
  end;
  if ((flag = DEVICE_RESPONSE_EXPECTED_ALWAYS_TRUE) or
      (flag = DEVICE_RESPONSE_EXPECTED_TRUE)) then begin
    result := true;
  end
  else begin
    result := false;
  end;
end;

procedure TDevice.SetResponseExpected(const functionID: byte; const responseExpected_: boolean);
var flag: byte;
begin
  flag := responseExpected[functionID];
  if (flag = DEVICE_RESPONSE_EXPECTED_INVALID_FUNCTION_ID) then begin
    raise Exception.Create('Invalid function ID ' + IntToStr(functionID));
  end;
  if (flag = DEVICE_RESPONSE_EXPECTED_ALWAYS_TRUE) then begin
    raise Exception.Create('Response Expected flag cannot be changed for function ID ' + IntToStr(functionID));
  end;
  if (responseExpected_) then begin
    responseExpected[functionID] := DEVICE_RESPONSE_EXPECTED_TRUE;
  end
  else begin
    responseExpected[functionID] := DEVICE_RESPONSE_EXPECTED_FALSE;
  end;
end;

procedure TDevice.SetResponseExpectedAll(const responseExpected_: boolean);
var flag: byte; i: longint;
begin
  if (responseExpected_) then begin
    flag := DEVICE_RESPONSE_EXPECTED_TRUE;
  end
  else begin
    flag := DEVICE_RESPONSE_EXPECTED_FALSE;
  end;
  for i := 0 to Length(responseExpected) - 1 do begin
    if ((responseExpected[i] = DEVICE_RESPONSE_EXPECTED_TRUE) or
        (responseExpected[i] = DEVICE_RESPONSE_EXPECTED_FALSE)) then begin
      responseExpected[i] := flag;
    end;
  end;
end;

{ NOTE: assumes that CheckValidity was successful }
function TDevice.SendRequest(const request: TByteArray; expectedResponseLength: byte): TByteArray;
var ipcon_: TIPConnection; kind, errorCode, functionID: byte;
begin
  result := []; { avoid compiler warning "function result variable of a managed type does not seem to be initialized" }
  SetLength(result, 0);
  ipcon_ := ipcon as TIPConnection;
  if (GetResponseExpectedFromData(request)) then begin
    functionID := GetFunctionIDFromData(request);
    requestMutex.Acquire;
    try
      expectedResponseFunctionID := functionID;
      expectedResponseSequenceNumber := GetSequenceNumberFromData(request);
      try
        ipcon_.SendRequest(request);
        while true do begin
          if (not responseQueue.Dequeue(kind, result, ipcon_.timeout)) then begin
            raise ETimeoutException.Create('Did not receive response in time for function ID ' + IntToStr(functionID));
          end;
          if ((expectedResponseFunctionID = GetFunctionIDFromData(result)) and
              (expectedResponseSequenceNumber = GetSequenceNumberFromData(result))) then begin
            { Ignore old responses that arrived after the timeout expired, but before setting
              expectedResponseFunctionID and expectedResponseSequenceNumber back to 0 }
            break;
          end;
        end;
      finally
        expectedResponseFunctionID := 0;
        expectedResponseSequenceNumber := 0;
      end;
    finally
      requestMutex.Release;
    end;
    errorCode := GetErrorCodeFromData(result);
    if (errorCode = 0) then begin
      if (expectedResponseLength = 0) then begin
        { Setter with response-expected enabled }
        expectedResponseLength := 8;
      end;
      if (Length(result) <> expectedResponseLength) then begin
        raise EWrongResponseLengthException.Create('Expected response of ' + IntToStr(expectedResponseLength) + ' byte for function ID ' + IntToStr(functionID) + ', got ' + IntToStr(Length(result)) + ' byte instead');
      end;
    end
    else if (errorCode = 1) then begin
      raise EInvalidParameterException.Create('Got invalid parameter for function ID ' + IntToStr(functionID));
    end
    else if (errorCode = 2) then begin
      raise ENotSupportedException.Create('Function ID ' + IntToStr(functionID) + ' is not supported');
    end
    else begin
      raise EUnknownErrorCodeException.Create('Function ID ' + IntToStr(functionID) + ' returned an unknown error');
    end;
  end
  else begin
    ipcon_.SendRequest(request);
  end;
end;

procedure TDevice.CheckValidity;
var request, response: TByteArray; deviceIdentifier: word;
begin
  if (replaced) then begin
    raise EDeviceReplacedException.Create('Device has been replaced');
  end;
  if (not uidValid) then begin
    raise EInvalidUIDException.Create('UID "' + uidString + '" is invalid');
  end;
  if (deviceIdentifierCheck = DEVICE_IDENTIFIER_CHECK_MATCH) then begin
    exit;
  end;
  deviceIdentifierMutex.Acquire;
  try
    if (deviceIdentifierCheck = DEVICE_IDENTIFIER_CHECK_PENDING) then begin
      request := (ipcon as TIPConnection).CreateRequestPacket(self, 255, 8); // GetIdentity
      response := SendRequest(request, 33);
      deviceIdentifier := LEConvertUInt16From(31, response);
      if (deviceIdentifier = deviceIdentifier_) then begin
        deviceIdentifierCheck := DEVICE_IDENTIFIER_CHECK_MATCH;
      end
      else begin
        deviceIdentifierCheck := DEVICE_IDENTIFIER_CHECK_MISMATCH;
        wrongDeviceDisplayName := GetDeviceDisplayName(deviceIdentifier);
      end;
    end;
    if (deviceIdentifierCheck = DEVICE_IDENTIFIER_CHECK_MISMATCH) then begin
      raise EWrongDeviceTypeException.Create('UID ' + uidString + ' belongs to a ' + wrongDeviceDisplayName +
                                             ' instead of the expected ' + deviceDisplayName);
    end;
  finally
    deviceIdentifierMutex.Release;
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

function TDeviceTable.Insert(const uid: longword; const device: TDevice; out replacedDevice: TDevice): boolean;
var len: longint; i: longint;
begin
  mutex.Acquire;
  try
    len := Length(uids);
    for i := 0 to len - 1 do begin
      if (uids[i] = uid) then begin
        replacedDevice := devices[i];
        devices[i] := device;
        result := true;
        exit;
      end;
    end;
    SetLength(uids, len + 1);
    SetLength(devices, len + 1);
    uids[len] := uid;
    devices[len] := device;
    result := false;
  finally
    mutex.Release;
  end;
end;

procedure TDeviceTable.Remove(const uid: longword);
var len: longint; i: longint; k: longint;
begin
  mutex.Acquire;
  try
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
  finally
    mutex.Release;
  end;
end;

function TDeviceTable.Get(const uid: longword): TDevice;
var len: longint; i: longint;
begin
  result := nil;
  mutex.Acquire;
  try
    len := Length(uids);
    for i := 0 to len - 1 do begin
      if (uids[i] = uid) then begin
        result := devices[i];
        exit;
      end;
    end;
  finally
    mutex.Release;
  end;
end;

end.
