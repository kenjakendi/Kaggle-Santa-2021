import sys
import time
import copy
import santa_utl as utl

# random.seed(1)


def nn_schedules(n_of_symbols: int, n_of_schedules: int):
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
            print("The End")

    shedule_strings = utl.schedules_as_strings(schedules, n_of_symbols)
    return shedule_strings, schedules


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Nearest neighbour requires two parameters: 'number of symbols' and 'number of schedules'")
    else:
        start_time = time.time()
        n = int(sys.argv[1])
        strings = int(sys.argv[2])
        final_schedule_strings = nn_schedules(n, strings)[0]
        final_score = utl.calculate_final_score(final_schedule_strings)
        for s in final_schedule_strings:
            print(s, end='\n\n')
        if utl.validate_answer(n, strings, final_schedule_strings):
            for s in utl.insert_emoji(strings, final_schedule_strings):
                print(s, end='\n\n')
            print(f'Score: {final_score}')
            print(f'Time: {round(time.time()-start_time, 2)} seconds')
