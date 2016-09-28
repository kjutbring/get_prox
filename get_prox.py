#!venv/bin/python

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

in_url = 'http://proxy-list.org/english/index.php?p='

def get_proxies(url):
	
	print '[+] Starting...'
	
	br = mechanize.Browser()
	br.set_handle_robots(False)

	# add proxies to list
	proxy_list = []
	for i in range(10):
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
				print "[+] Testing proxy: " + proxy
				br.set_proxies({"http": proxy})
				resp = br.open("http://icanhazip.com")
				ip = BeautifulSoup(resp, "lxml")
				# strip port for comparission
				strip_proxy = ''.join(re.findall(r'[0-9]+(?:\.[0-9]+){3}', str(proxy)))

				if str(ip).strip() == str(strip_proxy):
					print "[+] Proxy ok!"
					out_file.write(proxy + "\n")
				else:
					print "[-] Proxy not ok!"
					print str(ip) + " : " + strip_proxy
			except:
				print "[-] Connection error, proxy: " + proxy

def main():
	plist = get_proxies(in_url)

	test_proxies(plist)

if __name__ == "__main__":
	main()
