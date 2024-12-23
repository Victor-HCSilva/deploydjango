from django.db import models
from medicos.models import Medico
from pacientes.models import Paciente
from datetime import time

class AgendamentoConsulta(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    
    HORARIOS = (
        (time(8, 0), "08:00 às 09:00"),
        (time(9, 0), "09:00 às 10:00"),
        (time(10, 0), "10:00 às 11:00"),
        (time(11, 0), "11:00 às 12:00"),
        (time(12, 0), "12:00 às 13:00"),
        (time(13, 0), "13:00 às 14:00"),
    )
    
    data = models.DateField()
    hora = models.TimeField(
        choices=HORARIOS, default=time(8, 0)
    )

    def __str__(self):
        return f"Consulta de {self.paciente} com {self.medico} em {self.data} às {self.hora}"