#!/usr/bin/python3
import time
import pyaudio
from hashlib import blake2b
import sys
from von_neumann import VonNeumann
from params import set_param_int, set_param_gen
import math
from helpers import show_help, convert_bytes
from extract import von_neumann_extract, hash_extract

# set constants
SLEEP_TIME = 0.3
BURN_IN_BYTES = 96000
DEFAULT_NUM_BYTES = 64
DEFAULT_FORMAT = 'bytes'
DEFAULT_BYTE_INTERVAL = 128
DEFAULT_BLOCK_SIZE = 6400

if __name__ == '__main__':

  # help page
  if '-h' in sys.argv:
    show_help()
    exit()

  # setup pyaudio stuff
  p = pyaudio .PyAudio()
  stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=48000,
    output=True,
    input=True,
    frames_per_buffer=1024)

  stream.start_stream()

  # initalize variables
  _buffer = bytearray()

  num_bytes = set_param_int(sys.argv, '-n', DEFAULT_NUM_BYTES)
  _format = set_param_gen(sys.argv, '-f', DEFAULT_FORMAT,
    'must give format after -f flag')

  byte_interval = set_param_int(sys.argv, '-i', DEFAULT_BYTE_INTERVAL)
  if byte_interval % 2 != 0:
    raise BaseException('byte interval must be even')

  extract_method = 'von_neumann'
  if '--hash' in sys.argv:
    extract_method = 'hash'
  block_size = set_param_int(sys.argv, '-b', DEFAULT_BLOCK_SIZE)

  if '-r' in sys.argv:
    num_bytes = math.inf
  
  plot = False
  if '-p' in sys.argv:
    plot = True

  # initialize extraction variables
  if extract_method == 'von_neumann':
    vn = VonNeumann()
  elif extract_method == 'hash':
    h = blake2b()

  # init plot
  even_bytes = dict()
  odd_bytes = dict()
  for i in range(256):
    even_bytes[i] = 0
    odd_bytes[i] = 0

  # burn-in loop
  while len(_buffer) < BURN_IN_BYTES:
    available = stream.get_read_available()
    if available == 0:
      time.sleep(SLEEP_TIME)
      continue

    _buffer.extend(stream.read(available))

  # if we are hash extracting, hash the burn-in too, as it doesn't make sense
  # to waste it
  if extract_method == 'hash':
    h.update(_buffer[:BURN_IN_BYTES])
    
  # variables for main loop

  # get rid of burn in bytes
  _buffer = _buffer[BURN_IN_BYTES:]
  
  bytes_written = 0
  to_plot_le = []
  to_plot_be = []

  # main loop
  while bytes_written < num_bytes:

    # sleep until we have enough bytes, then read them into buffer
    available = stream.get_read_available()
    if available <= min(block_size, 2 * byte_interval):
      time.sleep(SLEEP_TIME)
      continue
    
    b = stream.read(available)

    # if we're plotting, populate the plot array
    if plot:
      for i in range(0, len(b) - 2, 2):
        to_plot_le.append(int.from_bytes(b[i:i+2], byteorder='little', signed=True))
        to_plot_be.append(int.from_bytes(b[i:i+2], byteorder='big', signed=True))
        even_bytes[b[i]] += 1
        odd_bytes[b[i+1]] += 1

    _buffer.extend(b)

    # extract
    if extract_method == 'von_neumann':
      _buffer, out = von_neumann_extract(vn, _buffer, byte_interval)
    elif extract_method == 'hash':
      _buffer, out = hash_extract(h, _buffer, block_size)

    # write state to output
    if _format == 'bytes':
      sys.stdout.buffer.write(out)
      sys.stdout.buffer.flush()
    else:
      sys.stdout.write(convert_bytes(out, _format))
      sys.stdout.flush()

    bytes_written += len(out)

  # end main loop
  stream.stop_stream()

  # add a newline at the end if we're not doing bytes
  if _format != 'bytes':
    print()

  # plot
  if plot:
    
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(4)
    fig.suptitle('ENSURE LITTLE ENDIANNESS')

    ax[0].plot(to_plot_le)
    ax[0].set_facecolor('black')
    ax[0].set_title('raw signal over time, LITTLE ENDIAN')

    ax[1].plot(to_plot_be)
    ax[1].set_facecolor('black')
    ax[1].set_title('raw signal over time, BIG ENDIAN')

    ax[2].bar(list(even_bytes.keys()), list(even_bytes.values()))
    ax[2].set_facecolor('black')
    ax[2].set_title('even bytes')

    ax[3].bar(list(odd_bytes.keys()), list(odd_bytes.values()))
    ax[3].set_facecolor('black')
    ax[3].set_title('odd bytes')

    plt.show()

