# Script to add UTF-8 BOM to all HTML files

Get-ChildItem -Path "." -Filter "*.html" -Recurse | ForEach-Object {
    $file = $_.FullName
    $content = Get-Content -Path $file -Raw -Encoding UTF8
    [System.IO.File]::WriteAllText($file, $content, [System.Text.Encoding]::UTF8)
}
