import click

class BrainFuck:
    def __init__(self, content):
        self.content = content
        self.memory = self.makeMemory()
        self.pos = 0
        self.pointer = 0
        self.programLenght = len(self.content)
        self.interpreter()

    def getMemory(self):
        return self.memory

    def makeMemory(self):
        list = []
        for i in range(30000):
            list.append(0)
        return list

    def internalInterpreter(self, content):
        pos = 0
        programLenght = len(content)
        while pos < programLenght:
            if content[pos] == ' ' or content[pos] == '\n' or content[pos] == '\t':
                pos += 1
            elif content[pos] == '+':
                self.memory[self.pointer] += 1
                pos += 1
            elif content[pos] == '-':
                self.memory[self.pointer] = 0 if self.memory[self.pointer] <= 0 else self.memory[self.pointer] - 1
                pos += 1
            elif content[pos] == '>':
                self.pointer += 1
                try:
                    self.memory[self.pos]
                except:
                    raise Exception('You exceded the memory limit. No more blocks availables')
                pos += 1
            elif content[pos] == '<':
                self.pointer -= 0 if self.pointer <= 0 else self.pointer-1
                pos += 1
            elif content[pos] == ',':
                char = input('Enter ASCII: ')

                try:
                    char.index('.')
                except:
                    try:
                        char = int(char)
                    except:
                        raise Exception('Error: You must enter ASCII, not string')
                else:
                    raise Exception('Error: You must enter ASCII, not float.')

                self.memory[self.pointer] = int(char)
                pos += 1
            elif content[pos] == '.':
                print(chr(self.memory[self.pointer]))
                pos += 1
            elif content[pos] == '[':
                self.loop(content)
                pos += 1
            else:
                pos += 1

    def interpreter(self):
        while self.pos < self.programLenght:
            if self.content[self.pos] == ' ' or self.content[self.pos] == '\n' or self.content[self.pos] == '\t':
                self.pos += 1
            elif self.content[self.pos] == '+':
                self.memory[self.pointer] += 1
                self.pos += 1
            elif self.content[self.pos] == '-':
                self.memory[self.pointer] = 0 if self.memory[self.pointer] <= 0 else self.memory[self.pointer] - 1
                self.pos += 1
            elif self.content[self.pos] == '>':
                self.pointer += 1
                self.pos += 1
            elif self.content[self.pos] == '<':
                self.pointer -= 0 if self.pointer <= 0 else self.pointer - 1
                self.pos += 1
            elif self.content[self.pos] == ',':
                char = input('Enter ASCII: ')

                try:
                    char.index('.')
                except:
                    try:
                        char = int(char)
                    except:
                        raise Exception('Error: You must enter ASCII, not string')
                else:
                    raise Exception('Error: You must enter ASCII, not float.')

                self.memory[self.pointer] = int(char)
                self.pos += 1
            elif self.content[self.pos] == '.':
                print(chr(self.memory[self.pointer]))
                self.pos += 1
            elif self.content[self.pos] == '[':
                self.loop(self.content)
                self.pos += 1
            else:
                self.pos += 1

    def loop(self, content):
        programLenght = len(content)
        loopStart = self.pos+1
        loopEnd = loopStart
        found = False
        while loopEnd < programLenght and content[loopEnd] != ']':
            loopEnd += 1

        if loopEnd < programLenght and content[loopEnd] == ']':
            pass
        else:
            raise SyntaxError('Expected \"]\" at the end of the loop. Not found')
        tmpContent = content[loopStart]

        while self.memory[self.pointer] != 0:
            self.internalInterpreter(tmpContent)
        self.pos = loopEnd

class BrainFuckInterpreter:
    def __init__(self, content):
        self.content = content
        self.memory = self.makeMemory()
        self.pos = 0
        self.pointer = 0
        self.programLenght = len(self.content)
        self.output = []

    def getMemory(self):
        return self.memory

    def makeMemory(self):
        list = []
        for i in range(30000):
            list.append(0)
        return list

    def internalInterpreter(self, content):
        pos = 0
        programLenght = len(content)
        while pos < programLenght:
            if content[pos] == ' ' or content[pos] == '\n' or content[pos] == '\t':
                pos += 1
            elif content[pos] == '+':
                self.memory[self.pointer] += 1
                pos += 1
            elif content[pos] == '-':
                self.memory[self.pointer] = 0 if self.memory[self.pointer] <= 0 else self.memory[self.pointer] - 1
                pos += 1
            elif content[pos] == '>':
                self.pointer += 1
                try:
                    self.memory[self.pos]
                except:
                    raise Exception('You exceded the memory limit. No more blocks availables')
                pos += 1
            elif content[pos] == '<':
                self.pointer -= 0 if self.pointer <= 0 else self.pointer-1
                pos += 1
            elif content[pos] == ',':
                char = input('Enter ASCII: ')

                try:
                    char.index('.')
                except:
                    try:
                        char = int(char)
                    except:
                        raise Exception('Error: You must enter ASCII, not string')
                else:
                    raise Exception('Error: You must enter ASCII, not float.')

                self.memory[self.pointer] = int(char)
                pos += 1
            elif content[pos] == '.':
                self.output.append(chr(self.memory[self.pointer]))
                pos += 1
            elif content[pos] == '[':
                self.loop(content)
                pos += 1
            else:
                pos += 1

    def interpreter(self):
        while self.pos < self.programLenght:
            if self.content[self.pos] == ' ' or self.content[self.pos] == '\n' or self.content[self.pos] == '\t':
                self.pos += 1
            elif self.content[self.pos] == '+':
                self.memory[self.pointer] += 1
                self.pos += 1
            elif self.content[self.pos] == '-':
                self.memory[self.pointer] = 0 if self.memory[self.pointer] <= 0 else self.memory[self.pointer] - 1
                self.pos += 1
            elif self.content[self.pos] == '>':
                self.pointer += 1
                self.pos += 1
            elif self.content[self.pos] == '<':
                self.pointer -= 0 if self.pointer <= 0 else self.pointer - 1
                self.pos += 1
            elif self.content[self.pos] == ',':
                char = input('Enter ASCII: ')

                try:
                    char.index('.')
                except:
                    try:
                        char = int(char)
                    except:
                        raise Exception('Error: You must enter ASCII, not string')
                else:
                    raise Exception('Error: You must enter ASCII, not float.')

                self.memory[self.pointer] = int(char)
                self.pos += 1
            elif self.content[self.pos] == '.':

                self.output.append(chr(self.memory[self.pointer]))
                self.pos += 1
            elif self.content[self.pos] == '[':
                self.loop(self.content)
                self.pos += 1
            else:
                self.pos += 1
        return self.output

    def loop(self, content):
        programLenght = len(content)
        loopStart = self.pos+1
        loopEnd = loopStart
        found = False
        while loopEnd < programLenght and content[loopEnd] != ']':
            loopEnd += 1

        if loopEnd < programLenght and content[loopEnd] == ']':
            pass
        else:
            raise SyntaxError('Expected \"]\" at the end of the loop. Not found')
        tmpContent = content[loopStart]

        while self.memory[self.pointer] != 0:
            self.internalInterpreter(tmpContent)
        self.pos = loopEnd

@click.command()
@click.option('--filename', '-f', help='Path of the BRainFuck file you want to run', required=True)
@click.option('--memory', '-m', help='Enter true if you want to see the memory after program execution', required=False)
def run(filename, memory=False):
    file = open(filename, 'r')
    content = file.read()
    br = BrainFuck(content)
    if memory:
        print(br.getMemory())

def interpreter(code):
    brf = BrainFuckInterpreter(code)
    return brf.interpreter()