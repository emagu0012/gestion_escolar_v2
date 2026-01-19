import csv
from django.contrib import admin
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from datetime import date
from .models import Usuario, Evaluacion, Pregunta, ResultadoExamen, Entrega, Asistencia, NotaManual

# --- 1. CONFIGURACIÓN DE INLINES ---
class AsistenciaInline(admin.TabularInline):
    model = Asistencia
    extra = 1

class NotaManualInline(admin.TabularInline):
    model = NotaManual
    extra = 1

class PreguntaInline(admin.TabularInline):
    model = Pregunta
    extra = 3

# --- 2. CONFIGURACIÓN DE USUARIO CON EXPORTADOR ---
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('apellido_completo', 'nombre_completo', 'curso', 'porcentaje_asistencia_view', 'promedio_examenes_view')
    list_filter = ('curso',)
    search_fields = ('apellido_completo', 'nombre_completo', 'username')
    inlines = [AsistenciaInline, NotaManualInline]
    actions = ['marcar_presente_hoy', 'marcar_ausente_hoy', 'exportar_planilla_excel_completa']

    @admin.action(description="📊 Generar Planilla Excel (Asistencias + VAR + TPs)")
    def exportar_planilla_excel_completa(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="Planilla_Escuela_{date.today()}.csv"'
        writer = csv.writer(response)
        
        fechas = Asistencia.objects.order_by('fecha').values_list('fecha', flat=True).distinct()
        header = ['CURSO', 'ALUMNOS', 'PRESENTE', 'FALTAS', '% ASIST', 'PROM. VAR', 'NOTAS TPs']
        for f in fechas:
            header.append(f.strftime('%d/%m'))
        writer.writerow(header)

        for alumno in queryset.order_by('curso', 'apellido_completo'):
            total_clases = Asistencia.objects.filter(alumno=alumno).count()
            presentes = Asistencia.objects.filter(alumno=alumno, estado='P').count()
            ausentes = Asistencia.objects.filter(alumno=alumno, estado='A').count()
            porc = f"{int((presentes / total_clases * 100))}%" if total_clases > 0 else "0%"
            
            notas_v = ResultadoExamen.objects.filter(alumno=alumno).values_list('nota', flat=True)
            prom_v = round(sum(notas_v) / len(notas_v), 1) if notas_v else "-"
            
            notas_m = NotaManual.objects.filter(alumno=alumno).values_list('nota', flat=True)
            txt_tps = " / ".join([str(n) for n in notas_m]) if notas_m else "-"

            fila = [alumno.get_curso_display(), f"{alumno.apellido_completo}, {alumno.nombre_completo}", presentes, ausentes, porc, prom_v, txt_tps]
            for f in fechas:
                asist = Asistencia.objects.filter(alumno=alumno, fecha=f).first()
                fila.append(asist.estado if asist else "-")
            writer.writerow(fila)
        return response

    def porcentaje_asistencia_view(self, obj):
        total = Asistencia.objects.filter(alumno=obj).count()
        if total == 0: return "0%"
        pres = Asistencia.objects.filter(alumno=obj, estado='P').count()
        porc = (pres / total) * 100
        color = "#28a745" if porc >= 70 else "#dc3545"
        return mark_safe(f'<b style="color:{color};">{int(porc)}%</b>')
    porcentaje_asistencia_view.short_description = "% Asist."

    def promedio_examenes_view(self, obj):
        notas = ResultadoExamen.objects.filter(alumno=obj).values_list('nota', flat=True)
        prom = sum(notas) / len(notas) if notas else 0
        color = "#28a745" if prom >= 7 else "#dc3545"
        return mark_safe(f'<b style="color:{color};">{round(prom, 2) if notas else "-"}</b>')
    promedio_examenes_view.short_description = "Prom. VAR"

    @admin.action(description="⚽ Marcar PRESENTE (Hoy)")
    def marcar_presente_hoy(self, request, queryset):
        for alumno in queryset:
            Asistencia.objects.update_or_create(alumno=alumno, fecha=date.today(), defaults={'estado': 'P'})

    @admin.action(description="❌ Marcar AUSENTE (Hoy)")
    def marcar_ausente_hoy(self, request, queryset):
        for alumno in queryset:
            Asistencia.objects.update_or_create(alumno=alumno, fecha=date.today(), defaults={'estado': 'A'})

# --- 3. CONFIGURACIÓN DE EVALUACIONES (SIN IA) ---
@admin.register(Evaluacion)
class EvaluacionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'curso', 'activa')
    fields = ('titulo', 'curso', 'activa', 'tiempo_limite')
    inlines = [PreguntaInline]

# --- 4. OTROS REGISTROS ---
@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'alumno', 'estado')
    list_filter = ('fecha', 'alumno__curso', 'estado')
    date_hierarchy = 'fecha'

@admin.register(ResultadoExamen)
class ResultadoExamenAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'evaluacion', 'nota', 'fecha', 'intento_fraude')
    list_filter = ('intento_fraude', 'alumno__curso')
    readonly_fields = ('fecha',)

@admin.register(NotaManual)
class NotaManualAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'tarea_nombre', 'nota')
    list_filter = ('alumno__curso',)

@admin.register(Entrega)
class EntregaAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'archivo', 'fecha_entrega')
    readonly_fields = ('fecha_entrega',)