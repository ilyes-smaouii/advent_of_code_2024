#include <array>
#include <cstddef>
#include <cstdint>
#include <cstdio>
#include <format>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

std::vector<std::string> fileToLines(const std::string &filename) {
  std::vector<std::string> res_vec{};
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

std::uint64_t getSumOf2000thNumbers(const std::vector<std::string> &lines) {
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

std::array<std::int8_t, 2001> get2000Prices(std::uint32_t initial_secret) {
  auto secrets_array = get2000NextSecrets(initial_secret);
  return secretsToPrices(secrets_array);
}

std::int8_t tryNegotiation(const std::array<std::int8_t, 2001> &prices_array,
                           const std::array<std::int8_t, 4> &negotiator_array) {
  const std::int8_t &n0{negotiator_array[0]}, &n1{negotiator_array[1]},
      &n2{negotiator_array[2]}, &n3{negotiator_array[3]};
  // TO-DO : go through array and try
  // something std::memcmp ?
  // []
  // element-by-element comparison ?
  /* n0 = -6;
  n1 = 0;
  n2 = 5;
  n3 = 1; */
  for (std::size_t i{0}; i < prices_array.size() - 4; i++) {
    const std::int8_t &p0{prices_array.at(i + 0)}, &p1{prices_array.at(i + 1)},
        &p2{prices_array.at(i + 2)}, &p3{prices_array.at(i + 3)},
        &p4{prices_array.at(i + 4)};
    if (p1 - p0 == n0 && p2 - p1 == n1 && p3 - p2 == n2 && p4 - p3 == n3) {
      return p4;
    }
  }
  return 0;
}

int main(int argc, char *argv[]) {
  const std::string le_filename{"../inputs/day_22_input.txt"};
  auto le_lines = fileToLines(le_filename);
  auto sum_of_2000th_numbers = getSumOf2000thNumbers(le_lines);
  std::cout << "Sum of 2000th numbers is :\n"
            << sum_of_2000th_numbers << std::endl;
  // constexpr std::size_t LE_POSSIBILITIES_COUNT = 18 * 18 * 18 * 18;
  std::array<std::int8_t, 4> negotiation_array{-18, -18, -18, -18};
  std::int8_t &n0{negotiation_array[0]}, &n1{negotiation_array[1]},
      &n2{negotiation_array[2]}, &n3{negotiation_array[3]};
  std::size_t iter{0};
  for (const auto &line : le_lines) {
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
  }
}