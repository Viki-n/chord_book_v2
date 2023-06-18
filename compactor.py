import re

CHORD_REGEX = '[A-H](#|b)?(maj|mi?|dim|sus|add|[0-9]){0,4}'
CHORD_REGEX = fr'\(?{CHORD_REGEX}( ?/ ?{CHORD_REGEX})?\)?'
CHORD_REGEX = re.compile(CHORD_REGEX)
