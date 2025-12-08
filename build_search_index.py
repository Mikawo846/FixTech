#!/usr/bin/env python3
"""
Проходит по всем HTML-файлам в проекте, извлекает заголовок, URL и текст
и сохраняет индекс в `search_index.json` для клиентского поиска.
"""
import os
import re
import json
import math
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Try to import pymorphy2 for Russian lemmatization. If not available,
# indexer will fall back to simple token forms.
try:
    import pymorphy2
    _MORPH = pymorphy2.MorphAnalyzer()
    USE_MORPH = True
except Exception:
    _MORPH = None
    USE_MORPH = False

# Basic stopwords (Russian + English small set). This reduces noise in the index.
STOPWORDS = {
    'и','в','во','не','что','он','на','я','с','со','как','а','то','все','она','так','его','но','да','ты',
    'к','у','же','за','бы','по','ее','мне','было','вот','от','меня','еще','нет','о','из','ему','теперь',
    'даже','ну','вдруг','ли','если','уже','или','ни','быть','был','него','до','вас','нибудь','опять',
    'весь','это','что','для','при','поэтому','из-за','через','там','тут','были','есть','вместо',
    'this','the','and','is','in','to','of','for'
}

def strip_tags(html: str) -> str:
    # Удаляем скрипты/стили сначала
    html = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", html)
    # Удаляем все теги
    text = re.sub(r"(?s)<[^>]+>", " ", html)
    # Нормализуем пробелы
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def extract_title(html: str) -> str:
    m = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    if m:
        return m.group(1).strip()
    # fallback: H1
    m2 = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.IGNORECASE | re.DOTALL)
    if m2:
        return re.sub(r"<[^>]+>", "", m2.group(1)).strip()
    return ""

def tokenize(text: str):
    if not text:
        return []
    # simple Unicode-aware tokenization for Cyrillic + Latin + digits
    toks = re.findall(r"[A-Za-zА-Яа-яёЁ0-9]+", text.lower())
    # require token length > 1, contain a letter and not be a stopword
    out = []
    for t in toks:
        if len(t) <= 1:
            continue
        if t in STOPWORDS:
            continue
        if not re.search(r"[A-Za-zА-Яа-яёЁ]", t):
            # skip tokens with no letters (pure numbers)
            continue
        out.append(t)
    return out

def lemma_token(t: str) -> str:
    if USE_MORPH:
        try:
            return _MORPH.parse(t)[0].normal_form
        except Exception:
            return t
    return t

def build_index(root: Path, top_k: int = 400, title_boost: int = 5) -> None:
    docs_raw = []
    # surface token -> lemma mapping
    surface2lemma = {}

    for dirpath, dirnames, filenames in os.walk(root):
        # skip hidden dirs
        if any(p.startswith('.') for p in Path(dirpath).parts):
            continue
        for fname in filenames:
            if not fname.lower().endswith('.html'):
                continue
            if fname.endswith('.bak'):
                continue
            full = Path(dirpath) / fname
            rel = full.relative_to(root)
            try:
                html = full.read_text(encoding='utf-8')
            except Exception:
                continue
            title = extract_title(html) or str(rel)
            content = strip_tags(html)
            excerpt = content[:300].strip()

            # tokenize and lemmatize
            tokens = tokenize(title + ' ' + content)
            lemmas = [lemma_token(t) for t in tokens]
            for s, l in zip(tokens, lemmas):
                if s not in surface2lemma:
                    surface2lemma[s] = l

            # build counts; apply title boost
            counts = Counter()
            title_tokens = tokenize(title)
            title_lemmas = [lemma_token(t) for t in title_tokens]
            for tl in title_lemmas:
                counts[tl] += title_boost

            for l in lemmas:
                counts[l] += 1

            total_terms = sum(counts.values()) or 1

            docs_raw.append({
                'title': title,
                'url': str(rel).replace('\\', '/'),
                'excerpt': excerpt,
                'content': content,
                'counts': counts,
                'total_terms': total_terms,
            })

    N = len(docs_raw)
    # document frequency per lemma
    df = Counter()
    for d in docs_raw:
        for t in d['counts'].keys():
            df[t] += 1

    # compute idf
    idf = {}
    for t, freq in df.items():
        idf[t] = math.log(1.0 + (N / float(freq)))

    # build final docs with top-k TF-IDF weights
    docs_out = []
    for d in docs_raw:
        counts = d['counts']
        total = d['total_terms']
        weights = {}
        # apply length normalization so very long/category pages get penalized
        # length_norm decreases with document length; adding 2 prevents div-by-zero
        length_norm = 1.0 / math.log(2.0 + float(total))
        for t, c in counts.items():
            tf = float(c) / float(total)
            w = tf * idf.get(t, 0.0)
            w = w * length_norm
            weights[t] = w
        # keep only top_k tokens by weight to reduce index size
        top_items = dict(sorted(weights.items(), key=lambda x: x[1], reverse=True)[:top_k])
        # keep truncated content to avoid excessive JSON size in the index
        docs_out.append({
            'title': d['title'],
            'url': d['url'],
            'excerpt': d['excerpt'],
            'content': (d.get('content') or '')[:2000],
            'weights': top_items,
        })

    out_data = {
        'meta': {'N': N},
        'surface_to_lemma': surface2lemma,
        'docs': docs_out,
    }

    # Build inverted index: lemma -> list of (doc_idx, weight)
    inv = {}
    for i, d in enumerate(docs_out):
        for lemma, w in (d.get('weights') or {}).items():
            inv.setdefault(lemma, []).append((i, float(w)))

    # Trim and sort posting lists to keep index compact
    MAX_POSTINGS = 200
    for lemma, postings in list(inv.items()):
        postings.sort(key=lambda x: x[1], reverse=True)
        if len(postings) > MAX_POSTINGS:
            inv[lemma] = postings[:MAX_POSTINGS]
        else:
            inv[lemma] = postings

    out_data['inv_index'] = inv

    out = root / 'search_index.json'
    with out.open('w', encoding='utf-8') as f:
        json.dump(out_data, f, ensure_ascii=False)
    print(f'Index written: {out} ({N} items, lemmas: {len(df)})')

if __name__ == '__main__':
    build_index(ROOT)
