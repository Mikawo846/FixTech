// Простой клиентский поиск, опирается на `search_index.json`.
// Загрузите индекс и выполняйте поиск по токенам (простой подсчёт совпадений).

document.addEventListener('DOMContentLoaded', () => {
  // Автоопределение BASE для GitHub Pages репозитория mikawo846/Repairo
  const repoName = 'Repairo';
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
  function fetchIndexUrl(url, timeoutMs = 15000) {
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => reject(new Error('timeout')), timeoutMs);
      fetch(url).then(r => {
        clearTimeout(timer);
        if (!r.ok) return reject(new Error('HTTP ' + r.status + ' ' + url));
        return r.json().then(resolve, reject);
      }).catch(err => { clearTimeout(timer); reject(err); });
    });
  }

  // Try several candidate URLs to be robust across desktop/mobile and subpaths
  const candidateUrls = [];
  try {
    // relative to current document
    candidateUrls.push(new URL('search_index.json', window.location.href).href);
  } catch (e) {}
  // base (for GitHub Pages in a subpath)
  if (BASE) candidateUrls.push(`${BASE}/search_index.json`);
  // root absolute
  candidateUrls.push('/search_index.json');

  // sequentially try candidates until one succeeds
  loadPromise = (async () => {
    for (const url of candidateUrls) {
      try {
        console.info('Trying search index URL:', url);
        const data = await fetchIndexUrl(url, 15000);
        indexData = data;
        ready = true;
        tryBuildFuse();
        console.info('Search index loaded from', url, 'docs:', (indexData.docs || []).length);
        return data;
      } catch (err) {
        console.warn('Index load failed for', url, err && err.message);
        // try next
      }
    }
    throw new Error('All index fetch attempts failed');
  })().catch(err => {
    loadError = true;
    console.warn('Search index not available after tries', err && err.message);
  });

  // ================== Простой индексный поиск ==================
  
  // Мы используем предвычисленные веса из `search_index.json` и инвертированный
  // индекс `inv_index` для быстрого получения кандидатов. Это простой и надёжный
  // алгоритм, который хорошо работает в браузере и не требует Fuse.

  let fuse = null;

  function tryBuildFuse() {
    if (!indexData || !window.Fuse) return;
    const docs = indexData.docs || [];
    // Build a lightweight Fuse corpus: only title + excerpt (much smaller than full content)
    const docsForFuse = docs.map((d, i) => ({
      title: d.title || '',
      excerpt: d.excerpt || '',
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
      excerpt = excerpt.replace(/Repairo\s*-?\s*/ig, '');
      if (excerpt.length > 180) excerpt = excerpt.slice(0, 177) + '...';
      const href = `${BASE}/${(it.url || '').replace(/^\/+/, '')}`;
      const safeTitle = escapeHtml(it.title || '');
      const safeExcerpt = escapeHtml(excerpt);
      // choose image from index if present, otherwise fallback to placeholder
      const imageSrc = it.image ? (it.image.match(/^https?:/) ? it.image : (BASE + '/' + it.image.replace(/^\/+/, ''))) : imgSrc;

      return `
        <article class="guide-card search-card">
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
    
    const inv = indexData && indexData.inv_index ? indexData.inv_index : {};
    const surface = indexData.surface_to_lemma || {};
    const docs = (indexData && indexData.docs) ? indexData.docs : [];
    
    const scores = new Map();
    // collect scores from postings
    for (const t of tokens) {
      const lemma = surface[t] || t;
      const postings = inv[lemma] || [];
      for (const p of postings) {
        const idx = p[0];
        const w = p[1] || 0;
        scores.set(idx, (scores.get(idx) || 0) + w);
      }
    }
    
    // If no candidates from inverted index, fall back to scanning docs (cheap TF scan)
    if (scores.size === 0) {
      for (let i = 0; i < docs.length; i++) {
        const it = docs[i];
        const s = scoreItem(it, tokens);
        if (s > 0) scores.set(i, s);
      }
    }
    
    if (scores.size === 0) {
      renderResults([], tokens);
      return;
    }
    
    // normalize scores
    const vals = Array.from(scores.values());
    const mx = Math.max(...vals);
    const mn = Math.min(...vals);
    
    const normalized = [];
    for (const [idx, v] of scores.entries()) {
      const norm = (mx === mn) ? (v > 0 ? 1 : 0) : ((v - mn) / (mx - mn));
      let score = norm;
      
      const item = docs[idx];
      const title = (item && item.title) ? item.title.toLowerCase() : '';
      const url = (item && item.url) ? item.url.toLowerCase() : '';
      const excerpt = (item && item.excerpt) ? item.excerpt.toLowerCase() : '';
      
      // title boost for token presence
      for (const t of tokens) {
        if (t && title.indexOf(t) !== -1) { score += 0.25; break; }
      }
      
      // penalty for template/category pages
      const isTemplate = /category|categories|all-guides|all_guides|index|категор|разделы|все гайды/.test(
        url + ' ' + title + ' ' + excerpt
      );
      if (isTemplate) score = score * (1 - 0.45);
      
      normalized.push({ idx, score });
    }
    
    normalized.sort((a, b) => b.score - a.score);
    const results = normalized.slice(0, 20).map(r => docs[r.idx]).filter(Boolean);
    renderResults(results, tokens);
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
