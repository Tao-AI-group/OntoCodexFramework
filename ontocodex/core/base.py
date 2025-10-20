from typing import Any, Protocol, runtime_checkable
@runtime_checkable
class Runnable(Protocol):
    def invoke(self, input: Any) -> Any: ...
    async def ainvoke(self, input: Any) -> Any: ...
class Pipe:
    def __init__(self, left: Runnable, right: Runnable): self.left, self.right = left, right
    def invoke(self, input: Any) -> Any: return self.right.invoke(self.left.invoke(input))
    async def ainvoke(self, input: Any) -> Any: return await self.right.ainvoke(await self.left.ainvoke(input))
def _or(self: Runnable, other: Runnable) -> Runnable: return Pipe(self, other)  # type: ignore
Runnable.__or__ = _or  # type: ignore
