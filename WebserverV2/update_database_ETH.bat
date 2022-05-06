@echo off

cd %~dp0

set database_filename=blockchair_ethereum_addresses_latest.tsv.gz
set database_url=https://gz.blockchair.com/ethereum/addresses/blockchair_ethereum_addresses_latest.tsv.gz --no-check-certificate

echo Downloading database from %database_url% 

datafiles\utils\wget.exe -O %database_filename% %database_url%

echo Unpacking database...

datafiles\utils\gzip.exe -d -f %database_filename%

del datafiles\BF\eth.bf
python datafiles\pd.py ethereum_addresses_latest.tsv eth_tmp
del ethereum_addresses_latest.tsv
python datafiles\red.py eth_tmp eth.txt
del eth_tmp
python datafiles\Cbloom.py eth.txt eth.bf
del eth.txt
move eth.bf %~dp0\datafiles\BF

echo Done!
