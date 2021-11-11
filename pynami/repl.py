from .interpreter import Interpreter, prepare
from .errors import InterpreterError
import traceback, sys, pprint

def run(code, interpreter, debug, autorestart):
  try:
    interpreter.run(prepare(code), debug)
    if autorestart:
      interpreter.restart()
  except (InterpreterError, SyntaxError) as e:
    print("\n".join(traceback.format_exception_only(sys.exc_info()[0], sys.exc_info()[1]))[:-1].lstrip())
  finally:
    interpreter.instructions = []
    print()

def repl():
  print("Pynami REPL version 1.0")
  print("Made by GingerIndustries 2021")
  print("Type /help for help.")

  interpreter = Interpreter(True)
  interpreter.fileName = "<shell>"
  debug = False
  autorestart = False
  outputnumbers = False
  pp = pprint.PrettyPrinter(indent=4)
  
  while True:
    try:
      code = input(">>> ")
    except KeyboardInterrupt:
      print("Goodbye!")
      exit()
    if code == "":
      pass
    elif code == "/help":
      print("""Commands list:
/help: Displays this menu
/load <path>: Loads and executes a .kc file
/autorestart: Toggle auto-restart (the interpreter will restart every time a group of code is run, off by default)
/restart: Restart the interpreter
/memdump: Print the contents of memory
/debug: Activates debug mode (the interpreter will print its memory, buffers, and pointers after each line is run)
/outputnumbers: Toggle showing the numerical value alongside the ascii one when using the << command (default off)
/toascii and /fromascii: Utilities that convert a number to ascii and a character from ascii.
      """)
    elif code == "/restart":
      print("==========INTERPRETER RESTART==========")
      interpreter.restart()
    elif code == "/memdump":
      print("Comparison buffer:", interpreter.comparisonBuffer)
      print("Memory dump:")
      pp.pprint(interpreter.memory)
    elif code == "/autorestart":
      autorestart = not autorestart
      print("Autorestart", autorestart)
    elif code == "/outputnumbers":
      outputnumbers = not outputnumbers
      interpreter.__outputnumbers__ = outputnumbers
      print("Output numbers:", outputnumbers)
    elif code == "/debug":
      debug = not debug
      print("Debug", debug)
    elif code == "/traceback":
      try:
        traceback.print_exception(None, interpreter.lastError[1], interpreter.lastError[2])
      except TypeError:
        print("No traceback available")
    elif code == "/exit":
      exit(0)
    elif code.startswith("/load"):
      name = " ".join(code.split(" ")[1:])
      try:
        kc = open(name)
      except FileNotFoundError:
        print("No such file:", name)
        continue
      except OSError as e:
        print("Error loading file \"", name, "\":", str(e))
        continue
      interpreter.fileName = " ".join(code.split(" ")[1:])
      program = kc.read()
      kc.close()
      interpreter.restart()
      print("=====INTERPRETER RESTART=====")
      try:
        run(program, interpreter, debug, False)
      except KeyboardInterrupt:
        print("Program terminated.")
      interpreter.fileName = "<shell>"
    elif code.startswith("/toascii"):
      try:
        print(ord("".join(code.split(" ")[1:])[0]))
      except:
        print("Error converting")
    elif code.startswith("/fromascii"):
      try:
        print(chr(int("".join(code.split(" ")[1:]))))
      except:
        print("Error converting")
    elif code.startswith("/"):
      print("Invalid command")
    else:
      try:
        run(code, interpreter, debug, autorestart)
      except KeyboardInterrupt:
        print("Program terminated.")

if __name__ == "__main__":
  repl()
