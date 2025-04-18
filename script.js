document.querySelector('.nav__link[href="#repair-categories"]').addEventListener('click', function(e) {
  e.preventDefault(); // Отменяем переход по ссылке
  const target = document.getElementById('repair-categories');
  target.scrollIntoView({ behavior: 'smooth' }); // Плавная прокрутка
});