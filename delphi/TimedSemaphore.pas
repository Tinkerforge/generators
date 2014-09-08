{
  Copyright (C) 2012, 2014 Matthias Bolte <matthias@tinkerforge.com>

  Redistribution and use in source and binary forms of this file,
  with or without modification, are permitted. See the Creative
  Commons Zero (CC0 1.0) License for more details.
}

unit TimedSemaphore;

{$ifdef FPC}
 {$mode OBJFPC}{$H+}
{$else}
 {$ifdef MACOS}{$define DELPHI_MACOS}{$endif}
{$endif}

interface

uses
  {$ifdef UNIX}CThreads,{$endif} {$ifdef MSWINDOWS}Windows{$else}SyncObjs{$endif};

type

{$ifndef MSWINDOWS}

  { Manual-Reset Event }
  TEventWrapper = class
  private
 {$ifdef DELPHI_MACOS}
    event: TEvent;
 {$else}
    event: PRTLEvent;
 {$endif}
  public
    constructor Create;
    destructor Destroy; override;
    procedure WaitFor(const timeout: longint);
    procedure SetEvent;
    procedure ResetEvent;
  end;

{$endif}

  { Semaphore with blocking lower bound, but without blocking upper bound }
  TTimedSemaphore = class
  private
    alive: boolean;
{$ifdef MSWINDOWS}
    handle: THandle;
{$else}
    mutex: TCriticalSection;
    event: TEventWrapper;
    available: longint;
{$endif}
  public
    constructor Create;
    destructor Destroy; override;
    function Acquire(const timeout: longint): boolean;
    procedure Release;
  end;

implementation

constructor TTimedSemaphore.Create;
begin
  alive := true;
{$ifdef MSWINDOWS}
  handle := CreateSemaphore(nil, 0, 2147483647, nil);
{$else}
  mutex := TCriticalSection.Create;
  event := TEventWrapper.Create;
  available := 0;
{$endif}
end;

destructor TTimedSemaphore.Destroy;
begin
  if (not alive) then begin
    exit;
  end;
  alive := false;
  Release;
{$ifdef MSWINDOWS}
  CloseHandle(handle);
{$else}
  event.Destroy;
  mutex.Destroy;
{$endif}
  inherited Destroy;
end;

function TTimedSemaphore.Acquire(const timeout: longint): boolean;
begin
{$ifdef MSWINDOWS}
  if (timeout < 0) then begin
    result := WaitForSingleObject(handle, INFINITE) = WAIT_OBJECT_0;
  end
  else begin
    result := WaitForSingleObject(handle, timeout) = WAIT_OBJECT_0;
  end;
{$else}
  result := false;
  mutex.Acquire;
  try
    if (available > 0) then begin
      Dec(available);
      result := true;
      if (available = 0) then begin
        event.ResetEvent();
      end;
    end;
  finally
    mutex.Release;
  end;
  if not result then begin
    event.WaitFor(timeout);
    mutex.Acquire;
    try
      if (available > 0) then begin
        Dec(available);
        result := true;
        if (available = 0) then begin
          event.ResetEvent();
        end;
      end;
    finally
      mutex.Release;
    end;
  end;
{$endif}
  if (not alive) then begin
    result := false;
  end;
end;

procedure TTimedSemaphore.Release;
begin
{$ifdef MSWINDOWS}
  ReleaseSemaphore(handle, 1, nil);
{$else}
  mutex.Acquire;
  try
    Inc(available);
  finally
    mutex.Release;
  end;
  event.SetEvent();
{$endif}
end;

{$ifndef MSWINDOWS}

{ TEventWrapper }
constructor TEventWrapper.Create;
begin
 {$ifdef DELPHI_MACOS}
  event := TEvent.Create(nil, true, false, '', false);
 {$else}
  event := RTLEventCreate; { This is a manual-reset event }
 {$endif}
end;

destructor TEventWrapper.Destroy;
begin
 {$ifdef DELPHI_MACOS}
  event.Destroy;
 {$else}
  RTLEventDestroy(event);
 {$endif}
  inherited Destroy;
end;

procedure TEventWrapper.WaitFor(const timeout: longint);
begin
  if (timeout < 0) then begin
 {$ifdef DELPHI_MACOS}
    event.WaitFor(INFINITE);
 {$else}
    RTLEventWaitFor(event);
 {$endif}
  end
  else begin
 {$ifdef DELPHI_MACOS}
    event.WaitFor(timeout);
 {$else}
    RTLEventWaitFor(event, timeout);
 {$endif}
  end;
end;

procedure TEventWrapper.SetEvent;
begin
 {$ifdef DELPHI_MACOS}
  event.SetEvent();
 {$else}
  RTLEventSetEvent(event);
 {$endif}
end;

procedure TEventWrapper.ResetEvent;
begin
 {$ifdef DELPHI_MACOS}
  event.ResetEvent();
 {$else}
  RTLEventResetEvent(event);
 {$endif}
end;

{$endif}

end.
