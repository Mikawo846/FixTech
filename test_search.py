#!/usr/bin/env python3
"""Простейший тест поискового индекса: имитирует логику `search.js`.
Запускает несколько запросов и печатает топ-N совпадений.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
IDX = ROOT / 'search_index.json'

def load_index(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def tokenize(s):
    if not s:
        return []
    toks = re.findall(r"[A-Za-zА-Яа-яёЁ0-9]+", s.lower())
    return [t for t in toks if t]

def score_item(item, tokens, surface_map=None):
    # Use precomputed TF-IDF weights if available
    weights = item.get('weights', {})
    score = 0.0
    for t in tokens:
        lemma = None
        if surface_map and t in surface_map:
            lemma = surface_map[t]
        else:
            lemma = t
        w = weights.get(lemma)
        if w:
            score += w
            # small title boost
            if item.get('title') and t in item.get('title','').lower():
                score += w * 0.3
    return score

def search(index, query, top=5):
    tokens = tokenize(query)
    if not tokens:
        return []
    scored = []
    for it in index:
        sc = score_item(it, tokens)
        if sc > 0:
            scored.append((sc, it))
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:top]

def short(s, n=200):
    return (s[:n] + '...') if len(s) > n else s

def main():
    idx = load_index(IDX)
    queries = [
        'замена экрана',
        'HDMI',
        'не работает телевизор',
        'чистка ноутбука',
        'ремонт Bluetooth в машине',
    ]
    for q in queries:
        print('\n=== Query: "{}" ==='.format(q))
        # detect new index format
        surface = None
        if isinstance(idx, dict) and 'docs' in idx:
            docs = idx['docs']
            surface = idx.get('surface_to_lemma')
        else:
            docs = idx

        res = []
        tokens = tokenize(q)
        if surface is None:
            # legacy index: use old search
            res = search(docs, q, top=7)
        else:
            scored = []
            for it in docs:
                sc = score_item(it, tokens, surface_map=surface)
                if sc > 0:
                    scored.append((sc, it))
            scored.sort(key=lambda x: x[0], reverse=True)
            res = scored[:7]
        if not res:
            print('No results')
            continue
        for score, it in res:
            print(f'[{score}] {it.get("title")} — {it.get("url")}')
            excerpt = it.get('excerpt') or it.get('content','')[:200]
            print('    ', short(excerpt.strip().replace('\n',' '), 180))

if __name__ == '__main__':
    main()
