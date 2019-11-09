class ProductionState:

    # production : Production
    # progress : int
    # action : str
    # goto : int
    def __init__(self, production, progress, action = "", goto = ""):
        self._production = production
        self._progress = progress
        self._action = action
        self._goto = goto
    
    def __repr__(self):
        return "ProductionState([" + repr(self._production) + "], [Progress : " + repr(self._progress) + "], [Action : " + self._action + "], [Goto : " + self._goto + "])"