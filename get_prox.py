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
import threading




in_url = 'http://proxy-list.org/english/index.php?p='


def get_proxies(url):
	print '[+] Starting...'
	br = mechanize.Browser()
	br.set_handle_robots(False)

	# add proxies to list
	proxy_list = []
	for i in range(10):
		try:
			resp = br.open(url + str(i + 1))
		except:
			print '[-] Failed, check your internet connection.'

		cold_soup = BeautifulSoup(resp, "lxml")
		div = cold_soup.find("div", {"class": "table"})
		prox = div.findAll("li", {"class": "proxy"})

		# extraction from html string
		for proxy in prox:
			slice1 = proxy.text[7:]
			slice2 = slice1[:-2]
			proxy_list.append(slice2.decode('base64'))
	print "Got " + str(len(proxy_list)) + " Proxies"
	return proxy_list


def ProxyTester(SingleProxy):
	br = mechanize.Browser()
	br.set_handle_robots(False)
	br.addheaders = [('User-agent', 'Firefox')]
	with open('outprox.txt', 'a') as out_file:
		try:
			print ('\033[33m' + "[+] Testing proxy: " + SingleProxy + '\033[37m')
			br.set_proxies({"http": SingleProxy})
			req = br.open("http://icanhazip.com", timeout=30)
			ipGotten=req.read().strip()
			br.close()
			strip_proxy = ''.join(re.findall(r'[0-9]+(?:\.[0-9]+){3}', str(SingleProxy)))

			# Sort though the responses:
			if ipGotten == strip_proxy:
					print ('\033[32m' + str(strip_proxy) + " is fine" + '\033[37m')
					out_file.write(SingleProxy + "\n")
			else:
				print ('\033[31m' + "[-] Proxy not ok! (" + str(strip_proxy)  + ') \033[37m')

		except Exception as e:
			print e
			print ('\033[31m' + "[-] Connection error, proxy: " + SingleProxy + '\033[37m')


def main():
	plist = get_proxies(in_url)
	threadList = []
	NumberOfThreads = 7
	for each in range(NumberOfThreads):
		try:
			while plist > 0:
				NewProxy = plist.pop()
				t = threading.Thread(target=ProxyTester, args=(NewProxy,))
				t.start()
				threadList.append(t)

		except Exception as e:
			print e

if __name__ == "__main__":
	main()
