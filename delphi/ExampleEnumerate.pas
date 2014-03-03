program ExampleEnumerate;

{$ifdef MSWINDOWS}{$apptype CONSOLE}{$endif}
{$ifdef FPC}{$mode OBJFPC}{$H+}{$endif}

uses
  SysUtils, IPConnection, Device;

type
  TExample = class
  private
    ipcon: TIPConnection;
  public
    procedure EnumerateCB(sender: TIPConnection;
                          const uid: string; const connectedUid: string; const position: char;
                          const hardwareVersion: TVersionNumber; const firmwareVersion: TVersionNumber;
                          const deviceIdentifier: word; const enumerationType: byte);
    procedure Execute;
  end;

const
  HOST = 'localhost';
  PORT = 4223;

var
  e: TExample;

{ Print incoming enumeration }
procedure TExample.EnumerateCB(sender: TIPConnection;
                               const uid: string; const connectedUid: string; const position: char;
                               const hardwareVersion: TVersionNumber; const firmwareVersion: TVersionNumber;
                               const deviceIdentifier: word; const enumerationType: byte);
begin
  WriteLn('UID:               ' + uid);
  WriteLn('Enumerate Type:    ' + IntToStr(enumerationType));

  if (enumerationType <> IPCON_ENUMERATION_TYPE_DISCONNECTED) then begin
    WriteLn('Connected UID:     ' + connectedUid);
    WriteLn('Position:          ' + position);
    WriteLn('Hardware Version:  ' + IntToStr(hardwareVersion[0]) + '.' +
                                    IntToStr(hardwareVersion[1]) + '.' +
                                    IntToStr(hardwareVersion[2]));
    WriteLn('Firmware Version:  ' + IntToStr(firmwareVersion[0]) + '.' +
                                    IntToStr(firmwareVersion[1]) + '.' +
                                    IntToStr(firmwareVersion[2]));
    WriteLn('Device Identifier: ' + IntToStr(deviceIdentifier));
  end;

  WriteLn('');
end;

procedure TExample.Execute;
begin
  { Create connection and connect to brickd }
  ipcon := TIPConnection.Create;
  ipcon.Connect(HOST, PORT);

  { Register enumeration callback to "EnumerateCB }
  ipcon.OnEnumerate := {$ifdef FPC}@{$endif}EnumerateCB;

  ipcon.Enumerate;

  WriteLn('Press key to exit');
  ReadLn;
  ipcon.Destroy; { Calls ipcon.Disconnect internally }
end;

begin
  e := TExample.Create;
  e.Execute;
  e.Destroy;
end.
