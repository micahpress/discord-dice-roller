from Advantage import Advantage
from typing import Optional

'''
Defines a class containing all the parameters needed to make a dice roll
of the form <quantity>d<sides>+<modifier>.
'''
class RollParams:
    '''
    Creates a RollParams object with quantity of dice set to quantity, 
    the number of sides of the die set to sides, and an optional modifier
    set to modifier, if present. During instantiation, the advantage state
    is set to Advantage.NONE.
    '''
    def __init__(self, quantity: int, sides: int, modifier: Optional[int], mod_sign: Optional[str]):
        # number of dice to roll
        self.quantity: int = quantity
        # number of sides on the die to use
        self.sides: int = sides
        # optional post-roll modifier
        self.modifier: Optional[int] = modifier
        # sign of the modifier if present
        self.mod_sign: Optional[str] = mod_sign
        # advantage state for the roll
        self.advantage: Advantage = Advantage.NONE
    
    def __str__(self) -> str:
        # builds the <quantity>d<sides> portion of a roll
        dice_clause = f'{self.quantity}d{self.sides}'
        # builds the +/-<modifier> portion
        modifier_clause = f' {self.mod_sign} {self.modifier}' if self.modifier else ""
        # builds the advantage description of a roll
        advantage_clause = f' with {self.advantage.value}' if self.advantage is not Advantage.NONE else ""

        return "".join([dice_clause, modifier_clause, advantage_clause])
    
    '''
    Sets the advantage state of this RollParams object to advantage. It can 
    be either ADVANTAGE, DISADVANTAGE, or NONE.
    '''
    def set_advantage(self, advantage: Advantage) -> None:
        self.advantage = advantage

    '''
    Returns the expected value of a dice roll according to the parameters 
    set in this object.
    '''
    def calculate_expected_value(self) -> int:
        quantity_times_ev = (self.quantity * ((self.sides + 1) / 2))
        return (quantity_times_ev + self.modifier) if self.mod_sign == "+" else (quantity_times_ev - self.modifier)