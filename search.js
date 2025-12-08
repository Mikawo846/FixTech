// Простой клиентский поиск, опирается на `search_index.json`.
// Загрузите индекс и выполняйте поиск по токенам (простой подсчёт совпадений).

document.addEventListener('DOMContentLoaded', () => {
  const input = document.querySelector('.search__input');
  const button = document.querySelector('.search__button');
  const resultsContainer = document.querySelector('.search-results');
  if (!input || !resultsContainer) return;

  let indexData = null;
  let ready = false;

  fetch('/search_index.json')
    .then(r => r.ok ? r.json() : Promise.reject(r.status))
    .then(data => {
      indexData = data;
      ready = true;
    })
    .catch(() => {
      console.warn('Search index not available');
    });

  // Build Fuse index if library loaded and docs are available
  let fuse = null;
  function tryBuildFuse() {
    if (!indexData || !window.Fuse) return;
    const docs = indexData.docs || [];
    // Prepare documents for Fuse (include truncated content for better recall)
    const docsForFuse = docs.map(d => ({
      title: d.title || '',
      excerpt: d.excerpt || '',
      content: (d.content || '').slice(0, 2000),
      url: d.url || ''
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
  const fuseTryInterval = setInterval(() => {
    if (ready) {
      tryBuildFuse();
      clearInterval(fuseTryInterval);
    }
  }, 200);

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
      // индекс ещё загружается — покажем индикатор
      resultsContainer.innerHTML = '<div class="search-loading">Идёт загрузка индекса...</div>';
      return;
    }
    const q = input.value.trim();
    if (!q) {
      resultsContainer.innerHTML = '';
      return;
    }
    const tokens = tokenize(q);
    // If Fuse is available prefer fuzzy search for better UX
    if (fuse) {
      const raw = fuse.search(q, { limit: 20 });
      const results = raw.map(r => r.item);
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
