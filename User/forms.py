from django import forms

class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length = 50, label = 'Ad Soyad') 
    username = forms.CharField(max_length = 50, label = 'Kullanıcı Adı')
    email = forms.EmailField(label = 'E-posta Adresiniz ')
    password = forms.CharField(max_length = 20, widget = forms.PasswordInput, label = 'Parola Belirleyiniz')
    confirm = forms.CharField(max_length = 20, widget = forms.PasswordInput, label = 'Parolayı Doğrulayınız')

    def clean(self):
        first_name = self.cleaned_data.get('first_name')
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        confirm = self.cleaned_data.get('confirm')

        if first_name and username and password and confirm and password != confirm:
            raise forms.ValidationError('Parolalar Uyuşmuyor')

        else:
            values = {
                'first_name' : first_name,
                'username' : username,
                'email' : email,
                'password' : password
            }
            return values    

class LoginForm(forms.Form):
    username = forms.CharField(max_length = 50, label = 'Kullanıcı Adı')
    password = forms.CharField(max_length = 20, widget = forms.PasswordInput, label = 'Parola')

    

    