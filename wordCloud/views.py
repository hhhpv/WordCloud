# Serve API Requests
# Hithesh


from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from .generator import *


@csrf_exempt
def index(request):

    with open("cloud-settings.txt", "r") as ifile:
        sttngs = json.load(ifile)
        if sttngs["loaded"] == "False":
            cloud = CreateMappings()
            with open("mappings.txt", "w+") as ofile:
                json.dump(cloud.mappings, ofile)
            sttngs["loaded"] = "True"
            with open("cloud-settings.txt", "w") as change:
                json.dump(sttngs, change)
    return render(request, "index.html", None)


@csrf_exempt
def generate(request):

    data = json.load(request.body)
    print(request.body)
    mappings = None
    with open("mappings.txt", "r") as rfile:
        mappings = json.load(rfile)
    cloud = Generator(mappings)
    result = cloud.process(
        data["range"], data["genre"], data["query_type"], data["num_words"]
    )
    return HttpResponse(json.dumps({"data": result}))
