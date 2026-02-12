# Script to generate updated sitemap.xml for all HTML files in the project

$root = $PSScriptRoot
$baseUrl = "https://repairo.ru"

$xml = '<?xml version="1.0" encoding="UTF-8"?>' + "`n"
$xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "`n"

Get-ChildItem -Path $root -Filter "*.html" -Recurse | ForEach-Object {
    $relativePath = $_.FullName -replace [regex]::Escape($root), ''
    $relativePath = $relativePath -replace '\\', '/'
    $url = $baseUrl + $relativePath
    $lastmod = $_.LastWriteTime.ToString("yyyy-MM-dd")
    $xml += "  <url>`n"
    $xml += "    <loc>$url</loc>`n"
    $xml += "    <lastmod>$lastmod</lastmod>`n"
    $xml += "  </url>`n"
}

$xml += '</urlset>'

Set-Content -Path "$root\sitemap.xml" -Value $xml -Encoding UTF8
