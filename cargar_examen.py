import os
import django

# 1. Configuración de Django (Asegurate que el nombre del proyecto sea correcto)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_escolar.settings')
django.setup()

from alumnos.models import Evaluacion, Pregunta

def ejecutar():
    print("Iniciando carga de examen para el más grande...")
    
    # 2. Creamos la Evaluación (o la buscamos si ya existe)
    # Se asigna al curso '6A' como ejemplo, podés cambiarlo a '5A' o el que necesites
    examen, created = Evaluacion.objects.get_or_create(
        titulo="Examen: Higiene y Seguridad Laboral",
        defaults={
            'curso': '6A', 
            'tiempo_limite': 40, 
            'activa': True
        }
    )

    # 3. Lista de las 20 preguntas (Ajustadas a tu models.py)
    # Formato: [Pregunta, Op1, Op2, Op3, Op4, Correcta('1'-'4')]
    datos = [
        ["¿Qué rama evita que un trabajador desarrolle una enfermedad por ruido a largo plazo?", "Higiene en el Ámbito Laboral", "Seguridad en el Ámbito Laboral", "Mantenimiento Preventivo", "Primeros Auxilios", "1"],
        ["Un operario se cae por no usar arnés. ¿Qué objetivo de seguridad falló?", "Eliminar o disminuir riesgo de accidentes", "Mejorar la productividad", "Evitar multas", "Prevenir enfermedades mentales", "1"],
        ["¿Por qué la Higiene Laboral tiene carácter preventivo?", "Actúa antes de que el empleado se enferme", "Se encarga de limpiar el piso", "Actúa solo después de un herido", "Reduce costos de seguro", "1"],
        ["En un incendio, ¿cuál es la función de cerrar puertas y ventanas?", "Evitar propagación por corrientes de aire", "Evitar robos durante el siniestro", "Mantener el aire acondicionado", "Facilitar que se rompan vidrios", "1"],
        ["Si falta un compañero en el punto de encuentro, ¿qué se debe hacer?", "Avisar inmediato al responsable", "Volver al edificio a buscarlo", "Esperar 10 minutos a que llegue", "Llamarlo por celular primero", "1"],
        ["¿Por qué el área de sistemas requiere un plan de emergencia técnico?", "Para proteger información y personal específico", "Para que los técnicos salgan primero", "Para evitar que se mojen equipos", "Para cumplir con la burocracia", "1"],
        ["¿Cuál es la prioridad absoluta de la Seguridad en el Trabajo?", "Evitar accidentes graves y mortales", "Que las máquinas no se ronpan", "Terminar la producción a tiempo", "Mantener el orden estético", "1"],
        ["¿Por qué es fundamental seguir el 'camino designado' en una evacuación?", "Es la ruta más segura y planificada", "Para que el director nos vea pasar", "Porque está prohibido ir por otro lado", "Para llegar primero al buffet", "1"],
        ["¿Cómo se define el área física donde se trabaja bajo supervisión?", "Lugar de Trabajo", "Sector de Recreación", "Zona de Peligro", "Propiedad Privada", "1"],
        ["¿Qué acción se coordina con Bomberos apenas llegan al lugar?", "Guiarlos al lugar exacto del siniestro", "Pedirles revisar matafuegos vencidos", "Preguntarles si quieren tomar algo", "Darles el listado de alumnos", "1"],
        ["¿Quién debe desconectar la energía eléctrica en una emergencia?", "El personal designado en el plan", "Cualquier alumno que pase cerca", "Nadie, se corta sola con el fuego", "El profesor de gimnasia", "1"],
        ["Si una empresa no tiene accidentes pero sí empleados con estrés, falla en:", "Higiene (integridad física y mental)", "Seguridad Industrial", "Contabilidad", "Logística", "1"],
        ["¿Por qué retirar productos inflamables de áreas próximas al fuego?", "Evitar propagación o explosiones", "Para que no se ensucien", "Porque son productos caros", "Para dejar espacio para caminar", "1"],
        ["¿Qué estudia la Higiene al analizar 'Hombre - Ambiente de trabajo'?", "Cómo el entorno afecta la salud", "Cuánta gente entra en la oficina", "La decoración del puesto", "Que los empleados no ensucien", "1"],
        ["¿Cuál es la última acción antes de abandonar una habitación con fuego?", "Cerrar la puerta sin llave", "Gritar para asustar al fuego", "Abrir todas las ventanas", "Esconderse bajo un mueble", "1"],
        ["¿Cuál es la diferencia entre riesgo y accidente?", "Riesgo es probabilidad, accidente es el hecho", "Son lo mismo", "El riesgo es solo en fábricas", "El accidente es planeado", "1"],
        ["¿Para qué sirve que todo el personal conozca los procedimientos?", "Evitar pánico y garantizar orden", "Para no preguntar nada durante el fuego", "Para aprobar exámenes de la ART", "Para parecer más profesionales", "1"],
        ["Si un extintor tiene la carga vencida, ¿qué se está incumpliendo?", "Control de equipos contra incendio", "Primeros Auxilios", "Ergonomía", "Derecho al descanso", "1"],
        ["¿Cómo se debe avanzar si el camino tiene mucho humo?", "Agachado o gateando", "Corriendo rápido sin respirar", "Subiendo al techo", "Saltando por la ventana", "1"],
        ["¿Cuál es el fin último de un puesto de trabajo seguro y digno?", "Que la salud no se deteriore trabajando", "Que el jefe esté contento", "Cobrar sueldos más altos", "Que la fábrica dure muchos años", "1"]
    ]

    # 4. Carga masiva (Usando los nombres de campos de tu models.py)
    for d in datos:
        pregunta, created_p = Pregunta.objects.get_or_create(
            evaluacion=examen,
            texto_pregunta=d[0],
            defaults={
                'opcion1': d[1],
                'opcion2': d[2],
                'opcion3': d[3],
                'opcion4': d[4],
                'respuesta_correcta': d[5]
            }
        )
        if created_p:
            print(f"Cargada: {d[0][:30]}...")
        else:
            print(f"Ya existía: {d[0][:30]}...")

    print("\n--- ¡GOLAZO! TERMINAMOS, HOLA BOSTERO CÓMO ESTÁS! EXAMEN LISTO ---")

if __name__ == "__main__":
    ejecutar()