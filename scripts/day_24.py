import helpers

# open file, collect content
le_filename = "../inputs/day_24_input.txt"
le_file_content = helpers.get_file_content_raw(le_filename)
# le_lines = helpers.get_file_content_as_lines(le_filename)
# le_char_table = helpers.get_file_content_as_table(le_filename)
le_test_content = """x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj"""

######
# PART 1
######

le_input_node_raw, le_gate_connections_raw = le_file_content.split("\n\n")
# le_initial_inputs_raw, le_gate_connections_raw = le_test_content.split("\n\n")

le_initial_inputs_str = helpers.raw_to_lines(le_input_node_raw)
le_gate_connections_str = helpers.raw_to_lines(le_gate_connections_raw)

def parse_initial_inputs_str (input_nodes_str) :
  initial_inputs = dict()
  for line in input_nodes_str :
    key, val_str = line.split(": ")
    initial_inputs[key] = int(val_str)
  return initial_inputs

def parse_gate_connections_str (gate_connections_str) :
  gate_connections = dict()
  for line in gate_connections_str :
    inputs, output = line.split(" -> ")
    operand_a, operator, operand_b = inputs.split(" ")
    gate_connections[output] = (operator, operand_a, operand_b)
  return gate_connections

le_input_nodes = parse_initial_inputs_str(le_initial_inputs_str)
le_gate_connections = parse_gate_connections_str(le_gate_connections_str)

def simulate_logic (input_nodes, gate_connections) :
  if type(input_nodes) != dict or type(gate_connections) != dict :
    raise RuntimeError("simulate_logic() error : bad arguments !")
  unprocessed_nodes = set(gate_connections.keys())
  processed_nodes = input_nodes.copy()
  while len(unprocessed_nodes) > 0 :
    for out in unprocessed_nodes.copy() :
      oper, op_a_key, op_b_key = gate_connections[out]
      if op_a_key in processed_nodes and op_b_key in processed_nodes :
        op_a = processed_nodes[op_a_key]
        op_b = processed_nodes[op_b_key]
        if oper == "AND" :
          processed_nodes[out] = (op_a & op_b)
        elif oper == "OR" :
          processed_nodes[out] = (op_a | op_b)
        elif oper == "XOR" :
          processed_nodes[out] = (op_a ^ op_b)
        else :
          raise RuntimeError("simulate_logic() error : bad operator ! ({})".format(oper))
        unprocessed_nodes.discard(out)
  return processed_nodes

def get_decimal (processed_nodes) :
  res = 0
  for node, value in processed_nodes.items() :
    if node[0] == 'z' :
      n = int(node[1:])
      res += (int(value) << n)
  return res

le_processed_nodes = simulate_logic(le_input_nodes, le_gate_connections)
le_decimal = get_decimal(le_processed_nodes)

######
# PART 2
######

