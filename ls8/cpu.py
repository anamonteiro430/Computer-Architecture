"""CPU functionality."""

import sys

filename = sys.argv[1]

#CPU class - def load - load a program into memory
#Load - address = 0  ---> program counter, index of the current instruction
#     - program = array of bytes ---> MEMORY , RAM  -->   inside there's instructions

LDI = 0b10000010   #reg[0] = 8
PRN = 0b01000111   #print(reg[0])
ADD = 0b10100000
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
HLT = 0b00000001

SP = 7
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.register = [0] * 8  #8 general-purpose register
        self.ram = [0] * 256 #256 bytes of memory
        self.pc = 0  #internal register
        self.SP = 7
        self.register[SP] = 0xF4
        self.branchtable = {}
        #load functions into branchtable
        self.branchtable[LDI] = self.LDI
        self.branchtable[PRN] = self.PRN
        self.branchtable[ADD] = self.ADD
        self.branchtable[MUL] = self.MUL
        self.branchtable[PUSH] = self.PUSH
        self.branchtable[POP] = self.POP
        self.branchtable[CALL] = self.CALL
        self.branchtable[RET] = self.RET
        self.branchtable[HLT] = self.HLT


    
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


    def LDI(self): #0b10000010
        print("LOAD")
        reg_num = self.ram_read(self.pc+1)
        value = self.ram_read(self.pc+2)
        self.register[reg_num] = value
        self.pc += 3 #3byte instruction
        print(self.register)

    def PRN(self):
        reg_num = self.ram_read(self.pc+1)
        print("PRINTING", self.register[reg_num])
        self.pc += 2 #2byte instruction

    def ADD(self):
        print("add")
        reg_num1 = self.ram[self.pc+1]
        reg_num2 = self.ram[self.pc+2]
        self.register[reg_num1] += self.register[reg_num2]
        self.pc += 3

    def MUL(self):
        reg_num1 = self.ram[self.pc+1]
        reg_num2 = self.ram[self.pc+2]
        self.register[reg_num1] *= self.register[reg_num2]
        self.pc += 3

    def PUSH(self): #Push the value in the given register on the stack.
        #decrement sp
        self.register[self.SP] -= 1
        #get the value we want to store from the register 
        reg_num = self.ram[self.pc + 1]
        #value is in register ith that number
        value = self.register[reg_num]
        #register 7 points to that address
        top_address = self.register[self.SP]
        #find it in ram and store the value there
        self.ram[top_address] = value
        #increment pc to next instruction
        self.pc += 2

    def POP(self):
        #find out the address of top of stack -- register[SP] points to ir
        top_address = self.register[self.SP]
        #the value is the number in ram at that address
        value = self.ram[top_address]
        #what's the register in the instruction
        reg_num = self.ram[self.pc + 1]
        #put the value in that register
        self.register[reg_num] = value
        #increment sp
        self.register[SP] += 1
        #increment pc to next instruction
        self.pc += 2

    def CALL(self): #contains a register operand
        #that register contains the address we want to jump to, address of a function
        #since CALL instruction takes two bytes to execute we want to access self.ram(pc + 2)
        print("calling")
        print("RAM", self.ram)
        print("REG,,", self.register)
        return_address = self.pc+2 #we're going to return here after
        #push it to the stack
        #decrement SP
        print("return address", return_address)
        self.register[self.SP] -= 1
        #check what's the top address:
        top_address = self.register[self.SP]
        print("top address", top_address)
        #find it in RAM and store the return_address there
        self.ram[top_address] = return_address
        print("RAM", self.ram)
        #get the register number from pc+1
        reg_num = self.ram[self.pc+1]
        print("reg number is", reg_num)
        #the address it's whatever is stored in that register number
        subroutine_address = self.register[reg_num]
        print("sub addr", subroutine_address)
        #call it
        self.pc = subroutine_address
        print("pc is", self.pc)

    def RET(self):
        #get the value from top of stack
        print("RET")
        top_address = self.register[self.SP]
        print("TOP", top_address)
        value = self.ram[top_address]
        self.pc = value

    def HLT(self):
        print("RAM is ", self.ram[:35])
        running = False
        sys.exit(0)
        

    def run(self):
        running = True
        
        while running:
            ir = self.ram_read(self.pc)

            if  ir in self.branchtable:
                self.branchtable[ir]()
                
            else:
                print((f'Unknown instruction: {ir}, at address PC: {self.pc}'))
                sys.exit(1)  
        
             

    ''' def run(self):
        """Run the CPU."""
        LDI = 0b10000010   #reg[0] = 8
        PRN = 0b01000111   #print(reg[0])
        MUL = 0b10100010 
        HLT = 0b00000001

        #initialize R7
        SP = 7
        register[SP] = 0xF4

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

            elif ir == PUSH:
                

            elif ir == HLT:
                running = False
                self.pc += 1

            else:
                print(f'Unknown instruction {ir} at address {self.pc}')
                sys.exit(1) '''


        