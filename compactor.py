import re

CHORD_REGEX = '[A-H](#|b)?(maj|mi?|dim|sus|add|\+|-|[0-9]){0,4}'
CHORD_REGEX = fr'\(?{CHORD_REGEX}(/{CHORD_REGEX})?\)?'
CHORD_REGEX = re.compile(CHORD_REGEX)


def is_chord_line(line):
    return line.startswith('!') or (line.strip() and all(CHORD_REGEX.fullmatch(word) for word in line.split()))


def compact(song):

    song = song.split('\n')
    new_song = []
    chord_line = None

    for line in song:
        if is_chord_line(line):
            if chord_line:
                new_song.append(compact_line('', chord_line))
            chord_line = line
        elif chord_line:
            new_song.append(compact_line(line, chord_line))
            chord_line = None
        else:
            new_song.append(line)

    if chord_line:
        new_song.append(compact_line('', chord_line))

    return '\n'.join(new_song)


def compact_line(line, chord_line):

    if len(line) < len(chord_line):
        line = line + ' ' * (len(chord_line))
    if chord_line.startswith('!'):
        chord_line = ' ' + chord_line[1:]

    chord_starts = [i for i, (a, b) in enumerate(zip(' ' + chord_line, chord_line + ' ')) if b != ' ' and a == ' ']
    pieces = iter([line[a:b] for a,b in zip([None] + chord_starts, chord_starts + [None])])  # noqa
    chords = iter([f'[{chord}]' if CHORD_REGEX.fullmatch(chord) else f'<{chord}>' for chord in chord_line.split()])

    line = []
    try:
        while True:
            line.append(next(pieces))
            line.append(next(chords))
    except StopIteration:
        return ''.join(line).strip()


def uncompact(song):

    song = song.split('\n')
    new_song = []
    last_pure_chords = False

    for line in song:
        if '[' in line or '<' in line:
            chord_line = ''
            lyrics_line = ''
            current_chord = ''

            overtext = False
            chord = False
            has_overtext = False
            has_lyrics = False

            for character in line:
                if character == '[' and (len(chord_line) <= len(lyrics_line) or not has_lyrics):
                    if len(chord_line) > len(lyrics_line):
                        lyrics_line += ' ' * (len(chord_line) - len(lyrics_line))
                    chord_line += ' ' * (len(lyrics_line) - len(chord_line))
                    chord = True
                    current_chord = ''
                elif character == '<' and (len(chord_line) <= len(lyrics_line) or not has_lyrics):
                    if len(chord_line) > len(lyrics_line):
                        lyrics_line += ' ' * (len(chord_line) - len(lyrics_line))
                    chord_line += ' ' * (len(lyrics_line) - len(chord_line))
                    overtext = True
                    has_overtext = True
                elif character == ']' and chord:
                    chord = False
                    chord_line += ' '
                    if not CHORD_REGEX.fullmatch(current_chord):
                        print(f'Warning: unrecognized chord {current_chord}')
                elif character == '>' and overtext:
                    overtext = False
                    chord_line += ' '
                elif chord:
                    chord_line += character
                    current_chord += character
                elif overtext:
                    chord_line += character
                else:
                    lyrics_line += character
                    if character != ' ':
                        has_lyrics = True

            if has_overtext:
                chord_line = '! ' + chord_line
                lyrics_line = '  ' + lyrics_line

            new_song.append(chord_line)
            if lyrics_line.strip():
                last_pure_chords = False
                new_song.append(lyrics_line)
            else:
                last_pure_chords = True
        else:
            if last_pure_chords:
                new_song.append('')
            new_song.append(line)
            last_pure_chords = False

    return '\n'.join(new_song)
