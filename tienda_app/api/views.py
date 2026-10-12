from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from tienda_app.infra.factories import PaymentFactory
from tienda_app.models import Libro
from tienda_app.services import CompraService

from .serializers import LibroSerializer, OrdenInputSerializer


class ProductoListAPIView(APIView):
    """
    GET /api/v1/productos/ -> Lista los libros disponibles (servido por Django v1).
    Sirve como prueba de coexistencia del monolito en el Strangler Pattern.
    """

    def get(self, request):
        libros = Libro.objects.all()
        serializer = LibroSerializer(libros, many=True)
        return Response(
            {
                'servicio': 'Tienda API (Django v1)',
                'endpoint': '/api/v1/productos/',
                'productos': serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class CompraAPIView(APIView):
    """
    Endpoint para procesar compras via JSON.
    GET  /api/v1/comprar/  -> Devuelve informacion del endpoint (evidencia del despliegue).
    POST /api/v1/comprar/  -> Procesa una compra.
    Payload POST: {"libro_id": 1, "direccion_envio": "Calle 123", "cantidad": 1}
    """

    def get(self, request):
        """
        Respuesta informativa para verificar que la API esta viva.
        Al abrir la URL en el navegador (GET) se vera este JSON servido desde AWS.
        """
        return Response(
            {
                'servicio': 'Tienda API',
                'endpoint': '/api/v1/comprar/',
                'estado': 'activo',
                'mensaje': 'API desplegada correctamente. Use POST para procesar una compra.',
                'metodos_disponibles': ['GET', 'POST'],
                'ejemplo_payload_post': {
                    'libro_id': 1,
                    'direccion_envio': 'Calle 123',
                    'cantidad': 1,
                },
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = OrdenInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        datos = serializer.validated_data

        try:
            gateway = PaymentFactory.get_processor()
            servicio = CompraService(procesador_pago=gateway)
            usuario = request.user if request.user.is_authenticated else None
            resultado = servicio.ejecutar_compra(
                libro_id=datos['libro_id'],
                cantidad=datos.get('cantidad', 1),
                direccion=datos['direccion_envio'],
                usuario=usuario,
            )

            return Response(
                {
                    'estado': 'exito',
                    'mensaje': f'Orden creada. Total: {resultado}',
                },
                status=status.HTTP_201_CREATED,
            )

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_409_CONFLICT)
        except Exception:
            return Response({'error': 'Error interno'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
