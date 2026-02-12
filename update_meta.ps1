# Script to update meta tags in HTML files in guides-laptops
# Shorten title to 50-60 characters, description to 150-160, add canonical URL

$directory = "gaids"

Get-ChildItem -Path $directory -Filter "*.html" | ForEach-Object {
    $file = $_.FullName
    $content = Get-Content -Path $file -Raw -Encoding Default

    # Remove existing canonical links
    $content = [regex]::Replace($content, '<link rel="canonical" href="[^"]*" />', '')

    # Filename for canonical
    $filename = $_.Name
    $canonicalUrl = "https://repairo.ru/gaids/$filename"

    # Update title
    $titleMatch = [regex]::Match($content, '<title>(.*?)</title>', [System.Text.RegularExpressions.RegexOptions]::Singleline)
    if ($titleMatch.Success) {
        $oldTitle = $titleMatch.Groups[1].Value
        if ($oldTitle.Length -gt 60) {
            $newTitle = $oldTitle.Substring(0, 60)
        } else {
            $newTitle = $oldTitle
        }
        $content = [regex]::Replace($content, [regex]::Escape('<title>' + $oldTitle + '</title>'), '<title>' + $newTitle + '</title>')
    }

    # Update description
    $descMatch = [regex]::Match($content, '<meta name="description" content="(.*?)"')
    if ($descMatch.Success) {
        $oldDesc = $descMatch.Groups[1].Value
        $newDesc = $oldDesc.Substring(0, [Math]::Min(160, $oldDesc.Length))
        $replacement = '<meta name="description" content="' + $newDesc + '">' + "`n    <link rel=`"canonical`" href=`"$canonicalUrl`" />"
        $content = [regex]::Replace($content, [regex]::Escape('<meta name="description" content="' + $oldDesc + '"'), $replacement)
    }

    # Save file
    Set-Content -Path $file -Value $content -Encoding UTF8
}
