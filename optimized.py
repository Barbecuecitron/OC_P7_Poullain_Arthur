import time


def can_buy(money_left, action_cost):
    if money_left - float(action_cost) >= 0:
        return True
    return False


def get_the_most_of_budget(actions, budget):
    actions_to_buy = []
    # Actions sorted by density
    best_actions = actions
    profit = 0
    actions_sorted_by_cheaper = sorted(actions, key=lambda action: action['cost'], reverse=True)
    cheaper_action_index = 0
    money_left = budget
    buying_index = 0

    # As long as our current money allows us to buy at least the cheapest action
    # We will continue. If not, looping is unnecessary and we will abort it.
    while money_left >= float(actions_sorted_by_cheaper[cheaper_action_index]['cost']):
        # If we can afford the best action
        if can_buy(money_left, best_actions[buying_index]['cost']):
            # Buy it
            actions_to_buy.append(best_actions[buying_index])
            money_left = money_left - float(best_actions[buying_index]['cost'])
            profit += float(best_actions[buying_index]['benef'])

            # If the action we are buying is the cheapest one, we must let the program know
            # if best_actions[buying_index] == actions_sorted_by_cheaper[cheaper_action_index]:
            # let's remove the actual cheaper one from the list
            actions_sorted_by_cheaper.remove(best_actions[buying_index])
        # Now we repeat on the previous action until we run out of budget
        buying_index += 1
    resultat = {"money_left": money_left, "profit": profit, "actions_to_buy": actions_to_buy}
    return resultat


def get_actions_from_files():
    # With open as
    file = open('resources\\dataset2_Python+P7.csv')
    data = file.read()
    file.close()
    # Split file by lines
    file_lines = data.split('\n')
    # Remove line 0
    del (file_lines[0])
    formated_actions = []

    for line in file_lines:
        str_elements = line.split(',')
        # Let's not add negative cost / benefits
        if float(str_elements[1]) > 0 and float(str_elements[2]) > 0:
            element = {'name': str_elements[0],
                       'cost': str_elements[1],
                       'percent_benef': str_elements[2],
                       # Le benef = au cout * %benefice / 100
                       'benef': float(str_elements[1]) * float(str_elements[2]) / 100,
                       # La densité est le résultat du benef / cout
                       'densite': float(str_elements[2]) / float(str_elements[1])
                       }

            formated_actions.append(element)
    # print(f"Les formated actions sont {formated_actions}")
    # print(formated_actions)
    return formated_actions


def main():
    wallet = 500
    # Result of algorithm
    start_time = time.time()
    actions = get_actions_from_files()
    print(f"Lancement de l'analyse de {len(actions)} action(s).")
    # Turns out that we have best results according to benef rather than density
    actions_by_density = sorted(actions, key=lambda action: action['densite'], reverse=True)
    actions_by_benef = sorted(actions, key=lambda action: action['benef'], reverse=True)

    # For security reasons, we will always try two different algorithms & compare them,
    # One based on pure benefits in €, the other in density, which is basically the benefits to cost ratio.
    # This aims at always having a "parachute" optimized result if the action with the biggest benefit prevents us
    # from buying more cost efficient, but less pricy actions.
    # Since they are absolutely inexpensive "ressourcewise" we can allow
    # Both running in a linear manner and compare them.
    density_comparison = get_the_most_of_budget(actions_by_density, wallet)
    benefits_comparison = get_the_most_of_budget(actions_by_benef, wallet)
    worst_choice = None
    best_choice = None

    if density_comparison['profit'] > benefits_comparison['profit']:
        best_choice = density_comparison
        worst_choice = benefits_comparison
    else:
        best_choice = benefits_comparison
        worst_choice = density_comparison

    print(
        f"\nIl nous reste {best_choice['money_left']} € sur {wallet} € de budget de départ. ")

    print(
        f"Nous avons un profit total de : {best_choice['profit']} € répartis sur {len(best_choice['actions_to_buy'])} "
        f"action(s).")
    print(
        f"Le choix secondaire nous rapportait {worst_choice['profit']} € répartis sur "
        f"{len(worst_choice['actions_to_buy'])} action(s).")

    for action in best_choice["actions_to_buy"]:
        print(action)

    duration = time.time() - start_time
    print(f"Le calcul de possibilités a pris {duration} secondes")


if __name__ == '__main__':
    main()
