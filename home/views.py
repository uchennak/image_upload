from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from . import forms as home_forms, models as home_models


def get_shareable_link(request, picture):
    """Generate a shareable link for the picture using the current host."""
    scheme = 'https' if request.is_secure() else 'http'
    host = request.get_host()
    return f"{scheme}://{host}/picture/{picture.pk}/"


def upload_picture(request):
    if request.method == 'POST':
        form = home_forms.PictureForm(request.POST, request.FILES)
        if form.is_valid():
            picture = form.save()
            shareable_link = get_shareable_link(request, picture)
            return render(request, 'picture_detail.html', {
                'picture': picture,
                'shareable_link': shareable_link,
                'just_uploaded': True
            })
    else:
        form = home_forms.PictureForm()
    return render(request, 'upload_image.html', {'form': form})


def picture_detail(request, pk):
    try:
        picture = home_models.Picture.objects.get(pk=pk)
    except home_models.Picture.DoesNotExist:
        return redirect('upload_picture')
    if picture.is_expired():
        picture.delete()
        return redirect('upload_picture')
    shareable_link = get_shareable_link(request, picture)
    return render(request, 'picture_detail.html', {
        'picture': picture,
        'shareable_link': shareable_link
    })


def recently_uploaded(request):
    pictures = home_models.Picture.objects.order_by('-created_at')[:10]
    return render(request, 'upload_picture.html', {'pictures': pictures})


def delete_picture(request, pk):
    picture = get_object_or_404(home_models.Picture, pk=pk)

    if request.method == 'POST':
        form = home_forms.DeletePictureForm(request.POST)
        if form.is_valid():
            if picture.check_delete_password(form.cleaned_data['password']):
                picture.image.delete()
                picture.delete()
                messages.success(request, 'Image deleted successfully.')
                return redirect('upload_picture')
            else:
                messages.error(request, 'Incorrect password.')
    else:
        form = home_forms.DeletePictureForm()

    return render(request, 'delete_picture.html', {
        'picture': picture,
        'form': form
    })
