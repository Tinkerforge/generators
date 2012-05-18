#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PHP Documentation Generator
Copyright (C) 2012 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generator_php_doc.py: Generator for PHP documentation

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
import php_common

sys.path.append(os.path.split(os.getcwd())[0])
import common

com = None
lang = 'en'
file_path = ''

def fix_links(text):
    cls = com['type'] + com['name'][0]
    for packet in com['packets']:
        name_false = ':func:`{0}`'.format(packet['name'][0])
        if packet['type'] == 'callback':
            name_upper = packet['name'][1].upper()
            name_right = ':php:member:`CALLBACK_{1} <{0}::CALLBACK_{1}>`'.format(cls, name_upper)
        else:
            name = packet['name'][0][0].lower() + packet['name'][0][1:]
            name_right = ':php:func:`{1} <{0}::{1}>`'.format(cls, name)
        text = text.replace(name_false, name_right)

    text = text.replace(":word:`parameter`", "parameter")
    text = text.replace(":word:`parameters`", "parameters")

    return text

def make_header():
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    ref = '.. _{0}_{1}_php:\n'.format(com['name'][1], com['type'].lower())
    name = common.camel_case_to_space(com['name'][0])
    title = 'PHP - {0} {1}'.format(name, com['type'])
    title_under = '='*len(title)
    return '{0}\n{1}\n{2}\n{3}\n'.format(common.gen_text_rst.format(date),
                                         ref,
                                         title,
                                         title_under)

def make_summary():
    su = """
This is the API site for the PHP bindings of the {0} {1}. General information
on what this device does and the technical specifications can be found
:ref:`here <{2}>`.

A tutorial on how to test the {0} {1} and get the first examples running
can be found :ref:`here <{3}>`.
"""

    hw_link = com['name'][1] + '_' + com['type'].lower()
    hw_test = hw_link + '_test'
    name = common.camel_case_to_space(com['name'][0])
    su = su.format(name, com['type'], hw_link, hw_test)
    return su

def make_examples():
    def title_from_file(f):
        f = f.replace('Example', '')
        f = f.replace('.php', '')
        return common.camel_case_to_space(f)

    ex = """
{0}

Examples
--------
"""

    imp = """
{0}
{1}

`Download <https://github.com/Tinkerforge/{3}/raw/master/software/examples/php/{4}>`__

.. literalinclude:: {2}
 :language: php
 :linenos:
 :tab-width: 4
"""

    ref = '.. _{0}_{1}_php_examples:\n'.format(com['name'][1], 
                                               com['type'].lower())
    ex = ex.format(ref)
    files = common.find_examples(com, file_path, 'php', 'Example', '.php')
    copy_files = []
    for f in files:
        include = '{0}_{1}_PHP_{2}'.format(com['name'][0], com['type'], f[0])
        copy_files.append((f[1], include))
        title = title_from_file(f[0])
        git_name = com['name'][1].replace('_', '-') + '-' + com['type'].lower()
        ex += imp.format(title, '^'*len(title), include, git_name, f[0])

    common.copy_examples(copy_files, file_path)
    return ex

def make_parameter_list(packet):
    param = []
    for element in packet['elements']:
        if element[3] == 'out' and packet['type'] == 'function':
            continue
        php_type = php_common.get_php_type(element[1])
        name = element[0]
        if element[2] > 1 and element[1] != 'string':
            php_type = 'array'
       
        param.append('{0} ${1}'.format(php_type, name))
    return ', '.join(param)

def make_methods(typ):
    version_method = """
.. php:function:: array {0}::getVersion()

 Returns the name (including the hardware version), the firmware version
 and the binding version of the device. The firmware and binding versions
 are given in arrays of size 3 with the syntax (major, minor, revision).

 The returned array contains name, firmwareVersion and bindingVersion.
"""

    methods = ''
    func_start = '.. php:function:: '
    cls = com['type'] + com['name'][0]
    for packet in com['packets']:
        if packet['type'] != 'function' or packet['doc'][0] != typ:
            continue

        ret_type = php_common.get_return_type(packet)
        name = packet['name'][0][0].lower() + packet['name'][0][1:]
        params = make_parameter_list(packet)
        desc = fix_links(common.shift_right(packet['doc'][1][lang], 1))
        func = '{0}{1} {2}::{3}({4})\n{5}'.format(func_start, 
                                                            ret_type,
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
    func_start = '.. php:member:: int '
    cls = com['type'] + com['name'][0]
    for packet in com['packets']:
        if packet['type'] != 'callback':
            continue

        params = make_parameter_list(packet)
        desc = fix_links(common.shift_right(packet['doc'][1][lang], 1))

        signature = """
 .. php:function:: void callback({0})
    :noindex:
""".format(params)

        func = '{0}{1}::CALLBACK_{2}\n{3}{4}'.format(func_start,
                                                      cls,
                                                      packet['name'][1].upper(),
                                                      signature,
                                                      desc)
        cbs += func + '\n'

    return cbs


def make_api():
    create_str = """
.. php:function:: class {3}{1}(string $uid)

 Creates an object with the unique device ID *$uid*:

 .. code-block:: php

    ${0} = new {3}{1}('YOUR_DEVICE_UID');

 This object can then be added to the IP connection (see examples
 :ref:`above <{0}_{2}_php_examples>`).
"""

    register_str = """
.. php:function:: void {3}{1}::registerCallback(int $id, callable $callback)

 Registers a callback with ID *$id* to the callable *$callback*. The available
 IDs with corresponding function signatures are listed
 :ref:`below <{0}_{2}_php_callbacks>`.
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
.. _{1}_{2}_php_callbacks:

Callbacks
^^^^^^^^^

*Callbacks* can be registered with *callback IDs* to receive
time critical or recurring data from the device. The registration is done
with the :php:func:`registerCallback <{3}{4}::registerCallback>` function of
the device object. The first parameter is the callback ID and the second
parameter the callback function::

    function my_callback($param)
    {{
        echo $param . "\\n";
    }}

    ${1}->registerCallback({3}{4}::CALLBACK_EXAMPLE, 'my_callback');

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
                            com['type'].lower(),
                            com['type'])
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

    ref = '.. _{0}_{1}_php_api:\n'.format(com['name'][1],
                                          com['type'].lower())

    api_desc = ''
    try:
        api_desc = com['api']
    except:
        pass

    return api.format(ref, api_desc, api_str)

def copy_examples_for_zip():
    examples = common.find_examples(com, file_path, 'php', 'Example', '.php')
    dest = os.path.join('/tmp/generator/pear/examples/',
                        com['type'].lower(),
                        com['name'][1])

    if not os.path.exists(dest):
        os.makedirs(dest)

    for example in examples:
        shutil.copy(example[1], dest)

def make_files(com_new, directory):
    global com
    com = com_new

    file_name = '{0}_{1}_PHP'.format(com['name'][0], com['type'])

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
    os.makedirs('/tmp/generator/pear/source/Tinkerforge')
    os.chdir('/tmp/generator')

    # Make bindings
    for config in configs:
        if config.endswith('_config.py'):
            module = __import__(config[:-3])
            print(" * {0}".format(config[:-10]))
            make_files(module.com, path)

    # Copy bindings and readme
    package_files = ['<file name="Tinkerforge/IPConnection.php" role="php" />']
    for filename in glob.glob(path + '/bindings/*.php'):
        shutil.copy(filename, '/tmp/generator/pear/source/Tinkerforge')
        package_files.append('<file name="Tinkerforge/{0}" role="php" />'.format(os.path.basename(filename)))

    shutil.copy(path + '/IPConnection.php', '/tmp/generator/pear/source/Tinkerforge')
    shutil.copy(path + '/changelog.txt', '/tmp/generator/pear')
    shutil.copy(path + '/readme.txt', '/tmp/generator/pear')

    # Write package.xml
    version = common.get_changelog_version(path)
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    file('/tmp/generator/pear/source/package.xml', 'wb').write("""<?xml version="1.0" encoding="UTF-8"?>
<package packagerversion="1.9.0" version="2.0" xmlns="http://pear.php.net/dtd/package-2.0">
 <name>Tinkerforge</name>
 <uri>http://download.tinkerforge.com/bindings/php/pear/Tinkerforge-{2}.{3}.{4}</uri>
 <summary>PHP API Bindings for Tinkerforge Bricks and Bricklets</summary>
 <description>no description</description>
 <lead>
  <name>Matthias Bolte</name>
  <user>matthias</user>
  <email>matthias@tinkerforge.com</email>
  <active>yes</active>
 </lead>
 <date>{0}</date>
 <version>
  <release>{2}.{3}.{4}</release>
  <api>{2}.{3}.{4}</api>
 </version>
 <stability>
  <release>stable</release>
  <api>stable</api>
 </stability>
 <license>Public Domain</license>
 <notes>no notes</notes>
 <contents>
  <dir name="Tinkerforge">
   {1}
  </dir>
 </contents>
 <dependencies>
  <required>
   <php>
    <min>5.3.0</min>
   </php>
   <pearinstaller>
    <min>1.9.0</min>
   </pearinstaller>
  </required>
 </dependencies>
 <phprelease />
</package>
""".format(date, '\n    '.join(package_files), *version))

    # Make PEAR package
    os.chdir('/tmp/generator/pear/source')
    args = ['/usr/bin/pear',
            'package',
            'package.xml']
    subprocess.call(args)

    # Remove build stuff
    shutil.move('/tmp/generator/pear/source/Tinkerforge-{0}.{1}.{2}.tgz'.format(*version),
                '/tmp/generator/pear/Tinkerforge.tgz')
    os.remove('/tmp/generator/pear/source/package.xml')

    # Make zip
    zipname = 'tinkerforge_php_bindings_{0}_{1}_{2}.zip'.format(*version)
    os.chdir('/tmp/generator/pear')
    args = ['/usr/bin/zip',
            '-r',
            zipname,
            '.']
    subprocess.call(args)

    # Copy zip
    shutil.copy(zipname, path)

if __name__ == "__main__":
    generate(os.getcwd())
