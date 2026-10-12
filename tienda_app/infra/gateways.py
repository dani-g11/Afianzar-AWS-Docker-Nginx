import datetime
from ..domain.interfaces import ProcesadorPago

class BancoNacionalProcesador(ProcesadorPago):
    """
    Implementación concreta de la infraestructura.
    Simula un banco local escribiendo en un log.
    """
    def pagar(self, monto: float) -> bool:
        # Simulamos una operación de red o persistencia externa.
        # El nombre del archivo incluye tu identidad para que la
        # evidencia de ejecución sea única (requisito del tutorial).
        archivo_log = "pagos_locales_Daniel_G.log"

        with open(archivo_log, "a") as f:
            f.write(f"[{datetime.datetime.now()}] BANCO NACIONAL - Cobro procesado: ${monto}\n")
        return True
