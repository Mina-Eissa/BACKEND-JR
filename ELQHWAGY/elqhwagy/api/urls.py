from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CRUDUser,
    CRUDProduct,
    CRUDOrder,
    CRUDClient,
    FilterClientByDate
)
"""
urls for Router of CRUD operations 
| Method | Endpoint                       | Description              |
| ------ | ------------------------------ | ------------------------ |
| GET    | `/api/{basename}/`             | List all {basename}      |
| POST   | `/api/{basename}/`             | Create a new {basename}  |
| GET    | `/api/{basename}/{id}/`        | Retrieve a {basename}    |
| PUT    | `/api/{basename}/{id}/`        | Update a {basename}      |
| PATCH  | `/api/{basename}/{id}/`        | Partial update           |
| DELETE | `/api/{basename}/{id}/`        | Delete a {basename}      |
"""
CRUDUserRouter = DefaultRouter()
CRUDUserRouter.register(r'employee', CRUDUser, basename='employee')

CRUDProductRouter = DefaultRouter()
CRUDProductRouter.register(r'product', CRUDProduct, basename='product')

CRUDOrderRouter = DefaultRouter()
CRUDOrderRouter.register(r'order', CRUDOrder, basename='order')

CRUDClientRouter = DefaultRouter()
CRUDClientRouter.register(r'client', CRUDClient, basename='client')

urlpatterns = [
    path('', include(CRUDUserRouter.urls)),
    path('', include(CRUDProductRouter.urls)),
    path('', include(CRUDOrderRouter.urls)),
    path('FilterClientByDate/<str:start>/<str:end>/',FilterClientByDate,name='FilterClientByDate')
]
