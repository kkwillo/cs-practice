def parse_record(line: str) -> dict:
    parts = line.split(";")
    if len(parts) != 3:
        raise ValueError(
            "ожидалось 3 поля, получено {}: '{}'".format(len(parts), line)
        )

    city = parts[0].strip()
    temp_str = parts[1].strip()
    date = parts[2].strip()

    if city == "":
        raise ValueError("пустой город: '" + line + "'")
    if date == "":
        raise ValueError("пустая дата: '" + line + "'")

    try:
        temperature = float(temp_str)
    except ValueError:
        raise ValueError(
            "температура не число: '" + temp_str + "' в строке '" + line + "'"
        )

    return {"city": city, "temperature": temperature, "date": date}


def read_valid(lines: list) -> list:
    records = []

    for line in lines:
        if line.strip() == "":
            continue

        try:
            record = parse_record(line)
        except ValueError:
            continue

        records.append(record)

    return records


def average_by_city(records: list) -> dict:
    sums = {}
    counts = {}

    for record in records:
        city = record["city"]
        temperature = record["temperature"]

        if city not in sums:
            sums[city] = 0.0
            counts[city] = 0

        sums[city] = sums[city] + temperature
        counts[city] = counts[city] + 1

    averages = {}
    for city in sums:
        averages[city] = round(sums[city] / counts[city], 1)

    return averages


def warmest_city(records: list) -> str:
    averages = average_by_city(records)

    if len(averages) == 0:
        raise ValueError("нет корректных записей")

    best_city = None
    best_average = None

    for city in sorted(averages):
        average = averages[city]

        if best_city is None:
            best_city = city
            best_average = average
            continue

        if average > best_average:
            best_city = city
            best_average = average

    return best_city