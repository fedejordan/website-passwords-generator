import argparse

parser = argparse.ArgumentParser(description='Generates random passwords combining words from desired website')
parser.add_argument('url', metavar='U', type=str, 
                   help='url of the website to get words')
parser.add_argument('--output', dest='output', default='output.txt',
                   help='output file to export list (default output.txt)')

args = parser.parse_args()
print(args.url)

# import urllib.request

# uf = urllib.request.urlopen(url)
# html = uf.read()