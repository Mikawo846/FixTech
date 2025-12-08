#!/usr/bin/env python3
"""Сравнивает выдачу TF-IDF (предрассчитанная в `search_index.json`) и приближённый
Fuse-подобный fuzzy-поиск (SequenceMatcher) для набора запросов.

Выводит результаты в терминал и сохраняет `compare_report.html` с подробной таблицей.
"""
import json
import html
from pathlib import Path
from difflib import SequenceMatcher

ROOT = Path(__file__).resolve().parent
IDX = ROOT / 'search_index.json'

QUERIES = [
    'замена экрана',
    'HDMI',
    'не работает телевизор',
    'чистка ноутбука',
    'ремонт Bluetooth в машине',
    'замена батареи смартфон',
    'не видит HDMI',
]

TOP_N = 10


def load_index(p):
    with open(p, 'r', encoding='utf-8') as f:
        return json.load(f)


def tfidf_score_for_doc(doc, tokens, surface_map):
    # doc.weights: lemma -> weight
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
    # SequenceMatcher ratio between strings -> [0,1]
    t_score = SequenceMatcher(None, ql, title).ratio()
    e_score = SequenceMatcher(None, ql, excerpt).ratio()
    c_score = SequenceMatcher(None, ql, content[:1000]).ratio()
    # weights similar to Fuse config used in frontend
    return 0.6 * t_score + 0.25 * e_score + 0.15 * c_score


def tokenize_simple(q):
    # simple tokenization compatible with index surface keys
    import re
    toks = re.findall(r"[A-Za-zА-Яа-яёЁ0-9]+", q.lower())
    return [t for t in toks if len(t) > 1]


def main():
    idx = load_index(IDX)
    docs = idx.get('docs') if isinstance(idx, dict) else idx
    surface = idx.get('surface_to_lemma') if isinstance(idx, dict) else {}

    rows_for_html = []

    print('Comparing TF-IDF vs fuzzy (SequenceMatcher approximation)')
    print('Index docs:', len(docs))

    for q in QUERIES:
        print('\n=== Query:', q, '===')
        tokens = tokenize_simple(q)

        # TF-IDF ranking
        tf_scores = []
        for d in docs:
            sc = tfidf_score_for_doc(d, tokens, surface)
            if sc > 0:
                tf_scores.append((sc, d))
        tf_scores.sort(key=lambda x: x[0], reverse=True)
        tf_top = tf_scores[:TOP_N]

        # Fuzzy ranking (approx Fuse)
        fuzzy_scores = []
        for d in docs:
            sc = fuzzy_score_for_doc(d, q)
            if sc > 0.01:
                fuzzy_scores.append((sc, d))
        fuzzy_scores.sort(key=lambda x: x[0], reverse=True)
        fuzzy_top = fuzzy_scores[:TOP_N]

        # Print concise lists
        print('\nTF-IDF top:')
        for sc, d in tf_top:
            print(f'[{sc:.4f}] {d.get("title")} — {d.get("url")}')

        print('\nFuzzy top:')
        for sc, d in fuzzy_top:
            print(f'[{sc:.4f}] {d.get("title")} — {d.get("url")}')

        # compute overlap (titles)
        tf_set = {d.get('url') for _, d in tf_top}
        fuzzy_set = {d.get('url') for _, d in fuzzy_top}
        overlap = len(tf_set & fuzzy_set)
        print(f'Overlap top {TOP_N}: {overlap}/{TOP_N}')

        rows_for_html.append((q, tf_top, fuzzy_top, overlap))

    # write HTML report
    out = ROOT / 'compare_report.html'
    with open(out, 'w', encoding='utf-8') as f:
        f.write('<!doctype html><meta charset="utf-8"><title>Compare TF-IDF vs Fuzzy</title>')
        f.write('<style>body{font-family:Arial,Helvetica,sans-serif;padding:20px}table{border-collapse:collapse;width:100%;}td,th{border:1px solid #ddd;padding:8px;vertical-align:top}th{background:#f4f4f4}</style>')
        f.write('<h1>Compare TF-IDF vs Fuzzy (approx)</h1>')
        for q, tf_top, fuzzy_top, overlap in rows_for_html:
            f.write(f'<h2>Query: {html.escape(q)} — Overlap: {overlap}/{TOP_N}</h2>')
            f.write('<table>')
            f.write('<tr><th>Rank</th><th>TF-IDF (score / title / url)</th><th>Fuzzy (score / title / url)</th></tr>')
            for i in range(TOP_N):
                lf = ''
                rf = ''
                if i < len(tf_top):
                    sc, d = tf_top[i]
                    lf = f'{sc:.4f} — {html.escape(d.get("title",""))} <br><small>{html.escape(d.get("url",""))}</small>'
                if i < len(fuzzy_top):
                    sc, d = fuzzy_top[i]
                    rf = f'{sc:.4f} — {html.escape(d.get("title",""))} <br><small>{html.escape(d.get("url",""))}</small>'
                f.write(f'<tr><td>{i+1}</td><td>{lf}</td><td>{rf}</td></tr>')
            f.write('</table>')
    print('\nHTML report written to', out)


if __name__ == '__main__':
    main()
