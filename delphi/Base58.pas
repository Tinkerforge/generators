{
  Copyright (C) 2012 Matthias Bolte <matthias@tinkerforge.com>

  Redistribution and use in source and binary forms of this file,
  with or without modification, are permitted. See the Creative
  Commons Zero (CC0 1.0) License for more details.
}

unit Base58;

{$ifdef FPC}{$mode OBJFPC}{$endif}

interface
  function Base58Encode(const value: uint64): string;
  function Base58Decode(const encoded: string): uint64;

const
  BASE58_ALPHABET = '123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ';

implementation

function Base58Encode(const value: uint64): string;
var quotient, remainder, tmp: uint64;
begin
  result := '';
  tmp := value;
  while (tmp >= 58) do begin
    quotient := tmp div 58;
    remainder := tmp mod 58;
    result := Copy(BASE58_ALPHABET, remainder + 1, 1) + result;
    tmp := quotient;
  end;
  result := Copy(BASE58_ALPHABET, tmp + 1, 1) + result;
end;

function Base58Decode(const encoded: string): uint64;
var i, index: longint; base: uint64;
begin
  result := 0;
  base := 1;
  for i := Length(encoded) - 1 downto 0 do begin
    index := Pos(Copy(encoded, i + 1, 1), BASE58_ALPHABET) - 1;
    result := result + (index * base);
    base := 58 * base;
  end;
end;

end.
