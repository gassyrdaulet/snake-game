from typing import Set, Callable, TypeVar

T = TypeVar("T")

class Storage:
    def __init__(self):
        self.objects: Set[object] = set()
        
    def find_by_class(self, cls: type[T]) -> Set[T]:
        return {o for o in self.objects if isinstance(o, cls)}

    def apply_to_class(self, cls: type[T], func: Callable[[T], None], only_for_first: bool = False) -> None:
        for o in self.objects:
            if isinstance(o, cls):
                func(o)
                if only_for_first: break