#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import glob
import configparser
import json
import subprocess

def error(message):
    print('\033[01;31m{0}\033[0m'.format(message))

def warning(message):
    print('\033[01;33m{0}\033[0m'.format(message))

def info(message):
    print('\033[01;34m{0}\033[0m'.format(message))

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
    elif os.system('cd {0}; git ls-files --error-unmatch "{1}" > /dev/null 2>&1'
                   .format(git_path, path.replace(git_path, '').lstrip('/'))) != 0:
        error('{0} is not tracked by git'.format(path.replace(git_path, '').lstrip('/')))

sys.path.append(os.path.realpath('configs'))

configs = {}
config_contents = {}
example_names = {}

config_header = '''# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# {0} communication config
'''

if os.path.exists('github_token.txt'):
    with open('github_token.txt', 'r') as f:
        github_token = f.read().strip()
else:
    github_token = None

for config_name in sorted(os.listdir('configs')):
    if not config_name.endswith('_config.py'):
        continue

    config = __import__(config_name[:-3]).com
    git_name = config['name'].lower().replace(' ', '-') + '-' + config['category'].lower()
    configs[git_name] = config

    with open(os.path.join('configs', config_name), 'r') as f:
        config_contents[git_name] = f.read()

    example_names[git_name] = []

    for example in config['examples']:
        example_names[git_name].append(example['name'])

example_name_formats = {
    'c': ['example_{under}.c'],
    'csharp': ['Example{camel}.cs'],
    'delphi': ['Example{camel}.pas'],
    'java': ['Example{camel}.java'],
    'javascript': ['Example{camel}.js', 'Example{camel}.html'],
    'labview': ['Example {space}.vi', 'Example {space}.vi.png', '10.0/Example {space}.vi'],
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

    if git_name in configs:
        description = configs[git_name]['description']['en']
        released = configs[git_name]['released']
        category = configs[git_name]['category']
        comcu = 'comcu_bricklet' in configs[git_name]['features']

        print('>>>', git_name, '(released)' if released else '(not released)')

        if len(description.strip()) == 0 or 'FIXME' in description or 'TBD' in description or 'TODO' in description:
            warning('invalid description: ' + description)

        if configs[git_name]['display_name'].endswith(' 2.0'):
            full_display_name = configs[git_name]['display_name'][:-4] + ' ' + configs[git_name]['category'] + ' 2.0'
        elif configs[git_name]['display_name'].endswith(' 3.0'):
            full_display_name = configs[git_name]['display_name'][:-4] + ' ' + configs[git_name]['category'] + ' 3.0'
        else:
            full_display_name = configs[git_name]['display_name'] + ' ' + configs[git_name]['category']

        if not config_contents[git_name].startswith(config_header.format(full_display_name)):
            error('wrong header comment in config')
    else:
        description = None

        if (git_name.endswith('-brick') or git_name.endswith('-bricklet')) and \
           not git_name.startswith('breakout-') and not git_name.startswith('stack-breakout-') and \
           not git_name.startswith('debug-'):
            released = False
        else:
            released = None

        if git_name.endswith('-brick'):
            category = 'Brick'
        elif git_name.endswith('-bricklet'):
            category = 'Bricklet'
        else:
            category = None

        if git_name.endswith('-bricklet') and not git_name.startswith('breakout-'):
            comcu = True
        else:
            comcu = None

        print('>>>', git_name, '(no config)')

    git_path = os.path.join('..', git_name)

    if github_token != None:
        if b'github.com' in subprocess.check_output('cd {0}; git remote get-url origin'.format(git_path), shell=True):
            github = json.loads(subprocess.check_output(['curl', 'https://{0}@api.github.com/repos/Tinkerforge/{1}'.format(github_token, git_name)], stderr=subprocess.DEVNULL))

            if description != None and github['description'] != description:
                warning('github description mismatch: {0} (github) != {1} (config)'.format(github['description'], description))
            else:
                print('github description:', github['description'])

            print('github homepage:', github['homepage'])
        else:
            print('not hosted on github')
    else:
        warning('no github token')

    base_name = '-'.join(git_name.split('-')[:-1])

    if not git_name.endswith('-extension'):
        if len(example_names.get(git_name, [])) == 0:
            error('no example definitions')
        else:
            print('examples:', ', '.join(example_names[git_name]))

    # .gitignore
    gitignore_path = os.path.join(git_path, '.gitignore')

    if not os.path.exists(gitignore_path):
        error('.gitignore is missing')
    else:
        with open(gitignore_path, 'r') as f:
            if 'hardware/kicad-libraries\n' not in f.readlines():
                error('hardware/kicad-libraries missing in .gitignore')

    # README.rst
    readme_path = os.path.join(git_path, 'README.rst')

    if not os.path.exists(readme_path):
        error('README.rst is missing')
    else:
        with open(readme_path, 'r') as f:
            readme_data = f.read()

        if released != None:
            in_development = '\n**This {0} is currently in development.**\n'.format(category) in readme_data

            if released and (in_development or '*This' in readme_data):
                error('README.rst has in-development marker but config says released')
            elif not released and not in_development:
                error('config says not released but README.rst misses in-development marker')

        if '\n If you want to ' in readme_data:
            warning('wrong indentation in README.rst')

        if comcu and '\ntutorial (https://www.tinkerforge.com/en/doc/Tutorials/Tutorial_Build_Environment/Tutorial.html).\n' not in readme_data:
            warning('Co-MCU Bricklet with old-style README.rst')

    # hardware
    hardware_path = os.path.join(git_path, 'hardware')

    if not os.path.exists(hardware_path):
        warning('hardware/* is missing')
    else:
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

            if 'eeschema/libraries' not in cp or 'eeschema/libraries' not in cp['eeschema/libraries'] or cp['eeschema/libraries']['LibName1'] != 'tinkerforge':
                error('invalid eeschema/libraries:LibName1 in hardware/*.pro')

    # software
    software_path = os.path.join(git_path, 'software')

    if not os.path.exists(software_path):
        warning('software/* is missing')
    else:
        # software/Makefile
        makefile_path = os.path.join(software_path, 'Makefile')

        if not os.path.exists(makefile_path):
            error('software/Makefile is missing')

        # software/examples
        for bindings_name in sorted(example_name_formats.keys()):
            try:
                existing_names = list(os.listdir(os.path.join(software_path, 'examples', bindings_name)))
            except FileNotFoundError:
                existing_names = []

            for example_name in example_names.get(git_name, []):
                for example_name_format in example_name_formats[bindings_name]:
                    example_full_name = example_name_format.format(space=example_name,
                                                                   camel=example_name.replace(' ', ''),
                                                                   under=example_name.replace(' ', '_').lower(),
                                                                   dash=example_name.replace(' ', '-').lower())
                    example_path = os.path.join(software_path, 'examples', bindings_name, example_full_name)

                    if not os.path.exists(example_path):
                        error('{0} is missing'.format(example_path.replace(git_path, '').lstrip('/')))
                    elif os.system('cd {0}; git ls-files --error-unmatch "{1}" > /dev/null 2>&1'
                                   .format(git_path, example_path.replace(git_path, '').lstrip('/'))) != 0:
                        error('{0} is not tracked by git'.format(example_path.replace(git_path, '').lstrip('/')))

                    if os.path.exists(example_path) and not example_path.endswith('.vi'): # ignore binary LabVIEW files
                        with open(example_path, 'rb') as f:
                            if b'incomplete' in f.read():
                                error('{0} is incomplete'.format(example_path.replace(git_path, '').lstrip('/')))

                    if example_full_name in existing_names:
                        existing_names.remove(example_full_name)

            # FIXME: ignore LabVIEW for now because of its extra files
            if len(existing_names) > 0 and bindings_name != 'labview':
                info('unexpected {0} example files: {1}'.format(bindings_name, ', '.join(existing_names)))

        if comcu:
            # software/src/communication.c
            communication_c_path = os.path.join(software_path, 'src/communication.c')

            if os.path.exists(communication_c_path):
                with open(communication_c_path, 'r') as f:
                    for i, line in enumerate(f.readlines()):
                        if 'header.length' in line and not '_Response' in line:
                            error('wrong response length in line {0}'.format(i + 1))

    print('')
