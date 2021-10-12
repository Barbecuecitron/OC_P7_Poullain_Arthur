import time


def brute_force(elements):
    if len(elements) == 0:
        return [[]]
    first_element = elements[0]
    # Copy the array without first element
    rest = elements[1:]

    combs_without_first = brute_force(rest)
    combs_with_first = []

    for comb in combs_without_first:
        comb_with_first = [*comb, first_element]
        combs_with_first.append(comb_with_first)
    # If combinations are still possible
    return [*combs_without_first, *combs_with_first]


def try_all_possibilities():
    file = open('resources\\actions_premiere_partie.csv')
    data = file.read()
    file.close()
    # Split file by lines
    file_lines = data.split('\n')
    # Remove line 0
    del (file_lines[0])
    formated_actions = []

    for line in file_lines:
        str_elements = line.split(',')
        element = {'name': str_elements[0],
                   'cost': str_elements[1],
                   'benef': str_elements[2]}
        if float(element['cost']) > 0:
            formated_actions.append(element)
    print(f"Nous allons analyser une liste de {len(formated_actions)} actions")
    print(f"{len(file_lines)- len(formated_actions)} actions ont été retirées de par leur prix (0 ou - )")
    total = 2**len(formated_actions)
    print(f"Nous avions {len(formated_actions)} entrées")
    print(f"Nous devrions trouver {total} combinaisons selon les lois de l'algorithme")
    result = brute_force(formated_actions)

    print(f"Nous avons trouvé {len(result)} possibilités")

    return result


def sort_to_fit_wallet(array_of_actions, money_to_spend):
    buyable_actions = []
    for action in array_of_actions:
        if float(action['total_cost']) <= money_to_spend:
            buyable_actions.append(action)
    return buyable_actions


def main():
    wallet = 500
    # Result of algorithm
    start_time = time.time()
    dict_combinations = try_all_possibilities()
    # Prepare array of dicts for cost, benefits
    combinations_with_properties = []
    # loop through our list of dicts and creates
    for comb in dict_combinations:
        total_price = 0
        benefice = 0
        # For every action :
        for action in comb:
            total_price += float(action['cost'])
            # Calcul du bénéfice
            benefice += float(action['cost']) * float(action['benef']) / 100
        combination = {'total_cost': total_price, 'benefice': benefice, 'action_list': comb}
        combinations_with_properties.append(combination)

    buyable_actions = sort_to_fit_wallet(combinations_with_properties, wallet)
    duration = time.time() - start_time
    print(f"Le calcul de possibilités a pris {duration} secondes")

    sorted_buyable_actions = sorted(buyable_actions, key=lambda action: action['benefice'], reverse=True)
    for i in range(3):
        print(f"\n{i + 1} - Bénéfice : {sorted_buyable_actions[i]['benefice']}\n"
              f"Coût : {sorted_buyable_actions[i]['total_cost']}\n"
              f"Actions à acheter : {sorted_buyable_actions[i]['action_list']}\n")


if __name__ == '__main__':
    main()
