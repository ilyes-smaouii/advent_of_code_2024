#include <algorithm>
#include <array>
#include <cassert>
#include <cstddef>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <format>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <type_traits>
#include <unordered_map>
#include <unordered_set>
#include <vector>

using strings_vec_t = std::vector<std::string>;

strings_vec_t fileToLines(const std::string &filename) {
  strings_vec_t res_vec{};
  std::ifstream file;
  file.open(filename);
  std::string curr_line;
  while (std::getline(file, curr_line)) {
    res_vec.push_back(curr_line);
  }
  return res_vec;
}

std::uint32_t nextSecret(std::uint32_t secret) {
  constexpr std::uint32_t MD_MASK = (1 << 24) - 1;
  secret = (secret << 6) ^ secret;
  secret &= MD_MASK;
  secret = (secret >> 5) ^ secret;
  secret &= MD_MASK;
  secret = (secret << 11) ^ secret;
  secret &= MD_MASK;
  return secret;
}

std::uint32_t getNthSecret(std::uint32_t secret_nbr_0, std::size_t n) {
  for (std::size_t i{0}; i < n; i++) {
    secret_nbr_0 = nextSecret(secret_nbr_0);
  }
  return secret_nbr_0;
}

std::uint64_t getSumOf2000thNumbers(const strings_vec_t &lines) {
  std::uint64_t sum{0};
  for (const auto &line : lines) {
    auto s_0 = std::stol(line); // std::stol rather than std::stoi so it's
    // always at least 32 bits wide
    sum += getNthSecret(s_0, 2000);
  }
  return sum;
}

std::array<std::uint32_t, 2001>
get2000NextSecrets_v5(std::uint32_t initial_secret) {
  std::array<std::uint32_t, 2001> secrets_array{};
  secrets_array[0] = initial_secret;
  for (std::size_t i{0}; i < 2000; i++) {
    // initial_secret = nextSecret(initial_secret);
    // secrets_array[i + 1] = initial_secret;
    secrets_array[i + 1] = nextSecret(secrets_array[i]);
  }
  // return secrets_array;
  return secrets_array;
}

std::array<std::uint8_t, 2001>
secretsToPrices_v5(const std::array<std::uint32_t, 2001> &secrets_array) {
  std::array<std::uint8_t, 2001> prices_array{};
  for (std::size_t i{0}; i < 2001; i++) {
    prices_array[i] = secrets_array[i] % 10;
  }
  return prices_array;
}

std::array<std::uint8_t, 2001> get2000Prices_v5(std::uint32_t initial_secret) {
  auto secrets_array = get2000NextSecrets_v5(initial_secret);
  return secretsToPrices_v5(secrets_array);
}

std::array<std::int8_t, 2000>
pricesToPriceChanges_v5(const std::array<std::uint8_t, 2001> &prices_array) {
  std::array<std::int8_t, 2000> changes_array{};
  for (std::size_t i{0}; i < changes_array.size(); i++) {
    changes_array.at(i) = static_cast<std::int8_t>(prices_array.at(i + 1)) -
                          static_cast<std::int8_t>(prices_array.at(i));
  }
  return changes_array;
}

std::vector<std::array<std::uint8_t, 2001>>
getPricesTable_v5(const strings_vec_t &lines) {
  std::vector<std::array<std::uint8_t, 2001>> res_table{};
  for (const auto &line : lines) {
    auto initial_secret = static_cast<std::uint32_t>(std::stoi(line));
    auto prices_array = get2000Prices_v5(initial_secret);
    res_table.push_back(prices_array);
  }
  return res_table;
}

std::vector<std::array<std::int8_t, 2000>> getChangesTable_v5(
    const std::vector<std::array<std::uint8_t, 2001>> &prices_table) {
  std::vector<std::array<std::int8_t, 2000>> changes_table{};
  for (const auto &prices_array : prices_table) {
    changes_table.push_back(pricesToPriceChanges_v5(prices_array));
  }
  return changes_table;
}

using neg_t = std::array<std::int8_t, 4>;

struct neg_hash {
  std::size_t operator()(const neg_t &neg_array) const {
    std::size_t v1{
        std::hash<std::size_t>()(static_cast<std::size_t>(neg_array.at(0)))},
        v2{std::hash<std::size_t>()(static_cast<std::size_t>(neg_array.at(1)))},
        v3{std::hash<std::size_t>()(static_cast<std::size_t>(neg_array.at(2)))},
        v4{std::hash<std::size_t>()(static_cast<std::size_t>(neg_array.at(3)))};
    std::size_t res = v1;
    res = res ^ v2 + 0x9e3779b9 + (res << 6) + (res >> 2);
    res = res ^ v3 + 0x9e3779b9 + (res << 6) + (res >> 2);
    res = res ^ v4 + 0x9e3779b9 + (res << 6) + (res >> 2);
    return res;
  }
};

std::uint64_t findMaxRevenue_v5(
    const std::vector<std::array<std::uint8_t, 2001>> &prices_table) {
  auto prices_changes_table = getChangesTable_v5(prices_table);

  std::unordered_map<neg_t, std::uint64_t, neg_hash> neg_map{};

  // First, fill neg_values with 0's
  std::size_t iter_count{0};
  neg_t neg_array{};
  std::int8_t &it_0{neg_array.at(0)}, &it_1{neg_array.at(1)},
      &it_2{neg_array.at(2)}, &it_3{neg_array.at(3)};
  for (it_0 = -9; it_0 < 10; it_0++) {
    for (it_1 = -9; it_1 < 10; it_1++) {
      for (it_2 = -9; it_2 < 10; it_2++) {
        for (it_3 = -9; it_3 < 10; it_3++) {
          iter_count++;
          auto max_it = std::max({it_0, it_1, it_2, it_3});
          auto min_it = std::min({it_0, it_1, it_2, it_3});
          neg_map[{it_0, it_1, it_2, it_3}] = 0;
        }
      }
    }
  }

  // then go through prices, and update corresponding neg_values accordingly
  iter_count = 0;
  for (std::size_t row_idx{0}; row_idx < prices_table.size(); row_idx++) {
    const auto &prices_array = prices_table.at(row_idx);
    const auto &changes_array = prices_changes_table.at(row_idx);
    std::unordered_set<neg_t, neg_hash> encountered_negs{};
    // std::cout << std::format("Currently at iteration n°{}", iter_count) <<
    // std::endl; // [Debugging]
    for (std::size_t col_idx{0}; col_idx < prices_array.size() - 4; col_idx++) {
      iter_count++;
      auto sub_changes_array =
          reinterpret_cast<const neg_t *>(&(changes_array.at(col_idx)));
      auto neg_iter = neg_map.find(*sub_changes_array);
      if (neg_iter != neg_map.end()) {
        if (encountered_negs.contains(neg_iter->first)) {
          ;
        } else {
          (neg_iter->second) += prices_array.at(col_idx + 4);
          encountered_negs.insert(neg_iter->first);
        }
      } else {
        throw std::runtime_error(
            std::format("Error : neg value ({}, {}, {}, {}) (found at row_idx, "
                        "col_idx = ({}, {})) should already be in map !",
                        sub_changes_array->at(0), sub_changes_array->at(1),
                        sub_changes_array->at(2), sub_changes_array->at(3),
                        row_idx, col_idx));
      }
    }
  }
  std::uint64_t max_revenue{0};
  for (auto neg_values_iter = neg_map.begin(); neg_values_iter != neg_map.end();
       neg_values_iter++) {
    max_revenue = std::max({max_revenue, neg_values_iter->second});
  }
  return max_revenue;
}

int main(int argc, char *argv[]) {
  // PART 1
  const std::string le_filename{"../inputs/day_22_input.txt"};
  auto le_lines = fileToLines(le_filename);
  auto sum_of_2000th_numbers = getSumOf2000thNumbers(le_lines);
  std::cout << "Sum of 2000th numbers is :\n"
            << sum_of_2000th_numbers << std::endl;

  // PART 2
  // v5
  auto prices_table = getPricesTable_v5(le_lines);
  // for (const auto &row : prices_table) {
  //   for (const auto &pr : row) {
  //     std::cout << (int)(pr) << ", "; // [Debugging]
  //   }
  //   std::cout << std::endl; // [Debugging]
  // }
  std::cout << std::endl; // [Debugging]
  auto max_rev = findMaxRevenue_v5(prices_table);
  std::cout << std::format("Found max possible revenue of {} !", max_rev)
            << std::endl;
}