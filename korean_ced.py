# Script to generate html/dalma_hanja.html files
# 100 hanja
# 者 [ 자 ], слов: 525
# 가입자 	加入者 	член, участник
# ...       ...     ...

import re
import os
import jinja2
import htmlmin
from collections import defaultdict, namedtuple


env = jinja2.Environment(loader=jinja2.FileSystemLoader(''))
template = env.get_template('dict.tmpl.html')


re_line = re.compile('(.+?)\s*\[(.*?)\]\s*/([^/]+)/?', re.UNICODE)
all_hanja = defaultdict(list)
Record = namedtuple('Record', ['word', 'hanja', 'meaning'])

ced_dictionary = dict()
hanja_pronunciation = defaultdict(set)


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def is_hanja(symbol):
    return 0x4E00 <= ord(symbol) <= 0x9FEF


def write_files(complete_list: bool):
    parent_dir = 'html'
    hanja_number_per_file = 100
    file_number = 1
    for chunk in chunks(sorted_hanja, hanja_number_per_file):
        yielded_html = template.render(hanja_list=chunk, hanja_words=all_hanja, word_dict=ced_dictionary,
                                       hanja_pronunciation=hanja_pronunciation,
                                       start_number=(file_number - 1) * hanja_number_per_file + 1,
                                       end_number=file_number * hanja_number_per_file)
        minified_html = htmlmin.minify(yielded_html)
        with open(os.path.join(parent_dir, f'dalma_hanja_{file_number:02}.html'), mode='w', encoding='utf8') as out_file:
            out_file.write(minified_html)
        file_number += 1
        if not complete_list:
            return


def add_pronunciation(word, hanja_word, index_in_hanja_word):
    if len(word) != len(hanja_word):
        return
    if index_in_hanja_word >= len(word):
        print(f'{hanja_word} {word} {index}')
        return
    else:
        pronunciation = word[index_in_hanja_word]
        symbol = hanja_word[index_in_hanja_word]
        hanja_pronunciation[symbol].add(pronunciation)
    #existing_pronunciation = hanja_pronunciation.get(symbol).add(pronunciation)
    #if existing_pronunciation is not None:
    #    if existing_pronunciation != pronunciation:
    #        print(f'{symbol} already has {existing_pronunciation} pronunciation while {pronunciation} to be added')
    #else:
    #    hanja_pronunciation[hanja] = pronunciation


def process(word: str, hanja_word: str, meaning: str):
    for index, symbol in enumerate(hanja_word):
        ced_dictionary[word + hanja_word] = (hanja_word, meaning)
        if is_hanja(symbol):
            all_hanja[symbol].append((word, hanja_word))
            add_pronunciation(word, hanja_word, index)


with open('krd_0_1.ced', encoding='utf16') as infile:
    for line in infile.readlines():
        line = line.strip()
        m = re_line.match(line)
        if m:
            word, hanja, meaning = m.groups()
            process(word, hanja, meaning)
        else:
            print(f'"{line}" does not match regex')


print(len(list(all_hanja)))

sorted_hanja = sorted(all_hanja.keys(), key=lambda x: len(all_hanja[x]), reverse=True)

write_files(True)


for hanja in sorted_hanja:
    break
    words = all_hanja[hanja]
    print(hanja)
    for word, hanja_word in words:
        hanja, meaning = ced_dictionary[word]
        print(f"   {word}\t{hanja}\t{meaning}")
