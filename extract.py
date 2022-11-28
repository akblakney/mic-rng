'''
extractions method for the RNG. Both take in buffer and return a modified
buffer as well as the extracted output
'''

# extracts as much of _buffer into VonNeumann object, and updates
# the buffer to get rid of extracted portion
#
# returns modified buffer and the extracted output
#
# vn is the VonNeumann object that has its own internal state
# and external state (output bytes)
#
# _buffer is the buffer that contains raw audio, we return
# a version of buffer that gets rid of already-processed data.
#
# byte_interval gives the byte interval for Von Neumann extractor.
def von_neumann_extract(vn, _buffer, byte_interval):

  # must assume that the state holds already-processed data
  vn.clear_state()

  # add as much of buffer as possible into VN
  while len(_buffer) > 2 * byte_interval:
    b1 = _buffer[0] % 2
    b2 = _buffer[byte_interval] % 2
    vn.compare_and_add(b1, b2)  
    _buffer = _buffer[2 * byte_interval:]

  return _buffer, vn.state()

# extracts as much of _buffer via hashing, and updates buffer to get rid of
# extracted portion
#
# returns modified buffer and the extracted output
#
# h is the hash object (blake2b hashlib object)
# 
# _buffer is the buffer that contains raw audio, to be updated
#
# block_size gives the size of blocks to hash
def hash_extract (h, _buffer, block_size):

  out = bytearray()

  while len(_buffer) > block_size:
    h.update(_buffer[:block_size])
    out.extend(h.digest())
    _buffer = _buffer[block_size:]

  return _buffer, out
  
