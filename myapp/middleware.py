from django.urls import reverse
from django.shortcuts import redirect
class RedirectAuthenticatedUserMiddleware:
    def __init__(self,get_response):  #get_response is a function is for to send the request to next middleware or if not,to the view
        self.get_response = get_response
    
    def __call__(self, request): #request --- this is request from the url which gets before goes to the view function
        #check if user is authenticated
        if request.user.is_authenticated:
            #Lists of paths to check
            paths_to_redirect = [reverse('members:login'),reverse('members:register')]

            if request.path in paths_to_redirect:
                return redirect(reverse('blog:index')) #change to homepage
        response=self.get_response(request)
        return response 
    
class RestrictUnauthenticatedUserMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
    
    def __call__(self, request):
        restricted_paths = [reverse('members:dashboard')]
        
        if not request.user.is_authenticated and request.path in restricted_paths:
            return redirect(reverse('members:login')) 
        
        response=self.get_response(request)
        return response 
