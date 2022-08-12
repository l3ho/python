from random import randint
from random import seed
import numpy as np
import time

runs = 10000
flips_per_run = 100
streak_length = 6

"""
1. Rzucamy monetą 100 razy
2. Sprawdzamy czy w ramach próby osiągnęliśmy 6 reszek bądź orłów pod rząd
3. Powtarzamy próbe, np. 10 000 razy
4. Sprawdzamy ile procent wszystkich rzutów stanowi wymagany rezultat z punktu 2.
"""

def rafals_code():
    total_streaks = 0
    for experiment_number in range(runs):
        flips = []
        for i in range(flips_per_run):
            if randint(0, 1) == 1:
                flips.append('H')
            else:
                flips.append('T')
        current_streak = 1
        previous_flip = None
        for flip in flips:
            if flip == previous_flip:
                current_streak += 1
                if current_streak == streak_length:
                    total_streaks += 1
                    current_streak = 0
            else:
                current_streak = 0
            previous_flip = flip
    percentage_with_streaks = total_streaks / runs
    print(f'Percentage of runs with streak of {total_streaks}: {percentage_with_streaks * 100: .2f}%')


def my_code1():
    total_streaks = 0
    cur_streak = 0
    flips = []
    for i in range(1000000):
        if randint(0, 1) == 1:
            flips.append('H')
        else:
            flips.append('T')
        if i > 0 or i % 100 != 0:
            if flips[i] == flips[i-1]:
                cur_streak += 1
            elif cur_streak == 5:
                total_streaks += 1
                cur_streak = 0
            elif flips[i] != flips[i-1]:
                cur_streak = 0
        if i % 99 == 0:
            cur_streak = 0
    percentage_with_streaks = total_streaks / runs
    print(f'Percentage of runs with streak of {total_streaks}: {percentage_with_streaks * 100: .2f}%')


def my_code2():
    total_streaks = 0
    cur_streak = 0
    flips = np.random.choice(2, 1000000)
    for i in range(1000000):
        if i > 0 or i % 100 != 0:
            if flips[i] == flips[i-1]:
                cur_streak += 1
            elif cur_streak == 5:
                total_streaks += 1
                cur_streak = 0
            elif flips[i] != flips[i-1]:
                cur_streak = 0
        if i % 99 == 0:
            cur_streak = 0
    percentage_with_streaks = total_streaks / runs
    print(f'Percentage of runs with streak of {total_streaks}: {percentage_with_streaks * 100: .2f}%')


def main():
    seed(123)
    np.random.seed(123)
    start_time = time.time()
    rafals_code()
    print("Rafal %s seconds ---" % (time.time() - start_time))
    start_time1 = time.time()
    my_code1()
    print("My_code1 %s seconds ---" % (time.time() - start_time1))
    start_time2 = time.time()
    my_code2()
    print("My_code2 %s seconds ---" % (time.time() - start_time2))


main()
