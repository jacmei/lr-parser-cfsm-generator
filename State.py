class State:

    # bases : list
    # closures : list
    # conflicts : set
    def __init__(self, value, bases, closures, conflicts = set()):
        self._value = value
        self._bases = bases
        self._closures = closures
        self._conflicts = conflicts
    
    def __repr__(self):
        return "State([Number: " + repr(self._value) + "] [" + repr(self._bases) + "] [" + repr(self._closures) + "])"
    
    def __eq__(self, other):
        if isinstance(other, State):
            return self._bases == other._bases
        else:
            return NotImplemented