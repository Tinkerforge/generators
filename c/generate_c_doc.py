#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
C/C++ Documentation Generator
Copyright (C) 2012 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generator_c_doc.py: Generator for C/C++ documentation

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

def get_c_type(py_type):
    if py_type == 'string':
        return 'char'
    if py_type in ( 'int8',  'int16',  'int32' , 'int64', \
                   'uint8', 'uint16', 'uint32', 'uint64'):
        return "{0}_t".format(py_type)
    return py_type

def shift_right(text, n):
    return text.replace('\n', '\n' + ' '*n)

def fix_links(text):
    for packet in com['packets']:
        name_false = ':func:`{0}`'.format(packet['name'][0])
        if packet['doc'][0] == 'c':
            name_upper = packet['name'][1].upper()
            pre_upper = com['name'][1].upper()
            name_right = ':c:data:`{0}_CALLBACK_{1}`'.format(pre_upper,
                                                             name_upper)
        else:
            name_right = ':c:func:`{0}_{1}`'.format(com['name'][1],
                                                    packet['name'][1])
        text = text.replace(name_false, name_right)

    text = text.replace(":word:`parameter`", "parameter")
    text = text.replace(":word:`parameters`", "parameters")

    return text

def find_examples():
    path = file_path
    start_path = path.replace('/generators/c', '')
    board = '{0}-{1}'.format(com['name'][1], com['type'].lower())
    board = board.replace('_', '-')
    board_path = os.path.join(start_path, board, 'software/examples/c')
    files = []
    for f in os.listdir(board_path):
        if f.startswith('example_') and f.endswith('.c'):
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

def make_parameter_list(packet):
    param = ''
    for element in packet['elements']:
        c_type = get_c_type(element[1])
        name = element[0]
        pointer = ''
        arr = ''
        if element[3] == 'out':
            pointer = '*'
            name = "ret_{0}".format(name)
        if element[2] > 1:
            arr = '[{0}]'.format(element[2])
            pointer = ''
       
        param += ', {0} {1}{2}{3}'.format(c_type, pointer, name, arr)
    return param

def make_header():
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    ref = '.. _{0}_{1}_c:\n'.format(com['name'][1], com['type'].lower())
    title = 'C/C++ - {0} {1}'.format(com['name'][0], com['type'])
    title_under = '='*len(title)
    return '{0}\n{1}\n{2}\n{3}\n'.format(gen_text.format(date), 
                                         ref,
                                         title, 
                                         title_under)

def make_summary():
    su = """
This is the API site for the C/C++ bindings of the {0} {1}. General information
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
        f = f.replace('example_', '')
        f = f.replace('.c', '')
        s = ''
        for l in f.split('_'):
            s += l[0].upper() + l[1:] + ' '
        return s[:-1]

    ex = """
{0}

Examples
--------
"""

    imp = """
{0}
{1}

`Download <https://github.com/Tinkerforge/{3}/raw/master/software/examples/c/{4}>`__

.. literalinclude:: {2}
 :language: c
 :linenos:
 :tab-width: 4
"""

    ref = '.. _{0}_{1}_c_examples:\n'.format(com['name'][1], 
                                             com['type'].lower())
    ex = ex.format(ref)
    files = find_examples()
    copy_files = []
    for f in files:
        include = '{0}_{1}_C_{2}'.format(com['name'][0], com['type'], f[0])
        copy_files.append((f[1], include))
        title = title_from_file(f[0])
        git_name = com['name'][1].replace('_', '-') + '-' + com['type'].lower()
        ex += imp.format(title, '^'*len(title), include, git_name, f[0])

    copy_examples(copy_files)
    return ex

def make_methods(typ):
    version_method = """
.. c:function:: int {0}_get_version({1} *{0}, char ret_name[40], uint8_t ret_firmware_version[3], uint8_t ret_binding_version[3])

 Returns the name (including the hardware version), the firmware version 
 and the binding version of the device. The firmware and binding versions are
 given in arrays of size 3 with the syntax [major, minor, revision].
"""

    methods = ''
    func_start = '.. c:function:: int '
    for packet in com['packets']:
        if packet['type'] != 'method' or packet['doc'][0] != typ:
            continue
        name = '{0}_{1}'.format(com['name'][1], packet['name'][1])
        plist = make_parameter_list(packet)
        params = '{0} *{1}{2}'.format(com['name'][0], com['name'][1], plist)
        desc = fix_links(shift_right(packet['doc'][1][lang], 1))
        func = '{0}{1}({2})\n{3}'.format(func_start, name, params, desc)
        methods += func + '\n'

    if typ == 'am':
        methods += version_method.format(com['name'][1], com['name'][0])

    return methods

def make_callbacks():
    cbs = ''
    func_start = '.. c:var:: '
    for packet in com['packets']:
        if packet['type'] != 'signal':
            continue

        plist = make_parameter_list(packet)[2:].replace('*ret_', '')
        if not plist:
            plist = 'void'
        params = """
 .. c:var:: signature: void callback({0})
    :noindex:
""".format(plist)
        #params = ' ´´void callback({0})´´\n'.format(plist[2:])

        desc = fix_links(shift_right(packet['doc'][1][lang], 1))
        name = '{0}_{1}'.format(com['name'][1].upper(), 
                                packet['name'][1].upper())

        func = '{0}{1}_CALLBACK_{2}\n{3}\n{4}'.format(func_start,
                                                      com['name'][1].upper(),
                                                      packet['name'][1].upper(),
                                                      params,
                                                      desc)
        cbs += func + '\n'

    return cbs
        
        
def make_api():
    create_str = """
.. c:function:: void {0}_create({1} *{0}, const char *uid)

 Creates an object with the unique device ID *uid*::

    {1} {0};
    {0}_create(&{0}, "YOUR_DEVICE_UID");

 This object can then be added to the IP connection (see examples 
 :ref:`above <{0}_{2}_c_examples>`).
"""

    register_str = """
.. c:function:: void {0}_register_callback({1} *{0}, uint8_t cb, void *func)

 Registers a callback with ID *cb* to the function *func*. The available
 IDs with corresponding function signatures are listed 
 :ref:`below <{0}_{2}_c_callbacks>`.
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

    c_str = r"""
.. _{0}_{3}_c_callbacks:

Callbacks
^^^^^^^^^

*Callbacks* can be registered with *callback IDs* to receive
time critical or recurring data from the device. The registration is done
with the :c:func:`{0}_register_callback` function. The parameters consist of
the device object, the callback ID and the callback function::

    void my_callback(int p) {{
        printf("parameter: %d\n", p);
    }}

    {0}_register_callback(&{0}, {1}_CALLBACK_EXAMPLE, (void*)my_callback);

The available constants with corresponding callback function signatures 
are described below.

 .. note::
  Using callbacks for recurring events is *always* prefered 
  compared to using getters. It will use less USB bandwith and the latency
  will be a lot better, since there is no roundtrip time.

{2}
"""

    api = """
{0}
API
---

Every function of the C/C++ bindings returns an integer which describes an
error code. Data returned from the device, when a getter is called,
is handled via call by reference. These parameters are labelled with the
``ret_`` prefix.

Possible error codes are

 * E_OK = 0
 * E_TIMEOUT = -1
 * E_NO_STREAM_SOCKET = -2
 * E_HOSTNAME_INVALID = -3
 * E_NO_CONNECT = -4
 * E_NO_THREAD = -5
 * E_NOT_ADDED = -6

as defined in :file:`ip_connection.h`.

{1}

{2}
"""
    cre = create_str.format(com['name'][1], 
                            com['name'][0], 
                            com['type'].lower())
    reg = register_str.format(com['name'][1], 
                              com['name'][0],
                              com['type'].lower())
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
        api_str += c_str.format(com['name'][1], 
                                com['name'][0].upper(), 
                                c,
                                com['type'].lower())

    ref = '.. _{0}_{1}_c_api:\n'.format(com['name'][1], 
                                        com['type'].lower())
    api_desc = ''
    try:
        api_desc = com['api']
    except:
        pass

    return api.format(ref, api_desc, api_str)

def copy_examples_for_zip():
    examples = find_examples()
    dest = os.path.join('/tmp/generator/examples/', 
                        com['type'].lower(), 
                        com['name'][1])

    if not os.path.exists(dest):
        os.makedirs(dest)

    for example in examples:
        shutil.copy(example[1], dest)

def make_files(com_new, directory):
    global com
    com = com_new

    file_name = '{0}_{1}_C'.format(com['name'][0], com['type'])
    
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
    os.makedirs('/tmp/generator/bindings')
    os.chdir('/tmp/generator/bindings')

    for config in configs:
        if config.endswith('_config.py'):
            module = __import__(config[:-3])
            print(" * {0}".format(config[:-10]))            
            make_files(module.com, path)

    # Copy bindings and readme
    for filename in glob.glob(path + '/bindings/*.[ch]'):
        shutil.copy(filename, '/tmp/generator/bindings')

    shutil.copy(path + '/ip_connection.c', '/tmp/generator/bindings')
    shutil.copy(path + '/ip_connection.h', '/tmp/generator/bindings')
    shutil.copy(path + '/changelog.txt', '/tmp/generator/')
    shutil.copy(path + '/readme.txt', '/tmp/generator/')

    # Make zip
    version = get_version(path)
    zipname = 'tinkerforge_c_bindings_{0}_{1}_{2}.zip'.format(*version)
    os.chdir('/tmp/generator')
    args = ['/usr/bin/zip',
            '-r',
            zipname,
            '.']
    subprocess.call(args)

    # Copy zip
    shutil.copy(zipname, path)

if __name__ == "__main__":
    generate(os.getcwd())
