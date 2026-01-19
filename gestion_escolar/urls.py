from django.contrib import admin
from django.urls import path
from alumnos import views 
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 1. LA HOME
    path('', views.home, name='home'),
    
    # 2. EL ADMIN
    path('admin/', admin.site.urls),
    
    # 3. REGISTRO
    path('registro/', views.registro, name='registro'),
    
    # 4. LOGIN (Sincronizado con settings)
    path('login/', auth_views.LoginView.as_view(template_name='alumnos/login.html'), name='login'),
    
    # 5. LOGOUT
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
    # 6. PANEL ALUMNO (Cambiado de 'panel' a 'panel_alumno' para coincidir con settings)
    path('panel/', views.panel_alumno, name='panel_alumno'),

    # 7. MIS NOTAS
    path('mis-notas/', views.mis_notas, name='mis_notas'),
    
    # 8. EL EXAMEN
    path('examen/<int:examen_id>/', views.rendir_examen, name='rendir_examen'),
    
    # 9. LA PLANILLA
    path('planilla-notas/', views.planilla_notas, name='planilla_notas'),
    
    # 10. EL VAR (Detalle)
    path('detalle-examen/<int:resultado_id>/', views.ver_detalle_examen, name='ver_detalle_examen'),
]

# 11. ARCHIVOS ESTÁTICOS Y MULTIMEDIA (Configuración robusta para producción)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)