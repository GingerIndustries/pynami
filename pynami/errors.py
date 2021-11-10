class InterpreterError(Exception):
  def __init__(self, message):
    super().__init__(message)
    self.message = message

class MemoryBufferError(InterpreterError):
  def __init__(self, message, address):
    super().__init__(message + " " + str(address))
    self.address = address

class InvalidMemoryIndexError(MemoryBufferError):
  def __init__(self, address):
    super().__init__("Attempted to access invalid memory address", address)