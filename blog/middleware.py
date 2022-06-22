def ua_middleware(get_response):
    def middleware(request):
        request.COOKIES['django_language'] = 'uk-UA'
        response = get_response(request)

        return response

    return middleware
