"""Stable clock, keyed randomness and canonical file IO."""
import csv
import hashlib
import json
import random
from datetime import datetime, timedelta
from pathlib import Path
from .schema import SCHEMA, PLAN_FILES, OPTIONAL_TABLES

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RULES = ROOT / 'data/generation/v0.4/generation_rules.json'
DEFAULT_OUTPUT = ROOT / 'data/generated/v0.4'
DEFAULT_MANIFEST = ROOT / 'data/generation/v0.4/dataset_manifest.json'

def parse(value):
    dt = datetime.fromisoformat(value)
    if dt.utcoffset() is None:
        raise ValueError('offset-aware timestamp required')
    return dt

def stamp(dt):
    return dt.isoformat(timespec='seconds')

def rng(rules, *keys):
    # Independent streams prevent channel draws or iteration order becoming a quality proxy.
    key = json.dumps([rules['seed'], rules.get('random_stream_version', rules['generation_version']), *keys], ensure_ascii=False)
    return random.Random(int.from_bytes(hashlib.sha256(key.encode()).digest(), 'big'))

def compact(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))

def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2)+'\n', encoding='utf-8')

def load_rules(path=DEFAULT_RULES):
    rules = json.loads(Path(path).read_text(encoding='utf-8'))
    if rules['timezone'] != 'Asia/Seoul':
        raise ValueError('Dataset timezone must be Asia/Seoul')
    if parse(rules['observation_start']) >= parse(rules['observation_end']):
        raise ValueError('Invalid observation window')
    return rules

def empty_data():
    return {name: [] for name in SCHEMA}

def write_data(directory, data):
    directory = Path(directory)
    if directory.resolve() in {(ROOT/'data/generated'/v).resolve() for v in ('v0.4','v0.5')}:
        raise ValueError('Preserved v0.4 source cannot be overwritten; use a new candidate path')
    if 'synthetic' in directory.parts or 'presentation' in directory.parts or any(v in directory.parts for v in ('v0.1','v0.2','v0.3')):
        raise ValueError('Review generator cannot write frozen/presentation data')
    directory.mkdir(parents=True, exist_ok=True)
    for name, fields in SCHEMA.items():
        if name in OPTIONAL_TABLES and not data.get(name):continue
        with (directory / (name+'.csv')).open('w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
            writer.writeheader()
            writer.writerows(data[name])
    for name in PLAN_FILES:
        dump(directory / (name+'.json'), data[name])

def read_data(directory):
    directory = Path(directory)
    data = {}
    for name in SCHEMA:
        if not (directory / (name+'.csv')).exists() and name in OPTIONAL_TABLES | {'activity_sessions','evaluator_reservations','targeted_followups','calibration_reviews'}:
            data[name]=[];continue
        with (directory / (name+'.csv')).open(encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            data[name] = list(reader)
            data['_headers_'+name] = reader.fieldnames
    for name in PLAN_FILES:
        data[name] = json.loads((directory / (name+'.json')).read_text(encoding='utf-8'))
    if (directory/'evidence_decision_sources.csv').exists():
        data['evidence_decision_sources']=[]
    return data

def file_hashes(directory):
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(Path(directory).iterdir())
            if p.name in {n+'.csv' for n in SCHEMA} | {n+'.json' for n in PLAN_FILES}}

def plus(dt, days=0, minutes=0):
    return dt + timedelta(days=days, minutes=minutes)
