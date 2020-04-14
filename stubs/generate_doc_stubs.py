#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Hardware Documentation Stubs Generator
Copyright (C) 2017 Olaf Lüke <olaf@tinkerforge.com>

generate_doc_stubs.py: Generator for hardware documentation stubs

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
import datetime
import shutil

sys.path.append(os.path.split(os.getcwd())[0])
import common
import c.c_common as c_common

class DocStubGenerator(common.Generator):
    template_en = """
:DISABLED_shoplink: ../../../shop/{6}s/{4}.html

.. include:: {3}.substitutions
   :start-after: >>>substitutions
   :end-before: <<<substitutions

.. _{1}:

{0}
{7}

.. note::
  This Bricklet is currently work-in-progress!

..
    .. raw:: html

	{{% tfgallery %}}

	Bricklets/bricklet_{2}_tilted_[?|?].jpg           {0}
	Bricklets/bricklet_{2}_horizontal_[?|?].jpg       {0}
	Bricklets/bricklet_{2}_master_[100|600].jpg       {0} with Master Brick
	Cases/bricklet_{2}_case_[100|600].jpg             {0} with case
	Bricklets/bricklet_{2}_brickv_[100|].jpg          {0} in Brick Viewer
	Dimensions/{1}_dimensions_[100|600].png  Outline and drilling plan

	{{% tfgalleryend %}}


Features
--------

* TBD
* TBD


.. _{1}_description:

Description
-----------

TBD


Technical Specifications
------------------------

================================  ============================================================
Property                          Value
================================  ============================================================
Current Consumption               TBDmA
--------------------------------  ------------------------------------------------------------
--------------------------------  ------------------------------------------------------------
P TBD                             V TBD
--------------------------------  ------------------------------------------------------------
--------------------------------  ------------------------------------------------------------
Dimensions (W x D x H)            TBD x TBD x TBDmm (TBD x TBD x TBD")
Weight                            TBDg
================================  ============================================================


Resources
---------

* Schematic (`Download <https://github.com/Tinkerforge/{4}/raw/master/hardware/{5}-schematic.pdf>`__)
* Outline and drilling plan (`Download <../../_images/Dimensions/{1}_dimensions.png>`__)
* Source code and design files (`Download <https://github.com/Tinkerforge/{4}/zipball/master>`__)
* 3D model (`View online <https://autode.sk/TBD>`__ | Download: `STEP <https://download.tinkerforge.com/3d/TBD/TBD.step>`__, `FreeCAD <https://download.tinkerforge.com/3d/TBD/TBD.FCStd>`__)


.. _{1}_test:

Test your {0}
----------{8}

|test_intro|

|test_connect|.

|test_tab|
If everything went as expected ... TBD.

..
	.. image:: /Images/Bricklets/bricklet_{2}_brickv.jpg
	   :scale: 100 %
	   :alt: {0} in Brick Viewer
	   :align: center
	   :target: ../../_images/Bricklets/bricklet_{2}_brickv.jpg

|test_pi_ref|


.. _{1}_case:

Case
----

..
	A `laser-cut case for the {0}
	<https://www.tinkerforge.com/en/shop/cases/case-{4}.html>`__ is available.

	.. image:: /Images/Cases/bricklet_{2}_case_350.jpg
	   :scale: 100 %
	   :alt: Case for {0}
	   :align: center
	   :target: ../../_images/Cases/bricklet_{2}_case_1000.jpg

	.. include:: {3}.substitutions
	   :start-after: >>>bricklet_case_steps
	   :end-before: <<<bricklet_case_steps

	.. image:: /Images/Exploded/{2}_exploded_350.png
	   :scale: 100 %
	   :alt: Exploded assembly drawing for {0}
	   :align: center
	   :target: ../../_images/Exploded/{2}_exploded.png

	|bricklet_case_hint|


.. _{1}_programming_interface:

Programming Interface
---------------------

See :ref:`Programming Interface <programming_interface>` for a detailed description.

.. include:: {3}_hlpi.table
"""

    template_de = """
:DISABLED_shoplink: ../../../shop/{6}s/{4}.html

.. include:: {3}.substitutions
   :start-after: >>>substitutions
   :end-before: <<<substitutions

.. _{1}:

{0}
{7}

.. note::
  Dieses Bricklet befindet sich aktuell noch in der Entwicklung!

..
    .. raw:: html

	{{% tfgallery %}}

	Bricklets/bricklet_{2}_tilted_[?|?].jpg           {0}
	Bricklets/bricklet_{2}_horizontal_[?|?].jpg       {0}
	Bricklets/bricklet_{2}_master_[100|600].jpg       {0} mit Master Brick
	Cases/bricklet_{2}_case_[100|600].jpg             {0} im Gehäuse
	Bricklets/bricklet_{2}_brickv_[100|].jpg          {0} im Brick Viewer
	Dimensions/{1}_dimensions_[100|600].png  Umriss und Bohrplan

	{{% tfgalleryend %}}


Features
--------

* TBD
* TBD


.. _{1}_description:

Beschreibung
------------

TBD


Technische Spezifikation
------------------------

================================  ============================================================
Eigenschaft                       Wert
================================  ============================================================
Stromverbrauch                    TBDmA
--------------------------------  ------------------------------------------------------------
--------------------------------  ------------------------------------------------------------
E TBD                             W TBD
--------------------------------  ------------------------------------------------------------
--------------------------------  ------------------------------------------------------------
Abmessungen (B x T x H)           TBD x TBD x TBDmm (TBD x TBD x TBD")
Gewicht                           TBDg
================================  ============================================================


Ressourcen
----------

* Schaltplan (`Download <https://github.com/Tinkerforge/{4}/raw/master/hardware/{5}-schematic.pdf>`__)
* Umriss und Bohrplan (`Download <../../_images/Dimensions/{1}_dimensions.png>`__)
* Quelltexte und Platinenlayout (`Download <https://github.com/Tinkerforge/{4}/zipball/master>`__)
* 3D Modell (`Online ansehen <https://autode.sk/TBD>`__ | Download: `STEP <https://download.tinkerforge.com/3d/TBD/TBD.step>`__, `FreeCAD <https://download.tinkerforge.com/3d/TBD/TBD.FCStd>`__)


.. _{1}_test:

Erster Test
-----------

|test_intro|

|test_connect|.

|test_tab|
Wenn alles wie erwartet funktioniert ... TBD.

..
	.. image:: /Images/Bricklets/bricklet_{2}_brickv.jpg
	   :scale: 100 %
	   :alt: {0} im Brick Viewer
	   :align: center
	   :target: ../../_images/Bricklets/bricklet_{2}_brickv.jpg

|test_pi_ref|


.. _{1}_case:

Gehäuse
-------

..
	Ein `laser-geschnittenes Gehäuse für das {0}
	<https://www.tinkerforge.com/de/shop/cases/case-{4}.html>`__ ist verfügbar.

	.. image:: /Images/Cases/bricklet_{2}_case_350.jpg
	   :scale: 100 %
	   :alt: Gehäuse für {0}
	   :align: center
	   :target: ../../_images/Cases/bricklet_{2}_case_1000.jpg

	.. include:: {3}.substitutions
	   :start-after: >>>bricklet_case_steps
	   :end-before: <<<bricklet_case_steps

	.. image:: /Images/Exploded/{2}_exploded_350.png
	   :scale: 100 %
	   :alt: Explosionszeichnung für {0}
	   :align: center
	   :target: ../../_images/Exploded/{2}_exploded.png

	|bricklet_case_hint|


.. _{1}_programming_interface:

Programmierschnittstelle
------------------------

Siehe :ref:`Programmierschnittstelle <programming_interface>` für eine detaillierte
Beschreibung.

.. include:: {3}_hlpi.table
"""

    def get_bindings_name(self):
        return 'stubs'

    def get_bindings_display_name(self):
        return 'Hardware Documentation Stubs'

    def get_device_class(self):
        return common.Device

    def get_packet_class(self):
        return c_common.CPacket

    def get_element_class(self):
        return c_common.CElement

    def get_doc_null_value_name(self):
        return 'NULL'

    def get_doc_formatted_param(self, element):
        return element.get_name().under

    def prepare(self):
        if self.get_config_name().space == 'Tinkerforge':
            name = 'doc'
        else:
            name = 'doc_' + self.get_config_name().under

        common.recreate_dir(os.path.join(self.get_root_dir(), name))

        for language in ['en', 'de']:
            for category in ['Bricks', 'Bricklets']:
                os.makedirs(os.path.join(self.get_root_dir(), name, language, category))

    def generate(self, device):
        if device.is_tng():
            return # FIXME

        if self.get_config_name().space == 'Tinkerforge':
            folder = 'doc'
        else:
            folder = 'doc_' + self.get_config_name().under

        # Example format:
        # {0} = Thermal Imaging Bricklet
        # {1} = thermal_imaging_bricklet
        # {2} = thermal_imaging
        # {3} = Thermal_Imaging
        # {4} = thermal-imaging-bricklet
        # {5} = thermal-imaging

        format0 = device.get_long_display_name()
        format1 = device.get_name().under + '_' + device.get_category().under
        format2 = device.get_name().under
        format3 = device.get_name().space.replace(' ', '_')
        format4 = device.get_name().dash + '-' + device.get_category().dash
        format5 = device.get_name().dash
        filename = format3.replace('Real_Time_Clock', 'RealTime_Clock')

        if device.get_category().space == 'Brick':
            filename += '_Brick.rst'
        else:
            filename += '.rst'

        with open(os.path.join(folder, 'en', device.get_category().camel + 's', filename), 'w') as doc:
            doc.write(self.template_en.format(format0, format1, format2, format3, format4, format5, device.get_category().under, '='*len(format0), '-'*len(format0)))

        with open(os.path.join(folder, 'de', device.get_category().camel + 's', filename), 'w') as doc:
            doc.write(self.template_de.format(format0, format1, format2, format3, format4, format5, device.get_category().under, '='*len(format0)))

def generate(root_dir):
    common.generate(root_dir, 'en', DocStubGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
