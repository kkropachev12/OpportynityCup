import os


def list_to_txt(l: list, file_name: str):
    with open(f'{file_name}.txt', 'w') as f:
        for id in l:
            f.write(id)
            f.write(',')
    with open(f'{file_name}.txt', 'rb+') as f:
        f.seek(-1, os.SEEK_END)
        f.truncate()
