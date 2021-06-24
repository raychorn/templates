import os
import sys
import json

fpath = os.path.dirname(os.path.dirname(__file__))

source_file1 = '{}/new-templates.json'.format(fpath)
source_file2 = '{}/templates-2.0.json'.format(fpath)
source_file3 = '{}/templates-1.20.0.json'.format(fpath)

sources = [source_file1, source_file2, source_file3]
target_file = '{}/templates.json'.format(fpath)

toks = list(os.path.splitext(target_file))
toks[0] = toks[0]+'_new'

new_target_file = ''.join(toks)

def read_templates(fname):
    try:
        data = None
        with open(fname, 'r') as f:
            data = json.load(f)
    except:
        pass
    return data

def read_templates_as_dict(fname=None, data=None):
    d = {}
    try:
        data = read_templates(fname) if (data is None) else data

        tplates = data.get('templates', []) if (isinstance(data, dict)) else data
        for t in tplates:
            tt = d.get('title')
            if (tt):
                print('DUPE: {}'.format(tt))
            else:
                d[t.get('title')] = t
    except:
        pass
    return d

d_sources = [read_templates_as_dict(fname=f) for f in sources]

target_data = read_templates(target_file)
d_target = read_templates_as_dict(data=target_data)

additions = []
for d in d_sources:
    for title,tplate in d.items():
        item = d_target.get(title)
        if (item):
            print('Found: {}'.format(title))
            #print('New:\n{}'.format(json.dumps(tplate, indent=3)))
            #print('Target:\n{}'.format(json.dumps(item, indent=3)))
            #print('\n\n')
            continue
        additions.append(tplate)
        target_data.append(tplate)

print('There are {} additions.'.format(len(additions)))
print('Writing {} templates.'.format(len(target_data)))
with open(new_target_file, 'w') as fOut:
    print(json.dumps(target_data, indent=3), file=fOut)
print('Done.')