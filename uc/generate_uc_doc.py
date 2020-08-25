#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
C/C++ for Microcontrollers Documentation Generator
Copyright (C) 2020 Erik Fleckstein <erik@tinkerforge.com>

generate_uc_doc.py: Generator for C/C++ documentation for microcontrollers

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
from generators.uc import uc_common
from generators.uc.uc_common import format

class UCDocDevice(common.Device):
    def specialize_c_doc_function_links(self, text):
        def specializer(packet, high_level):
            if packet.get_type() == 'callback':
                return format(':c:func:`{packet_space} <tf_{device_under}_register_{packet_under}_callback>`', packet.get_device(), packet, 0)
            else:
                return format(':c:func:`tf_{device_under}_{packet_under}`', packet.get_device(), packet, -2 if high_level else 0)

        return self.specialize_doc_rst_links(text, specializer, prefix='c')

    def get_c_examples(self):
        def title_from_filename(filename):
            filename = filename.replace('example_', '').replace('.c', '')
            return common.under_to_space(filename).replace('Pwm ', 'PWM ')

        return common.make_rst_examples(title_from_filename, self, language_from_filename=lambda f: 'c')

    def get_c_functions(self, type_):
        functions = []
        template = '.. c:function:: int tf_{device_under}_{packet_under}({params})\n\n{meta_table}{desc}\n'

        for packet in self.get_packets('function'):
            if packet.get_doc_type() != type_:
                continue

            if packet.get_name().under == 'get_api_version':
                continue

            skip = -2 if packet.has_high_level() else 0
            plist = common.wrap_non_empty(', ', packet.get_c_parameters(high_level=True), '')

            meta = packet.get_formatted_element_meta(lambda element, cardinality=None: element.get_c_type('meta', cardinality=cardinality),
                                                     lambda element, index=None: element.get_c_name(index=index),
                                                     output_parameter='always',
                                                     prefix_elements=[(self.get_name().under, 'TF_' + self.get_name().camel + ' *', 1, 'in')],
                                                     suffix_elements=[('error_code', 'int', 1, 'return')],
                                                     stream_length_suffix='_length',
                                                     high_level=True)

            functions.append(format(template, self, packet, skip,
                                    params=format('TF_{device_camel} *{device_under}{plist}', self, plist=plist),
                                    meta_table=common.make_rst_meta_table(meta),
                                    desc=packet.get_c_formatted_doc()))

        return ''.join(functions)

    def get_c_callbacks(self):
        callbacks = []
        template = '.. c:function:: void tf_{device_under}_register_{packet_under}_callback(TF_{device_camel} *{device_under}, TF_{device_camel}{packet_camel}Handler, void *user_data)\n{params}\n{meta_table}\n{desc}\n'
        param_template = {
            'en': """
 .. code-block:: c

  void handler({0})
""",
            'de': """
 .. code-block:: c

  void handler({0})
"""
        }

        for packet in self.get_packets('callback'):
            plist = format('TF_{device_camel} *{device_under}, ', self) + common.wrap_non_empty('', packet.get_c_parameters(), ', ') + 'void *user_data'

            meta = packet.get_formatted_element_meta(lambda element, cardinality=None: element.get_c_type('meta', cardinality=cardinality),
                                                     lambda element, index=None: element.get_c_name(index=index),
                                                     prefix_elements=[(format('{device_under}', self), format('TF_{device_camel} *', self), 1, 'out')],
                                                     suffix_elements=[('user_data', 'void *', 1, 'out')],
                                                     stream_length_suffix='_length')

            callbacks.append(format(template, self, packet,
                                    params=common.select_lang(param_template).format(plist),
                                    meta_table=common.make_rst_meta_table(meta),
                                    desc=packet.get_c_formatted_doc()))

        return ''.join(callbacks)

    def get_c_api(self):
        create_str = {
            'en': """
.. c:function:: int tf_{device_under}_create(TF_{device_camel} *{device_under}, const char *uid, TF_HalContext *hal)

{meta_table}

 Creates the device object ``{device_under}`` with the unique device ID ``uid`` and adds
 it to the HAL context ``hal``:

 .. code-block:: c

    TF_{device_camel} {device_under};
    tf_{device_under}_create(&{device_under}, "YOUR_DEVICE_UID", &hal);

 This device object can be used after the HAL has been initialized.
""",
            'de': """
.. c:function:: int tf_{device_under}_create(TF_{device_camel} *{device_under}, const char *uid, TF_HalContext *hal)

{meta_table}

 Erzeugt ein Geräteobjekt ``{device_under}`` mit der eindeutigen Geräte ID ``uid`` und
 fügt es dem HAL-Context ``hal`` hinzu:

 .. code-block:: c

    TF_{device_camel} {device_under};
    tf_{device_under}_create(&{device_under}, "YOUR_DEVICE_UID", &ipcon);

 Dieses Geräteobjekt kann benutzt werden, nachdem der HAL initialisiert wurde.
"""
        }

        destroy_str = {
            'en': """
.. c:function:: int tf_{device_under}_destroy(TF_{device_camel} *{device_under})

{meta_table}

 Removes the device object ``{device_under}`` from its HAL context and destroys it.
 The device object cannot be used anymore afterwards.
""",
            'de': """
.. c:function:: int tf_{device_under}_destroy(TF_{device_camel} *{device_under})

{meta_table}

 Entfernt das Geräteobjekt ``{device_under}`` von dessen HAL-Context und zerstört es.
 Das Geräteobjekt kann hiernach nicht mehr verwendet werden.
"""
        }

        c_str = {
            'en': """
.. _{device_doc_rst_ref}_uc_callbacks:

Callbacks
^^^^^^^^^

Callbacks can be registered to receive time critical or recurring data from the
device. The registration is done with the corresponding ``tf_{device_under}_register_*_callback`` function.
The ``user_data``  passed to the registration function as well as the device that triggered the callback are
passed to the registered callback handler.

.. note::
 Using callbacks for recurring events is preferred
 compared to using getters. Polling for a callback requires
 writing one Byte only. See here :ref:`api_bindings_uc_performance`.

.. warning::
 Calling bindings function from inside a callback handler is not allowed.
 See here :ref:`api_bindings_uc_thread_safety`.

{callbacks}
""",
            'de': """
.. _{device_doc_rst_ref}_uc_callbacks:

Callbacks
^^^^^^^^^

Callbacks können registriert werden um zeitkritische oder wiederkehrende Daten
vom Gerät zu erhalten. Die Registrierung kann mit der entsprechenden ``tf_{device_under}_register_*_callback``
Funktion durchgeführt werden. Die ``user_data``, sowie das Gerät, dass das Callback ausgelöst hat, werden
dem registrierten Callback-Handler übergeben.

Die verfügbaren Konstanten mit den zugehörigen Funktionssignaturen werden weiter
unten beschrieben.

.. note::
 Callbacks für wiederkehrende Ereignisse zu verwenden ist
 gegenüber der Verwendung von Abfragen zu bevorzugen.
 Es muss nur ein Byte abgefragt werden um zu prüfen ob ein Callback
 vorliegt. Siehe hier :ref:`api_bindings_uc_performance`.

.. warning::
 Aus Callback-Handlern heraus können keine Bindings-Funktionen verwendet werden.
 Siehe hier :ref:`api_bindings_uc_thread_safety`.

{callbacks}
"""
        }

        api = {
            'en': """
.. _{device_doc_rst_ref}_uc_api:

API
---

Every function of the C/C++ for microcontrollers bindings returns an integer which describes an
error code.

Possible error codes are:

* TF\_\ **E**\\ _OK = 0
* TF\_\ **E**\\ _TIMEOUT = -1
* TF\_\ **E**\\ _INVALID_PARAMETER = -2
* TF\_\ **E**\\ _NOT_SUPPORTED = -3
* TF\_\ **E**\\ _UNKNOWN_ERROR_CODE = -4
* TF\_\ **E**\\ _STREAM_OUT_OF_SYNC = -5
* TF\_\ **E**\\ _INVALID_CHAR_IN_UID = -6
* TF\_\ **E**\\ _UID_TOO_LONG = -7
* TF\_\ **E**\\ _UID_OVERFLOW = -8
* TF\_\ **E**\\ _TOO_MANY_DEVICES = -9
* TF\_\ **E**\\ _DEVICE_NOT_FOUND = -10
* TF\_\ **E**\\ _WRONG_DEVICE_TYPE = -11
* TF\_\ **E**\\ _CALLBACK_EXEC = -12
* TF\_\ **E**\\ _PORT_NOT_FOUND = -13

(as defined in :file:`errors.h`) as well as the errors returned from
the hardware abstraction layer (HAL) that is used.

.. cpp:namespace-push:: {device_under}

Use :cpp:func`tf_strerror` (also defined in :file:`errors.h`) to get
an error string for an error code.

.. cpp:function:: const char * tf_strerror(int rc)

 Returns an error string for the given error code.

.. cpp:namespace-pop::

Data returned from the device, when a getter is called,
is handled via output parameters. These parameters are labeled with the
``ret_`` prefix. The bindings will not write to an output parameter if NULL or nullptr
is passed. This can be used to ignore outputs that you are not interested in.

**None of the functions listed below are thread-safe.**
See the :ref:`API bindings description <api_bindings_uc>` for details.

{doc_str}

{api_str}
""",
            'de': """
.. _{device_doc_rst_ref}_uc_api:

API
---

Jede Funktion der C/C++ Bindings gibt einen Integer zurück, welcher einen
Fehlercode beschreibt.

Mögliche Fehlercodes sind:

* TF\_\ **E**\\ _OK = 0
* TF\_\ **E**\\ _TIMEOUT = -1
* TF\_\ **E**\\ _INVALID_PARAMETER = -2
* TF\_\ **E**\\ _NOT_SUPPORTED = -3
* TF\_\ **E**\\ _UNKNOWN_ERROR_CODE = -4
* TF\_\ **E**\\ _STREAM_OUT_OF_SYNC = -5
* TF\_\ **E**\\ _INVALID_CHAR_IN_UID = -6
* TF\_\ **E**\\ _UID_TOO_LONG = -7
* TF\_\ **E**\\ _UID_OVERFLOW = -8
* TF\_\ **E**\\ _TOO_MANY_DEVICES = -9
* TF\_\ **E**\\ _DEVICE_NOT_FOUND = -10
* TF\_\ **E**\\ _WRONG_DEVICE_TYPE = -11
* TF\_\ **E**\\ _CALLBACK_EXEC = -12
* TF\_\ **E**\\ _PORT_NOT_FOUND = -13

(wie in :file:`errors.h` definiert), sowie die Fehlercodes des verwendeten
Hardware-Abstraction-Layers (HALs). Mit ``tf_strerror`` (ebenfalls in :file:`errors.h`
definiert) kann ein Fehlerstring zu einem Fehlercode abgefragt werden.

Vom Gerät zurückgegebene Daten werden, wenn eine
Abfrage aufgerufen wurde, über Ausgabeparameter gehandhabt. Diese Parameter
sind mit dem ``ret_`` Präfix gekennzeichnet. Die Bindings schreiben einen
Ausgabeparameter nicht, wenn NULL bzw. nullptr übergeben wird. So können
uninteressante Ausgaben ignoriert werden.

**Keine der folgend aufgelisteten Funktionen ist Thread-sicher.**
Details finden sich in der :ref:`Beschreibung der API-Bindings <api_bindings_uc>`.

{doc_str}

{api_str}
"""
        }

        const_str = {
            'en': """
.. _{device_doc_rst_ref}_uc_constants:

Constants
^^^^^^^^^

.. c:var:: TF_{device_upper}_DEVICE_IDENTIFIER

 This constant is used to identify a {device_display}.

 The functions :c:func:`tf_{device_under}_get_identity` and :c:func:`tf_hal_get_device_info`
 have a ``device_identifier`` output parameter to specify
 the Brick's or Bricklet's type.

.. c:var:: TF_{device_upper}_DEVICE_DISPLAY_NAME

 This constant represents the human readable name of a {device_display}.
""",
            'de': """
.. _{device_doc_rst_ref}_uc_constants:

Konstanten
^^^^^^^^^^

.. c:var:: TF_{device_upper}_DEVICE_IDENTIFIER

 Diese Konstante wird verwendet um {article} {device_display} zu identifizieren.

 Die Funktionen :c:func:`tf_{device_under}_get_identity` und :c:func:`tf_hal_get_device_info`
 haben einen ``device_identifier`` Parameter um den Typ
 des Bricks oder Bricklets anzugeben.

.. c:var:: TF_{device_upper}_DEVICE_DISPLAY_NAME

 Diese Konstante stellt den Anzeigenamen eines {device_display} dar.
"""
        }

        create_meta = common.format_simple_element_meta([(format('{device_under}', self), format('TF_{device_camel} *', self), 1, 'in'),
                                                         ('uid', 'const char *', 1, 'in'),
                                                         ('hal', 'TF_HalContext *', 1, 'in')])
        create_meta_table = common.make_rst_meta_table(create_meta)

        cre = format(common.select_lang(create_str), self, meta_table=create_meta_table)

        destroy_meta = common.format_simple_element_meta([(format('{device_under}', self), format('TF_{device_camel} *', self), 1, 'in')])
        destroy_meta_table = common.make_rst_meta_table(destroy_meta)

        des = format(common.select_lang(destroy_str), self, meta_table=destroy_meta_table)

        bf = self.get_c_functions('bf')
        af = self.get_c_functions('af')
        ccf = self.get_c_functions('ccf')
        c = self.get_c_callbacks()
        vf = self.get_c_functions('vf')
        if_ = self.get_c_functions('if')
        api_str = ''

        if bf:
            api_str += common.select_lang(common.bf_str).format(cre + des, bf)

        if af:
            api_str += common.select_lang(common.af_str).format(af)

        if c:
            api_str += common.select_lang(common.ccf_str).format('', ccf)
            api_str += format(common.select_lang(c_str), self,
                              device_doc_rst_ref=self.get_doc_rst_ref_name(),
                              callbacks=c,
                              padding=' ' * len(self.get_name().under))

        if vf:
            api_str += common.select_lang(common.vf_str).format(vf)

        if if_:
            api_str += common.select_lang(common.if_str).format(if_)

        article = 'ein'

        if self.is_brick():
            article = 'einen'

        api_str += format(common.select_lang(const_str), self,
                          device_doc_rst_ref=self.get_doc_rst_ref_name(),
                          article=article)

        return format(common.select_lang(api), self,
                      device_doc_rst_ref=self.get_doc_rst_ref_name(),
                      doc_str=self.specialize_c_doc_function_links(common.select_lang(self.get_doc())),
                      api_str=api_str)

    def get_c_doc(self):
        doc  = common.make_rst_header(self)
        doc += common.make_rst_summary(self)
        doc += self.get_c_examples()
        doc += self.get_c_api()

        return doc

class UCDocPacket(uc_common.UCPacket):
    def get_c_formatted_doc(self):
        text = common.select_lang(self.get_doc_text())
        text = self.get_device().specialize_c_doc_function_links(text)

        def format_parameter(name):
            return '``{0}``'.format(name) # FIXME

        text = common.handle_rst_param(text, format_parameter)
        text = common.handle_rst_word(text)
        text = common.handle_rst_substitutions(text, self)

        prefix = 'TF_' + self.get_device().get_name().upper + '_'

        def format_element_name(element, index):
            if index == None:
                return element.get_c_name()

            return '{0}[{1}]'.format(element.get_c_name(), index)

        text += common.format_constants(prefix, self, format_element_name)
        text += common.format_since_firmware(self.get_device(), self)

        return common.shift_right(text, 1)

class UCDocGenerator(uc_common.UCGeneratorTrait, common.DocGenerator):
    def get_doc_rst_filename_part(self):
        return 'uC'

    def get_doc_example_regex(self):
        return r'^example_.*\.c$'

    def get_device_class(self):
        return UCDocDevice

    def get_packet_class(self):
        return UCDocPacket

    def get_element_class(self):
        return uc_common.UCElement

    def generate(self, device):
        if not device.has_comcu():
            return
        with open(device.get_doc_rst_path(), 'w') as f:
            f.write(device.get_c_doc())

def generate(root_dir, language):
    common.generate(root_dir, language, UCDocGenerator)

if __name__ == '__main__':
    for language in ['en', 'de']:
        print('=== Generating %s ===' % language)
        generate(os.getcwd(), language)
