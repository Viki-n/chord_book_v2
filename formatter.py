import re


def convert(source, target):
    if '\n' in source:
        lines = iter(source.split('\n'))
    else:
        with open(source, encoding='utf8') as f:
            lines = iter(f.readlines())

    name = next(lines).strip()
    author = next(lines).strip()

    with open(target, 'w', encoding='utf8') as f:
        f.write(f'\\fullsong{{{name}}}{{{author}}}{{')

        verse = False
        while True:
            try:
                line = next(lines).strip()
            except StopIteration:
                if verse:
                    f.write('}\n')
                break
            if line.startswith('#'):
                continue
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
                overtext = 0
                chord = False
                f.write(r'\chordline{\piece{')
                for character in line:
                    if character in '<[':
                        assert not overtext, f'extra "{character}" on line {line} in {name}'
                        overtext = True
                        if in_lyrics:
                            f.write(r'}')
                            in_lyrics = False
                        f.write(r'\chord{')
                        if character == '<':
                            f.write(r'{\rm ')
                            chord = False
                        else:
                            chord = True
                    elif character == ']':
                        assert overtext and chord,  f'extra "]" on line {line}'
                        f.write('}')
                        chord = False
                        overtext = False
                    elif character == '>':
                        assert overtext and not chord,  f'extra "]" on line {line}'
                        f.write('}}')
                        overtext = False
                    elif character == 'b' and chord:
                        f.write(r'$\flat$')
                    elif character == '|':
                        assert not chord
                        f.write(r'}}\piece{\lyricsspace{')
                    elif character == ' ' and not overtext and not any_lyrics:
                        any_lyrics = True
                        f.write(r'\lyricsspace{\hskip\startskip}')
                    else:
                        if not overtext and not in_lyrics:
                            in_lyrics = True
                            any_lyrics = True
                            if last_space:
                                f.write(r'\lyricsspace{')
                            else:
                                f.write(r'\lyrics{')
                        if not overtext:
                            last_space = character == ' '
                        f.write(character)
                if in_lyrics:
                    f.write('}')
                f.write('}}\n')
        f.write('}\n')

    return name


if __name__ == '__main__':
    # convert(*argv[1:])
    convert('songs/testsong.txt', 'tmp/testsong.tex')
