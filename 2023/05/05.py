with open("input.txt", "r") as f:
    sections = [
        (x.split(":")[0], x.split(":")[1].strip("\n").strip(" "))
        for x in f.read().split("\n\n")
    ]
    seeds = [int(seed) for seed in sections[0][1].split(" ")]
    maps = [
        [[int(val) for val in line.split(" ")] for line in sec[1].split("\n")]
        for sec in sections[1:]
    ]

#### Part 1
answer_1 = int(1e100)
for start in seeds:
    for m in maps:
        for target, source, l in m:
            src_end = source + l
            pos = start - source
            if pos >= 0 and pos <= l:
                start = target + pos
                break
    if start < answer_1:
        answer_1 = start
print(answer_1)


#### Part 2
class Sequence:
    def __init__(self, first, length=None, last=None, pos=None):
        self.first = first
        if length is not None:
            if last is not None:
                raise RuntimeError("Cannot specify both length and last.")
            self.length = length
            self.last = first + length - 1
        else:
            self.last = last
            self.length = last - first + 1
        self.pos = pos

    def show(self):
        msg = f"[ {self.first:10d} : {self.last:10d} ]"
        if not self.is_valid():
            msg += " [INVALID]"
        if self.pos is not None:
            msg += f" [{self.pos=}]"
        print(msg)

    def is_valid(self):
        return self.length > 0

    def intersect(self, other):
        """Find maximum intersection of two sequences.
        Returns another sequence, possibly invalid."""
        first = max(self.first, other.first)
        last = min(self.last, other.last)
        length = last - first + 1
        pos_first = first - self.first
        return Sequence(first, length, pos=pos_first)

    def diff(self, other=None, intrs=None):
        """Find a difference of two sequences.
        Returns a list of valid sequences."""
        if intrs is None:
            intrs = self.intersect(other)
        if not intrs.is_valid():
            return [self]
        out = [
            Sequence(self.first, last=intrs.first - 1),
            Sequence(intrs.last + 1, last=self.last),
        ]
        return [s for s in out if s.is_valid()]

    def map(self, source, target):
        """Map the sequence via source to target.
        Returns a tuple, where the first element is the mapped portion (can be None)
        and the second element is a list of unmapped portions."""
        mapped = None
        intrs = source.intersect(self)
        if not intrs.is_valid():
            return None, self
        mapped = Sequence(target.first + intrs.pos, intrs.length)
        diff = self.diff(source, intrs=intrs)
        return mapped, diff

    def push(self, m):
        """Push the sequence through a map."""
        mapped = []
        queue = [self]
        for t0, s0, l in m:
            source = Sequence(s0, l)
            target = Sequence(t0, l)
            new_queue = []
            for s in queue:
                s_mapped, s_diff = s.map(source, target)
                if s_mapped is not None:
                    mapped.append(s_mapped)
                    new_queue += s_diff
                else:
                    new_queue.append(s)
            queue = new_queue
        return mapped + queue

    def push_all(self, maps):
        queue = [seed]
        for m in maps:
            queue = [x for s in queue for x in s.push(m)]
        return queue


answer_2 = int(1e32)
for k in range(len(seeds) // 2):
    seed = Sequence(seeds[2 * k], seeds[2 * k + 1])
    queue = seed.push_all(maps)
    answer_2 = min(answer_2, *map(lambda x: x.first, queue))
print(answer_2)
