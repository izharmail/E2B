from django import http
from django.urls import path

from app.src.connectors.api_domain.service_adapters import DomainServiceAdapter
from app.src.connectors.domain_storage.service_adapters import StorageServiceAdapter
from app.src.layers.api import models as api_models
from app.src.layers.api import views
from app.src.layers.domain.services import DomainService
from app.src.layers.storage.services import StorageService


# Dependency injection
storage_service = StorageService()
storage_service_adapter = StorageServiceAdapter(storage_service)
domain_service = DomainService(storage_service_adapter)
domain_service_adapter = DomainServiceAdapter(domain_service)

view_shared_args = dict(
    domain_service=domain_service_adapter,
    model_class=api_models.ICSR,
)

urlpatterns = [
    path('test', lambda *args, **kwargs: http.HttpResponse('This is a test')),

    path('icsr', views.ModelClassView.as_view(**view_shared_args)),
    path('icsr/<int:pk>', views.ModelInstanceView.as_view(**view_shared_args)),
    path('icsr/validate', views.ModelBusinessValidationView.as_view(**view_shared_args)),
]
