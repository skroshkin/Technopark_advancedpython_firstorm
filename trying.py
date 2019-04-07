import re

s = 'rer or hui'
if re.findall([r'\bor\b, \band\b'], s):
    print('yes')
else:
    print('no')
