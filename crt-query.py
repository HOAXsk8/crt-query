# crt-query.py

''' This program searches crt.sh for registered certificates for a company name or url, scrapes the generated
	html and writes the set of hosts to a text file '''


import requests
from bs4 import BeautifulSoup
import re


def get_soup(search_query):
	""" Takes a search query, sends a request to crt.sh and returns the raw html """

	page = requests.get("http://crt.sh/?q=" + search_query)
	soup = BeautifulSoup(page.content, "html.parser")
	return soup


def extract_hosts(raw_html):
	""" Find the host names using regex, trim them, and append to a set (no duplicate records) """

	hosts = set()

	raw_list = re.findall(r"(\>.*?\.[a-zA-Z0-9].*?\.[a-zA-Z0-9].*?\<)", str(raw_html))	
	for i in raw_list:

		if "<br/>" in i:
			host = i.split("<br/>")
			host = host[1].split("<")
			host = host[0]
			if host.startswith("*."):
				host = host.split("*.")
				host = host[1]
			if host:
				hosts.add(host)

		elif ">" in i:
			host = i.split(">")
			host = host[1].split("<")
			host = host[0]
			if host.startswith("*."):
				host = host.split("*.")
				host = host[1]
			if host:
				hosts.add(host)

	return hosts
	

def write_to_file(data, file, mode="a"):
    """ Write data to a file. Default write mode=append """

    with open(file, mode) as new_file:
        new_file.write(str(data + "\r\n"))
        new_file.close()


def main():
	file_name = "hosts.txt"

	query = input("Enter a search query or url... ")
	soup = get_soup(query)
	hosts = extract_hosts(soup)
	for i in hosts:
		write_to_file(i, file_name)


if __name__ == "__main__":
	main()