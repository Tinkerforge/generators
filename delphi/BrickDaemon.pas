{
  Copyright (C) 2014 Matthias Bolte <matthias@tinkerforge.com>

  Redistribution and use in source and binary forms of this file,
  with or without modification, are permitted. See the Creative
  Commons Zero (CC0 1.0) License for more details.
}

unit BrickDaemon;

{$ifdef FPC}{$mode OBJFPC}{$H+}{$endif}

interface

uses
  Device, LEConverter;

const
  BRICK_DAEMON_FUNCTION_GET_AUTHENTICATION_NONCE = 1;
  BRICK_DAEMON_FUNCTION_AUTHENTICATE = 2;

type
  TArray0To3OfUInt8 = array [0..3] of byte;
  TArray0To19OfUInt8 = array [0..19] of byte;

  TBrickDaemon = class(TDevice)
  public
    constructor Create(const uid__: string; ipcon_: TObject);
    function GetAuthenticationNonce: TArray0To3OfUInt8; virtual;
    procedure Authenticate(const clientNonce: TArray0To3OfUInt8; const digest: TArray0To19OfUInt8); virtual;
    procedure GetIdentity(out uid: string; out connectedUid: string; out position: char; out hardwareVersion: TVersionNumber; out firmwareVersion: TVersionNumber; out deviceIdentifier: word); override;
  end;

implementation

uses
  IPConnection;

constructor TBrickDaemon.Create(const uid__: string; ipcon_: TObject);
begin
  inherited Create(uid__, ipcon_);
  apiVersion[0] := 2;
  apiVersion[1] := 0;
  apiVersion[2] := 0;
  responseExpected[BRICK_DAEMON_FUNCTION_GET_AUTHENTICATION_NONCE] := DEVICE_RESPONSE_EXPECTED_ALWAYS_TRUE;
  responseExpected[BRICK_DAEMON_FUNCTION_AUTHENTICATE] := DEVICE_RESPONSE_EXPECTED_TRUE;
end;

function TBrickDaemon.GetAuthenticationNonce: TArray0To3OfUInt8;
var request, response: TByteArray; i: longint;
begin
  request := (ipcon as TIPConnection).CreateRequestPacket(self, BRICK_DAEMON_FUNCTION_GET_AUTHENTICATION_NONCE, 8);
  response := SendRequest(request);
  for i := 0 to 3 do result[i] := LEConvertUInt8From(8 + i, response);
end;

procedure TBrickDaemon.Authenticate(const clientNonce: TArray0To3OfUInt8; const digest: TArray0To19OfUInt8);
var request: TByteArray; i: longint;
begin
  request := (ipcon as TIPConnection).CreateRequestPacket(self, BRICK_DAEMON_FUNCTION_AUTHENTICATE, 32);
  for i := 0 to Length(clientNonce) - 1 do LEConvertUInt8To(clientNonce[i], 8 + i, request);
  for i := 0 to Length(digest) - 1 do LEConvertUInt8To(digest[i], 12 + i, request);
  SendRequest(request);
end;

procedure TBrickDaemon.GetIdentity(out uid: string; out connectedUid: string; out position: char; out hardwareVersion: TVersionNumber; out firmwareVersion: TVersionNumber; out deviceIdentifier: word);
var i: longint;
begin
  uid := '';
  connectedUid := '';
  position := char(0);
  for i := 0 to 2 do hardwareVersion[i] := 0;
  for i := 0 to 2 do firmwareVersion[i] := 0;
  deviceIdentifier := 0;
end;

end.
