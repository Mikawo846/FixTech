// Плавная прокрутка к #categories при загрузке страницы с якорем
document.addEventListener('DOMContentLoaded', function() {

  // Обработка якоря при загрузке страницы
  if (window.location.hash === '#categories') {
    scrollToCategories();
  }

  // Обработчик для всех ссылок с #categories
  document.querySelectorAll('a[href*="#categories"]').forEach(link => {
    link.addEventListener('click', function(e) {
      // Если это внутренняя ссылка на текущей странице
      if (this.href === window.location.href || this.href.includes(`${window.location.pathname}#categories`)) {
        e.preventDefault();
        scrollToCategories();
      }
      // Если ссылка ведет на другую страницу (например, index.html#categories)
      // Разрешаем стандартное поведение - браузер сам перейдет
    });
  });

  // Функция плавной прокрутки
  function scrollToCategories() {
    const target = document.getElementById('categories');
    if (target) {
      setTimeout(() => {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start' // Прокрутка к началу элемента
        });
      }, 100);
    }
  }

  // Улучшенный код для скрытия/показа шапки
  const header = document.querySelector('.header');
  let lastScroll = 0;
  let ticking = false;
  const mobileBreakpoint = 768;
  const scrollUpThreshold = 50; // Минимальное расстояние скролла вверх для показа
  const scrollDownThreshold = 10; // Минимальное расстояние скролла вниз для скрытия

  window.addEventListener('scroll', function() {
    if (!ticking && window.innerWidth <= mobileBreakpoint) {
      window.requestAnimationFrame(function() {
        const currentScroll = window.pageYOffset;
        const scrollDirection = currentScroll > lastScroll ? 'down' : 'up';
        const scrollDistance = Math.abs(currentScroll - lastScroll);

        // В самом верху страницы - показываем шапку
        if (currentScroll <= 0) {
          header.classList.remove('hide');
          lastScroll = currentScroll;
          ticking = false;
          return;
        }

        // Скролл вниз - скрываем шапку после преодоления порога
        if (scrollDirection === 'down' && scrollDistance > scrollDownThreshold && !header.classList.contains('hide')) {
          header.classList.add('hide');
        }
        // Скролл вверх - показываем шапку после преодоления порога
        else if (scrollDirection === 'up' && scrollDistance > scrollUpThreshold && header.classList.contains('hide')) {
          header.classList.remove('hide');
        }

        lastScroll = currentScroll;
        ticking = false;
      });
      ticking = true;
    } else if (window.innerWidth > mobileBreakpoint) {
      // На десктопах всегда показываем шапку
      header.classList.remove('hide');
    }
  });

  // === Поиск по гайдам ===
  const searchInput = document.getElementById('guide-search-input');
  const guideCards = document.querySelectorAll('.guide-card');

  if (searchInput && guideCards.length > 0) {
    function filterGuides() {
      const query = searchInput.value.trim().toLowerCase();
      guideCards.forEach(card => {
        const title = card.querySelector('.guide-card__title')?.innerText.toLowerCase() || '';
        const excerpt = card.querySelector('.guide-card__excerpt')?.innerText.toLowerCase() || '';
        if (title.includes(query) || excerpt.includes(query)) {
          card.style.display = '';
        } else {
          card.style.display = 'none';
        }
      });
    }

    searchInput.addEventListener('input', filterGuides);

    // Если форма поиска - <form id="guide-search-form">
    const searchForm = document.getElementById('guide-search-form');
    if (searchForm) {
      searchForm.addEventListener('submit', function(e) {
        e.preventDefault();
        filterGuides();
      });
    }
  }

});
