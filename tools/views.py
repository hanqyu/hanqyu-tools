from django.shortcuts import render

# Create your views here.
from .forms import PostUrlForm
from .models import Photo
from .models import download_image


def show_photo(request):
    if request.method == 'POST':
        form = PostUrlForm(request.POST)
        if form.is_valid():
            url = request.POST.dict()['url']
            photo = Photo(url)
            photo.make_profile_img()
            photo.save_image_to_local()
            return render(request, 'tools/index.html', {'img_temp': photo.img_tmp})
    else:
        form = PostUrlForm()
        return render(request, 'tools/index.html', {'form': form})


def download(request):
    if 'download' in request.POST:
        form = PostUrlForm(request.POST)
        if form.is_valid():
            url = request.POST.dict()['url']
            photo = Photo(url)
            photo.make_profile_img()
            photo.save_image_to_local()
            return download_image(photo.file_dir)
            # img_json = {'image_file': settings.MEDIA_URL + photo.image_path}
            # return render(request, 'tools/index.html', {'image_path': photo.image_path})
    else:
        form = PostUrlForm()
        return render(request, 'tools/index.html', {'form': form})

