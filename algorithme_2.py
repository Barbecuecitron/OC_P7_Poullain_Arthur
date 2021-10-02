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
    # We will increment the cheaper action index instead in the list instead of reorganizing the list
    # To optimize the result
    actions_sorted_by_cheaper = sorted(actions, key= lambda action:action['cost'], reverse=True)
    cheaper_action_index = 0
    # Initialize our money as the client's budget from parameter
    money_left = budget
    # We will buy index 0 since it's the best of all
    # And increment it instead of reorganizing the list, just like we did with the cheapest action
    # This way we don't need any looping / slowing process.
    buying_index = 0

    # As long as our current money allows us to buy at least the cheapest action
    # We will try to get the next best action to buy
    while money_left >= float(actions_sorted_by_cheaper[cheaper_action_index]['cost']):
        # If we can afford the best action
        if can_buy(money_left, best_actions[buying_index]['cost']):
            # Buy it
            actions_to_buy.append(best_actions[buying_index])
            money_left = money_left - float(best_actions[buying_index]['cost'])
            profit += float(best_actions[buying_index]['benef'])
            # If the action we are buying is the cheapest one, we must let the program know
            # The cheapest is now the old cheapest + 1
            if best_actions[buying_index] == actions_sorted_by_cheaper[cheaper_action_index]:
                cheaper_action_index += 1
        # Now we repeat on the next action until we run out of budget
        buying_index+=1
    print(f"Nous n'avons plus d'argent à dépenser")
    print(f"Il nous reste {money_left} € ")
    print(f"Nous avons un profit total de :{profit} € établi sur {len(actions_to_buy)} actions.")
    #print(actions_to_buy)

def get_actions_from_files():
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
        if float(str_elements[1]) and float(str_elements[2]) > 0:
            element = {'name' : str_elements[0],
                       'cost' : str_elements[1],
                       'benef' : str_elements[2],
                       # La densité est le résultat du benef / cout
                       'densite': float(str_elements[2]) / float(str_elements[1])
                       }

        if float(element['cost']) > 0:
            formated_actions.append(element)
   # print(f"Les formated actions sont {formated_actions}")
    print(f"Nous allons analyser une liste de {len(formated_actions)} actions")
    #print(formated_actions)
    return formated_actions



def main():
    wallet = 500
    # Result of algorithm
    start_time = time.time()
    actions = get_actions_from_files()
    actions_by_density = sorted(actions, key=lambda action: action['densite'], reverse=True)
    get_the_most_of_budget(actions_by_density, wallet)

    duration = time.time() - start_time
    print(f"Le calcul de possibilités a pris {duration} secondes")

if __name__ == '__main__':
    main()