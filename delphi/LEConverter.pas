{
  Copyright (C) 2012-2013 Matthias Bolte <matthias@tinkerforge.com>

  Redistribution and use in source and binary forms of this file,
  with or without modification, are permitted. See the Creative
  Commons Zero (CC0 1.0) License for more details.
}

unit LEConverter;

{$ifdef FPC}{$mode OBJFPC}{$H+}{$endif}

interface

type
  TByteArray = array of byte;
  PByteArray = ^TByteArray;
  PByte = ^byte;

  TFloatAsBytes = record
    case boolean of
      true:  (bytes : packed array [0..4] of byte);
      false: (float : single);
  end;

  procedure LEConvertInt8To(const value: shortint; const offset: longint; var data: TByteArray);
  procedure LEConvertUInt8To(const value: byte; const offset: longint; var data: TByteArray);
  procedure LEConvertInt16To(const value: smallint; const offset: longint; var data: TByteArray);
  procedure LEConvertUInt16To(const value: word; const offset: longint; var data: TByteArray);
  procedure LEConvertInt32To(const value: longint; const offset: longint; var data: TByteArray);
  procedure LEConvertUInt32To(const value: longword; const offset: longint; var data: TByteArray);
  procedure LEConvertInt64To(const value: int64; const offset: longint; var data: TByteArray);
  procedure LEConvertUInt64To(const value: uint64; const offset: longint; var data: TByteArray);
  procedure LEConvertFloatTo(const value: single; const offset: longint; var data: TByteArray);
  procedure LEConvertBooleanTo(const value: boolean; const offset: longint; var data: TByteArray);
  procedure LEConvertStringTo(const value: string; const offset: longint; const len: longint; var data: TByteArray);
  procedure LEConvertCharTo(const value: char; const offset: longint; var data: TByteArray);

  function LEConvertInt8From(const offset: longint; const data: TByteArray): shortint;
  function LEConvertUInt8From(const offset: longint; const data: TByteArray): byte;
  function LEConvertInt16From(const offset: longint; const data: TByteArray): smallint;
  function LEConvertUInt16From(const offset: longint; const data: TByteArray): word;
  function LEConvertInt32From(const offset: longint; const data: TByteArray): longint;
  function LEConvertUInt32From(const offset: longint; const data: TByteArray): longword;
  function LEConvertInt64From(const offset: longint; const data: TByteArray): int64;
  function LEConvertUInt64From(const offset: longint; const data: TByteArray): uint64;
  function LEConvertFloatFrom(const offset: longint; const data: TByteArray): single;
  function LEConvertBooleanFrom(const offset: longint; const data: TByteArray): boolean;
  function LEConvertStringFrom(const offset: longint; const len: longint; const data: TByteArray): string;
  function LEConvertCharFrom(const offset: longint; const data: TByteArray): char;

implementation

procedure LEConvertInt8To(const value: shortint; const offset: longint; var data: TByteArray);
begin
  LEConvertUInt8To(byte(value), offset, data);
end;

procedure LEConvertUInt8To(const value: byte; const offset: longint; var data: TByteArray);
begin
  data[offset] := value;
end;

procedure LEConvertInt16To(const value: smallint; const offset: longint; var data: TByteArray);
begin
  LEConvertUInt16To(word(value), offset, data);
end;

procedure LEConvertUInt16To(const value: word; const offset: longint; var data: TByteArray);
begin
  data[offset + 0] := byte((value shr 0) and $FF);
  data[offset + 1] := byte((value shr 8) and $FF);
end;

procedure LEConvertInt32To(const value: longint; const offset: longint; var data: TByteArray);
begin
  LEConvertUInt32To(longword(value), offset, data);
end;

procedure LEConvertUInt32To(const value: longword; const offset: longint; var data: TByteArray);
var i: longint;
begin
  for i := 0 to 3 do begin
    data[offset + i] := byte((value shr (i * 8)) and $FF);
  end;
end;

procedure LEConvertInt64To(const value: int64; const offset: longint; var data: TByteArray);
begin
  LEConvertUInt64To(uint64(value), offset, data);
end;

procedure LEConvertUInt64To(const value: uint64; const offset: longint; var data: TByteArray);
var i: longint;
begin
  for i := 0 to 7 do begin
    data[offset + i] := byte((value shr (i * 8)) and $FF);
  end;
end;

procedure LEConvertFloatTo(const value: single; const offset: longint; var data: TByteArray);
var i: longint; fab: TFloatAsBytes;
begin
  fab.float := value;
  for i := 0 to 3 do begin
    data[offset + i] := fab.bytes[i];
  end;
end;

procedure LEConvertBooleanTo(const value: boolean; const offset: longint; var data: TByteArray);
begin
  if (value) then begin
    data[offset] := 1;
  end
  else begin
    data[offset] := 0;
  end;
end;

procedure LEConvertStringTo(const value: string; const offset: longint; const len: longint; var data: TByteArray);
var i: longint;
begin
  i := 0;
  while ((i < len) and (i < Length(value))) do begin
    data[offset + i] := byte(value[i + 1]);
    i := i + 1;
  end;
  while (i < len) do begin
    data[offset + i] := 0;
    i := i + 1;
  end;
end;

procedure LEConvertCharTo(const value: char; const offset: longint; var data: TByteArray);
begin
  data[offset] := byte(value);
end;

function LEConvertInt8From(const offset: longint; const data: TByteArray): shortint;
begin
  result := shortint(LEConvertUInt8From(offset, data));
end;

function LEConvertUInt8From(const offset: longint; const data: TByteArray): byte;
begin
  result := data[offset];
end;

function LEConvertInt16From(const offset: longint; const data: TByteArray): smallint;
begin
  result := smallint(LEConvertUInt16From(offset, data));
end;

function LEConvertUInt16From(const offset: longint; const data: TByteArray): word;
begin
  result := word(data[offset + 0]) shl 0 or
            word(data[offset + 1]) shl 8;
end;

function LEConvertInt32From(const offset: longint; const data: TByteArray): longint;
begin
  result := longint(LEConvertUInt32From(offset, data));
end;

function LEConvertUInt32From(const offset: longint; const data: TByteArray): longword;
var i: longint;
begin
  result := 0;
  for i := 0 to 3 do begin
    result := result or (longword(data[offset + i]) shl (i * 8));
  end;
end;

function LEConvertInt64From(const offset: longint; const data: TByteArray): int64;
begin
  result := int64(LEConvertUInt64From(offset, data));
end;

function LEConvertUInt64From(const offset: longint; const data: TByteArray): uint64;
var i: longint;
begin
  result := 0;
  for i := 0 to 7 do begin
    result := result or (uint64(data[offset + i]) shl (i * 8));
  end;
end;

function LEConvertFloatFrom(const offset: longint; const data: TByteArray): single;
var i: longint; fab: TFloatAsBytes;
begin
  for i := 0 to 3 do begin
    fab.bytes[i] := data[offset + i];
  end;
  result := fab.float;
end;

function LEConvertBooleanFrom(const offset: longint; const data: TByteArray): boolean;
begin
  result := data[offset] <> 0;
end;

function LEConvertStringFrom(const offset: longint; const len: longint; const data: TByteArray): string;
var i: longint;
begin
  result := '';
  for i := offset to offset + len - 1 do begin
    if (data[i] = 0) then begin
      break;
    end;
    result := result + char(data[i]);
  end;
end;

function LEConvertCharFrom(const offset: longint; const data: TByteArray): char;
begin
  result := char(data[offset]);
end;

end.
