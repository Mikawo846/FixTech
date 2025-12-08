#!/usr/bin/env python3
"""Extended comparison runner: генерирует список запросов из индекса и
выполняет сравнение TF-IDF vs fuzzy (SequenceMatcher approximation).

Результаты: `extended_compare_report.html` и `extended_compare.csv`.
"""
import json
from pathlib import Path
from collections import Counter
from difflib import SequenceMatcher
import csv
import math

ROOT = Path(__file__).resolve().parent
IDX = ROOT / 'search_index.json'

NUM_QUERIES = 50
TOP_N = 10


def load_index(p):
    with open(p, 'r', encoding='utf-8') as f:
        return json.load(f)


def tokenize_from_text(s):
    import re
    return [t for t in re.findall(r"[A-Za-zА-Яа-яёЁ0-9]+", s.lower()) if len(t) > 1]


def tfidf_score_for_doc(doc, tokens, surface_map):
    weights = doc.get('weights', {})
    s = 0.0
    for t in tokens:
        lemma = surface_map.get(t, t) if surface_map else t
        s += float(weights.get(lemma, 0.0))
    return s


def fuzzy_score_for_doc(doc, q):
    ql = q.lower()
    title = (doc.get('title') or '').lower()
    excerpt = (doc.get('excerpt') or '').lower()
    content = (doc.get('content') or '').lower()
    t_score = SequenceMatcher(None, ql, title).ratio()
    e_score = SequenceMatcher(None, ql, excerpt).ratio()
    c_score = SequenceMatcher(None, ql, content[:1000]).ratio()
    return 0.6 * t_score + 0.25 * e_score + 0.15 * c_score


def build_queries_from_index(idx, num_queries=50):
    token_counts = Counter()
    if isinstance(idx, dict) and 'surface_to_lemma' in idx:
        for s, l in idx['surface_to_lemma'].items():
            token_counts[l] += 1
    docs = idx.get('docs', []) if isinstance(idx, dict) else idx
    for d in docs:
        for t, w in d.get('weights', {}).items():
            token_counts[t] += int(math.ceil(w * 100))

    common = [t for t, _ in token_counts.most_common(200)]
    queries = []
    for t in common[:20]:
        queries.append(t)
        if len(queries) >= num_queries:
            return queries
    i = 0
    while len(queries) < num_queries and i < len(common):
        for j in range(i+1, min(i+6, len(common))):
            queries.append(common[i] + ' ' + common[j])
            if len(queries) >= num_queries:
                break
        i += 1
    return queries[:num_queries]


def run_compare(idx, queries):
    docs = idx.get('docs') if isinstance(idx, dict) else idx
    surface = idx.get('surface_to_lemma') if isinstance(idx, dict) else {}

    rows = []
    overlaps = []

    for q in queries:
        tokens = tokenize_from_text(q)
        tf_scores = []
        for d in docs:
            sc = tfidf_score_for_doc(d, tokens, surface)
            if sc > 0:
                tf_scores.append((sc, d))
        tf_scores.sort(key=lambda x: x[0], reverse=True)
        tf_top = [d for _, d in tf_scores[:TOP_N]]

        fuzzy_scores = []
        for d in docs:
            sc = fuzzy_score_for_doc(d, q)
            if sc > 0.01:
                fuzzy_scores.append((sc, d))
        fuzzy_scores.sort(key=lambda x: x[0], reverse=True)
        fuzzy_top = [d for _, d in fuzzy_scores[:TOP_N]]

        tf_urls = [d.get('url') for d in tf_top]
        fuzzy_urls = [d.get('url') for d in fuzzy_top]
        overlap = len(set(tf_urls) & set(fuzzy_urls))
        overlaps.append(overlap)

        rows.append({'query': q, 'overlap': overlap, 'tf_top': tf_urls, 'fuzzy_top': fuzzy_urls})

    avg_overlap = sum(overlaps) / len(overlaps) if overlaps else 0
    rows_sorted_low = sorted(rows, key=lambda r: r['overlap'])

    csv_out = ROOT / 'extended_compare.csv'
    with open(csv_out, 'w', encoding='utf-8', newline='') as cf:
        w = csv.writer(cf)
        w.writerow(['query', 'overlap', 'tf_top_urls', 'fuzzy_top_urls'])
        for r in rows:
            w.writerow([r['query'], r['overlap'], ' | '.join(r['tf_top']), ' | '.join(r['fuzzy_top'])])

    html_out = ROOT / 'extended_compare_report.html'
    with open(html_out, 'w', encoding='utf-8') as hf:
        hf.write('<!doctype html><meta charset="utf-8"><title>Extended Compare</title>')
        hf.write('<style>body{font-family:Arial;padding:16px}table{border-collapse:collapse;width:100%}th,td{border:1px solid #ddd;padding:6px;text-align:left}th{background:#f4f4f4}</style>')
        hf.write(f'<h1>Extended compare ({len(queries)} queries) — avg overlap: {avg_overlap:.2f}</h1>')
        hf.write('<table><tr><th>#</th><th>Query</th><th>Overlap</th><th>TF-IDF top</th><th>Fuzzy top</th></tr>')
        for i, r in enumerate(rows, 1):
            hf.write('<tr>')
            hf.write(f'<td>{i}</td>')
            hf.write(f'<td>{html_escape(r["query"])}</td>')
            hf.write(f'<td>{r["overlap"]}</td>')
            hf.write(f'<td><small>{html_escape("\n".join(r["tf_top"])[:1000])}</small></td>')
            hf.write(f'<td><small>{html_escape("\n".join(r["fuzzy_top"])[:1000])}</small></td>')
            hf.write('</tr>')
        hf.write('</table>')

    return {'avg_overlap': avg_overlap, 'rows': rows, 'csv': csv_out, 'html': html_out, 'lowest': rows_sorted_low[:10]}


def html_escape(s):
    import html
    return html.escape(s)


def main():
    idx = load_index(IDX)
    queries = build_queries_from_index(idx, NUM_QUERIES)
    print('Generated', len(queries), 'queries — sample:', queries[:10])
    res = run_compare(idx, queries)
    print('Avg overlap:', res['avg_overlap'])
    print('CSV:', res['csv'])
    print('HTML:', res['html'])
    print('Lowest-overlap queries (sample):')
    for r in res['lowest'][:10]:
        print(r['query'], '->', r['overlap'])


if __name__ == '__main__':
    main()
