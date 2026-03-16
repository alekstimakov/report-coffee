@echo off
setlocal EnableExtensions

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
"$ErrorActionPreference = 'Stop'; ^
$files = Get-ChildItem -File -Filter *.csv; ^
if (-not $files) { Write-Host 'Error: no CSV files found in current folder.'; exit 1 }; ^
$rows = foreach ($f in $files) { Import-Csv -Path $f.FullName }; ^
$result = foreach ($g in ($rows ^| Group-Object student)) { ^
    $vals = @($g.Group ^| ForEach-Object { [double]$_.coffee_spent } ^| Sort-Object); ^
    $n = $vals.Count; ^
    if ($n %% 2 -eq 1) { $m = $vals[[int]($n / 2)] } else { $m = ($vals[$n / 2 - 1] + $vals[$n / 2]) / 2 }; ^
    [pscustomobject]@{ student = $g.Name; median_coffee = $m } ^
}; ^
$result ^| Sort-Object median_coffee -Descending ^| Format-Table -AutoSize"

set "EXIT_CODE=%ERRORLEVEL%"
echo.
pause
exit /b %EXIT_CODE%
