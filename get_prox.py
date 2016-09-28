#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################################################
# get_prox.py
#
# gets proxies, nothing more, nothing less.
# now also test if proxy is working.
#
# author kjutbring
##################################################

from bs4 import BeautifulSoup

import re
import mechanize
import time
import threading

in_url = 'http://proxy-list.org/english/index.php?p='

def get_proxies(url):

	print '[+] Starting...'

	br = mechanize.Browser()
	br.set_handle_robots(False)

	# add proxies to list
	proxy_list = []
	for i in range(3):
		try:
			resp = br.open(url+str(i+1))
		except:
			print '[-] Failed, check your internet connection.'

		cold_soup = BeautifulSoup(resp, "lxml")
		div = cold_soup.find("div", {"class": "table"})
		prox = div.findAll("li", {"class": "proxy"})

		# extraction from html string
		for proxy in prox:
			slice1=proxy.text[7:]
			slice2=slice1[:-2]
			proxy_list.append(slice2.decode('base64'))
	print "Got " + str(len(proxy_list)) + " Proxies"
	return proxy_list

def test_proxies(proxies):
	br = mechanize.Browser()
	br.set_handle_robots(False)
	br.addheaders = [('User-agent', 'Firefox')]

	with open('outprox.txt', 'w') as out_file:
		for proxy in proxies:
			try:
				print ('\033[33m' + "[+] Testing proxy: " + proxy + '\033[37m')
				br.set_proxies({"http": proxy})
				now = time.time()
				br.set_handle_refresh(False)
				resp = br.open("http://icanhazip.com")
				latency = (time.time())-now
				# strip port for comparission
				strip_proxy = ''.join(re.findall(r'[0-9]+(?:\.[0-9]+){3}', str(proxy)))

				if(resp.wrapped.code==200):
					if latency < 4:
						print ('\033[32m' + str(strip_proxy) + " is fine" + '\033[37m')
						out_file.write(proxy + "\n")
					elif latency > 4:
						print ('\033[33m' + str(strip_proxy) + " is kind of slow (latency: " + str(int(latency)) + " sec), ignoring." + '\033[37m')
				else:
					print ('\033[31m' + str(strip_proxy) + " is no good" + '\033[37m')

			except:
				print ('\033[31m' + "[-] Connection error, proxy: " + proxy + '\033[37m')

def main():
	plist = get_proxies(in_url)

	test_proxies(plist)

if __name__ == "__main__":
	main()
