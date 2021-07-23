#!/usr/bin/env python3

import requests
import re
import sys
import os
import threading
import tempfile
import colorama
from bs4 import BeautifulSoup
from argparse import *
from datetime import datetime




BANNER = """
   ___            _                        _  _  
  / __|   _  _   | |__   __ __ __ __ _    | || | 
  \__ \  | +| |  | '_ \  \ V  V // _` |    \_, | 
  |___/   \_,_|  |_.__/   \_/\_/ \__,_|   _|__/  
_|\"\"\"\"\"\|_|\"\"\"\"\"|_|\"\"\"\"\"|_|\"\"\"\"\"|_|\"\"\"\"\"|_| \"\"\"\"| 
\"`-0-0-'\"`-0-0-'\"`-0-0-'\"`-0-0-'\"`-0-0-'\"`-0-0-'

"""


HTML_OBJECTS =	{
	"a": "href",
	"applet": ["archive","codebase"],
	"area": "href",
	"base": "href",
	"blockquote": "cite",
	"body": "background",
	"del": "cite",
	"form": "action",
	"frame": ["src","longdesc"],
	"head": "profile",
	"iframe": ["src","longdesc"],
	"img": ["src","srcset","longdesc","usemap"],
	"input": ["src","usemap"],
	"ins": "cite",
	"link": "href",
	"object": ["classid","codebase","data","usemap"],
	"q": "cite",
	"script": "src",
	"audio": "src",
	"button": "formaction",
	"command": "icon",
	"embed": "src",
	"html": "manifest",
	"input": "formaction",
	"source": "src",
	"track": "src",
	"video": ["poster","src"],
	"source": "srcset",
	"meta": "content",
}

def parse_url(url):
	if url.startswith('http'):
		url = re.sub(r'https?://', '', url)
	if url.startswith('www.'):
		url = re.sub(r'www.', '', url)
	return url

# TODO: make this pull subdomains from various apis
def enum(wordlist, output_file, url):
	try:
		url = parse_url(url)
		f = open(wordlist, 'r')
		lines = f.readlines()
		for line in lines:
			sub = check_status(f"{line.strip()}.{url}")
			if sub:
				if output_file:
					save_output(output_file, sub)
				else:
					pass
			else:
				pass
	except Exception as e:
		print(f"[ERROR] {str(e)}")


def recursive_enum(file, tmpfile, depth):
	url_l = url
	for i in range(depth):
		for line in file:
			url_l = line + "." + url_l
			if check_status(url_l):
				tmpfile.write(check_status[1] + "\n")
				url_l = url_l + "/" + line
				file = tmpfile
				#Theres a massive logic flaw in this function, do not use until fixed


def save_output(file, data):
	with open(file, 'w') as f:
		f.write(data + "\n")


def check_status(url_l):
	try:
		print(f"[*]Currently trying: {url_l}", end='\r')
		r = requests.get(f"http://{url_l}", timeout=5)
	except requests.ConnectionError:
		pass
	else:
		r = requests.get(f"http://{url_l}")
		r_unicode = r.text
		title = r_unicode[r_unicode.find('<title>') + 7 : r_unicode.find('</title>')]
		r.close()
		print(f"[{title}][{r.status_code}] {url_l}")
		return f"[{title}][{r.status_code}] {url_l}"

def print_info(url_l, wordlist_l, output):
	text_break = "\n" + ("="*50) + "\n"

	print(f"{text_break}Started @ [{datetime.now()}]\nHostname: {url_l}\nVersion: 0.1\nWordlist: {wordlist_l}\nOuput file: {output}{text_break}")


def main():

	#TODO: ???
	parser = ArgumentParser(description="Enumerate subdomains and URLs",
							usage="use '%(prog)s --help' for more information",
							formatter_class=RawTextHelpFormatter)
	parser.add_argument("--banner", "-b", help="disable banner")
	parser.add_argument("--url", "-u", required=True, help="Target URL")

	parser.add_argument("--output", "-o", dest="output", help="Output file")
	parser.add_argument("--wordlist", "-w", default=None,
						help="Subdomain wordlist")

	parser.add_argument("--multisub", "-ms", help="multilevel subdomain enumeration")
	parser.add_argument("--crawl", "-c", action='store_true', help="crawl source for URLs")
	parser.add_argument("--outurl", "-ou", action='store_true', help="output ALL found URLs")
	parser.add_argument("--inurl", "-iu", action='store_true',
						help="include URLs that are found inside the site's source [href]")
	parser.add_argument("--inaurl", "-iau", action='store_true',
						help="include ALL found URLs in the site's source [href]")
	args = parser.parse_args()
	
	
	if args.banner:
		pass
	else:
		print(BANNER)

	url = args.url
	wordlist = args.wordlist
	output = args.output
	print_info(url, wordlist, output)

	try:
		enum(wordlist, output, url)
	except KeyboardInterrupt as e:
		print(f"\n\nYou have exited the program...")
	
	# ======================================================================
	# The purpose of this code is to save time by fuzzing subdomains
	# recursively by using process of elimination to create
	# a new wordlist to be used in the next iteration/depth
	# ======================================================================
	


"""	if args.multisub:
		temp_wordlist = tempfile.mkstemp()
		with os.fdopen(temp_wordlist, 'w') as tmp_f:
				with open(wordlist) as wordlist_f:
					recursive_enum(wordlist_f, tmp_f, args.multisub[1])
		os.remove(temp_wordlist)

	# ======================================================================

	if args.crawl:
		r = s_request(url)
		for link in BeautifulSoup(r, parse_only=SoupStrainer('a')):
			for i in link:
				if link.has_attr('href'):
					print(link['href'])
					if args.outurl:
						pass
					if args.inurl:
						pass
					if args.inaurl:
						pass
						"""

	#TODO: multithread this shit

if __name__ == "__main__":
	main()
