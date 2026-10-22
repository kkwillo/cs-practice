"""Утилиты для анализа журнала сервиса."""

LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR")


def parse_event(line: str) -> dict:
    """Строка журнала -> {"time", "level", "message"}; негодная -> ValueError."""
    parts = line.strip().split(maxsplit=2)
    if len(parts) != 3:
        raise ValueError(f"негодная строка: {line!r}")
    if parts[1] not in LEVELS:
        raise ValueError(f"незнакомый уровень: {parts[1]!r}")
    if len(parts[0]) != 19 or parts[0][10] != "T" or parts[0].count(":") != 2:
        raise ValueError(f"кривое время: {parts[0]!r}")

    time, level, message = parts
    return {"time": time, "level": level, "message": message}


def count_levels(lines) -> dict:
    """Сколько строк каждого уровня; негодные — под ключом BROKEN."""
    counts = {}
    for line in lines:
        if not line.strip():
            continue
        try:
            event = parse_event(line)
        except ValueError:
            counts["BROKEN"] = counts.get("BROKEN", 0) + 1
        else:
            counts[event["level"]] = counts.get(event["level"], 0) + 1
    return counts


def top_errors(lines, n: int) -> list:
    """n самых частых сообщений ERROR: пары [сообщение, сколько]; при равенстве — по алфавиту."""
    counts = {}
    for line in lines:
        if not line.strip():
            continue
        try:
            event = parse_event(line)
        except ValueError:
            continue
        if event["level"] == "ERROR":
            counts[event["message"]] = counts.get(event["message"], 0) + 1

    ordered = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return [[message, count] for message, count in ordered[:n]]


def format_report(counts: dict, errors: list) -> str:
    """Текст отчёта по готовым подсчётам."""
    lines = ["Отчёт по журналу", ""]
    for level in sorted(counts):
        lines.append(f"{level}: {counts[level]}")
    lines.append("")
    lines.append("Частые ошибки:")
    for message, count in errors:
        lines.append(f"- {message} — {count}")
    return "\n".join(lines) + "\n"