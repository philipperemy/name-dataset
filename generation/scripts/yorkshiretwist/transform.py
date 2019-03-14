import sys

open(sys.argv[1] + '.out', 'w').write('\n'.join([a.strip() for a in open(sys.argv[1], 'r').readlines()]))
