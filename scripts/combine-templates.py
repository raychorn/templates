import os
import sys
import json

import dotenv

fp_env = dotenv.find_dotenv()
print(fp_env)
dotenv.load_dotenv(fp_env, verbose=True)

do_these_match = lambda a,b:a == b

ppath = os.environ.get('PYTHON_PATH')
if (isinstance(ppath, str) and (len(ppath) > 0)):
    paths = ppath.split(os.pathsep)
    for p in paths:
        cnt = 0
        for i,pp in enumerate(sys.path):
            if (do_these_match(pp, p)):
                cnt += 1
                continue
        if (cnt == 0):
            sys.path.insert(0, p)

print('-'*30)
for f in sys.path:
    print(f)
print('-'*30)

class CaseInsensitiveDict(dict):
    @classmethod
    def _k(cls, key):
        return key.lower() if isinstance(key, str) else key

    def __init__(self, *args, **kwargs):
        super(CaseInsensitiveDict, self).__init__(*args, **kwargs)
        self._convert_keys()
    def __getitem__(self, key):
        return super(CaseInsensitiveDict, self).__getitem__(self.__class__._k(key))
    def __setitem__(self, key, value):
        super(CaseInsensitiveDict, self).__setitem__(self.__class__._k(key), value)
    def __delitem__(self, key):
        return super(CaseInsensitiveDict, self).__delitem__(self.__class__._k(key))
    def __contains__(self, key):
        return super(CaseInsensitiveDict, self).__contains__(self.__class__._k(key))
    def has_key(self, key):
        return super(CaseInsensitiveDict, self).has_key(self.__class__._k(key))
    def pop(self, key, *args, **kwargs):
        return super(CaseInsensitiveDict, self).pop(self.__class__._k(key), *args, **kwargs)
    def get(self, key, *args, **kwargs):
        return super(CaseInsensitiveDict, self).get(self.__class__._k(key), *args, **kwargs)
    def setdefault(self, key, *args, **kwargs):
        return super(CaseInsensitiveDict, self).setdefault(self.__class__._k(key), *args, **kwargs)
    def update(self, E={}, **F):
        super(CaseInsensitiveDict, self).update(self.__class__(E))
        super(CaseInsensitiveDict, self).update(self.__class__(**F))
    def _convert_keys(self):
        for k in list(self.keys()):
            v = super(CaseInsensitiveDict, self).pop(k)
            self.__setitem__(k, v)


fpath = os.path.dirname(os.path.dirname(__file__))

source_file1 = '{}/new-templates.json'.format(fpath)
source_file2 = '{}/templates-2.0.json'.format(fpath)
source_file3 = '{}/templates-1.20.0.json'.format(fpath)

sources = [source_file1, source_file2, source_file3]

for i in range(0, 999):
    source_fileN = '{}/template-self-hoststed{}.json'.format(fpath, i)
    if (os.path.exists(source_fileN) and os.path.isfile(source_fileN)):
        sources.append(source_fileN)

target_file = '{}/templates.json'.format(fpath)

def change_filename(fname, new_name=None):
    if (isinstance(new_name, str)) and (len(new_name) > 0):
        toks = list(os.path.splitext(fname))
        toks[0] = toks[0]+'_'+new_name
        return ''.join(toks)
    return fname

new_target_file = change_filename(target_file, 'new')

def read_templates(fname):
    try:
        data = None
        with open(fname, 'r') as f:
            data = json.load(f)
    except:
        pass
    return data

def read_templates_as_dict(fname=None, data=None, dict_class=dict):
    d = dict_class()
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
d_target = read_templates_as_dict(data=target_data, dict_class=CaseInsensitiveDict)

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

old_target_file = change_filename(target_file, 'old')
os.rename(target_file, old_target_file)
os.rename(new_target_file, target_file)

print('Done.')