import random
import time
import copy
import sys
import santa_utl as utl

# random.seed(1)


def nn_schedules_blank(n_of_symbols: int, n_of_schedules: int):
    # Create string of symbols
    symbols = ''.join(str(i+1) for i in range(n_of_symbols))

    # Create list of all permutations as strings
    mandatory = utl.list_mandatory_permutations(symbols)
    regular_left = utl.list_regular_permutations(symbols, mandatory)
    mandatory_left = []
    for _ in range(n_of_schedules):
        mandatory_left.append(copy.deepcopy(mandatory))

    # Beginning of Nearest Neighbour Algorithm
    schedules = []
    for _ in range(n_of_schedules):
        schedules.append([''])

    end = False
    iteration = 1
    while not end:
        print(f'Iteration: {iteration}\n'
              f'{len(regular_left)} regular permutations left\n'
              f'{sum([len(m) for m in mandatory_left])} mandatory permutations left')
        iteration += 1
        for sched, sched_mandatory in zip(schedules, mandatory_left):
            neighbour = utl.get_random_nearest(n_of_symbols, sched[-1], sched_mandatory+regular_left)
            if neighbour is None:
                continue
            sched.append(neighbour)
            # Removing chosen neightbour from list
            if neighbour[:2] == '12':
                sched_mandatory.remove(neighbour)
            else:
                regular_left.remove(neighbour)

        # End condition
        if end := utl.check_end(regular_left, mandatory_left):
            print('Added all permutations')

    print('Adding blanks')
    for sched in schedules:
        add_blanks(symbols, sched)

    shedule_strings = utl.schedules_as_strings_blank(schedules, symbols)
    print('The end')
    return shedule_strings


def add_blanks(symbols: str, permutation_list: list, blank='*'):
    replace_idx_1 = None
    replace_s_1 = None

    replace_idx_2 = None
    replace_s_2 = None

    best_dist_1 = len(symbols)
    best_dist_2 = len(symbols)

    for current_idx in range(len(permutation_list)-1):
        first = permutation_list[current_idx]
        second = permutation_list[current_idx+1]
        distance = utl.calculate_distance_blank(symbols, first, second)
        if distance == len(symbols):
            current_symbol, current_dist = find_best_blank(symbols, first, second)
            if current_dist < best_dist_1:
                if replace_idx_1 is None:
                    best_dist_1 = current_dist
                    replace_s_1 = current_symbol
                    replace_idx_1 = current_idx
                elif check_blank_distance(permutation_list, replace_idx_1, current_idx, replace_s_1, current_symbol, symbols) and best_dist_1 < best_dist_2:
                    best_dist_2 = best_dist_1
                    replace_s_2 = replace_s_1
                    replace_idx_2 = replace_idx_1
                    best_dist_1 = current_dist
                    replace_s_1 = current_symbol
                    replace_idx_1 = current_idx
            elif current_dist < best_dist_2 and check_blank_distance(permutation_list, replace_idx_1, current_idx, replace_s_1, current_symbol, symbols):
                best_dist_2 = current_dist
                replace_s_2 = current_symbol
                replace_idx_2 = current_idx

    if replace_idx_1 is not None and replace_s_1 is not None:
        permutation_list[replace_idx_1] = permutation_list[replace_idx_1].replace(replace_s_1, blank)
    if replace_idx_2 is not None and replace_s_2 is not None:
        permutation_list[replace_idx_2] = permutation_list[replace_idx_2].replace(replace_s_2, blank)


def check_blank_distance(permutation_list: list, first_idx: int, second_idx: int, first_symbol: str, second_symbol: str, symbols: str, blank: str = '*') -> bool:
    if first_idx < second_idx:
        merge = permutation_list[first_idx:second_idx+1]
        merge[0] = merge[0].replace(first_symbol, blank)
        merge[-1] = merge[-1].replace(second_symbol, blank)
    else:
        merge = permutation_list[second_idx:first_idx+1]
        merge[0] = merge[0].replace(second_symbol, blank)
        merge[-1] = merge[-1].replace(first_symbol, blank)
    merge = utl.merge_permutations_blank(merge, symbols)
    distance = len(merge.split(blank)[1])
    return distance >= len(symbols)


def find_best_blank(symbols: str, first: str, second: str, blank='*'):
    core = first[1:]
    best_distance = len(symbols)
    to_replace = None
    for s in core:
        replacement = first[0] + core.replace(s, blank)
        current_dist = utl.calculate_distance_blank(symbols, replacement, second)
        if current_dist < best_distance:
            best_distance = current_dist
            to_replace = s
    return to_replace, best_distance


def list_nearest_neighbours_blank(symbols: str, permutation: str, neighbours_list: list):
    nearest_neighbours = []
    shortest_distance = len(symbols)
    for neighbour in neighbours_list:
        distance = utl.calculate_distance_blank(symbols, permutation, neighbour)
        if distance < shortest_distance:
            shortest_distance = distance
            nearest_neighbours.clear()
            nearest_neighbours.append(neighbour)
        elif distance == shortest_distance:
            nearest_neighbours.append(neighbour)

    return nearest_neighbours


def get_random_nearest_blank(symbols: str, permutation: str, neighbours_list: list):
    nearest_neighbours = list_nearest_neighbours_blank(symbols, permutation, neighbours_list)
    if nearest_neighbours:
        return random.choice(nearest_neighbours)
    return None


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Nearest neighbour requires two parameters: 'number of symbols' and 'number of schedules'")
    else:
        start_time = time.time()
        n = int(sys.argv[1])
        strings = int(sys.argv[2])
        final_schedule_strings = nn_schedules_blank(n, strings)
        final_score = utl.calculate_final_score(final_schedule_strings)
        for s in final_schedule_strings:
            print(s, end='\n\n')
        if utl.validate_answer_blank(n, final_schedule_strings):
            for s in utl.insert_emoji(strings, final_schedule_strings):
                print(s, end='\n\n')
            print(f'Score: {final_score}')
            print(f'Time: {round(time.time()-start_time, 2)} seconds')
