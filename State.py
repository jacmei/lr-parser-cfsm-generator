class State:

    # bases : list
    # closures : list
    def __init__(self, num, bases, closures):
        self._num = num
        self._bases = bases
        self._closures = closures
    
    def __repr__(self):
        return "State([Number: " + repr(self._num) + "] [" + repr(self._bases) + "] [" + repr(self._closures) + "])"