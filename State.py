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
        return "State([Number: " + repr(self._num) + "] [" + repr(self._bases) + "] [" + repr(self._closures) + "])"