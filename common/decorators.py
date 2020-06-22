from django.http import HttpResponseBadRequest

def ajax_required(f):
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return f(request, *args, **kwargs)
    wrap.__doc__=f.__doc__
    wrap.__name__=f.__name__
    return wrap


# imaportance of custom decorators is 
# avoid the same check in multiple views 
# in this example instead of using is_ajax() method multiple times
# we use a decorator
