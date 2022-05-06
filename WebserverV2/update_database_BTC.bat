@echo off

cd %~dp0

set database_filename=Bitcoin_addresses_LATEST.txt.gz
set database_url=http://addresses.loyce.club/Bitcoin_addresses_LATEST.txt.gz

echo Downloading database from %database_url%

datafiles\utils\wget.exe -O %database_filename% %database_url%

echo Unpacking database...

datafiles\utils\gzip.exe -d -f %database_filename%



del datafiles\BF\btc.bf
python datafiles\Cbloom.py Bitcoin_addresses_LATEST.txt btc.bf
del Bitcoin_addresses_LATEST.txt
move btc.bf %~dp0\datafiles\BF

echo Done!