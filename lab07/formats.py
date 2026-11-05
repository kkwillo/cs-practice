import json


def csv_to_records(text: str) -> list[dict]:
    """CSV с заголовком -> список словарей, значения - строки."""
    lines = [ln for ln in (l.strip() for l in text.splitlines()) if ln]
    if not lines:
        return []
    header = [c.strip() for c in lines[0].split(",")]
    records = []
    for line in lines[1:]:
        values = [c.strip() for c in line.split(",")]
        records.append(dict(zip(header, values)))
    return records


def _convert(value: str):
    """Приводит строку YAML к типу: число / bool / строка."""
    s = value.strip()
    if s.lower() in ("true", "yes"):
        return True
    if s.lower() in ("false", "no"):
        return False
    try:
        return int(s)
    except ValueError:
        pass
    try:
        return float(s)
    except ValueError:
        pass
    return s


def parse_settings(lines: list[str]) -> dict:
    """Учебный YAML: 'ключ: значение', списки через '- ', '#' - комментарий."""
    result: dict = {}
    list_key = None
    for raw in lines:
        line = raw.split("#", 1)[0].rstrip()      # отбрасываем комментарий
        stripped = line.strip()
        if not stripped:
            continue
        if list_key is not None and stripped.startswith("- "):
            result[list_key].append(_convert(stripped[2:]))
            continue
        if stripped.endswith(":"):               # «ключ:» открывает список
            list_key = stripped[:-1].strip()
            result[list_key] = []
            continue
        list_key = None
        key, _, value = stripped.partition(":")
        result[key.strip()] = _convert(value)
    return result


def merge_by_key(rows: list[dict], extra: dict, key: str = "id") -> list[dict]:
    """Дополняет записи из справочника extra по ключу; поля записи главнее."""
    merged = []
    for row in rows:
        info = extra.get(str(row.get(key, "")), {})
        merged.append({**info, **row})
    return merged


def records_to_json(records: list[dict]) -> str:
    """Список словарей -> JSON: ключи по алфавиту, отступ 2, кириллица как есть."""
    return json.dumps(records, indent=2, ensure_ascii=False, sort_keys=True)