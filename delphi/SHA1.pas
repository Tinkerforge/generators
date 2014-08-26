{
  SHA-1 implementation based on two Public Domain implementations by

  Steve Reid <steve@edmweb.com>
  Jordan Russell <jr-2010@jrsoftware.org>

  100% Public Domain
}

unit SHA1;

{$ifdef FPC}{$mode OBJFPC}{$H+}{$endif}

interface

uses
  {$ifdef FPC}
   Sockets
  {$else}
   {$ifdef MSWINDOWS}
    WinSock
   {$else}
     Posix.ArpaInet
   {$endif}
  {$endif};

type
  TSHA1Block = array [0..63] of byte;
  TSHA1Digest = array [0..19] of byte;

  TSHA1 = record
    state: array [0..4] of longword;
    count: uint64;
    buffer: TSHA1Block;
  end;

  TLongWordConverter = packed record case longword of
    0: (bytes: array [0..3] of byte);
    1: (total: longword);
  end;

  procedure SHA1Init(var sha1: TSHA1);
  procedure SHA1Update(var sha1: TSHA1; const data: array of byte);
  function SHA1Final(var sha1: TSHA1): TSHA1Digest;

implementation

procedure SHA1Transform(var sha1: TSHA1; const buffer: TSHA1Block);
const K1 = $5A827999; K2 = $6ED9EBA1; K3 = $8F1BBCDC; K4 = $CA62C1D6;
var i, k: longint; converter: TLongWordConverter; temp, A, B, C, D, E: longword;
    W: array [0..79] of longword;
begin
  { convert buffer to 32-bit (big endian) numbers }
  for i := 0 to 15 do begin
    for k := 0 to 3 do begin
      converter.bytes[k] := buffer[i * 4 + k];
    end;
    W[i] := htonl(converter.total);
  end;
  for i := 16 to 79 do begin
    temp := W[i - 3] xor W[i - 8] xor W[i - 14] xor W[i - 16];
    W[i] := (temp shl 1) or (temp shr 31);
  end;
  A := sha1.state[0];
  B := sha1.state[1];
  C := sha1.state[2];
  D := sha1.state[3];
  E := sha1.state[4];
  for i := 0 to 19 do begin
    temp := ((A shl 5) or (A shr 27)) + (D xor (B and (C xor D))) + E + W[i] + K1;
    E := D;
    D := C;
    C := (B shl 30) or (B shr 2);
    B := A;
    A := temp;
  end;
  for i := 20 to 39 do begin
    temp := ((A shl 5) or (A shr 27)) + (B xor C xor D) + E + W[i] + K2;
    E := D;
    D := C;
    C := (B shl 30) or (B shr 2);
    B := A;
    A := temp;
  end;
  for i := 40 to 59 do begin
    temp := ((A shl 5) or (A shr 27)) + ((B and C) or (B and D) or (C and D)) + E + W[i] + K3;
    E := D;
    D := C;
    C := (B shl 30) or (B shr 2);
    B := A;
    A := temp;
  end;
  for i := 60 to 79 do begin
    temp := ((A shl 5) or (A shr 27)) + (B xor C xor D) + E + W[i] + K4;
    E := D;
    D := C;
    C := (B shl 30) or (B shr 2);
    B := A;
    A := temp;
  end;
  Inc(sha1.state[0], A);
  Inc(sha1.state[1], B);
  Inc(sha1.state[2], C);
  Inc(sha1.state[3], D);
  Inc(sha1.state[4], E);
end;

procedure SHA1Init(var sha1: TSHA1);
begin
  sha1.state[0] := $67452301;
  sha1.state[1] := $EFCDAB89;
  sha1.state[2] := $98BADCFE;
  sha1.state[3] := $10325476;
  sha1.state[4] := $C3D2E1F0;
  sha1.count := 0;
end;

procedure SHA1Update(var sha1: TSHA1; const data: array of byte);
var len, i, j: longword; buffer: TSHA1Block;
begin
  len := Length(data);
  j := longword((sha1.count shr 3) and 63);
  Inc(sha1.count, len shl 3);
  if ((j + len) > 63) then begin
    i := 64 - j;
    Move(data[0], sha1.buffer[j], i);
    SHA1Transform(sha1, sha1.buffer);
    while ((i + 63) < len) do begin
      Move(data[i], buffer[0], 64);
      SHA1Transform(sha1, buffer);
      Inc(i, 64);
    end;
    j := 0;
  end
  else begin
    i := 0;
  end;
  Move(data[i], sha1.buffer[j], len - i);
end;

function SHA1Final(var sha1: TSHA1): TSHA1Digest;
var count: array of byte; i: longint; pad: array of byte;
begin
  SetLength(count, 8);
  for i := 0 to 7 do begin
    count[i] := byte((sha1.count shr ((7 - (i and 7)) * 8)) and 255); { endian independent }
  end;
  SetLength(pad, 1);
  pad[0] := 128;
  SHA1Update(sha1, pad);
  pad[0] := 0;
  while ((sha1.count and 504) <> 448) do begin
    SHA1Update(sha1, pad);
  end;
  SHA1Update(sha1, count);
  for i := 0 to 19 do begin
    result[i] := byte((sha1.state[i shr 2] shr ((3 - (i and 3)) * 8)) and 255);
  end;
  FillChar(sha1, SizeOf(sha1), 0);
end;

end.
