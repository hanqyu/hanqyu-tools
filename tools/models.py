import face_recognition  # https://github.com/ageitgey/face_recognition
from PIL import Image
from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage


def download_image(file_dir):
    import os
    from django.http import HttpResponse

    if os.path.exists(file_dir):
        with open(file_dir, 'rb') as fh:

            response = HttpResponse(fh.read(), content_type='image/png')
            response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(file_dir)
            return response
    raise Http404


class Photo(models.Model):
    name = models.CharField(max_length=100)

    def __init__(self, url):
        self.source_url = url
        self._get_file_name()
        self.image_path = self._file_dir()
        self.file_dir = settings.MEDIA_ROOT + '/' + self.image_path

    def _get_file_name(self, file_name='image'):
        self.file_name = file_name

    def _file_dir(self):
        import os
        path = settings.MEDIA_ROOT + '/' + self.file_name + '.png'
        i = 1
        while os.path.exists(path):
            path = settings.MEDIA_ROOT + '/' + self.file_name + str(i) + '.png'
            i += 1
        return self.file_name + str(i) + '.png'

    def make_profile_img(self):
        image_object = self.img_object_from_url()
        original_image_size = Image.open(image_object).size

        # Load the jpg file into a numpy array
        image = face_recognition.load_image_file(image_object)

        # Find all the faces in the image using the default HOG-based model.
        # This method is fairly accurate, but not as accurate as the CNN model and not GPU accelerated.
        # See also: find_faces_in_picture_cnn.py
        face_locations = face_recognition.face_locations(image)

        # print("I found {} face(s) in this photograph.".format(len(face_locations)))

        for face_location in face_locations:

            # Print the location of each face in this image
            top, right, bottom, left = face_location
            # print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))

            vertical, horizontal = [axis == min(original_image_size) for axis in original_image_size]

            if vertical:
                middle = (bottom - top) / 2 + top
                top, bottom = middle - min(original_image_size)/2, middle + min(original_image_size)/2
                left, right = 0, min(original_image_size)

            if horizontal:
                middle = (right - left) / 2 + left
                left, right = middle - min(original_image_size)/2, middle + min(original_image_size)/2
                top, bottom = 0, min(original_image_size)

            top, right, bottom, left = [int(x) for x in [top, right, bottom, left]]
            # You can access the actual face itself like this:
            face_image = image[top:bottom, left:right]
            pil_image = Image.fromarray(face_image)
            # return pil_image
            self.image = pil_image

    def save_image_to_local(self):
        self.image.save(self.file_dir, 'PNG')

        image_storage = FileSystemStorage(
            # Physical file location ROOT
            location=u'{0}'.format(settings.MEDIA_ROOT),
            # Url for file
            base_url=u'{0}'.format(settings.MEDIA_URL),
        )

        self.img_tmp = models.ImageField(upload_to=self.file_dir, storage=image_storage)
        return self.file_dir

    def img_object_from_url(self):
        import requests
        from io import BytesIO

        response = requests.get(self.source_url)
        img = BytesIO(response.content)

        return img
