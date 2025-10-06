import sys
from typing import Any, Dict, List, Tuple

from src.utils import add_numbers

name: str = "Adithya"
age: int = 21
numbers: List[int] = [1, 2, 3, 4, 5]
info: Dict[str, Any] = {"course": "Python", "level": "Beginner"}
coords: Tuple[int, int] = (10, 20)

if __name__ == "__main__":
    if len(sys.argv) > 2:
        arg1: str = sys.argv[1]
        arg2: int = int(sys.argv[2])
        print(f"Arguments: {arg1}, {arg2}")
    else:
        print("No arguments given")

    if age < 18:
        print("You are a minor.")
    elif age < 30:
        print("You are young.")
    else:
        print("You are experienced.")

    print("\nFor loop with enumerate:")
    for i, val in enumerate(numbers):
        print(f"Index {i}, Value {val}, id={id(val)}")

    print("\nWhile loop:")
    k: int = 0
    while k < len(numbers):
        print(f"numbers[{k}] = {numbers[k]}")
        k += 1

    print("\nUsing range:")
    for j in range(3):
        print("j =", j)

    print("\nData structures:")
    print("List:", numbers)
    print("Tuple:", coords)
    print("Dictionary:", info)

    print("\nUsing function from utils:")
    print("2 + 3 =", add_numbers(2, 3))
