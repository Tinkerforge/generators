#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Rust Generator
Copyright (C) 2018 Erik Fleckstein <erik@tinkerforge.com>

rust_common.py: Common Library for generation of Rust bindings and documentation

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

sys.path.append(os.path.split(os.getcwd())[0])
import common

class RustDevice(common.Device):
    def get_rust_name(self):
        return self.get_name().camel + self.get_category().camel
    def specialize_rust_doc_function_links(self, text):
        specialized = []
        def specializer(packet, high_level):
            if packet.get_type() == 'callback':
                name = 'get_{0}_receiver'.format(packet.get_name(skip=-2 if high_level else 0).under)                
            else:
                name = packet.get_name(skip=-2 if high_level else 0).under
            result = '[`{0}`]'.format(name)
            specialized.append(result + ": #method."+name)
            return result
        result_text = self.specialize_doc_rst_links(text, specializer)
        result = (result_text, [link for link in specialized if link.split(':')[0] in result_text])
        return result

class RustPacket(common.Packet):
    def get_return_type(self):
        returns = self.get_elements(direction='out')
        if len(returns) == 0:
            return "()"
        if len(returns) == 1:
            if self.has_high_level():
                return self.get_rust_type_name()
            else:
                return returns[0].get_rust_type()            
        
        return self.get_rust_type_name()

    def get_stream_info_return_type(self):
        returns = [elem for elem in self.get_elements(direction='out') if elem.get_level() == 'low']
        if len(returns) == 0:
            return "()"
        if len(returns) == 1:
            return returns[0].get_rust_type()            
        
        return self.get_rust_type_name()

    def get_rust_name(self, skip=0):
        return self.get_name(skip=skip).camel

    def get_rust_type_name(self, skip=0):        
        name = self.get_rust_name(skip)

        if self.get_name(skip).under.startswith('get_'):
            name = name[3:]
        if self.get_name(skip).under.startswith('is_'):
            name = name[2:]

        return name

    def get_rust_derivable_traits(self, high_level_only=False):
        filtered_returns = self.get_elements(direction='out') if not high_level_only else [ret for ret in self.get_elements(direction='out') if ret.get_level() != 'low']        
        result = ["Clone"]
        
        #String can be cloned, but not copied, so don't derive copy if the struct will contain strings
        if all("String" not in x.get_rust_type() for x in filtered_returns):
            result.append("Copy")

        #Arrays with more than 32 entries don't implement any traits except clone and copy
        if all(x.get_cardinality() <= 32 for x in filtered_returns):
            result += ["Debug", "Default", "PartialEq"]
            #Floats implement PartialEq only, as NaN != NaN
            if all("f" not in x.get_rust_type() for x in filtered_returns):
                result += ["Eq", "Hash"]

        return result

    def get_rust_formatted_doc(self):
        text = common.select_lang(self.get_doc_text())

        # handle links      
        text = text.replace(":ref:", "")
        text = text.replace(":func:", "")
        #if ":ref:" in text:
            #substitutions = {
            #    "device_identifier": "https://www.tinkerforge.com/en/doc/Software/Device_Identifier.html",
            #    "tutorial_authentication": "https://www.tinkerforge.com/en/doc/Tutorials/Tutorial_Authentication/Tutorial.html",
            #    "gps_bricklet_fix_led": "https://www.tinkerforge.com/en/doc/Hardware/Bricklets/GPS.html#fix-led",
            #    "gps_v2_bricklet_fix_led": "https://www.tinkerforge.com/en/doc/Hardware/Bricklets/GPS_V2.html#fix-led",
            #    "led_strip_bricklet_ram_constraints": "https://www.tinkerforge.com/en/doc/Hardware/Bricklets/LED_Strip.html#ram-constraints",
            #}
            #for match in  re.finditer(":ref:`([^<]+) <([^>]+)>`", text):
            #    link_text, url = match.groups()
            #    subst = substitutions[url]
            #    re.sub("`("+link_text+") <"+url+">`", "[\g<1>]("+subst+")", text)

        text = re.sub("`([^<]+) <([^>]+)>`", r"[\g<1>](\g<2>)", text)


        # handle tables
        lines = text.split('\n')
        replaced_lines = []
        in_table_head = False
        in_table_body = False
        col_count = 0
        for line in lines:  
            line = line.replace('"', '')          
            if line.strip() == '.. csv-table::':
                in_table_head = True
            elif line.strip().startswith(':header: ') and in_table_head:
                line = line[len(':header: '):]
                col_count = line.count(",") + 1
                line = line.replace(",", "|")
                replaced_lines.append(line)
            elif line.strip().startswith(':widths:') and in_table_head:
                pass
            elif len(line.strip()) == 0 and in_table_head:
                in_table_head = False
                in_table_body = True

                replaced_lines.append("|".join([" --- "] * col_count))
            elif in_table_head:
                replaced_lines.append(line.replace(",", "|"))
            elif len(line.strip()) == 0 and in_table_body:
                in_table_body = False
                replaced_lines.append('')
            elif in_table_body:
                replaced_lines.append(line.replace(",", "|"))
            else:
                replaced_lines.append(line)

        text = '\n'.join(replaced_lines)
        text, links = self.get_device().specialize_rust_doc_function_links(text)
        text += '\n' + '\n'.join(links)

        text = text.replace('Callback ', 'Listener ')
        text = text.replace(' Callback', ' Listener')
        text = text.replace('callback ', 'listener ')
        text = text.replace(' callback', ' listener')
        text = text.replace('.. note::', '# Note')
        text = text.replace('.. warning::', '# Warning')

        def format_parameter(name):
            return '\\c {0}'.format(name) # FIXME

        text = common.handle_rst_param(text, format_parameter)
        text = common.handle_rst_word(text)
        text = common.handle_rst_substitutions(text, self)
        text += common.format_since_firmware(self.get_device(), self)

        return '/// ' + '\n\t/// '.join(text.strip().split('\n'))


class RustElement(common.Element):
    def get_rust_name(self):
        blacklist = ["abstract", "alignof", "as", "become", "box", "break", "const", "continue", "crate", "do", "else", "enum", "extern", "false", "final", "fn", "for", "if", "impl", "in", "let", "loop", "macro", "match", "mod", "move", "mut", "offsetof", "override", "priv", "proc", "pub", "pure", "ref", "return", "Self", "self", "sizeof", "static", "struct", "super", "trait", "true", "type", "typeof", "unsafe", "unsized", "use", "virtual", "where", "while", "yield"]
        name = self.get_name().under
        if name in blacklist:
            return name + "_"
        return name

    def get_rust_type(self, ignore_cardinality=False):
        if self.get_type() == 'string':
            return 'String'
        elif self.get_type() in ('int8', 'int16', 'int32', 'int64', 'uint8', 'uint16', 'uint32', 'uint64'):
            element_type = self.get_type().replace('uint', 'u').replace('int', 'i')            
        elif self.get_type() == 'bool':
            element_type = 'bool'
        elif self.get_type() == 'float':
            element_type = 'f32'
        else:
            element_type = self.get_type()
        if self.get_cardinality() > 1 and not ignore_cardinality:
            return "[{type}; {count}]".format(type=element_type, count=self.get_cardinality())
        else:
            return element_type

rust_types = {
    'int8':   'i8',
    'uint8':  'u8',
    'int16':  'i16',
    'uint16': 'u16',
    'int32':  'i32',
    'uint32': 'u32',
    'int64':  'i64',
    'uint64': 'u64',
    'float':  'f32',
    'bool':   'bool',
    'char':   'char',
    'string': 'String'
}

def get_rust_type(type_, cardinality):
    rust_type = rust_types[type_]

    if cardinality != 1 and type_ != 'string':
        rust_type = '[{}]'.format(rust_type)

    return rust_type