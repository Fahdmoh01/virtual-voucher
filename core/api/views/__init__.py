from .events import *
from .auth import *
from .vouchers import *


class OverviewAPI(APIView):
    '''Gives overview of api - testing only'''

    def get(self, request, *args, **kwargs):
        return Response({
            "message": "Welcome to the API!",
            "description": "This is a REST API for the eVoucher App.",
        })
