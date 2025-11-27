from django import forms
from .models import Media

class MediaForm(forms.ModelForm):
    MEDIA_TYPE_CHOICES = [
        ('photo', 'Photo'),
        ('video', 'Video'),
    ]
    
    media_type = forms.ChoiceField(
        choices=MEDIA_TYPE_CHOICES,
        initial='photo',
        widget=forms.RadioSelect
    )
    
    class Meta:
        model = Media
        fields = ['media_type', 'title', 'description', 'file']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].required = False
        self.fields['description'].required = False
        
    def clean_file(self):
        file = self.cleaned_data.get('file')
        media_type = self.cleaned_data.get('media_type')
        
        if not file:
            raise forms.ValidationError("Please select a file to upload.")
        
        if media_type == 'photo':
            valid_extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp']
            file_extension = file.name.split('.')[-1].lower()
            if file_extension not in valid_extensions:
                raise forms.ValidationError(
                    f"Unsupported image format. Supported formats: {', '.join(valid_extensions)}"
                )
                
        elif media_type == 'video':
            valid_extensions = ['mp4', 'mov', 'avi', 'wmv', 'flv', 'webm']
            file_extension = file.name.split('.')[-1].lower()
            if file_extension not in valid_extensions:
                raise forms.ValidationError(
                    f"Unsupported video format. Supported formats: {', '.join(valid_extensions)}"
                )
        
        return file
