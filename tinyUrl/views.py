import json
from typing import Optional

from django.db.models import F
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from tinyUrl.models import TinyUrl


@csrf_exempt
def create(request):
    # check if request method is POST
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method, only POST is allowed'}, status=405)
    # check if request body is provided
    if not request.body:
        return JsonResponse({'error': 'Request body must be provided'}, status=400)
    # check if request content type is JSON
    if request.content_type != 'application/json':
        return JsonResponse({'error': 'Invalid Content-Type, only application/json is allowed'}, status=415)
    # check if request body is valid JSON
    try:
        data: dict = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    # check if url is provided correctly
    long_url = data.get('url')
    if not long_url:
        return JsonResponse({'error': 'URL not provided'}, status=400)
    if not isinstance(long_url, str):
        return JsonResponse({'error': 'URL must be a string'}, status=400)
    # check if url is existing in database
    tiny_url = TinyUrl.objects.filter(full_url=long_url).first()
    if tiny_url:
        return JsonResponse({'short_url': tiny_url.short_url}, status=200)
    # create short url and save to database
    tiny_url = TinyUrl.objects.create(full_url=long_url)
    return JsonResponse({'short_url': tiny_url.short_url}, status=201)


def redirect(request, short_url: Optional[str] = None):
    # check if request method is GET
    if request.method != 'GET':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    # check if short url is provided
    if not short_url:
        return JsonResponse({'error': 'Short URL not provided'}, status=404)
    if len(short_url) != 7:
        return JsonResponse({'error': 'Invalid short URL'}, status=404)
    # check if short url is existing in database
    if not TinyUrl.objects.filter(short_url=short_url).exists():
        return JsonResponse({'error': 'Short URL not found'}, status=404)

    # get full url and update hit count
    url = TinyUrl.objects.get(short_url=short_url)
    TinyUrl.objects.filter(short_url=short_url).update(hit_count=F('hit_count') + 1)
    # redirect to full url
    return HttpResponseRedirect(url.full_url)


def error_404(request, exception=None):
    return JsonResponse({'error': 'ERROR 404: page not found'}, status=404)
