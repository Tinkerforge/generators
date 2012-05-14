#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python Documentation Generator
Copyright (C) 2012 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generator_python_doc.py: Generator for Python documentation

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

sys.path.append(os.path.split(os.getcwd())[0])
import common

com = None
lang = 'en'
file_path = ''

def type_to_pytype(element):
    type_dict = {
        'int8': 'int',
        'uint8': 'int',
        'int16': 'int',
        'uint16': 'int',
        'int32': 'int',
        'uint32': 'int',
        'int64': 'int',
        'uint64': 'int',
        'bool': 'bool',
        'char': 'chr',
        'string': 'str',
        'float': 'float'
    }

    t = type_dict[element[1]]
    
    if element[2] == 1 or t == 'str':
        return t

    return '[' + ', '.join([t]*element[2]) + ']'

def fix_links(text):
    cls = com['name'][0]
    for packet in com['packets']:
        name_false = ':func:`{0}`'.format(packet['name'][0])
        if packet['type'] == 'callback':
            name_upper = packet['name'][1].upper()
            name_right = ':py:attr:`{0}.CALLBACK_{1}`'.format(cls, name_upper)
        else:
            name_right = ':py:func:`{0}.{1}`'.format(cls, packet['name'][1])
        text = text.replace(name_false, name_right)

    text = text.replace(":word:`parameter`", "parameter")
    text = text.replace(":word:`parameters`", "parameters")

    return text

def make_header():
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    ref = '.. _{0}_{1}_python:\n'.format(com['name'][1], com['type'].lower())
    title = 'Python - {0} {1}'.format(com['name'][0], com['type'])
    title_under = '='*len(title)
    return '{0}\n{1}\n{2}\n{3}\n'.format(common.gen_text_rst.format(date),
                                         ref,
                                         title, 
                                         title_under)

def make_summary():
    su = """
This is the API site for the Python bindings of the {0} {1}. General information
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
        f = f.replace('.py', '')
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

`Download <https://github.com/Tinkerforge/{3}/raw/master/software/examples/python/{4}>`__

.. literalinclude:: {2}
 :language: python
 :linenos:
 :tab-width: 4
"""

    ref = '.. _{0}_{1}_python_examples:\n'.format(com['name'][1], 
                                                  com['type'].lower())
    ex = ex.format(ref)
    files = common.find_examples(com, file_path, 'python', 'example_', '.py')
    copy_files = []
    for f in files:
        include = '{0}_{1}_Python_{2}'.format(com['name'][0], com['type'], f[0])
        copy_files.append((f[1], include))
        title = title_from_file(f[0])
        git_name = com['name'][1].replace('_', '-') + '-' + com['type'].lower()
        ex += imp.format(title, '^'*len(title), include, git_name, f[0])

    common.copy_examples(copy_files, file_path)
    return ex

def make_parameter_list(packet):
    params = []
    for element in packet['elements']:
        if element[3] != 'in':
            continue
        params.append(element[0])
    return ", ".join(params)

def make_parameter_desc(packet, io):
    desc = '\n'
    param = ' :param {0}: {1}\n'
    for element in packet['elements']:
        if element[3] != io:
            continue
        t = type_to_pytype(element)
        desc += param.format(element[0], t)

    return desc

def make_return_desc(packet):
    ret = ' :rtype: {0}\n'
    ret_list = []
    for element in packet['elements']:
        if element[3] != 'out':
            continue
        ret_list.append(type_to_pytype(element))
    if len(ret_list) == 0:
        return ret.format(None)
    elif len(ret_list) == 1:
        return ret.format(ret_list[0])
    
    return ret.format('(' + ', '.join(ret_list) + ')')

def make_methods(typ):
    version_method = """
.. py:function:: {0}.get_version()

 :rtype: (str, [int, int, int], [int, int, int])

 Returns the name (including the hardware version), the firmware version 
 and the binding version of the device. The firmware and binding versions are
 given in arrays of size 3 with the syntax [major, minor, revision].
"""

    methods = ''
    func_start = '.. py:function:: '
    cls = com['name'][0]
    for packet in com['packets']:
        if packet['type'] != 'function' or packet['doc'][0] != typ:
            continue
        name = packet['name'][1]
        params = make_parameter_list(packet)
        pd = make_parameter_desc(packet, 'in')
        r = make_return_desc(packet)
        d = fix_links(common.shift_right(packet['doc'][1][lang], 1))
        desc = '{0}{1}{2}'.format(pd, r, d)
        func = '{0}{1}.{2}({3})\n{4}'.format(func_start, 
                                             cls, 
                                             name, 
                                             params, 
                                             desc)
        methods += func + '\n'

    if typ == 'am':
        methods += version_method.format(cls)

    return methods 

def make_callbacks():
    cbs = ''
    func_start = '.. py:attribute:: '
    cls = com['name'][0]
    for packet in com['packets']:
        if packet['type'] != 'callback':
            continue

        param_desc = make_parameter_desc(packet, 'out')
        desc = fix_links(common.shift_right(packet['doc'][1][lang], 1))

        func = '{0}{1}.CALLBACK_{2}\n{3}\n{4}'.format(func_start,
                                                      cls,
                                                      packet['name'][1].upper(),
                                                      param_desc,
                                                      desc)
        cbs += func + '\n'

    return cbs
       

def make_api():
    create_str = """
.. py:function:: {1}(uid)

 Creates an object with the unique device ID *uid*:

 .. code-block:: python

    {0} = {1}("YOUR_DEVICE_UID");

 This object can then be added to the IP connection (see examples 
 :ref:`above <{0}_{2}_python_examples>`).
"""

    register_str = """
.. py:function:: {1}.register_callback(cb, func)

 :param cb: int
 :param func: function
 :rtype: None

 Registers a callback with ID *cb* to the function *func*. The available
 IDs with corresponding function signatures are listed 
 :ref:`below <{0}_{2}_python_callbacks>`.
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
.. _{1}_{2}_python_callbacks:

Callbacks
^^^^^^^^^

*Callbacks* can be registered with *callback IDs* to receive
time critical or recurring data from the device. The registration is done
with the :py:func:`register_callback <{3}.register_callback>` function of
the device object. The first parameter is the callback ID and the second
parameter the callback function::

    def my_callback(param):
        print(param)

    {1}.register_callback({3}.CALLBACK_EXAMPLE, my_callback)

The available constants with inherent number and type of parameters are 
described below.

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
        api_str += c_str.format(c, com['name'][1], com['type'].lower(), com['name'][0])

    ref = '.. _{0}_{1}_python_api:\n'.format(com['name'][1], 
                                             com['type'].lower())

    api_desc = ''
    try:
        api_desc = com['api']
    except:
        pass

    return api.format(ref, api_desc, api_str) 
       
def copy_examples_for_zip():
    examples = common.find_examples(com, file_path, 'python', 'example_', '.py')
    dest = os.path.join('/tmp/generator/egg/examples/', 
                        com['type'].lower(), 
                        com['name'][1])

    if not os.path.exists(dest):
        os.makedirs(dest)

    for example in examples:
        shutil.copy(example[1], dest)
  
def make_files(com_new, directory):
    global com
    com = com_new

    file_name = '{0}_{1}_Python'.format(com['name'][0], com['type'])
    
    directory += '/doc'
    if not os.path.exists(directory):
        os.makedirs(directory)

    f = file('{0}/{1}.rst'.format(directory, file_name), "w")
    f.write(make_header())
    f.write(make_summary())
    f.write(make_examples())
    f.write(make_api())

    copy_examples_for_zip()

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
    os.makedirs('/tmp/generator/egg/source/tinkerforge')
    os.chdir('/tmp/generator')

    # Make bindings
    for config in configs:
        if config.endswith('_config.py'):
            module = __import__(config[:-3])
            print(" * {0}".format(config[:-10]))            
            make_files(module.com, path)

    # Copy bindings and readme
    for filename in glob.glob(path + '/bindings/*.py'):
        shutil.copy(filename, '/tmp/generator/egg/source/tinkerforge')

    shutil.copy(path + '/ip_connection.py', '/tmp/generator/egg/source/tinkerforge')
    shutil.copy(path + '/changelog.txt', '/tmp/generator/egg')
    shutil.copy(path + '/readme.txt', '/tmp/generator/egg')

    # Write setup.py
    version = common.get_version(path)
    file('/tmp/generator/egg/source/setup.py', 'wb').write("""
#!/usr/bin/env python

from setuptools import setup

setup(
    name='tinkerforge',
    version='{0}.{1}.{2}',
    description='TCP/IP based library for Bricks and Bricklets',
    author='Tinkerforge GmbH',
    author_email='olaf@tinkerforge.com',
    url='http://www.tinkerforge.com',
    packages=['tinkerforge'])
""".format(*version))

    # Make egg
    os.chdir('/tmp/generator/egg/source')
    args = ['/usr/bin/python',
            'setup.py',
            'bdist_egg']
    subprocess.call(args)

    # Remove build stuff
    shutil.rmtree('/tmp/generator/egg/source/build')
    shutil.rmtree('/tmp/generator/egg/source/tinkerforge.egg-info')
    shutil.copy('/tmp/generator/egg/source/dist/' + 
                os.listdir('/tmp/generator/egg/source/dist')[0], 
                '/tmp/generator/egg/tinkerforge.egg')
    shutil.rmtree('/tmp/generator/egg/source/dist')

    # Make __init__.py
    f = open('/tmp/generator/egg/source/tinkerforge/__init__.py', 'w')
    f.write(' ')
    f.close()

    # Make zip
    zipname = 'tinkerforge_python_bindings_{0}_{1}_{2}.zip'.format(*version)
    os.chdir('/tmp/generator/egg')
    args = ['/usr/bin/zip',
            '-r',
            zipname,
            '.']
    subprocess.call(args)

    # Copy zip
    shutil.copy(zipname, path)

if __name__ == "__main__":
    generate(os.getcwd())
