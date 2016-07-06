#
# GDB Tools python scripts.
#
import sys
import os

def less(command):
    os.popen('less', 'w').write(gdb.execute(command, to_string = True))

# Show contents of Python value
def pyp(expression, path = ''):
    value = gdb.parse_and_eval(expression)
    # Dereference and cast
    value = pye_value(value)
    # Extract path if specified
    if path:
        value = pye_path(value, path)
    # Try to print the value
    pyp_print(value)
    # Print via gdb to store casted reference
    gdb.execute('print (' + str(pye_type(value))+  ') *' + str(value.address))

# Pretty print Python value
def pyp_print(value):
    if str(value.type).endswith('**'):
        print 'Unsupported type: ' + str(value.type)
        return
    kind = pye_kind(value)
    if not hasattr(sys.modules[__name__], 'pyp_' + kind):
        print 'Unsupported type: ' + kind
        return
    getattr(sys.modules[__name__], 'pyp_' + kind)(value)

# Pretty print function value
def pyp_function(value):
    print 'Function: ' + pye_string(value['func_name'])

# Pretty print string value
def pyp_string(value):
    print 'String: ' + pye_string(value)

# Extract value of Python string object
def pye_string(value):
    value = pye_value(value)
    return value['ob_sval'].string('utf-8', '', value['ob_size'])

# Extract Python object type name
def pye_kind(value):
    kind = value['ob_type']['tp_name'].string()
    if kind == 'str': return 'string'
    return kind

# Extract Python object type
def pye_type(value):
    if value.type.code == gdb.TYPE_CODE_PTR:
        value = value.dereference()
    try:
        return gdb.lookup_type('Py' + pye_kind(value).capitalize() + 'Object')
    except:
        return gdb.lookup_type('PyObject')

# Extract casted dereferenced value
def pye_value(value):
    if (str(value.type).endswith('**')):
        return value
    if value.type.code == gdb.TYPE_CODE_PTR:
        value = value.dereference()
    return value.cast(pye_type(value))

# Extract path component from the value
def pye_path(value, path):
    if not path:
        return value
    elif path.startswith('['):
        index = int(path[1:path.find(']')])
        return pye_path(pye_value(value[index]), path[path.find(']') + 1:])
    else:
        name = path.split('.')[0]
        if (name.find('[') > -1):
            name = name[:name.find('[')]
        return pye_path(pye_value(value[name]), path[len(name):].strip('.'))

