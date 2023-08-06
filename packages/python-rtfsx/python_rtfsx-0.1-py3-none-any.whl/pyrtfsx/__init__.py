import argparse
from rtfs_code import Bottle

parser = argparse.ArgumentParser('Pyrtfs-cli', usage='A Shortcut for the pyrtfs module', description='Run a shortcut command for pyrtfs on the timeline')
f = parser.add_argument('--bottle',  type=str,  metavar='-r', help='start running')
f = parser.add_argument('--r', type=str,  metavar='-r',)
cl = parser.parse_args()
if cl.bottle:
    if cl.bottle == '.':
        pass
    elif cl.bottle.endswith('.'):
        pass
    elif cl.bottle == (' '):
        pass
    else:
        f = open('Pyrtfs/bottle.txt', 'w+')
        if cl.bottle in f:
            pass
        else:
            f.write(cl.bottle)

if cl.r:
    if cl.r == '.':
        pass
    elif cl.r.endswith('.'):
        pass
    elif cl.r == (' '):
        pass
    else:
        f = open('Pyrtfs/bottle.txt', 'r+')
        bottle = Bottle()
        bottle.LoadFile(f.read())