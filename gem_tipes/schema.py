from enum import Enum

class GemClarity(int,Enum):
    SI = 1
    VS = 2
    VVS = 3
    FL = 4

class GemColor(str,Enum):
    D = "D"
    E = "E"
    F = "F"
    G = "G"
    H = "H"
    I = "I"

class GemType(str,Enum):
    DIAMOND = "DIAMOND"
    RUBY = "RUBY"
    EMERALD = "EMERALD"
