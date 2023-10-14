import os

import compactor
import formatter


translit_dict = dict(zip('ěščřžýáíéťóďň', 'escrzyaietodn'))


def translit(s):
    s = s.lower()
    # ensure accented letters are immediately after their non-accented variant
    return [(translit_dict.get(ch, ch), ch) for ch in s]

def make_book():

    songs = {}

    os.makedirs('./tmp', exist_ok=True)
    for file in os.listdir('./songs'):
        with open('./songs/' + file, encoding='utf8') as f:
            song = ''.join(f.readlines())
        song = compactor.compact(song)
        out_path = file.split('.')
        if len(out_path) == 1:
            out_path.append('tex')
        else:
            out_path[-1] = 'tex'
        out_path = '.'.join(out_path)
        out_path = './tmp/' + out_path

        name = formatter.convert(song, out_path)
        songs[name] = out_path

    with open('./songs.tex', 'w', encoding='utf8') as f:
        for song in sorted(songs, key=translit):
            f.write(f'\\input {songs[song]}\n')


if __name__ == '__main__':
    make_book()

