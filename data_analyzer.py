import sys
from utils import add_numbers

name = "Adithya"
age = 21
numbers = [1, 2, 3, 4, 5]
info = {"course": "Python", "level": "Beginner"}
coords = (10, 20)

if __name__ == "__main__":
    if len(sys.argv) > 2:
        arg1 = sys.argv[1]
        arg2 = int(sys.argv[2])
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
    i = 0
    while i < len(numbers):
        print(f"numbers[{i}] = {numbers[i]}")
        i += 1

    print("\nUsing range:")
    for j in range(3):
        print("j =", j)

    print("\nData structures:")
    print("List:", numbers)
    print("Tuple:", coords)
    print("Dictionary:", info)

    print("\nUsing function from utils:")
    print("2 + 3 =", add_numbers(2, 3))