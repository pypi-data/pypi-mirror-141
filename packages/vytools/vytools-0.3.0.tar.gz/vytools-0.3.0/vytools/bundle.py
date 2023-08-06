import hashlib, logging, json, io, glob, requests, os
import vytools.utils as utils
import vytools.printer
from vytools.config import ITEMS
import cerberus
from pathlib import Path

SCHEMA = utils.BASE_SCHEMA.copy()
SCHEMA.update({
  'thingtype':{'type':'string', 'allowed':['bundle']},
  'publish':{'type':'boolean','required':False},
  'bundles':{
    'type':'list',
    'schema': {
      'type': 'dict',
      'schema': {
        'name': {'type': 'string', 'maxlength': 128},
        'serch': {'type': 'string', 'maxlength': 128},
        'rplce': {'type': 'string', 'maxlength': 128}
      }
    }
  },
  'philes':{
    'type':'list',
    'schema': {
      'type': 'dict',
      'schema': {
        'path': {'type': 'string', 'maxlength': 1024},
        'name': {'type': 'string', 'maxlength': 128},
        'hash': {'type': 'string', 'maxlength': 32}
      }
    }
  }
})

VALIDATE = cerberus.Validator(SCHEMA)

def fhash(pth):
  md5 = hashlib.md5()
  BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
  try:
    with open(pth, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)
  except Exception as exc:
    logging.error('Failed to get hash for {}: {}'.format(pth,exc))
  return md5.hexdigest()

def parse(name, pth, items):
  item = {
    'name':name,
    'thingtype':'bundle',
    'philes':[],
    'bundles':[],
    'depends_on':[],
    'path':pth,
    'loaded':True
  }
  try:
    content = json.load(io.open(pth, 'r', encoding='utf-8-sig'))
    item['bundles'] = content.get('bundles',[])
    item['publish'] = content.get('publish',False)
    for phile in content.get('philes',[]):
      path = phile.get('path',None)
      prefix = phile.get('prefix',None)
      if path is not None:
        thisdir = os.getcwd()
        try:
          dirpath = os.path.dirname(pth)
          os.chdir(dirpath)
          file_list = glob.glob(path,recursive=True)
          # print('----------',item['name'],file_list)
          for file in file_list:
            filepath = os.path.join(dirpath,file)
            if not os.path.isfile(filepath) or any([file.endswith(ext) for ext in ['.bundle.json','.vydir']]):
              continue
            item['philes'].append({
              'name':file if not prefix else prefix+'/'+file,
              'hash':fhash(filepath),
              'path':filepath
            })
            # print(item['philes'][-1])
        except Exception as exc:
          logging.error('Failed to parse object "{n}" at "{p}": {e}'.format(n=name, p=pth, e=exc))
          return False
        os.chdir(thisdir)
  except Exception as exc:
    logging.error('Failed to parse object "{n}" at "{p}": {e}'.format(n=name, p=pth, e=exc))
    return False

  return utils._add_item(item, items, VALIDATE)

def find_all(items, contextpaths=None):
  success = utils.search_all(r'(.+)\.bundle\.json', parse, items, contextpaths=contextpaths)
  if success: # process bundles
    for (type_name, item) in items.items():
      if type_name.startswith('bundle:'):
        (typ, name) = type_name.split(':',1)
        item['depends_on'] = []
        successi = True
        for e in item['bundles']:
          if e['name'] in items:
            item['depends_on'].append(e['name'])
          else:
            successi = False
            logging.error('bundle "{n}" has an reference to a bundle {t}'.format(n=name, t=e['name']))
        success &= successi
        item['loaded'] &= successi
        utils._check_self_dependency(type_name, item)
  return success

def _update_bundle(bundle,check_only,url,headers):
  bundle['check_only'] = check_only
  res = requests.post(url+'/update_bundle', json=bundle, headers=headers)
  result = res.json()
  if not result.get('processed',False):
    return json.dumps(result)
  elif check_only:
    if result.get('confirm',False):
      if 'y' != input(result['confirm']).lower():
        return ' update canceled'
    elif result.get('nochange',False):
      return ' bundle is identical in database'
  return result

def upload(type_name, url, uname, token, check_first, items=None):
  if items is None: items = ITEMS
  if not utils.ok_dependency_loading('upload', type_name, items):
    return False
  headers = {'token':token, 'username':uname}
  success = True
  reason = ''
  try:
    bundle = items[type_name]
    result = _update_bundle(bundle, check_first, url, headers)
    if type(result) == str:
      vytools.printer.print_info('Bundle "{n}" not updated: {e}'.format(n=type_name, e=result))
      return False
    elif check_first:
      result = _update_bundle(bundle, False, url, headers)
      if type(result) == str:
        vytools.printer.print_fail('Failed upload of bundle "{n}" {e}'.format(n=type_name, e=result))
        return False

    refresh = result.get('refresh')
    for phile in bundle['philes']:
      if phile['name'] in refresh:
        res = requests.post(url+'/update_phile', json={'_id':refresh[phile['name']],
          'hash':phile['hash'],
          'content':Path(phile['path']).read_text()},headers=headers)
        if not res.json().get('processed',False):
          success = False
          vytools.printer.print_fail('Failed to update phile "{}": {}'.format(phile['name'],res.json()))
        else:
          vytools.printer.print_success('Uploaded updated phile "{}"'.format(phile['name']))
    res = requests.post(url+'/clean_philes', json={}, headers=headers)
  except Exception as exc:
    reason = exc
    success = False

  if not success:
    vytools.printer.print_fail('Failed upload of bundle "{n}" {e}'.format(n=type_name, e=reason))
  else:
    vytools.printer.print_success('Finished uploading bundle "{}"'.format(type_name))
  return success

def upload_all(url, uname, token, check_first, items=None):
  if items is None: items = ITEMS
  lst = [type_name for type_name in items if type_name.startswith('bundle')]
  for type_name in vytools.utils.sort(lst, items):
    upload(type_name, url, uname, token, check_first, items=items)
