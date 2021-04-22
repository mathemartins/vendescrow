import json

from django.http import JsonResponse

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from rest_framework import status

from posts.models import Post


class PostDetailViewController(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PostDetailViewController, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        instance = Post.objects.get(image=data.get('imageUrl'))
        payload = {
            "url": instance.get_api_url(),
            "id": instance.id,
            "title": instance.title,
            "slug": instance.slug,
            "content": instance.content,
            "html": instance.get_markdown(),
            "publish": instance.publish,
            "image": instance.image
        }
        return JsonResponse(status=status.HTTP_200_OK, data=payload)
