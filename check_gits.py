#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import glob
import configparser

def error(message):
    print('\033[01;31m{0}\033[0m'.format(message))

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

    os.path.join(git_path, 'hardware')

    pro_paths = glob.glob(os.path.join(hardware_path, '*.pro'))

    if len(pro_paths) == 0:
        error('hardware/*.pro is missing')
    elif len(pro_paths) > 1:
        error('too many hardware/*.pro files')
    else:
        pro_path = pro_paths[0]

        if not pro_path.endswith('/{0}.pro'.format(base_name)):
            error('hardware/*.pro has wrong name')

        # hardware/*.sch
        sch_path = pro_path[:-4] + '.sch'

        if not os.path.exists(sch_path):
            error('hardware/*.sch is missing')
        elif not sch_path.endswith('/{0}.sch'.format(base_name)):
            error('hardware/*.sch has wrong name')
        elif os.system('cd {0}; git ls-files --error-unmatch {1} > /dev/null 2>&1'
                       .format(git_path, sch_path.replace(git_path, '').lstrip('/'))) != 0:
            error('hardware/*.sch is not tracked by git')

        pdf_paths = glob.glob(os.path.join(hardware_path, '*-schematic.pdf'))

        # hardware/*-schematic.pdf
        if len(pdf_paths) == 0:
            error('hardware/*-schematic.pdf is missing')
        elif len(pdf_paths) > 1:
            error('too many hardware/*-schematic.pdf files')
        elif not pdf_paths[0].endswith('/{0}-schematic.pdf'.format(base_name)):
            error('hardware/*-schematic.pdf has wrong name')
        elif os.system('cd {0}; git ls-files --error-unmatch {1} > /dev/null 2>&1'
                       .format(git_path, pdf_paths[0].replace(git_path, '').lstrip('/'))) != 0:
            error('hardware/*-schematic.pdf is not tracked by git')

        # hardware/*.kicad_pcb
        kicad_pcb_path = pro_path[:-4] + '.kicad_pcb'

        if not os.path.exists(kicad_pcb_path):
            error('hardware/*.kicad_pcb is missing')
        elif not kicad_pcb_path.endswith('/{0}.kicad_pcb'.format(base_name)):
            error('hardware/*.kicad_pcb has wrong name')
        elif os.system('cd {0}; git ls-files --error-unmatch {1} > /dev/null 2>&1'
                       .format(git_path, kicad_pcb_path.replace(git_path, '').lstrip('/'))) != 0:
            error('hardware/*.kicad_pcb is not tracked by git')

        # hardware/*.step
        step_path = pro_path[:-4] + '.step'

        if not os.path.exists(step_path):
            error('hardware/*.step is missing')
        elif not step_path.endswith('/{0}.step'.format(base_name)):
            error('hardware/*.step has wrong name')
        elif os.system('cd {0}; git ls-files --error-unmatch {1} > /dev/null 2>&1'
                       .format(git_path, step_path.replace(git_path, '').lstrip('/'))) != 0:
            error('hardware/*.step is not tracked by git')

        # hardware/*.FCStd
        fcstd_path = pro_path[:-4] + '.FCStd'

        if not os.path.exists(fcstd_path):
            error('hardware/*.FCStd is missing')
        elif not fcstd_path.endswith('/{0}.FCStd'.format(base_name)):
            error('hardware/*.FCStd has wrong name')
        elif os.system('cd {0}; git ls-files --error-unmatch {1} > /dev/null 2>&1'
                       .format(git_path, fcstd_path.replace(git_path, '').lstrip('/'))) != 0:
            error('hardware/*.FCStd is not tracked by git')

        # hardware/*.brd
        if os.path.exists(pro_path[:-4] + '.brd'):
            error('hardware/*.brd found')

        # check kicad-libraries configuration
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

