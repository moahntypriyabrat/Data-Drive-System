from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import File
from .forms import FileForm,FolderStructureForm,FolderDeletionForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import os
import shutil
from pathlib import Path
from django.conf import settings
from django.http import JsonResponse

@login_required
def create_folder(request):
    if request.method == 'POST':
        form = FolderStructureForm(request.POST)
        if form.is_valid():
            folder_structure = form.cleaned_data['folder_structure']
            base_directory = os.path.join(settings.MEDIA_ROOT,folder_structure)
            os.makedirs(base_directory, exist_ok=True)
            return HttpResponse(f'Nested folders created at {base_directory}')
    else:
        form = FolderStructureForm()
    return render(request, 'folder/create_folder.html', {'form': form})


def file_list(request):
    # folders = NewFolder.objects.filter(parent_folder=None)
    base_directory = os.path.join(settings.MEDIA_ROOT)
    print(base_directory)
    folders = []
    for root, dirs, files in os.walk(base_directory):
        for directory in dirs:
            folder_path = os.path.join(root, directory)
            relative_path = os.path.relpath(folder_path, base_directory)
            folders.append(relative_path)
    files = File.objects.all
    return render(request, 'folder/file_list.html',{'folders': folders, 'files': files})

@login_required
def create_file(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.owner = request.user
            file.save()
            messages.success(request, 'File uploaded successfully!')
            return redirect('file_list')

    else:
        form = FileForm()

    return render(request, 'folder/create_file.html', {'form': form})

@login_required
def delete_folder(request):
    if request.method == 'POST':
        form = FolderDeletionForm(request.POST)
        if form.is_valid():
            folder_to_delete = form.cleaned_data['folder_to_delete']
            base_directory = os.path.join(settings.MEDIA_ROOT)
            folder_path = os.path.join(base_directory, folder_to_delete)

            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)
                return HttpResponse(f'Folder "{folder_to_delete}" has been deleted.')
            else:
                return HttpResponse(f'Folder "{folder_to_delete}" does not exist.')
    else:
        form = FolderDeletionForm()

    return render(request, 'folder/delete_folder.html', {'form': form})


@login_required
def delete_file(request, file_id):
    file = get_object_or_404(File, id=file_id)

    if request.method == 'POST':
        file.delete()
        messages.success(request, 'File deleted successfully!')
        return redirect('file_list')

    return render(request, 'folder/delete_file.html', {'file': file})


