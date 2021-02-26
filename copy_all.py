#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

if sys.hexversion < 0x3040000:
    print('Python >= 3.4 required')
    sys.exit(1)

import os
import shutil
import filecmp
import socket
import zipfile
import tempfile
import glob
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

doc_git = 'doc'

def text_files_are_not_the_same(src_file, dest_path):
    dest_file = os.path.join(dest_path, src_file.split('/')[-1])

    try:
        with open(src_file, 'r') as f:
            lines1 = f.readlines()

        with open(dest_file, 'r') as f:
            lines2 = f.readlines()
    except:
        return True

    if len(lines1) != len(lines2):
        return True

    t = 'This file was automatically generated on'
    for l1, l2 in zip(lines1, lines2):
        if l1 != l2:
            if t in l1 and t in l2:
                continue

            return True

    return False

def files_are_not_the_same(src_file, dest_path):
    if src_file.endswith('.vi') or src_file.endswith('.vi.png'):
        dest_file = os.path.join(dest_path, src_file.split('/')[-1])

        try:
            with open(src_file, 'rb') as f:
                data1 = f.read()

            with open(dest_file, 'rb') as f:
                data2 = f.read()
        except:
            return True

        return data1 != data2
    else:
        return text_files_are_not_the_same(src_file, dest_path)

def main():
    path = generators_dir
    start_path = os.path.realpath(os.path.join(generators_dir, '..'))
    brickv_path_bindings = os.path.join(start_path, 'brickv/src/brickv/bindings')
    flash_test_path_bindings = os.path.join(start_path, 'flash-test/src/flash-test/plugin_system/tinkerforge')
    bindings = []

    for binding in os.listdir(generators_dir):
        if not os.path.isdir(binding) or os.path.exists(os.path.join(generators_dir, binding, 'skip_copy_all')):
            continue

        if binding not in ['.git', '.m2', '.vscode', '__pycache__', 'configs', 'docker']:
            bindings.append(binding)

    bindings = sorted(bindings)

    if socket.gethostname() != 'tinkerforge.com':
        for tool_name, tool_path in [('brickv', brickv_path_bindings),
                                     ('flash-test', flash_test_path_bindings)]:
            print('')
            print('Copying ip_connection to {0}:'.format(tool_name))

            src_file = os.path.join(path, 'python', 'ip_connection.py')

            if files_are_not_the_same(src_file, tool_path):
                shutil.copy(src_file, tool_path)
                print(' * ip_connection.py')

            print('')
            print('Copying Python bindings to {0}:'.format(tool_name))

            path_binding = os.path.join(path, 'python')
            src_file_path = os.path.join(path_binding, 'bindings')
            files = [f for f in os.listdir(src_file_path) if f.endswith('.py')]

            files.remove('device_factory.py')

            if tool_name != 'flash-test':
                files.remove('device_factory_all.py')

            for f in files:
                src_file = os.path.join(src_file_path, f)

                if files_are_not_the_same(src_file, tool_path):
                    shutil.copy(src_file, tool_path)
                    print(' * {0}'.format(f))

    doc_copy = [('_Brick_', 'Bricks'),
                ('_Bricklet_', 'Bricklets'),
                ('IPConnection_', '.')]

    to_delete = {'en': {}, 'de': {}}

    doc_path = os.path.join(doc_git, '{0}/source/Software')
    labview_image_path = os.path.join(doc_git, 'en/source/Images/Screenshots/LabVIEW')

    for lang in ['en', 'de']:
        print('')
        print("Copying '{0}' documentation and examples:".format(lang))

        for t in doc_copy:
            dest_dir = os.path.join(start_path, doc_path.format(lang), t[1])

            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)

            to_delete[lang][t[1]] = os.listdir(dest_dir)

        for binding in bindings:
            path_binding = os.path.join(path, binding)
            src_file_path = os.path.join(path_binding, 'doc', lang)

            for f in os.listdir(src_file_path):
                if f.endswith('.swp'):
                    continue

                for t in doc_copy:
                    if t[0] in f:
                        src_file = os.path.join(src_file_path, f)

                        if f.endswith('.vi.png'):
                            if lang != 'en':
                                continue

                            dest_path = os.path.join(start_path, labview_image_path)
                        else:
                            dest_path = os.path.join(start_path, doc_path.format(lang), t[1])
                            try:
                                to_delete[lang][t[1]].remove(f)
                            except:
                                pass

                        if files_are_not_the_same(src_file, dest_path):
                            shutil.copy(src_file, dest_path)
                            print(' * {0}'.format(f))

    if socket.gethostname() != 'tinkerforge.com':
        for lang in ['en', 'de']:
            print('')
            print('Copying Tinkerforge.js to {0}:'.format(os.path.join(doc_git, lang)))

            src_file = os.path.join(path, 'javascript', 'Tinkerforge.js')
            dest_dir = os.path.join(start_path, doc_path.format(lang), t[1])

            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)

            if files_are_not_the_same(src_file, dest_dir):
                shutil.copy(src_file, dest_dir)
                print(' * Tinkerforge.js')
    else:
        tmp_dir = tempfile.mkdtemp()

        zf = zipfile.ZipFile('/srv/web/com.tinkerforge.download/downloads/bindings/javascript/tinkerforge_javascript_bindings_latest.zip')
        zf.extract('browser/source/Tinkerforge.js', tmp_dir)
        zf.close()

        for lang in ['en', 'de']:
            print('')
            print('Copying Tinkerforge.js to {0}:'.format(os.path.join(doc_git, lang)))

            src_file = os.path.join(tmp_dir, 'browser', 'source', 'Tinkerforge.js')
            dest_dir = os.path.join(start_path, doc_path.format(lang), t[1])

            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)

            if files_are_not_the_same(src_file, dest_dir):
                shutil.copy(src_file, dest_dir)
                print(' * Tinkerforge.js')

        shutil.rmtree(tmp_dir)

    if socket.gethostname() == 'tinkerforge.com':
        print('')
        print('Linking 3D models:')

        for git in os.listdir(os.path.join(path, '..')):
            hardware_dir = os.path.normpath(os.path.join(path, '..', git, 'hardware'))

            if not os.path.exists(hardware_dir):
                continue

            models = []

            for suffix in ['*.step', '*.FCStd']:
                for match in glob.glob(os.path.join(hardware_dir, suffix)):
                    models.append(os.path.relpath(match, hardware_dir))

            for root, dirs, _ in os.walk(hardware_dir):
                for name in dirs:
                    for suffix in ['*.step', '*.FCStd']:
                        for match in glob.glob(os.path.join(root, name, suffix)):
                            models.append(os.path.relpath(match, hardware_dir))

            if len(models) == 0:
                continue

            if git.endswith('-brick'):
                category = 'bricks'
                device = '_'.join(git.split('-')[:-1])
            elif git.endswith('-bricklet'):
                category = 'bricklets'
                device = '_'.join(git.split('-')[:-1])
            elif git.endswith('-extension'):
                category = 'extensions'
                device = '_'.join(git.split('-')[:-1])
            elif git.endswith('-powersupply'):
                category = 'power_supplies'
                device = '_'.join(git.split('-')[:-1])
            else:
                category = 'accessories'
                device = git.replace('-', '_')

            target_dir = os.path.join('/srv/web/com.tinkerforge.download/downloads/3d', category, device)

            if not os.path.exists(target_dir):
                os.makedirs(target_dir)

            for model in models:
                source = os.path.join(hardware_dir, model)
                base, name = os.path.split(model)
                target_base = os.path.join(target_dir, base)

                if not os.path.exists(target_base):
                    os.makedirs(target_base)

                target = os.path.join(target_dir, model)

                if not os.path.exists(target):
                    os.symlink(source, target)
                    print(' * {0}/{1}/{2}'.format(category, device, model))

    print('')
    print("Removing stale files:")

    for lang in ['en', 'de']:
        for t in doc_copy:
            if t[1] == '.':
                continue

            for x in to_delete[lang][t[1]]:
                if x.endswith('_openHAB.rst') or x.endswith('.rules'):
                    continue

                if x.endswith('.table'):
                    continue

                p = os.path.join(doc_git, lang, "source", "Software", t[1], x)
                os.remove(os.path.join(start_path, p))
                print(' * {0}'.format(p))

    print('')
    print('\033[01;35m>>> done\033[0m')

if __name__ == '__main__':
    common.dockerize('', __file__)

    main()
