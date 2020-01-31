from django.shortcuts import render
from django.http import HttpResponse

from django.http import JsonResponse

from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
import io

from .models import Incident
from .serializers import IncidentSerializer
from django.views.decorators.csrf import csrf_exempt

def index(request):
    # This is a view
    return HttpResponse("Your are on the main page: isn't it beautiful ?")

@csrf_exempt
def i_want_a_list(request):
    if request.method == "GET":
        incidents = Incident.objects.all()
        serializer = IncidentSerializer(incidents, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        content = JSONParser().parse(request)
        serializer = IncidentSerializer(data = content)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def incident_detail(request, incident_id):
    try:
        incident = Incident.objects.get(pk=incident_id)
    except Incident.DoesNotExist:
        return HttpResponse(str(incident_id), status=404)
    if request.method == "GET":
        serializer = IncidentSerializer(incident)
        return JsonResponse(serializer.data)
    elif request.method == "PUT":
        # je recup le content du request et parse en JSON
        content = JSONParser().parse(request)
        # je serialise le JSON en instance de House
        serializer = IncidentSerializer(incident) # , data = content)
        #if serializer.is_valid():
        #    serializer.save()
        #    return JsonResponse(serializer.data, status=201)

        #return JsonResponse(serializer.errors, status=400)
        serializer.update(incident, content)

        return JsonResponse(serializer.data, status=201)
    elif request.method == "DELETE":
        incident.delete()
        return HttpResponse("Suppression faite!", status=204)

def predict_time(unscaled_data):
    from sklearn.externals import joblib
    colonnes        = ["active", "incident_state", "resolved_at", "opened_at", "number", "sys_mod_count",
                        "u_priority_confirmation"]
    path_to_model   = "./ipynb/algorithme.sav"
    path_for_scaler = "./ipynb/scaler.sav"
    unscaled_data   = [unscaled_data[colonne] for colonne in colonnes]
    model           = joblib.load(path_to_model)
    scaler          = joblib.load(path_for_scaler)
    donnees_scalees = scaler.transform([unscaled_data])
    medv            = model.predict(donnees_scalees)
    return medv

@csrf_exempt
def predict(request):
    """
    Renvoie une house avec la MEDV completee
    (Attend une MEDV innexistante == null)
    """
    if request.method == 'GET':
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'POST':
        data        = JSONParser().parse(request)
        serializer  = IncidentSerializer(data=data)
        if serializer.is_valid():
            data["duree"]        = predict_time(data)
            serializer          = IncidentSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data  , status=201)
        return     JsonResponse(serializer.errors, status=400)
