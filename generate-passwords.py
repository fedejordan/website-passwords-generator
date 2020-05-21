import argparse
import urllib.request
from bs4 import BeautifulSoup
import io
import sys

def capture_args():
	parser = argparse.ArgumentParser(description='Generates random passwords combining words from desired website')
	parser.add_argument('url', metavar='U', type=str, 
	                   help='url of the website to get words')
	parser.add_argument('--output', dest='output', type=str, default='output.txt',
	                   help='output file to export list (default output.txt)')
	parser.add_argument('--minimum-characters', type=int, dest='min_char', default=3,
	                   help='minimum amount of characters to consider a word (default: 3)')
	parser.add_argument('--combinations-number', type=int, dest='combinations_number', default=2,
	                   help='number of combinations between words (default: 2)')
	return parser.parse_args()

def get_text_from_url(url):
	html = urllib.request.urlopen(url).read()
	soup = BeautifulSoup(html, features="html.parser")

	# kill all script and style elements
	for script in soup(["script", "style"]):
	    script.extract()    # rip it out

	# get text
	text = soup.get_text()

	# break into lines and remove leading and trailing space on each
	lines = (line.strip() for line in text.splitlines())
	# break multi-headlines into a line each
	chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
	# drop blank lines
	return '\n'.join(chunk for chunk in chunks if chunk)

def get_words(text, min_char):
	s = io.StringIO(text)
	words = []
	for line in s:
		possible_words = line.split()
		for possible_word in possible_words:
			if len(possible_word) >= min_char:
				words.append(possible_word)

def combinate_words(words, combinations_number, previous_combinations=[]):
	if len(previous_combinations) == 0:
		return combinate_words(words, combinations_number, words)

	new_combinations = []
	for word in words:
		for previous_combination in previous_combinations:
			new_combinations.append(word + previous_combination)

	if combinations_number > 1:
		return combinate_words(words, combinations_number - 1, new_combinations)
	return new_combinations

def generate_output(list, outputFile):
	with open(outputFile, 'w') as f:
		for item in list:
			f.write("%s\n" % item)

args = capture_args()
print("Getting text from " + args.url)
text = get_text_from_url(args.url)
print("Getting possible words...")
words = get_words(text, args.min_char)
print("Making combinations...")
list = combinate_words(words, args.combinations_number)
print("Generating file with " + str(len(list)) + " combinations. Total " + str(sys.getsizeof(list)) + " bytes")
generate_output(list, args.output)
print("Done.")
