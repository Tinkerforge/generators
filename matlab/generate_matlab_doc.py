#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MATLAB/Octave Documentation Generator
Copyright (C) 2012-2015, 2017-2019 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011-2013 Olaf Lüke <olaf@tinkerforge.com>

generate_matlab_doc.py: Generator for MATLAB/Octave documentation

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

if sys.hexversion < 0x3040000:
    print('Python >= 3.4 required')
    sys.exit(1)

import os
import importlib.util
import importlib.machinery

def create_generators_module():
    generators_dir = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]

    if sys.hexversion < 0x3050000:
        generators_module = importlib.machinery.SourceFileLoader('generators', os.path.join(generators_dir, '__init__.py')).load_module()
    else:
        generators_spec = importlib.util.spec_from_file_location('generators', os.path.join(generators_dir, '__init__.py'))
        generators_module = importlib.util.module_from_spec(generators_spec)

        generators_spec.loader.exec_module(generators_module)

    sys.modules['generators'] = generators_module

if 'generators' not in sys.modules:
    create_generators_module()

from generators import common
from generators.matlab import matlab_common

class MATLABDocDevice(matlab_common.MATLABDevice):
    def specialize_matlab_doc_function_links(self, text):
        def specializer(packet, high_level):
            if packet.get_type() == 'callback':
                return ':matlab:member:`{1}Callback <{0}::{1}Callback>`'.format(packet.get_device().get_matlab_class_name(),
                                                                                packet.get_name(skip=-2 if high_level else 0).camel)
            else:
                return ':matlab:func:`{1}() <{0}::{1}>`'.format(packet.get_device().get_matlab_class_name(),
                                                                packet.get_name(skip=-2 if high_level else 0).headless)

        return self.specialize_doc_rst_links(text, specializer, prefix='matlab')

    def get_matlab_examples(self):
        def title_from_filename(filename):
            title = filename.replace('matlab_example_', '').replace('octave_example_', '').replace('.m', '')

            if filename.startswith('matlab_'):
                return common.under_to_space(title) + ' (MATLAB)'
            elif filename.startswith('octave_'):
                return common.under_to_space(title) + ' (Octave)'
            else:
                raise common.GeneratorError('Invalid filename ' + filename)

        def language_from_filename(filename):
            if filename.startswith('matlab_'):
                return 'matlab'
            elif filename.startswith('octave_'):
                return 'octave_fixed'
            else:
                raise common.GeneratorError('Invalid filename ' + filename)

        return common.make_rst_examples(title_from_filename, self,
                                        language_from_filename=language_from_filename)

    def get_matlab_functions(self, type_):
        functions = []
        template = '.. matlab:function:: {0} {1}::{2}({3})\n\n{4}{5}\n'
        cls = self.get_matlab_class_name()

        for packet in self.get_packets('function'):
            if packet.get_doc_type() != type_:
                continue

            skip = -2 if packet.has_high_level() else 0
            ret_type = packet.get_matlab_return_type(True, high_level=True)
            name = packet.get_name(skip=skip).headless
            params = packet.get_matlab_parameter_list(high_level=True)
            meta = packet.get_formatted_element_meta(lambda element, cardinality=None: element.get_matlab_type(cardinality=cardinality),
                                                     lambda element, index=None: element.get_name(index=index).headless,
                                                     return_object='conditional',
                                                     explicit_string_cardinality=True,
                                                     explicit_variable_stream_cardinality=True,
                                                     explicit_fixed_stream_cardinality=True,
                                                     explicit_common_cardinality=True,
                                                     high_level=True)
            meta_table = common.make_rst_meta_table(meta, index_format_func=lambda index: str(index + 1))
            desc = packet.get_matlab_formatted_doc(1)

            functions.append(template.format(ret_type, cls, name, params, meta_table, desc))

        return ''.join(functions)

    def get_matlab_callbacks(self):
        callbacks = []
        template = {
            'en': """
.. matlab:member:: callback {0}::{1}Callback

{2}

{3}

 In MATLAB the ``set()`` function can be used to register a callback function
 to this callback.

 In Octave a callback function can be added to this callback using the
 ``add{1}Callback()`` function. An added callback function can be removed with
 the ``remove{1}Callback()`` function.

""",
            'de': """
.. matlab:member:: callback {0}::{1}Callback

{2}

{3}

 In MATLAB kann die ``set()`` Function verwendet werden um diesem Callback eine
 Callback-Function zuzuweisen.

 In Octave kann diesem Callback mit ``add{1}Callback()`` eine Callback-Function
 hinzugefügt werden. Eine hinzugefügter Callback-Function kann mit
 ``remove{1}Callback()`` wieder entfernt werden.

"""
        }
        cls = self.get_matlab_class_name()

        for packet in self.get_packets('callback'):
            skip = -2 if packet.has_high_level() else 0
            desc = packet.get_matlab_formatted_doc(1)
            meta = packet.get_formatted_element_meta(lambda element, cardinality=None: element.get_matlab_type(cardinality=cardinality),
                                                     lambda element, index=None: element.get_name(index=index).headless,
                                                     callback_object='always',
                                                     callback_object_label_override={'en': 'Event Object', 'de': 'Event-Objekt'},
                                                     no_out_value={'en': 'empty object', 'de': 'leeres Objekt'},
                                                     explicit_string_cardinality=True,
                                                     explicit_variable_stream_cardinality=True,
                                                     explicit_fixed_stream_cardinality=True,
                                                     explicit_common_cardinality=True,
                                                     high_level=True)
            meta_table = common.make_rst_meta_table(meta, indent_level=1, index_format_func=lambda index: str(index + 1))

            callbacks.append(common.select_lang(template).format(cls,
                                                 packet.get_name(skip=skip).camel,
                                                 meta_table,
                                                 desc))

        return ''.join(callbacks)

    def get_matlab_api(self):
        create_str = {
            'en': """
.. matlab:function:: class {0}(String uid, IPConnection ipcon)

{2}

 Creates an object with the unique device ID ``uid``.

 In MATLAB:

 .. code-block:: matlab

  import com.tinkerforge.{0};

  {1} = {0}('YOUR_DEVICE_UID', ipcon);

 In Octave:

 .. code-block:: octave_fixed

  {1} = java_new("com.tinkerforge.{0}", "YOUR_DEVICE_UID", ipcon);

 This object can then be used after the IP Connection is connected.
""",
            'de': """
.. matlab:function:: class {0}(String uid, IPConnection ipcon)

{2}

 Erzeugt ein Objekt mit der eindeutigen Geräte ID ``uid``.

 In MATLAB:

 .. code-block:: matlab

  import com.tinkerforge.{0};

  {1} = {0}("YOUR_DEVICE_UID", ipcon);

 In Octave:

 .. code-block:: octave_fixed

  {1} = java_new("com.tinkerforge.{0}", "YOUR_DEVICE_UID", ipcon);

 Dieses Objekt kann benutzt werden, nachdem die IP Connection verbunden ist.
"""
        }

        ccf_str = {
            'en': """
Callback Configuration Functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

{0}
""",
            'de': """
Konfigurationsfunktionen für Callbacks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

{0}
"""
        }

        c_str = {
            'en': """
.. _{0}_matlab_callbacks:

Callbacks
^^^^^^^^^

Callbacks can be registered to receive time critical or recurring data from
the device. The registration is done with "set" function of MATLAB. The
parameters consist of the IP Connection object, the callback name and the
callback function. For example, it looks like this in MATLAB:

.. code-block:: matlab

    function my_callback(e)
        fprintf('Parameter: %s\\n', e.param);
    end

    set(device, 'ExampleCallback', @(h, e) my_callback(e));

Due to a difference in the Octave Java support the "set" function cannot be
used in Octave. The registration is done with "add*Callback" functions of the
device object. It looks like this in Octave:

.. code-block:: octave_fixed

    function my_callback(e)
        fprintf("Parameter: %s\\n", e.param);
    end

    device.addExampleCallback(@my_callback);

It is possible to add several callbacks and to remove them with the
corresponding "remove*Callback" function.

The parameters of the callback are passed to the callback function as fields of
the structure ``e``, which is derived from the ``java.util.EventObject`` class.
The available callback names with corresponding structure fields are described
below.

.. note::
 Using callbacks for recurring events is *always* preferred
 compared to using getters. It will use less USB bandwidth and the latency
 will be a lot better, since there is no round trip time.


{1}
""",
            'de': """
.. _{0}_matlab_callbacks:

Callbacks
^^^^^^^^^

Callbacks können registriert werden um zeitkritische oder wiederkehrende
Daten vom Gerät zu erhalten. Die Registrierung wird mit MATLABs "set"
Funktion durchgeführt. Die Parameter sind ein Gerätobjekt, der Callback-Name
und die Callback-Funktion. Hier ein Beispiel in MATLAB:

.. code-block:: matlab

    function my_callback(e)
        fprintf('Parameter: %s\\n', e.param);
    end

    set(device, 'ExampleCallback', @(h, e) my_callback(e));

Die Octave Java Unterstützung unterscheidet sich hier von MATLAB, die "set"
Funktion kann hier nicht verwendet werden. Die Registrierung wird in Octave
mit  "add*Callback" Funktionen des Gerätobjekts durchgeführt. Hier ein Beispiel
in Octave:

.. code-block:: octave_fixed

    function my_callback(e)
        fprintf("Parameter: %s\\n", e.param);
    end

    device.addExampleCallback(@my_callback);

Es ist möglich mehrere Callback-Funktion hinzuzufügen und auch mit einem
korrespondierenden "remove*Callback" wieder zu entfernen.

Die Parameter des Callbacks werden der Callback-Funktion als Felder der
Struktur ``e`` übergeben. Diese ist von der ``java.util.EventObject`` Klasse
abgeleitete. Die verfügbaren Callback-Namen mit den entsprechenden
Strukturfeldern werden unterhalb beschrieben.

.. note::
 Callbacks für wiederkehrende Ereignisse zu verwenden ist
 *immer* zu bevorzugen gegenüber der Verwendung von Abfragen.
 Es wird weniger USB-Bandbreite benutzt und die Latenz ist
 erheblich geringer, da es keine Paketumlaufzeit gibt.

{1}
"""
        }

        api = {
            'en': """
.. _{0}_matlab_api:

API
---

Generally, every method of the MATLAB bindings that returns a value can
throw a ``TimeoutException``. This exception gets thrown if the
device did not respond. If a cable based connection is used, it is
unlikely that this exception gets thrown (assuming nobody unplugs the
device). However, if a wireless connection is used, timeouts will occur
if the distance to the device gets too big.

Beside the ``TimeoutException`` there is also a ``NotConnectedException`` that
is thrown if a method needs to communicate with the device while the
IP Connection is not connected.

Since the MATLAB bindings are based on Java and Java does not support multiple
return values and return by reference is not possible for primitive types, we
use small classes that only consist of member variables. The member variables
of the returned objects are described in the corresponding method descriptions.

The package for all Brick/Bricklet bindings and the IP Connection is
``com.tinkerforge.*``

All methods listed below are thread-safe.

{1}

{2}
""",
            'de': """
.. _{0}_matlab_api:

API
---

Prinzipiell kann jede Methode der MATLAB Bindings eine ``TimeoutException``
werfen. Diese Exception wird
geworfen wenn das Gerät nicht antwortet. Wenn eine Kabelverbindung genutzt
wird, ist es unwahrscheinlich, dass die Exception geworfen wird (unter der
Annahme, dass das Gerät nicht abgesteckt wird). Bei einer drahtlosen Verbindung
können Zeitüberschreitungen auftreten, sobald die Entfernung zum Gerät zu
groß wird.

Neben der ``TimeoutException`` kann auch noch eine ``NotConnectedException``
geworfen werden, wenn versucht wird mit einem Brick oder Bricklet zu
kommunizieren, aber die IP Connection nicht verbunden ist.

Da die MATLAB Bindings auf Java basieren und Java nicht mehrere Rückgabewerte
unterstützt und eine Referenzrückgabe für elementare Type nicht möglich ist,
werden kleine Klassen verwendet, die nur aus Member-Variablen bestehen. Die
Member-Variablen des zurückgegebenen Objektes werden in der jeweiligen
Methodenbeschreibung erläutert.

Das Package für alle Brick/Bricklet Bindings und die IP Connection ist
``com.tinkerforge.*``

Alle folgend aufgelisteten Methoden sind Thread-sicher.

{1}

{2}
"""
        }

        const_str = {
            'en': """
.. _{0}_matlab_constants:

Constants
^^^^^^^^^

.. matlab:member:: int {1}::DEVICE_IDENTIFIER

 This constant is used to identify a {3}.

 The :matlab:func:`getIdentity() <{1}::getIdentity>` function and the
 :matlab:member:`IPConnection.EnumerateCallback <IPConnection::EnumerateCallback>`
 callback of the IP Connection have a ``deviceIdentifier`` parameter to specify
 the Brick's or Bricklet's type.

.. matlab:member:: String {1}::DEVICE_DISPLAY_NAME

 This constant represents the human readable name of a {3}.
""",
            'de': """
.. _{0}_matlab_constants:

Konstanten
^^^^^^^^^^

.. matlab:member:: int {1}::DEVICE_IDENTIFIER

 Diese Konstante wird verwendet um {2} {3} zu identifizieren.

 Die :matlab:func:`getIdentity() <{1}::getIdentity>` Funktion und der
 :matlab:member:`IPConnection.EnumerateCallback <IPConnection::EnumerateCallback>`
 Callback der IP Connection haben ein ``deviceIdentifier`` Parameter um den Typ
 des Bricks oder Bricklets anzugeben.

.. matlab:member:: String {1}::DEVICE_DISPLAY_NAME

 Diese Konstante stellt den Anzeigenamen eines {3} dar.
"""
        }

        create_meta = common.format_simple_element_meta([('uid', 'String', 1, 'in'),
                                                         ('ipcon', 'IPConnection', 1, 'in'),
                                                         (self.get_name().headless, self.get_matlab_class_name(), 1, 'out')])
        create_meta_table = common.make_rst_meta_table(create_meta, index_format_func=lambda index: str(index + 1))

        cre = common.select_lang(create_str).format(self.get_matlab_class_name(),
                                                    self.get_name().headless,
                                                    create_meta_table)

        bf = self.get_matlab_functions('bf')
        af = self.get_matlab_functions('af')
        ccf = self.get_matlab_functions('ccf')
        c = self.get_matlab_callbacks()
        vf = self.get_matlab_functions('vf')
        if_ = self.get_matlab_functions('if')
        api_str = ''

        if bf:
            api_str += common.select_lang(common.bf_str).format(cre, bf)

        if af:
            api_str += common.select_lang(common.af_str).format(af)

        if c:
            if ccf:
                api_str += common.select_lang(ccf_str).format(ccf)

            api_str += common.select_lang(c_str).format(self.get_doc_rst_ref_name(), c)

        if vf:
            api_str += common.select_lang(common.vf_str).format(vf)

        if if_:
            api_str += common.select_lang(common.if_str).format(if_)

        article = 'ein'

        if self.is_brick():
            article = 'einen'

        api_str += common.select_lang(const_str).format(self.get_doc_rst_ref_name(),
                                                        self.get_matlab_class_name(),
                                                        article,
                                                        self.get_long_display_name())

        return common.select_lang(api).format(self.get_doc_rst_ref_name(),
                                              self.specialize_matlab_doc_function_links(common.select_lang(self.get_doc())),
                                              api_str)

    def get_matlab_doc(self):
        doc  = common.make_rst_header(self)
        doc += common.make_rst_summary(self)
        doc += self.get_matlab_examples()
        doc += self.get_matlab_api()

        return doc

class MATLABDocPacket(matlab_common.MATLABPacket):
    def get_matlab_formatted_doc(self, shift_right):
        text = common.select_lang(self.get_doc_text())
        text = self.get_device().specialize_matlab_doc_function_links(text)

        def format_parameter(name):
            return '``{0}``'.format(name) # FIXME

        text = common.handle_rst_param(text, format_parameter)
        text = common.handle_rst_word(text)
        text = common.handle_rst_substitutions(text, self)

        prefix = self.get_device().get_matlab_class_name() + '.'

        def format_element_name(element, index):
            if index == None:
                return element.get_name().headless

            return '{0}({1})'.format(element.get_name().headless, index + 1)

        text += common.format_constants(prefix, self, format_element_name)
        text += common.format_since_firmware(self.get_device(), self)

        return common.shift_right(text, shift_right)

class MATLABDocGenerator(matlab_common.MATLABGeneratorTrait, common.DocGenerator):
    def get_bindings_name(self):
        return 'matlab'

    def get_bindings_display_name(self):
        return 'MATLAB/Octave'

    def get_doc_rst_filename_part(self):
        return 'MATLAB'

    def get_doc_example_regex(self):
        return r'^(matlab|octave)_example_.*\.m$'

    def get_device_class(self):
        return MATLABDocDevice

    def get_packet_class(self):
        return MATLABDocPacket

    def get_element_class(self):
        return matlab_common.MATLABElement

    def get_example_sort_key(self, example):
        return example[1].split('_')[0], example[2], example[0] # flavor, lines, filename

    def generate(self, device):
        with open(device.get_doc_rst_path(), 'w') as f:
            f.write(device.get_matlab_doc())

def generate(root_dir, language, internal):
    common.generate(root_dir, language, internal, MATLABDocGenerator)

if __name__ == '__main__':
    args = common.dockerize('matlab', __file__, add_internal_argument=True)

    for language in ['en', 'de']:
        generate(os.getcwd(), language, args.internal)
