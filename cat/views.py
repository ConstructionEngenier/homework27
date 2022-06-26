import json

import pandas
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from cat.models import Category


class AddCatData(View):
    def get(self, request):
        data_cat = pandas.read_csv('/Users/artem/Artems documents/Python/lesson27/homework27/data/categories.csv',
                                   sep=',').to_dict()

        i = 0
        while max(data_cat['id'].keys()) > i:
            cat = Category.objects.create(
                name=data_cat["name"][i],
            )
            i += 1
        return JsonResponse("Data upload successful", safe=False, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class CategoryView(View):

    def get(self, request):
        categories = Category.objects.all()

        response = []
        for category in categories:
            response.append({
                "id": category.id,
                "name": category.name,
            })

        return JsonResponse(response, safe=False)

    def post(self, request):
        category_data = json.loads(request.body)

        category = Category.objects.create(
            name=category_data["name"]
        )
        return JsonResponse({
            "id": category.id,
            "name": category.name,
        }, safe=False)


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        category = self.get_object()

        return JsonResponse({
            "id": category.id,
            "name": category.name,
        })
