import re


def convert(source, target):
    if '\n' in source:
        lines = iter(source.split('\n'))
    else:
        with open(source, encoding='utf8') as f:
            lines = iter(f.readlines())

    pre = ''
    name = next(lines).strip()
    while name.startswith('?'):
        pre += name[1:] + '\n'
        name = next(lines).strip()
    author = next(lines).strip()

    with open(target, 'w', encoding='utf8') as f:
        f.write(f'{pre}\\fullsong{{{name}}}{{{author}}}{{')

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
            if line.startswith('?'):
                f.write(line[1:])
                continue
            line = re.sub(r'] *\[', '][', line)
            if not line and verse:
                f.write('}\n')
                verse = False
            elif line and not verse:
                f.write('\\verse{\n')
                verse = True
            if line:
                bold = False
                italics = False
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
                    elif character == '*':
                        if not in_lyrics and not overtext:
                            any_lyrics = True
                            in_lyrics = True
                            start_lyrics(last_space, f)
                        if bold:
                            f.write('}')
                        else:
                            f.write('{\\bf{}')
                        bold = not bold
                    elif character == '_':
                        if not in_lyrics and not overtext:
                            in_lyrics = True
                            any_lyrics = True
                            start_lyrics(last_space, f)
                        if italics:
                            f.write('}')
                        else:
                            f.write('{\\it{}')
                        italics = not italics
                    else:
                        if not overtext and not in_lyrics:
                            in_lyrics = True
                            any_lyrics = True
                            start_lyrics(last_space, f)
                        if not overtext:
                            last_space = character == ' '
                        f.write(character)
                if in_lyrics:
                    f.write('}')
                f.write('}}\n')
                assert not bold and not italics, f'unmatched * or _ in {line}, {name}'
        f.write('}\n')

    return name


def start_lyrics(last_space, f):
    if last_space:
        f.write(r'\lyricsspace{')
    else:
        f.write(r'\lyrics{')


if __name__ == '__main__':
    # convert(*argv[1:])
    convert('songs/testsong.txt', 'tmp/testsong.tex')
