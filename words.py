
import re
import jinja2
from collections import namedtuple
from collections import defaultdict


Record = namedtuple('Record', ['word', 'hanja', 'synonym', 'meaning', 'pos', 'level'])

pos_map = {'1': 'n',
           '2': 'v',
           '3': 'adv',
           '4': 'adj',
           '5': 'cnt',
           '6': 'int',
           '7': 'prop',
           '8': 'pn',
           '9': 'num',
           }
all_hanja = defaultdict(list)
non_hanja = []
re_line = re.compile("(.+)\t(.*)\t(.*)\t(.+)\t(\d{1,2}|\w)\t(\w)")

env = jinja2.Environment(loader=jinja2.FileSystemLoader(''))
template = env.get_template('hanja.tmpl.html')


def add_hanja(rec: Record):
    for sym in rec.hanja:
        if 0x4E00 <= ord(sym) <= 0x9FEF:
            all_hanja[sym].append(rec)


with open('6k_popular_words.txt', encoding='utf8') as infile:
    infile.readline()
    for line in infile.readlines():
        line = line.strip()
        m = re_line.match(line)
        if m is not None:
            word, hanja, synonym, meaning, pos, level = m.groups()
            rec = Record(word, hanja, synonym, meaning, pos, level)
            if len(rec.hanja) == 0:
                non_hanja.append(rec)
            else:
                add_hanja(rec)
        else:
            print(f'{line} - no match')


print(f'total hanja: {len(all_hanja)}')
for hanja_sym in all_hanja.keys():
    all_hanja[hanja_sym] = sorted(all_hanja[hanja_sym], key=lambda rc: rc.hanja)
   # print(f'{hanja_sym}: {rec}')

sorted(non_hanja, key=lambda rc: rc.word)

with open('nonhanja_out.txt', mode='w', encoding='utf8') as out_file:
    for rec in non_hanja:
        pos = pos_map.get(rec.pos, '')
        out_file.write(f'{rec.word}\t{rec.meaning + " " + rec.synonym}\t{pos}\t{rec.level}\n')

if False:
    out_tmpl = template.render(hanja_recs=all_hanja)
    with open('hanja_out.html', mode='w', encoding='utf8') as out_file:
        out_file.write(out_tmpl)
