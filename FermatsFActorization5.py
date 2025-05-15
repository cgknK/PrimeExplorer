import math
import numpy as np
import random
import time
from typing import List, Tuple, Optional
from concurrent.futures import ProcessPoolExecutor
import matplotlib.pyplot as plt


def optimized_sieve_of_eratosthenes(limit: int) -> List[int]:
    if limit < 2:
        return []

    is_prime = np.zeros(limit + 1, dtype=bool)
    is_prime[2] = True
    is_prime[3:limit + 1:2] = True  # Set all odd numbers to true, assume primes

    for num in range(3, int(math.sqrt(limit)) + 1, 2):
        if is_prime[num]:
            is_prime[num * num:limit + 1:num * 2] = False  # Mark multiples as not prime

    return np.nonzero(is_prime)[0].tolist()  # Return list of prime numbers


def random_prime_pair_choice(primes: List[int]) -> Tuple[int, int]:
    return tuple(random.sample(primes, 2))


def is_square(n: int) -> bool:
    sqrt_n = np.int64(np.sqrt(n))
    return sqrt_n * sqrt_n == n


def fermat_factorization(num: int, time_limit: Optional[int] = None, max_iterations: int = 10**9) -> Tuple[Optional[int], Optional[int], int]:
    a = np.int64(np.ceil(np.sqrt(num)))  # Faster square root with numpy
    delta = a * a - num
    count = 0
    start_time = time.process_time()

    for _ in range(max_iterations):
        if is_square(delta):
            b = np.int64(np.sqrt(delta))
            return a - b, a + b, count

        a += 1
        delta = a * a - num
        count += 1

        if time_limit and (time.process_time() - start_time > time_limit):
            return None, None, count

    return None, None, max_iterations


def check_result(n: int, factors: Tuple[Optional[int], Optional[int], int]) -> bool:
    if factors[0] is None or factors[1] is None:
        return False
    p, q = factors[:2]
    return p * q == n


def run_single_test(primes: List[int], time_limit: Optional[int]) -> bool:
    p, q = random_prime_pair_choice(primes)
    n = p * q
    result_fermats = fermat_factorization(n, time_limit=time_limit)
    return check_result(n, result_fermats)


def run_test_wrapper(args):
    return run_single_test(*args)


def run_tests(primes: List[int], num_tests: int, time_limit: Optional[int], num_repeats: int = 5) -> List[float]:
    success_rates = []
    for _ in range(num_repeats):
        with ProcessPoolExecutor() as executor:
            args = [(primes, time_limit) for _ in range(num_tests)]
            results = list(executor.map(run_test_wrapper, args))

        successes = sum(results)
        success_rate = (successes / num_tests) * 100
        success_rates.append(success_rate)

    return success_rates


def plot_success_rate_by_time(primes: List[int], num_tests: int):
    time_limits = [5, 10, 15, 20, 25, 30]
    avg_success_rates = []

    for time_limit in time_limits:
        success_rates = run_tests(primes, num_tests, time_limit)
        avg_success_rate = sum(success_rates) / len(success_rates)
        avg_success_rates.append(avg_success_rate)

    # Plot the results
    plt.figure(figsize=(8, 6))
    plt.plot(time_limits, avg_success_rates, marker='o', linestyle='-', color='b', label='Success Rate')
    plt.title('Success Rate of Fermat Factorization vs. Time Limits')
    plt.xlabel('Time Limit (seconds)')
    plt.ylabel('Average Success Rate (%)')
    plt.grid(True)
    plt.legend()
    plt.show()


def main():
    limit = 10**8
    primes = optimized_sieve_of_eratosthenes(limit)  # Smaller prime list for faster testing
    num_tests = 25
    plot_success_rate_by_time(primes, num_tests)


if __name__ == '__main__':
    main()
