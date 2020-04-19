from django.shortcuts import render
from .models import candidates
import mockAadharServer3 
from app2 import RSAcode2 as rs
from django.core.mail import send_mail
from app.forms import Aadhaarverify,regForm,candidateVote
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import requests,json

# Create your views here.

def home(request):
	return render(request,'welcome_page.html')

def verify(request):
	global flag
	global s
	global zc
	global args
	global ca
	args=dict()
	zc=0
	ca = None
	s=""
	flag=0
	
	if request.method == 'POST':
		form = Aadhaarverify(request.POST)
		if form.is_valid():
			text = form.cleaned_data['aadhaar_no']
			args = {'form': form, 'text':text}
			url = 'http://127.0.0.1:5000/returnSign/' + text
			r1 = requests.get(url)
			d1,x,y = json.loads(r1.text)

			if len(d1)!=0:
				url1 = 'http://127.0.0.1:5000/esign/' + text
				r1 = requests.get(url1)
				d = json.loads(r1.text)
				zc = d['Zipcode']
				s = 'Aadhaar Number:' + str(d['Aadhaar Number']) + '\n' + 'Name:' + str(d['Name']) + '\n' + 'Date of Birth:' + str(d['Date of Birth']) + '\n' + 'Address:' + str(d['Address']) + '\n' + 'Zipcode:'+str(d['Zipcode'])
				flag=1
				ca = candidates.objects.filter(zipcode=zc)
				args = {'ca':ca}
			

	else:
		form = Aadhaarverify() 
	return render(request,'verify.html',{'form':form,'flag':flag,'s':s,'zc':zc,'ca':ca})


def generateKeys(request):
	global flag
	flag=0
	if request.method == 'POST':
		form = regForm(request.POST)
		if form.is_valid():

			text = form.cleaned_data['email']
			args = {'form': form, 'text':text}
			ob = rs.RSA()
			pr,pu = ob.gen_key_pair()  
			pem1 = pu.public_bytes(
				encoding=serialization.Encoding.PEM,
				format=serialization.PublicFormat.SubjectPublicKeyInfo
			)

			pem2 = pr.private_bytes(
			   encoding=serialization.Encoding.PEM,
			   format=serialization.PrivateFormat.PKCS8,
			   encryption_algorithm=serialization.NoEncryption()
			)
			pub = str("Your Public Key:" + str(pem1)) # remove this
			priv = str("Your Private Key:" + str(pem2))
			flag=1
			s = pub + '\n' + priv
			send_mail(
			'Keys',
			s,
			'kapilrathod1234@gmail.com',
			[text],
			fail_silently=False,
			)	
	else:
		form = regForm() 
	return render(request,'generateKeys.html',{'form':form,'flag':flag})

def generate2(request):
	return render(request,'generate2.html')

def vote(request):
	if request.method == 'POST':
		form = candidateVote(request.POST)
		if form.is_valid():
			cname = form.cleaned_data['candidate_name']
	else:
		form = candidateVote()

	return render(request,'vote.html',{'form':form,'ca':ca})

def final(request):
	return render(request,'final.html')




