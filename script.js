// Плавная прокрутка к #categories при загрузке страницы с якорем
document.addEventListener('DOMContentLoaded', function() {
  // Обработка якоря #categories
  if (window.location.hash === '#categories') {
    const target = document.getElementById('categories');
    if (target) {
      setTimeout(() => {
        target.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    }
  }

  // Обработка якоря #repair-categories (если он существует на странице)
  if (window.location.hash === '#repair-categories') {
    const target = document.getElementById('repair-categories');
    if (target) {
      setTimeout(() => {
        target.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    }
  }

  // Обработчик для всех ссылок с #categories
  document.querySelectorAll('a[href*="#categories"]').forEach(link => {
    link.addEventListener('click', function(e) {
      // Если ссылка ведет на текущую страницу
      if (this.href.includes(window.location.pathname)) {
        e.preventDefault();
        const target = document.getElementById('categories');
        if (target) {
          target.scrollIntoView({ behavior: 'smooth' });
        }
      }
      // Иначе - переход на index.html с якорем
      else {
        e.preventDefault();
        window.location.href = 'index.html#categories';
      }
    });
  });

  // Обработчик для #repair-categories (если элемент существует)
  const repairCategoriesLink = document.querySelector('.nav__link[href="#repair-categories"]');
  const repairCategoriesTarget = document.getElementById('repair-categories');
  
  if (repairCategoriesLink && repairCategoriesTarget) {
    repairCategoriesLink.addEventListener('click', function(e) {
      e.preventDefault();
      repairCategoriesTarget.scrollIntoView({ behavior: 'smooth' });
    });
  }
});
