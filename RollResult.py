import copy
from RollParams import RollParams
from Advantage import Advantage
from random import randint

'''
Defines a class representing the results of a dice roll, according to a RollParams object.
'''
class RollResult:
    '''
    Creates a RollResult instance according to the params argument. While 
    in a RollParams object all outcomes are hypothetical, this class 
    represents the concrete outcome of a roll.
    '''
    def __init__(self, params: RollParams):
        # the params this roll was built from
        self.params: RollParams = params
        # the final total of this roll
        self.total: int = None
        # contains the rolls that this roll was chosen from, if rolled 
        # with (dis)advantage
        self.tries: [RollResult] = []
        # contains the individual die rolls that make up this roll
        self.die_rolls: [int] = []

        # if the roll is made with (dis)advantage, we make two rolls with 
        # the same params as this object, and then choose the appropriate one
        if self.params.advantage is not Advantage.NONE:
            # copy the params and set the advantage state
            params_without_advantage = copy.deepcopy(self.params)
            params_without_advantage.set_advantage(Advantage.NONE)

            # make the two rolls and save them
            self.tries.append(RollResult(params_without_advantage))
            self.tries.append(RollResult(params_without_advantage))

            # determine whether the best or worst roll should be chosen and sort the tries
            # accordingly
            highest_first = True if self.params.advantage is Advantage.ADVANTAGE else False
            self.tries.sort(key=(lambda roll_result : roll_result.total), reverse=highest_first)

            # store the relevant roll information into this object
            chosen_try = self.tries[0]
            self.total = chosen_try.total
            self.die_rolls = chosen_try.die_rolls
        # if the roll isn't made with (dis)advantage, roll the dice and store the results
        else:
            # roll each die and store the individual results
            for _ in range(self.params.quantity):
                self.die_rolls.append(randint(1, self.params.sides))

            # calculate the total
            total_ex_modifier = sum(self.die_rolls)
            signed_modifier = 0
            if self.params.modifier:
                if self.params.mod_sign == "+":
                    signed_modifier = self.params.modifier
                elif self.params.mod_sign == "-":
                    signed_modifier = self.params.modifier * -1
            self.total = total_ex_modifier + signed_modifier
            self.tries.append(self)
    
    def __str__(self):
        # builds the string detailing the individual die rolls
        die_rolls_clause = f'({" + ".join(str(die_roll) for die_roll in self.die_rolls)})'
        # builds the modifier portion of the roll if present
        modifier_clause = f' {self.params.mod_sign} {self.params.modifier}' if self.params.modifier else ""
        # builds the total portion of the result
        total_clause = f' = {self.total}'
        # builds the portion of the result showing the sub-rolls if made with (dis)advantage
        chosen_from_clause = '\nchosen from:\n%s' % '\n'.join(str(tried_result) for tried_result in self.tries) if self.params.advantage is not Advantage.NONE else ""
        # builds the string used if the roll was made with (dis)advantage
        with_clause = f'\nwith {self.params.advantage.value}' if self.params.advantage is not Advantage.NONE else ""

        return "".join([die_rolls_clause, modifier_clause, total_clause, chosen_from_clause, with_clause])