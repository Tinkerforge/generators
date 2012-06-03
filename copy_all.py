#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import shutil
import filecmp

def files_are_not_the_same(src_file, dest_path):
    dest_file = os.path.join(dest_path, src_file.split('/')[-1])
    try:
        f1 = file(src_file)
        f2 = file(dest_file)
    except:
        return True

    i = 0
    for l1, l2 in map(None, f1, f2):
        if i > 2:
            if l1 != l2:
                return True
        i += 1
        
    return False

bind_trans = [('brick_imu', 'imu-brick', 'imu', 'IMU_Brick'),
              ('brick_servo', 'servo-brick', 'servo', 'Servo_Brick'),
              ('brick_master', 'master-brick', 'master', 'Master_Brick'),
              ('brick_dc', 'dc-brick', 'dc', 'DC_Brick'),
              ('brick_stepper', 'stepper-brick', 'stepper', 'Stepper_Brick'),
              ('bricklet_rotary_poti', 'rotary-poti-bricklet', 'rotary_poti', 'RotaryPoti_Bricklet'),
              ('bricklet_linear_poti', 'linear-poti-bricklet', 'linear_poti', 'LinearPoti_Bricklet'),
              ('bricklet_joystick', 'joystick-bricklet', 'joystick', 'Joystick_Bricklet'),
              ('bricklet_humidity', 'humidity-bricklet', 'humidity', 'Humidity_Bricklet'),
              ('bricklet_current25', 'current25-bricklet', 'current25', 'Current25_Bricklet'),
              ('bricklet_current12', 'current12-bricklet', 'current12', 'Current12_Bricklet'),
              ('bricklet_distance_ir', 'distance-ir-bricklet', 'distance_ir', 'DistanceIR_Bricklet'),
              ('bricklet_voltage', 'voltage-bricklet', 'voltage', 'Voltage_Bricklet'),
              ('bricklet_dual_relay', 'dual-relay-bricklet', 'dual_relay', 'DualRelay_Bricklet'),
              ('bricklet_temperature', 'temperature-bricklet', 'temperature', 'Temperature_Bricklet'),
              ('bricklet_piezo_buzzer', 'piezo-buzzer-bricklet', 'piezo_buzzer', 'PiezoBuzzer_Bricklet'),
              ('bricklet_lcd_20x4', 'lcd-20x4-bricklet', 'lcd_20x4', 'LCD20x4_Bricklet'),
              ('bricklet_lcd_16x2', 'lcd-16x2-bricklet', 'lcd_16x2', 'LCD16x2_Bricklet'),
              ('bricklet_temperature_ir', 'temperature-ir-bricklet', 'temperature_ir', 'TemperatureIR_Bricklet'),
              ('bricklet_io16', 'io16-bricklet', 'io16', 'IO16_Bricklet'),
              ('bricklet_io4', 'io4-bricklet', 'io4', 'IO4_Bricklet'),
              ('bricklet_ambient_light', 'ambient-light-bricklet', 'ambient_light', 'AmbientLight_Bricklet'),
              ('bricklet_analog_in', 'analog-in-bricklet', 'analog_in', 'AnalogIn_Bricklet'),
              ('bricklet_analog_out', 'analog-out-bricklet', 'analog_out', 'AnalogOut_Bricklet')]

path = os.getcwd()
start_path = path.replace('/generators', '')
brickv_path_bindings = '{0}/{1}'.format(start_path, 'brickv/src/brickv/bindings')

bindings = []
for d in os.listdir(path):
    if os.path.isdir(d):
        if not d in ('configs', '.git'):
            bindings.append(d)

print('')
print('Copying ip_connection to brickv:')
src_file = '{0}/{1}'.format(path, 'python/ip_connection.py')
if files_are_not_the_same(src_file, brickv_path_bindings):
    shutil.copy(src_file, brickv_path_bindings)
    print(' * ip_connection.py')

print('')
print('Copying Python bindings to brickv:')
path_binding = '{0}/{1}'.format(path, 'python')
src_file_path = '{0}/{1}'.format(path_binding, 'bindings')
for f in os.listdir(src_file_path):
    if f.endswith('.py'):
        src_file = '{0}/{1}'.format(src_file_path, f)
        dest_path = brickv_path_bindings

        if files_are_not_the_same(src_file, dest_path):
            shutil.copy(src_file, dest_path)
            print(' * {0}'.format(f))

print('')
print('Copying documentation and examples:')
doc_copy = [('_Brick_', 'Bricks'), 
            ('_Bricklet_', 'Bricklets')]
doc_path = 'doc/source/Software'

for t in doc_copy:
    dest_dir = '{0}/{1}/{2}'.format(start_path, doc_path, t[1])
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

for binding in bindings:
    path_binding = '{0}/{1}'.format(path, binding)
    src_file_path = '{0}/{1}'.format(path_binding, 'doc')
    for f in os.listdir(src_file_path):
        if not f.endswith('.swp'):
            for t in doc_copy:
                if t[0] in f:
                    src_file = '{0}/{1}'.format(src_file_path, f)
                    dest_path = '{0}/{1}/{2}'.format(start_path,
                                                     doc_path,
                                                     t[1])
                    if files_are_not_the_same(src_file, dest_path):
                        shutil.copy(src_file, dest_path)
                        print(' * {0}'.format(f))

