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

import sys
import os
import shutil
import subprocess
import glob
import re
import csharp_common

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
    link = ':csharp:func:`{2}() <{0}{1}::{2}>`' 

    cls = device.get_camel_case_name()
    for packet in device.get_packets():
        name_false = ':func:`{0}`'.format(packet.get_camel_case_name())
        name = packet.get_camel_case_name()
        name_right = link.format(device.get_category(), cls, name)

        text = text.replace(name_false, name_right)

    text = text.replace(":word:`parameter`", parameter[lang])
    text = text.replace(":word:`parameters`", parameters[lang])

    return text

def make_examples():
    def title_from_file(f):
        f = f.replace('Example', '')
        f = f.replace('.cs', '')
        return common.camel_case_to_space(f)

    return common.make_rst_examples(title_from_file, device, file_path,
                                    'csharp', 'Example', '.cs', 'CSharp')

def make_methods(typ):
    method_version = {
    'en': """
.. csharp:function:: public void {0}::GetVersion(out string name, out byte[] firmwareVersion, out byte[] bindingVersion)

 Returns the name (including the hardware version), the firmware version 
 and the binding version of the device. The firmware and binding versions are
 given in arrays of size 3 with the syntax [major, minor, revision].
""",
    'de': """
"""
    }
    version_changed = {
    'en': """
 .. versionchanged:: 1.1.0
    Result is returned. Previously it was passed as ``out`` parameter.
""",
    'de': """
"""
    }

    methods = ''
    func_start = '.. csharp:function:: '
    cls = device.get_category() + device.get_camel_case_name()
    for packet in device.get_packets('function'):
        if packet.get_doc()[0] != typ:
            continue

        signature = csharp_common.make_method_signature(packet, True, device)
        desc = fix_links(common.shift_right(packet.get_doc()[1][lang], 1))
        func = '{0}{1}\n{2}'.format(func_start, 
                                    signature, 
                                    desc)
        methods += func + '\n'

        if len(packet.get_elements('out')) == 1:
            methods += version_changed[lang] + '\n'

    if typ == 'am':
        methods += method_version[lang].format(cls)

    return methods

def make_callbacks():
    cb = {
    'en': """
.. csharp:function:: public delegate void {0}::{1}({2})

{3}
""",
    'de': """
.. csharp:function:: public delegate void {0}::{1}({2})

{3}
"""
    }

    cbs = ''
    cls = device.get_camel_case_name()
    for packet in device.get_packets('callback'):
        desc = fix_links(common.shift_right(packet.get_doc()[1][lang], 2))
        params = csharp_common.make_parameter_list(packet)

        cbs += cb[lang].format(device.get_category() + device.get_camel_case_name(),
                               packet.get_camel_case_name(),
                               params,
                               desc)

    return cbs

def make_api():
    create_str = {
    'en': """
.. csharp:function:: class {3}{1}(String uid)

 Creates an object with the unique device ID *uid*:

 .. code-block:: csharp

  {3}{1} {0} = new {3}{1}("YOUR_DEVICE_UID");

 This object can then be added to the IP connection (see examples 
 :ref:`above <{4}_{2}_csharp_examples>`).
""",
    'de': """
"""
    }

    register_str = {
    'en': """
.. csharp:function:: public void {3}{1}::RegisterCallback(Delegate d)

 Registers a callback function. The available callbacks are listed 
 :ref:`below <{0}_{2}_csharp_callbacks>`.
""",
    'de': """
"""
    }

    bm_str = {
    'en':  """
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
""",
    'de': """
"""
    }

    api = {
    'en': """
{0}
API
---

Generally, every method of the C# bindings that returns a value can
throw a ``Tinkerforge.TimeoutException``. This exception gets thrown if the
device didn't respond. If a cable based connection is used, it is
unlikely that this exception gets thrown (Assuming nobody plugs the 
device out). However, if a wireless connection is used, timeouts will occur
if the distance to the device gets too big.

Since C# does not support multiple return values directly, we use the out
keyword to return multiple values from a mathod.

The namespace for all Brick/Bricklet bindings and the IPConnection is
``Tinkerforge.*``

All methods listed below are thread-safe.

{1}

{2}
""",
    'de': """
"""
    }

    cre = create_str[lang].format(device.get_headless_camel_case_name(),
                                  device.get_camel_case_name(),
                                  device.get_category().lower(),
                                  device.get_category(),
                                  device.get_underscore_name())
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

    ref = '.. _{0}_{1}_csharp_api:\n'.format(device.get_underscore_name(),
                                             device.get_category().lower())

    api_desc = ''
    try:
        api_desc = device.com['api'][lang]
    except KeyError:
        pass

    return api[lang].format(ref, api_desc, api_str)
        
def copy_examples_for_zip():
    examples = common.find_examples(device, file_path, 'csharp', 'Example', '.cs')
    dest = os.path.join('/tmp/generator/dll/examples/', 
                        device.get_category(),
                        device.get_camel_case_name())

    if not os.path.exists(dest):
        os.makedirs(dest)

    for example in examples:
        shutil.copy(example[1], dest)

def make_files(com_new, directory):
    global device
    device = common.Device(com_new)
    file_name = '{0}_{1}_CSharp'.format(device.get_camel_case_name(), device.get_category())
    title = {
    'en': 'C# bindings',
    'de': 'C# Bindings'
    }
    
    directory += '/doc'
    if not os.path.exists(directory):
        os.makedirs(directory)

    f = file('{0}/{1}.rst'.format(directory, file_name), "w")
    f.write(common.make_rst_header(device, 'csharp', 'C#'))
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
    version = common.get_changelog_version(path)
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
            '/doc:/tmp/generator/dll/Tinkerforge.xml',
            '/tmp/generator/dll/source/Tinkerforge/*.cs']
    subprocess.call(args)

    # Make zip
    common.make_zip('csharp', '/tmp/generator/dll', path, version)

if __name__ == "__main__":
    generate(os.getcwd())
