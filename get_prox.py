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
import re

in_url = 'http://proxy-list.org/english/index.php?p='

def get_proxies(url):
	br = mechanize.Browser()
	response = br.open(url)

	# add proxies to list
	proxy_list = []
	for i in range(10):
		resp = br.open(url+str(i+1))
		cold_soup = BeautifulSoup(resp)
		div = cold_soup.find("div", {"class": "table"})
		prox = div.findAll("li", {"class": "proxy"})

		# extraction from html string
		for proxy in prox:
			proxy_list.append(''.join(re.findall(r'[0-9]+(?:\.[0-9]+)(?:\.+)*(?:\:[0-9]+)*', str(proxy))))

	return proxy_list

def main():
	plist = get_proxies(in_url)

	for i in plist:
		print i

if __name__ == "__main__":
	main()