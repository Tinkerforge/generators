#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Mathematica Bindings Generator
Copyright (C) 2017 Matthias Bolte <matthias@tinkerforge.com>

txt2nb.py: Convert Mathematica code from .txt to .nb

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public
License along with this program; if not, write to the
Free Software Foundation, Inc., 59 Temple Place - Suite 330,
Boston, MA 02111-1307, USA.
"""

import sys
import os
import re
import functools

parsers = []

def escape_string(raw):
    escaped = ''

    if sys.hexversion < 0x03000000:
        chars = unicode(raw, 'utf-8')
    else:
        chars = raw

    for c in chars:
        cp = ord(c)

        if cp < 32 or cp > 126:
            if cp < 256:
                escaped += '\\.{0:02x}'.format(cp)
            else:
                escaped += '\\:{0:04x}'.format(cp)
        else:
            escaped += c

    return escaped

def parse_newline(line):
    if line.startswith('\t'):
        return ['"\\n"', '"\\[IndentingNewLine]"'], line[1:]

    return None, line

def parse_continuation(line):
    if line.startswith('\r'):
        return '"\\[IndentingNewLine]"', line[1:]

    return None, line

def parse_call(line):
    parsed_identifier, identifier_tail = parse_identifier(line)

    if parsed_identifier != None:
        parsed_block, block_tail = parse_block('[', ']', identifier_tail)

        if parsed_block != None:
            return (parsed_identifier,) + tuple(parsed_block), block_tail

    return None, line

def parse_identifier(line):
    m = re.match('^([A-Za-z][A-Za-z0-9`]*_?)(.*)', line)

    if m != None:
        return '"{0}"'.format(m.group(1)), m.group(2)

    return None, line

def parse_number(line):
    m = re.match('^([0-9]+(?:\.[0-9]+)?)(.*)', line)

    if m != None:
        return '"{0}"'.format(m.group(1)), m.group(2)

    return None, line

def parse_operator(line):
    m = re.match('^(<=|>=|!=|==|=|:=|\+=|\+\+|\+|-=|--|-|\*|/|<>|<|>|,|@|;;|;)(.*)', line)

    if m != None:
        if m.group(1) == '=':
            parsed, tail = parse_one(m.group(2))

            if type(parsed) == list:
                parsed = tuple(parsed)

            return ['"{0}"'.format(m.group(1)), parsed], tail

        return '"{0}"'.format(m.group(1)), m.group(2)

    return None, line

def parse_comment(line):
    if line.startswith('(*'):
        i = line.find('*)')
        tail = line[i + 2:]
        parts = line[2:i].split('"')
        comment = ''

        if len(parts) == 1:
            comment = parts[0]
        else:
            for i, part in enumerate(parts[:-1]):
                comment += part

                if i % 2 == 0:
                    comment += '", "\\"\\<'
                else:
                    comment += '\\>\\"", "'

            comment += parts[-1]

            if len(parts) % 2 == 0:
                comment += '\\>'

        return ('"(*"', '"{0}"'.format(escape_string(comment)), '"*)"'), tail

    return None, line

def parse_string(line):
    if line.startswith('"'):
        i = line.find('"', 1)
        tail = line[i + 1:]

        return '"\\"\\<{0}\\>\\""'.format(escape_string(line[1:i])), tail

    return None, line

def parse_block(left, right, line):
    if line.startswith(left):
        result = []
        tail = line[len(left):]

        while True:
            parsed, tail = parse_all(tail, until=',')

            if parsed == None:
                break

            if type(parsed) == list:
                result.append(tuple(parsed))
            else:
                result.append(parsed)

            if tail.startswith(','):
                result.append('","')
                tail = tail[1:]

        if not tail.startswith(right):
            raise Exception('missing {0} in tail {1} of line {2}'.format(right, repr(tail), repr(line)))

        tail = tail[len(right):]

        if len(result) == 0:
            return ['"{0}"'.format(left), '"{0}"'.format(right)], tail

        return ['"{0}"'.format(left), tuple(result), '"{0}"'.format(right)], tail

    return None, line

parsers = [
    parse_newline,
    parse_continuation,
    parse_call,
    parse_identifier,
    parse_number,
    parse_operator,
    parse_comment,
    parse_string,
    functools.partial(parse_block, '[', ']'),
    functools.partial(parse_block, '{', '}'),
]

def parse_one(line):
    for parser in parsers:
        parsed, tail = parser(line)

        if parsed != None:
            return parsed, tail

    return None, line

def parse_all(line, until=None):
    result = []
    old_tail = None
    new_tail = line

    while old_tail != new_tail and (until == None or not new_tail.startswith(until)):
        old_tail = new_tail

        parsed, new_tail = parse_one(old_tail)

        if parsed != None:
            if type(parsed) == list:
                result += parsed
            else:
                result.append(parsed)

    if len(result) == 0:
        result = None

    try:
        i = result.index('"=="')
    except:
        pass
    else:
        result = [tuple(result[:i]), '"=="', tuple(result[i + 1:])]

    return result, new_tail

def flatten(parsed):
    flattened = []

    for item in parsed:
        if type(item) == tuple:
            flattened.append(flatten(item))
        else:
            flattened.append(item)

    if len(flattened) > 1:
        return 'RowBox[{{{0}}}]'.format(', '.join(flattened))

    if len(flattened) == 1:
        return flattened[0]

    return ''

def txt2nb(txt_path):
    txt = open(txt_path, 'r')

    nb_path = os.path.splitext(txt_path)[0] # assuming name ends with .nb.txt
    nb = open(nb_path, 'w')
    nb.write('Notebook[{\n Cell[\n  BoxData[{')

    boxdata_first = True
    ignore_empty_line = False
    lines1 = []
    lines2 = []

    for line in txt.readlines():
        line = line.rstrip().replace('\\', '\\\\')

        if line.startswith(' ') or line.startswith(']'):
            lines1[-1] += '\r' + line.strip()
        else:
            lines1.append(line)

    for line in lines1:
        if line.startswith('\r'):
            lines2[-1] += '\t' + line[1:]
        else:
            lines2.append(line)

    for line in lines2:
        if len(line) == 0:
            if not ignore_empty_line:
                if boxdata_first:
                    boxdata_first = False
                else:
                    nb.write(',')

                nb.write('\n   RowBox[{"\n"}]')
            else:
                ignore_empty_line = False

            continue

        parsed, tail = parse_all(line, None)

        if parsed == None:
            raise Exception('could not parse line: {0}'.format(repr(line)))

        if len(tail) > 0:
            raise Exception('could not parse tail: {0}'.format(repr(tail)))

        if boxdata_first:
            boxdata_first = False
        else:
            nb.write(',')

        nb.write('\n   {0}'.format(flatten(parsed)))

        if 'LoadNETAssembly' in line:
            nb.write('\n  }], "Input"\n ],\n Cell[\n  BoxData[{')
            boxdata_first = True
            ignore_empty_line = True

    nb.write('\n  }], "Input"\n ]\n}]\n')

if __name__ == '__main__':
    txt2nb(sys.argv[1])
