from os import system as sy
from time import sleep as slp
import sys
import hashlib
import itertools
import threading
def md5(hash,wd):
	try:
		open(wd,'r')
	except:
		raise FileNotFoundError('Wordlist Not found!')
		
		sy('clear')
		
	f=open(wd,'r')
	while True:
		rt=f.readline()
		rf=rt.replace('\n','').encode()
		rehash=hashlib.md5(rf).hexdigest()
		
		if hash==rehash:
			done = True
			print('[*] Hash Found : '+rf.decode()); break
		else:
			pass
		if len(rf)==0:
			print('[*] Hash not in wordlist!'); break
def sha256(hash,wd):
	try:
		open(wd,'r')
	except:
		raise FileNotFoundError('Wordlist Not found!')
		
		
	f=open(wd,'r')
	while True:
		rt=f.readline()
		rf=rt.replace('\n','').encode()
		rehash=hashlib.sha256(rf).hexdigest()
		print(rehash)
		if hash==rehash:
			done = True
			print('[*] Hash Found : '+rf.decode()); break
		else:
			pass
		if len(rf)==0:
			print('[*] Hash not in wordlist!'); break
def sha512(hash,wd):
	try:
		open(wd,'r')
	except:
		raise FileNotFoundError('Wordlist Not found!')
		
	
	f=open(wd,'r')
	while True:
		rt=f.readline()
		rf=rt.replace('\n','').encode()
		rehash=hashlib.sha512(rf).hexdigest()
		
		if hash==rehash:
			done = True
			print('[*] Hash Found : '+rf.decode()); break
		else:
			pass
		if len(rf)==0:
			print('[*] Hash not in wordlist!'); break
def sha3_256(hash,wd):
	try:
		open(wd,'r')
	except:
		raise FileNotFoundError('Wordlist Not found!')
		
	
	f=open(wd,'r')
	while True:
		rt=f.readline()
		rf=rt.replace('\n','').encode()
		rehash=hashlib.sha3_256(rf).hexdigest()
		
		if hash==rehash:
			done = True
			print('[*] Hash Found : '+rf.decode()); break
		else:
			pass
		if len(rf)==0:
			print('[*] Hash not in wordlist!'); break
def sha3_512(hash,wd):
	try:
		open(wd,'r')
	except:
		raise FileNotFoundError('Wordlist Not found!')
		
	
	f=open(wd,'r')
	while True:
		rt=f.readline()
		rf=rt.replace('\n','').encode()
		rehash=hashlib.sha3_512(rf).hexdigest()
		
		if hash==rehash:
			done = True
			print('[*] Hash Found : '+rf.decode()); break
		else:
			pass
		if len(rf)==0:
			print('[*] Hash not in wordlist!'); break
def blake2b(hash,wd):
	try:
		open(wd,'r')
	except:
		raise FileNotFoundError('Wordlist Not found!')
		
	
	f=open(wd,'r')
	while True:
		rt=f.readline()
		rf=rt.replace('\n','').encode()
		rehash=hashlib.blake2b(rf).hexdigest()
		
		if hash==rehash:
			done = True
			print('[*] Hash Found : '+rf.decode()); break
		else:
			pass
		if len(rf)==0:
			print('[*] Hash not in wordlist!'); break
def blake2s(hash,wd):
	try:
		open(wd,'r')
	except:
		raise FileNotFoundError('Wordlist Not found!')
	
	f=open(wd,'r')
	while True:
		rt=f.readline()
		rf=rt.replace('\n','').encode()
		rehash=hashlib.blake2s(rf).hexdigest(); print(rehash)
		if hash==rehash:
			done = True
			print('[*] Hash Found : '+rf.decode()); break
		else:
			pass
		if len(rf)==0:
			print('[*] Hash not in wordlist!'); break