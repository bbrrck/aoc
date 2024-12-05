from abc import ABCMeta, abstractmethod
from collections import deque
from dataclasses import dataclass, field
from enum import Enum

# filename = "example1.txt"
# filename = "example2.txt"
filename = "input.txt"

with open(filename) as f:
    steps = f.read().strip("\n").split("\n")


class Pulse(Enum):
    NO_PULSE = "no"
    LOW_PULSE = "low"
    HIGH_PULSE = "high"


@dataclass
class Module(metaclass=ABCMeta):
    name: str
    symbol: str = None
    outputs: list["Module"] = None

    def __str__(self) -> str:
        return (
            f"{self.symbol}{self.name} -> {', '.join([o.name for o in self.outputs])}"
        )

    def __repr__(self) -> str:
        return f"{self.name}"

    def set_outputs(self, outputs):
        self.outputs = outputs

    @abstractmethod
    def send_pulse(self, input_module_name, input_pulse): ...


@dataclass
class FlipFlop(Module):
    """Flip-flop modules (prefix %) are either on or off; they are initially off. If a flip-flop module receives a high pulse, it is ignored and nothing happens. However, if a flip-flop module receives a low pulse, it flips between on and off. If it was off, it turns on and sends a high pulse. If it was on, it turns off and sends a low pulse."""

    on: bool = False
    symbol: str = "%"

    def send_pulse(self, input_module_name, input_pulse):
        # If a flip-flop module receives a high pulse, it is ignored and nothing happens.
        if input_pulse == Pulse.HIGH_PULSE:
            # print(f"{self.name} received a high pulse, nothing happens")
            return Pulse.NO_PULSE
        # However, if a flip-flop module receives a low pulse, it flips between on and off.
        self.on = not self.on
        if self.on:
            # If it was off, it turns on and sends a high pulse.
            # print(f"{self.name} turns on and sends a high pulse")
            return Pulse.HIGH_PULSE
        else:
            # If it was on, it turns off and sends a low pulse.
            # print(f"{self.name} turns off and sends a low pulse")
            return Pulse.LOW_PULSE

    def __str__(self):
        return super().__str__() + f" [on={int(self.on)}]"


@dataclass
class Conjunction(Module):
    """Conjunction modules (prefix &) remember the type of the most recent pulse received from each of their connected input modules; they initially default to remembering a low pulse for each input. When a pulse is received, the conjunction module first updates its memory for that input. Then, if it remembers high pulses for all inputs, it sends a low pulse; otherwise, it sends a high pulse."""

    symbol: str = "&"
    last_pulses: dict[str, bool] = field(default_factory=dict)

    def send_pulse(self, input_module_name, input_pulse):
        self.last_pulses[input_module_name] = input_pulse
        # print(self.name, self.last_pulses)
        for p in self.last_pulses.values():
            if p == Pulse.LOW_PULSE:
                return Pulse.HIGH_PULSE
        return Pulse.LOW_PULSE

    def __str__(self):
        state = ""
        for name, pulse in self.last_pulses.items():
            state += f" [{name}={pulse.value}]"
        return super().__str__() + state


@dataclass
class Broadcaster(Module):
    """There is a single broadcast module (named broadcaster). When it receives a pulse, it sends the same pulse to all of its destination modules."""

    symbol: str = ""

    def send_pulse(self, input_module_name, input_pulse):
        return Pulse.LOW_PULSE


@dataclass
class Output(Module):
    symbol: str = ""

    def send_pulse(self, input_module_name, input_pulse):
        return Pulse.NO_PULSE


# +
modules = {}
counter_low = 0
counter_high = 0
cycle_id = 0


def init():
    global modules
    global counter_low
    global counter_high
    modules = {}
    counter_low = 0
    counter_high = 0
    all_outputs = []
    for step in steps:
        x, outputs = step.split(" -> ")
        all_outputs += outputs.split(", ")
        name = None
        ModuleType = None
        if x == "broadcaster":
            ModuleType = Broadcaster
            name = x
        elif x.startswith("%"):
            ModuleType = FlipFlop
            name = x[1:]
        elif x.startswith("&"):
            ModuleType = Conjunction
            name = x[1:]
        else:
            raise RuntimeError(f"Invalid module type: {x}")
        m = ModuleType(name=name)  # , pulse=Pulse.LOW_PULSE)
        modules[name] = m

    all_outputs = sorted(list(set(all_outputs)))
    outputs_only = [x for x in all_outputs if x not in modules]
    for x in outputs_only:
        modules[x] = Output(x)
        modules[x].set_outputs([])

    for step in steps:
        name, outputs = step.split(" -> ")
        if name != "broadcaster":
            name = name[1:]
        outputs = outputs.split(", ")
        modules[name].set_outputs([modules[o] for o in outputs])
        # if the output is a Conjunction, store its input module
        for o in outputs:
            if isinstance(modules[o], Conjunction):
                # print(f"{o} : store last pulse for {name}")
                modules[o].last_pulses[name] = Pulse.LOW_PULSE


def show():
    global modules
    for module in modules.values():
        print(module)


def cycle():
    global modules
    global counter_low
    global counter_high
    global cycle_id
    q = deque()
    q.append((modules["broadcaster"], "button", Pulse.LOW_PULSE))
    n_iter = 0
    while q:
        n_iter += 1
        if n_iter > 1000:
            raise RuntimeError("Max # iters reached")
        module, in_name, in_pulse = q.popleft()
        if module.name == "rx" and in_pulse == Pulse.LOW_PULSE:
            print(f"{cycle_id}: sending {in_pulse} to rx")
            return False
        if in_pulse == Pulse.LOW_PULSE:
            counter_low += 1
        elif in_pulse == Pulse.HIGH_PULSE:
            counter_high += 1
        else:
            raise RuntimeError(f"Invalid pulse: {Pulse.HIGH_PULSE.value}")
        out_pulse = module.send_pulse(in_name, in_pulse)
        if out_pulse == Pulse.NO_PULSE:
            continue
        for o in module.outputs:
            q.append((o, module.name, out_pulse))
    return True


init()
for cycle_id in range(1000):
    if not cycle():
        break
answer_1 = counter_high * counter_low
print(answer_1)

# init()
# cycle()
# show()

# TODO: PART 2
