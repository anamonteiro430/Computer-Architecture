"""CPU functionality."""

import sys

filename = sys.argv[1]

#CPU class - def load - load a program into memory
#Load - address = 0  ---> program counter, index of the current instruction
#     - program = array of bytes ---> MEMORY , RAM  -->   inside there's instructions


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.register = [0] * 8  #8 general-purpose register
        self.ram = [0] * 256 #256 bytes of memory
        self.pc = 0  #internal register

    
    def load(self):
        """Load a program into memory."""
        #Load program from examples - print8.ls8
        #no longer hardcoded!
        with open(filename) as f:
            address = 0
            for line in f:
                line = line.split("#")
                try:
                    value = int(line[0], 2)
                    self.ram_write(value, address)
                    address += 1
                except ValueError:
                    continue
                print(value)
        print("RAM", self.ram[:15])


        # For now, we've just hardcoded a program:

        ''' program = [
            # From print8.ls8
            0b10000010,  # LDI in R0 save 8  
            0b00000000,  #R0                 
            0b00001000,  #8
            0b01000111,  # PRN R0
            0b00000000,  #R0
            0b00000001,  # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1 '''


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()



    def ram_read(self, address):
        value = self.ram[address]
        return value

    def ram_write(self, value, address):
        self.ram[address] = value

    def run(self):
        """Run the CPU."""
        LDI = 0b10000010   #reg[0] = 8
        PRN = 0b01000111   #print(reg[0])
        MUL = 0b10100010 
        HLT = 0b00000001

        #self.pc --> index of current instruction
        #ir --> instruction register, the instruction at index pc

        running = True

        while running:
            ir = self.ram[self.pc]

            if ir == LDI:
                reg_num = self.ram_read(self.pc+1)
                value = self.ram_read(self.pc+2)
                self.register[reg_num] = value
                self.pc += 3 #3byte instruction

            elif ir == PRN:
                reg_num = self.ram_read(self.pc+1)
                print(self.register[reg_num])
                self.pc += 2 #2byte instruction

            elif ir == MUL:
                
                reg_num1 = self.ram[self.pc+1]
                reg_num2 = self.ram[self.pc+2]
                self.register[reg_num1] *= self.register[reg_num2]
                self.pc += 3

            elif ir == HLT:
                running = False
                self.pc += 1

            else:
                print(f'Unknown instruction {ir} at address {self.pc}')
                sys.exit(1)
    
