from Tracker.models import RequestLogs
class RequestLogging:
    def __init__(self,get_response) -> None:
        self.get_response = get_response
    def __call__(self,request):
        request_info=(request)
        RequestLogs.objects.create(
            request_info=vars(request_info),
            request_type=request_info.method,
            request_method=request_info.path
        )

        print(self.get_response(request))

        return self.get_response(request)