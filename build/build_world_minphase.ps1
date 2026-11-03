param(
  [Parameter(Mandatory=$true)][string]$WorldRoot,
  [ValidateSet('arm','host')][string]$Target='arm',
  [string]$Compiler='',
  [switch]$MinphasePl
)
$ErrorActionPreference='Stop'
if ($MinphasePl -and $Target -ne 'arm') {throw 'MinphasePl requires the ARM target'}
$root=Split-Path -Parent $PSScriptRoot
$out=Join-Path $root 'build/generated/world_minphase_ps'
New-Item -ItemType Directory -Force $out | Out-Null
if (!$Compiler) {
  $Compiler=if($Target -eq 'arm') {'D:/USER_Software/vivado/2026.1/gnu/aarch32/nt/gcc-arm-linux-gnueabi/bin/arm-linux-gnueabihf-g++.exe'} else {'D:/mingw64/bin/g++.exe'}
}
$sources=@(Get-ChildItem "$WorldRoot/src/*.cpp" | Where-Object Name -NotIn @('common.cpp','synthesis.cpp','synthesisrealtime.cpp') | ForEach-Object FullName)
$flags=@('-O3','-funroll-loops','-fno-math-errno','-fno-trapping-math','-std=c++11','-ffp-contract=off','-pthread','-static')
if($Target -eq 'arm') {$flags+=@('-mcpu=cortex-a9','-mfpu=neon','-mfloat-abi=hard')}
$includes=@('-I',"$root/src/ps/world_v23",'-I',"$root/src/ps",'-I',$out,'-I',"$WorldRoot/src",'-I',"$WorldRoot/tools")
$bin=Join-Path $out "world_minphase_$Target"
if($MinphasePl) {
  $bin+='_pl'
  $sources+=@("$root/src/ps/world_minphase_pl.cpp")
  $flags+='-Wl,--wrap=GetMinimumPhaseSpectrum'
}
if($Target -eq 'host') {$bin+='.exe'}
& $Compiler @flags @includes "$root/src/ps/world_live_stream.cpp" "$WorldRoot/src/common.cpp" "$root/src/ps/world_v23/synthesis.cpp" "$root/src/ps/world_v23/synthesisrealtime.cpp" @sources "$WorldRoot/tools/audioio.cpp" -lm -o $bin
if($LASTEXITCODE) {throw 'WORLD runtime build failed'}

if($MinphasePl) {
  $probeFlags=@('-O3','-std=c++11','-Wall','-Wextra','-Werror','-Wno-missing-field-initializers','-static','-mcpu=cortex-a9','-mfpu=neon','-mfloat-abi=hard')
  $probeIncludes=@('-I',"$root/src/ps/world_v23",'-I',"$WorldRoot/src")
  $probeSources=@("$root/src/ps/world_minphase_dma_probe.cpp","$WorldRoot/src/common.cpp","$WorldRoot/src/fft.cpp","$WorldRoot/src/matlabfunctions.cpp")
  & $Compiler @probeFlags @probeIncludes @probeSources -lm -o (Join-Path $out 'world_minphase_dma_probe')
  if($LASTEXITCODE) {throw 'Minimum-phase DMA probe build failed'}
}
Get-FileHash $bin
