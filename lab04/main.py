import sys

from stats import average_by_city, read_valid, warmest_city


def main():
    lines = sys.stdin.read().splitlines()

    records = read_valid(lines)

    total = len(lines)
    empty = 0
    for line in lines:
        if line.strip() == "":
            empty = empty + 1
    skipped = total - empty - len(records)

    print(len(records))
    print(skipped)

    averages = average_by_city(records)
    best = warmest_city(records)
    print("{:.1f}".format(averages[best]))


if __name__ == "__main__":
    main()