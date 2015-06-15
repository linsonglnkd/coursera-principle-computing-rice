"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """

    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score
    """
    score_dict = {}
    for number in hand:
        score_dict[number] = score_dict.get(number,0) + number
    score_array = score_dict.values()
    score_array.sort(reverse = True)
    return score_array[0]

hand = (1,1,3,8)
print score(hand)

def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    outcome = range(1, num_die_sides+1)
    all_trials = gen_all_sequences(outcome, num_free_dice)
    sum_score = 0.0
    for each_trial in all_trials:
        held_dice_list = list(held_dice)
        held_dice_list.extend(each_trial)
        held_dice_list.sort()
        hand = tuple(held_dice_list)
        sum_score += score(hand)
    return sum_score / len(all_trials)

def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    hand = list(hand)
    hand.sort()
    hand = tuple(hand)
    answer_set = []
    length = len(hand)
    for dummy_i in range(2**length):
        temp_set = []
        for index in range(length):
            # if i-th bit is 1
            if ((2 ** index) & dummy_i) > 0:
                temp_set.append(hand[index])
        answer_set.append(tuple(temp_set))
    return set(answer_set)   

def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    best_held = None
    best_score = -1.0
    all_held = gen_all_holds(hand)
    for each in all_held:
        num_free_dice = len(hand) - len(each)
        current_score = expected_value(each, num_die_sides, num_free_dice)
        if current_score > best_score:
            best_held = each
            best_score = current_score
    return (best_score, best_held)

print strategy((1,),6)

def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score


run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
