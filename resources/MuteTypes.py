import json


def get_value(obj):
    try:
        return obj.value[0]
    except:
        return obj


class MuteNum:
    def __init__(self, value):
        # Mutable storage because `list` defines a location
        self.value = [value]

    def __dict__(self):
        return self.value[0].__dict__

    def __set__(self, value):
        self.value[0] = get_value(value)

    def __str__(self):
        return get_value(self).__str__()

    # Define the comparison interface
    def __eq__(self, other):
        return get_value(self) == get_value(other)

    def __ne__(self, other):
        return get_value(self) != get_value(other)

    def __le__(self, other):
        return get_value(self) <= get_value(other)

    def __lt__(self, other):
        return get_value(self) < get_value(other)

    def __ge__(self, other):
        return get_value(self) >= get_value(other)

    def __gt__(self, other):
        return get_value(self) > get_value(other)

    # Define the numerical operator interface, returning new instances
    # of mutable_number
    def __add__(self, other):
        return MuteNum(self.value[0] + get_value(other))

    def __radd__(self, other):
        return MuteNum(get_value(other) + self.value[0])

    def __sub__(self, other):
        return MuteNum(self.value[0] - get_value(other))

    def __rsub__(self, other):
        return MuteNum(get_value(other) - self.value[0])

    def __mul__(self, other):
        return MuteNum(self.value[0] * get_value(other))

    def __rmul__(self, other):
        return MuteNum(get_value(other) * self.value[0])

    def __truediv__(self, other):
        return MuteNum(self.value[0] / get_value(other))

    def __rtruediv__(self, other):
        return MuteNum(get_value(other) / self.value[0])

    def __mod__(self, other):
        return MuteNum(self.value[0] % get_value(other))

    def __rmod__(self, other):
        return MuteNum(get_value(other) % self.value[0])

    def __pow__(self, power, modulo=None):
        return MuteNum(self.value[0] ** get_value(power))

    def __rpow__(self, other):
        return MuteNum(get_value(other) ** self.value[0])

    def __neg__(self):
        return MuteNum(-self.value[0])

    # In-place operations alter the shared location
    def __iadd__(self, other):
        self.value[0] += get_value(other)
        return self

    def __isub__(self, other):
        self.value[0] -= get_value(other)
        return self

    def __imul__(self, other):
        self.value[0] *= get_value(other)
        return self

    def __idiv__(self, other):
        self.value[0] /= get_value(other)
        return self

    def __imod__(self, other):
        self.value[0] %= get_value(other)
        return self

    # Logic operators
    def __invert__(self):
        return MuteNum(~self.value[0])

    def __and__(self, other):
        return MuteNum(self.value[0] & get_value(other))

    def __rand__(self, other):
        return MuteNum(get_value(other) & self.value[0])

    def __or__(self, other):
        return MuteNum(self.value[0] | get_value(other))

    def __ror__(self, other):
        return MuteNum(get_value(other) | self.value[0])

    def __xor__(self, other):
        return MuteNum(self.value[0] ^ get_value(other))

    def __rxor__(self, other):
        return MuteNum(get_value(other) ^ self.value[0])

    def __index__(self):
        return self.value[0]

    # Define the copy interface
    def __copy__(self):
        new = MuteNum(0)
        new.value = self.value
        return new

    def __repr__(self):
        return repr(self.value[0])

    def __bool__(self):
        return self.value[0].__bool__()


class MuteBool:
    def __init__(self, value):
        self.value = [value]

    def __dict__(self):
        return self.value[0].__dict__

    def __set__(self, value):
        self.value[0] = get_value(value)

    def __str__(self):
        return get_value(self).__str__()

    def __repr__(self):
        return repr(self.value[0])

    def __and__(self, other):
        return get_value(self) and get_value(other)

    def __or__(self, other):
        return get_value(self) or get_value(other)

    def __rand__(self, other):
        return get_value(other) and get_value(self)

    def __ror__(self, other):
        return get_value(other) or get_value(self)

    def __xor__(self, other):
        return get_value(self) ^ get_value(other)

    def __rxor__(self, other):
        return get_value(other) ^ get_value(self)

    def __bool__(self):
        return self.value[0]


class MuteStr:
    def __init__(self, value=""):
        self.value = [value]

    def __dict__(self):
        return self.value[0].__dict__

    def __set__(self, value):
        self.value[0] = get_value(value)

    def __add__(self, other):
        return MuteStr(self.value[0] + get_value(other))

    def __contains__(self, item):
        return get_value(item) in self.value[0]

    def __eq__(self, other):
        return self.value[0] == get_value(other)

    def __getitem__(self, item):
        return self.value[0].__getitem__(item)

    def __ge__(self, other):
        return self.value[0] >= get_value(other)

    def __gt__(self, other):
        return self.value[0] > get_value(other)

    def __hash__(self):
        return hash(self.value[0])

    def __iter__(self):
        return iter(self.value[0])

    def __len__(self):
        return len(self.value[0])

    def __le__(self, other):
        return self.value[0] <= get_value(other)

    def __lt__(self, other):
        return self.value[0] < get_value(other)

    def __mod__(self, other):
        return MuteStr(self.value[0] % get_value(other))

    def __mul__(self, other):
        return MuteStr(self.value[0] * get_value(other))

    def __ne__(self, other):
        return self.value[0] != get_value(other)

    def __rmod__(self, other):
        return MuteStr(get_value(other) % self.value[0])

    def __rmul__(self, other):
        return MuteStr(get_value(other) * self.value[0])

    def __sizeof__(self):
        return self.value[0].__sizeof__()

    def __str__(self):
        return self.value[0]

    def __repr__(self):
        return repr(self.value[0])


class MuteBytes:
    def __init__(self, value=b""):
        self.value = [value]

    def __dict__(self):
        return self.value[0].__dict__

    def __set__(self, value):
        self.value[0] = get_value(value)

    def __add__(self, other):
        return MuteBytes(self.value[0] + get_value(other))

    def __contains__(self, item):
        return self.value[0].__contains__(get_value(item))

    def __eq__(self, other):
        return self.value[0] == get_value(other)

    def __getitem__(self, item):
        return self.value[0].__getitem__(get_value(get_value(item)))

    def __ge__(self, other):
        return self.value[0] >= get_value(other)

    def __gt__(self, other):
        return self.value[0] > get_value(other)

    def __hash__(self):
        return hash(self.value[0])

    def __iter__(self):
        self.value[0].__iter__()

    def __len__(self):
        return self.value[0].__len__()

    def __le__(self, other):
        return self.value[0] >= get_value(other)

    def __lt__(self, other):
        return self.value[0] > get_value(other)

    def __mod__(self, other):
        return MuteBytes(self.value[0] % get_value(other))

    def __mul__(self, other):
        return MuteBytes(self.value[0] * get_value(other))

    def __ne__(self, other):
        return self.value[0] != get_value(other)

    def __rmod__(self, other):
        return MuteBytes(get_value(other) % self.value[0])

    def __rmul__(self, other):
        return MuteBytes(get_value(other) * self.value[0])

    def __str__(self):
        return self.value[0].__str__()

    def __repr__(self):
        return repr(self.value[0])


class MuteEncoder(json.JSONEncoder):
    def default(self, obj):
        return get_value(obj)
