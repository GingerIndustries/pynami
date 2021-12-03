import enum
from .errors import *
import string

def parseNumber(number, interpreter):
  original = number.replace("(", "").replace(")", "")
  number = original.split(">")
  number.reverse()
  allowed = [">", "^"]
  result = 0
  for c, char in enumerate(original):
    if char not in allowed:
      raise SyntaxError("Illegal character!", (interpreter.fileName, 1, c+1, original))
  for base, count in enumerate(number):
    result += len(count) * (10 ** base)
  return result

class SpecialNumberType(enum.Enum):
  INCREASE = "increase"
  DECREASE = "decrease"
  
  def __str__(self):
    if self.value == "increase":
      return "(>)"
    else:
      return "(<)"

class Number():
  def __init__(self, interpreter, representation):
    self.numberType = None
    self.rep = representation
    self.interpreter = interpreter
  def getValue(self):
    if self.rep == "((>))":
      value = SpecialNumberType.INCREASE
    elif self.rep == "((<))":
      value = SpecialNumberType.DECREASE
    elif self.rep == "((S))":
      value = self.interpreter.comparisonBuffer
    elif self.rep == "((^))":
      value = self.interpreter.getValueAtAddress(self.interpreter.addressPointer)
    elif self.rep == "((<))":
      value = self.interpreter.addressPointer
    else:
      value = parseNumber(self.rep, self.interpreter)
    return value
    
  
  def __str__(self):
    return self.rep

class Instruction():
  def __init__(self, interpreter):
    self.interpreter = interpreter
  
  def execute(self):
    pass

class SetAddressInstruction(Instruction):
  def __init__(self, interpreter, value):
    super().__init__(interpreter)
    self.value = value
    self.rep = value
  
  def execute(self):
    self.interpreter.setValueAtAddress(self.interpreter.addressPointer, self.value.getValue())
  def __str__(self):
    return "v" + str(self.rep)

class SetPointerInstruction(Instruction):
  def __init__(self, interpreter, address):
    super().__init__(interpreter)
    self.address = address
    self.rep = address
  
  def execute(self):
    self.interpreter.setAddressPointer(self.address.getValue())
  def __str__(self):
    return ">" + str(self.rep)

class SetComparisonBufferInstruction(Instruction):
  def __init__(self, interpreter, value):
    super().__init__(interpreter)
    self.value = value
    self.rep = value
  
  def execute(self):
    self.interpreter.setComparisonBuffer(self.value.getValue())
  def __str__(self):
    return "S" + str(self.rep)

class OutputInstruction(Instruction):
  def execute(self):
    print(chr(self.interpreter.getValueAtAddress(self.interpreter.addressPointer)), end="")
    if self.interpreter.__outputnumbers__:
      print()
      print("[" + str(self.interpreter.getValueAtAddress(self.interpreter.addressPointer)) + "]")
  
  def __str__(self):
    return "<<"

class RawOutputInstruction(Instruction):
  def execute(self):
    print(self.interpreter.getValueAtAddress(self.interpreter.addressPointer), end="")
  def __str__(self):
    return "<<<"

class InputInstruction(Instruction):
  def __init__(self, interpreter):
    super().__init__(interpreter)
  
  def execute(self):
    value = input()
    if value:
      f = 0
      for addr, char in enumerate(value, start=self.interpreter.addressPointer):
        self.interpreter.setValueAtAddress(addr, ord(char))
        f = addr
      self.interpreter.setAddressPointer(f+1)
  
  def __str__(self):
    return ">>"

class RawInputInstruction(Instruction):
  def execute(self):
    try:
      value = int(input())
    except ValueError:
      value = 0
    self.interpreter.setValueAtAddress(self.interpreter.addressPointer, value)
  def __str__(self):
    return ">>>"

class LoopMarker(Instruction):
  def __init__(self, interpreter, id):
    super().__init__(interpreter)
    self.id = id
  def __str__(self):
    return "L" + str(self.id.getValue())

class EqualJumpInstruction(Instruction):
  def __init__(self, interpreter, id_):
    super().__init__(interpreter)
    self.id = id_
  def execute(self):
    if self.interpreter.getValueAtAddress(self.interpreter.addressPointer) == self.interpreter.comparisonBuffer:
      for pointer, instruction in enumerate(self.interpreter.instructions):
        if type(instruction) == LoopMarker:
          if instruction.id.getValue() == self.id.getValue():
            self.interpreter.instructionPointer = pointer
            return
      self.interpreter.error("No matching ID! (" + str(self.id) + ")", 1, str(self))

  def __str__(self):
    return "A" + str(self.id)
class UnequalJumpInstruction(Instruction):
  def __init__(self, interpreter, id_):
    super().__init__(interpreter)   
    self.id = id_
  def execute(self):
    #print(self.interpreter.getValueAtAddress(self.interpreter.addressPointer) != self.interpreter.comparisonBuffer)
    if self.interpreter.getValueAtAddress(self.interpreter.addressPointer) != self.interpreter.comparisonBuffer:
      for pointer, instruction in enumerate(self.interpreter.instructions):
        if type(instruction) == LoopMarker:
          if instruction.id.getValue() == self.id.getValue():
            self.interpreter.instructionPointer = pointer
            return
      self.interpreter.error("No matching ID! (" + str(self.id) + ")", 1, str(self))
  def __str__(self):
    return "B" + str(self.id)
