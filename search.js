// Простой клиентский поиск, опирается на `search_index.json`.
// Загрузите индекс и выполняйте поиск по токенам (простой подсчёт совпадений).

document.addEventListener('DOMContentLoaded', () => {
  // Автоопределение BASE для GitHub Pages репозитория mikawo846/FixTech
  const repoName = 'FixTech';
  const path = window.location.pathname;
  const BASE = path.startsWith('/' + repoName + '/') ? '/' + repoName : '';

  const input = document.querySelector('.search__input');
  const button = document.querySelector('.search__button');
  const resultsContainer = document.querySelector('.search-results');
  if (!input || !resultsContainer) return;

  let indexData = null;
  let ready = false;
  let loadError = false;
  let loadPromise = null;

  // Загрузка JSON‑индекса
  function fetchIndexUrl(url) {
    return fetch(url).then(r => {
      if (!r.ok) throw new Error('HTTP ' + r.status + ' ' + url);
      return r.json();
    });
  }

  loadPromise = fetchIndexUrl(`${BASE}/search_index.json`)
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

  // ================== Fuse.js индекс ==================

  let fuse = null;

  function tryBuildFuse() {
    if (!indexData || !window.Fuse) return;
    const docs = indexData.docs || [];
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
        { name: 'title',   weight: 0.6 },
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

  // ================== Вспомогательные функции ==================

  function tokenize(s) {
    return s.toLowerCase().split(/[^\p{L}\p{N}]+/u).filter(Boolean);
  }

  function scoreItem(item, tokens) {
    const weights = item.weights || {};
    const surface = indexData && indexData.surface_to_lemma ? indexData.surface_to_lemma : {};
    let score = 0;
    for (const t of tokens) {
      const lemma = surface[t] || t;
      const w = weights[lemma];
      if (w) {
        score += w;
        if (item.title && item.title.toLowerCase().indexOf(t) !== -1) {
          score += w * 0.3;
        }
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
  // Escape HTML in excerpts/titles to avoid injection
  function escapeHtml(s) {
    if (!s) return '';
    return s.replace(/[&<>\"]/g, function(c) { return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; });
  }

  function renderResults(list, tokens) {
    if (!list.length) {
      resultsContainer.innerHTML = '<div class="search-empty">Ничего не найдено</div>';
      return;
    }

    // small inline SVG placeholder to avoid external image 404s
    const svgPlaceholder = encodeURIComponent(`
      <svg xmlns='http://www.w3.org/2000/svg' width='400' height='240' viewBox='0 0 400 240'>
        <rect width='100%' height='100%' fill='%23f3f3f3'/>
        <g fill='%23c8c8c8' opacity='0.9'>
          <rect x='24' y='24' width='120' height='80' rx='6'/>
          <rect x='160' y='30' width='216' height='18' rx='6'/>
          <rect x='160' y='60' width='180' height='12' rx='6'/>
          <rect x='160' y='80' width='140' height='12' rx='6'/>
        </g>
      </svg>`);
    const imgSrc = 'data:image/svg+xml;utf8,' + svgPlaceholder;

    const cards = list.map(it => {
      let excerpt = it.excerpt ? it.excerpt : (it.content || '').slice(0, 240);
      excerpt = excerpt.replace(/\s+/g, ' ').trim();
      // remove obvious site header fragments
      excerpt = excerpt.replace(/TechFix\s*-?\s*/ig, '');
      if (excerpt.length > 180) excerpt = excerpt.slice(0, 177) + '...';
      const href = `${BASE}/${(it.url || '').replace(/^\/+/, '')}`;
      const safeTitle = escapeHtml(it.title || '');
      const safeExcerpt = escapeHtml(excerpt);
      // choose image from index if present, otherwise fallback to placeholder
      const imageSrc = it.image ? (it.image.match(/^https?:/) ? it.image : (BASE + '/' + it.image.replace(/^\/+/, ''))) : imgSrc;

      return `
        <article class="guide-card search-card">
          <div class="guide-card__image">
            <img src="${imageSrc}" alt="${safeTitle}">
          </div>
          <div class="guide-card__content">
            <h3 class="guide-card__title"><a href="${href}">${highlight(safeTitle, tokens)}</a></h3>
            <p class="guide-card__excerpt">${highlight(safeExcerpt, tokens)}</p>
            <div class="guide-card__meta">
              <a class="button button--small" href="${href}">Открыть</a>
            </div>
          </div>
        </article>`;
    }).join('\n');

    resultsContainer.innerHTML = `<div class="guides__grid search-cards">${cards}</div>`;
  }

  // ================== Поиск ==================

  let debounceTimer = null;

  function doSearch() {
    if (!ready) {
      if (loadError) {
        resultsContainer.innerHTML =
          '<div class="search-error">Ошибка загрузки индекса. Попробуйте обновить страницу.</div>';
        return;
      }
      resultsContainer.innerHTML =
        '<div class="search-loading">Идёт загрузка индекса...</div>';
      if (loadPromise) {
        loadPromise.then(() => doSearch()).catch(() => {});
      }
      return;
    }

    const q = input.value.trim();
    if (!q) {
      resultsContainer.innerHTML = '';
      return;
    }

    const tokens = tokenize(q);

    // кандидаты из обратного индекса
    let candidateIds = new Set();
    const inv = indexData && indexData.inv_index ? indexData.inv_index : null;
    if (inv && tokens.length) {
      const surface = indexData.surface_to_lemma || {};
      for (const t of tokens) {
        const lemma = surface[t] || t;
        const postings = inv[lemma] || [];
        for (const p of postings) {
          candidateIds.add(p[0]); // postings: [docIdx, weight]
        }
      }
    }

    // ---------- Ветка с Fuse (фаззи + TF‑IDF) ----------
    if (fuse) {
      const raw = fuse.search(q, { limit: 200 });

      const rawMap = new Map();
      raw.forEach(r => {
        const it = r.item;
        const idx = it.__idx;
        const fuseScore = (typeof r.score === 'number') ? (1 - r.score) : 0;
        rawMap.set(idx, fuseScore);
        candidateIds.add(idx);
      });

      const tfidfMap = new Map();
      const fuzzyMap = new Map();
      const candidateList = Array.from(candidateIds).slice(0, 400);

      for (const idx of candidateList) {
        const item = indexData.docs[idx];
        if (!item) continue;
        const tf = scoreItem(item, tokens);
        tfidfMap.set(idx, tf);
        const fscore = rawMap.has(idx) ? rawMap.get(idx) : 0;
        fuzzyMap.set(idx, fscore);
      }

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

      const fuzzyWeight = 0.35;
      const templatePenalty = 0.45;
      const titleBoostFactor = 0.25;

      const combined = [];
      for (const [idx, fscore] of fuzzyNorm) {
        const tscore = tfidfNorm.get(idx) || 0;
        let score = (1 - fuzzyWeight) * tscore + fuzzyWeight * fscore;

        const item = indexData.docs[idx];
        const title   = (item && item.title)   ? item.title.toLowerCase()   : '';
        const url     = (item && item.url)     ? item.url.toLowerCase()     : '';
        const excerpt = (item && item.excerpt) ? item.excerpt.toLowerCase() : '';

        // буст, если токен в заголовке
        for (const t of tokens) {
          if (t && title.indexOf(t) !== -1) {
            score += titleBoostFactor;
            break;
          }
        }

        // штраф за шаблонные/категорийные страницы
        const isTemplate = /category|categories|all-guides|all_guides|index|категор|разделы|все гайды/.test(
          url + ' ' + title + ' ' + excerpt
        );
        if (isTemplate) score = score * (1 - templatePenalty);

        combined.push({ idx, score });
      }

      combined.sort((a, b) => b.score - a.score);
      const results = combined
        .slice(0, 20)
        .map(r => indexData.docs[r.idx] || null)
        .filter(Boolean);

      renderResults(results, tokens);
      return;
    }

    // ---------- Фоллбэк: только TF‑IDF ----------
    const docs = (indexData && indexData.docs) ? indexData.docs : [];
    const scored = docs
      .map(it => ({ it, score: scoreItem(it, tokens) }))
      .filter(x => x.score > 0);

    scored.sort((a, b) => b.score - a.score);
    renderResults(scored.slice(0, 20).map(x => x.it), tokens);
  }

  // ================== Обработчики UI ==================

  input.addEventListener('input', () => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(doSearch, 250);
  });

  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      doSearch();
    }
  });

  if (button) {
    button.addEventListener('click', (e) => {
      e.preventDefault();
      doSearch();
    });
  }
});
