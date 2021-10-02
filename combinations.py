def GetCombinationsBitwise(array):
    sz = len(array)
    all_combinations = []

    for mask in range((1 << sz)):
        comb = []

        for pos in range(sz):
            if (mask & (1 << pos)):
                comb.append(array[pos])
        all_combinations.append(comb)

    for comb in (all_combinations):
        print(comb)


def main():
    array = [1, 2, 3, 4,5,6,7,8,9,10,11,12,13]
    GetCombinationsBitwise(array)


if __name__ == "__main__":
    main()