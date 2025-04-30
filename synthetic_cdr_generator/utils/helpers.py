"""
This module contains helper functions for the synthetic CDR generator.
"""

from typing import List
import random



def init_pool(pool_size=10000) -> List[str]:
    """
    Initialize the pool of callers.
    """
    return list(
        [
            f"212{random.choice([6, 7])}{random.randint(10000000, 99999999)}"
            for _ in range(pool_size)
        ]
    )


def get_random_caller(pool: List[str]) -> str:
    """
    Get a random caller from the pool.
    """
    return random.choice(pool)


if __name__ == "__main__":
    _pool = init_pool(pool_size=100)
    print(f"Pool size: {len(_pool)}")
    print(f"Random caller: {get_random_caller(pool=_pool)}")
