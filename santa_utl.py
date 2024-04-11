from itertools import permutations
import random


def validate_answer(n_of_symbols: int, n_of_schedules: int, final_schedule_strings: list):
    symbol_string = ''.join(str(i+1) for i in range(n_of_symbols))
    mandatory_perms = list_mandatory_permutations(symbol_string)
    regular_perms = list_regular_permutations(symbol_string, mandatory_perms)

    all_okay = True
    # Conditions testing
    for perm in regular_perms:
        not_in_string = 0
        for s in range(n_of_schedules):
            if perm not in final_schedule_strings[s]:
                not_in_string += 1
        if not_in_string == n_of_schedules:
            print(f"Permutation '{perm}' missing")
            all_okay = False
    for perm in mandatory_perms:
        for s in range(n_of_schedules):
            if perm not in final_schedule_strings[s]:
                print(f"Obligatory permutation '{perm}' missing from shcedule {s+1}")
                all_okay = False
    if all_okay:
        print("All okay")
    return all_okay


def validate_answer_blank(n_of_symbols: int, schedule_strings: list, blank='*'):
    symbols = ''.join(str(i+1) for i in range(n_of_symbols))
    mandatory = list_mandatory_permutations(symbols)
    regular = list_regular_permutations(symbols, mandatory)

    perms_in_schedules = []
    for sched in schedule_strings:
        perms_in_schedules.append(extract_substrings_blank(sched, symbols, blank=blank))

    all_okay = True

    for perm in regular:
        found = False
        for sched in perms_in_schedules:
            if perm in sched:
                found = True
                break
        if not found:
            print(f"Permutation '{perm}' missing")
            all_okay = False

    for perm in mandatory:
        for i, sched in enumerate(perms_in_schedules):
            if perm not in sched:
                print(f"Obligatory permutation '{perm}' missing from shcedule {i+1}")
                all_okay = False

    if all_okay:
        print("All okay")
    return all_okay


def insert_emoji(n_of_schedules: int, final_schedule_strings: list) -> list:
    emoji_dict = {'1': '🎅', '2': '🤶', '3': '🦌', '4': '🧝', '5': '🎄', '6': '🎁', '7': '🎀', '*': '🌟'}

    for i in range(n_of_schedules):
        for number, emoji in emoji_dict.items():
            final_schedule_strings[i] = final_schedule_strings[i].replace(number, emoji)

    return final_schedule_strings


def list_all_permutations(symbol_string: str) -> list:
    return [''.join(p) for p in permutations(symbol_string)]


def list_mandatory_permutations(symbol_string: str) -> list:
    return ['12' + ''.join(p) for p in permutations(symbol_string[2:])]


def list_regular_permutations(symbol_string: str, mandatory_permutations: list) -> list:
    return [''.join(p) for p in permutations(symbol_string) if ''.join(p) not in mandatory_permutations]


def check_score(schedule: list, permutation_length: int) -> int:
    merged = merge_permutations(schedule, permutation_length)
    return len(merged)


def merge_permutations(permutation_sequence: list, permutation_length: int) -> str:
    schedule_string = ''
    for i in range(len(permutation_sequence)):
        nextperm = permutation_sequence[i]
        distance = calculate_distance(permutation_length, schedule_string, nextperm)
        schedule_string += nextperm[-distance:]
    return schedule_string


def merge_permutations_blank(permutation_sequence: list, symbols: str, blank='*') -> str:
    schedule_string = ''
    for perm in permutation_sequence:
        distance = calculate_distance_blank(symbols, schedule_string, perm, blank)
        schedule_string += perm[-distance:]
        if (blank_pos := perm.find(blank)) != -1:
            replace_pos = blank_pos - len(symbols)
            schedule_string = blank.join(schedule_string.rsplit(schedule_string[replace_pos], 1))
    return schedule_string


def schedules_as_strings(schedules: list, n_of_symbols: int) -> list:
    schedule_strings = []
    for sched in schedules:
        sched_str = merge_permutations(sched, n_of_symbols)
        schedule_strings.append(sched_str)
    return schedule_strings


def schedules_as_strings_blank(schedules: list, symbols: str, blank='*') -> list:
    schedule_strings = []
    for sched in schedules:
        sched_str = merge_permutations_blank(sched, symbols, blank)
        schedule_strings.append(sched_str)
    return schedule_strings


def calculate_distance(permutation_length: int, first: str, second: str) -> int:
    if second == '*':
        return 1
    last_perm = first[-permutation_length:]
    if last_perm == '':
        return permutation_length
    for distance in range(permutation_length+1):
        if last_perm[distance:] == second[:permutation_length-distance]:
            return distance


def calculate_distance_blank(symbols: str, first: str, second: str, blank='*') -> int:
    if second == blank:
        return 1
    permutation_length = len(symbols)
    for distance in range(permutation_length+1):
        if blank_compare(first[distance-permutation_length:], second[:permutation_length-distance]):
            return distance
    return distance


def blank_compare(first: str, second: str, blank: str = '*'):
    for f, s in zip(first, second):
        if not (f == s or f == blank or s == blank):
            return False
    return True


def calculate_final_score(schedule_strings: list) -> int:
    score = 0
    for sched_str in schedule_strings:
        temp_score = len(sched_str)
        if temp_score > score:
            score = temp_score
    return score


def extract_substrings(sequence: str, substring_length: int, verbose=False, skip_duplicates=True) -> list:
    substrings = []
    for i in range(len(sequence)-substring_length+1):
        permutation = sequence[i:i+substring_length]
        if verbose:
            print(f"{permutation} ({i+1})")
        if not skip_duplicates or permutation not in substrings:
            substrings.append(permutation)
    return substrings


def extract_substrings_blank(sequence: str, symbol_string: str, verbose=False, skip_duplicates=True, blank='*') -> list:
    substrings = []
    for i in range(len(sequence)-len(symbol_string)+1):
        sub_str = sequence[i:i+len(symbol_string)]
        sub_str = replace_blank(sub_str, symbol_string)
        if verbose:
            print(f"{sub_str} ({i+1})")
        if not skip_duplicates or sub_str not in substrings:
            substrings.append(sub_str)
    return substrings


def replace_blank(permutation: str, symbols: str, blank: str = '*') -> str:
    if blank in permutation:
        for s in symbols:
            if s not in permutation:
                return permutation.replace(blank, s)
    return permutation


def check_end(regular_left: list, mandatory_left: list):
    if regular_left:
        return False
    for sched_mandatory in mandatory_left:
        if sched_mandatory:
            return False
    return True


def list_nearest_neighbours(permutation_length: int, permutation: str, neighbours_list: list):
    shortest_distance = permutation_length
    nearest_neighbours = []

    for neighbour in neighbours_list:
        distance = calculate_distance(permutation_length, permutation, neighbour)
        if distance < shortest_distance:
            shortest_distance = distance
            nearest_neighbours.clear()
            nearest_neighbours.append(neighbour)
        elif distance == shortest_distance:
            nearest_neighbours.append(neighbour)

    return nearest_neighbours


def get_random_nearest(permutation_length: int, permutation: str, neighbours_list: list):
    nearest_neighbours = list_nearest_neighbours(permutation_length, permutation, neighbours_list)
    if nearest_neighbours:
        return random.choice(nearest_neighbours)
    return None
