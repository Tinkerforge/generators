#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import glob
import configparser

def error(message):
    print('\033[01;31m{0}\033[0m'.format(message))

def warning(message):
    print('\033[01;33m{0}\033[0m'.format(message))

def check_file(git_path, glob_pattern, expected_name, others_allowed=False):
    paths = glob.glob(os.path.join(git_path, glob_pattern))

    if len(paths) == 0:
        error('{0} is missing'.format(glob_pattern))
        return

    if len(paths) == 1:
        path = paths[0]
    else:
        if not others_allowed:
            error('more than one {0} file'.format(glob_pattern))
            return

        path = None

        for candidate in paths:
            if candidate.endswith(expected_name):
                path = candidate
                break

        if path == None:
            error('{0} is missing, or has wrong name'.format(expected_name))
            return

    if not path.endswith(expected_name):
        warning('{0} has wrong name (expected: {1}, found: {2})'.format(glob_pattern, os.path.split(expected_name)[-1], os.path.split(path)[-1]))
    elif os.system('cd {0}; git ls-files --error-unmatch {1} > /dev/null 2>&1'
                   .format(git_path, path.replace(git_path, '').lstrip('/'))) != 0:
        error('{0} is not tracked by git'.format(path.replace(git_path, '').lstrip('/')))

sys.path.append(os.path.realpath('configs'))

example_names = {}

for config_name in sorted(os.listdir('configs')):
    if not config_name.endswith('_config.py'):
        continue

    config = __import__(config_name[:-3]).com

    git_name = config['name'].lower().replace(' ', '-') + '-' + config['category'].lower()

    example_names[git_name] = []

    for example in config['examples']:
        example_names[git_name].append(example['name'])

example_name_formats = {
    'c': ['example_{under}.c'],
    'csharp': ['Example{camel}.cs'],
    'delphi': ['Example{camel}.pas'],
    'java': ['Example{camel}.java'],
    'javascript': ['Example{camel}.js', 'Example{camel}.html'],
    'labview': ['Example {space}.vi'],
    'mathematica': ['Example{camel}.nb', 'Example{camel}.nb.txt'],
    'matlab': ['matlab_example_{under}.m', 'octave_example_{under}.m'],
    'perl': ['example_{under}.pl'],
    'php': ['Example{camel}.php'],
    'python': ['example_{under}.py'],
    'ruby': ['example_{under}.rb'],
    'shell': ['example-{dash}.sh'],
    'vbnet': ['Example{camel}.vb'],
}

for git_name in sorted(os.listdir('..')):
    if not git_name.endswith('-brick') and not git_name.endswith('-bricklet') and not git_name.endswith('-extension'):
        continue

    print('>>>', git_name)

    base_name = '-'.join(git_name.split('-')[:-1])

    if not git_name.endswith('-extension'):
        if len(example_names.get(git_name, [])) == 0:
            error('no example definitions')
        else:
            print('examples:', ', '.join(example_names[git_name]))

    git_path = os.path.join('..', git_name)
    gitignore_path = os.path.join(git_path, '.gitignore')

    if not os.path.exists(gitignore_path):
        error('hardware/.gitignore is missing')
    else:
        with open(gitignore_path, 'r') as f:
            if 'hardware/kicad-libraries\n' not in f.readlines():
                error('hardware/kicad-libraries missing in .gitignore')

    hardware_path = os.path.join(git_path, 'hardware')
    kicad_libraries_path = os.path.join(hardware_path, 'kicad-libraries')

    if not os.path.exists(kicad_libraries_path):
        error('hardware/kicad-libraries is missing')

    # hardware/*.pro
    check_file(git_path, 'hardware/*.pro', 'hardware/{0}.pro'.format(base_name))

    # hardware/*.sch
    check_file(git_path, 'hardware/*.sch', 'hardware/{0}.sch'.format(base_name), others_allowed=True)

    # hardware/*-schematic.pdf
    check_file(git_path, 'hardware/*-schematic.pdf', 'hardware/{0}-schematic.pdf'.format(base_name))

    # hardware/*.kicad_pcb
    check_file(git_path, 'hardware/*.kicad_pcb', 'hardware/{0}.kicad_pcb'.format(base_name))

    # hardware/*.step
    check_file(git_path, 'hardware/*.step', 'hardware/{0}.step'.format(base_name))

    # hardware/*.FCStd
    check_file(git_path, 'hardware/*.FCStd', 'hardware/{0}.FCStd'.format(base_name))

    # hardware/*.brd
    if len(glob.glob(os.path.join(git_path, 'hardware/*.brd'))) > 0:
        warning('hardware/*.brd found')

    # check kicad-libraries configuration
    pro_path = os.path.join(git_path, 'hardware/{0}.pro'.format(base_name))

    if os.path.exists(pro_path):
        with open(pro_path, 'r') as f:
            pro_content = '[__dummy__]\n' + f.read()

        if '=special\n' in pro_content:
            error('hardware/*.pro uses special library')

        cp = configparser.ConfigParser()

        cp.read_string(pro_content)

        if 'pcbnew/libraries' in cp and \
           cp['pcbnew/libraries'].get('LibDir', 'kicad-libraries') != 'kicad-libraries':
            print('invalid pcbnew/libraries:LibDir in hardware/*.pro')

        if cp['eeschema']['LibDir'] != 'kicad-libraries':
            error('invalid eeschema:LibDir in hardware/*.pro')

        if cp['eeschema/libraries']['LibName1'] != 'tinkerforge':
            error('invalid eeschema/libraries:LibName1 in hardware/*.pro')

    # check examples
    for bindings_name in sorted(example_name_formats.keys()):
        for example_name in example_names.get(git_name, []):
            for example_name_format in example_name_formats[bindings_name]:
                example_full_name = example_name_format.format(space=example_name,
                                                               camel=example_name.replace(' ', ''),
                                                               under=example_name.replace(' ', '_').lower(),
                                                               dash=example_name.replace(' ', '-').lower())
                example_path = os.path.join(git_path, 'software/examples', bindings_name, example_full_name)

                if not os.path.exists(example_path):
                    error('{0} is missing'.format(example_path.replace(git_path, '').lstrip('/')))


    print('')

