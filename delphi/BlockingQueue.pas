{
  Copyright (C) 2012 Matthias Bolte <matthias@tinkerforge.com>

  Redistribution and use in source and binary forms of this file,
  with or without modification, are permitted. See the Creative
  Commons Zero (CC0 1.0) License for more details.
}

unit BlockingQueue;

{$ifdef FPC}{$mode OBJFPC}{$H+}{$endif}

{$ifndef FPC}
 {$ifdef CONDITIONALEXPRESSIONS}
  {$if CompilerVersion >= 14.0}
   {$define USE_GENERICS}
  {$ifend}
 {$endif}
{$endif}

interface

uses
{$ifdef USE_GENERICS}
  Generics.Collections,
{$else}
  Contnrs,
{$endif}
  SyncObjs, LEConverter, TimedSemaphore;

type
  TBlockingQueue = class
  private
    mutex: TCriticalSection;
    semaphore: TTimedSemaphore;
{$ifdef USE_GENERICS}
    kinds: TQueue<PByte>;
    items: TQueue<PByteArray>;
{$else}
    kinds: TQueue;
    items: TQueue;
{$endif}
  public
    constructor Create;
    destructor Destroy; override;
    procedure Enqueue(const kind: byte; const item: TByteArray);
    function Dequeue(out kind: byte; out item: TByteArray; const timeout: longint): boolean;
  end;

implementation

constructor TBlockingQueue.Create;
begin
  inherited;
  mutex := TCriticalSection.Create;
  semaphore := TTimedSemaphore.Create;
{$ifdef USE_GENERICS}
  kinds := TQueue<PByte>.Create;
  items := TQueue<PByteArray>.Create;
{$else}
  kinds := TQueue.Create;
  items := TQueue.Create;
{$endif}
end;

destructor TBlockingQueue.Destroy;
var pkind: PByte; pitem: PByteArray;
begin
  mutex.Acquire;
  try
    while (kinds.Count > 0) do begin
{$ifdef USE_GENERICS}
      pkind := kinds.Dequeue;
{$else}
      pkind := kinds.Pop;
{$endif}
      Dispose(pkind);
    end;
    while (items.Count > 0) do begin
{$ifdef USE_GENERICS}
      pitem := items.Dequeue;
{$else}
      pitem := items.Pop;
{$endif}
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
{$ifdef USE_GENERICS}
    kinds.Enqueue(pkind);
{$else}
    kinds.Push(pkind);
{$endif}
    New(pitem);
    pitem^ := item;
{$ifdef USE_GENERICS}
    items.Enqueue(pitem);
{$else}
    items.Push(pitem);
{$endif}
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
{$ifdef USE_GENERICS}
      pkind := kinds.Dequeue;
{$else}
      pkind := kinds.Pop;
{$endif}
      kind := pkind^;
      Dispose(pkind);
{$ifdef USE_GENERICS}
      pitem := items.Dequeue;
{$else}
      pitem := items.Pop;
{$endif}
      item := pitem^;
      Dispose(pitem);
      result := true;
    finally
      mutex.Release;
    end;
  end;
end;

end.
