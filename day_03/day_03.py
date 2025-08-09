import re

# open file, collect content
le_filename = "day_03_input.txt"
le_file = open(le_filename, "r")
le_file_content = le_file.read()

# print("File content :\n", le_file_content, sep="") # [debugging]

######
# PART 1
######

mul_instruct_regex = """mul\([0-9]{1,3},[0-9]{1,3}\)"""

def process_mul_instruction(mul_instruct) :
    if (re.search("^" + mul_instruct_regex + "$", mul_instruct) == None) :
        return None
    # strip string of "mul(" at beginning and ")" at the end, them split around comma
    operands = [int(operand_str) for operand_str in mul_instruct[4:-1].split(",")]
    return operands[0] * operands[1]

sum = 0
for m in re.findall(mul_instruct_regex, le_file_content) :
    # print("First match :", m) # [debugging]
    sum += process_mul_instruction(m)

print("Found total sum of :\n", sum, sep = "")

######
# PART 2
######


def process_enabled_mul_instructions(raw_text) :
    # first, strip text of irrelevant characters, and make it more easy to process
    useful_text = "do()" + "".join(re.findall(mul_instruct_regex + "|do\\(\\)|don't\\(\\)", raw_text))
    # print("Useful text :\n", useful_text, sep = "") # [debugging]
    useful_text = useful_text.replace("don't()", "N")
    useful_text = useful_text.replace("do()", "Y")
    # print("Useful text after replacing :\n", useful_text, sep = "") # [debugging]
    # Now that we've re-formatted the text, we can define a new regex for the enabled mul instructions
    enabled_mul_instructs_regex = "(Y)" + "(" + mul_instruct_regex + ")+"
    enabled_mul_instructs_regex = r"Y(?:%s)+" % mul_instruct_regex
    sum = 0
    for mul_instructs in re.findall(enabled_mul_instructs_regex, useful_text) :
        # print("mul_instructs :\n", mul_instructs, sep="")# [debugging]
        for mul_instr in re.findall(mul_instruct_regex, mul_instructs) :
            # print("mul_instr :\n", mul_instr, sep = "") # [debugging]
            sum += process_mul_instruction(mul_instr)
    return sum

# test_text_1 = """
# mul(3,4)gjkljkljdfs
# don't()mul(4,4)gfdgdk
# do()mul(5,5)
# do()don't()mul(5,5)
# """
# test_text_2 = """
# mul(1,2)mul(1,1)mul(3,4)gjkljkljdfs
# don't()mul(4,4)gfdgdk
# do()do()mul(5,5)mul(5,25)mul(1,500)
# do()don't()mul(5,5)
# do()don't()lskgklj do()dklgjklsfjgmul(5,5)
# """
# print("Found \"enabled\" sum of :\n", process_enabled_mul_instructions(test_text_1), sep = "") # Just testing out stuff
# print("Found \"enabled\" sum of :\n", process_enabled_mul_instructions(test_text_2), sep = "") # Just testing out stuff

enabled_sum = process_enabled_mul_instructions(le_file_content)

print("Found \"enabled\" sum of :\n", enabled_sum, sep = "")