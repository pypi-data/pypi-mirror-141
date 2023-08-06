#!/usr/bin/env python3
import argparse, sys, os, json, argcomplete, re
import subprocess
import vytools
from getpass import getpass


import logging
logging.basicConfig(level=logging.INFO)

TLIST = '(repo, vydir, definition, object, stage, compose, episode)'

def add_all(parser):
  parser.add_argument('--all', action='store_true', 
                      help='If present, rebuild all dependent stages. '
                            'Otherwise only rebuild top level and missing stages')

def make_parser():
  parser = argparse.ArgumentParser(prog='vytools', description='tools for working with vy')
  parser.add_argument('--version','-v', action='store_true', 
    help='Print vytools version')
  parser.add_argument('--contexts', type=str, default='',
    help='Comma or semi-colon delimited list of paths to context folders')
  parser.add_argument('--secret', metavar='KEY=VALUE', action = 'append', required=False,  default=[],
    help='Key-value pair for docker build secrets e.g. --secret MYSECRET=/path/to/my_secret.txt '
                            "(do not put spaces before or after the = sign). "
                            "Value is the path to the file containing the secret. If the path "
                            "contains spaces, you should define it with double quotes: "
                            'foo="/path/to some/place/secret".')
  parser.add_argument('--ssh', metavar='KEY=VALUE', action = 'append', required=False, default=[],
    help='Key-value pair for ssh keys e.g. --ssh MYKEY=/path/to/my_key '
                            "(do not put spaces before or after the = sign). "
                            "Value is the path to the ssh key. If the path "
                            "contains spaces, you should define it with double quotes: "
                            'foo="/path/to some/place/sshkey".')      
  parser.add_argument('--jobs', type=str, required=False, 
    help='Path to jobs folder. All jobs will be written to this folder.')
  parser.add_argument('--anchor','-a', metavar='KEY=VALUE', action = 'append', required=False,
                      help="Set key-value pairs "
                            "(do not put spaces before or after the = sign). "
                            "If a value contains spaces, you should define "
                            "it with double quotes: "
                            'foo="this is a sentence". Note that '
                            "values are always treated as strings.")      
  parser.add_argument('--name','-n', action='append', choices=vytools.CONFIG.get('items'),
    help='Name of thing '+TLIST+' ', metavar='')

  subparsers = parser.add_subparsers(help='specify action', dest='action')

  build_sub_parser = subparsers.add_parser('build',
    help='Build docker images that are dependent on named items')
  add_all(build_sub_parser)

  grep_sub_parser = subparsers.add_parser('grep',
    help='Grep logs or things '+TLIST)
  grep_sub_parser.add_argument('--pattern','-p', type=str, required=True, help='grep pattern')
  grep_sub_parser.add_argument('--flags','-f', action='append', help='grep flags, use a space before a dash. e.g. vytools grep --pattern "error:" -flags " -i" --lastlog', metavar='')
  grep_sub_parser.add_argument('--lastlog','-l', action='store_true', help='grep the last log')

  clean_sub_parser = subparsers.add_parser('clean',
    help='Clean images ')

  info_sub_parser = subparsers.add_parser('info',
    help='Print things '+TLIST)
  info_sub_parser.add_argument('--images','-i', action='store_true', 
    help='List images')
  info_sub_parser.add_argument('--private','-p', action='store_true', 
    help='List ssh/secrets')
  info_sub_parser.add_argument('--dependencies','-d', action='store_true', 
    help='List dependencies of items')
  info_sub_parser.add_argument('--expand','-e', action='store_true', 
    help='Expand items')

  upload_sub_parser = subparsers.add_parser('upload',
    help='Upload bundles')
  upload_sub_parser.add_argument('--force','-f', action='store_true',
    help='Force updates without confirming')
  upload_sub_parser.add_argument('--url', type=str, default='https://vy.tools',
    help='Upload url')
  upload_sub_parser.add_argument('--username','-u', type=str,
    help='https://vy.tools username')
  upload_sub_parser.add_argument('--token', type=str,
    help='https://vy.tools token')

  run_sub_parser = subparsers.add_parser('run',
    help='Run specified stage/compose/episode items')
  run_sub_parser.add_argument('--save','-s', action='store_true', 
    help='If present, save episodes.')
  run_sub_parser.add_argument('--build', action='store_true', 
    help='If present, build dependent stages (also note --all flag).')
  add_all(run_sub_parser)
  run_sub_parser.add_argument('--persist','-p', action='store_true', 
    help='Persist created docker volumes after running')
  run_sub_parser.add_argument('--clean', action='store_true', 
    help='Clean episode folders before running')
  run_sub_parser.add_argument('--compose', type=str, required=False, 
    help='Replace default episode compose file')
  run_sub_parser.add_argument('--object-mods','-o', metavar='KEY=VALUE', action = 'append', required=False,
                      help='Set key-value pairs of objects '
                            '(do not put spaces before or after the = sign). '
                            'If a value contains spaces, you should define '
                            'it with double quotes: foo="this is a sentence". Note that '
                            'values are always treated as strings.')  
  run_sub_parser.add_argument('--cmd', type=str, required=False, 
    help='Stage command')

  return parser

def parse_key_value(kv,typ):
  args = {}
  success = True
  if kv:
    for arg in kv:
      if '=' not in arg:
        success = False
        logging.error('A {s} ({a}) failed to be in the form KEY=VALUE'.format(s=typ,a=arg))
      else:
        (k,v) = arg.split('=',1)
        args[k] = v
  return (success, args)

def parse_anchors(ba):
  return parse_key_value(ba,'anchor (--anchor, -a)')

def parse_object_mods(args):
  oa = args.object_mods if 'object_mods' in dir(args) and args.object_mods else []
  (success, obj) = parse_key_value(oa,'object-mods (--object-mods, -o)')
  if success:
    for k,v in obj.items():
      try:
        obj[k] = json.loads(v)
      except Exception as exc:
        logging.error('Failed to parse input object-mods:'+str(exc))
        success = False
  return (success, obj)

def grep(lst,pattern,flags,lastlog):
  cmd = ['grep',pattern]
  out = ''
  if flags: cmd += [f.strip() for f in flags]
  if lastlog:
    path = os.path.join(vytools.CONFIG.job_path(),'__dockerfiles__')
    paths = [os.path.join(path, basename) for basename in os.listdir(path) if basename.endswith('.log')]
    if len(paths) > 0:
      out = subprocess.check_output(cmd+[max(paths, key=os.path.getctime)]).decode('utf8')
  else:
    pass
  print(out)

def main():
  notScanningPreexistingContext = vytools.CONFIG.get('contexts') and '--contexts' not in sys.argv
  notAskingForHelp = '-h' not in sys.argv and '--help' not in sys.argv
  notAskingForVersion = '-v' not in sys.argv and '--version' not in sys.argv
  someArguments = len(sys.argv)>1
  if notScanningPreexistingContext and someArguments and notAskingForHelp and notAskingForVersion:
    vytools.printer.print_def('scanning...')
    vytools.scan()
  parser = make_parser()
  argcomplete.autocomplete(parser)
  args = parser.parse_args()
  if args.version:
    vytools.printer.print_def(vytools.__version__)
    return

  if args.contexts: 
    vytools.CONFIG.set('contexts', re.split(';|,',args.contexts))
    vytools.scan()
  if args.jobs: vytools.CONFIG.set('jobs',args.jobs)
  if vytools.stage.DOCKER_VERSION is None:
    vytools.printer.print_fail('Docker does not appear to be installed. Install docker and docker-compose')
  if not vytools.CONFIG.get('contexts'):
    vytools.printer.print_fail('The vy context(s) has not been initialized. Please provide a --contexts')
    return

  if 'ssh' in dir(args) and args.ssh:
    success, sshkeys = parse_key_value(args.ssh,'argument (--ssh)')
    if not success: return
    vytools.CONFIG.set('ssh', sshkeys)
  if 'secret' in dir(args) and args.secret:
    success, secrets = parse_key_value(args.secret,'argument (--secret)')
    if not success: return
    vytools.CONFIG.set('secrets', secrets)

  lst = [n for n in args.name] if 'name' in dir(args) and args.name else []
  anchor_args = None if 'anchor' not in dir(args) else args.anchor
  rootcompose = args.compose if 'compose' in dir(args) else None
  success, anchors = parse_anchors(anchor_args)
  if not success: return
  build_level = 1 if 'all' in dir(args) and args.all else 0
  persist = args.persist if 'persist' in dir(args) else False
  if args.action == 'build':
    return bool(vytools.build(lst, anchors=anchors, build_level=build_level, compose=rootcompose))
  elif args.action == 'clean':
    vytools.clean()
  elif args.action == 'run':
    success, object_mods = parse_object_mods(args)
    if not success: return
    cmd = None if 'cmd' not in dir(args) else args.cmd
    if object_mods == False:
      return False
    if args.build:
      br = vytools.build(lst, anchors=anchors, build_level=build_level, compose=rootcompose)
      if br == False: return False
    return bool(vytools.run(lst, anchors=anchors, clean=args.clean, save=args.save, object_mods=object_mods, cmd=cmd, persist=persist, compose=rootcompose))
  elif args.action == 'upload':
    uname = input('Enter username:') if ('username' not in dir(args) or not args.username) else args.username
    token = getpass('Enter token:') if ('token' not in dir(args) or not args.token) else args.token
    vytools.upload(lst, args.url, uname, token, check_first=not args.force)
  elif args.action == 'info':
    vytools.info(lst, list_dependencies=args.dependencies, list_private=args.private, list_images=args.images, expand=args.expand)
  elif args.action == 'grep':
    flags = args.flags if 'flags' in dir(args) else None
    lastlog = args.lastlog if 'lastlog' in dir(args) else None
    grep(lst, args.pattern, flags, lastlog)
  else:
    return False
