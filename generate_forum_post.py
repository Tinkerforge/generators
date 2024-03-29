#!/usr/bin/env python3
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
    'vbnet':       'Visual Basic .NET',
    'uc':          'C/C++ for Microcontrollers'
}

BINDINGS_ORDER = [
    'c',
    'uc',
    'csharp',
    'delphi',
    'go',
    'java',
    'javascript',
    'labview',
    'mathematica',
    'matlab',
    'mqtt',
    'perl',
    'php',
    'python',
    'ruby',
    'rust',
    'saleae',
    'shell',
    'vbnet'
]

def main():
    bindings = []

    for binding in os.listdir(generators_dir):
        if not os.path.isdir(binding) or os.path.exists(os.path.join(generators_dir, binding, 'skip_generate_forum_post')):
            continue

        if binding not in ['.git', '.vscode', '.m2', '__pycache__', 'configs', 'docker']:
            bindings.append(binding)

    result = {}

    for binding in bindings:
        if len(sys.argv) > 1 and binding not in sys.argv[1:]:
            continue

        path = os.path.join(generators_dir, binding)
        version = common.get_changelog_version(path)

        result[binding] = ('{0} {1}.{2}.{3}'.format(DISPLAY_NAMES[binding], *version),
                           '<a href="https://download.tinkerforge.com/bindings/{0}/tinkerforge_{0}_bindings_{2}_{3}_{4}.zip">{1}</a>'
                           .format(binding, DISPLAY_NAMES[binding], *version))

    sorted_result = []

    for binding in BINDINGS_ORDER:
        try:
            sorted_result.append(result[binding])
        except KeyError:
            pass

    print("""<p><strong>Bindings:
{0}
</strong></p>
<ul>
<li>...</li>
</ul>
<p>Download:
{1}
</p>
""".format(',\n'.join([item[0] for item in sorted_result]), ',\n'.join([item[1] for item in sorted_result])))

if __name__ == '__main__':
    main()
