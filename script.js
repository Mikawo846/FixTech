// smooth-header.js

document.addEventListener('DOMContentLoaded', function() {
  // Плавная прокрутка к #categories при загрузке страницы с якорем
  function scrollToCategories() {
    const target = document.getElementById('categories');
    if (target) {
      setTimeout(() => {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }, 100);
    }
  }

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
      else if (this.href.includes('index.html#categories')) {
        // Разрешаем стандартное поведение
        return;
      }
    });
  });

  // Скрытие/показ шапки только после прокрутки до блока поиска
  const header = document.querySelector('.header');
  const searchSection = document.querySelector('.search-section');
  let lastScroll = window.pageYOffset;
  let ticking = false;
  const mobileBreakpoint = 768;
  const scrollUpThreshold = 50;
  const scrollDownThreshold = 10;

  // Получаем абсолютную позицию блока поиска
  let searchSectionTop = 0;
  function updateSearchSectionTop() {
    if (searchSection) {
      searchSectionTop = searchSection.getBoundingClientRect().top + window.scrollY;
    }
  }
  updateSearchSectionTop();
  window.addEventListener('resize', updateSearchSectionTop);

  window.addEventListener('scroll', function() {
    if (!header) return;
    if (!ticking && window.innerWidth <= mobileBreakpoint) {
      window.requestAnimationFrame(function() {
        const currentScroll = window.pageYOffset;

        // Скрипт скрытия шапки начинает работать только после прокрутки до блока поиска
        if (currentScroll < searchSectionTop) {
          header.classList.remove('hide');
          lastScroll = currentScroll;
          ticking = false;
          return;
        }

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
      header.classList.remove('hide');
    }
  });
});
