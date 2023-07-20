# Viki's songbook generator

This repository is not a singular tool, but rather meant as collection of loose TeX macro files (as much as possible compatible with both LaTeX and PlainTeX) and python scripts meant to assist with creations of songbooks.

## Usage:

This section is meant for people who want to use the tool as is; thorough programmers manual will not be provided.

### Creation of songs

Replace the contents of the snongs directory by your own choice of songs. The format is as follows:

Each song is separate text file (using utf8 encoding)

First line of the file contains the name of the song
Second line contains the author

Then there are the actual lyrics. Chords and other texts that are supposed to go above the lyrics can be specified
in three ways.

1) Lines that only contain chords and spaces are considered to be chords. Align first character of a chord vertically
with the letter above which is it supposed to go. What exactly is a chord is specified by regex at the top of
compactor.py.
2) Lines that have an exclamation mark as their first character are considered to be chords. All of their contents
will be typeset above the lyrics (as aligned -- see previous point) but only chords will be typeset in bold
3) Directly in the lyrics, you can have chords in square brackets and other material that goes above chords
in pointy brackets (<>)
4) Directly in the lyrics (not inside of any chord), you can have the pipe (|) character. That is a suggestion
for a good line break. Note that
   1) No other line breaks will happen, ever (lyrics may flow out of the right end of the page)
   2) Line breaks will only happen if the line would not fit within the width of the page otherwise. Line breaks will not occur to allow columned typesetting. 
   3) Do not forget about whitespace around the pipe. For best results, use one space before pipe and no spaces after it. 

Verses are separated by one or more empty lines (in case the last line of verse has chords
only (rather than also lyrics), use a minimum of two empty lines).

Any lines (other than first two) prefixed by a hash symbol (#) are considered to be comments and ignored
This is only done in te secnd phase of processing, so if you have a line of chords above a comment
(as specified in points 1 and 2 above), one of the following two things will happen:

 - chords will be inserted into the comment and then ignored thogeher with the comment
 - chords will be inserted into the comment, displacing the initial hash, thus letting the comment appear in the product

Any plain TeX code that can normally appear in a horizontal list can appear as part of both lyrics and chords

#### Upcoming additions

 - Songs already in the repository are not cleaned up -- that is comming

### Compiling

 - Run make.py (tested for python 3.9, but 3.7 or above should work)
 - make sure to rewrite contents of titlepage.tex to your liking
 - compile songbook.tex using your favorite pdf plain TeX compiler (pdfcsplain is recommended for usage with czech characters)

## Further upcoming additions

 - there will be more songs prepared for your convenience
 - downloaders from some czech and international chord servers are planned (pisnicky-akordy.cz, supermusic.sk, ultimate-guitar.com)
 - Option for alternating margins on odd and even pages for printing purposes will be added