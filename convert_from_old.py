import os
import re

import compactor


def convert(source):

    for file in os.listdir(source):
        if file.startswith('.'):
            continue
        print(file)
        with open(source + '/' + file, encoding='utf8') as f:
            song = f.readlines()

        new_song = []

        name = '\n'
        author = '\n'
        for line in song:
            if line.startswith('##title:'):
                name = line[8:]
            elif line.startswith('##author:'):
                author = line[9:]
            elif line.startswith('##'):
                pass
            elif re.fullmatch('=+\n', line):
                new_song.append('\n')
            else:
                new_song.append(line)
        song = ''.join([name, author, '\n'] + new_song)
        song = compactor.uncompact(song)

        out_path = file.split('.')
        if len(out_path) == 1:
            out_path.append('txt')
        else:
            out_path[-1] = 'txt'
        out_path = '.'.join(out_path)
        out_path = './songs/' + out_path

        with open(out_path, 'w', encoding='utf8') as f:
            f.write(song)

if __name__ == '__main__':
    convert('../../karlovo')