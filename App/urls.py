"""Kiosco URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('',views.home,name="home"),
    path('administrador/',views.admin,name="admin"),
    path('gefe/',views.gefe,name="gefe"),

    path('administrador/articulos/',views.mostrar_articulos_admin,name="articulos_admin"),
    path('articulos/vender/',views.vender_articulos,name="vender"),

    path('articulos/',views.mostrar_articulos_empleado,name="articulos"),
    path('administrador/articulos/modificar/articulo/<int:art>',views.modificar_articulos,name="modificar"),
    path('administrador/articulos/eliminar/',views.eliminar_articulos,name="eliminar"),
    path('administrador/articulos/agregar/',views.agregar_articulos,name="agregar"),
    path('administrador/articulos/rubros/',views.rubros,name="rubros"),
    path('administrador/articulos/modificar/rubro/<int:rub>',views.modificar_rubro,name="modificar_rubro"),


    path('gefe/agregar_empleado/',views.agregar_empleado,name="agregar_empleado"),
    path('gefe/modificar_empleado/',views.modificar_empleado,name="modificar_empleado"),
    path('gefe/empleados/',views.empleados,name="empleados"),
    path('gefe/ventas/',views.ventas,name="ventas"),

    
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
