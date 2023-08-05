from .models import Population,Family
from django.utils import timezone


def getnewidp(id_suku):
    result = Population.objects.last()
    newid = 0 
    if result:
	    newid = result.id + 1
    else:
	    newid = 1
    id = str(id_suku)+str(newid) 
    return id

def createnewid(id_suku):
    newid = timezone.now().strftime("%y%m%d")
    id = str(id_suku)+str(newid)
    return id



def getnewidf():
    result = Family.objects.last()
    newid = 0 
    if result:
	    newid = result.id + 1
    else:
	    newid = 1
    id = newid
    return id


def getfulan():

    getfulan = [
        {"fulan" :"Janeiru","id" : "1"},
        {"fulan" : "Fevereiru","id" : "2"},
        {"fulan" : "Marsu","id" : "3"},
        {"fulan" : "Abril","id" : "4"},
        {"fulan" : "Maio","id" : "5"},
        {"fulan" : "Junhu","id" : "6"},
        {"fulan" : "Julhu","id" : "7"},
        {"fulan" : "Agostu","id" : "8"},
        {"fulan" : "Setembru","id" : "9"},
        {"fulan" : "Outubru","id" : "10"},
        {"fulan" : "Novembru","id" : "11"},
        {"fulan" : "Dezembru","id" : "12"},
        ]
    return getfulan