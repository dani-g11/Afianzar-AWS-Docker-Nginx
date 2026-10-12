from django.shortcuts import render
from django.views import View

from .infra.factories import PaymentFactory
from .services import CompraService


class CompraView(View):
    """Vista "portero": solo recibe la petición y delega en CompraService."""

    template_name = 'tienda_app/compra.html'

    def get(self, request, libro_id):
        servicio = CompraService(PaymentFactory.get_processor())
        contexto = servicio.obtener_detalle_producto(libro_id)
        return render(request, self.template_name, contexto)

    def post(self, request, libro_id):
        servicio = CompraService(PaymentFactory.get_processor())
        try:
            total = servicio.ejecutar_compra(libro_id, cantidad=1)
            return render(request, self.template_name, {'total': total, 'mensaje_exito': f"¡Gracias por su compra! Total: ${total}"})
        except Exception as e:
            return render(request, self.template_name, {'error': str(e)}, status=400)
