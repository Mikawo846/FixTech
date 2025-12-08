// Простой клиентский поиск, опирается на `search_index.json`.
// Загрузите индекс и выполняйте поиск по токенам (простой подсчёт совпадений).

document.addEventListener('DOMContentLoaded', () => {
  const input = document.querySelector('.search__input');
  const button = document.querySelector('.search__button');
  const resultsContainer = document.querySelector('.search-results');
  if (!input || !resultsContainer) return;

  let indexData = null;
  let ready = false;
  let loadError = false;
  let loadPromise = null;
  // Загружаем индекс и сохраняем промис, чтобы другие функции могли дождаться.
  // Сначала пробуем относительный путь (удобно для поддиректорий), затем абсолютный '/'.
  function fetchIndexUrl(url) {
    return fetch(url).then(r => {
      if (!r.ok) throw new Error('HTTP ' + r.status + ' ' + url);
      return r.json();
    });
  }

  loadPromise = fetchIndexUrl('search_index.json')
    .catch(err => {
      console.warn('Relative index load failed, trying absolute /search_index.json', err);
      return fetchIndexUrl('/search_index.json');
    })
    .then(data => {
      indexData = data;
      ready = true;
      tryBuildFuse();
      console.info('Search index loaded, docs:', (indexData.docs || []).length);
    })
    .catch((err) => {
      loadError = true;
      console.warn('Search index not available', err);
    });

  // Build Fuse index if library loaded and docs are available
  let fuse = null;
  function tryBuildFuse() {
    if (!indexData || !window.Fuse) return;
    const docs = indexData.docs || [];
    // Prepare documents for Fuse (include truncated content for better recall)
    const docsForFuse = docs.map((d, i) => ({
      title: d.title || '',
      excerpt: d.excerpt || '',
      content: (d.content || '').slice(0, 2000),
      url: d.url || '',
      __idx: i
    }));
    const options = {
      includeScore: true,
      threshold: 0.45,
      ignoreLocation: true,
      minMatchCharLength: 2,
      keys: [
        { name: 'title', weight: 0.6 },
        { name: 'excerpt', weight: 0.25 },
        { name: 'content', weight: 0.15 }
      ]
    };
    try {
      fuse = new Fuse(docsForFuse, options);
    } catch (e) {
      console.warn('Fuse build failed', e);
      fuse = null;
    }
  }

  // try to build Fuse once index is ready and Fuse lib probably loaded
  // tryBuildFuse() вызывается после успешной загрузки индекса

  function tokenize(s) {
    return s.toLowerCase().split(/[^\p{L}\p{N}]+/u).filter(Boolean);
  }

  function scoreItem(item, tokens) {
    // Using TF-IDF weights precomputed by the indexer.
    // `item.weights` is a map lemma->weight. We map query tokens to lemmas
    // using `surface_to_lemma` published in the index.
    const weights = item.weights || {};
    const surface = indexData && indexData.surface_to_lemma ? indexData.surface_to_lemma : {};
    let score = 0;
    for (const t of tokens) {
      const lemma = surface[t] || t;
      const w = weights[lemma];
      if (w) {
        score += w;
        // small extra boost if token appears in title text
        if (item.title && item.title.toLowerCase().indexOf(t) !== -1) score += w * 0.3;
      }
    }
    return score;
  }

  function highlight(text, tokens) {
    let out = text;
    for (const t of tokens) {
      if (!t) continue;
      const re = new RegExp('(' + t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'ig');
      out = out.replace(re, '<mark>$1</mark>');
    }
    return out;
  }

  function renderResults(list, tokens) {
    if (!list.length) {
      resultsContainer.innerHTML = '<div class="search-empty">Ничего не найдено</div>';
      return;
    }
    const html = list.map(it => {
      const excerpt = it.excerpt ? it.excerpt : (it.content || '').slice(0, 250);
      return `
        <article class="search-result">
          <h3 class="search-result__title"><a href="/${it.url}">${highlight(it.title, tokens)}</a></h3>
          <p class="search-result__excerpt">${highlight(excerpt, tokens)}...</p>
          <a class="search-result__link" href="/${it.url}">Открыть →</a>
        </article>`;
    }).join('\n');
    resultsContainer.innerHTML = html;
  }

  let debounceTimer = null;
  function doSearch() {
    if (!ready) {
      if (loadError) {
        resultsContainer.innerHTML = '<div class="search-error">Ошибка загрузки индекса. Попробуйте обновить страницу.</div>';
        return;
      }
      // индекс ещё загружается — покажем индикатор и подождём
      resultsContainer.innerHTML = '<div class="search-loading">Идёт загрузка индекса...</div>';
      if (loadPromise) {
        loadPromise.then(() => doSearch()).catch(() => {/* error already shown */});
      }
      return;
    }
    const q = input.value.trim();
    if (!q) {
      resultsContainer.innerHTML = '';
      return;
    }
    const tokens = tokenize(q);

    // If we have an inverted index, collect candidate doc ids from token postings
    let candidateIds = new Set();
    const inv = indexData && indexData.inv_index ? indexData.inv_index : null;
    if (inv && tokens.length) {
      const surface = indexData.surface_to_lemma || {};
      for (const t of tokens) {
        const lemma = surface[t] || t;
        const postings = inv[lemma] || [];
        for (const p of postings) {
          // postings are [docIdx, weight]
          candidateIds.add(p[0]);
        }
      }
    }
    // If Fuse is available prefer combined fuzzy + TF-IDF ranking for better UX
    if (fuse) {
      const raw = fuse.search(q, { limit: 200 });

      // map fuse results to idx->fuseScore
      const rawMap = new Map();
      raw.forEach(r => {
        const it = r.item;
        const idx = it.__idx;
        const fuseScore = (typeof r.score === 'number') ? (1 - r.score) : 0;
        rawMap.set(idx, fuseScore);
        candidateIds.add(idx);
      });

      // Prepare maps for scores
      const tfidfMap = new Map();
      const fuzzyMap = new Map();

      // Candidate list is union of inv_index hits and fuse hits
      const candidateList = Array.from(candidateIds).slice(0, 400);

      for (const idx of candidateList) {
        const item = indexData.docs[idx];
        if (!item) continue;
        const tf = scoreItem(item, tokens);
        tfidfMap.set(idx, tf);
        const fscore = rawMap.has(idx) ? rawMap.get(idx) : 0;
        fuzzyMap.set(idx, fscore);
      }

      // Normalize both maps
      function normalizeMap(m) {
        const vals = Array.from(m.values());
        if (!vals.length) return new Map();
        const mx = Math.max(...vals);
        const mn = Math.min(...vals);
        const out = new Map();
        if (mx === mn) {
          for (const [k, v] of m) out.set(k, v > 0 ? 1 : 0);
          return out;
        }
        for (const [k, v] of m) out.set(k, (v - mn) / (mx - mn));
        return out;
      }

      const tfidfNorm = normalizeMap(tfidfMap);
      const fuzzyNorm = normalizeMap(fuzzyMap);

      // Combine with heuristics
      const fuzzyWeight = 0.35; // balance between TF-IDF and fuzzy
      const templatePenalty = 0.45; // how much to demote template/category pages
      const titleBoostFactor = 0.25; // boost when token found in title

      const combined = [];
      for (const [idx, fscore] of fuzzyNorm) {
        const tscore = tfidfNorm.get(idx) || 0;
        let score = (1 - fuzzyWeight) * tscore + fuzzyWeight * fscore;

        const item = indexData.docs[idx];
        const title = (item && item.title) ? item.title.toLowerCase() : '';
        const url = (item && item.url) ? item.url.toLowerCase() : '';
        const excerpt = (item && item.excerpt) ? item.excerpt.toLowerCase() : '';

        // Title exact-token boost
        for (const t of tokens) {
          if (t && title.indexOf(t) !== -1) {
            score += titleBoostFactor;
            break;
          }
        }

        // Demote template/category pages detected by common patterns
        const isTemplate = /category|categories|all-guides|all_guides|index|категор|разделы|все гайды/.test(url + ' ' + title + ' ' + excerpt);
        if (isTemplate) score = score * (1 - templatePenalty);

        combined.push({ idx, score });
      }

      combined.sort((a, b) => b.score - a.score);
      const results = combined.slice(0, 20).map(r => indexData.docs[r.idx] || null).filter(Boolean);
      renderResults(results, tokens);
      return;
    }
    // fallback to TF-IDF scoring
    const docs = (indexData && indexData.docs) ? indexData.docs : [];
    const scored = docs.map(it => ({it, score: scoreItem(it, tokens)})).filter(x => x.score > 0);
    scored.sort((a,b) => b.score - a.score);
    renderResults(scored.slice(0, 20).map(x => x.it), tokens);
  }

  input.addEventListener('input', () => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(doSearch, 250);
  });

  // Enter в поле должен запускать поиск
  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      doSearch();
    }
  });

  // Кнопка может отсутствовать в некоторых шаблонах — защитимся
  if (button) {
    button.addEventListener('click', (e) => { e.preventDefault(); doSearch(); });
  }
});
