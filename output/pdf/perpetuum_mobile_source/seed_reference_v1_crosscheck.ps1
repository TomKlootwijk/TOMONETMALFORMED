$ErrorActionPreference = 'Stop'
# Independent byte framing and SHA-256 API check on this same Windows machine.
# This is not a second-platform qualification or an independent full JCS parser.
function Hash-Bytes([byte[]] $Data) {
    $hasher = [System.Security.Cryptography.SHA256]::Create()
    try { return ,$hasher.ComputeHash($Data) } finally { $hasher.Dispose() }
}
function Hex-Bytes([byte[]] $Data) {
    return [BitConverter]::ToString($Data).Replace('-', '').ToLowerInvariant()
}
function U64-Be([UInt64] $Value) {
    $bytes = [BitConverter]::GetBytes($Value)
    if ([BitConverter]::IsLittleEndian) { [Array]::Reverse($bytes) }
    return ,$bytes
}
function U16-Be([UInt16] $Value) {
    $bytes = [BitConverter]::GetBytes($Value)
    if ([BitConverter]::IsLittleEndian) { [Array]::Reverse($bytes) }
    return ,$bytes
}
$fixtureText = '{"algorithms":{"sampler":"sha256-counter-v1"},"assets":[],"family":"digital","numeric_mode":"u64-mod","parameters":{"range_n":"10"},"schema":"ppm-seed-v1","seed_hex":"0000000000000000000000000000000000000000000000000000000000000000","sources":[],"sub_v":"reference-1.0.0"}'
$fixtureBytes = [Text.Encoding]::UTF8.GetBytes($fixtureText)
$manifestTag = [Text.Encoding]::ASCII.GetBytes('PPM/MANIFEST/v1') + [byte]0
$seedTag = [Text.Encoding]::ASCII.GetBytes('PPM/SEED/v1') + [byte]0
$blockTag = [Text.Encoding]::ASCII.GetBytes('PPM/BLOCK/v1') + [byte]0
$manifestDigest = Hash-Bytes ($manifestTag + (U64-Be $fixtureBytes.Length) + $fixtureBytes)
$zeroSeed = New-Object byte[] 32
$keyBytes = Hash-Bytes ($seedTag + $zeroSeed + $manifestDigest)
$domainBytes = [Text.Encoding]::ASCII.GetBytes('geometry/instance/0/position')
$actualBlocks = @()
foreach ($index in 0..2) {
    $actualBlocks += Hex-Bytes (Hash-Bytes ($blockTag + $keyBytes + (U16-Be $domainBytes.Length) + $domainBytes + (U64-Be $index)))
}
$expected = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'seed_reference_v1_results.json') -Raw | ConvertFrom-Json
if ((Hex-Bytes $manifestDigest) -cne $expected.manifest_digest) { throw 'manifest digest mismatch' }
if ((Hex-Bytes $keyBytes) -cne $expected.key) { throw 'seed key mismatch' }
foreach ($index in 0..2) {
    if ($actualBlocks[$index] -cne $expected.blocks_0_1_2[$index]) { throw "block $index mismatch" }
}
$checkResults = [ordered]@{
    status = 'passed'
    scope = 'Five byte-framing and SHA-256 comparisons via .NET on same Windows machine'
    checks_passed = 5
    powershell_version = $PSVersionTable.PSVersion.ToString()
    dotnet_environment_version = [Environment]::Version.ToString()
    canonical_fixture_length = $fixtureBytes.Length
    manifest_digest = Hex-Bytes $manifestDigest
    key = Hex-Bytes $keyBytes
    blocks_0_1_2 = $actualBlocks
    script_sha256 = (Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant()
}
$jsonResult = $checkResults | ConvertTo-Json -Depth 10
[IO.File]::WriteAllText((Join-Path $PSScriptRoot 'seed_reference_v1_crosscheck_results.json'), $jsonResult + [Environment]::NewLine, (New-Object Text.UTF8Encoding $false))
$jsonResult
