#!venv/bin/python


##################################################
# get_prox.py
#
# gets proxies, nothing more, nothing less
# 
#
# author kjutbring
##################################################

from bs4 import BeautifulSoup
import mechanize

in_url = 'http://proxy-list.org/english/index.php?p='

def get_proxies(url):
	br = mechanize.Browser()
	response = br.open(url)

	hot_soup = BeautifulSoup(response)

	div_content = hot_soup.find("div", {"class": "table"})

	proxies = div_content.findAll("li", {"class": "proxy"})

	return proxies

def main():
	proxlist = []

	for i in range(10):
		proxlist.append(get_proxies(in_url+str(i+1)))

	for a in proxlist:
		print a

if __name__ == "__main__":
	main()