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
get2000NextSecrets(std::uint32_t initial_secret) {
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

std::array<std::int8_t, 2001>
secretsToPrices(const std::array<std::uint32_t, 2001> &secrets_array) {
  std::array<std::int8_t, 2001> prices_array{};
  for (std::size_t i{0}; i < 2001; i++) {
    prices_array[i] = secrets_array[i] % 10;
  }
  return prices_array;
}

std::array<std::uint8_t, 2001>
secretsToPrices_v3(const std::array<std::uint32_t, 2001> &secrets_array) {
  std::array<std::uint8_t, 2001> prices_array{};
  for (std::size_t i{0}; i < 2001; i++) {
    prices_array[i] = secrets_array[i] % 10;
  }
  return prices_array;
}

std::array<std::int8_t, 2001> get2000Prices(std::uint32_t initial_secret) {
  auto secrets_array = get2000NextSecrets(initial_secret);
  return secretsToPrices(secrets_array);
}

std::array<std::uint8_t, 2001> get2000Prices_v3(std::uint32_t initial_secret) {
  auto secrets_array = get2000NextSecrets(initial_secret);
  return secretsToPrices_v3(secrets_array);
}

/* std::int8_t tryNegotiation(const std::array<std::int8_t, 2001>
&prices_array, const std::array<std::int8_t, 4> &negotiator_array) { const
std::int8_t &n0{negotiator_array[0]}, &n1{negotiator_array[1]},
      &n2{negotiator_array[2]}, &n3{negotiator_array[3]};
  // TO-DO : go through array and try

  // something with std::memcmp ?
  // auto p8 = reinterpret_cast<const std::int8_t*>(&prices_array.at(i))
  // auto p32 = reinterpret_cast<const std::uint32_t*>(p8)
  // auto n32 = reinterpret_cast<const std::uint32_t*>([array as arr_element *
  // -1 + smth for each element, w/ 0 <= elem <= 9 (same as prices)])
  // auto sum = p32 + n32
  // auto vals_8 = reinterpret_cast<const std::uint8*>(&sum);
  // if (vals_8[0] == vals_8[1] && [...])
  // {
  //  return p8[3];
  // }

  // element-by-element comparison ?
  // n0 = -6;
  // n1 = 0;
  // n2 = 5;
  // n3 = 1;
  for (std::size_t i{0}; i < prices_array.size() - 4; i++) {
    const std::int8_t &p0{prices_array.at(i + 0)}, &p1{prices_array.at(i + 1)},
        &p2{prices_array.at(i + 2)}, &p3{prices_array.at(i + 3)},
        &p4{prices_array.at(i + 4)};
    if (p1 - p0 == n0 && p2 - p1 == n1 && p3 - p2 == n2 && p4 - p3 == n3) {
      return p4;
    }
  }
  return 0;
} */

std::int8_t
tryNegotiation_v2(const std::array<std::int8_t, 2001> &prices_array,
                  const std::array<std::int8_t, 4> &negotiator_array) {
  const auto nego_32 =
      reinterpret_cast<const std::uint32_t *>(negotiator_array.data());
  const std::uint32_t *price_32;
  auto sum32 = new std::uint32_t;
  std::int8_t *sum_8 = reinterpret_cast<std::int8_t *>(sum32);
  for (std::size_t i{0}; i < prices_array.size() - 4; i++) {
    // price_32 =
    // reinterpret_cast<const std::uint32_t *>(&(prices_array.at(i + 1)));
    std::int8_t sum1 = prices_array.at(i + 1) + negotiator_array.at(0),
                sum2 = prices_array.at(i + 2) + negotiator_array.at(1),
                sum3 = prices_array.at(i + 3) + negotiator_array.at(2),
                sum4 = prices_array.at(i + 4) + negotiator_array.at(3);

    // if (prices_array.at(i) == sum_8[0] == sum_8[1] == sum_8[2] == sum_8[3]) {
    //   return prices_array.at(i + 4);
    // }
    if ((prices_array.at(i) == sum1) && (sum1 == sum2) && (sum2 == sum3) &&
        (sum3 == sum4)) {
      return prices_array.at(i + 4);
    }
    // if (prices_array.at(i) ==
    //     (prices_array.at(i + 1) + negotiator_array.at(0)) ==
    //     (prices_array.at(i + 2) + negotiator_array.at(1)) ==
    //     (prices_array.at(i + 3) + negotiator_array.at(2)) ==
    //     (prices_array.at(i + 4) + negotiator_array.at(3))) {
    //   return prices_array.at(i + 4);
    // }
    // if (prices_array.at(i) == *sum_8 && std::memcmp(sum_8, sum_8 + 1, 3) ==
    // 0) {
    //   return prices_array.at(i + 4);
    // }
  }
  return 0;
}

std::uint8_t
tryNegotiation_v3(const std::array<std::uint8_t, 2001> &prices_array,
                  std::int8_t offset,
                  const std::array<std::uint8_t, 4> &negotiator_array) {
  const auto nego_32 =
      reinterpret_cast<const std::uint32_t *>(negotiator_array.data());
  const std::uint32_t *price_32;
  auto sum32 = new std::uint32_t;
  std::uint8_t *sum_8 = reinterpret_cast<std::uint8_t *>(sum32);
  std::uint16_t *sum_16 = reinterpret_cast<std::uint16_t *>(sum32);
  for (std::size_t i{0}; i < prices_array.size() - 4; i++) {
    price_32 =
        reinterpret_cast<const std::uint32_t *>(&(prices_array.at(i + 1)));
    *sum32 = *nego_32 + *price_32;
    if (static_cast<std::int8_t>(prices_array.at(i + 1)) -
            static_cast<std::int8_t>(prices_array.at(i)) ==
        offset) {
      if (sum_16[0] == sum_16[1] && sum_8[0] == sum_8[1]) {
        return prices_array.at(i + 4);
      }
    }
  }
  return 0;
}

std::array<std::int8_t, 2000>
pricesToPriceChanges(const std::array<std::uint8_t, 2001> &prices_array) {
  std::array<std::int8_t, 2000> changes_array{};
  for (std::size_t i{0}; i < changes_array.size(); i++) {
    changes_array.at(i) = static_cast<std::int8_t>(prices_array.at(i + 1)) -
                          static_cast<std::int8_t>(prices_array.at(i));
  }
  return changes_array;
}

std::uint64_t findMaxRevenue_v2(
    const std::vector<std::array<std::int8_t, 2001>> &prices_table) {
  std::array<std::int8_t, 4> nego_array{};
  std::uint64_t max_revenue_all_nego{0};
  // loop through all possible negotiation arrays
  std::size_t iter_count{0};
  for (std::int8_t it_0{-9}; it_0 < 10; it_0++) {
    // nego_array.at(0) = it_1;
    for (std::int8_t it_1{-9}; it_1 < 10; it_1++) {
      // nego_array.at(1) = it_2;
      std::cout << std::format("findMaxRevenue() - Currently at "
                               "iteration/negotiation array n°{}",
                               iter_count)
                << std::endl; // [Debugging]
      std::cout << std::format("(max revenue currently at {})",
                               max_revenue_all_nego)
                << std::endl; // [Debugging]
      for (std::int8_t it_2{-9}; it_2 < 10; it_2++) {
        // nego_array.at(2) = it_3;
        for (std::int8_t it_4{-9}; it_4 < 10; it_4++) {
          iter_count++;

          // [check on validity of nego array]
          auto max_it = std::max({it_0, it_1, it_2, it_4});
          auto min_it = std::min({it_0, it_1, it_2, it_4});
          if ((max_it - min_it) > 9) {
            continue;
          }

          // nego_array.at(3) = it_4;
          nego_array = {it_0, it_1, it_2, it_4};
          // for each possible negotiation array :
          std::uint64_t total_revenue_curr_nego{0};
          // try all negotiation with current negotiation
          for (const auto &prices_array : prices_table) {
            total_revenue_curr_nego +=
                tryNegotiation_v2(prices_array, nego_array);
          }
          if (total_revenue_curr_nego > max_revenue_all_nego) {
            max_revenue_all_nego = total_revenue_curr_nego;
          }
        }
      }
    }
  }
  return max_revenue_all_nego;
}

std::uint64_t findMaxRevenue_v3(
    const std::vector<std::array<std::uint8_t, 2001>> &prices_table) {
  std::array<std::uint8_t, 4> nego_array{};
  std::uint64_t max_revenue_all_nego{0};
  // loop through all possible negotiation arrays
  std::size_t iter_count{0};
  for (std::uint8_t it_0{0}; it_0 < 10; it_0++) {
    // nego_array.at(0) = it_1;
    for (std::uint8_t it_1{0}; it_1 < 10; it_1++) {
      // nego_array.at(1) = it_2;
      std::cout << std::format("findMaxRevenue() - Currently at "
                               "iteration/negotiation array n°{}",
                               iter_count)
                << std::endl; // [Debugging]
      std::cout << std::format("(max revenue currently at {})",
                               max_revenue_all_nego)
                << std::endl; // [Debugging]
      for (std::uint8_t it_2{0}; it_2 < 10; it_2++) {
        // nego_array.at(2) = it_3;
        for (std::uint8_t it_4{0}; it_4 < 10; it_4++) {
          for (std::int8_t offset{-9}; offset < 10; offset++) {
            iter_count++;

            // nego_array.at(3) = it_4;
            nego_array = {it_0, it_1, it_2, it_4};
            // for each possible negotiation array :
            std::uint64_t total_revenue_curr_nego{0};
            // try all negotiation with current negotiation
            for (const auto &prices_array : prices_table) {
              total_revenue_curr_nego +=
                  tryNegotiation_v3(prices_array, offset, nego_array);
            }
            if (total_revenue_curr_nego > max_revenue_all_nego) {
              max_revenue_all_nego = total_revenue_curr_nego;
            }
          }
        }
      }
    }
  }
  return max_revenue_all_nego;
}

std::vector<std::array<std::int8_t, 2001>>
getPricesTable_v2(const strings_vec_t &lines) {
  std::vector<std::array<std::int8_t, 2001>> res_table{};
  for (const auto &line : lines) {
    auto initial_secret = static_cast<std::uint32_t>(std::stoi(line));
    auto prices_array = get2000Prices(initial_secret);
    res_table.push_back(prices_array);
  }
  return res_table;
}

std::vector<std::array<std::uint8_t, 2001>>
getPricesTable_v3(const strings_vec_t &lines) {
  std::vector<std::array<std::uint8_t, 2001>> res_table{};
  for (const auto &line : lines) {
    auto initial_secret = static_cast<std::uint32_t>(std::stoi(line));
    auto prices_array = get2000Prices_v3(initial_secret);
    res_table.push_back(prices_array);
  }
  return res_table;
}

std::uint8_t
tryNegotiation_v4(const std::array<std::uint8_t, 2001> &prices_array,
                  const std::array<std::int8_t, 2000> &price_changes_array,
                  const std::array<std::int8_t, 4> &negotiator_array) {
  for (std::size_t i{0}; i < price_changes_array.size() - 4; i++) {
    // if (price_changes_array.at(i) == negotiator_array.at(0) &&
    //     price_changes_array.at(i + 1) == negotiator_array.at(1) &&
    //     price_changes_array.at(i + 2) == negotiator_array.at(2) &&
    //     price_changes_array.at(i + 3) == negotiator_array.at(3)) {
    //   return prices_array.at(i + 4);
    // }
    auto changes_32{
        reinterpret_cast<const std::int32_t *>(&(price_changes_array.at(i)))};
    auto negotiatior_32{
        reinterpret_cast<const std::int32_t *>(negotiator_array.data())};
    if (*changes_32 == *negotiatior_32) {
      return prices_array.at(i + 4);
    }
  }
  return 0;
}

std::vector<std::array<std::int8_t, 2000>> getChangesTable(
    const std::vector<std::array<std::uint8_t, 2001>> &prices_table) {
  std::vector<std::array<std::int8_t, 2000>> changes_table{};
  for (const auto &prices_array : prices_table) {
    changes_table.push_back(pricesToPriceChanges(prices_array));
  }
  return changes_table;
}

std::uint64_t findMaxRevenue_v4(
    const std::vector<std::array<std::uint8_t, 2001>> &prices_table) {
  auto prices_changes_table = getChangesTable(prices_table);
  std::uint64_t max_revenue_all_nego{0};
  std::size_t iter_count{0};
  std::array<std::int8_t, 4> neg_array{};
  for (std::int8_t it_0{-9}; it_0 < 10; it_0++) {
    // nego_array.at(0) = it_1;
    for (std::int8_t it_1{-9}; it_1 < 10; it_1++) {
      // nego_array.at(1) = it_2;
      std::cout << std::format("findMaxRevenue() - Currently at "
                               "iteration/negotiation array n°{}",
                               iter_count)
                << std::endl; // [Debugging]
      std::cout << std::format("(max revenue currently at {})",
                               max_revenue_all_nego)
                << std::endl; // [Debugging]
      for (std::int8_t it_2{-9}; it_2 < 10; it_2++) {
        // nego_array.at(2) = it_3;
        for (std::int8_t it_3{-9}; it_3 < 10; it_3++) {
          iter_count++;
          auto max_it = std::max({it_0, it_1, it_2, it_3});
          auto min_it = std::min({it_0, it_1, it_2, it_3});
          if ((max_it - min_it) > 9) {
            continue;
          }
          neg_array = {it_0, it_1, it_2, it_3};
          std::uint64_t revenue_curr_nego{0};
          for (std::size_t row_idx{0}; row_idx < prices_table.size();
               row_idx++) {
            revenue_curr_nego +=
                tryNegotiation_v4(prices_table[row_idx],
                                  prices_changes_table[row_idx], neg_array);
          }
          if (revenue_curr_nego > max_revenue_all_nego) {
            max_revenue_all_nego = revenue_curr_nego;
          }
        }
      }
    }
  }
  return max_revenue_all_nego;
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
  auto prices_changes_table = getChangesTable(prices_table);

  std::unordered_map<neg_t, std::uint64_t, neg_hash> neg_map{};

  // First, fill neg_values with 0's
  std::size_t iter_count{0};
  neg_t neg_array{};
  std::int8_t &it_0{neg_array.at(0)}, &it_1{neg_array.at(1)},
      &it_2{neg_array.at(2)}, &it_3{neg_array.at(3)};
  for (it_0 = -9; it_0 < 10; it_0++) {
    // nego_array.at(0) = it_1;
    for (it_1 = -9; it_1 < 10; it_1++) {
      // nego_array.at(1) = it_2;
      // std::cout << std::format("findMaxRevenue() - filling - currently at "
      //                          "iteration/negotiation array n°{}",
      //                          iter_count)
      //           << std::endl; // [Debugging]
      for (it_2 = -9; it_2 < 10; it_2++) {
        // nego_array.at(2) = it_3;
        for (it_3 = -9; it_3 < 10; it_3++) {
          // if (neg_array == neg_t{-1, 8, 2, 3}) {
          //   throw std::runtime_error("Found it !");
          // }
          iter_count++;
          auto max_it = std::max({it_0, it_1, it_2, it_3});
          auto min_it = std::min({it_0, it_1, it_2, it_3});
          if ((max_it - min_it) > 9) {
            // continue;
          }
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
    // std::cout << std::format("Currently at iteration n°{}", iter_count) << std::endl; // [Debugging]
    for (std::size_t col_idx{0}; col_idx < prices_array.size() - 4; col_idx++) {
      iter_count++;
      auto sub_changes_array =
          reinterpret_cast<const neg_t *>(&(changes_array.at(col_idx)));
      auto neg_iter = neg_map.find(*sub_changes_array);
      if (neg_iter != neg_map.end()) {
        // if (prices_array.at(col_idx + 4) !=
        //     prices_array.at(col_idx) + sub_changes_array->at(0) +
        //         sub_changes_array->at(1) + sub_changes_array->at(2) +
        //         sub_changes_array->at(3)) {
        //   throw std::runtime_error("Error : bad (inconsistent) changes array
        //   !");
        // }
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
      // neg_values[*changes_array] += prices_array.at(col_idx + 4);
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
  const std::string le_filename{"../inputs/day_22_input.txt"};
  auto le_lines = fileToLines(le_filename);
  auto sum_of_2000th_numbers = getSumOf2000thNumbers(le_lines);
  std::cout << "Sum of 2000th numbers is :\n"
            << sum_of_2000th_numbers << std::endl;
  // constexpr std::size_t LE_POSSIBILITIES_COUNT = 18 * 18 * 18 * 18;
  // // std::array<std::int8_t, 4> negotiation_array{-18, -18, -18, -18};
  // std::int8_t &n0{negotiation_array[0]}, &n1{negotiation_array[1]},
  //     &n2{negotiation_array[2]}, &n3{negotiation_array[3]};
  // std::size_t iter{0};
  /* for (const auto &line : le_lines) {
    std::uint32_t le_initial_secret{
        static_cast<std::uint32_t>(std::stoi(line))};
    std::int8_t max_price{0};
    auto _2000_prices = get2000Prices(le_initial_secret);
    std::cout << "prices :\n"; // [Debugging]
    for (auto price : _2000_prices) {
      std::cout << static_cast<int>(price) << ", "; // [Debugging]
    }
    std::cout << std::endl;
    for (std::size_t i{0};; i++) {
      n0++;
      if (n0 > 18) {
        n0 = -18;
        n1++;
        if (n1 > 18) {
          n1 = -18;
          n2++;
          if (n2 > 18) {
            n2 = -18;
            n3++;
            if (n3 > 18) {
              break;
            }
          }
        }
      }
      // std::cout << "Trying negotiation..." << std::endl;
      auto res = tryNegotiation(_2000_prices, negotiation_array);
      // std::cout << std::format("res {} for i = {}", res, i)
      //           << std::endl; // [Debugging]
      // std::cout << "Negotiation tried !" << std::endl;
      if (res > max_price) {
        max_price = res;
      }
    }
    std::cout
        << std::format(
               "Found max price of {} (iteration n°{}, initial secret of {})",
               static_cast<int>(max_price), iter, le_initial_secret)
        << std::endl;
    iter++;
  } */

  // v2
  // auto prices_table = getPricesTable_v2(le_lines);
  // // for (const auto &row : prices_table) {
  // //   for (const auto &pr : row) {
  // //     std::cout << (int)(pr) << ", "; // [Debugging]
  // //   }
  // //   std::cout << std::endl; // [Debugging]
  // // }
  // std::cout << std::endl; // [Debugging]
  // auto max_rev = findMaxRevenue_v2(prices_table);
  // std::cout << std::format("Found max revenue of {} !", max_rev) <<
  // std::endl;
  //
  // v3
  // auto prices_table = getPricesTable_v3(le_lines);
  // // for (const auto &row : prices_table) {
  // //   for (const auto &pr : row) {
  // //     std::cout << (int)(pr) << ", "; // [Debugging]
  // //   }
  // //   std::cout << std::endl; // [Debugging]
  // // }
  // std::cout << std::endl; // [Debugging]
  // auto max_rev = findMaxRevenue_v3(prices_table);
  // std::cout << std::format("Found max revenue of {} !", max_rev) <<
  // std::endl;
  //
  // v4
  // auto prices_table = getPricesTable_v3(le_lines);
  // // for (const auto &row : prices_table) {
  // //   for (const auto &pr : row) {
  // //     std::cout << (int)(pr) << ", "; // [Debugging]
  // //   }
  // //   std::cout << std::endl; // [Debugging]
  // // }
  // std::cout << std::endl; // [Debugging]
  // auto max_rev = findMaxRevenue_v4(prices_table);
  // std::cout << std::format("Found max revenue of {} !", max_rev) <<
  // std::endl;
  //
  // v5
  auto prices_table = getPricesTable_v3(le_lines);
  // for (const auto &row : prices_table) {
  //   for (const auto &pr : row) {
  //     std::cout << (int)(pr) << ", "; // [Debugging]
  //   }
  //   std::cout << std::endl; // [Debugging]
  // }
  std::cout << std::endl; // [Debugging]
  auto max_rev = findMaxRevenue_v5(prices_table);
  std::cout << std::format("Found max possible revenue of {} !", max_rev) << std::endl;
  //
  // auto prices_table = getPricesTable({"1", "2", "3", "2024"});
  // auto prices_array = get2000Prices(std::stoi(argv[1]));
  // for (const auto &pr : prices_array) {
  //   std::cout << (int)(pr) << ", "; // [Debugging]
  // }
  // std::cout << std::endl; // [Debugging]
  // auto price = tryNegotiation_v2(prices_array, {0, 2, 2, -5});
  // // price = findMaxRevenue({prices});
  // std::cout << "price : " << static_cast<int>(price) << std::endl;
}