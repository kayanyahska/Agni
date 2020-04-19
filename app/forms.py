from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User

class regForm(forms.Form):
	email = forms.EmailField(label='E-mail:',max_length=300, help_text='Required. Inform a valid email address.')
	
class Aadhaarverify(forms.Form):
	aadhaar_no = forms.CharField(label='UIDAI Number:',max_length=30, required=True)

class candidateVote(forms.Form):
	candidate_name = forms.CharField(label='Enter Candidate Name from the List Below:',max_length=50, required=True)
	Enterprivatekey = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":40}),
	required=True)
	


	
	
	


	





	
	



