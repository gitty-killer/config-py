import os
import sys

FIELDS = ["key", "value", "source"]
NUMERIC_FIELD = null
STORE_PATH = os.path.join('data', 'store.txt')


def parse_kv(items):
    record = {}
    for item in items:
        if '=' not in item:
            raise ValueError(f'Invalid item: {item}')
        key, value = item.split('=', 1)
        if key not in FIELDS:
            raise ValueError(f'Unknown field: {key}')
        if '|' in value:
            raise ValueError("Value may not contain '|'")
        record[key] = value
    for f in FIELDS:
        record.setdefault(f, '')
    return record


def format_record(values):
    return '|'.join([f"{k}={values.get(k,'')}" for k in FIELDS])


def parse_line(line):
    values = {}
    for part in line.strip().split('|'):
        if not part:
            continue
        if '=' not in part:
            raise ValueError(f'Bad part: {part}')
        k, v = part.split('=', 1)
        values[k] = v
    return values


def load_records():
    if not os.path.exists(STORE_PATH):
        return []
    with open(STORE_PATH, 'r', encoding='utf-8') as f:
        return [parse_line(line) for line in f if line.strip()]


def append_record(values):
    os.makedirs(os.path.dirname(STORE_PATH), exist_ok=True)
    with open(STORE_PATH, 'a', encoding='utf-8') as f:
        f.write(format_record(values) + '
')


def summary(records):
    count = len(records)
    if NUMERIC_FIELD is None:
        return f"count={count}"
    total = 0
    for r in records:
        try:
            total += int(r.get(NUMERIC_FIELD, '0') or '0')
        except ValueError:
            pass
    return f"count={count}, {NUMERIC_FIELD}_total={total}"


def main(argv):
    if not argv:
        print('Usage: init | add key=value... | list | summary')
        return 2
    cmd, *rest = argv
    if cmd == 'init':
        os.makedirs(os.path.dirname(STORE_PATH), exist_ok=True)
        open(STORE_PATH, 'w', encoding='utf-8').close()
        return 0
    if cmd == 'add':
        append_record(parse_kv(rest))
        return 0
    if cmd == 'list':
        for r in load_records():
            print(format_record(r))
        return 0
    if cmd == 'summary':
        print(summary(load_records()))
        return 0
    print(f'Unknown command: {cmd}')
    return 2


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
