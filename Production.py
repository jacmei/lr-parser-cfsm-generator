class Production:

    # LHS : str
    # RHS : list
    def __init__(self, LHS, RHS):
        self._LHS = LHS
        self._RHS = RHS
    
    def __repr__(self):
        r = ""
        for sym in self._RHS:
            r += sym + " "
        return "Production([" + self._LHS + "] : [" + r.rstrip() + "])"

