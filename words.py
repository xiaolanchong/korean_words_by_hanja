
import re
import os
import jinja2
from collections import namedtuple
from collections import defaultdict


Record = namedtuple('Record', ['word', 'suffix', 'hanja', 'synonym', 'meaning', 'pos', 'level'])

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
re_line = re.compile(r"(.+)\t(.*)\t(.*)\t(.+)\t(\d{1,2}|\w)\t(\w)")

env = jinja2.Environment(loader=jinja2.FileSystemLoader(''),
                         extensions=['jinja2htmlcompress.HTMLCompress'],
                         trim_blocks=True, lstrip_blocks=True)
template = env.get_template('hanja.tmpl.html')


def add_hanja(rec: Record):
    for sym in rec.hanja:
        if 0x4E00 <= ord(sym) <= 0x9FEF:
            all_hanja[sym].append(rec)


def is_cjk(ch):
    return 0x4E00 <= ord(sym) <= 0x9FEF


with open('6k_popular_words.txt', encoding='utf8') as infile:
    re_suffix = re.compile('^(.+?)(하다|되다|롭다|스럽다|히)$')
    already_added = set()
    infile.readline()
    for line in infile.readlines():
        line = line.strip()
        m = re_line.match(line)
        if m is None:
            print(f'{line} - no match')
            continue

        word, hanja, synonym, meaning, pos, level = m.groups()
        if len(hanja) == 0:
            #non_hanja.append(rec)
            continue
        for sym in hanja:
            # to exclude  일요일 	日曜日 	Sunday
            unique_rec = (sym, hanja, word, meaning)
            if is_cjk(sym) and unique_rec not in already_added:
                already_added.add(unique_rec)
                m_suffix = re_suffix.match(word)
                stripped_word, suffix = (m_suffix.group(1), m_suffix.group(2)) if m_suffix is not None else (word, '')
                meaning = meaning.replace(r"\\'", "'")
                rec = Record(stripped_word, suffix, hanja, synonym, meaning, pos, level)
                all_hanja[sym].append(rec)


print(f'total hanja: {len(all_hanja)}')
for hanja_sym in all_hanja.keys():
    all_hanja[hanja_sym] = sorted(all_hanja[hanja_sym], key=lambda rc: rc.hanja)
   # print(f'{hanja_sym}: {rec}')

sorted(non_hanja, key=lambda rc: rc.word)

with open('nonhanja_out.txt', mode='w', encoding='utf8') as out_file:
    for rec in non_hanja:
        pos = pos_map.get(rec.pos, '')
        out_file.write(f'{rec.word}\t{rec.meaning + " " + rec.synonym}\t{pos}\t{rec.level}\n')

if True:
    title = '6000 наиболее популярных слов из ханчи'
    out_tmpl = template.render(hanja_recs=all_hanja, title=title)
    with open(os.path.join('html', 'hanja6k.html'), mode='w', encoding='utf8') as out_file:
        out_file.write(out_tmpl)
