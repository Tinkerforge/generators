#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

if sys.hexversion < 0x3040000:
    print('Python >= 3.4 required')
    sys.exit(1)

import os
import common

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
'shell':       'Shell',
'vbnet':       'Visual Basic .NET'
}

def download_links(base_path):
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
 
    print("""<p><strong>Bindings: {0}</strong></p>

<ul>
<li>...</li>
</ul>
<p>Download: {1}</p>
""".format(', '.join(display_names), ', '.join(downloads)))

if __name__ == "__main__":
    download_links(os.getcwd())
