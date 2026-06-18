import functools
from collections.abc import Callable
from typing import Any


def transaction_scope_async(func: Callable) -> Callable:
    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs) -> Any:
        try:
            async with self.session_factory.begin() as session:
                return await func(self, session, *args, **kwargs)

        except Exception as e:
            method_name = func.__name__
            self.logger.error(
                f"Database error [{type(e).__name__}] in {method_name}: {str(e)}",
                exc_info=True,
            )
            raise RuntimeError(f"Failed to execute database operation: {method_name}") from e

    return wrapper
