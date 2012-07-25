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
    queue: TQueue;
  public
    constructor Create;
    destructor Destroy; override;
    procedure Enqueue(const item: TByteArray);
    function Dequeue(out item: TByteArray; const timeout: longint): boolean;
  end;

implementation

constructor TBlockingQueue.Create;
begin
  mutex := TCriticalSection.Create;
  semaphore := TTimedSemaphore.Create;
  queue := TQueue.Create;
end;

destructor TBlockingQueue.Destroy;
var p: PByteArray;
begin
  mutex.Acquire;
  try
    while (queue.Count > 0) do begin
      p := queue.Pop;
      Dispose(p);
    end;
  finally
    mutex.Release;
  end;
  mutex.Destroy;
  semaphore.Destroy;
  queue.Destroy;
  inherited Destroy;
end;

procedure TBlockingQueue.Enqueue(const item: TByteArray);
var p: PByteArray;
begin
  mutex.Acquire;
  try
    New(p);
    p^ := item;
    queue.Push(p);
    semaphore.Release;
  finally
    mutex.Release;
  end;
end;

function TBlockingQueue.Dequeue(out item: TByteArray; const timeout: longint): boolean;
var p: PByteArray;
begin
  result := false;
  if (semaphore.Acquire(timeout)) then begin
    mutex.Acquire;
    try
      p := queue.Pop;
      item := p^;
      Dispose(p);
      result := true;
    finally
      mutex.Release;
    end;
  end;
end;

end.
