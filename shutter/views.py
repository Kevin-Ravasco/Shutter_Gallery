from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages

from .models import Album, Photo, Profile
from .forms import CreateProfileForm, ContactForm, AddAlbumForm, AddPhotoForm


@login_required
def home(request):
    albums = Album.objects.filter(created_by=request.user).order_by('-date_created')
    form = AddAlbumForm()
    if request.method == 'POST':
        form = AddAlbumForm(request.POST)
        if form.is_valid():
            album_name = form.cleaned_data['album']
            album = Album.objects.create(name=album_name, created_by=request.user)
            redirect_url = reverse('photos', args=[album.id])
            return HttpResponseRedirect(redirect_url)

    context = {'albums': albums, 'form': form, }
    return render(request, 'shutter/index.html', context)


@login_required
def photos(request, id):
    album = get_object_or_404(Album, id=id)
    images = Photo.objects.filter(album=album).order_by('-date_created')
    form = AddPhotoForm()
    album_form = AddAlbumForm()
    if request.method == 'POST':
        form = AddPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            photo = Photo.objects.create(album=album, image=image)
            data = {'is_valid': True, 'url': photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)
        return HttpResponseRedirect(reverse('photos'))
    context = {'photos': images, 'album': album, 'album_form':  album_form, }
    return render(request, 'shutter/single.html', context)


@login_required
def profile(request):
    photos = Photo.objects.filter(album__created_by=request.user).order_by('-date_created')[:6]
    profile = request.user.profile
    form = CreateProfileForm(instance=profile)
    if request.method == 'POST':
        form = CreateProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone = form.cleaned_data['phone']
            image = form.cleaned_data['image']

            user_profile, created = Profile.objects.update_or_create(user=request.user,
                                                                     defaults=dict(first_name=first_name,
                                                                                   last_name=last_name,
                                                                                   phone=phone, image=image))

            # messages.success(request, 'Profile details updated.')
            return HttpResponseRedirect(reverse('profile'))

    context = {'photos': photos, 'form': form}
    return render(request, 'shutter/profile.html', context)


@login_required
def delete_album(request, id):
    album = get_object_or_404(Album, id=id)
    if request.method == 'POST':
        Photo.objects.filter(album=album).delete()
        album.delete()
        return HttpResponseRedirect(reverse('home'))


@login_required
def delete_album_page(request, id):
    album = get_object_or_404(Album, id=id)
    context = {'album': album, }
    return render(request, 'shutter/delete_album.html', context)


@login_required
def update_album(request, id):
    album = Album.objects.get(id=id)
    form = AddAlbumForm()
    if request.method == 'POST':
        form = AddAlbumForm(request.POST)
        if form.is_valid():
            album_name = form.cleaned_data['album']
            album.name = album_name
            album.save()
            # Album.objects.filter(id=id).update(name=album_name)
            redirect_url = reverse('photos', args=[album.id])
            return HttpResponseRedirect(redirect_url)


@login_required
def contact(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            message_sent = [first_name + ' ' + last_name + '\n ' + message]

            send_mail(subject, message_sent, email, [''])
            messages.success(request, 'Message sent successfully!')
            return redirect(reverse('contact'))

    context = {'form': form, }
    return render(request, 'shutter/contact.html', context)
