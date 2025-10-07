from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection, transaction
from django.db.models import (
    Avg,
    Count,
    DecimalField,
    ExpressionWrapper,
    F,
    Func,
    Max,
    Min,
    Q,
    Sum,
    Value,
)
from django.db.models.functions import Concat
from django.http import HttpResponse
from django.shortcuts import render

from store.models import Collection, Customer, Order, OrderItem, Product
from tags.models import Tag, TaggedItem


# @transaction.atomic() # treat function as transaction
def say_hello(request):

    return render(request, "hello.html", {"name": "moataz", "tags": []})
