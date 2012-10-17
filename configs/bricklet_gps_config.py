# -*- coding: utf-8 -*-

# GPS Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'version': [1, 0, 0],
    'category': 'Bricklet',
    'name': ('GPS', 'gps', 'GPS'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for receiving GPS position',
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('GetCoordinates', 'get_coordinates'),
'elements': [('latitude', 'uint32', 1, 'out'),
             ('ns', 'char', 1, 'out'),
             ('longitude', 'uint32', 1, 'out'),
             ('ew', 'char', 1, 'out'),
             ('pdop', 'uint16', 1, 'out'),
             ('hdop', 'uint16', 1, 'out'),
             ('vdop', 'uint16', 1, 'out'),
             ('epe', 'uint16', 1, 'out')],
'doc': ['bf', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetStatus', 'get_status'),
'elements': [('fix', 'uint8', 1, 'out'),
             ('satellites_view', 'uint8', 1, 'out'),
             ('satellites_used', 'uint8', 1, 'out')],
'doc': ['bf', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetAltitude', 'get_altitude'),
'elements': [('altitude', 'uint32', 1, 'out'),
             ('geoidal_separation', 'uint32', 1, 'out')],
'doc': ['bf', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetMotion', 'get_motion'),
'elements': [('course', 'uint32', 1, 'out'),
             ('speed', 'uint32', 1, 'out')],
'doc': ['bf', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetDateTime', 'get_date_time'),
'elements': [('date', 'uint32', 1, 'out'),
             ('time', 'uint32', 1, 'out')],
'doc': ['bf', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('Restart', 'restart'),
'elements': [('restart_type', 'uint8', 1, 'in')],
'doc': ['af', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetCoordinatesCallbackPeriod', 'set_coordinates_callback_period'),
'elements': [('period', 'uint32', 1, 'in')],
'doc': ['ccf', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetCoordinatesCallbackPeriod', 'get_coordinates_callback_period'),
'elements': [('period', 'uint32', 1, 'out')],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetCoordinatesCallbackPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetCoordinatesCallbackPeriod`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetStatusCallbackPeriod', 'set_status_callback_period'),
'elements': [('period', 'uint32', 1, 'in')],
'doc': ['ccf', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetStatusCallbackPeriod', 'get_status_callback_period'),
'elements': [('period', 'uint32', 1, 'out')],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetStatusCallbackPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetStatusCallbackPeriod`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetAltitudeCallbackPeriod', 'set_altitude_callback_period'),
'elements': [('period', 'uint32', 1, 'in')],
'doc': ['ccf', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetAltitudeCallbackPeriod', 'get_altitude_callback_period'),
'elements': [('period', 'uint32', 1, 'out')],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetAltitudeCallbackPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetAltitudeCallbackPeriod`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetDateTimeCallbackPeriod', 'set_date_time_callback_period'),
'elements': [('period', 'uint32', 1, 'in')],
'doc': ['ccf', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetDateTimeCallbackPeriod', 'get_date_time_callback_period'),
'elements': [('period', 'uint32', 1, 'out')],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetDateTimeCallbackPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetDateTimeCallbackPeriod`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetMotionCallbackPeriod', 'set_motion_callback_period'),
'elements': [('period', 'uint32', 1, 'in')],
'doc': ['ccf', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetMotionCallbackPeriod', 'get_motion_callback_period'),
'elements': [('period', 'uint32', 1, 'out')],
'doc': ['ccf', {
'en':
"""
Returns the period as set by :func:`SetMotionCallbackPeriod`.
""",
'de':
"""
Gibt die Periode zurück, wie von :func:`SetMotionCallbackPeriod`
gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('Coordinates', 'coordinates'),
'elements': [('latitude', 'uint32', 1, 'out'),
             ('ns', 'char', 1, 'out'),
             ('longitude', 'uint32', 1, 'out'),
             ('ew', 'char', 1, 'out'),
             ('pdop', 'uint16', 1, 'out'),
             ('hdop', 'uint16', 1, 'out'),
             ('vdop', 'uint16', 1, 'out'),
             ('epe', 'uint16', 1, 'out')],
'doc': ['c', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('Status', 'status'),
'elements': [('fix', 'uint8', 1, 'out'),
             ('satellites_view', 'uint8', 1, 'out'),
             ('satellites_used', 'uint8', 1, 'out')],
'doc': ['c', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('Altitude', 'altitude'),
'elements': [('altitude', 'uint32', 1, 'out'),
             ('geoidal_separation', 'uint32', 1, 'out')],
'doc': ['c', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('Motion', 'motion'),
'elements': [('course', 'uint32', 1, 'out'),
             ('speed', 'uint32', 1, 'out')],
'doc': ['c', {
'en':
"""
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('DateTime', 'date_time'),
'elements': [('date', 'uint32', 1, 'out'),
             ('time', 'uint32', 1, 'out')],
'doc': ['c', {
'en':
"""
""",
'de':
"""
"""
}]
})
