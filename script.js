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
      else if (this.href.includes('index.html#categories')) {
        // Разрешаем стандартное поведение - браузер сам перейдет
        return;
      }
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

  // Код для скрытия/показа шапки при скролле (только на мобильных устройствах)
  const header = document.querySelector('.header');
  let lastScroll = 0;
  const mobileBreakpoint = 768;
  
  window.addEventListener('scroll', function() {
    if (window.innerWidth <= mobileBreakpoint) {
      const currentScroll = window.pageYOffset;
      
      if (currentScroll <= 0) {
        // В самом верху страницы - показываем шапку
        header.classList.remove('hide');
        return;
      }
      
      if (currentScroll > lastScroll && !header.classList.contains('hide')) {
        // Скролл вниз - скрываем шапку
        header.classList.add('hide');
      } else if (currentScroll < lastScroll && header.classList.contains('hide')) {
        // Скролл вверх - показываем шапку
        header.classList.remove('hide');
      }
      
      lastScroll = currentScroll;
    } else {
      // На десктопах всегда показываем шапку
      header.classList.remove('hide');
    }
  });
});
