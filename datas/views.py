from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from datas.models import Data

from datas.serializers import DataSerializer
from devices.models import Device
from iotdashboard.debug import debug


def ip_address(request):
    """
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip


def datalist(request):
    datas = Data.objects.all()
    return render(request, 'back/data_list.html', locals())


class DataList(APIView):
    """
    List all datas, or create a new data.
    """

    def get(self, request, format=None):
        if 'last' in request.GET:
            datas = Data.objects.all()[:1]
        elif 'result' in request.GET:
            datas = Data.objects.all()[:int(request.GET['result'])]
        else:
            datas = Data.objects.all()

        serializer = DataSerializer(datas, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        try:
            api_key = request.data['api_key']
            device = get_object_or_404(Device, api_key=api_key, enable=True)
            request.data['device'] = device.pk
            request.data['remote_address'] = ip_address(request)
            serializer = DataSerializer(data=request.data)
            debug(serializer)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            msg_err = {'err': 'API KEY not found!'}
            return Response(msg_err, status=status.HTTP_400_BAD_REQUEST)


class DataDetail(APIView):
    """
    Retrieve, update or delete a datas instance.
    """

    def get_object(self, pk):
        try:
            return Data.objects.get(pk=pk)
        except Data.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        datas = self.get_object(pk)
        serializer = DataSerializer(datas)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        datas = self.get_object(pk)
        serializer = DataSerializer(datas, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        datas = self.get_object(pk)
        datas.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def data_chart(request, id):
    device = Device.objects.get(pk=id)
    datas = Data.objects.filter(device=device)
    return render(request, 'back/data_chart.html', locals())


def data_chart_ajax(request, id):
    device = Device.objects.get(pk=id)
    datas = Data.objects.filter(device=device)[:10]

    labels = []
    data = []

    for entry in datas:
        labels.append(entry.pub_date)
        data.append(entry.field_1)

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })
