from abc import ABC
import didiator


class EventHandler[E](didiator.EventHandler[E], ABC): ...
