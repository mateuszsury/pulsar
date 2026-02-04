/**
 * Enhanced MicroPython completions for Monaco Editor.
 *
 * Provides completions for:
 * - Python built-in functions (print, len, range, etc.)
 * - Python keywords (if, for, def, class, etc.)
 * - Built-in type methods (str., list., dict., etc.)
 * - MicroPython modules (machine, network, etc.)
 * - ESP32-specific modules
 * - User-defined symbols (functions, classes, variables)
 * - Code snippets
 */

// =============================================================================
// PYTHON BUILT-IN FUNCTIONS
// =============================================================================

const PYTHON_BUILTINS = [
  // I/O Functions
  { name: 'print', signature: 'print(*objects, sep=" ", end="\\n")', description: 'Print objects to the text stream' },
  { name: 'input', signature: 'input(prompt="")', description: 'Read a line from input' },
  { name: 'open', signature: 'open(file, mode="r")', description: 'Open a file and return a file object' },

  // Type Constructors
  { name: 'int', signature: 'int(x=0, base=10)', description: 'Convert to integer' },
  { name: 'float', signature: 'float(x=0)', description: 'Convert to floating point number' },
  { name: 'str', signature: 'str(object="")', description: 'Convert to string' },
  { name: 'bool', signature: 'bool(x=False)', description: 'Convert to boolean' },
  { name: 'bytes', signature: 'bytes(source, encoding)', description: 'Create bytes object' },
  { name: 'bytearray', signature: 'bytearray(source)', description: 'Create mutable bytes array' },
  { name: 'list', signature: 'list(iterable)', description: 'Create a list' },
  { name: 'tuple', signature: 'tuple(iterable)', description: 'Create a tuple' },
  { name: 'dict', signature: 'dict(**kwargs)', description: 'Create a dictionary' },
  { name: 'set', signature: 'set(iterable)', description: 'Create a set' },
  { name: 'frozenset', signature: 'frozenset(iterable)', description: 'Create an immutable set' },

  // Sequence Functions
  { name: 'len', signature: 'len(s)', description: 'Return the length of an object' },
  { name: 'range', signature: 'range(stop) / range(start, stop, step)', description: 'Generate sequence of numbers' },
  { name: 'enumerate', signature: 'enumerate(iterable, start=0)', description: 'Return enumerate object' },
  { name: 'zip', signature: 'zip(*iterables)', description: 'Iterate over multiple iterables' },
  { name: 'map', signature: 'map(function, iterable)', description: 'Apply function to every item' },
  { name: 'filter', signature: 'filter(function, iterable)', description: 'Filter elements by function' },
  { name: 'sorted', signature: 'sorted(iterable, key=None, reverse=False)', description: 'Return sorted list' },
  { name: 'reversed', signature: 'reversed(seq)', description: 'Return a reverse iterator' },
  { name: 'min', signature: 'min(iterable) / min(a, b, ...)', description: 'Return the smallest item' },
  { name: 'max', signature: 'max(iterable) / max(a, b, ...)', description: 'Return the largest item' },
  { name: 'sum', signature: 'sum(iterable, start=0)', description: 'Sum of all items' },
  { name: 'any', signature: 'any(iterable)', description: 'True if any element is true' },
  { name: 'all', signature: 'all(iterable)', description: 'True if all elements are true' },
  { name: 'slice', signature: 'slice(stop) / slice(start, stop, step)', description: 'Create a slice object' },
  { name: 'iter', signature: 'iter(object)', description: 'Return an iterator' },
  { name: 'next', signature: 'next(iterator, default)', description: 'Get next item from iterator' },

  // Math Functions
  { name: 'abs', signature: 'abs(x)', description: 'Return absolute value' },
  { name: 'round', signature: 'round(number, ndigits=None)', description: 'Round a number' },
  { name: 'pow', signature: 'pow(base, exp, mod=None)', description: 'Return base to the power exp' },
  { name: 'divmod', signature: 'divmod(a, b)', description: 'Return quotient and remainder' },

  // Object/Type Functions
  { name: 'type', signature: 'type(object)', description: 'Return the type of an object' },
  { name: 'isinstance', signature: 'isinstance(object, classinfo)', description: 'Check if object is instance' },
  { name: 'issubclass', signature: 'issubclass(class, classinfo)', description: 'Check if class is subclass' },
  { name: 'callable', signature: 'callable(object)', description: 'Check if object is callable' },
  { name: 'id', signature: 'id(object)', description: 'Return the identity of an object' },
  { name: 'hash', signature: 'hash(object)', description: 'Return hash value of object' },

  // Attribute Functions
  { name: 'getattr', signature: 'getattr(object, name, default)', description: 'Get attribute of object' },
  { name: 'setattr', signature: 'setattr(object, name, value)', description: 'Set attribute of object' },
  { name: 'hasattr', signature: 'hasattr(object, name)', description: 'Check if object has attribute' },
  { name: 'delattr', signature: 'delattr(object, name)', description: 'Delete attribute of object' },
  { name: 'dir', signature: 'dir(object)', description: 'List of object attributes' },
  { name: 'vars', signature: 'vars(object)', description: 'Return __dict__ of object' },

  // String Functions
  { name: 'chr', signature: 'chr(i)', description: 'Return Unicode character from code' },
  { name: 'ord', signature: 'ord(c)', description: 'Return Unicode code from character' },
  { name: 'repr', signature: 'repr(object)', description: 'Return printable representation' },
  { name: 'ascii', signature: 'ascii(object)', description: 'Return ASCII-only representation' },
  { name: 'format', signature: 'format(value, format_spec)', description: 'Format a value' },

  // Binary Functions
  { name: 'bin', signature: 'bin(x)', description: 'Convert to binary string' },
  { name: 'oct', signature: 'oct(x)', description: 'Convert to octal string' },
  { name: 'hex', signature: 'hex(x)', description: 'Convert to hexadecimal string' },

  // Object Creation
  { name: 'object', signature: 'object()', description: 'Return a new featureless object' },
  { name: 'property', signature: 'property(fget, fset, fdel, doc)', description: 'Return a property attribute' },
  { name: 'classmethod', signature: '@classmethod', description: 'Convert method to class method' },
  { name: 'staticmethod', signature: '@staticmethod', description: 'Convert method to static method' },
  { name: 'super', signature: 'super(type, object)', description: 'Return proxy object for parent class' },

  // Execution
  { name: 'eval', signature: 'eval(expression)', description: 'Evaluate Python expression' },
  { name: 'exec', signature: 'exec(code)', description: 'Execute Python code' },
  { name: 'compile', signature: 'compile(source, filename, mode)', description: 'Compile source to code object' },
  { name: 'globals', signature: 'globals()', description: 'Return global symbol table' },
  { name: 'locals', signature: 'locals()', description: 'Return local symbol table' },

  // Memory
  { name: 'memoryview', signature: 'memoryview(obj)', description: 'Create memory view of object' },
]

// =============================================================================
// PYTHON KEYWORDS
// =============================================================================

const PYTHON_KEYWORDS = [
  { name: 'if', description: 'Conditional statement' },
  { name: 'elif', description: 'Else if branch' },
  { name: 'else', description: 'Else branch' },
  { name: 'for', description: 'For loop' },
  { name: 'while', description: 'While loop' },
  { name: 'break', description: 'Exit loop' },
  { name: 'continue', description: 'Continue to next iteration' },
  { name: 'pass', description: 'Null statement placeholder' },
  { name: 'def', description: 'Define function' },
  { name: 'return', description: 'Return from function' },
  { name: 'yield', description: 'Yield from generator' },
  { name: 'class', description: 'Define class' },
  { name: 'try', description: 'Try block for exception handling' },
  { name: 'except', description: 'Handle exception' },
  { name: 'finally', description: 'Always execute block' },
  { name: 'raise', description: 'Raise an exception' },
  { name: 'with', description: 'Context manager' },
  { name: 'as', description: 'Alias in import/with' },
  { name: 'import', description: 'Import module' },
  { name: 'from', description: 'Import from module' },
  { name: 'global', description: 'Declare global variable' },
  { name: 'nonlocal', description: 'Declare nonlocal variable' },
  { name: 'lambda', description: 'Anonymous function' },
  { name: 'and', description: 'Logical AND' },
  { name: 'or', description: 'Logical OR' },
  { name: 'not', description: 'Logical NOT' },
  { name: 'in', description: 'Membership test' },
  { name: 'is', description: 'Identity test' },
  { name: 'True', description: 'Boolean true' },
  { name: 'False', description: 'Boolean false' },
  { name: 'None', description: 'Null value' },
  { name: 'async', description: 'Define async function/context' },
  { name: 'await', description: 'Await coroutine' },
  { name: 'assert', description: 'Assert condition' },
  { name: 'del', description: 'Delete object' },
]

// =============================================================================
// BUILT-IN TYPE METHODS
// =============================================================================

const STRING_METHODS = [
  { name: 'upper', signature: 'upper()', description: 'Return uppercase copy' },
  { name: 'lower', signature: 'lower()', description: 'Return lowercase copy' },
  { name: 'capitalize', signature: 'capitalize()', description: 'Capitalize first character' },
  { name: 'title', signature: 'title()', description: 'Titlecase words' },
  { name: 'strip', signature: 'strip(chars=None)', description: 'Remove leading/trailing whitespace' },
  { name: 'lstrip', signature: 'lstrip(chars=None)', description: 'Remove leading whitespace' },
  { name: 'rstrip', signature: 'rstrip(chars=None)', description: 'Remove trailing whitespace' },
  { name: 'split', signature: 'split(sep=None, maxsplit=-1)', description: 'Split string into list' },
  { name: 'rsplit', signature: 'rsplit(sep=None, maxsplit=-1)', description: 'Split from right' },
  { name: 'splitlines', signature: 'splitlines(keepends=False)', description: 'Split at line boundaries' },
  { name: 'join', signature: 'join(iterable)', description: 'Join iterable with string' },
  { name: 'replace', signature: 'replace(old, new, count=-1)', description: 'Replace occurrences' },
  { name: 'find', signature: 'find(sub, start=0, end=-1)', description: 'Find substring index' },
  { name: 'rfind', signature: 'rfind(sub, start=0, end=-1)', description: 'Find from right' },
  { name: 'index', signature: 'index(sub, start=0, end=-1)', description: 'Find or raise ValueError' },
  { name: 'rindex', signature: 'rindex(sub, start=0, end=-1)', description: 'Find from right or raise' },
  { name: 'count', signature: 'count(sub, start=0, end=-1)', description: 'Count occurrences' },
  { name: 'startswith', signature: 'startswith(prefix, start=0, end=-1)', description: 'Check if starts with' },
  { name: 'endswith', signature: 'endswith(suffix, start=0, end=-1)', description: 'Check if ends with' },
  { name: 'isalpha', signature: 'isalpha()', description: 'Check if all alphabetic' },
  { name: 'isdigit', signature: 'isdigit()', description: 'Check if all digits' },
  { name: 'isalnum', signature: 'isalnum()', description: 'Check if alphanumeric' },
  { name: 'isspace', signature: 'isspace()', description: 'Check if all whitespace' },
  { name: 'isupper', signature: 'isupper()', description: 'Check if all uppercase' },
  { name: 'islower', signature: 'islower()', description: 'Check if all lowercase' },
  { name: 'encode', signature: 'encode(encoding="utf-8")', description: 'Encode to bytes' },
  { name: 'format', signature: 'format(*args, **kwargs)', description: 'Format string' },
  { name: 'center', signature: 'center(width, fillchar=" ")', description: 'Center in field' },
  { name: 'ljust', signature: 'ljust(width, fillchar=" ")', description: 'Left justify' },
  { name: 'rjust', signature: 'rjust(width, fillchar=" ")', description: 'Right justify' },
  { name: 'zfill', signature: 'zfill(width)', description: 'Pad with zeros' },
  { name: 'partition', signature: 'partition(sep)', description: 'Split into 3 parts' },
  { name: 'rpartition', signature: 'rpartition(sep)', description: 'Split from right into 3' },
]

const LIST_METHODS = [
  { name: 'append', signature: 'append(x)', description: 'Add item to end' },
  { name: 'extend', signature: 'extend(iterable)', description: 'Extend list by iterable' },
  { name: 'insert', signature: 'insert(i, x)', description: 'Insert item at index' },
  { name: 'remove', signature: 'remove(x)', description: 'Remove first occurrence' },
  { name: 'pop', signature: 'pop(i=-1)', description: 'Remove and return item' },
  { name: 'clear', signature: 'clear()', description: 'Remove all items' },
  { name: 'index', signature: 'index(x, start=0, end=-1)', description: 'Return index of item' },
  { name: 'count', signature: 'count(x)', description: 'Count occurrences' },
  { name: 'sort', signature: 'sort(key=None, reverse=False)', description: 'Sort in place' },
  { name: 'reverse', signature: 'reverse()', description: 'Reverse in place' },
  { name: 'copy', signature: 'copy()', description: 'Return shallow copy' },
]

const DICT_METHODS = [
  { name: 'keys', signature: 'keys()', description: 'Return view of keys' },
  { name: 'values', signature: 'values()', description: 'Return view of values' },
  { name: 'items', signature: 'items()', description: 'Return view of key-value pairs' },
  { name: 'get', signature: 'get(key, default=None)', description: 'Get value or default' },
  { name: 'pop', signature: 'pop(key, default)', description: 'Remove and return value' },
  { name: 'popitem', signature: 'popitem()', description: 'Remove and return last item' },
  { name: 'setdefault', signature: 'setdefault(key, default=None)', description: 'Get or set default' },
  { name: 'update', signature: 'update(other)', description: 'Update from dict/iterable' },
  { name: 'clear', signature: 'clear()', description: 'Remove all items' },
  { name: 'copy', signature: 'copy()', description: 'Return shallow copy' },
  { name: 'fromkeys', signature: 'fromkeys(seq, value=None)', description: 'Create dict from keys' },
]

const SET_METHODS = [
  { name: 'add', signature: 'add(elem)', description: 'Add element' },
  { name: 'remove', signature: 'remove(elem)', description: 'Remove element or raise' },
  { name: 'discard', signature: 'discard(elem)', description: 'Remove element if present' },
  { name: 'pop', signature: 'pop()', description: 'Remove and return arbitrary element' },
  { name: 'clear', signature: 'clear()', description: 'Remove all elements' },
  { name: 'copy', signature: 'copy()', description: 'Return shallow copy' },
  { name: 'union', signature: 'union(*others)', description: 'Return union' },
  { name: 'intersection', signature: 'intersection(*others)', description: 'Return intersection' },
  { name: 'difference', signature: 'difference(*others)', description: 'Return difference' },
  { name: 'symmetric_difference', signature: 'symmetric_difference(other)', description: 'Return symmetric difference' },
  { name: 'update', signature: 'update(*others)', description: 'Update with union' },
  { name: 'intersection_update', signature: 'intersection_update(*others)', description: 'Update with intersection' },
  { name: 'difference_update', signature: 'difference_update(*others)', description: 'Update with difference' },
  { name: 'issubset', signature: 'issubset(other)', description: 'Test if subset' },
  { name: 'issuperset', signature: 'issuperset(other)', description: 'Test if superset' },
  { name: 'isdisjoint', signature: 'isdisjoint(other)', description: 'Test if disjoint' },
]

const BYTES_METHODS = [
  { name: 'decode', signature: 'decode(encoding="utf-8")', description: 'Decode to string' },
  { name: 'find', signature: 'find(sub)', description: 'Find subsequence' },
  { name: 'rfind', signature: 'rfind(sub)', description: 'Find from right' },
  { name: 'count', signature: 'count(sub)', description: 'Count occurrences' },
  { name: 'startswith', signature: 'startswith(prefix)', description: 'Check if starts with' },
  { name: 'endswith', signature: 'endswith(suffix)', description: 'Check if ends with' },
  { name: 'split', signature: 'split(sep)', description: 'Split by separator' },
  { name: 'join', signature: 'join(iterable)', description: 'Join with bytes' },
  { name: 'replace', signature: 'replace(old, new)', description: 'Replace bytes' },
  { name: 'strip', signature: 'strip()', description: 'Remove whitespace' },
  { name: 'hex', signature: 'hex()', description: 'Convert to hex string' },
]

const FILE_METHODS = [
  { name: 'read', signature: 'read(size=-1)', description: 'Read up to size bytes' },
  { name: 'readline', signature: 'readline(size=-1)', description: 'Read one line' },
  { name: 'readlines', signature: 'readlines(hint=-1)', description: 'Read all lines' },
  { name: 'write', signature: 'write(s)', description: 'Write string/bytes' },
  { name: 'writelines', signature: 'writelines(lines)', description: 'Write list of lines' },
  { name: 'close', signature: 'close()', description: 'Close the file' },
  { name: 'flush', signature: 'flush()', description: 'Flush write buffers' },
  { name: 'seek', signature: 'seek(offset, whence=0)', description: 'Change stream position' },
  { name: 'tell', signature: 'tell()', description: 'Return current position' },
]

// =============================================================================
// MICROPYTHON MODULES
// =============================================================================

const MICROPYTHON_MODULES = [
  { name: 'machine', description: 'Hardware control (Pin, I2C, SPI, etc.)' },
  { name: 'network', description: 'WiFi and network interface' },
  { name: 'time', description: 'Time-related functions' },
  { name: 'os', description: 'Operating system interface' },
  { name: 'gc', description: 'Garbage collection' },
  { name: 'sys', description: 'System-specific parameters' },
  { name: 'json', description: 'JSON encoder/decoder' },
  { name: 'struct', description: 'Pack/unpack binary data' },
  { name: 'socket', description: 'Socket interface' },
  { name: 'select', description: 'I/O multiplexing' },
  { name: 'asyncio', description: 'Asynchronous I/O' },
  { name: 'uasyncio', description: 'MicroPython asyncio' },
  { name: 'uctypes', description: 'C-compatible data types' },
  { name: 'hashlib', description: 'Hashing algorithms' },
  { name: 'binascii', description: 'Binary/ASCII conversions' },
  { name: 'random', description: 'Random number generator' },
  { name: 'errno', description: 'Error numbers' },
  { name: 'io', description: 'I/O streams' },
  { name: 're', description: 'Regular expressions' },
  { name: 'collections', description: 'Container datatypes' },
  { name: 'array', description: 'Efficient arrays' },
  { name: 'micropython', description: 'MicroPython internals' },
  { name: 'math', description: 'Mathematical functions' },
  { name: 'cmath', description: 'Complex number math' },
  { name: 'ubinascii', description: 'Binary/ASCII conversions' },
  { name: 'uhashlib', description: 'Hashing algorithms' },
  { name: 'uio', description: 'I/O streams' },
  { name: 'ujson', description: 'JSON encoder/decoder' },
  { name: 'uos', description: 'Operating system interface' },
  { name: 'urandom', description: 'Random number generator' },
  { name: 'ure', description: 'Regular expressions' },
  { name: 'uselect', description: 'I/O multiplexing' },
  { name: 'usocket', description: 'Socket interface' },
  { name: 'ustruct', description: 'Pack/unpack binary data' },
  { name: 'utime', description: 'Time-related functions' },
]

const ESP32_MODULES = [
  { name: 'esp', description: 'ESP8266/ESP32 module' },
  { name: 'esp32', description: 'ESP32-specific functions' },
  { name: 'espnow', description: 'ESP-NOW protocol' },
  { name: 'bluetooth', description: 'Bluetooth/BLE' },
  { name: 'ntptime', description: 'NTP time sync' },
  { name: 'webrepl', description: 'WebREPL setup' },
  { name: 'neopixel', description: 'NeoPixel/WS2812 LEDs' },
  { name: 'onewire', description: 'OneWire protocol' },
  { name: 'dht', description: 'DHT temperature sensor' },
  { name: 'ds18x20', description: 'DS18x20 temperature sensor' },
  { name: 'framebuf', description: 'Frame buffer manipulation' },
]

// =============================================================================
// MODULE MEMBERS
// =============================================================================

const MACHINE_MEMBERS = [
  { name: 'Pin', kind: 'Class', description: 'GPIO pin control' },
  { name: 'I2C', kind: 'Class', description: 'I2C bus interface' },
  { name: 'SoftI2C', kind: 'Class', description: 'Software I2C' },
  { name: 'SPI', kind: 'Class', description: 'SPI bus interface' },
  { name: 'SoftSPI', kind: 'Class', description: 'Software SPI' },
  { name: 'UART', kind: 'Class', description: 'UART interface' },
  { name: 'PWM', kind: 'Class', description: 'PWM output' },
  { name: 'ADC', kind: 'Class', description: 'Analog-to-digital converter' },
  { name: 'DAC', kind: 'Class', description: 'Digital-to-analog converter' },
  { name: 'Timer', kind: 'Class', description: 'Hardware timer' },
  { name: 'RTC', kind: 'Class', description: 'Real-time clock' },
  { name: 'WDT', kind: 'Class', description: 'Watchdog timer' },
  { name: 'TouchPad', kind: 'Class', description: 'Touch sensor' },
  { name: 'Signal', kind: 'Class', description: 'Signal (inverted pin)' },
  { name: 'SDCard', kind: 'Class', description: 'SD card interface' },
  { name: 'reset', kind: 'Function', description: 'Reset the device' },
  { name: 'soft_reset', kind: 'Function', description: 'Soft reset the device' },
  { name: 'reset_cause', kind: 'Function', description: 'Get reset cause' },
  { name: 'freq', kind: 'Function', description: 'Get/set CPU frequency' },
  { name: 'unique_id', kind: 'Function', description: 'Get unique chip ID' },
  { name: 'idle', kind: 'Function', description: 'Enter idle mode' },
  { name: 'sleep', kind: 'Function', description: 'Enter sleep mode' },
  { name: 'deepsleep', kind: 'Function', description: 'Enter deep sleep' },
  { name: 'lightsleep', kind: 'Function', description: 'Enter light sleep' },
  { name: 'wake_reason', kind: 'Function', description: 'Get wake reason' },
  { name: 'time_pulse_us', kind: 'Function', description: 'Time a pulse' },
  { name: 'bitstream', kind: 'Function', description: 'Transmit bits' },
  { name: 'disable_irq', kind: 'Function', description: 'Disable interrupts' },
  { name: 'enable_irq', kind: 'Function', description: 'Enable interrupts' },
  { name: 'mem8', kind: 'Variable', description: 'Direct memory access (8-bit)' },
  { name: 'mem16', kind: 'Variable', description: 'Direct memory access (16-bit)' },
  { name: 'mem32', kind: 'Variable', description: 'Direct memory access (32-bit)' },
  { name: 'PWRON_RESET', kind: 'Constant', description: 'Power-on reset cause' },
  { name: 'HARD_RESET', kind: 'Constant', description: 'Hard reset cause' },
  { name: 'SOFT_RESET', kind: 'Constant', description: 'Soft reset cause' },
  { name: 'WDT_RESET', kind: 'Constant', description: 'Watchdog reset cause' },
  { name: 'DEEPSLEEP_RESET', kind: 'Constant', description: 'Deep sleep wake cause' },
]

const NETWORK_MEMBERS = [
  { name: 'WLAN', kind: 'Class', description: 'WiFi interface' },
  { name: 'LAN', kind: 'Class', description: 'Ethernet interface' },
  { name: 'PPP', kind: 'Class', description: 'PPP interface' },
  { name: 'STA_IF', kind: 'Constant', description: 'Station (client) interface' },
  { name: 'AP_IF', kind: 'Constant', description: 'Access point interface' },
  { name: 'hostname', kind: 'Function', description: 'Get/set hostname' },
  { name: 'country', kind: 'Function', description: 'Set country code' },
  { name: 'phy_mode', kind: 'Function', description: 'Get/set PHY mode' },
]

const TIME_MEMBERS = [
  { name: 'sleep', kind: 'Function', description: 'Sleep for seconds' },
  { name: 'sleep_ms', kind: 'Function', description: 'Sleep for milliseconds' },
  { name: 'sleep_us', kind: 'Function', description: 'Sleep for microseconds' },
  { name: 'ticks_ms', kind: 'Function', description: 'Millisecond counter' },
  { name: 'ticks_us', kind: 'Function', description: 'Microsecond counter' },
  { name: 'ticks_cpu', kind: 'Function', description: 'CPU ticks counter' },
  { name: 'ticks_diff', kind: 'Function', description: 'Compute tick difference' },
  { name: 'ticks_add', kind: 'Function', description: 'Add to tick value' },
  { name: 'time', kind: 'Function', description: 'Seconds since epoch' },
  { name: 'localtime', kind: 'Function', description: 'Convert to local time tuple' },
  { name: 'mktime', kind: 'Function', description: 'Convert time tuple to seconds' },
  { name: 'gmtime', kind: 'Function', description: 'Convert to UTC time tuple' },
]

const OS_MEMBERS = [
  { name: 'listdir', kind: 'Function', description: 'List directory contents' },
  { name: 'mkdir', kind: 'Function', description: 'Create directory' },
  { name: 'rmdir', kind: 'Function', description: 'Remove directory' },
  { name: 'remove', kind: 'Function', description: 'Remove file' },
  { name: 'rename', kind: 'Function', description: 'Rename file/directory' },
  { name: 'stat', kind: 'Function', description: 'Get file/directory status' },
  { name: 'statvfs', kind: 'Function', description: 'Get filesystem status' },
  { name: 'chdir', kind: 'Function', description: 'Change directory' },
  { name: 'getcwd', kind: 'Function', description: 'Get current directory' },
  { name: 'ilistdir', kind: 'Function', description: 'Iterator over directory' },
  { name: 'mount', kind: 'Function', description: 'Mount filesystem' },
  { name: 'umount', kind: 'Function', description: 'Unmount filesystem' },
  { name: 'uname', kind: 'Function', description: 'System information' },
  { name: 'urandom', kind: 'Function', description: 'Random bytes' },
  { name: 'dupterm', kind: 'Function', description: 'Duplicate terminal' },
]

const GC_MEMBERS = [
  { name: 'collect', kind: 'Function', description: 'Run garbage collection' },
  { name: 'enable', kind: 'Function', description: 'Enable automatic GC' },
  { name: 'disable', kind: 'Function', description: 'Disable automatic GC' },
  { name: 'isenabled', kind: 'Function', description: 'Check if GC enabled' },
  { name: 'mem_free', kind: 'Function', description: 'Get free memory' },
  { name: 'mem_alloc', kind: 'Function', description: 'Get allocated memory' },
  { name: 'threshold', kind: 'Function', description: 'Get/set GC threshold' },
]

const SYS_MEMBERS = [
  { name: 'exit', kind: 'Function', description: 'Exit the interpreter' },
  { name: 'print_exception', kind: 'Function', description: 'Print exception traceback' },
  { name: 'path', kind: 'Variable', description: 'Module search path' },
  { name: 'modules', kind: 'Variable', description: 'Loaded modules dict' },
  { name: 'argv', kind: 'Variable', description: 'Command line arguments' },
  { name: 'version', kind: 'Variable', description: 'Python version string' },
  { name: 'version_info', kind: 'Variable', description: 'Version info tuple' },
  { name: 'implementation', kind: 'Variable', description: 'Implementation info' },
  { name: 'platform', kind: 'Variable', description: 'Platform identifier' },
  { name: 'byteorder', kind: 'Variable', description: 'Byte order' },
  { name: 'maxsize', kind: 'Variable', description: 'Maximum integer' },
  { name: 'stdin', kind: 'Variable', description: 'Standard input' },
  { name: 'stdout', kind: 'Variable', description: 'Standard output' },
  { name: 'stderr', kind: 'Variable', description: 'Standard error' },
]

const JSON_MEMBERS = [
  { name: 'dumps', kind: 'Function', description: 'Serialize object to JSON string' },
  { name: 'loads', kind: 'Function', description: 'Parse JSON string to object' },
  { name: 'dump', kind: 'Function', description: 'Serialize object to file' },
  { name: 'load', kind: 'Function', description: 'Parse JSON from file' },
]

const SOCKET_MEMBERS = [
  { name: 'socket', kind: 'Class', description: 'Create socket' },
  { name: 'getaddrinfo', kind: 'Function', description: 'Get address info' },
  { name: 'AF_INET', kind: 'Constant', description: 'IPv4 address family' },
  { name: 'AF_INET6', kind: 'Constant', description: 'IPv6 address family' },
  { name: 'SOCK_STREAM', kind: 'Constant', description: 'TCP socket type' },
  { name: 'SOCK_DGRAM', kind: 'Constant', description: 'UDP socket type' },
  { name: 'SOCK_RAW', kind: 'Constant', description: 'Raw socket type' },
  { name: 'IPPROTO_TCP', kind: 'Constant', description: 'TCP protocol' },
  { name: 'IPPROTO_UDP', kind: 'Constant', description: 'UDP protocol' },
  { name: 'SOL_SOCKET', kind: 'Constant', description: 'Socket level' },
  { name: 'SO_REUSEADDR', kind: 'Constant', description: 'Reuse address option' },
]

const ASYNCIO_MEMBERS = [
  { name: 'run', kind: 'Function', description: 'Run async main function' },
  { name: 'create_task', kind: 'Function', description: 'Create a task' },
  { name: 'sleep', kind: 'Function', description: 'Async sleep (seconds)' },
  { name: 'sleep_ms', kind: 'Function', description: 'Async sleep (milliseconds)' },
  { name: 'gather', kind: 'Function', description: 'Run awaitables concurrently' },
  { name: 'wait_for', kind: 'Function', description: 'Wait with timeout' },
  { name: 'Event', kind: 'Class', description: 'Async event' },
  { name: 'Lock', kind: 'Class', description: 'Async lock' },
  { name: 'StreamReader', kind: 'Class', description: 'Stream reader' },
  { name: 'StreamWriter', kind: 'Class', description: 'Stream writer' },
  { name: 'open_connection', kind: 'Function', description: 'Open TCP connection' },
  { name: 'start_server', kind: 'Function', description: 'Start TCP server' },
  { name: 'current_task', kind: 'Function', description: 'Get current task' },
  { name: 'CancelledError', kind: 'Class', description: 'Task cancelled exception' },
  { name: 'TimeoutError', kind: 'Class', description: 'Timeout exception' },
]

const ESP32_MEMBERS = [
  { name: 'hall_sensor', kind: 'Function', description: 'Read hall sensor' },
  { name: 'raw_temperature', kind: 'Function', description: 'Read internal temperature' },
  { name: 'ULP', kind: 'Class', description: 'Ultra-low-power coprocessor' },
  { name: 'NVS', kind: 'Class', description: 'Non-volatile storage' },
  { name: 'Partition', kind: 'Class', description: 'Flash partition' },
  { name: 'RMT', kind: 'Class', description: 'Remote control transceiver' },
  { name: 'wake_on_ext0', kind: 'Function', description: 'Wake on external pin 0' },
  { name: 'wake_on_ext1', kind: 'Function', description: 'Wake on external pin 1' },
  { name: 'wake_on_touch', kind: 'Function', description: 'Wake on touch' },
  { name: 'gpio_deep_sleep_hold', kind: 'Function', description: 'Hold GPIO during sleep' },
  { name: 'WAKEUP_ALL_LOW', kind: 'Constant', description: 'Wake when all low' },
  { name: 'WAKEUP_ANY_HIGH', kind: 'Constant', description: 'Wake when any high' },
]

const BLUETOOTH_MEMBERS = [
  { name: 'BLE', kind: 'Class', description: 'Bluetooth Low Energy' },
  { name: 'UUID', kind: 'Class', description: 'UUID for BLE' },
  { name: 'FLAG_READ', kind: 'Constant', description: 'Characteristic read flag' },
  { name: 'FLAG_WRITE', kind: 'Constant', description: 'Characteristic write flag' },
  { name: 'FLAG_NOTIFY', kind: 'Constant', description: 'Characteristic notify flag' },
  { name: 'FLAG_INDICATE', kind: 'Constant', description: 'Characteristic indicate flag' },
]

const PIN_MEMBERS = [
  { name: 'init', kind: 'Method', description: 'Initialize the pin' },
  { name: 'value', kind: 'Method', description: 'Get/set pin value' },
  { name: 'on', kind: 'Method', description: 'Set pin high' },
  { name: 'off', kind: 'Method', description: 'Set pin low' },
  { name: 'irq', kind: 'Method', description: 'Set interrupt handler' },
  { name: 'IN', kind: 'Constant', description: 'Input mode' },
  { name: 'OUT', kind: 'Constant', description: 'Output mode' },
  { name: 'OPEN_DRAIN', kind: 'Constant', description: 'Open drain mode' },
  { name: 'ALT', kind: 'Constant', description: 'Alternate function mode' },
  { name: 'ALT_OPEN_DRAIN', kind: 'Constant', description: 'Alt function open drain' },
  { name: 'PULL_UP', kind: 'Constant', description: 'Pull-up resistor' },
  { name: 'PULL_DOWN', kind: 'Constant', description: 'Pull-down resistor' },
  { name: 'PULL_HOLD', kind: 'Constant', description: 'Hold pull state' },
  { name: 'IRQ_RISING', kind: 'Constant', description: 'Rising edge interrupt' },
  { name: 'IRQ_FALLING', kind: 'Constant', description: 'Falling edge interrupt' },
  { name: 'IRQ_LOW_LEVEL', kind: 'Constant', description: 'Low level interrupt' },
  { name: 'IRQ_HIGH_LEVEL', kind: 'Constant', description: 'High level interrupt' },
  { name: 'WAKE_LOW', kind: 'Constant', description: 'Wake on low' },
  { name: 'WAKE_HIGH', kind: 'Constant', description: 'Wake on high' },
]

const I2C_MEMBERS = [
  { name: 'init', kind: 'Method', description: 'Initialize I2C' },
  { name: 'deinit', kind: 'Method', description: 'Deinitialize I2C' },
  { name: 'scan', kind: 'Method', description: 'Scan for devices' },
  { name: 'start', kind: 'Method', description: 'Generate start condition' },
  { name: 'stop', kind: 'Method', description: 'Generate stop condition' },
  { name: 'readinto', kind: 'Method', description: 'Read into buffer' },
  { name: 'write', kind: 'Method', description: 'Write bytes' },
  { name: 'readfrom', kind: 'Method', description: 'Read from device' },
  { name: 'readfrom_into', kind: 'Method', description: 'Read from device into buffer' },
  { name: 'writeto', kind: 'Method', description: 'Write to device' },
  { name: 'readfrom_mem', kind: 'Method', description: 'Read from device memory' },
  { name: 'readfrom_mem_into', kind: 'Method', description: 'Read from memory into buffer' },
  { name: 'writeto_mem', kind: 'Method', description: 'Write to device memory' },
]

const SPI_MEMBERS = [
  { name: 'init', kind: 'Method', description: 'Initialize SPI' },
  { name: 'deinit', kind: 'Method', description: 'Deinitialize SPI' },
  { name: 'read', kind: 'Method', description: 'Read bytes' },
  { name: 'readinto', kind: 'Method', description: 'Read into buffer' },
  { name: 'write', kind: 'Method', description: 'Write bytes' },
  { name: 'write_readinto', kind: 'Method', description: 'Write and read simultaneously' },
  { name: 'LSB', kind: 'Constant', description: 'LSB first' },
  { name: 'MSB', kind: 'Constant', description: 'MSB first' },
]

const UART_MEMBERS = [
  { name: 'init', kind: 'Method', description: 'Initialize UART' },
  { name: 'deinit', kind: 'Method', description: 'Deinitialize UART' },
  { name: 'any', kind: 'Method', description: 'Check if data available' },
  { name: 'read', kind: 'Method', description: 'Read bytes' },
  { name: 'readinto', kind: 'Method', description: 'Read into buffer' },
  { name: 'readline', kind: 'Method', description: 'Read line' },
  { name: 'write', kind: 'Method', description: 'Write bytes' },
  { name: 'sendbreak', kind: 'Method', description: 'Send break condition' },
  { name: 'irq', kind: 'Method', description: 'Set IRQ handler' },
  { name: 'flush', kind: 'Method', description: 'Wait for TX complete' },
  { name: 'txdone', kind: 'Method', description: 'Check TX complete' },
]

const PWM_MEMBERS = [
  { name: 'init', kind: 'Method', description: 'Initialize PWM' },
  { name: 'deinit', kind: 'Method', description: 'Deinitialize PWM' },
  { name: 'freq', kind: 'Method', description: 'Get/set frequency' },
  { name: 'duty', kind: 'Method', description: 'Get/set duty (0-1023)' },
  { name: 'duty_u16', kind: 'Method', description: 'Get/set duty (0-65535)' },
  { name: 'duty_ns', kind: 'Method', description: 'Get/set duty in nanoseconds' },
]

const ADC_MEMBERS = [
  { name: 'init', kind: 'Method', description: 'Initialize ADC' },
  { name: 'deinit', kind: 'Method', description: 'Deinitialize ADC' },
  { name: 'read', kind: 'Method', description: 'Read ADC value' },
  { name: 'read_u16', kind: 'Method', description: 'Read as 16-bit value' },
  { name: 'read_uv', kind: 'Method', description: 'Read in microvolts' },
  { name: 'atten', kind: 'Method', description: 'Set attenuation' },
  { name: 'width', kind: 'Method', description: 'Set bit width' },
  { name: 'block', kind: 'Method', description: 'Get ADC block' },
  { name: 'ATTN_0DB', kind: 'Constant', description: '0dB attenuation' },
  { name: 'ATTN_2_5DB', kind: 'Constant', description: '2.5dB attenuation' },
  { name: 'ATTN_6DB', kind: 'Constant', description: '6dB attenuation' },
  { name: 'ATTN_11DB', kind: 'Constant', description: '11dB attenuation' },
  { name: 'WIDTH_9BIT', kind: 'Constant', description: '9-bit resolution' },
  { name: 'WIDTH_10BIT', kind: 'Constant', description: '10-bit resolution' },
  { name: 'WIDTH_11BIT', kind: 'Constant', description: '11-bit resolution' },
  { name: 'WIDTH_12BIT', kind: 'Constant', description: '12-bit resolution' },
]

const TIMER_MEMBERS = [
  { name: 'init', kind: 'Method', description: 'Initialize timer' },
  { name: 'deinit', kind: 'Method', description: 'Deinitialize timer' },
  { name: 'value', kind: 'Method', description: 'Get current value' },
  { name: 'ONE_SHOT', kind: 'Constant', description: 'One-shot mode' },
  { name: 'PERIODIC', kind: 'Constant', description: 'Periodic mode' },
]

const WLAN_MEMBERS = [
  { name: 'active', kind: 'Method', description: 'Activate/deactivate interface' },
  { name: 'connect', kind: 'Method', description: 'Connect to WiFi' },
  { name: 'disconnect', kind: 'Method', description: 'Disconnect from WiFi' },
  { name: 'isconnected', kind: 'Method', description: 'Check connection status' },
  { name: 'scan', kind: 'Method', description: 'Scan for networks' },
  { name: 'status', kind: 'Method', description: 'Get connection status' },
  { name: 'ifconfig', kind: 'Method', description: 'Get/set IP configuration' },
  { name: 'config', kind: 'Method', description: 'Get/set interface config' },
]

const SOCKET_INSTANCE_MEMBERS = [
  { name: 'close', kind: 'Method', description: 'Close socket' },
  { name: 'bind', kind: 'Method', description: 'Bind to address' },
  { name: 'listen', kind: 'Method', description: 'Listen for connections' },
  { name: 'accept', kind: 'Method', description: 'Accept connection' },
  { name: 'connect', kind: 'Method', description: 'Connect to address' },
  { name: 'send', kind: 'Method', description: 'Send data' },
  { name: 'sendall', kind: 'Method', description: 'Send all data' },
  { name: 'recv', kind: 'Method', description: 'Receive data' },
  { name: 'sendto', kind: 'Method', description: 'Send to address (UDP)' },
  { name: 'recvfrom', kind: 'Method', description: 'Receive from address (UDP)' },
  { name: 'setsockopt', kind: 'Method', description: 'Set socket option' },
  { name: 'settimeout', kind: 'Method', description: 'Set timeout' },
  { name: 'setblocking', kind: 'Method', description: 'Set blocking mode' },
  { name: 'makefile', kind: 'Method', description: 'Create file-like object' },
  { name: 'read', kind: 'Method', description: 'Read data' },
  { name: 'readline', kind: 'Method', description: 'Read line' },
  { name: 'write', kind: 'Method', description: 'Write data' },
]

// =============================================================================
// CODE SNIPPETS
// =============================================================================

const CODE_SNIPPETS = [
  {
    label: 'pin-output',
    insertText: 'from machine import Pin\n\nled = Pin(${1:2}, Pin.OUT)\nled.value(${2:1})',
    description: 'Setup output pin (LED)',
  },
  {
    label: 'pin-input',
    insertText: 'from machine import Pin\n\nbutton = Pin(${1:0}, Pin.IN, Pin.PULL_UP)\nvalue = button.value()',
    description: 'Setup input pin with pull-up',
  },
  {
    label: 'pin-irq',
    insertText: `from machine import Pin

def callback(pin):
    print("Pin changed:", pin)

button = Pin(\${1:0}, Pin.IN, Pin.PULL_UP)
button.irq(trigger=Pin.IRQ_FALLING, handler=callback)`,
    description: 'Pin with interrupt handler',
  },
  {
    label: 'wifi-connect',
    insertText: `import network

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('\${1:SSID}', '\${2:password}')

while not wlan.isconnected():
    pass

print('Connected:', wlan.ifconfig())`,
    description: 'Connect to WiFi network',
  },
  {
    label: 'wifi-ap',
    insertText: `import network

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='\${1:ESP32-AP}', password='\${2:12345678}')

print('AP Active:', ap.ifconfig())`,
    description: 'Create WiFi access point',
  },
  {
    label: 'i2c-scan',
    insertText: `from machine import Pin, I2C

i2c = I2C(\${1:0}, scl=Pin(\${2:22}), sda=Pin(\${3:21}))
devices = i2c.scan()
print('I2C devices:', [hex(d) for d in devices])`,
    description: 'Scan I2C bus for devices',
  },
  {
    label: 'i2c-read-write',
    insertText: `from machine import Pin, I2C

i2c = I2C(\${1:0}, scl=Pin(\${2:22}), sda=Pin(\${3:21}))

# Write to device
i2c.writeto(\${4:0x48}, bytes([\${5:0x00}]))

# Read from device
data = i2c.readfrom(\${4:0x48}, \${6:2})
print('Data:', data)`,
    description: 'I2C read/write example',
  },
  {
    label: 'spi-init',
    insertText: `from machine import Pin, SPI

spi = SPI(\${1:1}, baudrate=\${2:1000000}, polarity=0, phase=0,
          sck=Pin(\${3:18}), mosi=Pin(\${4:23}), miso=Pin(\${5:19}))
cs = Pin(\${6:5}, Pin.OUT)

cs.off()
data = spi.read(\${7:4})
cs.on()
print('Data:', data)`,
    description: 'SPI initialization and read',
  },
  {
    label: 'pwm-led',
    insertText: `from machine import Pin, PWM

pwm = PWM(Pin(\${1:2}))
pwm.freq(\${2:1000})
pwm.duty(\${3:512})  # 0-1023`,
    description: 'PWM LED brightness control',
  },
  {
    label: 'pwm-fade',
    insertText: `from machine import Pin, PWM
import time

pwm = PWM(Pin(\${1:2}))
pwm.freq(1000)

while True:
    for duty in range(0, 1024, 8):
        pwm.duty(duty)
        time.sleep_ms(10)
    for duty in range(1023, -1, -8):
        pwm.duty(duty)
        time.sleep_ms(10)`,
    description: 'PWM LED fade effect',
  },
  {
    label: 'adc-read',
    insertText: `from machine import Pin, ADC

adc = ADC(Pin(\${1:34}))
adc.atten(ADC.ATTN_11DB)  # 0-3.3V range
adc.width(ADC.WIDTH_12BIT)  # 0-4095

value = adc.read()
voltage = value * 3.3 / 4095
print(f'ADC: {value}, Voltage: {voltage:.2f}V')`,
    description: 'ADC voltage reading',
  },
  {
    label: 'uart-init',
    insertText: `from machine import UART, Pin

uart = UART(\${1:2}, baudrate=\${2:115200}, tx=Pin(\${3:17}), rx=Pin(\${4:16}))

# Write data
uart.write('Hello\\n')

# Read data
if uart.any():
    data = uart.read()
    print('Received:', data)`,
    description: 'UART communication',
  },
  {
    label: 'timer-periodic',
    insertText: `from machine import Timer

def callback(t):
    print('Timer triggered!')

timer = Timer(\${1:0})
timer.init(period=\${2:1000}, mode=Timer.PERIODIC, callback=callback)`,
    description: 'Periodic timer callback',
  },
  {
    label: 'timer-oneshot',
    insertText: `from machine import Timer

def callback(t):
    print('One-shot timer!')

timer = Timer(\${1:0})
timer.init(period=\${2:5000}, mode=Timer.ONE_SHOT, callback=callback)`,
    description: 'One-shot timer',
  },
  {
    label: 'async-blink',
    insertText: `import asyncio
from machine import Pin

async def blink(pin, period_ms):
    while True:
        pin.on()
        await asyncio.sleep_ms(period_ms)
        pin.off()
        await asyncio.sleep_ms(period_ms)

async def main():
    asyncio.create_task(blink(Pin(\${1:2}, Pin.OUT), \${2:500}))
    while True:
        await asyncio.sleep(1)

asyncio.run(main())`,
    description: 'Async LED blink',
  },
  {
    label: 'async-multi',
    insertText: `import asyncio
from machine import Pin

async def task1():
    led = Pin(\${1:2}, Pin.OUT)
    while True:
        led.value(not led.value())
        await asyncio.sleep_ms(\${2:500})

async def task2():
    while True:
        print('Task 2 running')
        await asyncio.sleep(\${3:1})

async def main():
    await asyncio.gather(task1(), task2())

asyncio.run(main())`,
    description: 'Multiple async tasks',
  },
  {
    label: 'web-server',
    insertText: `import socket

def web_page():
    return '''<!DOCTYPE html>
<html><body>
<h1>ESP32 Web Server</h1>
</body></html>'''

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 80))
s.listen(5)
print('Server running on port 80')

while True:
    conn, addr = s.accept()
    print('Connection from', addr)
    request = conn.recv(1024)
    response = web_page()
    conn.send('HTTP/1.1 200 OK\\r\\n')
    conn.send('Content-Type: text/html\\r\\n')
    conn.send('Connection: close\\r\\n\\r\\n')
    conn.send(response)
    conn.close()`,
    description: 'Simple HTTP web server',
  },
  {
    label: 'async-web-server',
    insertText: `import asyncio

async def handle_client(reader, writer):
    request = await reader.read(1024)
    response = '''HTTP/1.1 200 OK\\r\\nContent-Type: text/html\\r\\n\\r\\n
<html><body><h1>ESP32 Async Server</h1></body></html>'''
    writer.write(response)
    await writer.drain()
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_client, '0.0.0.0', 80)
    print('Server running on port 80')
    await server.wait_closed()

asyncio.run(main())`,
    description: 'Async web server',
  },
  {
    label: 'neopixel',
    insertText: `from machine import Pin
from neopixel import NeoPixel

np = NeoPixel(Pin(\${1:5}), \${2:8})  # pin, num LEDs
np[0] = (\${3:255}, \${4:0}, \${5:0})  # RGB
np.write()`,
    description: 'NeoPixel LED strip',
  },
  {
    label: 'neopixel-rainbow',
    insertText: `from machine import Pin
from neopixel import NeoPixel
import time

np = NeoPixel(Pin(\${1:5}), \${2:8})

def wheel(pos):
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)

while True:
    for j in range(256):
        for i in range(len(np)):
            np[i] = wheel((i * 256 // len(np) + j) & 255)
        np.write()
        time.sleep_ms(20)`,
    description: 'NeoPixel rainbow effect',
  },
  {
    label: 'dht-sensor',
    insertText: `from machine import Pin
import dht

sensor = dht.DHT\${1|11,22|}(Pin(\${2:4}))
sensor.measure()
print('Temperature:', sensor.temperature())
print('Humidity:', sensor.humidity())`,
    description: 'DHT temperature/humidity sensor',
  },
  {
    label: 'ds18b20',
    insertText: `from machine import Pin
import onewire
import ds18x20
import time

ow = onewire.OneWire(Pin(\${1:4}))
ds = ds18x20.DS18X20(ow)
roms = ds.scan()
print('Found devices:', roms)

ds.convert_temp()
time.sleep_ms(750)
for rom in roms:
    print(f'Temperature: {ds.read_temp(rom):.1f}°C')`,
    description: 'DS18B20 temperature sensor',
  },
  {
    label: 'deep-sleep',
    insertText: `import machine
import time

print('Going to sleep in 5 seconds...')
time.sleep(5)

# Sleep for specified microseconds
machine.deepsleep(\${1:10000000})  # 10 seconds`,
    description: 'Enter deep sleep mode',
  },
  {
    label: 'deep-sleep-ext',
    insertText: `import machine
import esp32
from machine import Pin

# Configure wake on external pin
wake_pin = Pin(\${1:0}, Pin.IN, Pin.PULL_UP)
esp32.wake_on_ext0(pin=wake_pin, level=esp32.WAKEUP_ALL_LOW)

print('Going to sleep, wake on pin low...')
machine.deepsleep()`,
    description: 'Deep sleep with external wake',
  },
  {
    label: 'rtc-time',
    insertText: `from machine import RTC
import ntptime
import network

# Connect to WiFi first
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('\${1:SSID}', '\${2:password}')
while not wlan.isconnected():
    pass

# Sync time from NTP
ntptime.settime()

# Read RTC
rtc = RTC()
print('Current time:', rtc.datetime())`,
    description: 'RTC with NTP sync',
  },
  {
    label: 'watchdog',
    insertText: `from machine import WDT

# Initialize watchdog with 5 second timeout
wdt = WDT(timeout=\${1:5000})

# In your main loop, feed the watchdog
while True:
    # ... do work ...
    wdt.feed()  # Reset watchdog timer`,
    description: 'Watchdog timer',
  },
  {
    label: 'file-read-write',
    insertText: `# Write to file
with open('\${1:/data.txt}', 'w') as f:
    f.write('Hello, MicroPython!\\n')

# Read from file
with open('\${1:/data.txt}', 'r') as f:
    content = f.read()
    print(content)`,
    description: 'File read/write operations',
  },
  {
    label: 'json-config',
    insertText: `import json

# Save config
config = {
    'ssid': '\${1:WiFi}',
    'password': '\${2:pass}',
    'settings': {'brightness': 100}
}
with open('/config.json', 'w') as f:
    json.dump(config, f)

# Load config
with open('/config.json', 'r') as f:
    config = json.load(f)
print(config)`,
    description: 'JSON config file',
  },
  {
    label: 'class-def',
    insertText: `class \${1:MyClass}:
    def __init__(self\${2:, arg}):
        self.\${3:value} = \${2:arg}

    def \${4:method}(self):
        return self.\${3:value}`,
    description: 'Class definition',
  },
  {
    label: 'async-def',
    insertText: `async def \${1:function_name}(\${2:args}):
    \${3:await asyncio.sleep(1)}
    return \${4:result}`,
    description: 'Async function definition',
  },
  {
    label: 'try-except',
    insertText: `try:
    \${1:# code}
except \${2:Exception} as e:
    print('Error:', e)
finally:
    \${3:# cleanup}`,
    description: 'Try-except block',
  },
  {
    label: 'for-enumerate',
    insertText: `for \${1:i}, \${2:item} in enumerate(\${3:items}):
    print(f'{\${1:i}}: {\${2:item}}')`,
    description: 'For loop with enumerate',
  },
  {
    label: 'list-comprehension',
    insertText: '[\${1:x} for \${1:x} in \${2:items}\${3: if \${1:x} > 0}]',
    description: 'List comprehension',
  },
  {
    label: 'dict-comprehension',
    insertText: '{\${1:k}: \${2:v} for \${1:k}, \${2:v} in \${3:items}.items()}',
    description: 'Dict comprehension',
  },
  {
    label: 'mqtt-client',
    insertText: `from umqtt.simple import MQTTClient

client = MQTTClient('\${1:client_id}', '\${2:broker.hivemq.com}')
client.connect()

# Publish
client.publish(b'\${3:topic}', b'\${4:message}')

# Subscribe
def callback(topic, msg):
    print(topic, msg)

client.set_callback(callback)
client.subscribe(b'\${5:topic}')

while True:
    client.check_msg()`,
    description: 'MQTT client example',
  },
  {
    label: 'http-request',
    insertText: `import urequests

response = urequests.get('\${1:http://httpbin.org/get}')
print('Status:', response.status_code)
print('Body:', response.text)
response.close()`,
    description: 'HTTP GET request',
  },
  {
    label: 'espnow-init',
    insertText: `import network
import espnow

# Initialize WiFi in station mode
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Initialize ESP-NOW
e = espnow.ESPNow()
e.active(True)

# Add peer (MAC address)
peer = b'\\xaa\\xbb\\xcc\\xdd\\xee\\xff'
e.add_peer(peer)

# Send data
e.send(peer, b'Hello ESP-NOW!')

# Receive data
host, msg = e.recv()
print('From:', host, 'Message:', msg)`,
    description: 'ESP-NOW communication',
  },
]

// =============================================================================
// MODULE MEMBER MAP
// =============================================================================

const MODULE_MEMBERS: Record<string, typeof MACHINE_MEMBERS> = {
  'machine': MACHINE_MEMBERS,
  'network': NETWORK_MEMBERS,
  'time': TIME_MEMBERS,
  'utime': TIME_MEMBERS,
  'os': OS_MEMBERS,
  'uos': OS_MEMBERS,
  'gc': GC_MEMBERS,
  'sys': SYS_MEMBERS,
  'json': JSON_MEMBERS,
  'ujson': JSON_MEMBERS,
  'socket': SOCKET_MEMBERS,
  'usocket': SOCKET_MEMBERS,
  'asyncio': ASYNCIO_MEMBERS,
  'uasyncio': ASYNCIO_MEMBERS,
  'esp32': ESP32_MEMBERS,
  'bluetooth': BLUETOOTH_MEMBERS,
}

const CLASS_MEMBERS: Record<string, typeof PIN_MEMBERS> = {
  'Pin': PIN_MEMBERS,
  'I2C': I2C_MEMBERS,
  'SoftI2C': I2C_MEMBERS,
  'SPI': SPI_MEMBERS,
  'SoftSPI': SPI_MEMBERS,
  'UART': UART_MEMBERS,
  'PWM': PWM_MEMBERS,
  'ADC': ADC_MEMBERS,
  'Timer': TIMER_MEMBERS,
  'WLAN': WLAN_MEMBERS,
  'socket': SOCKET_INSTANCE_MEMBERS,
}

const TYPE_METHODS: Record<string, typeof STRING_METHODS> = {
  'str': STRING_METHODS,
  'list': LIST_METHODS,
  'dict': DICT_METHODS,
  'set': SET_METHODS,
  'bytes': BYTES_METHODS,
  'bytearray': BYTES_METHODS,
  'file': FILE_METHODS,
}

// =============================================================================
// USER CODE ANALYSIS
// =============================================================================

interface UserSymbol {
  name: string
  kind: 'Function' | 'Class' | 'Variable' | 'Method'
  signature?: string
  line: number
}

function extractUserSymbols(code: string): UserSymbol[] {
  const symbols: UserSymbol[] = []
  const lines = code.split('\n')

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i]
    const lineNum = i + 1

    // Function definitions
    const funcMatch = line.match(/^\s*(?:async\s+)?def\s+(\w+)\s*\(([^)]*)\)/)
    if (funcMatch) {
      symbols.push({
        name: funcMatch[1],
        kind: 'Function',
        signature: `${funcMatch[1]}(${funcMatch[2]})`,
        line: lineNum,
      })
    }

    // Class definitions
    const classMatch = line.match(/^\s*class\s+(\w+)(?:\s*\([^)]*\))?:/)
    if (classMatch) {
      symbols.push({
        name: classMatch[1],
        kind: 'Class',
        line: lineNum,
      })
    }

    // Top-level variable assignments (simple cases)
    const varMatch = line.match(/^(\w+)\s*=\s*(?!.*def\s|.*class\s)/)
    if (varMatch && !line.trim().startsWith('#')) {
      symbols.push({
        name: varMatch[1],
        kind: 'Variable',
        line: lineNum,
      })
    }
  }

  return symbols
}

// =============================================================================
// HELPER FUNCTIONS
// =============================================================================

function getKind(kind: string, monaco: any): number {
  switch (kind) {
    case 'Class': return monaco.languages.CompletionItemKind.Class
    case 'Function': return monaco.languages.CompletionItemKind.Function
    case 'Method': return monaco.languages.CompletionItemKind.Method
    case 'Variable': return monaco.languages.CompletionItemKind.Variable
    case 'Constant': return monaco.languages.CompletionItemKind.Constant
    case 'Module': return monaco.languages.CompletionItemKind.Module
    case 'Snippet': return monaco.languages.CompletionItemKind.Snippet
    case 'Keyword': return monaco.languages.CompletionItemKind.Keyword
    case 'Property': return monaco.languages.CompletionItemKind.Property
    default: return monaco.languages.CompletionItemKind.Text
  }
}

// Detect type from variable assignment
function detectType(code: string, varName: string): string | null {
  const patterns: [RegExp, string][] = [
    [new RegExp(`${varName}\\s*=\\s*['"]`), 'str'],
    [new RegExp(`${varName}\\s*=\\s*\\[`), 'list'],
    [new RegExp(`${varName}\\s*=\\s*\\{`), 'dict'],
    [new RegExp(`${varName}\\s*=\\s*\\(`), 'tuple'],
    [new RegExp(`${varName}\\s*=\\s*set\\(`), 'set'],
    [new RegExp(`${varName}\\s*=\\s*b['"]`), 'bytes'],
    [new RegExp(`${varName}\\s*=\\s*bytearray\\(`), 'bytearray'],
    [new RegExp(`${varName}\\s*=\\s*open\\(`), 'file'],
    [new RegExp(`${varName}\\s*=\\s*Pin\\(`), 'Pin'],
    [new RegExp(`${varName}\\s*=\\s*I2C\\(`), 'I2C'],
    [new RegExp(`${varName}\\s*=\\s*SoftI2C\\(`), 'I2C'],
    [new RegExp(`${varName}\\s*=\\s*SPI\\(`), 'SPI'],
    [new RegExp(`${varName}\\s*=\\s*SoftSPI\\(`), 'SPI'],
    [new RegExp(`${varName}\\s*=\\s*UART\\(`), 'UART'],
    [new RegExp(`${varName}\\s*=\\s*PWM\\(`), 'PWM'],
    [new RegExp(`${varName}\\s*=\\s*ADC\\(`), 'ADC'],
    [new RegExp(`${varName}\\s*=\\s*Timer\\(`), 'Timer'],
    [new RegExp(`${varName}\\s*=\\s*WLAN\\(`), 'WLAN'],
    [new RegExp(`${varName}\\s*=\\s*network\\.WLAN\\(`), 'WLAN'],
    [new RegExp(`${varName}\\s*=\\s*socket\\.socket\\(`), 'socket'],
  ]

  for (const [pattern, type] of patterns) {
    if (pattern.test(code)) {
      return type
    }
  }
  return null
}

// =============================================================================
// MAIN COMPLETION PROVIDER
// =============================================================================

export function registerMicroPythonCompletions(monaco: any) {
  monaco.languages.registerCompletionItemProvider('python', {
    triggerCharacters: ['.', ' ', '(', ',', '[', '{', "'", '"'],

    provideCompletionItems(model: any, position: any) {
      const textUntilPosition = model.getValueInRange({
        startLineNumber: position.lineNumber,
        startColumn: 1,
        endLineNumber: position.lineNumber,
        endColumn: position.column,
      })

      const fullText = model.getValue()
      const word = model.getWordUntilPosition(position)
      const range = {
        startLineNumber: position.lineNumber,
        startColumn: word.startColumn,
        endLineNumber: position.lineNumber,
        endColumn: word.endColumn,
      }

      const suggestions: any[] = []

      // =======================================================================
      // 1. IMPORT COMPLETIONS
      // =======================================================================
      if (/^\s*import\s+$/.test(textUntilPosition) ||
          /^\s*from\s+$/.test(textUntilPosition)) {
        for (const mod of [...MICROPYTHON_MODULES, ...ESP32_MODULES]) {
          suggestions.push({
            label: mod.name,
            kind: monaco.languages.CompletionItemKind.Module,
            insertText: mod.name,
            detail: mod.description,
            range,
            sortText: '0' + mod.name,
          })
        }
        return { suggestions }
      }

      // from module import ...
      const fromImportMatch = textUntilPosition.match(/^\s*from\s+(\w+)\s+import\s+$/)
      if (fromImportMatch) {
        const moduleName = fromImportMatch[1]
        const members = MODULE_MEMBERS[moduleName]
        if (members) {
          for (const member of members) {
            suggestions.push({
              label: member.name,
              kind: getKind(member.kind, monaco),
              insertText: member.name,
              detail: member.description,
              range,
            })
          }
          return { suggestions }
        }
      }

      // =======================================================================
      // 2. DOT COMPLETIONS (module.X, type.X, variable.X)
      // =======================================================================
      const dotMatch = textUntilPosition.match(/(\w+)\.\s*$/)
      if (dotMatch) {
        const prefix = dotMatch[1]

        // Check if it's a module
        if (MODULE_MEMBERS[prefix]) {
          for (const member of MODULE_MEMBERS[prefix]) {
            suggestions.push({
              label: member.name,
              kind: getKind(member.kind, monaco),
              insertText: member.name,
              detail: member.description,
              range,
            })
          }
          return { suggestions }
        }

        // Check if it's a class (static members)
        if (CLASS_MEMBERS[prefix]) {
          for (const member of CLASS_MEMBERS[prefix]) {
            suggestions.push({
              label: member.name,
              kind: getKind(member.kind, monaco),
              insertText: member.kind === 'Method' ? member.name + '()' : member.name,
              detail: member.description,
              range,
            })
          }
          return { suggestions }
        }

        // Check if it's a basic type name
        if (TYPE_METHODS[prefix]) {
          for (const method of TYPE_METHODS[prefix]) {
            suggestions.push({
              label: method.name,
              kind: monaco.languages.CompletionItemKind.Method,
              insertText: method.name + '()',
              detail: method.signature,
              documentation: method.description,
              range,
            })
          }
          return { suggestions }
        }

        // Try to detect variable type
        const detectedType = detectType(fullText, prefix)
        if (detectedType) {
          // Check class instance methods
          if (CLASS_MEMBERS[detectedType]) {
            for (const member of CLASS_MEMBERS[detectedType]) {
              suggestions.push({
                label: member.name,
                kind: getKind(member.kind, monaco),
                insertText: member.kind === 'Method' ? member.name + '()' : member.name,
                detail: member.description,
                range,
              })
            }
            return { suggestions }
          }

          // Check type methods
          if (TYPE_METHODS[detectedType]) {
            for (const method of TYPE_METHODS[detectedType]) {
              suggestions.push({
                label: method.name,
                kind: monaco.languages.CompletionItemKind.Method,
                insertText: method.name + '()',
                detail: method.signature,
                documentation: method.description,
                range,
              })
            }
            return { suggestions }
          }
        }
      }

      // =======================================================================
      // 3. INSTANCE METHOD COMPLETION (e.g., wlan.connect)
      // =======================================================================
      // Common pattern: variable_name. when variable is an instance
      const instanceMatch = textUntilPosition.match(/(\w+)\.\s*(\w*)$/)
      if (instanceMatch) {
        const varName = instanceMatch[1].toLowerCase()

        // Try common naming conventions
        const nameToClass: Record<string, string> = {
          'pin': 'Pin', 'led': 'Pin', 'button': 'Pin', 'relay': 'Pin',
          'i2c': 'I2C', 'spi': 'SPI', 'uart': 'UART', 'serial': 'UART',
          'pwm': 'PWM', 'adc': 'ADC', 'timer': 'Timer', 'rtc': 'RTC',
          'wlan': 'WLAN', 'wifi': 'WLAN', 'ap': 'WLAN', 'sta': 'WLAN',
          'sock': 'socket', 's': 'socket', 'conn': 'socket', 'server': 'socket',
          'f': 'file', 'file': 'file',
        }

        for (const [pattern, className] of Object.entries(nameToClass)) {
          if (varName.includes(pattern) || varName === pattern) {
            const members = CLASS_MEMBERS[className]
            if (members) {
              for (const member of members) {
                suggestions.push({
                  label: member.name,
                  kind: getKind(member.kind, monaco),
                  insertText: member.kind === 'Method' ? member.name + '()' : member.name,
                  detail: member.description,
                  range,
                })
              }
              return { suggestions }
            }
          }
        }
      }

      // =======================================================================
      // 4. DEFAULT COMPLETIONS (no specific context)
      // =======================================================================

      // Python built-in functions
      for (const builtin of PYTHON_BUILTINS) {
        if (!word.word || builtin.name.toLowerCase().startsWith(word.word.toLowerCase())) {
          suggestions.push({
            label: builtin.name,
            kind: monaco.languages.CompletionItemKind.Function,
            insertText: builtin.name,
            detail: builtin.signature,
            documentation: builtin.description,
            range,
            sortText: '1' + builtin.name,
          })
        }
      }

      // Python keywords
      for (const kw of PYTHON_KEYWORDS) {
        if (!word.word || kw.name.toLowerCase().startsWith(word.word.toLowerCase())) {
          suggestions.push({
            label: kw.name,
            kind: monaco.languages.CompletionItemKind.Keyword,
            insertText: kw.name,
            detail: kw.description,
            range,
            sortText: '2' + kw.name,
          })
        }
      }

      // User-defined symbols from current file
      const userSymbols = extractUserSymbols(fullText)
      for (const symbol of userSymbols) {
        if (!word.word || symbol.name.toLowerCase().startsWith(word.word.toLowerCase())) {
          suggestions.push({
            label: symbol.name,
            kind: getKind(symbol.kind, monaco),
            insertText: symbol.name,
            detail: symbol.signature || `User ${symbol.kind.toLowerCase()} (line ${symbol.line})`,
            range,
            sortText: '0' + symbol.name, // User symbols first
          })
        }
      }

      // Modules (for general typing)
      for (const mod of [...MICROPYTHON_MODULES, ...ESP32_MODULES]) {
        if (!word.word || mod.name.toLowerCase().startsWith(word.word.toLowerCase())) {
          suggestions.push({
            label: mod.name,
            kind: monaco.languages.CompletionItemKind.Module,
            insertText: mod.name,
            detail: mod.description,
            range,
            sortText: '3' + mod.name,
          })
        }
      }

      // Code snippets
      for (const snippet of CODE_SNIPPETS) {
        if (!word.word || snippet.label.toLowerCase().startsWith(word.word.toLowerCase())) {
          suggestions.push({
            label: snippet.label,
            kind: monaco.languages.CompletionItemKind.Snippet,
            insertText: snippet.insertText,
            insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
            detail: 'Snippet: ' + snippet.description,
            documentation: snippet.description,
            range,
            sortText: '9' + snippet.label,
          })
        }
      }

      return { suggestions }
    },
  })
}

// =============================================================================
// TERMINAL HINTS
// =============================================================================

export const TERMINAL_HINTS: Record<string, string[]> = {
  'import ': ['machine', 'network', 'time', 'os', 'gc', 'json', 'asyncio', 'socket', 'sys', 'struct'],
  'from ': ['machine', 'network', 'time', 'os', 'gc', 'json', 'asyncio', 'socket'],
  'from machine import ': ['Pin', 'I2C', 'SoftI2C', 'SPI', 'UART', 'PWM', 'ADC', 'Timer', 'RTC', 'WDT'],
  'from network import ': ['WLAN'],
  'machine.': ['Pin', 'I2C', 'SPI', 'UART', 'PWM', 'ADC', 'Timer', 'reset', 'freq', 'deepsleep', 'lightsleep'],
  'network.': ['WLAN', 'STA_IF', 'AP_IF', 'hostname'],
  'Pin.': ['IN', 'OUT', 'PULL_UP', 'PULL_DOWN', 'OPEN_DRAIN', 'IRQ_RISING', 'IRQ_FALLING'],
  'Pin(': ['0', '1', '2', '4', '5', '12', '13', '14', '15', '16', '17', '18', '19', '21', '22', '23', '25', '26', '27', '32', '33'],
  'wlan.': ['active', 'connect', 'disconnect', 'isconnected', 'scan', 'status', 'ifconfig', 'config'],
  'time.': ['sleep', 'sleep_ms', 'sleep_us', 'ticks_ms', 'ticks_us', 'ticks_diff', 'time', 'localtime'],
  'gc.': ['collect', 'mem_free', 'mem_alloc', 'threshold', 'enable', 'disable'],
  'os.': ['listdir', 'mkdir', 'remove', 'rmdir', 'rename', 'stat', 'uname', 'getcwd', 'chdir'],
  'sys.': ['exit', 'path', 'modules', 'version', 'platform', 'print_exception'],
  'json.': ['dumps', 'loads', 'dump', 'load'],
  'asyncio.': ['run', 'create_task', 'sleep', 'sleep_ms', 'gather', 'Event', 'Lock'],
  'socket.': ['socket', 'getaddrinfo', 'AF_INET', 'SOCK_STREAM', 'SOCK_DGRAM'],
  'print(': ["'Hello'", 'f"Value: {x}"', 'variable', 'list()', 'dict()'],
  'len(': ['string', 'list', 'dict', 'bytes'],
  'range(': ['10', 'start, stop', 'start, stop, step'],
  'for ': ['i in range(', 'item in list:', 'key, value in dict.items():'],
  'if ': ['condition:', 'x > 0:', 'x is None:', 'x in list:'],
  'def ': ['function_name(args):', 'main():', '__init__(self):'],
  'class ': ['ClassName:', 'ClassName(Base):'],
  'with ': ['open(file) as f:', 'lock:'],
  'try:': [],
  'except ': ['Exception as e:', 'OSError:', 'ValueError:'],
  'async def ': ['main():', 'task():'],
  'await ': ['asyncio.sleep(', 'task', 'gather('],
}

export function getTerminalHint(input: string): string | null {
  const trimmed = input.trimStart()

  // Find best matching prefix
  let bestMatch = ''
  for (const prefix of Object.keys(TERMINAL_HINTS)) {
    if (trimmed.endsWith(prefix) && prefix.length > bestMatch.length) {
      bestMatch = prefix
    }
  }

  if (bestMatch) {
    const hints = TERMINAL_HINTS[bestMatch]
    return hints[0] || null
  }

  return null
}
