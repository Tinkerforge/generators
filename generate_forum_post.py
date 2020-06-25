#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

if sys.hexversion < 0x3040000:
    print('Python >= 3.4 required')
    sys.exit(1)

import os
import importlib.util
import importlib.machinery

generators_dir = os.path.dirname(os.path.realpath(__file__))

def create_generators_module():
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

DISPLAY_NAMES = {
'c':           'C/C++',
'csharp':      'C#',
'delphi':      'Delphi/Lazarus',
'go':          'Go',
'java':        'Java',
'javascript':  'JavaScript',
'labview':     'LabVIEW',
'mathematica': 'Mathematica',
'matlab':      'MATLAB/Octave',
'mqtt':        'MQTT',
'perl':        'Perl',
'php':         'PHP',
'python':      'Python',
'ruby':        'Ruby',
'rust':        'Rust',
'saleae':      'Saleae',
'shell':       'Shell',
'vbnet':       'Visual Basic .NET'
}

def main(base_path):
    bindings = []

    for d in sorted(os.listdir(base_path)):
        if os.path.isdir(d):
            if not d in ['tcpip', 'modbus', 'configs', '.git', '__pycache__', 'tvpl', 'json', 'stubs', 'openhab']:
                bindings.append(d)

    display_names = []
    downloads = []

    for binding in bindings:
        if len(sys.argv) > 1 and binding not in sys.argv[1:]:
            continue

        path = os.path.join(base_path, binding)
        version = common.get_changelog_version(path)

        display_names.append('{0} {1}.{2}.{3}'.format(DISPLAY_NAMES[binding], *version))
        downloads.append('<a href="https://download.tinkerforge.com/bindings/{0}/tinkerforge_{0}_bindings_{2}_{3}_{4}.zip">{1}</a>'
                         .format(binding, DISPLAY_NAMES[binding], *version))

    print("""<p><strong>Bindings:
{0}
</strong></p>
<ul>
<li>...</li>
</ul>
<p>Download:
{1}
</p>
""".format(',\n'.join(display_names), ',\n'.join(downloads)))

if __name__ == "__main__":
    main(os.getcwd())
