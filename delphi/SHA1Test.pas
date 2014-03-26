program SHA1Test;

{$ifdef MSWINDOWS}{$apptype CONSOLE}{$endif}
{$ifdef FPC}{$mode OBJFPC}{$H+}{$endif}

uses
  SysUtils, SHA1;

var
  ctx: TSHA1;
  buffer: array of byte;
  digest: TSHA1Digest;

begin
  SetLength(buffer, 3);
  buffer[0] := byte('a');
  buffer[1] := byte('b');
  buffer[2] := byte('c');

  SHA1Init(ctx);
  SHA1Update(ctx, buffer);
  digest := SHA1Final(ctx);

  WriteLn('expected A9 99 3E 36 47    6 81 6A BA 3E   25 71 78 50 C2   6C 9C D0 D8 9D');
  WriteLn(Format('got      %02x %02x %02x %02x %02x   %02x %02x %02x %02x %02x   %02x %02x %02x %02x %02x   %02x %02x %02x %02x %02x',
          [digest[ 0], digest[ 1], digest[ 2], digest[ 3], digest[ 4], digest[ 5], digest[ 6], digest[ 7], digest[ 8], digest[ 9],
           digest[10], digest[11], digest[12], digest[13], digest[14], digest[15], digest[16], digest[17], digest[18], digest[19]]));
end.
