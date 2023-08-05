import zipfile

def start(zip,wd):
	try:
		zip_file=zipfile.ZipFile(zip)
	except:
		raise FileNotFoundError('Zip File Not Found!')
	try:
		word=open(wd,'r')
		pass_c=len(list(open(wd, "rb")))
	except:
		raise FileNotFoundError('Wordlist Not Found!')
	c=0
	while True:
		word_p=word.readline()
		word_p=word_p.strip()
		c=c+1
		if c-1==pass_c:
			print('\n[!] Password Not in Wordlist!')
			break
		try:
			zip_file.extractall(pwd=word_p.encode())
			print('[*] Password Found : '+word_p)
			break
		except:
			print('[*] Wrong Password : ',word_p)	