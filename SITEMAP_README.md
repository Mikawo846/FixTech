# Sitemap Generator

Этот скрипт генерирует `sitemap.xml` и `robots.txt` для сайта repairo.ru.

## Использование

Запустите скрипт из корневой папки проекта:

```bash
python generate_sitemap.py
```

## Что делает скрипт

1. **Собирает HTML-файлы**: Рекурсивно обходит все папки от корня проекта
2. **Фильтрует исключения**: Пропускает файлы в папках `/static`, `/assets`, `/img`, `/images`, `/css`, `/js` и файлы, начинающиеся с `_`
3. **Генерирует sitemap.xml**: Создает XML-карту сайта с URL вида `https://repairo.ru/<относительный_путь>`
4. **Создает robots.txt**: Файл с инструкциями для поисковых роботов

## Результат

- `sitemap.xml` - содержит 3419 URL страниц сайта
- `robots.txt` - разрешает индексацию всех страниц и указывает на sitemap

## Структура URL

Каждый HTML-файл преобразуется в URL:
- `index.html` → `https://repairo.ru/index.html`
- `gaids/some-file.html` → `https://repairo.ru/gaids/some-file.html`

Все URL отсортированы по алфавиту для удобства.
