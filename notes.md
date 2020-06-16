import sys

#I can ignore asm directory, interrupts, stretch 
#TODO, figure out what each file does
#ls8, FAq, spec
#Day 1 - implement 3 instructions
#READ ME in ls8
#ls8 examples, programs that my emulator will be able to run

#Computer emulator
''' project for the week. - limited by memory
Software that pretends to be hardware
At the end of the week it's going to be turing complete it can solve any problem for which there is na algorithm
 '''
#Memory is like a big array and the index into #the memory array is the address or pointer

memory = [0] * 256 #RAM

PRINT_BEEJ = 1
HALT = 2
SAVE_REG = 3   #SAVE_REG R1, 37   r1 = 37  register[1] = 37
PRINT_REG = 4  #PRINT_REG R1   print(register[1])
ADD = 5

#we have to encode the instruction

memory = [
     SAVE_REG,   #SAVE_REG R1, 37  instruction 3 bytes long
     1,  # <--- index into the register array
     99, # <--- value we want to store in there
     SAVE_REG,   #PRINT_REG R1 instruction  2bytes
     2,
     11,
     ADD,  #ADD R1, R2  register[1]+=register[2]
     1,
     2,
     PRINT_REG,
     1,
     PRINT_BEEJ,
     HALT
]

register = [0] * 8 # 8 registers, like variables
#they are in hardware, we can't make more of them without adding hardware  - general purpose register

pc = 0 #program counter, index of the current instruction
running = True

while running:
     ir = memory[pc] #Instruction register

     if ir == PRINT_BEEJ:
          print("Beej!")
          pc += 1
     elif ir == SAVE_REG:
          reg_num = memory[pc + 1]
          value = memory[pc + 2]
          register[reg_num] = value
          pc += 3

     elif ir == PRINT_REG:
          reg_num = memory[pc+1]
          print(register[reg_num])
          pc += 2
     
     elif ir == ADD:
          reg_num1 = memory[pc+1]
          reg_num2 = memory[pc + 2]
          register[reg_num1] += register[reg_num2]
          pc += 3

     elif ir == HALT:
          running = False
          pc += 1

     else:
          print(f'Unknown instruction {ir} at address {pc}')
          sys.exit(1)

 

#Objective - how a CPU functions at a low level
#Emulator - LS-8 - 8bit memory addressing

#only 8 wires available for addresses - where something is in memory , computations and instructions

#With 8 bits - CPU has a total of 256 bytes - can only compute values up to 255

#FIRST
#Execute code that stores the value 8 in a register then prints out:

# print8.ls8: Print the number 8 on the screen

''' 
10000010 # LDI R0,8  #machine code value of thhe instruction -- opcode --
00000000
00001000
01000111 # PRN R0
00000000
00000001 # HLT 
'''

#one of the opcode arguments (eg. `00000000` for R0 or `00001000` for the value `8`) -- operands --

#Implementation of 3 instructions
'''
`LDI` -- load immediate, store a value in a register or "set this register to this value"
`PRN` -- a pseudo instruction that print the numeric value stored in a register
`HLT` -- halt the CPU and exit the emulator
'''


##STEP 0 : inventory what is in ls8.py
# make a list of files
     #examples directory
     #cpu.py
     #ls8.py
     #README 
# write short descriptions of each file
     #programs to run on the emulator
     #
# what has been implemented and not
# skim spec

#SPECS LS 8

#REGISTERS

#INTERNAL REGISTERS

#FLAGS

#MEMORY

#STACK

#INTERRUPTS



