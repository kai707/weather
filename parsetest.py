import argparse
parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument('-a')
group.add_argument('-b')
group.add_argument('-c')


