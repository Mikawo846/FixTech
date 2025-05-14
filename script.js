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
const allGuideCards = document.querySelectorAll('.guide-card, .news .guide-card'); // Ищем во всех блоках
const guidesContainer = document.querySelector('.guides__grid');
const newsContainer = document.querySelector('.news .guides__grid');

if (searchInput && allGuideCards.length > 0) {
    // Создаем элемент для сообщения "Ничего не найдено"
    const noResultsMessage = document.createElement('div');
    noResultsMessage.className = 'no-results-message';
    noResultsMessage.textContent = 'Ничего не найдено. Попробуйте изменить запрос.';
    noResultsMessage.style.display = 'none';
    noResultsMessage.style.textAlign = 'center';
    noResultsMessage.style.padding = '2rem';
    noResultsMessage.style.gridColumn = '1 / -1';
    
    if (guidesContainer) guidesContainer.appendChild(noResultsMessage);
    
    function filterGuides() {
        const query = searchInput.value.trim().toLowerCase();
        let hasResults = false;
        
        allGuideCards.forEach(card => {
            const title = card.querySelector('.guide-card__title')?.textContent.toLowerCase() || '';
            const excerpt = card.querySelector('.guide-card__excerpt')?.textContent.toLowerCase() || '';
            
            if (query === '' || title.includes(query) || excerpt.includes(query)) {
                card.style.display = '';
                hasResults = true;
            } else {
                card.style.display = 'none';
            }
        });
        
        // Показываем/скрываем сообщение "Ничего не найдено"
        if (noResultsMessage) {
            noResultsMessage.style.display = hasResults || query === '' ? 'none' : 'block';
        }
    }
    
    searchInput.addEventListener('input', filterGuides);
    
    // Обработка формы поиска
    const searchForm = document.getElementById('guide-search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            filterGuides();
            
            // Прокрутка к результатам
            if (searchInput.value.trim() !== '') {
                const firstResultsSection = document.querySelector('.guides__grid') || 
                                         document.querySelector('.news');
                if (firstResultsSection) {
                    firstResultsSection.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    }
}
});
