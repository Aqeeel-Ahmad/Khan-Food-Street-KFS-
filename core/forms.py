from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-[#121212] border border-amber-500/30 rounded-xl text-white focus:outline-none focus:border-amber-400 placeholder-gray-500 transition-all',
                'placeholder': 'Your Full Name'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-[#121212] border border-amber-500/30 rounded-xl text-white focus:outline-none focus:border-amber-400 placeholder-gray-500 transition-all',
                'placeholder': '03XX XXXXXXX / +92 ...'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-[#121212] border border-amber-500/30 rounded-xl text-white focus:outline-none focus:border-amber-400 placeholder-gray-500 transition-all',
                'placeholder': 'Subject (e.g. Table Booking, Party Order, Feedback)'
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 bg-[#121212] border border-amber-500/30 rounded-xl text-white focus:outline-none focus:border-amber-400 placeholder-gray-500 transition-all h-32 resize-none',
                'placeholder': 'Tell us how we can serve you better...'
            }),
        }
