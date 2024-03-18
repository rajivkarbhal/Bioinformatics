import requests
from bs4 import BeautifulSoup
import re
import sys
import io
import time
import subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')


class ens:
    def __init__(self,url):
        self.url = url

    def add(self):
        try:
            ensurl = self.url
            response = requests.get(ensurl)
            cot = response.text
            blocks = response.text.split("version: 0")
            for item in enumerate(blocks):                  
                if (pnm := re.match(r".+dbname: EntrezGene", str(item), re.IGNORECASE)):
                        #print (pnm)                                
                    if (idm := re.match(r".+primary_id: (\S+)", str(item), re.IGNORECASE)):
                            #print (idm)
                        gid = idm.group(1)
                        gid = gid.replace("\\n", "" )
                        return (gid)                                        
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

url = "https://rest.ensembl.org/xrefs/id/ENSG00000139618?"
response = requests.get(url)
blocks = response.text.split("\n")
db = ""
for item in enumerate(blocks):
    if (err := re.match(r".+dbname: (EntrezGene).+", str(item), re.IGNORECASE)):
        db = err.group(1)
if db:
    geneid = ens(url)
    gid=geneid.add()
    print (gid)
else:
    print("Please check accession number")

gnnumbvalue = locals().get('gid') #To avoid printing 'NameError' error


NCBI_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=gene&id=%s"%gid
gnnm = ncbi(NCBI_url)
ndata=gnnm.ncbidata()
#print (ndata)
rj = ndata.split("_")
symbol = rj[0]
synnm = rj[1]
unp = rj[2]
print (unp)
#$curl = "curl --request POST https://rest.uniprot.org/idmapping/run --form ids=P05067 --form from=UniProtKB_AC-ID --form to=$crossdb";

output = subprocess.run("curl --request POST https://rest.uniprot.org/idmapping/run --form ids=P05067 --form from=UniProtKB_AC-ID --form to=DIP", shell=True, capture_output=True, text=True)
idmap = output.stdout
time.sleep(10)
if (jobidchk := re.match(r"\{\"jobId\"\:\"(\S+)\"\}", idmap, re.IGNORECASE)):
    jid = jobidchk.group(1)
    reslink = "https://rest.uniprot.org/idmapping/stream/%s?format=tsv"%jid
    #url = "https://rest.ensembl.org/xrefs/id/ENSG00000139618?"
    unpresponse = requests.get(reslink)
    print (unpresponse.text)