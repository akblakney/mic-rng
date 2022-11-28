
# defines class for Von Neumann randomness extractor
class VonNeumann():
  
  def __init__(self):
    self.out = bytearray()
    self.curr_value = 0
    self.bit_count = 0

  def compare_and_add(self, b1, b2):

    # if they're the same, do nothing
    if b1 == b2:
      return

    # set according to one of the bits
    if b1 == 1:
      self.curr_value = set_bit(self.curr_value, self.bit_count)
    elif b1 == 0:
      self.curr_value = clear_bit(self.curr_value, self.bit_count)
    else:
      raise BaseException('invlaid bit value')
    self.bit_count += 1

    # check for bit_count of 8 to add byte to output, and reset internal state
    if self.bit_count == 8:
      self.out.append(self.curr_value)
      self.curr_value = 0
      self.bit_count = 0
      
  # return output state
  def state(self):
    return self.out

  # clears the OUTPUT state only, not the internal state (value, bit_count, etc.)
  # useful if we want to periodically read the state and reset it
  # for continued generation
  def clear_state(self):
    self.out = bytearray()
  
# helper method to set a bit (set to 1) at position
def set_bit(value, position):
  mask = 1 << position
  return value | mask

# helper method to clear a bit (set to 0) at position
def clear_bit(value, position):
  mask = 1 << position
  return value & ~mask
