from collections import namedtuple
from dataclasses import dataclass
from functools import wraps
from time import perf_counter
from typing import TypedDict

import numpy as np
import pandas as pd
from pydantic import BaseModel


class UserTypedDict(TypedDict):
    id: int
    username: str
    role: str
    last_login: str


UserNamedTuple = namedtuple("UserNamedTuple", ["id", "username", "role", "last_login"])


@dataclass
class UserDataclass:
    id: int
    username: str
    role: str
    last_login: str


class UserPydantic(BaseModel):
    id: int
    username: str
    role: str
    last_login: str


LIST_SIZE = 10_000_000
SCALAR = 1.10

python_list = list(range(LIST_SIZE))
numpy_array = np.array(python_list, dtype=np.float64)


def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = perf_counter()
        result = func(*args, **kwargs)
        end_time = perf_counter()
        print(f"|--- {func.__name__}: {end_time - start_time:.6f} seconds ---|")
        return result

    return wrapper


@measure_time
def multiply_list(data: list, scalar: float) -> list:
    return [x * scalar for x in data]


@measure_time
def multiply_numpy(data: np.ndarray, scalar: float) -> np.ndarray:
    return data * scalar


print("\n--- Performance Comparison (Scalar-Vector Multiplication) ---")
multiply_list(python_list, SCALAR)
multiply_numpy(numpy_array, SCALAR)


def load_and_print_csv(file_path: str):
    df = pd.read_csv(file_path)
    print("\n--- Pandas DataFrame Content (from users.csv) ---")
    print(df.to_markdown(index=False))

load_and_print_csv('users.csv')