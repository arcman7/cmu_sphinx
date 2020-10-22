import collections
import os

counter = collections.Counter()
dir_name = 'accent_archive'
text_file_name = 'reading-passage.txt'
print('creating dictionary from "{}"'.format(os.path.join(dir_name, 'AA_unpacked', text_file_name)))
# The Accent Archive uses the same text transcript for every audio recording
text = None
# clean up text and add to counts
with open(os.path.join(dir_name, 'AA_unpacked', text_file_name), 'r') as f:
    counter += collections.Counter(f.read().replace('\n', '').replace('.', '').replace(',', '').replace(':', '').replace('  ', ' ').upper().split())

phone_counter = collections.Counter()
sphinx_dic = {}
sphinx_dic_list = None

with open ('sphinx.dic', 'r') as f:
    # each line in sphinx.dic looks like:
    # aalborg AO1 L B AO0 R G # place, danish
    sphinx_dic_list = f.read().split('\n')
    for index in range(len(sphinx_dic_list)):
        row = sphinx_dic_list[index].split(' ')
        sphinx_dic[row[0].upper()] = index

out_dir_name  = os.path.join(dir_name, 'etc')

# create .vocab file
print('writing "{}.vocab" to {}'.format(dir_name, out_dir_name))
with open(os.path.join(out_dir_name, dir_name + '.vocab'), 'w') as f:
    for item in counter:
        f.write(item + '\n')

print('writing "{}.dic" to {}'.format(dir_name, out_dir_name))
# create .dic file
with open(os.path.join(out_dir_name, dir_name + '.dic'), 'w') as f:
    for item in counter:
        if item in sphinx_dic:
            index = sphinx_dic[item]
            row = sphinx_dic_list[index]
            f.write(row.upper()  + '\n')
            # remove comments if any, then split phones by spaces
            phone_counter += collections.Counter(row.split('#')[0].split(' ')[1:])

print('writing "{}.phone" to {}'.format(dir_name, out_dir_name))
# create .phone file
with open(os.path.join(out_dir_name, dir_name + '.phone'), 'w') as f:
    for item in phone_counter:
        f.write(item.upper() + '\n')
    f.write('SIL\n')

############### used for Forced Alignment ###############
# create phoneme.dict file
print('writing "phonemes.dict"')
with open(os.path.join(dir_name, 'phonemes.dict'), 'w') as f:
    for item in phone_counter:
        if (item.lower() == 'ss'):
            f.write('ss\tS')
        else:
            f.write(item.lower() + '\t' + item.upper() + '\n')
    f.write('sil\tSIL\n')
# create words.dict file
print('writing "words.dict"')
with open(os.path.join(dir_name, 'words.dict'), 'w') as f:
    for item in counter:
        if item in sphinx_dic:
            index = sphinx_dic[item]
            row = sphinx_dic_list[index]
            row = row.split(item.lower())
            f.write(item.lower()+ '\t' + row[1].strip().upper() + '\n')
    f.write('sil\tSIL\n')

print('finished.')