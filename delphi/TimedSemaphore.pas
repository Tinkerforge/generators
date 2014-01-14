{
  Copyright (C) 2012 Matthias Bolte <matthias@tinkerforge.com>

  Redistribution and use in source and binary forms of this file,
  with or without modification, are permitted. See the Creative
  Commons Zero (CC0 1.0) License for more details.
}

unit TimedSemaphore;

{$ifdef FPC}{$mode OBJFPC}{$H+}{$endif}

interface

uses
  {$ifdef UNIX}CThreads,{$endif} {$ifdef MSWINDOWS}Windows{$else}SyncObjs{$endif};

type
  { Semaphore with blocking lower bound, but without blocking upper bound }
  TTimedSemaphore = class
  private
    alive: boolean;
{$ifdef MSWINDOWS}
    handle: THandle;
{$else}
    mutex: TCriticalSection;
    event: PRTLEvent;
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
  event := RTLEventCreate;
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
  RTLeventDestroy(event);
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
        RTLeventResetEvent(event);
      end;
    end;
  finally
    mutex.Release;
  end;
  if not result then begin
    if (timeout < 0) then begin
      RTLeventWaitFor(event);
    end
    else begin
      RTLeventWaitFor(event, timeout);
    end;
    mutex.Acquire;
    try
      if (available > 0) then begin
        Dec(available);
        result := true;
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
  RTLeventSetEvent(event);
{$endif}
end;

end.
