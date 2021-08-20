from django.utils.deprecation import MiddlewareMixin
import datetime


class RequestLogMiddleware(MiddlewareMixin):    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)    
    
    def process_request(self, request):
        if request.method in ['GET']:
            # request.req_body = request.body
            request.start_time = datetime.datetime.now()
            with open('middle.txt', 'a') as f:
                f.write(f'{request} {request.start_time} \n')





