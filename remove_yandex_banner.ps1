# Script to remove Yandex Market banner styles from all HTML files

Get-ChildItem -Path "." -Filter "*.html" -Recurse | ForEach-Object {
    $file = $_.FullName
    $content = Get-Content -Path $file -Raw -Encoding UTF8

    # Remove lines containing ym-hero
    $content = $content -replace '(?m)^.*ym-hero.*$\r?\n?', ''

    # Save file
    Set-Content -Path $file -Value $content -Encoding UTF8
}
