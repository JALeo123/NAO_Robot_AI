import random

def get_question():
    nums = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    nums_org = nums.copy()
    nums_value = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    check = 0
    val_1 = random.choice(nums_value)

    while(check == 0):
        val_2 = random.choice(nums_value)
        if(val_1 + val_2 > 9):
            ind = nums_value.index(val_2)
            nums_value.remove(val_2)
            nums.pop(ind)
        else:
            question = "What is " + nums_org[val_1] + " plus " + nums_org[val_2]
            answer = val_1 + val_2
            check = 1

    return question, answer