from tkinter import *
import hashlib
from tkinter import ttk
from bs4 import BeautifulSoup
from PIL import ImageTk,Image
import requests, json
import mockAadharServer2
import smtplib 
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


def gen_key_pair():
    private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
    )
    public_key = private_key.public_key()
    return (private_key, public_key)

def onselect(evt):
    # Note here that Tkinter passes an event object to onselect()
    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    print('You selected item %d: "%s"' % (index, value))

    vote = value

    root1 = Tk()
    root1.geometry('2500x2500')
    display = Label(root1,text = "Welcome to SAFE VOTE ",bg='brown',fg='white',width=20,font=("bold",30))
    display.place(x=470,y=5)
    sentence = Label(root1,text = "You have voted for : " + str(vote),bg='brown',fg='white',width=50,font=("bold",20))
    sentence.place(x=470,y=200)

    enter_priv = Label(root1,text = "Enter Private key",bg='brown',fg='white',width=20,font=("bold",20))
    enter_priv.place(x=275,y= 350)

    ano = Entry(root1)
    ano.place(x=650,y=350,width=350,height=250)
    vote_now = Button(root1,text="Cast Vote", width=20,bg='white',fg='black',font=("bold"))
    vote_now.place(x=275,y=500)



def storeInAzure():
    hash_val,signature = mockAadharServer2.returnHash()
    s = str(hash_val) + str(signature)
    output = hashlib.sha256(s.encode())    

def gen():
    
    pr,pu = gen_key_pair()  
    pem1 = pu.public_bytes(
	encoding=serialization.Encoding.PEM,
	format=serialization.PublicFormat.SubjectPublicKeyInfo)

    pem2 = pr.private_bytes(
       encoding=serialization.Encoding.PEM,
       format=serialization.PrivateFormat.PKCS8,
       encryption_algorithm=serialization.NoEncryption()
    )
    pub = str("Your Public Key:" + str(pem1)) # remove this
    priv = str("Your Private Key:" + str(pem2))
    

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("kapilrathod1234@gmail.com", "aquarius29/1/19991234")

    msg = '\n'+ pub + '\n' + '\n' + priv
    server.sendmail("kapilrathod1234@gmail.com", "kapilrathod1234@gmail.com", msg)
    server.quit()
    stat=Label(root,bg='brown',fg='white',width=25,font=("bold",10),text="Your Keys are Mailed to You")
    stat.place(x=900 ,y=200)
   
def verify_Aadhaar():
    url = 'http://127.0.0.1:5000/returnSign/' + ano.get()
    r1 = requests.get(url)
    d1,x,y = json.loads(r1.text)
    fl=0
    if len(d1)==0 or d1 == None:
        vstatus = Label(root, width =20,font=("bold",10),text = 'Aadhaar Doesnt Exist')
    else:
        vstatus = Label(root, width =20,font=("bold",10),text = 'Aadhaar Verified')
        fl=1
    
    vstatus.place(x=300 ,y=300)
    if fl==1:
        url = 'http://127.0.0.1:5000/esign/' + ano.get()
        r = requests.get(url)
        d = json.loads(r.text)

        generate = Button(root,text="Generate Your Keys", width=25,bg='brown',fg='white',command=gen)
        generate.place(x= 630 ,y = 320)
        
        s = 'Your Aadhaar Details:' + '\n' + str(d['Aadhaar Number']) + '\n' + str(d['Name']) + '\n' + str(d['Date of Birth']) + '\n' + str(d['Address']) + '\n' + str(d['Zipcode'])
        details=Label(root,bg='brown',fg='white',width=20,font=("bold",10),text=s)
        details.place(x=400 ,y=650)

        zipc = d['Zipcode']
        url = 'http://127.0.0.1:8000/app/data'
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        st = soup.get_text()
        choices= []
        st = st.strip().split('\n')

        
        cand=Label(root,width=120,height=10,font=("bold",10),text='Candidates in your Constituency with Zipcode: '+zipc)
        cand.place(x=5 ,y=350)

        votefor = Label(root,width=100,font=("bold",10),text='Select the Candidate: you want to Vote for: ')
        votefor.place(x = 0, y=460)
        listbox = Listbox(root,selectmode=SINGLE)
        listbox.place(x=400,y=460)

        for i in st:
            listbox.insert(END,i)
        
        listbox.bind('<<ListboxSelect>>',onselect)
    
    else:
        details=Label(root,bg='brown',fg='white',width=20,font=("bold",10),text='Aadhaar Does Not Exist')
    
        
    
    
    
root = Tk()
root.geometry('2500x2500')

display = Label(root,text = "Welcome to SAFE VOTE ",bg='brown',fg='white',width=20,font=("bold",30))
display.place(x=470,y=5)

aadhaar_no = Label(root,text = "Enter your Aadhaar Number:",bg='brown',fg='white',width =25,font=("bold",20))
aadhaar_no.place(x = 170 ,y = 200)

ano = Entry(root)
ano.place(x=630,y=200)

verify = Button(root,text="Verify Aadhaar", width=20,bg='white',fg='black',font=("bold"),command = verify_Aadhaar)
verify.place(x = 630 ,y = 270)



root.mainloop()

