import sys
from antlr4 import *
from .agCodeLexer import agCodeLexer
from .agCodeParser import agCodeParser
from .Collector import Collector

def run(input, outputFile=None):
    lexer = agCodeLexer(input)
    stream = CommonTokenStream(lexer)
    parser = agCodeParser(stream)
    tree = parser.prog()

    collector = Collector(doLog=False)
    gCode = collector.visit(tree)

    if outputFile is not None:
        output = open(outputFile, "w")
        print(f'Generated G-Code to file: \'{outputFile}\'.')
        output.write(gCode)
        output.close()
    else:
        print(gCode)


def generate(inputFile, outputFile):
    run(FileStream(inputFile), outputFile)
    

def shell():
    print("###################### gCodeGen REPL ######################")
    print("Press CTRL+Z (on windows), CTRL+D (on linux) to evaluate")
    lines = []
    while(True):
        try:
            line = input("> ")
            lines.append(line)
        except EOFError:
            prog = '\n'.join(lines)
            run(InputStream(prog))
            break


if __name__ == "__main__":
    generate(sys.argv)
