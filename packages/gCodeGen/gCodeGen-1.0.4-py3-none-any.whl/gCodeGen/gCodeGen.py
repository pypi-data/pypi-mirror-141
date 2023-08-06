import sys
from antlr4 import *
from .agCodeLexer import agCodeLexer
from .agCodeParser import agCodeParser
from .Collector import Collector

def run(input, outputFile=True):
    lexer = agCodeLexer(input)
    stream = CommonTokenStream(lexer)
    parser = agCodeParser(stream)
    tree = parser.prog()

    collector = Collector(doLog=False)
    gCode = collector.visit(tree)

    if outputFile:
        output = open("Output.cnc", "w")
        print(f'Generated G-Code to file: \'Output.cnc\'.')
        output.write(gCode)
        output.close()
    else:
        print(gCode)


def generate(file):
    run(FileStream(file), True)
    

def shell():
    print("###################### PyGcode REPL######################")
    print("Press CTRL+Z (on windows), CTRL+D (on linux) to evaluate")
    lines = []
    while(True):
        try:
            line = input("> ")
            lines.append(line)
        except EOFError:
            prog = '\n'.join(lines)
            run(InputStream(prog), False)
            break


if __name__ == "__main__":
    generate(sys.argv)
