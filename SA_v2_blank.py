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
    best_result = schedules_as_strings(schedules, n_of_symbols)
    best_score = utl.calculate_final_score(best_result)
    iterations = 1
    while iterations < iteration_limit:
        print(f'Iteration: {iterations}')
        iterations += 1

        neighbour = get_random_neighbour(schedules, n_of_schedules)

        current_score = utl.calculate_final_score(schedules_as_strings(schedules, n_of_symbols))
        neighbour_score = utl.calculate_final_score(schedules_as_strings(neighbour, n_of_symbols))
        r = random.random()
        pa = math.exp(-(abs(neighbour_score-current_score))/temperature)
        if neighbour_score < current_score:
            schedules = neighbour
        elif r < pa:
            schedules = neighbour

        current = schedules_as_strings(schedules, n_of_symbols)
        current_score = utl.calculate_final_score(current)
        if current_score < best_score:
            best_result = current
            best_score = current_score

        temperature = temperature * cooling_rate
        print(f"Current score: {current_score}")
        print(f"Best score: {best_score}")
        print(f'Temperature: {temperature}')

    return best_result


def create_base_schedules(mandatory: list, regular: list, n_of_schedules: int, blank='*'):
    schedules = []
    for _ in range(n_of_schedules):
        schedules.append(copy.deepcopy(mandatory))

    random.shuffle(regular)
    div, mod = divmod(len(regular), n_of_schedules)
    split_permutations = [regular[s * div + min(s, mod):(s+1) * (div) + min(s+1, mod)] for s in range(n_of_schedules)]
    for s in range(n_of_schedules):
        schedules[s] += split_permutations[s]
        schedules[s].insert(len(schedules[s])-1, blank)
        schedules[s].insert(1, blank)

    return schedules


def get_random_neighbour(schedule: list, n_of_schedules: int, blank='*') -> list:
    neighbour = copy.deepcopy(schedule)
    while True:
        possible_replacement = False
        while not possible_replacement:
            string1 = random.randint(0, n_of_schedules-1)
            string2 = random.randint(0, n_of_schedules-1)
            index1 = random.randint(0, len(neighbour[string1])-1)
            element1 = neighbour[string1][index1]
            index2 = random.randint(0, len(neighbour[string2])-1)
            element2 = neighbour[string2][index2]
            if string1 == string2:
                possible_replacement = True
            elif (element1[:2] != '12' and element2[:2] != '12') and (element1 != blank and element2 != blank):
                possible_replacement = True

            if element1 == blank and (index2 == 0 or index2 == len(neighbour[string2])-1):
                possible_replacement = False
            if element2 == blank and (index1 == 0 or index1 == len(neighbour[string1])-1):
                possible_replacement = False

        neighbour[string1][index1] = element2
        neighbour[string2][index2] = element1

        validate_neighbour = 0
        for s in range(n_of_schedules):
            blank_indices = [i for i, perm in enumerate(neighbour[s]) if perm == blank]
            if abs(blank_indices[0]-blank_indices[1]) != 1:
                validate_neighbour += 1
            else:
                neighbour[string1][index1] = element1
                neighbour[string2][index2] = element2

        if validate_neighbour == n_of_schedules:
            return neighbour


def merge_permutations(permutation_sequence: list, permutation_length: int, blank='*') -> str:
    permutation_sequence = copy.deepcopy(permutation_sequence)

    blank_indices = [i for i, perm in enumerate(permutation_sequence) if perm == blank]
    blank_permutations_list = []
    for index in blank_indices:
        permutation_with_blank = permutation_sequence[index-1] + '*' + permutation_sequence[index+1]
        permutation_with_blank = permutation_with_blank[1:len(permutation_with_blank)-1]
        blank_permutations_list += blank_replaced_permutations(permutation_with_blank, permutation_length)

    for index in blank_indices:
        blank_perm_first_element = permutation_sequence[index-1]
        blank_perm_last_element = permutation_sequence[index+1]
        if blank_perm_first_element in blank_permutations_list:
            blank_permutations_list.remove(blank_perm_first_element)
        if blank_perm_last_element in blank_permutations_list:
            blank_permutations_list.remove(blank_perm_last_element)

    for perm in blank_permutations_list:
        if perm in permutation_sequence:
            permutation_sequence.remove(perm)

    schedule_string = ''
    for i in range(len(permutation_sequence)):
        nextperm = permutation_sequence[i]
        distance = utl.calculate_distance(permutation_length, schedule_string, nextperm)
        schedule_string += nextperm[-distance:]
    return schedule_string


def schedules_as_strings(schedules: list, n_of_symbols: int) -> list:
    schedule_strings = []
    for sched in schedules:
        sched_str = merge_permutations(sched, n_of_symbols)
        schedule_strings.append(sched_str)
    return schedule_strings


def blank_replaced_permutations(blank_sequence: str, permutation_length: int):
    symbol_string = ''.join(str(i+1) for i in range(permutation_length))

    replaced_perms_with_blank = []
    for i in range(permutation_length):
        replaced_perms_with_blank.append(blank_sequence[i:permutation_length+i])

    replaced_perms = []
    for perm_with_blank in replaced_perms_with_blank:
        replaced_perms.append(utl.replace_blank(perm_with_blank, symbol_string))
    return replaced_perms


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
        if utl.validate_answer_blank(n, final_schedule_strings):
            for s in utl.insert_emoji(strings, final_schedule_strings):
                print(s, end='\n\n')
            print(f'Score: {final_score}')
            print(f'Time: {round(time.time()-start_time, 2)} seconds')
