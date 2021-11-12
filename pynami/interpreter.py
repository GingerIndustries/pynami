from .errors import *
from .instructions import *
import sys
import string

def prepare(program):
  # Removes comments, linebreaks, and spaces from a passed program

  def removeChunk(sentence, matches):
    new_s = ''
    lbound = 0
    for l, h in matches:
        new_s += sentence[lbound:l]
        lbound = h
    new_s += sentence[matches[-1][1]:]
    return new_s
  
  commentPositions = []
  for start, char in enumerate(program):
    if char == "[":
      end = None
      for e, char2 in enumerate(program[start:]):
        if char2 == "]":
          end = e+start+1
          break
      if not end:
        raise UnclosedCommentError
      commentPositions.append((start, end))
  
  if len(commentPositions):
    program = removeChunk(program, commentPositions)
  return program.replace("\n", "").replace(" ", "")


class Interpreter():
  def __init__(self, repl=False):
    self.memory = {}
    self.fileName = ""
    self.lastError = None
    self.addressPointer = 0
    self.instructionPointer = 0
    self.instructions = []
    self.comparisonBuffer = 0
    self.depth = 0
    self.__repl__ = repl
    self.__outputnumbers__ = False
  
  def error(self, message, position = None, text=None):
    if not position:
      position = self.instructionPointer
    if not text:
      text = str(self.instructions[self.instructionPointer])
    raise SyntaxError(message, (self.fileName, 1, position, text))
  
  def getValueAtAddress(self, addr):
    try:
      return self.memory[addr]
    except KeyError:
      raise InvalidMemoryIndexError(addr) from None
  
  def setValueAtAddress(self, addr, value):
    if value is SpecialNumberType.INCREASE:
      try:
        self.memory[addr] += 1
      except KeyError:
        self.memory[addr] = 1
    elif value is SpecialNumberType.DECREASE:
      try:
        self.memory[addr] -= 1
      except KeyError:
        self.memory[addr] = -1
    else:
      self.memory[addr] = value
  
  def setAddressPointer(self, addr):
    if addr is SpecialNumberType.INCREASE:
      self.addressPointer += 1
    elif addr is SpecialNumberType.DECREASE:
      self.addressPointer -= 1
    else:
      self.addressPointer = addr
  
  def setComparisonBuffer(self, value):
    if value is SpecialNumberType.INCREASE:
      self.comparisonBuffer += 1
    elif value is SpecialNumberType.DECREASE:
      self.comparisonBuffer -= 1
    else:
      self.comparisonBuffer = value
  
  def interpret(self, program):
    numberCache = []
    cachedInstruction = None
    program += "  "
    usedIDs = []
    skipInstructions = 0 #for << and >>
    for c, textInstruction in enumerate(list(program)):
      if skipInstructions > 0:
        skipInstructions -= 1
        continue
      if textInstruction == ")" and list(program)[c+1] != ")":
        numberCache.append(")")
        if len(numberCache) < 2:
          self.error("Malformed number!", c+1, program)
        if cachedInstruction == EqualJumpInstruction or cachedInstruction == UnequalJumpInstruction:
          if Number(self, "".join(numberCache)).value in usedIDs:
            self.error("Duplicate loop ID!", c, program)
        if cachedInstruction == EqualJumpInstruction or cachedInstruction == UnequalJumpInstruction or cachedInstruction == LoopMarker:
          _ = Number(self, "".join(numberCache)).value
          if _ == SpecialNumberType.INCREASE or _ == SpecialNumberType.DECREASE:
            self.error("Cannot use special numbers here!", c, program)
        self.instructions.append(cachedInstruction(self, Number(self, "".join(numberCache))))
        numberCache = []
        cachedInstruction = None
      elif textInstruction == "(" or len(numberCache) > 0:
        if not cachedInstruction:
          self.error("This command doesn't have a parameter!", c, program)
        numberCache.append(textInstruction)
        continue
      elif cachedInstruction:
        self.error("This command should have a parameter!", c, program)
      if textInstruction == "v":
        cachedInstruction = SetAddressInstruction
      elif textInstruction == ">":
        if list(program)[c+1] == ">":
          skipInstructions = 1
          self.instructions.append(InputInstruction(self))
        else:
          cachedInstruction = SetPointerInstruction
      elif textInstruction == "S":
        cachedInstruction = SetComparisonBufferInstruction
      elif textInstruction == "<" and list(program)[c+1] == "<":
        if list(program)[c+2] == "<":
          skipInstructions = 2
          self.instructions.append(RawOutputInstruction(self))
        else:
          skipInstructions = 1
          self.instructions.append(OutputInstruction(self))
      elif textInstruction == "L":
        cachedInstruction = LoopMarker
      elif textInstruction == "A":
        cachedInstruction = EqualJumpInstruction
      elif textInstruction == "B":
        cachedInstruction = UnequalJumpInstruction
  
  def restart(self):
    self.memory = {}
    self.addressPointer = 0
    self.instructionPointer = 0
    self.instructions = []
    self.comparisonBuffer = 0
    self.depth = 0

  def run(self, program, debug = False):
    self.instructionPointer = 0
    if program == "^^vv<><>BALS":
      # :)
      print("Hello World!")
      return
    try:
      self.interpret(program)
    except (SyntaxError, InterpreterError) as e:
      self.lastError = sys.exc_info()
      raise
    except Exception as e:
      self.lastError = sys.exc_info()
      raise InterpreterError("Error interpreting program: " + str(e) + "\nThis is probably a bug with the interpreter; use /traceback for a detailed log")
    for c, char in enumerate(program):
      if char not in ["^", "<", ">", "v", "A", "B", "S", "L", "(", ")", "\n", " "]:
        self.error("Illegal character!", c+1, program.replace("\n", ""))
    
    while True:
      try:
        self.instructions[self.instructionPointer].execute()
      except IndexError as e:
        self.lastError = sys.exc_info()
        self.error("Invalid syntax! (check for typos)", text=program)
      except InterpreterError as e:
        self.lastError = sys.exc_info()
        raise
      except Exception as e:
        self.lastError = sys.exc_info()
        raise InterpreterError("Error executing instruction " + str(self.instructions[self.instructionPointer]) + ": " + str(e) + "\nThis is probably a bug with the interpreter; use /traceback for a detailed log)")
      self.instructionPointer += 1
      if self.instructionPointer == len(self.instructions):
        break
