import math
import random
import sys
import time
import copy
import santa_utl as utl

random.seed(1)


def sa_schedules(n_of_symbols: int, n_of_schedules: int, temperature: int, cooling_rate: int, iteration_limit: int):
    # Create string of symbols
    symbol_string = ''.join(str(i+1) for i in range(n_of_symbols))

    # Create list of all permutations as strings
    mandatory_perms = utl.list_mandatory_permutations(symbol_string)
    regular_perms = utl.list_regular_permutations(symbol_string, mandatory_perms)

    # Beginning of Simulated Annealing Algorithm
    schedules = create_base_schedules(mandatory_perms, regular_perms, n_of_schedules)
    best_result = utl.schedules_as_strings(schedules, n_of_symbols)
    best_score = utl.calculate_final_score(best_result)
    iterations = 1
    while iterations < iteration_limit:
        print(f'Iteration: {iterations}')
        iterations += 1

        for s in range(n_of_schedules):
            neighbour = get_random_neighbour(schedules[s])

            current_score = utl.check_score(schedules[s], n_of_symbols)
            neighbour_score = utl.check_score(neighbour, n_of_symbols)
            r = random.random()
            pa = math.exp(-(abs(neighbour_score-current_score))/temperature)
            if neighbour_score < current_score:
                schedules[s] = neighbour
            elif r < pa:
                schedules[s] = neighbour

        current = utl.schedules_as_strings(schedules, n_of_symbols)
        current_score = utl.calculate_final_score(current)
        if current_score < best_score:
            best_result = current
            best_score = current_score

        temperature = temperature * cooling_rate
        print(f"Current score: {current_score}")
        print(f"Best score: {best_score}")
        print(f'Temperature: {temperature}')

    return best_result


def create_base_schedules(mandatory: list, regular: list, n_of_schedules: int):
    schedules = []
    for _ in range(n_of_schedules):
        schedules.append(copy.deepcopy(mandatory))

    random.shuffle(regular)
    div, mod = divmod(len(regular), n_of_schedules)
    split_permutations = [regular[s * div + min(s, mod):(s+1) * (div) + min(s+1, mod)] for s in range(n_of_schedules)]
    for s in range(n_of_schedules):
        schedules[s] += split_permutations[s]
    return schedules


def get_random_neighbour(schedule: list) -> list:
    neighbour = copy.deepcopy(schedule)
    index1 = random.randint(0, len(neighbour)-1)
    element1 = neighbour[index1]
    index2 = random.randint(0, len(neighbour)-1)
    element2 = neighbour[index2]
    neighbour[index1] = element2
    neighbour[index2] = element1
    return neighbour


if __name__ == '__main__':

    if len(sys.argv) < 6:
        print("Nearest neighbour requires two parameters: 'number of symbols', 'number of schedules', 'temperature', 'cooling rate' and 'max iterations'")
    else:
        start_time = time.time()
        n = int(sys.argv[1])
        strings = int(sys.argv[2])
        T = float(sys.argv[3])
        cool_rate = float(sys.argv[4])
        max_iter = int(sys.argv[5])

        final_schedule_strings = sa_schedules(n, strings, T, cool_rate, max_iter)
        final_score = utl.calculate_final_score(final_schedule_strings)
        for s in final_schedule_strings:
            print(s, end='\n\n')
        if utl.validate_answer(n, strings, final_schedule_strings):
            for s in utl.insert_emoji(strings, final_schedule_strings):
                print(s, end='\n\n')
            print(f'Score: {final_score}')
            print(f'Time: {round(time.time()-start_time, 2)} seconds')
