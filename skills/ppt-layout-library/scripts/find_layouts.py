"""Search saved layout references; this tool does not alter source content."""
import argparse
import json
from pathlib import Path

root=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser()
p.add_argument('--family',choices=['hierarchy','center','process','comparison','convergence','text'])
p.add_argument('--query',default='')
p.add_argument('--id')
args=p.parse_args()
data=json.loads((root/'catalog.json').read_text())
for item in data['patterns']:
    if args.family and item['family'] != args.family: continue
    if args.id and item['id'].lower() != args.id.lower(): continue
    if args.query and args.query.lower() not in json.dumps(item,ensure_ascii=False).lower(): continue
    print(json.dumps(dict(item,preview_absolute=str(root/item['preview'])),ensure_ascii=False))
