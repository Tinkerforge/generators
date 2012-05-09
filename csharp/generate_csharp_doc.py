#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
C# Documentation Generator
Copyright (C) 2012 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generator_csharp_doc.py: Generator for C# documentation

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

import datetime
import sys
import os
import shutil
import subprocess
import glob
import re

com = None
lang = 'en'
file_path = ''

gen_text = """..
 #############################################################
 # This file was automatically generated on {0}.      #
 #                                                           #
 # If you have a bugfix for this file and want to commit it, #
 # please fix the bug in the generator. You can find a link  #
 # to the generator git on tinkerforge.com                   #
 #############################################################
"""

def shift_right(text, n):
    return text.replace('\n', '\n' + ' '*n)

def fix_links(text):
    link = ':csharp:func:`{2}() <{0}{1}::{2}>`' 

    cls = com['name'][0]
    for packet in com['packets']:
        name_false = ':func:`{0}`'.format(packet['name'][0])
        name = packet['name'][0] 
        name_right = link.format(com['type'], cls, name)

        text = text.replace(name_false, name_right)

    text = text.replace(":word:`parameter`", "parameter")
    text = text.replace(":word:`parameters`", "parameters")

    return text

def find_examples():
    path = file_path
    start_path = path.replace('/generators/csharp', '')
    board = '{0}-{1}'.format(com['name'][1], com['type'].lower())
    board = board.replace('_', '-')
    board_path = os.path.join(start_path, board, 'software/examples/csharp')
    files = []
    for f in os.listdir(board_path):
        if f.startswith('Example') and f.endswith('.cs'):
            f_dir = '{0}/{1}'.format(board_path, f)
            lines = 0
            for line in open(os.path.join(f, f_dir)):
                lines += 1
            files.append((f, f_dir, lines))

    files.sort(lambda i, j: cmp(i[2], j[2]))

    return files
   
def copy_examples(cf):
    path = file_path
    doc_path = '{0}/doc'.format(path)
    print('  * Copying examples:')
    for f in cf:
        doc_dest = '{0}/{1}'.format(doc_path, f[1])
        doc_src = f[0]
        shutil.copy(doc_src, doc_dest)
        print('   - {0}'.format(f[1]))
    

def make_header():
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    ref = '.. _{0}_{1}_csharp:\n'.format(com['name'][1], com['type'].lower())
    title = 'C# - {0} {1}'.format(com['name'][0], com['type'])
    title_under = '='*len(title)
    return '{0}\n{1}\n{2}\n{3}\n'.format(gen_text.format(date), 
                                         ref,
                                         title, 
                                         title_under)

def make_summary():
    su = """
This is the API site for the C# bindings of the {0} {1}. General information
on what this device does and the technical specifications can be found
:ref:`here <{2}>`.

A tutorial on how to test the {0} {1} and get the first examples running
can be found :ref:`here <{3}>`.
"""

    hw_link = com['name'][1] + '_' + com['type'].lower()
    hw_test = hw_link + '_test'
    su = su.format(com['name'][0], com['type'], hw_link, hw_test)
    return su

def make_examples():
    def title_from_file(f):
        f = f.replace('Example', '')
        f = f.replace('.cs', '')
        pattern = re.compile('([A-Z][A-Z][a-z])|([a-z][A-Z])')
        return pattern.sub(lambda m: m.group()[:1] + " " + m.group()[1:], f)

    ex = """
{0}

Examples
--------
"""

    imp = """
{0}
{1}

`Download <https://github.com/Tinkerforge/{3}/raw/master/software/examples/csharp/{4}>`__

.. literalinclude:: {2}
 :language: csharp
 :linenos:
 :tab-width: 4
"""

    ref = '.. _{0}_{1}_csharp_examples:\n'.format(com['name'][1], 
                                                  com['type'].lower())
    ex = ex.format(ref)
    files = find_examples()
    copy_files = []
    for f in files:
        include = '{0}_{1}_CSharp_{2}'.format(com['name'][0], com['type'], f[0])
        copy_files.append((f[1], include))
        title = title_from_file(f[0])
        git_name = com['name'][1].replace('_', '-') + '-' + com['type'].lower()
        ex += imp.format(title, '^'*len(title), include, git_name, f[0])

    copy_examples(copy_files)
    return ex

def to_camel_case(name):
    names = name.split('_')
    ret = names[0]
    for n in names[1:]:
        ret += n[0].upper() + n[1:]
    return ret

def get_csharp_type(typ):
    forms = {
        'int8' : 'sbyte',
        'uint8' : 'byte',
        'int16' : 'short',
        'uint16' : 'ushort',
        'int32' : 'int',
        'uint32' : 'uint',
        'int64' : 'long',
        'uint64' : 'ulong',
        'float' : 'float',
        'bool' : 'bool',
        'string' : 'string',
        'char' : 'char'
    }

    if typ in forms:
        return forms[typ]

    return ''

def get_num_return(elements): 
    num = 0
    for element in elements:
        if element[3] == 'out':
            num += 1

    return num

def make_parameter_list(packet):
    param = []
    for element in packet['elements']:
        out = ''
        if element[3] == 'out' and packet['type'] == 'method':
            out = 'out '

        csharp_type = get_csharp_type(element[1])
        name = to_camel_case(element[0])
        arr = ''
        if element[2] > 1 and element[1] != 'string':
            arr = '[]'
       
        param.append('{0}{1}{2} {3}'.format(out, csharp_type, arr, name))
    return ', '.join(param)

def make_methods(typ):
    method_version = """
.. csharp:function:: public void {0}::GetVersion(out string name, out byte[] firmwareVersion, out byte[] bindingVersion)

 Returns the name (including the hardware version), the firmware version 
 and the binding version of the device. The firmware and binding versions are
 given in arrays of size 3 with the syntax [major, minor, revision].
"""

    methods = ''
    func_start = '.. csharp:function:: '
    cls = com['type'] + com['name'][0]
    for packet in com['packets']:
        if packet['type'] != 'method' or packet['doc'][0] != typ:
            continue

        name = packet['name'][0]
        params = make_parameter_list(packet)
        desc = fix_links(shift_right(packet['doc'][1][lang], 1))
        func = '{0}public void {1}::{2}({3})\n{4}'.format(func_start, 
                                                             cls, 
                                                             name, 
                                                             params, 
                                                             desc)
        methods += func + '\n'

    if typ == 'am':
        methods += method_version.format(cls)

    return methods

def make_callbacks():
    cb = """
.. csharp:function:: public delegate void {0}::{1}({2})

{3}
"""

    cbs = ''
    cls = com['name'][0]
    for packet in com['packets']:
        if packet['type'] != 'signal':
            continue

        desc = fix_links(shift_right(packet['doc'][1][lang], 2))
        params = make_parameter_list(packet)

        cbs += cb.format(com['type'] + com['name'][0],
                         packet['name'][0],
                         params,
                         desc)

    return cbs
       

def make_api():
    create_str = """
.. csharp:function:: class {3}{1}(String uid)

 Creates an object with the unique device ID *uid*:

 .. code-block:: csharp

  {3}{1} {0} = new {3}{1}("YOUR_DEVICE_UID");

 This object can then be added to the IP connection (see examples 
 :ref:`above <{4}_{2}_csharp_examples>`).
"""

    register_str = """
.. csharp:function:: public void {3}{1}::RegisterCallback(Delegate d)

 Registers a callback function. The available callbacks are listed 
 :ref:`below <{0}_{2}_csharp_callbacks>`.
"""

    bm_str = """
Basic Methods
^^^^^^^^^^^^^

{0}

{1}
"""

    am_str = """
Advanced Methods
^^^^^^^^^^^^^^^^

{0}
"""

    ccm_str = """
Callback Configuration Methods
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

{0}

{1}
"""

    c_str = """
.. _{1}_{2}_csharp_callbacks:

Callbacks
^^^^^^^^^

*Callbacks* can be registered to receive
time critical or recurring data from the device. The registration is done
with the :csharp:func:`RegisterCallback <{3}{4}::RegisterCallback>` function
of the device object.

The parameter is a delegate object of the corresponding method, for example:

.. code-block:: csharp
    
    void Callback(int value)
    {{
        System.Console.WriteLine("Value: " + value);
    }}

    device.RegisterCallback(new BrickDevice.Property(Callback));

The available delegates are described below.

.. note::
 Using callbacks for recurring events is *always* prefered 
 compared to using getters. It will use less USB bandwith and the latency
 will be a lot better, since there is no roundtrip time.

{0}
"""

    api = """
{0}
API
---

Generally, every method of the C# bindings that returns a value can
throw a ``Tinkerforge.TimeoutException``. This exception gets thrown if the
device didn't answer. If a cable based connection is used, it is 
unlikely that this exception gets thrown (Assuming nobody plugs the 
device out). However, if a wireless connection is used, timeouts will occur
if the distance to the device gets too big.

Since C# does not support multiple return values directly, we use the out
keyword for all outgoing data that is to be returned. 

The namespace for all Brick/Bricklet bindings and the IPConnection is
``Tinkerforge.*``

{1}

{2}
"""
    cre = create_str.format(com['name'][0][0].lower() + com['name'][0][1:],
                            com['name'][0], 
                            com['type'].lower(),
                            com['type'],
                            com['name'][1])
    reg = register_str.format(com['name'][1], 
                              com['name'][0],
                              com['type'].lower(),
                              com['type'])

    bm = make_methods('bm')
    am = make_methods('am')
    ccm = make_methods('ccm')
    c = make_callbacks()
    api_str = ''
    if bm:
        api_str += bm_str.format(cre, bm)
    if am:
        api_str += am_str.format(am)
    if c:
        api_str += ccm_str.format(reg, ccm)
        api_str += c_str.format(c, com['name'][1], com['type'].lower(), com['type'], com['name'][0])

    ref = '.. _{0}_{1}_csharp_api:\n'.format(com['name'][1], 
                                             com['type'].lower())

    api_desc = ''
    try:
        api_desc = com['api']
    except:
        pass

    return api.format(ref, api_desc, api_str) 
        
def copy_examples_for_zip():
    examples = find_examples()
    dest = os.path.join('/tmp/generator/dll/examples/', 
                        com['type'], 
                        com['name'][0])

    if not os.path.exists(dest):
        os.makedirs(dest)

    for example in examples:
        shutil.copy(example[1], dest)

def make_files(com_new, directory):
    global com
    com = com_new

    file_name = '{0}_{1}_CSharp'.format(com['name'][0], com['type'])
    
    directory += '/doc'
    if not os.path.exists(directory):
        os.makedirs(directory)

    f = file('{0}/{1}.rst'.format(directory, file_name), "w")
    f.write(make_header())
    f.write(make_summary())
    f.write(make_examples())
    f.write(make_api())

    copy_examples_for_zip()

def get_version(path):
    r = re.compile('^(\d+)\.(\d+)\.(\d+):')
    last = None
    for line in file(path + '/changelog.txt').readlines():
        m = r.match(line)

        if m is not None:
            last = (m.group(1), m.group(2), m.group(3))

    return last

def generate(path):
    global file_path
    file_path = path
    path_list = path.split('/')
    path_list[-1] = 'configs'
    path_config = '/'.join(path_list)
    sys.path.append(path_config)
    configs = os.listdir(path_config)

    # Make temporary generator directory
    if os.path.exists('/tmp/generator'):
        shutil.rmtree('/tmp/generator/')
    os.makedirs('/tmp/generator/dll/source/Tinkerforge')
    os.chdir('/tmp/generator')

    # Make bindings
    for config in configs:
        if config.endswith('_config.py'):
            module = __import__(config[:-3])
            print(" * {0}".format(config[:-10]))            
            make_files(module.com, path)
               
    # Copy bindings and readme
    for filename in glob.glob(path + '/bindings/*.cs'):
        shutil.copy(filename, '/tmp/generator/dll/source/Tinkerforge')

    shutil.copy(path + '/IPConnection.cs', '/tmp/generator/dll/source/Tinkerforge')
    shutil.copy(path + '/changelog.txt', '/tmp/generator/dll')
    shutil.copy(path + '/Readme.txt', '/tmp/generator/dll')

    # Write AssemblyInfo
    version = get_version(path)
    file('/tmp/generator/dll/source/Tinkerforge/AssemblyInfo.cs', 'wb').write("""
using System.Reflection;
using System.Runtime.CompilerServices;

[assembly: AssemblyTitle("C# API Bindings")]
[assembly: AssemblyDescription("C# API Bindings for Tinkerforge Bricks and Bricklets")]
[assembly: AssemblyConfiguration("")]
[assembly: AssemblyCompany("Tinkerforge GmbH")]
[assembly: AssemblyProduct("C# API Bindings")]
[assembly: AssemblyCopyright("Tinkerforge GmbH 2011-2012")]
[assembly: AssemblyTrademark("")]
[assembly: AssemblyCulture("")]
[assembly: AssemblyVersion("{0}.{1}.{2}.0")]
""".format(*version))

    # Make dll
    args = ['/usr/bin/gmcs',
            '/optimize',
            '/target:library',
            '/out:/tmp/generator/dll/Tinkerforge.dll',
            '/tmp/generator/dll/source/Tinkerforge/*.cs']
    subprocess.call(args)

    # Make zip
    zipname = 'tinkerforge_csharp_bindings_{0}_{1}_{2}.zip'.format(*version)
    os.chdir('/tmp/generator/dll')
    args = ['/usr/bin/zip',
            '-r',
            zipname,
            '.']
    subprocess.call(args)

    # Copy zip
    shutil.copy(zipname, path)


if __name__ == "__main__":
    generate(os.getcwd())
