import helpers

# open file, collect content
le_filename = "../inputs/day_23_input.txt"
# le_file_content = helpers.get_file_content_raw(le_filename)
le_lines = helpers.get_file_content_as_lines(le_filename)
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
      conn_dict[dev1] = set()
    conn_dict[dev1].add(dev2)
    # if len(conn_dict[dev1]) > 1 :
      # groups_set.add(dev1)
    if dev2 not in conn_dict :
      conn_dict[dev2] = set()
    conn_dict[dev2].add(dev1)
    # if len(conn_dict[dev2]) > 1 :
      # groups_set.add(dev2)
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

def keep_groups_with_t(groups_dict) :
  groups_with_t = dict()
  for dev, neighbors in groups_dict.items() :
    for neighbor in neighbors :
      if neighbor[0] == "t" or dev[0] == "t" :
        groups_with_t[dev] = neighbors
        break
  return groups_with_t

def count_group_ts(groups_dict) :
  t_count_dict = dict()
  for dev, neighbors in groups_dict.items() :
    t_count_dict[dev] = [0, 1 + len(neighbors)]
    if dev[0] == "t" :
      t_count_dict[dev][0] = 1
    for neighbor in neighbors :
      if neighbor[0] == "t" :
        t_count_dict[dev][0] += 1
  return t_count_dict

def binomial_coef(k, n) :
  if not (0 <= k <= n) :
    return 0
  num = n
  denom = 1
  for i in range(1, k) :
    num *= (n-i)
    denom *= (i + 1)
  if (num % denom) != 0 :
    raise RuntimeError("Error : bad (k, n) computation !")
  else :
    return num//denom

def count_groups_of_3_with_t(t_count_dict) :
  sum = 0
  for t_count, group_size in t_count_dict.values() :
    if (group_size) >= 3 :
      for i in range(1, 1 + min(t_count, 3)) :
        binomial_t = binomial_coef(i, t_count)
        binomial_non_t = binomial_coef(3-i, group_size - t_count)
        sum += binomial_t * binomial_non_t
  return sum

cd = get_connections_dict(le_lines)
ga3 = get_groups_of_at_least_3(cd)
ta3 = keep_groups_with_t(ga3)
tc = count_group_ts(ga3)
g3c = count_groups_of_3_with_t(tc)
it = iter(tc)

######
# PART 2
######