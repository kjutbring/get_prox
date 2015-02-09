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
import os
import re
import requests

in_url = 'http://proxy-list.org/english/index.php?p='

def get_proxies(url):
	
	print '[+] Starting...'
	
	# add proxies to list
	proxy_list = []
	for i in range(10):
		try:
			resp = requests.get(url+str(i+1))
		except:
			print '[-] Failed, check your internet connection.'

		cold_soup = BeautifulSoup(resp.text)
		div = cold_soup.find("div", {"class": "table"})
		prox = div.findAll("li", {"class": "proxy"})

		# extraction from html string
		for proxy in prox:
			proxy_list.append(''.join(re.findall(r'[0-9]+(?:\.[0-9]+)(?:\.+)*(?:\:[0-9]+)*', str(proxy))))

	return proxy_list

def test_proxies(proxies):
	pass

def main():
	plist = get_proxies(in_url)

	for i in plist:
		print i

if __name__ == "__main__":
	main()