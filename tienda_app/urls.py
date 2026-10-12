from django.urls import path
from .views import CompraView
from .api.views import CompraAPIView

urlpatterns = [
    # Vista HTML (una "puerta" hacia la lógica de negocio).
    path('compra/<int:libro_id>/', CompraView.as_view(), name='finalizar_compra'),
    # API REST JSON (la otra "puerta" hacia la MISMA lógica: CompraService).
    path('api/v1/comprar/', CompraAPIView.as_view(), name='api_comprar'),
]
