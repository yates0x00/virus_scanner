# scanner for virus

## setup

python3 ( 3.11 )

$ pip3 install click


## Usage

A virus scanner. It can scan the files by sha1 or by regexp. can run on linux/windows/mac

```
Usage:  \n
$ python3 scanner.py --target=C:\ --strategy=sha1 --output=result.csv
```

for more details, please refer to `--help` option

## prepare the virus databases

1. download malware/virus samples to local
2. process these samples into a new file format ( a sha256 string line by line, see database/db_sample_for_sha1.txt )
3. run the script.
