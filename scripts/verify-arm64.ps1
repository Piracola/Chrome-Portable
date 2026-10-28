$ErrorActionPreference = 'Stop'

function Get-PeMachine([string] $Path) {
    $stream = [System.IO.File]::OpenRead($Path)
    $reader = [System.IO.BinaryReader]::new($stream)
    try {
        if ($reader.ReadUInt16() -ne 0x5A4D) { throw "Not an MZ executable: $Path" }
        $stream.Position = 0x3C
        $peOffset = $reader.ReadUInt32()
        $stream.Position = $peOffset
        if ($reader.ReadUInt32() -ne 0x00004550) { throw "Not a PE executable: $Path" }
        return $reader.ReadUInt16()
    } finally {
        $reader.Dispose()
        $stream.Dispose()
    }
}

foreach ($channel in @('stable', 'beta')) {
    $archive = Get-ChildItem "build/assets/Chrome++_${channel}_arm64_*.7z" |
        Sort-Object LastWriteTime -Descending | Select-Object -First 1
    if (-not $archive) { throw "Missing ARM64 $channel archive" }
    $destination = Join-Path 'build/pe-check' ([guid]::NewGuid().ToString('N'))
    & 7z x $archive.FullName "-o$destination" 'Chrome/chrome.exe' 'Chrome/version.dll' -y
    if ($LASTEXITCODE -ne 0) { throw "PE extraction failed: $($archive.Name)" }
    foreach ($name in @('chrome.exe', 'version.dll')) {
        $path = Join-Path $destination "Chrome/$name"
        $machine = Get-PeMachine $path
        if ($machine -ne 0xAA64) {
            throw ('Expected ARM64 (0xAA64), got 0x{0:X4}: {1}' -f $machine, $path)
        }
        Write-Host ('ARM64 PE verified: {0} / {1} (0x{2:X4})' -f $archive.Name, $name, $machine)
    }
}
