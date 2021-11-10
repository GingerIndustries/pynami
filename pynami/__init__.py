from .interpreter import Interpreter, prepare

"""
Pynami KonamiCode interpreter by GingerIndustries 2021

For details on how KonamiCode works and how to write in it, take a look at details.txt, or the included examples.
"""

def run(program):
  # Prepares and runs a program for you
  interpreter = Interpreter()
  interpreter.run(prepare(program))
