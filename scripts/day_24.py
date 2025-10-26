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

max_bit_pos = 0


def parse_initial_inputs_str(input_nodes_str):
  global max_bit_pos
  initial_inputs = dict()
  for line in input_nodes_str:
    key, val_str = line.split(": ")
    bit_pos = int(key[1:])
    max_bit_pos = max(max_bit_pos, bit_pos)
    initial_inputs[key] = int(val_str)
  return initial_inputs


def parse_gate_connections_str(gate_connections_str):
  gate_connections = dict()
  for line in gate_connections_str:
    inputs, output = line.split(" -> ")
    operand_a, operator, operand_b = inputs.split(" ")
    gate_connections[output] = (operator, operand_a, operand_b)
  return gate_connections


le_input_nodes = parse_initial_inputs_str(le_initial_inputs_str)
le_gate_connections = parse_gate_connections_str(le_gate_connections_str)


def simulate_logic(input_nodes, gate_connections):
  if type(input_nodes) != dict or type(gate_connections) != dict:
    raise RuntimeError("simulate_logic() error : bad arguments !")
  unprocessed_nodes = set(gate_connections.keys())
  processed_nodes = input_nodes.copy()
  while len(unprocessed_nodes) > 0:
    for out in unprocessed_nodes.copy():
      oper, op_a_key, op_b_key = gate_connections[out]
      if op_a_key in processed_nodes and op_b_key in processed_nodes:
        op_a = processed_nodes[op_a_key]
        op_b = processed_nodes[op_b_key]
        if oper == "AND":
          processed_nodes[out] = op_a & op_b
        elif oper == "OR":
          processed_nodes[out] = op_a | op_b
        elif oper == "XOR":
          processed_nodes[out] = op_a ^ op_b
        else:
          raise RuntimeError(
              "simulate_logic() error : bad operator ! ({})".format(oper)
          )
        unprocessed_nodes.discard(out)
  return processed_nodes


def get_decimal(processed_nodes):
  res = 0
  for node, value in processed_nodes.items():
    if node[0] == "z":
      n = int(node[1:])
      res += int(value) << n
  return res


le_processed_nodes = simulate_logic(le_input_nodes, le_gate_connections)
le_decimal = get_decimal(le_processed_nodes)

helpers.set_log_by_parts()

helpers.print_log_entries(
  "Resulting decimal :", le_decimal, log_cats={"R", "P1"})

######
# PART 2
######


def get_wire_name(prefix, n):
  if n < 0:
    raise RuntimeError("get_input_name() error : n should be >= 0 !")
  if n < 10:
    return prefix + "0" + str(n)
  elif n < 99:
    return prefix + str(n)
  else:
    raise RuntimeError("get_input_name() error : n > 99 !")


def generate_zeroed_input(max):
  input_nodes = dict()
  for j in range(max):
    x_input_name = get_wire_name("x", j)
    y_input_name = get_wire_name("y", j)
    input_nodes[x_input_name] = 0
    input_nodes[y_input_name] = 0
  return input_nodes


def fuzzing_test_v1(input_type, gate_connections, max_input_nbr=45):
  bad_inputs = set()
  for i in range(max_input_nbr):
    bad_input_name = get_wire_name(input_type, i)
    z_output_name = get_wire_name("z", i)
    input_nodes = generate_zeroed_input(max_input_nbr)
    input_nodes[bad_input_name] = 1
    curr_test_nodes = simulate_logic(input_nodes, gate_connections)
    if curr_test_nodes[z_output_name] != 1:
      bad_inputs.add(i)
  return bad_inputs


# def fuzzing_test_v2(input_type, gate_connections, max_input_nbr=45):
#   bad_inputs = set()
#   for i in range(max_input_nbr):
#     z_output_name = get_wire_name("z", i + 1)
#     x_bad_input_name = get_wire_name("x", i)
#     y_bad_input_name = get_wire_name("y", i)
#     input_nodes = generate_zeroed_input(max_input_nbr)
#     input_nodes[x_bad_input_name] = 1
#     input_nodes[y_bad_input_name] = 1
#     curr_test_nodes = simulate_logic(input_nodes, gate_connections)
#     if curr_test_nodes[z_output_name] != 1:
#       bad_inputs.add(i)
#   return bad_inputs


def fuzzing_test_v3(gate_connections, max_input_nbr=45):
  bad_inputs = set()
  for i in range(max_input_nbr - 1):
    z_output_name = get_wire_name("z", i + 2)
    x_bad_input_name = get_wire_name("x", i)
    x_bad_input_name_2 = get_wire_name("x", i + 1)
    y_bad_input_name = get_wire_name("y", i)
    input_nodes = generate_zeroed_input(max_input_nbr)
    input_nodes[x_bad_input_name] = 1
    input_nodes[y_bad_input_name] = 1
    input_nodes[x_bad_input_name_2] = 1
    curr_test_nodes = simulate_logic(input_nodes, gate_connections)
    if curr_test_nodes[z_output_name] != 1:
      bad_inputs.add(i)
  return bad_inputs


le_x_candidates_v1 = fuzzing_test_v1("x", le_gate_connections, 45)
le_xy_candidates_v3 = fuzzing_test_v3(le_gate_connections, 45)
le_candidates = le_x_candidates_v1 | le_xy_candidates_v3

helpers.print_log_entries("[Approach 1] Candidates :",
                          le_candidates, log_cats={"I", "P1"})

# Structure of logic gates :
# X_N XOR Y_N --> r_n
# X_N AND Y_N --> a_n
# CARRY_(N-1) XOR r_n --> z_n
# CARRY_(N-1) AND r_n --> b_n
# a_n OR b_n --> carry_n

# INPUTS : X, Y, AA[-1], CARRY[-1]
# OUTPUTS : R, Z, AA


def find_miscategorized_outputs(gate_connections):
  """
  Assuming the following gate connections exist - and only them - for each
  bit, with maybe the exception of the 0-th bit :
  x_n XOR y_n --> r_n
  x_n AND y_n --> a_n
  carry_(n-1) XOR r_n --> z_n
  carry_(n-1) AND r_n --> b_n
  a_n OR b_n --> carry_n

  (actual names for variables of types x/y/z is different in input, this is only
  a representation, and the underscore is also not present in the problem input)
  """

  # format for `possibilties` :
  # {cat : (XOR_count, AND_count, OR_count)}
  # With cat in ("r", "a", "z", "b", "c") and the count's counting how many times
  # a variable of each category is supposed to be used as an operand with the
  # corresponding operator
  out_possibilities = {
      "r": (1, 1, 0),
      "a": (0, 0, 1),
      "z": (0, 0, 0),
      "b": (0, 0, 1),
      "c": (1, 1, 0),
  }
  miscategorized = set()
  involvements = dict()
  # First, fill dictionary with zeroed-out values
  for output, (oper, op_a, op_b) in gate_connections.items():
    if {op_a, op_b} == {"x00", "y00"}:
      if (output, oper) == ("z00", "XOR"):
        involvements[output] = {
            "name": "z00",
            "XOR": 0,
            "AND": 0,
            "OR": 0,
        }
      elif oper == "AND":
        involvements[output] = {
            "name": "c00",
            "XOR": 0,
            "AND": 0,
            "OR": 0,
        }
      else:
        raise RuntimeWarning(
            "find_involvements() error : unknown case encountered !"
          )
    elif op_a[0] in ("x", "y"):
      bit_pos = int(op_a[1:])
      if oper == "XOR":
        involvements[output] = {
            "name": get_wire_name("r", bit_pos),
            "XOR": 0,
            "AND": 0,
            "OR": 0,
        }
      elif oper == "AND":
        involvements[output] = {
            "name": get_wire_name("a", bit_pos),
            "XOR": 0,
            "AND": 0,
            "OR": 0,
        }
    else:
      if oper == "XOR":
        involvements[output] = {
            "name": "z?",
            "XOR": 0,
            "AND": 0,
            "OR": 0,
        }
      elif oper == "AND":
        involvements[output] = {
            "name": "b?",
            "XOR": 0,
            "AND": 0,
            "OR": 0,
        }
      elif oper == "OR":
        involvements[output] = {
            "name": "c?",
            "XOR": 0,
            "AND": 0,
            "OR": 0,
        }
  #
  # Now, update dictionary
  for output, (oper, op_a, op_b) in gate_connections.items():
    # 5 cases (c.f. above)
    if op_a[0] in ("x", "y"):
      pass
    else:
      involvements[op_a][oper] += 1
      involvements[op_b][oper] += 1
  #
  # Finally, check produced dictionary
  for output, val in involvements.items():
    name, x_c, a_c, o_c = val["name"], val["XOR"], val["AND"], val["OR"]
    cat = name[0]
    if out_possibilities[cat] != (x_c, a_c, o_c):
      miscategorized.add((output, name))
    else:
      helpers.print_log_entries(
        "Good (out, val) pair : ({}, {})".format(output, val), log_cats={"D"})
  return miscategorized


# helpers.LOG_DICT["D"][0] = True

le_mis = find_miscategorized_outputs(le_gate_connections)
le_mis = {e for e in le_mis if e[0] != get_wire_name("z", max_bit_pos + 1)}

if len(le_mis) != 8:
  raise RuntimeWarning(
    "Warning : couldn't find all swapped wires in miscategorized wires !"
    "\n(i.e. some wires were swapped with other wires of the same categories)")

helpers.print_log_entries(
  "[Approach 2] Miscategorized outputs :", le_mis, log_cats={"R", "P2"})
helpers.print_log_entries("[PART 2 - Approach 2] Resulting string :", ",".join(
  sorted([e[0] for e in le_mis])), log_cats={"R", "P2"})
