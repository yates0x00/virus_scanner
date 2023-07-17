import os
import hashlib
import click
import re
import pprint
import csv

IS_DEBUG = True
FILE_TYPES_REGEX =  r'\.(exe|dll|ps|bat|jsp)$'

# compare target file by its sha256
def compare_sha256(root, filename, virus_database, result):

    filepath = os.path.join(root, filename)

    if IS_DEBUG:
        print("== scanning file: ", filename)

    with open(filepath, 'rb') as f:
        sha256 = hashlib.sha256(f.read()).hexdigest()

        if sha256 in virus_database:
            if IS_DEBUG:
                print("Found virus.")
            result.append("{},{}".format(filepath, sha256))

# compare by regexp
def compare_regexp(root, filename, virus_database, result):
    filepath = os.path.join(root, filename)

    if IS_DEBUG:
        print("== scanning file: ", filepath)

    # 读取 source_file 文件内容
    with open(filepath, 'r') as f:
        source_text = f.read()

    # 在 source_file 中搜索匹配项
    for regex in virus_database:

        b = re.compile(r'getRuntime')
        match = re.search(b, source_text)
        if match:

            if IS_DEBUG:
                print("Found virus.")
            result.append("{},{}".format(filepath, sha256))

# determine is the target file is binary
def is_binary_file(root, filename):
    filepath = os.path.join(root, filename)

    with open(filepath, 'rb') as f:
        first_few_bytes = f.read(1024)

    for byte in first_few_bytes:
        if byte < 9 or (byte > 10 and byte < 13) or byte > 127:
            return True

    return False

# determine the target file's type ( extension, e.g. dll, exe .. )
def is_target_file_type(root, filename):
    result = False

    match = re.search(FILE_TYPES_REGEX, filename, re.IGNORECASE)

    if match:
        result = True

    return result

# save the result to a csv file, format is: <file_name>,<sha256>
def save_to_csv(result, output):
    with open(output, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for e in result:
            writer.writerow(e.split(','))
    print("csv file saved as: " , output)

# core method, do the scan
def do_scan(target, strategy, virus_db_file, output):

    result = []

    virus_database = []
    with open(virus_db_file, 'r') as f:
        for line in f:
            virus_database.append(line.strip())

    for root, dirs, files in os.walk(target):

        for filename in files:
            if strategy == 'regexp':
                if is_binary_file(root, filename):
                    continue
                else:
                    compare_regexp(root, filename, virus_database, result)
            elif strategy == 'sha256':
                if is_target_file_type(root, filename):
                    compare_sha256(root, filename, virus_database, result)
                else:
                    continue
            else:
                print("TODO: this strategy is not implemented yet")

    save_to_csv(result, output)


@click.command()
@click.option("--target", default="'C:\'", prompt="Please input path(e.g. C:\)", help="Target Path you want to scan, e.g. 'C:\\'")
@click.option('--strategy',
  prompt="Please choose the scan strategy",
  default="sha256",
  type=click.Choice(['sha256', 'regexp'], case_sensitive=False),
  help=
  """
  sha256: scan files by comparing file's sha256(scan all files).
  regexp: scan files by regxp(in this mode it will skip binary files)
  """
  )
@click.option('--virus_db_file', default="database/db_sample_for_sha256.txt", prompt="virus db file path", help=
    """
    The Virus DB file, e.g. 'db_sample_for_sha256.txt' \n \
    which consists of sha256 string line by line. see this file for details \
    """
    )
@click.option('--output', default="result.csv", prompt="Output file name", help="The file name of the CSV result, e.g. 'result.csv' ")

def main(target, strategy, virus_db_file, output):
    """
    A virus scanner. It can scan the files by sha256 or by regexp.
    Usage:
    $ cd <this folder>
    $ python3 scanner.py --target=virus_samples --strategy=sha256 --virus_db_file=database/db_sample_for_sha256.txt --output=result.csv
    """

    do_scan(target, strategy, virus_db_file, output)

if __name__ == '__main__':
    main()
