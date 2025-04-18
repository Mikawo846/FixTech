// Плавная прокрутка к #categories при загрузке страницы с якорем
document.addEventListener('DOMContentLoaded', function() {
  if (window.location.hash === '#categories') {
    const target = document.getElementById('categories');
    if (target) {
      setTimeout(() => {
        target.scrollIntoView({ behavior: 'smooth' });
      }, 100); // Небольшая задержка для корректной работы
    }
  }

// Обработка клика для всех ссылок с #categories (если они есть на других страницах)
document.querySelectorAll('a[href*="#categories"]').forEach(link => {
  link.addEventListener('click', function(e) {
    if (this.getAttribute('href').startsWith('index.html')) {
      return; // Если ссылка уже ведет на index.html, позволить браузеру обработать её стандартно
    }
    e.preventDefault();
    window.location.href = 'index.html#categories';
  });
});
document.querySelector('.nav__link[href="#repair-categories"]').addEventListener('click', function(e) {
  e.preventDefault(); // Отменяем переход по ссылке
  const target = document.getElementById('repair-categories');
  target.scrollIntoView({ behavior: 'smooth' }); // Плавная прокрутка
});
