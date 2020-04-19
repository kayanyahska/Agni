from flask import Flask
import RSAcode2
from cryptography.hazmat.primitives import serialization
import random
import hashlib
app = Flask(__name__)



@app.route('/returnSign/<int:aadhaar_no>',methods={'GET','POST'})

def returnSign(aadhaar_no):
	obj = RSAcode2.RSA()
	priv,pub = obj.gen_key_pair()
	global pem 
	pem = pub.public_bytes(
	encoding=serialization.Encoding.PEM,
	format=serialization.PublicFormat.SubjectPublicKeyInfo)
	global sig
	sig = obj.sign(bytes(aadhaar_no),priv)
	global auth
	auth = {'Aadhaar Number':aadhaar_no,'Public Key': str(pem),'Signature': str(sig)}
	return auth

def returnHash(aadhaar_no):
	obj = hashlib.sha256(str(aadhaar_no).encode())
	signature = auth['Signature']
	return obj,signature

@app.route('/esign/<int:aadhaar_no>',methods={'GET','POST'})
def esign(aadhaar_no):

	names = ['Kapil','Pruthvi','Akshay']
	dob = ['29-01-1999','05-03-1999','23-07-1999']
	add = ['Mumbai','Mysore','Jaipur']
	zipcodes = ['400088','500023','445611']
	d = dict(returnSign(aadhaar_no))
	ano = d['Aadhaar Number']
	r = random.randint(0,2)
	s = names[r]+dob[r]+add[r]+zipcodes[r]+d['Signature']
	s =s.encode('utf-8')
	
	return {'Aadhaar Number': ano, "Name": names[r],"Date of Birth":dob[r],"Address": add[r],"Zipcode":zipcodes[r]
	,"Public Key": str(pem) ,"Sign": str(sig)}


	
if __name__ == '__main__':
	app.run(debug=True)


