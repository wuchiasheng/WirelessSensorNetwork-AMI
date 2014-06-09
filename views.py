from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from ami.models import Sensorparser
from ami.serializers import sensorSerializer

class JSONResponse(HttpResponse):
    """
        An HttpResponse that renders its content into JSON.
        """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def snippet_list(request):
    """
        List all code snippets, or create a new snippet.
        """
    if request.method == 'GET':
        sensor = Sensorparser.objects.all()
        serializer = sensorSerializer(sensor, many=True)
        return JSONResponse(serializer.data)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        sensor = sensorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

@csrf_exempt
def snippet_detail(request, pk):
    """
        Retrieve, update or delete a code snippet.
        """
    try:
        sensor = Sensorparser.objects.get(pk=pk)
    except Sensorparser.DoesNotExist:
        return HttpResponse(status=404)
    
    if request.method == 'GET':
        serializer = sensorSerializer(sensor)
        return JSONResponse(serializer.data)
    
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = sensorSerializer(sensor, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)
    
    elif request.method == 'DELETE':
        sensor.delete()
        return HttpResponse(status=204)