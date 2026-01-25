#!/usr/bin/env python3
"""
CLI поиск по сайту: комбинирует предвычисленные TF-IDF веса и фуззи-поиск по заголовкам.
Запуск: python3 site_search.py "замена экрана"
Опции: --top N, --fuzzy-weight (0..1)
"""
import json
import argparse
import math
from rapidfuzz import process, fuzz


def load_index(path='search_index.json'):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def tokenize(s):
    import re
    return [t for t in re.split(r"[^\w\u0400-\u04FF]+", s.lower()) if t]


def tfidf_score_item(item, tokens, surface_to_lemma):
    weights = item.get('weights', {})
    score = 0.0
    for t in tokens:
        lemma = surface_to_lemma.get(t, t) if surface_to_lemma else t
        w = weights.get(lemma)
        if w:
            score += w
            # small title bonus
            if item.get('title') and t in item['title'].lower():
                score += w * 0.3
    return score


def normalize_scores(scores):
    # normalize to 0..1
    if not scores:
        return {}
    vals = list(scores.values())
    mx = max(vals)
    mn = min(vals)
    out = {}
    if mx == mn:
        for k, v in scores.items():
            out[k] = 1.0 if v > 0 else 0.0
        return out
    for k, v in scores.items():
        out[k] = (v - mn) / (mx - mn)
    return out


def search(index, query, top=10, fuzzy_weight=0.3):
    docs = index.get('docs', [])
    surface = index.get('surface_to_lemma', {})
    tokens = tokenize(query)

    # TF-IDF scoring
    tfidf_scores = {}
    for i, d in enumerate(docs):
        s = tfidf_score_item(d, tokens, surface)
        if s > 0:
            tfidf_scores[i] = s

    tfidf_norm = normalize_scores(tfidf_scores)

    # Fuzzy scoring on titles (and excerpts fallback)
    title_map = {i: (d.get('title','') or '') for i,d in enumerate(docs)}
    choices = list(title_map.values())
    # Use rapidfuzz.process to get ratios; it returns tuples (match, score, idx)
    # We'll compute per-index fuzzy score by matching query against title + excerpt
    fuzzy_scores = {}
    for i, d in enumerate(docs):
        title = (d.get('title') or '')
        excerpt = (d.get('excerpt') or '')
        # prefer title similarity
        score_title = fuzz.token_set_ratio(query, title) if title else 0
        score_excerpt = fuzz.token_set_ratio(query, excerpt) if excerpt else 0
        fuzzy_scores[i] = max(score_title, score_excerpt)

    fuzzy_norm = normalize_scores({k: v for k,v in fuzzy_scores.items() if v > 0})

    # Combine
    final = {}
    for i in range(len(docs)):
        t = tfidf_norm.get(i, 0.0)
        f = fuzzy_norm.get(i, 0.0)
        # final = (1 - fuzzy_weight) * t + fuzzy_weight * f
        final[i] = (1.0 - fuzzy_weight) * t + fuzzy_weight * f

    # sort and return top
    ranked = sorted(final.items(), key=lambda x: x[1], reverse=True)
    results = [(index['docs'][i], score) for i, score in ranked[:top] if score > 0]
    return results


def pretty_print(results):
    if not results:
        print('Ничего не найдено')
        return
    for r, sc in results:
        title = r.get('title') or '<без заголовка>'
        url = r.get('url') or ''
        excerpt = r.get('excerpt') or (r.get('content') or '')[:200]
        print(f'[{sc:.3f}] {title} — {url}')
        print('   ', excerpt.replace('\n',' ')[:200])
        print()


def main():
    p = argparse.ArgumentParser()
    p.add_argument('query', nargs='?', help='Поисковый запрос (в кавычках если несколько слов)')
    p.add_argument('--top', type=int, default=10)
    p.add_argument('--fuzzy-weight', type=float, default=0.3, help='Доля вклада фуззи (0..1)')
    p.add_argument('--index', default='search_index.json')
    args = p.parse_args()

    if not args.query:
        q = input('Введите запрос: ').strip()
    else:
        q = args.query
    idx = load_index(args.index)
    results = search(idx, q, top=args.top, fuzzy_weight=args.fuzzy_weight)
    pretty_print(results)


if __name__ == '__main__':
    main()
