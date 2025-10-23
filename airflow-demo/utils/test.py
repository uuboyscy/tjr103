import sys


def two_sum(x: int, y: int) -> int:
    print(x + y)

if __name__ == "__main__":
    print(sys.argv[0])
    two_sum(int(sys.argv[1]), int(sys.argv[2]))
