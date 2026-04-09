from .models import Website

class CustomDomainMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().split(':')[0]
        
        # We process the request if the host is not a standard development address
        # but could be a custom domain mapped in the hosts file.
        if host not in ['127.0.0.1', 'localhost', '0.0.0.0'] and 'ngrok' not in host:
            try:
                website = Website.objects.get(custom_domain__iexact=host, published=True)
                
                # Under the hood, we rewrite the incoming request path so Django
                # routes it to the correct view, passing the username/slug!
                original_path = request.path_info
                
                if original_path == '/':
                    request.path_info = f'/sites/{website.user.username}/{website.slug}/'
                else:
                    # e.g., /contact/ -> /sites/username/slug/contact/
                    request.path_info = f'/sites/{website.user.username}/{website.slug}{original_path}'
                    
            except Website.DoesNotExist:
                pass
                
        return self.get_response(request)
