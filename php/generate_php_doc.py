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

device = None
lang = 'en'
file_path = ''

def fix_links(text):
    parameter = {
    'en': 'parameter',
    'de': 'Parameter'
    }
    parameters = {
    'en': 'parameters',
    'de': 'Parameter'
    }

    cls = device.get_category() + device.get_camel_case_name()
    for packet in device.get_packets():
        name_false = ':func:`{0}`'.format(packet.get_camel_case_name())
        if packet.get_type() == 'callback':
            name_upper = packet.get_upper_case_name()
            name_right = ':php:member:`CALLBACK_{1} <{0}::CALLBACK_{1}>`'.format(cls, name_upper)
        else:
            name = packet.get_headless_camel_case_name()
            name_right = ':php:func:`{1} <{0}::{1}>`'.format(cls, name)
        text = text.replace(name_false, name_right)

    text = text.replace(":word:`parameter`", parameter[lang])
    text = text.replace(":word:`parameters`", parameters[lang])

    return text

def make_examples():
    def title_from_file(f):
        f = f.replace('Example', '')
        f = f.replace('.php', '')
        return common.camel_case_to_space(f)

    return common.make_rst_examples(title_from_file, device, file_path,
                                    'php', 'Example', '.php', 'PHP')

def make_parameter_list(packet):
    param = []
    for element in packet.get_elements():
        if element[3] == 'out' and packet.get_type() == 'function':
            continue
        php_type = php_common.get_php_type(element[1])
        name = element[0]
        if element[2] > 1 and element[1] != 'string':
            php_type = 'array'
       
        param.append('{0} ${1}'.format(php_type, name))
    return ', '.join(param)

def make_methods(typ):
    version_method = {
    'en': """
.. php:function:: array {0}::getVersion()

 Returns the name (including the hardware version), the firmware version
 and the binding version of the device. The firmware and binding versions
 are given in arrays of size 3 with the syntax (major, minor, revision).

 The returned array contains name, firmwareVersion and bindingVersion.
""",
    'de': """
"""
    }

    methods = ''
    func_start = '.. php:function:: '
    cls = device.get_category() + device.get_camel_case_name()
    for packet in device.get_packets('function'):
        if packet.get_doc()[0] != typ:
            continue

        ret_type = php_common.get_return_type(packet)
        name = packet.get_headless_camel_case_name()
        params = make_parameter_list(packet)
        desc = fix_links(common.shift_right(packet.get_doc()[1][lang], 1))
        func = '{0}{1} {2}::{3}({4})\n{5}'.format(func_start, 
                                                            ret_type,
                                                            cls, 
                                                            name, 
                                                            params, 
                                                            desc)
        methods += func + '\n'

    if typ == 'am':
        methods += version_method[lang].format(cls)

    return methods

def make_callbacks():
    signature_str = {
    'en':  """
 .. code-block:: php

  void callback({0})
""",
    'de':  """
 .. code-block:: php

  void callback({0})
"""
    }

    cbs = ''
    func_start = '.. php:member:: int '
    cls = device.get_category() + device.get_camel_case_name()
    for packet in device.get_packets('callback'):
        params = make_parameter_list(packet)
        desc = fix_links(common.shift_right(packet.get_doc()[1][lang], 1))
        signature = signature_str[lang].format(params)
        func = '{0}{1}::CALLBACK_{2}\n{3}{4}'.format(func_start,
                                                     cls,
                                                     packet.get_upper_case_name(),
                                                     signature,
                                                     desc)
        cbs += func + '\n'

    return cbs

def make_api():
    create_str = {
    'en': """
.. php:function:: class {3}{1}(string $uid)

 Creates an object with the unique device ID *$uid*:

 .. code-block:: php

    ${0} = new {3}{1}('YOUR_DEVICE_UID');

 This object can then be added to the IP connection (see examples
 :ref:`above <{0}_{2}_php_examples>`).
""",
    'de': """
"""
    }

    register_str = {
    'en': """
.. php:function:: void {3}{1}::registerCallback(int $id, callable $callback)

 Registers a callback with ID *$id* to the callable *$callback*. The available
 IDs with corresponding function signatures are listed
 :ref:`below <{0}_{2}_php_callbacks>`.
""",
    'de': """
"""
    }

    bm_str = {
    'en': """
Basic Methods
^^^^^^^^^^^^^

{0}

{1}
""",
    'de': """
"""
    }

    am_str = {
    'en': """
Advanced Methods
^^^^^^^^^^^^^^^^

{0}
""",
    'de': """
"""
    }

    ccm_str = {
    'en': """
Callback Configuration Methods
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

{0}

{1}
""",
    'de': """
"""
    }

    c_str = {
    'en': """
.. _{1}_{2}_php_callbacks:

Callbacks
^^^^^^^^^

*Callbacks* can be registered with *callback IDs* to receive
time critical or recurring data from the device. The registration is done
with the :php:func:`registerCallback <{3}{4}::registerCallback>` function of
the device object. The first parameter is the callback ID and the second
parameter the callback function:

.. code-block:: php

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
""",
    'de': """
"""
    }

    api = {
    'en': """
{0}
API
---

{1}

{2}
""",
    'de': """
"""
    }

    cre = create_str[lang].format(device.get_underscore_name(),
                                  device.get_camel_case_name(),
                                  device.get_category().lower(),
                                  device.get_category())
    reg = register_str[lang].format(device.get_underscore_name(),
                                    device.get_camel_case_name(),
                                    device.get_category().lower(),
                                    device.get_category())

    bm = make_methods('bm')
    am = make_methods('am')
    ccm = make_methods('ccm')
    c = make_callbacks()
    api_str = ''
    if bm:
        api_str += bm_str[lang].format(cre, bm)
    if am:
        api_str += am_str[lang].format(am)
    if c:
        api_str += ccm_str[lang].format(reg, ccm)
        api_str += c_str[lang].format(c, device.get_underscore_name(),
                                      device.get_category().lower(),
                                      device.get_category(),
                                      device.get_camel_case_name())

    ref = '.. _{0}_{1}_php_api:\n'.format(device.get_underscore_name(),
                                          device.get_category().lower())

    api_desc = ''
    try:
        api_desc = device.com['api'][lang]
    except KeyError:
        pass

    return api[lang].format(ref, api_desc, api_str)

def copy_examples_for_zip():
    examples = common.find_examples(device, file_path, 'php', 'Example', '.php')
    dest = os.path.join('/tmp/generator/pear/examples/',
                        device.get_category().lower(),
                        device.get_underscore_name())

    if not os.path.exists(dest):
        os.makedirs(dest)

    for example in examples:
        shutil.copy(example[1], dest)

def make_files(com_new, directory):
    global device
    device = common.Device(com_new)
    file_name = '{0}_{1}_PHP'.format(device.get_camel_case_name(), device.get_category())
    title = {
    'en': 'PHP bindings',
    'de': 'PHP Bindings'
    }

    directory += '/doc'
    if not os.path.exists(directory):
        os.makedirs(directory)

    f = file('{0}/{1}.rst'.format(directory, file_name), "w")
    f.write(common.make_rst_header(device, 'php', 'PHP'))
    f.write(common.make_rst_summary(device, title[lang]))
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
    common.make_zip('php', '/tmp/generator/pear', path, version)

if __name__ == "__main__":
    generate(os.getcwd())
