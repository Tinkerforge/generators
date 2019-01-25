program ExampleAuthenticate;

{$ifdef MSWINDOWS}{$apptype CONSOLE}{$endif}
{$ifdef FPC}{$mode OBJFPC}{$H+}{$endif}

uses
  SysUtils, IPConnection, Device;

type
  TExample = class
  private
    ipcon: TIPConnection;
  public
    procedure ConnectedCB(sender: TIPConnection; const connectReason: byte);
    procedure EnumerateCB(sender: TIPConnection;
                          const uid: string; const connectedUid: string; const position: char;
                          const hardwareVersion: TVersionNumber; const firmwareVersion: TVersionNumber;
                          const deviceIdentifier: word; const enumerationType: byte);
    procedure Execute;
  end;

const
  HOST = 'localhost';
  PORT = 4223;
  SECRET = 'My Authentication Secret!';

var
  e: TExample;

{ Authenticate each time the connection got (re-)established }
procedure TExample.ConnectedCB(sender: TIPConnection; const connectReason: byte);
begin
  case connectReason of
    IPCON_CONNECT_REASON_REQUEST:
    begin
      WriteLn('Connected by request');
    end;
    IPCON_CONNECT_REASON_AUTO_RECONNECT:
    begin
      WriteLn('Auto-Reconnect');
    end;
  end;
  { Authenticate first... }
  try
    sender.Authenticate(SECRET);
    WriteLn('Authentication succeeded');
  except
    WriteLn('Could not authenticate');
    exit;
  end;

  { ...reenable auto reconnect mechanism, as described below... }
  sender.SetAutoReconnect(true);

  { ...then trigger enumerate }
  sender.Enumerate;
end;

{ Print incoming enumeration }
procedure TExample.EnumerateCB(sender: TIPConnection;
                               const uid: string; const connectedUid: string; const position: char;
                               const hardwareVersion: TVersionNumber; const firmwareVersion: TVersionNumber;
                               const deviceIdentifier: word; const enumerationType: byte);
begin
  WriteLn('UID: ' + uid + ', Enumerate Type: ' + IntToStr(enumerationType));
end;

procedure TExample.Execute;
begin
  { Create IP Connection }
  ipcon := TIPConnection.Create;

  { Disable auto reconnect mechanism, in case we have the wrong secret. If the authentication is successful, reenable it. }
  ipcon.SetAutoReconnect(false);

  { Register connected callback to "ConnectedCB" }
  ipcon.OnConnected := {$ifdef FPC}@{$endif}ConnectedCB;

  { Register enumerate callback to "EnumerateCB" }
  ipcon.OnEnumerate := {$ifdef FPC}@{$endif}EnumerateCB;

  { Connect to brickd }
  ipcon.Connect(HOST, PORT);

  WriteLn('Press key to exit');
  ReadLn;
  ipcon.Destroy; { Calls ipcon.Disconnect internally }
end;

begin
  e := TExample.Create;
  e.Execute;
  e.Destroy;
end.
