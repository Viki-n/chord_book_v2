import re

CHORD_REGEX = '[A-H](#|b)?(maj|mi?|dim|sus|add|[0-9]){0,4}'
CHORD_REGEX = fr'\(?{CHORD_REGEX}(/{CHORD_REGEX})?\)?'
CHORD_REGEX = re.compile(CHORD_REGEX)


def is_chord_line(line):
    return line.startswith('!') or (line and all(CHORD_REGEX.fullmatch(word) for word in line.strip))


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
        return ''.join(line)
