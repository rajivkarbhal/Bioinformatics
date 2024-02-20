#This script for UniProt database ID mapping

import requests
from bs4 import BeautifulSoup
import re
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

gen = ['P05067','P05050']
dbs = ['pdb','dip','intact']

for ecgn in gen:
	print(ecgn)
    for ecdb in dbs:
    	print(ecdb)
        url = "https://rest.uniprot.org/uniprotkb/stream?fields=accession%2Corganism_name%2Cxref_{}&format=tsv&query=%28%28accession%3A{}%29%29+AND+%28reviewed%3Atrue%29" .format(ecdb,ecgn)
        print (url)
