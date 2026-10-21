"""
CSC2107 Design & Analysis of Algorithms — Assignment 5.1
Naive vs. Memoized Fibonacci

Run:
    python daa_assignment_5_1.py

The program:
- implements naive recursion and recursion with memoization;
- checks both implementations for n = 0..20;
- measures function calls and elapsed time;
- prints result tables;
- saves a call-count graph;
- demonstrates the recursion-limit issue and two alternatives.
"""
import math
import sys
import time
import matplotlib.pyplot as plt

# Global call counters requested in Part 1.
naive_calls = 0
memo_calls = 0


def fib_naive(n):
    """Algorithm A: plain recursive Fibonacci."""
    global naive_calls
    naive_calls += 1

    if n == 0 or n == 1:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)


def fib_memo(n, fibtable):
    """Algorithm B: recursive Fibonacci with memoization.

    None means 'not calculated yet'. This is important because F(0) is 0.
    """
    global memo_calls
    memo_calls += 1

    # Use an explicit sentinel check; do not use `if fibtable[n]`,
    # because a stored value of 0 would look false.
    if fibtable[n] is not None:
        return fibtable[n]

    if n == 0 or n == 1:
        value = n
    else:
        value = fib_memo(n - 1, fibtable) + fib_memo(n - 2, fibtable)

    fibtable[n] = value
    return value


def run_naive_experiments():
    """Measure Algorithm A for the required n values, stopping over 60 seconds."""
    results = []
    for n in [5, 10, 15, 20, 25, 30, 35]:
        global naive_calls
        naive_calls = 0
        start = time.perf_counter()
        value = fib_naive(n)
        elapsed = time.perf_counter() - start
        results.append((n, naive_calls, elapsed, value))
        print(f"Algorithm A: n={n:4d}, calls={naive_calls:>12,}, "
              f"time={elapsed:.6f} s, F(n)={value}")
        if elapsed > 60:
            print("Stopping Algorithm A because this run exceeded 60 seconds.")
            break
    return results


def run_memo_experiments():
    """Measure Algorithm B, clearing the memo table before every run."""
    results = []
    for n in [10, 50, 100, 200, 500, 1000]:
        global memo_calls
        memo_calls = 0
        fibtable = [None] * (n + 1)  # a fresh table for every run
        start = time.perf_counter()
        value = fib_memo(n, fibtable)
        elapsed = time.perf_counter() - start
        results.append((n, memo_calls, elapsed, value))
        print(f"Algorithm B: n={n:4d}, calls={memo_calls:>8,}, "
              f"time={elapsed:.6f} s, digits in F(n)={len(str(value))}")
    return results


def verify_equal_values():
    """Part 1: verify that both algorithms agree for n = 0 through 20."""
    for n in range(21):
        naive_calls = 0
        table = [None] * (n + 1)
        a = fib_naive(n)
        b = fib_memo(n, table)
        assert a == b, f"Mismatch at n={n}: {a} != {b}"
    print("Verification passed: both algorithms agree for every n from 0 to 20.")


def save_results_and_plot(naive_results, memo_results):
    """Save result tables as CSV and a graph of n against function calls."""
    import csv

    with open("algorithm_a_results.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["n", "calls", "time (s)"])
        writer.writerows((n, calls, f"{elapsed:.9f}")
                         for n, calls, elapsed, _ in naive_results)

    with open("algorithm_b_results.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["n", "calls", "time (s)"])
        writer.writerows((n, calls, f"{elapsed:.9f}")
                         for n, calls, elapsed, _ in memo_results)

    # A log y-axis makes the rapid exponential increase of Algorithm A visible
    # alongside the much slower linear increase of Algorithm B.
    plt.figure(figsize=(9, 5.5))
    plt.plot([r[0] for r in naive_results], [r[1] for r in naive_results],
             marker="o", label="Algorithm A: naive recursion")
    plt.plot([r[0] for r in memo_results], [r[1] for r in memo_results],
             marker="s", label="Algorithm B: memoization")
    plt.yscale("log")
    plt.xlabel("Input n")
    plt.ylabel("Number of function calls (log scale)")
    plt.title("Function calls: naive recursion vs. memoization")
    plt.grid(True, which="both", linestyle=":")
    plt.legend()
    plt.tight_layout()
    plt.savefig("fibonacci_call_counts.png", dpi=200)
    print("Saved CSV tables and fibonacci_call_counts.png in the current directory.")


def iterative_fibonacci(n):
    """Fix 1 alternative: bottom-up iteration; no recursive calls or stack growth."""
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return 0
    previous, current = 0, 1
    for _ in range(2, n + 1):
        previous, current = current, previous + current
    return current


def memo_with_adjusted_recursion_limit(n):
    """Fix 2 alternative: temporarily raise the recursion limit.

    Raising the limit is environment-dependent; excessively high limits can
    risk exhausting the process stack. This function restores the old limit.
    """
    old_limit = sys.getrecursionlimit()
    try:
        if old_limit < n + 100:
            sys.setrecursionlimit(n + 100)
        table = [None] * (n + 1)
        global memo_calls
        memo_calls = 0
        return fib_memo(n, table)
    finally:
        sys.setrecursionlimit(old_limit)


def demonstrate_part_4():
    print(f"Current Python recursion limit: {sys.getrecursionlimit()}")
    n = 1000
    print(f"Iterative result for n={n} has {len(str(iterative_fibonacci(n)))} digits.")
    print(f"Memoized result after adjusting recursion limit has "
          f"{len(str(memo_with_adjusted_recursion_limit(n)))} digits.")
    print("If the interpreter's recursion limit is below the required call depth, "
          "plain recursive memoization may raise RecursionError.")
    print("The iterative approach avoids that recursion-depth problem.")


def main():
    verify_equal_values()
    print("\n--- Algorithm A: naive recursion ---")
    naive_results = run_naive_experiments()
    print("\n--- Algorithm B: memoization ---")
    memo_results = run_memo_experiments()
    save_results_and_plot(naive_results, memo_results)
    print("\n--- Part 4: n=1000 and recursion limit ---")
    demonstrate_part_4()


if __name__ == "__main__":
    main()
