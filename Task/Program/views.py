import json

from django.db import transaction
from django.shortcuts import render
import requests
# Create your views here.
from math import sin,cos, sqrt,atan2, radians
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from Task.Program.models import ModelQ, ModelQQ
from Task.Program.serializer import SerializerQ


class View(viewsets.ModelViewSet):
    queryset = ModelQ.objects.all()
    serializer_class = SerializerQ

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_403_FORBIDDEN)


    def list(self, request, *args, **kwargs):
        # 55.7545512,37.6172572 STATE HISTORICAL MUSEUM, THE CENTER OF MKAD
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    @action(methods=["get"],detail=False)
    def address(self,request,*args,**kwargs):
        query = ModelQQ.objects.all()
        #19.1 KM from Zarechye, Oblast Moskwa, Rusia
        outside_mkad = 0.1715774
        # set Center of MKAD is State Historical Museum, Red Square, 1, Moscow, Rusia
        latitude_of_center_mkad,longtitude_of_center_mkad= 37.6227195,55.7374375
        #R Earth
        R = 6373
        poup = 0
        pouprespon = 0
        yan = "https://geocode-maps.yandex.ru/1.x/?apikey=cbdb11a2-ffdd-4bb1-b8af-55e1dd8014c6&geocode={}&format=json&lang=en_us".format(kwargs["address"])
        yandex = requests.get(yan)
        #for create
        dataQ={
            "request_address":yandex.json()["response"]["GeoObjectCollection"]["metaDataProperty"]["GeocoderResponseMetaData"]["request"],
            "array_address":[]
        }
        # for response
        dataresponse=[

        ]
        for x in yandex.json()["response"]["GeoObjectCollection"]["featureMember"]:
            dataresponse.append({})
            #if len > 0 its mean the data from yandex is already in database and no need to create anymore
            if len(query.filter(name_address=x["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["text"]))>0:
                print(len(query.filter(name_address=x["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["text"])))
                tt=query.filter(name_address=x["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["text"]).first()
                dataresponse[pouprespon]["name_address"] = tt.name_address
                dataresponse[pouprespon]["latitude_coordinate_x"] = tt.latitude_coordinate_x
                dataresponse[pouprespon]["longtitude_coordinate_y"] = tt.longtitude_coordinate_y
                dataresponse[pouprespon]["distance_to_MKAD"] = tt.distance_to_MKAD
            else:
                dataQ["array_address"].append({})
                # if query.get(name_address = x["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["text"])
                dataQ["array_address"][poup]["name_address"] = x["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["text"]
                dataQ["array_address"][poup]["latitude_coordinate_x"],dataQ["array_address"][poup]["longtitude_coordinate_y"] = x["GeoObject"]["Point"]["pos"].split(" ")
                dataQ["array_address"][poup]["latitude_coordinate_x"], dataQ["array_address"][poup]["longtitude_coordinate_y"] = float(dataQ["array_address"][poup]["latitude_coordinate_x"]),float(dataQ["array_address"][poup]["longtitude_coordinate_y"])
                # define outside of MKAD or inside of MKAD
                if dataQ["array_address"][poup]["latitude_coordinate_x"] > (latitude_of_center_mkad + outside_mkad) or dataQ["array_address"][poup]["latitude_coordinate_x"] < (latitude_of_center_mkad - outside_mkad) or dataQ["array_address"][poup]["longtitude_coordinate_y"] < (longtitude_of_center_mkad - outside_mkad) or dataQ["array_address"][poup]["longtitude_coordinate_y"] > (longtitude_of_center_mkad + outside_mkad):

                    lat1 = radians(dataQ["array_address"][poup]["latitude_coordinate_x"])
                    lon1 = radians(dataQ["array_address"][poup]["longtitude_coordinate_y"])
                    lat2 = radians(latitude_of_center_mkad)
                    lon2 = radians(longtitude_of_center_mkad)

                    dlon = lon2 - lon1
                    dlat = lat2 - lat1

                    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
                    c = 2 * atan2(sqrt(a), sqrt(1 - a))

                    distance = R * c
                    dataQ["array_address"][poup]["distance_to_MKAD"] = str("%.2f"%distance)+ " Km"
                else:
                    dataQ["array_address"][poup]["distance_to_MKAD"] = "inside MKAD"
                dataresponse[pouprespon]["name_address"] = x["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["text"]
                dataresponse[pouprespon]["latitude_coordinate_x"] = dataQ["array_address"][poup]["latitude_coordinate_x"]
                dataresponse[pouprespon]["longtitude_coordinate_y"] = dataQ["array_address"][poup]["longtitude_coordinate_y"]
                dataresponse[pouprespon]["distance_to_MKAD"] = dataQ["array_address"][poup]["distance_to_MKAD"]
                poup = poup + 1
            pouprespon = pouprespon + 1
        print("done")
        serializer = self.get_serializer(data=dataQ)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(dataresponse, status=status.HTTP_201_CREATED, headers=headers)
        # try:
        #     # print(yandex.json()["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"])
        #     print(yandex.json()["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["text"])
        #     # print(yandex.json()["response"]["GeoObjectCollection"]["featureMember"][1]["GeoObject"]["metaDataProperty"])
        #     # print(yandex.json()["response"]["GeoObjectCollection"]["featureMember"][1]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"])
        #
        # except Exception as e:
        #     print(str(e))
        #     pass
        # print(yandex.json()["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"])
        # return Response(kwargs,status.HTTP_200_OK)
