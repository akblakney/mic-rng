''' helper methods '''

def show_help():
  print('''
***** mic-rng *****
Usage: python3 rng.py [OPTIONS]
Synopsis: Reads raw data from the microphone and uses it to produce a random
  output, which is printed to stdout. 
Options: 
  -h bring up this help menu

  -n <num_bytes> gives the number of bytes to be output by the generator.
     the default value is set to 64. Note that the generator will output
     AT LEAST this many bytes, i.e. it sometimes generates more.

  -f <format> gives the format of the output. Current supported formats are
     raw bytes (the default if none is specified), ascii, alpha-numeric,
     dicewire, dicewire-alt, hex.

  -i <byte_interval> sets the interval between bytes considered by the Von
     Neumann extractor. The default is 128, but any even positive integer
     should work, with larger values being more robust.

  -r run the generator forever until terminated by the user

  --hash use hash extraction instead of Von Neumann extraction. Blake2b hash
    algorithm is used

  -b <block_size> specify block size for hash extraction. Default value is 6400,
     which should be sufficient for most cases. The higher the value, the slower
     the generator, but the more assurance that the output is random (more
     entropy per bit of hashed output). It is not recommended to use less than
     the default value of 6400.

  -p uses matplotlib library to plot the raw input used to generate random output
     matplotlib library must be installed.
Examples:

  python3 rng.py -n 16 -f ascii
    Prints 16 bytes of random data in the format of printable ascii characters.
    Note that this does NOT mean that 16 ascii characters are printed, as the 
    conversion from raw bytes to ascii characters is not one-to-one.

  python3 rng.py -n 1000 -i 16 > random_data
    Output 1kb (1,000 bytes) of random data to the file random_data in the form
    of raw bytes (random_data will be a binary file). Alos, the -i flag specifies
    that the Von Neumann generator will consider bytes that are 16 apart, which
    will be more efficient than the default value of 128 (8 times as fast), but
    potentially not as robust (no test results have been able to prove that
    smaller values give outputs that are less random, however).

  python3 rng.py -r > random_data
    Continually output random data into the file random_data until the user
    terminates the program. Since no format was specified, the data will be
    in the form of raw bytes, i.e. random_data will be a binary file.

  python3 rng.py --hash -b 100000 -f ascii
    Output 64 bytes (default) in ascii format, with hash extraction used on block
    sizes of 100kb.
''')

def hex_from_bytes(b):
  return b.hex()

# random in in range [a, b)
# using the "division with rejection" method from here: 
# https://www.pcg-random.org/posts/bounded-rands.html
# return None if sample fails
def unbiased_randint(_bytes, a, b):

  if b <= a:
    raise BaseException('invalid range')

  i = int.from_bytes(_bytes, byteorder='little')

  _range = b - a 
  _max = 2 ** (len(_bytes) * 8)

  if _range > _max:
    raise BaseException('not enough bytes to sample that range')

  # this essentially finds which bin the number is in
  # there are _range bins, each of size _max // _range
  ret = (i // (_max // _range))

  # reject if needed
  if ret >= _range:
    return None

  # adjust to fit in range
  return ret + a

# get ascii from bytearray
def ascii_from_bytes(b):
    ret = ''
    ascii_list = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-=~!@#$%^&*()_+[]{};\':\",./<>?|'
    n = len(ascii_list)

    for i in range(len(b)):
        r = unbiased_randint(b[i:i+1], 0, n)
        if r is None:
            continue
        curr = ascii_list[r]
        ret = '{}{}'.format(ret, curr)
    return ret

# alphanumeric with lower case
def alpha_numeric_from_bytes(b):
  ret = ''
  an_list = 'abcdefghijklmnopqrstuvwxyz0123456789'
  n = len(an_list)
  
  for i in range(len(b)):
    r = unbiased_randint(b[i:i+1], 0, n)
    if r is None:
      continue
    curr = an_list[r]
    ret = '{}{}'.format(ret, curr)
  return ret

# get digit from single byte
# we are using the unbiased sampling method meaning there is a chance of
# failure, in which case None is returned
def digit_from_byte(x):
  return unbiased_randint([x], 0, 10)

# b is a byte array, generate digits accordingly
def digits_from_bytes(b):
    ret = ''
    for x in b:
        curr = digit_from_byte(x)
        if curr is not None:
            ret = '{}{}'.format(ret, digit_from_byte(x))

    return ret

# Helper method to convert bytes to different formats
# take in bytes (s) and a format, output the bytes converted to the format
def convert_bytes(s, _format):
  if _format == 'hex':
    return hex_from_bytes(s)
  elif _format == 'ascii':
    return ascii_from_bytes(s)
  elif _format == 'alpha-numeric':
    return alpha_numeric_from_bytes(s)
  elif _format == 'digits':
    return digits_from_bytes(s)
  elif _format == 'bytes':
    return s
