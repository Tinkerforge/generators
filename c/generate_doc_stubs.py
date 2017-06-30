#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
C/C++ Bindings Generator
Copyright (C) 2017 Olaf Lüke <olaf@tinkerforge.com>

generate_doc_stubs.py: Generator for documentstion stubs
                        
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
import datetime
import shutil
from sets import Set

sys.path.append(os.path.split(os.getcwd())[0])
import common
import c_common

class DocStubBindingsDevice(common.Device):
    pass


class DocStubBindingsPacket(c_common.CPacket):
    pass

class DocStubBindingsGenerator(common.BindingsGenerator):
    template_en = """:breadcrumbs: <a href="../../index.html">Home</a> / <a href="../../index.html#hardware">Hardware</a> / {0}
:FIXME_shoplink: ../../../shop/bricklets/{4}.html

.. include:: {3}.substitutions
   :start-after: >>>substitutions
   :end-before: <<<substitutions

.. _{1}:

{0}
========================

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
* 3D model (`View online <TBD>`__ | Download: `STEP <http://download.tinkerforge.com/3d/TBD/TBD.step>`__, `FreeCAD <http://download.tinkerforge.com/3d/TBD/TBD.FCStd>`__)

.. _{1}_test:

Test your {0}
----------------------------------

|test_intro|

|test_connect|.

|test_tab|
If everything went as expected ... TBD.

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

    template_de = """:breadcrumbs: <a href="../../index.html">Home</a> / <a href="../../index.html#hardware">Hardware</a> / {0}
:FIXME_shoplink: ../../../shop/bricklets/{4}.html

.. include:: {3}.substitutions
   :start-after: >>>substitutions
   :end-before: <<<substitutions

.. _{1}:

{0}
========================

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



Resources
---------

* Schaltplan (`Download <https://github.com/Tinkerforge/{4}/raw/master/hardware/{5}-schematic.pdf>`__)
* Umriss und Bohrplan (`Download <../../_images/Dimensions/{1}_dimensions.png>`__)
* Quelltexte und Platinenlayout (`Download <https://github.com/Tinkerforge/{4}/zipball/master>`__)
* 3D Modell (`Online ansehen <TBD>`__ | Download: `STEP <http://download.tinkerforge.com/3d/TBD/TBD.step>`__, `FreeCAD <http://download.tinkerforge.com/3d/TBD/TBD.FCStd>`__)

.. _{1}_test:

Erster Test
-----------

|test_intro|

|test_connect|.

|test_tab|
Wenn alles wie erwartet funktioniert ... TBD.

.. image:: /Images/Bricklets/bricklet_{2}_brickv.jpg
   :scale: 100 %
   :alt: {0} im Brick Viewer
   :align: center
   :target: ../../_images/Bricklets/bricklet_{2}_brickv.jpg

|test_pi_ref|

.. _{1}_case:

Case
----

..
	Ein `laser-geschnittenes Gehäuse für das {0} 
	<https://www.tinkerforge.com/de/shop/cases/case-{4}.html>`__ ist verfügbar.

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

    def get_bindings_name(self):
        return 'c'

    def get_bindings_display_name(self):
        return 'doc'

    def get_device_class(self):
        return DocStubBindingsDevice

    def get_packet_class(self):
        return DocStubBindingsPacket

    def get_element_class(self):
        return c_common.CElement

    def generate(self, device):
        folder = os.path.join(self.get_bindings_root_directory(), 'doc_output', '{0}_{1}'.format(device.get_underscore_category(), device.get_underscore_name()))
        try:
            shutil.rmtree(folder) # first we delete the doc output if it already exists for this device
        except:
            pass # It is OK if the directory does not exist...
        
        # Example format:
        # {0} = Thermal Imaging Bricklet
        # {1} = thermal_imaging_bricklet
        # {2} = thermal_imaging
        # {3} = Thermal_Imaging
        # {4} = thermal-imaging-bricklet
        # {5} = thermal-imaging

        format0 = device.get_long_display_name()
        format1 = device.get_underscore_name() + '_' + device.get_underscore_category()
        format2 = device.get_underscore_name()
        format3 = device.get_name().replace(' ', '_')
        format4 = device.get_dash_name() + '-' + device.get_underscore_category()
        format5 = device.get_dash_name()
        filename = format3 + '.rst'

        os.makedirs(os.path.join(folder, 'en'))
        os.makedirs(os.path.join(folder, 'de'))


        with open(os.path.join(folder, 'en', filename), 'w') as doc:
            doc.write(self.template_en.format(format0, format1, format2, format3, format4, format5))

        with open(os.path.join(folder, 'de', filename), 'w') as doc:
            doc.write(self.template_de.format(format0, format1, format2, format3, format4, format5))

def generate(bindings_root_directory):
    common.generate(bindings_root_directory, 'en', DocStubBindingsGenerator)

if __name__ == "__main__":
    generate(os.getcwd())
