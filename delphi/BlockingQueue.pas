{
  Copyright (C) 2012 Matthias Bolte <matthias@tinkerforge.com>

  Redistribution and use in source and binary forms of this file,
  with or without modification, are permitted. See the Creative
  Commons Zero (CC0 1.0) License for more details.
}

unit BlockingQueue;

{$ifdef FPC}{$mode OBJFPC}{$H+}{$endif}

interface

uses
  Contnrs, SyncObjs, LEConverter, TimedSemaphore;

type
  TBlockingQueue = class
  private
    mutex: TCriticalSection;
    semaphore: TTimedSemaphore;
    kinds: TQueue;
    items: TQueue;
  public
    constructor Create;
    destructor Destroy; override;
    procedure Enqueue(const kind: byte; const item: TByteArray);
    function Dequeue(out kind: byte; out item: TByteArray; const timeout: longint): boolean;
  end;

implementation

constructor TBlockingQueue.Create;
begin
  mutex := TCriticalSection.Create;
  semaphore := TTimedSemaphore.Create;
  kinds := TQueue.Create;
  items := TQueue.Create;
end;

destructor TBlockingQueue.Destroy;
var pkind: PByte; pitem: PByteArray;
begin
  mutex.Acquire;
  try
    while (kinds.Count > 0) do begin
      pkind := kinds.Pop;
      Dispose(pkind);
    end;
    while (items.Count > 0) do begin
      pitem := items.Pop;
      Dispose(pitem);
    end;
  finally
    mutex.Release;
  end;
  mutex.Destroy;
  semaphore.Destroy;
  kinds.Destroy;
  items.Destroy;
  inherited Destroy;
end;

procedure TBlockingQueue.Enqueue(const kind: byte; const item: TByteArray);
var pkind: PByte; pitem: PByteArray;
begin
  mutex.Acquire;
  try
    New(pkind);
    pkind^ := kind;
    kinds.Push(pkind);
    New(pitem);
    pitem^ := item;
    items.Push(pitem);
    semaphore.Release;
  finally
    mutex.Release;
  end;
end;

function TBlockingQueue.Dequeue(out kind: byte; out item: TByteArray; const timeout: longint): boolean;
var pkind: PByte; pitem: PByteArray;
begin
  result := false;
  if (semaphore.Acquire(timeout)) then begin
    mutex.Acquire;
    try
      pkind := kinds.Pop;
      kind := pkind^;
      Dispose(pkind);
      pitem := items.Pop;
      item := pitem^;
      Dispose(pitem);
      result := true;
    finally
      mutex.Release;
    end;
  end;
end;

end.
