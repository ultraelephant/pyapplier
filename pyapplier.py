#!/usr/bin/python3

import argparse
import datetime
import getpass
import pylast
import time
import yaml
import csv
import sys
import os

try:

  API_KEY = "b9cb047abc894c445999900d40ab0f37"
  API_SECRET = "95f53a50c42025faf59269fe95502f5b"

  homedir = os.path.expanduser("~")
  credsfile = '{}/.config/pyapplier/saved_creds'.format(homedir)


  def loadcreds (filepath,dry,select_user=None):
    with open(filepath) as file:
      creds_dict = yaml.full_load(file)
      if dry == True:
        try:
          for usernamepass in creds_dict['users']:
            testusername = usernamepass['username']
            testpass = usernamepass['hash']
          return True
        except:
          print ('Credential file was removed because it have not pass consistancy check')
          os.remove(filepath)
          getcreds(filepath)
      else:
        if len(creds_dict['users']) > 1:
          if select_user == None:
            listcreds(filepath)
            select_user = input('\nSelect username: ')
          for usernamepass in creds_dict['users']:
            if select_user == usernamepass['username']:
              username = usernamepass['username']
              password_hash = usernamepass['hash']
          try:
            username
          except NameError:
            print ('No user with name {}'.format(select_user))
            sys.exit(0)
        else:
          username = creds_dict['users'][0]['username']
          password_hash = creds_dict['users'][0]['hash']
    
        return username, password_hash


  def getcreds(filepath):
    username = input("Last.fm username: ")
    password = getpass.getpass("Last.fm password: ")
    password_hash = pylast.md5(password)
    while True: 
      answer_save = input("Would you like to save credentials?. y/n: ")
      answer_save = answer_save[0].lower() 
      if answer_save not in ['y','n']: 
          print('Please answer with y or n!') 
      else: 
          break
    if answer_save == 'y':
      try:
        os.makedirs('{}/.config/pyapplier'.format(homedir))
      except:
        pass
      creds_dict = {'users': [{'username': username, 'hash': password_hash}]}
      with open(filepath, 'w') as file:
        yamldump = yaml.dump(creds_dict, file)
    
    return username, password_hash


  def submitlog (filepath,dry,tracks=0,skip=0,network=None):
    with open(filepath) as tsv:
      iteration = 0
      skipped = 0
      for line in csv.reader(tsv, dialect="excel-tab"):
        iteration = iteration + 1
        if iteration < 4:
          continue
        if line[5] == 'S':
          skipped = skipped + 1
          if dry == False:
            print ('[X] Skipped ({}%): Artist: {}; Track: {}; Time: {}'.format(str(round(100*(iteration-3)/(tracks-3),2)),artist,track,unix_timestamp.strftime('%Y-%m-%d %H:%M:%S')))
          continue
        elif line[5] != 'L':
          print ('ERROR: .scrobbler.log malformed. Exiting...')
          sys.exit(1)
        try:
          artist = line[0]
          track = line[2]
          unix_timestamp = line[6]       
          unix_timestamp = datetime.datetime.fromtimestamp(int(unix_timestamp))
          local_tz = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
          unix_timestamp = unix_timestamp.replace(tzinfo=local_tz).astimezone(tz=datetime.timezone.utc)
        except:
          print ('ERROR: .scrobbler.log malformed. Exiting...')
          sys.exit(1)
        if dry == False:
          print ('[V] Scrobled ({}%): Artist: {}; Track: {}; Time: {}'.format(str(round(100*(iteration-3)/(tracks-3),2)),artist,track,unix_timestamp.strftime('%Y-%m-%d %H:%M:%S')))
          network.scrobble(artist=artist, title=track, timestamp=unix_timestamp.replace(tzinfo=local_tz).astimezone(tz=datetime.timezone.utc))
      if dry == False:
        print("\n{} tracks scrobbled".format(str(iteration-(3+skip))))
        os.remove(scrobblerlogpath)
      else:
        return iteration, skipped


  def wup(t):
    while t:
        mins, secs = divmod(t, 60)
        timeformat = 'Countdown: {:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        t -= 1
    print('\nDone!\n')


  def listcreds(filepath):
    try:
      with open(filepath) as file:
        creds_dict = yaml.full_load(file)
        print ('\n\nFollowing users credential saved on this device:')
        for usernamepass in creds_dict['users']:
          print ('\n\t{}'.format(usernamepass['username']))
        print ('\n\n')
    except:
      print('Can not open {}'.format(filepath))
      sys.exit(1)




  usage = '''
  credentials managment: pyapplier.py creds list | edit USERNAME | add USERNAME | del USERNAME
  .scrobbler.log submit: pyapplier.py -f /PATH/TO/.scrobbler.log [-w] [-y [USERNAME]]
  '''

  parser = argparse.ArgumentParser(usage=usage,formatter_class=argparse.RawTextHelpFormatter)
  parser.add_argument('creds',nargs='*',default=None,help=argparse.SUPPRESS)
  parser.add_argument('-w', '--warmup', action='store_true',default=False,help=argparse.SUPPRESS)
  parser.add_argument('-f', '--file',default=None,help=argparse.SUPPRESS)
  parser.add_argument('-y', '--yes',nargs='?',default=False,const=True,help=argparse.SUPPRESS)
  args = parser.parse_args()
  args = vars(args)

  if args['file'] == None and args['creds'] == []:
    print ('--file or creds argument required. --help for info')
    sys.exit(1)

  scrobblerlogpath = args['file']

  if args['creds'] and os.path.isfile(credsfile):
    loadcreds (credsfile,True)
    if 1 in range (len(args['creds'])):
      if args['creds'][1] == 'list':
        listcreds(credsfile)
        sys.exit(0)
      elif args['creds'][1] == 'edit' and 2 in range (len(args['creds'])):
        with open(credsfile) as file:
          creds_dict = yaml.full_load(file)
          for usernamepass in creds_dict['users']:
            if args['creds'][2] == usernamepass['username']:
              password = getpass.getpass("Last.fm password for user {}: ".format(args['creds'][2]))
              usernamepass['hash'] = pylast.md5(password)
              with open(credsfile, 'w') as file:
                yamldump = yaml.dump(creds_dict, file)
              sys.exit(0)
          print ('No user with name {}'.format(args['creds'][2]))
          sys.exit(0)
      elif args['creds'][1] == 'add' and 2 in range (len(args['creds'])):
        with open(credsfile) as file:
          creds_dict = yaml.full_load(file)
          username = args['creds'][2]
          password = getpass.getpass("Last.fm password: ")
          password_hash = pylast.md5(password)
          creds_dict['users'].append({'username': username, 'hash': password_hash})
          with open(credsfile, 'w') as file:
            yamldump = yaml.dump(creds_dict, file)
          sys.exit(0)
      elif args['creds'][1] == 'del' and 2 in range (len(args['creds'])):
        with open(credsfile) as file:
          creds_dict = yaml.full_load(file)
          iteration = 0
          for usernamepass in creds_dict['users']:
            if args['creds'][2] == usernamepass['username']:
              creds_dict['users'].pop(iteration)
              if len(creds_dict['users']) > 0:
                with open(credsfile, 'w') as file:
                  yamldump = yaml.dump(creds_dict, file)
              else:
                os.remove(credsfile)
              sys.exit(0)
            iteration = iteration + 1
          print ('No user with name {}'.format(args['creds'][2]))
          sys.exit(0)
      else:
        print ('Wrong arguments usage. Check pyapplier.py --help for info')
        sys.exit(0)
    else:
      print ('Wrong arguments usage. Check pyapplier.py --help for info')
      sys.exit(0)
  elif args['creds'] and not os.path.isfile(credsfile):
    print ('Credentials file not exist')
    sys.exit(0)




  try:
    if not os.path.isfile(credsfile):
      username, password_hash = getcreds(credsfile)
    else:
      if loadcreds (credsfile,True) == True:
        if type(args['yes']) == bool:
          username, password_hash = loadcreds(credsfile,False)
        else:
          username, password_hash = loadcreds(credsfile,False,args['yes'])
  except Exception as e:
    print (e)
    sys.exit(1)

  try:
    network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET, username=username, password_hash=password_hash)
  except Exception as e:
    print (e)
    sys.exit(1)

  if args['yes'] != False:
    pass
  else:
    answer_submit = input("Please be informed, .scrobbler.log will be removed after submiting. 'Yes' for continue: ")
    if answer_submit.lower() != 'yes':
      sys.exit(0)
  
  print ('\n')

  try:
    trackstoscrobb, trackstoskip = submitlog(scrobblerlogpath,True)
    if trackstoscrobb > 0:
      submitlog(scrobblerlogpath,False,trackstoscrobb,trackstoskip,network)
  except Exception as e:
    print (e)
    sys.exit(1)

  print ("\n")

  if args['warmup']:
    wup(300)
  else:
    print ("Please be informed, scrobbled tracks appears with delay. Delay may be up to 5 min. Use '-w' flag for 5 minutes timer after log submitting.")

except KeyboardInterrupt:
  sys.exit(0)