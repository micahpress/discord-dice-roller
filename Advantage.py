from enum import Enum, unique, auto

'''
Defines enums for the different advantage states of a roll.
'''
@unique
class Advantage(Enum):
    ADVANTAGE = "advantage"
    DISADVANTAGE = "disadvantage"
    NONE = ""