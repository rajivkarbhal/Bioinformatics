import time
import spacy
import requests
import re
from googletrans import Translator
nlp = spacy.load("en_core_web_sm")

testout = open("extracntr.txt","w",encoding='utf-8')
with open('spcctout.txt', 'r') as file:
	for line in file:
		cntst=""
		line = line.strip()
		testout.write("\n" + line + ", ")
		if (lnmt := re.match(r"(^.+):.+", str(line), re.IGNORECASE)):
			spnm = lnmt.group(1)
			spnm = spnm.strip()
			print (spnm)
			url = 'https://wikimonde.com/article/%s'%spnm
			headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
			response = requests.get(url,headers=headers)
			if response.status_code == 200:
				concatenated_text = ' '.join(response.text.split())
				if (mth := re.match(r".+Distribution\<\/span\>\<\/h2\>(.+)\<h2\>\<span id", str(concatenated_text), re.IGNORECASE)):
					cntst = mth.group(1)
					cntst = re.sub(r'<span class="cite_crochet">.+', '', cntst)        
					cntst = re.sub(r'<.*?>', '', cntst)
					cntst = cntst.lstrip()
					translator = Translator()
					transcntst = translator.translate(cntst, src='fr', dest='en')
					transcntst = transcntst.text
					doc = nlp(transcntst)
					countries = [ent.text for ent in doc.ents if ent.label_ == "GPE"]
					if countries:
						result = ', '.join(countries)
						testout.write(result)
					else:
						testout.write(str(doc))
						print("No countries found.")
			else:
				print(f"Failed to retrieve webpage. Status code: {response.status_code}")
