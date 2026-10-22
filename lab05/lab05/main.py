"""Читает журнал построчно, печатает сводку и пишет report.txt."""

from logstats import count_levels, format_report, parse_event, top_errors


def main() -> None:
    path = input().strip()

    total = errors = broken = 0
    with open(path, encoding="utf-8") as log:
        for line in log:
            if not line.strip():
                continue
            total += 1
            try:
                event = parse_event(line)
            except ValueError:
                broken += 1
            else:
                if event["level"] == "ERROR":
                    errors += 1

    print(total)
    print(errors)
    print(broken)

    with open(path, encoding="utf-8") as log:
        counts = count_levels(log)
    with open(path, encoding="utf-8") as log:
        top = top_errors(log, 3)

    with open("report.txt", "w", encoding="utf-8") as out:
        out.write(format_report(counts, top))


if __name__ == "__main__":
    main()