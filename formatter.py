import re
from sys import argv


def convert(source, target):
    with open(source) as f:
        lines = iter(f.readlines())

    name = next(lines).strip()
    author = next(lines).strip()

    with open(target, 'w') as f:
        f.write(f'\\fullsong{{{name}}}{{{author}}}{{')

        verse = False
        while True:
            try:
                line = next(lines).strip()
            except StopIteration:
                if verse:
                    f.write('}\n')
                break
            line = re.sub(r'] *\[', '][', line)
            if not line and verse:
                f.write('}\n')
                verse = False
            elif line and not verse:
                f.write('\\verse{\n')
                verse = True
            if line:
                any_lyrics = False
                in_lyrics = False
                last_space = True
                depth=0
                f.write(r'\chordline{')
                for character in line:
                    if character in '<[':
                        depth += 1
                        if depth == 1:
                            if in_lyrics:
                                f.write(r'}')
                                in_lyrics = False
                            f.write(r'\chord{')
                            if character == '<':
                                f.write(r'{\rm ')
                    elif character == ']':
                        depth -= 1
                        if depth == 0:
                            f.write('}')
                    elif character == '>':
                        depth -= 1
                        if depth == 0:
                            f.write('}}')
                    else:
                        if character == ' ' and not depth and not any_lyrics:
                            any_lyrics = True
                            f.write(r'\lyricsspace{\hskip\startskip}')
                            continue
                        if not depth and not in_lyrics:
                            in_lyrics = True
                            any_lyrics = True
                            if last_space:
                                f.write(r'\lyricsspace{')
                            else:
                                f.write(r'\lyrics{')
                        if not depth:
                            last_space = character == ' '
                        f.write(character)
                if in_lyrics:
                    f.write('}')
                f.write('}\n')
        f.write('}\n')


if __name__ == '__main__':
    # convert(*argv[1:])
    convert('songs/testsong.txt', 'tmp/testsong.tex')
