import helpers

# open file, collect content
le_filename = "../inputs/day_23_input.txt"
# le_file_content = helpers.get_file_content_raw(le_filename)
le_lines = helpers.get_file_content_as_lines(le_filename)
le_test_lines = helpers.raw_to_lines("""kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn""")
# le_char_table = helpers.get_file_content_as_table(le_filename)

######
# PART 1
######

def get_connections_dict(lines) :
  conn_dict = dict()
  # groups_set = set()
  for line in lines :
    dev1, dev2 = line.split("-")
    if dev1 not in conn_dict :
      conn_dict[dev1] = set({dev1})
    if dev2 not in conn_dict :
      conn_dict[dev2] = set({dev2})
    conn_dict[dev1].add(dev2)
    conn_dict[dev2].add(dev1)
  return conn_dict

def get_connections_dict_v2(lines) :
  """
  Computes connections dictionary (with duplicates)
  """
  conn_dict = dict()
  # groups_set = set()
  for line in lines :
    dev1, dev2 = line.split("-")
    conn_dict[dev1] = set()
    conn_dict[dev2] = set()
  for line in lines :
    dev1, dev2 = line.split("-")
    conn_dict[dev1].add(dev2)
    conn_dict[dev2].add(dev1)
  return conn_dict

def get_groups_of_at_least_3(conn_dict) :
  groups_set = dict()
  for dev, neighbors in conn_dict.items() :
    if len(neighbors) > 1 :
      first_of_group = True
      for neighbor in neighbors :
        if neighbor in groups_set :
          first_of_group = False
      if first_of_group :
        groups_set[dev] = conn_dict[dev]
  return groups_set

def get_groups_of_exactly_3(conn_dict) :
  groups_set = dict()
  for dev, neighbors in conn_dict.items() :
    if len(neighbors) == 2 :
      first_of_group = True
      for neighbor in neighbors :
        if neighbor in groups_set :
          first_of_group = False
      if first_of_group :
        groups_set[dev] = conn_dict[dev]
  return groups_set

def get_groups_of_exactly_3_v2(conn_dict) :
  """
  Retrieves all groups of exactly 3 interconnected devices (no duplicates, each group
  is only represented once in the dictionary)
  """
  groups_set = dict()
  processed_devs = set()
  for dev, neighbors in conn_dict.items() :
    groups_set[dev] = []
    processed_neighbors = set()
    for neighbor1 in neighbors :
      for neighbor2 in neighbors :
        if (neighbor2 not in processed_neighbors) and (neighbor2 != neighbor1)\
          and neighbor1 not in processed_devs and neighbor2 not in processed_devs : # avoid groups being represented twice
          if neighbor2 in conn_dict[neighbor1] :
            groups_set[dev].append({dev, neighbor1, neighbor2})
      processed_neighbors.add(neighbor1)
    processed_devs.add(dev)
  return groups_set

def keep_groups_with_t(groups_dict) :
  groups_with_t = dict()
  for dev, neighbors in groups_dict.items() :
    for neighbor in neighbors :
      if neighbor[0] == "t" or dev[0] == "t" :
        groups_with_t[dev] = neighbors
        break
  return groups_with_t

def keep_groups_with_t_v2(groups_dict) :
  groups_with_t = dict()
  for dev, neighbors_list in groups_dict.items() :
    if dev not in groups_with_t :
      groups_with_t[dev] = []
    for neighbors in neighbors_list :
      for neighbor in neighbors :
        if neighbor[0] == "t" :
          groups_with_t[dev].append(neighbors)
          break
  return groups_with_t

def get_t_count_dict(groups_dict) :
  t_count_dict = dict()
  for dev, neighbors in groups_dict.items() :
    t_count_dict[dev] = [0, 1 + len(neighbors)]
    if dev[0] == "t" :
      t_count_dict[dev][0] = 1
    for neighbor in neighbors :
      if neighbor[0] == "t" :
        t_count_dict[dev][0] += 1
  return t_count_dict

def get_t_count_dict_v2(groups_dict) :
  t_count_dict = dict()
  for dev, neighbors_list in groups_dict.items() :
    t_count_dict[dev] = len(neighbors_list)
  return t_count_dict

def binomial_coef(k, n) :
  if not (0 <= k <= n) :
    return 0
  num = 1
  denom = 1
  for i in range(0, k) :
    num *= (n-i)
    denom *= (i + 1)
  if (num % denom) != 0 :
    raise RuntimeError("Error : bad (k, n) computation !")
  else :
    return num//denom

def count_g3_from_tc(t_count, group_size) :
  if (group_size) >= 3 :
      sum = 0  
      for i in range(1, 4) :
        binomial_t = binomial_coef(i, t_count)
        binomial_non_t = binomial_coef(3-i, group_size - t_count)
        sum += (binomial_t * binomial_non_t)
      assert(binomial_coef(3, group_size) - binomial_coef(3, group_size - t_count) == sum)
  return sum

def count_groups_of_3_with_t(t_count_dict) :
  sum = 0
  for t_count, group_size in t_count_dict.values() :
    if (group_size) >= 3 :
      temp_sum = count_g3_from_tc(t_count, group_size)
      sum += temp_sum
  return sum

def count_groups_of_3_with_t_v2(t_count_dict) :
  sum = 0
  for t_count in t_count_dict.values() :
    sum += t_count
  return sum

# cd = get_connections_dict(le_lines)
# cd = get_connections_dict(le_test_lines)
# ga3 = get_groups_of_at_least_3(cd)
# ta3 = keep_groups_with_t(ga3)
# tc = get_t_count_dict(ta3)
# g3c = count_groups_of_3_with_t(tc)
# it = iter(tc)

cd = get_connections_dict_v2(le_lines)
# cd = get_connections_dict_v2(le_test_lines)
g3 = get_groups_of_exactly_3_v2(cd)
t3 = keep_groups_with_t_v2(g3)
tc = get_t_count_dict_v2(t3)
g3c = count_groups_of_3_with_t_v2(tc)
it = iter(tc)

helpers.print_log_entries("Number of groups of three inter-connected"
                          "computers with at least one potential Chief Historian :"
                          , g3c, log_cats = {"R"})

######
# PART 2
######

