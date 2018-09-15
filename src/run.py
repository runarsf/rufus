""" run bot """
import os

# check config
if not os.path.isfile('config.py'):
    confile = open('config.py', 'w+')

    confile.write('token = \'\'\n')
    confile.write('puush = \'\'\n')
    confile.write('prefix = \'>\'\n')
    confile.write('game = \'in his container\'\n')
    confile.write('games = [\'1\',\'2\']\n')
    confile.write('description = \'Descropt\'\n')
    confile.write('start_msg = \'\'\n')
    confile.write('\n')
    confile.write('announcements_id = \'290272570425737216\'\n')
    confile.write('owner_id = \'177098893069254656\'\n')
    confile.write('dev_id = [\'85467784179351552\', \'198414561706115072\']\n')
    confile.write('admin_id = [\'315908137976856579\', \'198414561706115072\']\n')
    confile.write('swears = [\'frick\', \'heck\']\n')
    confile.write('mention = [\'rufus\', \'runar\']\n')

    confile.close()
    print('created config from template')
    exit()

print('detected config file, continuing')

import rufus