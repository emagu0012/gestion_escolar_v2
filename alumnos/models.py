import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg

# --- 1. MODELO DE USUARIO ---
class Usuario(AbstractUser):
    CURSOS = [
        ('2A', '2do A'),
        ('2B', '2do B'),
        ('5A', '5to A'),
        ('6A', '6to'),
    ]
    nombre_completo = models.CharField(max_length=100, verbose_name="Nombre")
    apellido_completo = models.CharField(max_length=100, verbose_name="Apellido")
    curso = models.CharField(max_length=2, choices=CURSOS, default='2A')

    def __str__(self):
        return f"{self.apellido_completo}, {self.nombre_completo} ({self.get_curso_display()})"

# --- 2. MODELOS DE EVALUACIÓN Y NOTAS ---
class Evaluacion(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Título del Examen")
    archivo_base = models.FileField(
        upload_to='examenes_pdf/', 
        null=True, 
        blank=True, 
        verbose_name="Archivo PDF/Texto para IA"
    )
    curso = models.CharField(max_length=2, choices=Usuario.CURSOS)
    activa = models.BooleanField(default=True)
    tiempo_limite = models.PositiveIntegerField(default=60, verbose_name="Tiempo límite (min)")

    class Meta:
        verbose_name_plural = "Evaluaciones"

    def __str__(self):
        return f"{self.titulo} - {self.get_curso_display()}"

class Pregunta(models.Model):
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE, related_name='preguntas')
    texto_pregunta = models.TextField()
    opcion1 = models.CharField(max_length=255)
    opcion2 = models.CharField(max_length=255)
    opcion3 = models.CharField(max_length=255)
    opcion4 = models.CharField(max_length=255, null=True, blank=True)
    respuesta_correcta = models.CharField(
        max_length=1, 
        choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')]
    )

    def __str__(self):
        return f"Pregunta de: {self.evaluacion.titulo}"

class ResultadoExamen(models.Model):
    alumno = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE)
    nota = models.FloatField() # CAMBIO A FLOAT PARA DECIMALES (0.5 por pregunta)
    intento_fraude = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)
    respuestas_detalle = models.JSONField(null=True, blank=True)

    class Meta:
        unique_together = ('alumno', 'evaluacion')
        verbose_name_plural = "Resultados de Exámenes"

class NotaManual(models.Model):
    alumno = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tarea_nombre = models.CharField(max_length=100)
    nota = models.FloatField() # También aceptamos decimales acá

    class Meta:
        verbose_name_plural = "Notas Manuales"

class Entrega(models.Model):
    alumno = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='entregas/')
    fecha_entrega = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Entregas de Alumnos"

# --- 3. MODELO DE ASISTENCIA ---
class Asistencia(models.Model):
    ESTADOS = (('P', 'Presente'), ('A', 'Ausente'))
    alumno = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha = models.DateField()
    estado = models.CharField(max_length=1, choices=ESTADOS)

    class Meta:
        unique_together = ('alumno', 'fecha')
        verbose_name_plural = "Asistencias"

    def __str__(self):
        return f"{self.alumno.apellido_completo} - {self.fecha}: {self.estado}"

# --- 4. SEÑAL PARA GOOGLE SHEETS ---
@receiver(post_save, sender=Asistencia)
def sincronizar_con_sheets(sender, instance, **kwargs):
    try:
        import gspread
        from oauth2client.service_account import ServiceAccountCredentials
        
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        ruta_json = '/home/tecnica283/google-credentials.json'
        
        if not os.path.exists(ruta_json):
            return

        creds = ServiceAccountCredentials.from_json_keyfile_name(ruta_json, scope)
        client = gspread.authorize(creds)
        spreadsheet = client.open("Asistencia283Taller2025") 
        nombre_hoja = instance.alumno.get_curso_display()
        worksheet = spreadsheet.worksheet(nombre_hoja)

        alumno = instance.alumno
        total_clases = Asistencia.objects.filter(alumno=alumno).count()
        presentes = Asistencia.objects.filter(alumno=alumno, estado='P').count()
        porcentaje = (presentes / total_clases * 100) if total_clases > 0 else 0

        n_examenes = ResultadoExamen.objects.filter(alumno=alumno).aggregate(Avg('nota'))['nota__avg'] or 0
        n_manuales = NotaManual.objects.filter(alumno=alumno).aggregate(Avg('nota'))['nota__avg'] or 0
        
        if n_examenes > 0 and n_manuales > 0:
            promedio_final = (n_examenes + n_manuales) / 2
        else:
            promedio_final = n_examenes or n_manuales or 0

        nombre_buscar = f"{alumno.apellido_completo}, {alumno.nombre_completo}"
        fecha_buscar = instance.fecha.strftime('%d/%m')

        celda_alumno = worksheet.find(nombre_buscar)
        
        if celda_alumno:
            fila = celda_alumno.row
            celda_fecha = worksheet.find(fecha_buscar)
            if celda_fecha:
                worksheet.update_cell(fila, celda_fecha.col, instance.estado)

            worksheet.update_cell(fila, 2, f"{porcentaje:.1f}%")
            worksheet.update_cell(fila, 3, round(promedio_final, 2))

    except Exception as e:
        print(f"Error en sincronización: {e}")