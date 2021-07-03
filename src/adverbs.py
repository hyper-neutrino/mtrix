@Hyper("Ξ", "¹")
def filter_over(link):
    if link.arity == 0:
        return attrdict(arity = 1, call = lambda x: filter(lambda a: ut(link.call)(), make_iterable(x, make_range = True)))
    elif link.arity == 1:
        return attrdict(arity = 1, call = lambda x: filter(ut(link.call), make_iterable(x, make_range = True)))
    else:
        return attrdict(arity = 2, call = lambda x, y: filter(lambda a: ut(link.call)(a, y), make_iterable(x, make_range = True)))

@Hyper("υ", "Σ")
def deep_recurse(link):
    def _inner(*x):
        if isinstance(x[0], (list, sequence)):
            return ut(link.call)(map(lambda a: _inner(a, *x[1:]), x[0]), *x[1:])
        return x[0]
    return attrdict(arity = max(link.arity, 1), call = _inner)

@Adverb("φ", lambda x: len(x) == 1, fail = lambda inner, links, outerindex: nth_link_nilad([attrdict(arity = 0, call = lambda: 1)], links, outerindex))
def nth_link_nilad(inner, links, outerindex):
    position = (inner[0].call(*map(lambda k: verbs[k].call(), ["α", "ω"][:inner[0].arity])) - 1) % (len(links) - 1)
    if position >= outerindex:
        position += 1
    return attrdict(arity = 0, call = lambda: trampoline(links[position], []))

@Adverb("χ", lambda x: len(x) == 1, fail = lambda inner, links, outerindex: nth_link_nilad([attrdict(arity = 0, call = lambda: 1)], links, outerindex))
def nth_link_monad(inner, links, outerindex):
    position = (inner[0].call(*map(lambda k: verbs[k].call(), ["α", "ω"][:inner[0].arity])) - 1) % (len(links) - 1)
    if position >= outerindex:
        position += 1
    return attrdict(arity = 1, call = lambda x: trampoline(links[position], [x]))

@Adverb("ψ", lambda x: len(x) == 1, fail = lambda inner, links, outerindex: nth_link_nilad([attrdict(arity = 0, call = lambda: 1)], links, outerindex))
def nth_link_dyad(inner, links, outerindex):
    position = (inner[0].call(*map(lambda k: verbs[k].call(), ["α", "ω"][:inner[0].arity])) - 1) % (len(links) - 1)
    if position >= outerindex:
        position += 1
    return attrdict(arity = 2, call = lambda x, y: trampoline(links[position], [x, y]))

@Adverb("?", lambda x: len(x) == 3, fail = lambda inner, links, outerindex: conditional(inner, links, outerindex))
def conditional(inner, links, outerindex):
    if len(inner) == 0:
        t, f, c = const(1), const(0), verbs["¹"]
    elif len(inner) == 1:
        t, f, c = inner[0], verbs["¹"], verbs["¹"]
    elif len(inner) == 2:
        t, f, c = inner[0], verbs["¹"], inner[1]
    else:
        t, f, c = inner
        return attrdict(arity = max(t.arity, f.arity, c.arity), call = lambda *a: t.call(*a[:t.arity]) if ut(c.call)(*a[:c.arity]) else f.call(*a[:f.arity]))

@Hyper("@", ",")
def swap_arguments(link):
    if link.arity == 0:
        return attrdict(arity = 1, call = lambda x: link.call())
    elif link.arity == 1:
        return attrdict(arity = 2, call = lambda x, y: link.call(y))
    else:
        return attrdict(arity = 2, call = lambda x, y: link.call(y, x))

@Adverb("/", lambda x: len(x) == 1 and x[0].arity != 0 or len(x) == 2)
def ynreduce(inner, links, outerindex):
    call = (lambda x, y: ut(inner[0].call)()) if inner[0].arity == 0 else (lambda x, y: ut(inner[0].call)([x, y])) if inner[0].arity == 1 else ut(inner[0].call)
    return attrdict(arity = 1, call = lambda a: reduce(call, a, default = 0, nwise = ut(inner[1].call)() if len(inner) > 1 else None))

@Adverb("\\", lambda x: len(x) == 1 and x[0].arity != 0 or len(x) == 2)
def yncumulative_reduce(inner, links, outerindex):
    call = (lambda x, y: ut(inner[0].call)()) if inner[0].arity == 0 else (lambda x, y: ut(inner[0].call)([x, y])) if inner[0].arity == 1 else ut(inner[0].call)
    return attrdict(arity = 1, call = lambda a: cumulative_reduce(call, a, nwise = ut(inner[1].call)() if len(inner) > 1 else None))

@Hyper("`", ",")
def reflect_arguments(link):
    if link.arity == 0:
        return attrdict(arity = 1, call = lambda x: link.call())
    elif link.arity == 1:
        return attrdict(arity = 2, call = lambda x, y: link.call(x))
    else:
        return attrdict(arity = 1, call = lambda x: link.call(x, x))

@Adverb("¿", lambda x: len(x) == 2, fail = lambda inner, links, outerindex: while_loop_end_result(inner, links, outerindex))
def while_loop_end_result(inner, links, outerindex):
    if len(inner) == 0:
        raise RuntimeError("`¿` needs at least one link")
    elif len(inner) == 1:
        loop, condition = inner[0], verbs["¹"]
    else:
        loop, condition = inner
    return while_loop(loop, condition)

@Adverb("ʔ", lambda x: len(x) == 2, fail = lambda inner, links, outerindex: while_loop_end_result(inner, links, outerindex))
def while_loop_end_result(inner, links, outerindex):
    if len(inner) == 0:
        raise RuntimeError("`ʔ` needs at least one link")
    elif len(inner) == 1:
        loop, condition = inner[0], verbs["¹"]
    else:
        loop, condition = inner
    return while_loop(loop, condition, keep = True)

@Hyper("‖", "¹")
def filter_against(link):
    if link.arity == 0:
        return attrdict(arity = 1, call = lambda x: filter(lambda a: not ut(link.call)(), make_iterable(x, make_range = True)))
    elif link.arity == 1:
        return attrdict(arity = 1, call = lambda x: filter(lambda a: not ut(link.call)(a), make_iterable(x, make_range = True)))
    else:
        return attrdict(arity = 2, call = lambda x, y: filter(lambda a: not ut(link.call)(a, y), make_iterable(x, make_range = True)))

@Hyper("ᴀS")
class monodirectional_recursive_sequence(sequence):
    def __init__(self, link):
        sequence.__init__(self, self.func)
        self.f = ut(link.call)
        self.arity = link.arity
        self.found = []
    def call(self, *a):
        self.found = list(a)
        return self
    def func(self, index):
        if index < 0:
            raise RuntimeError("cannot get elements left of the origin of a monodirectional recursive sequence")
        else:
            while len(self.found) <= index:
                if self.arity == 0:
                    self.found.append(self.f())
                else:
                    self.found.append(self.f(*self.found[-self.arity:]))
            return self.found[index]

@Adverb("ᴀs", lambda x: len(x) == 2, fail = lambda inner, links, outerindex: bidirectional_recursive_sequence(inner, links, outerindex))
class bidirectional_recursive_sequence(sequence):
    def __init__(self, inner, links, outerindex):
        sequence.__init__(self, self.func)
        if len(inner) == 0:
            raise RuntimeError("cannot create bidirectional sequence with no verbs")
        elif len(inner) == 1:
            self.backtrack = self.advance = ut(inner.call)
        else:
            self.backtrack, self.advance = ut(inner[0].call), ut(inner[1].call)
        self.arity = max(link.arity for link in inner)
        self.f_arity = inner[-1].arity
        self.b_arity = inner[0].arity
        self.forward = []
        self.backward = []
    def call(self, *a):
        self.forward = list(a)[:self.f_arity]
        self.backward = list(a)[::-1][:self.b_arity]
        return self
    def func(self, index):
        if index < 0:
            while len(self.backward) - self.b_arity < -index:
                if self.b_arity == 0:
                    self.backward.append(self.backtrack())
                else:
                    self.backward.append(self.backtrack(*self.backward[-self.b_arity:]))
            return self.backward[self.b_arity - 1 - index]
        else:
            while len(self.forward) <= index:
                if self.f_arity == 0:
                    self.forward.append(self.advance())
                else:
                    self.forward.append(self.advance(*self.forward[-self.f_arity:]))
            return self.forward[index]

@Adverb("Ի", lambda x: True)
def last_link_nilad(inner, links, outerindex):
    return attrdict(arity = 0, call = lambda: trampoline(links[(outerindex - 1) % len(links)], []))

@Adverb("Ը", lambda x: True)
def last_link_monad(inner, links, outerindex):
    return attrdict(arity = 1, call = lambda x: trampoline(links[(outerindex - 1) % len(links)], [x]))

@Adverb("Թ", lambda x: True)
def last_link_dyad(inner, links, outerindex):
    return attrdict(arity = 2, call = lambda x, y: trampoline(links[(outerindex - 1) % len(links)], [x, y]))

@Adverb("ɨ", lambda x: True)
def this_link_nilad(inner, links, outerindex):
    return attrdict(arity = 0, call = lambda: trampoline(links[outerindex], []))

@Adverb("ɫ", lambda x: True)
def this_link_monad(inner, links, outerindex):
    return attrdict(arity = 1, call = lambda x: trampoline(links[outerindex], [x]))

@Adverb("ɬ", lambda x: True)
def this_link_dyad(inner, links, outerindex):
    return attrdict(arity = 2, call = lambda x, y: trampoline(links[outerindex], [x, y]))

@Adverb("ի", lambda x: True)
def next_link_nilad(inner, links, outerindex):
    return attrdict(arity = 0, call = lambda: trampoline(links[(outerindex + 1) % len(links)], []))

@Adverb("ը", lambda x: True)
def next_link_monad(inner, links, outerindex):
    return attrdict(arity = 1, call = lambda x: trampoline(links[(outerindex + 1) % len(links)], [x]))

@Adverb("թ", lambda x: True)
def next_link_dyad(inner, links, outerindex):
    return attrdict(arity = 2, call = lambda x, y: trampoline(links[(outerindex + 1) % len(links)], [x, y]))
