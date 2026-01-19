from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegistroAlumnoForm
from .models import Entrega, Evaluacion, Pregunta, ResultadoExamen

# --- VISTAS DEL SISTEMA ---

@login_required
def panel_alumno(request):
    """Vista principal para los estudiantes: lista de exámenes activos."""
    examenes = Evaluacion.objects.filter(curso=request.user.curso, activa=True)
    return render(request, 'alumnos/panel.html', {'examenes': examenes})

@login_required
def rendir_examen(request, examen_id):
    """Lógica para que el alumno rinda y se calcule su nota con valor 0.5 por pregunta."""
    evaluacion = get_object_or_404(Evaluacion, id=examen_id)
    
    # Verificamos si ya rindió para no duplicar
    if ResultadoExamen.objects.filter(alumno=request.user, evaluacion=evaluacion).exists():
        messages.warning(request, "Ya has rendido este examen.")
        return redirect('panel_alumno')

    if request.method == 'POST':
        fraude = request.POST.get('fraude') == 'true'
        preguntas = evaluacion.preguntas.all()
        puntos = 0
        
        for p in preguntas:
            respuesta_alumno = request.POST.get(f'pregunta_{p.id}')
            # Comparamos con respuesta_correcta que ahora es un String ('1', '2', etc.)
            if respuesta_alumno == str(p.respuesta_correcta):
                puntos += 1
        
        # --- CÁLCULO DE NOTA (Cada pregunta vale 0.5) ---
        # ARREGLO CLAVE: Cambiamos 'no' por 'not'
        if not fraude:
            nota = puntos * 0.5
        else:
            nota = 1.0  # Si hubo fraude, la nota es 1.0
            
        # Guardamos el resultado (ResultadoExamen ahora usa FloatField)
        ResultadoExamen.objects.create(
            alumno=request.user, 
            evaluacion=evaluacion, 
            nota=float(nota), 
            intento_fraude=fraude
        )
        
        return render(request, 'alumnos/resultado_examen.html', {
            'nota': nota, 
            'fraude': fraude, 
            'evaluacion': evaluacion,
            'puntos': puntos
        })
        
    return render(request, 'alumnos/evaluacion_detalle.html', {'evaluacion': evaluacion})

@login_required
def mis_notas(request):
    """Historial de notas del alumno logueado."""
    res = ResultadoExamen.objects.filter(alumno=request.user).select_related('evaluacion')
    return render(request, 'alumnos/mis_notas.html', {'notas_examenes': res})

@login_required
def planilla_notas(request): 
    """Vista para el profesor: lista de todas las notas de todos los alumnos."""
    res = ResultadoExamen.objects.all().select_related('alumno', 'evaluacion')
    return render(request, 'alumnos/planilla_notas.html', {'alumnos_notas': res})

@login_required
def ver_detalle_examen(request, resultado_id):
    """Detalle de un examen específico rendido."""
    res = get_object_or_404(ResultadoExamen, id=resultado_id)
    return render(request, 'alumnos/detalle_resultado_profe.html', {
        'resultado': res, 
        'evaluacion': res.evaluacion
    })

def home(request): 
    """Página de inicio."""
    return render(request, 'alumnos/home.html')

def registro(request):
    """Formulario de registro para nuevos alumnos."""
    if request.method == 'POST':
        form = RegistroAlumnoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Registro exitoso! Ya podés iniciar sesión.")
            return redirect('login')
    else:
        form = RegistroAlumnoForm()
    return render(request, 'alumnos/registro.html', {'form': form})