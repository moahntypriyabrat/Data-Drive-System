from django import forms
from .models import File


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['name', 'file']


class FolderStructureForm(forms.Form):
    folder_structure = forms.CharField(label='Enter Folder Structure')


class FolderDeletionForm(forms.Form):
    folder_to_delete = forms.CharField(label='Folder to Delete')