from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from .forms import *
from .models import *
from datetime import date
# Create your views here.

def home(request):

    return redirect('articulos')

def admin(request):
    return redirect('articulos_admin')

def gefe(request):

    return redirect('ventas')


def mostrar_articulos_empleado(request):
    bdArticulos = Articulos.objects.all()
    return render(request,'App/articulos.html',{'Articulos':bdArticulos})

def mostrar_articulos_admin(request):
    bdArticulos = Articulos.objects.all()
    return render(request,'App/articulos_admin.html',{'Articulos':bdArticulos})


def agregar_articulos(request):
    state = ''
    frmArt = FormArticulos()

    lista = []
    for i in Rubros.objects.all():
        lista.append(i.descripcion)

    if request.method == 'POST':

        if 'rubro' in request.POST:
            idru = request.POST['rubro']
        else:
            idru = None


        if not Articulos.objects.filter(nombre_art=request.POST['nombre_art'],rubro_id=idru).exists():
            try:
                bdArt = Articulos()

                bdArt.nombre_art = request.POST['nombre_art']
                bdArt.precio = request.POST['precio']

                if 'rubro' in request.POST:
                    bdArt.rubro_id = request.POST['rubro']
                elif 'agregar_rubro' in request.POST and request.POST['agregar_rubro'].strip() != '':

                    if not request.POST['agregar_rubro'] in lista :
                        bdRub = Rubros(descripcion=request.POST['agregar_rubro'])
                        bdRub.save()
                        bdArt.rubro_id = bdRub.id
                    else:
                        rubro = Rubros.objects.get(descripcion=request.POST['agregar_rubro'])
                        bdArt.rubro_id = rubro.id
                else:
                    bdArt.rubro_id = ''

                
                bdArt.stock = request.POST['stock']
                bdArt.save()

                state = 'Articulo agregado'
            except:
                state = 'Ocurrio un error, verifique los campos'
        else:
            state = 'El articulo ya existe'

    return render(request,'App/agregar_articulo.html',{'Formulario':frmArt,'Estado':state })


def modificar_articulos(request,art=None):
    state = ''

    selecArt = Articulos.objects.get(id=art)
    idart = selecArt.id
    frmArticulos = FormArticulos(initial={
        'nombre_art': selecArt.nombre_art,
        'precio': selecArt.precio,
        'rubro': selecArt.rubro,
        'stock': selecArt.stock,
        })
    
    if request.method == 'POST':

        if not Articulos.objects.filter(nombre_art=request.POST['nombre_art'],rubro_id=request.POST['rubro']).exists():
            
            frmArticulos = FormArticulos(request.POST)
            if frmArticulos.is_valid():
                datos = Articulos.objects.get(id=request.POST['idart'])
                datos.nombre_art = request.POST['nombre_art']
                datos.precio = request.POST['precio']
                datos.rubro_id = request.POST['rubro']
                datos.stock = request.POST['stock']
                datos.save()

                state = 'Articulo Modificado'
            else:
                state = 'Error al modificar el formulario'
                #frmArticulos.save()

        else:
            state = 'El articulo ya existe'
    return render(request,'App/modificar_articulo.html',{
        'Formulario':frmArticulos,
        'Id':idart,
        'Estado':state
        })


def eliminar_articulos(request):
    if request.method == 'GET':
        articulo = request.GET['id']

        if Articulos.objects.filter(id=articulo).exists():

            bdArticulos = Articulos.objects.get(id=articulo)
            bdArticulos.delete()

        return redirect('articulos_admin')

def vender_articulos(request):
    if request.method == "GET":
        #Personas
        idart = request.GET['id']
        cantidad = 1

        gettipo = Tipo_persona.objects.get(descripcion='Empleado')

        bdPersona = Personas.objects.filter(tipo_persona=gettipo.id)

        articulo = Articulos.objects.get(id=idart)
        total = int(articulo.precio) * int(cantidad)
        fecha = date.today()

        return render(request,'App/vender.html',{
            'Personas':bdPersona,
            'Articulo':articulo,
            'Cantidad':cantidad,
            'Total':total,
            'Fecha':fecha
            })
    if request.method == "POST":

        bdFactura = Facturas()
        bdDetFactura = Det_factura()
        bdVenta = Ventas()
        bdDetVenta = Det_venta()

        persona = Personas.objects.get(id=request.POST['Vendedor'])
        articulo = Articulos.objects.get(id=request.POST['Articulo'])

        bdDetFactura.fecha_compra = request.POST['Fecha']
        bdDetFactura.precio = int(request.POST['Total'])
        bdDetFactura.tipo_persona_id = persona.tipo_persona_id
        bdDetFactura.cant_compra = request.POST['Cantidad']
        bdDetFactura.save()

        bdFactura.articulo_id = articulo.id
        bdFactura.descripcion = request.POST['Descripcion']
        bdFactura.detalle_id = bdDetFactura.id
        bdFactura.save()

        bdDetVenta.articulo_id = articulo.id
        bdDetVenta.fecha_venta = request.POST['Fecha']
        bdDetVenta.precio = request.POST['Total']
        bdDetVenta.cant_venta = request.POST['Cantidad']
        bdDetVenta.save()

        bdVenta.factura_id = bdFactura.id
        bdVenta.det_venta_id = bdDetVenta.id
        bdVenta.persona_id = persona.id
        bdVenta.save()

        articulo.stock = int(articulo.stock) - int(request.POST['Cantidad'])
        articulo.save()
        
        return redirect("articulos")



def ventas(request):
    ventas = Ventas.objects.all()

    return render(request,'App/ventas.html',{'Ventas':ventas})



def rubros(request):
    rubros = Rubros.objects.all()
    state = ''

    lista = []
    for i in Rubros.objects.all():
        lista.append(i.descripcion)

    if request.method == "POST":
        newrubro = request.POST['newrubro'].strip()
        
        if not newrubro in lista:
            Rubros(descripcion=newrubro).save()
            state = "Se agrego correctamente"
        else:
            state = "El rubro ingresado ya existe"

    if request.method == "GET":
        if 'idrubro' in request.GET:
            idrubro = request.GET['idrubro']

            listasid = []
            for i in Rubros.objects.all():
                listasid.append(i.id)

            print(listasid)

            if int(idrubro) in listasid:
                slcrub = Rubros.objects.get(id=idrubro)
                rubtext = slcrub.descripcion
                slcrub.delete()

                state = "El rubro " + rubtext + " se elimino"
            else:
                return redirect("rubros")

    return render(request,'App/rubros.html',{'Rubros':rubros,'Estado':state})


def modificar_rubro(request,rub=None):
    state = ""
    lista = []
    for i in Rubros.objects.all():
        lista.append(i.descripcion)
    
    rubro = Rubros.objects.get(id=rub)

    if request.method == "POST":
        if not request.POST['new'] in lista:
            try:
                rubro = Rubros(id=request.POST['id'])
                rubro.descripcion = request.POST['new']
                rubro.save()
                state = "Rubro modificado correctamente"
            except:
                state = "Ocurrio un error al modificar el rubro"
        else:
            state = "El rubro ingresado ya existe"

    return render(request,'App/modificar_rubro.html',{"Rubro":rubro,"Estado":state})




#Empleado
def empleados(request):
    empleados = Personas.objects.all()
    state = ""

    if request.method == 'GET':
        if 'id' in request.GET:
            try:
                empleado = Personas.objects.get(id=request.GET['id'])
                if Contacto.objects.filter(id=empleado.datos_personales.contacto_id).exists():
                    Contacto.objects.get(id=empleado.datos_personales.contacto_id).delete()
                Datos_personales.objects.get(id=empleado.datos_personales_id).delete()
                Legajo_empleado.objects.get(id=empleado.legajo_empleado_id).delete()
                
                state = "Empleado eliminado"
            except:
                state = "Ocurrio un error al eliminar, vuelva a intentarlo"

    return render(request,'App/empleados.html',{'Empleados':empleados,'Estado':state})



def agregar_empleado(request):
    bdDomicilio = Domicilio.objects.all()
    bdTipoPersona = Tipo_persona.objects.all()

    stat = ""

    if request.method == "POST":

        if not Datos_personales.objects.filter(nombre=request.POST['Nombre'],apellido=request.POST['Apellido'], fecha_nac=request.POST['Fecha_Nac']).exists():

            bdPersona = Personas()
            bdContacto = Contacto()
            bdDatosP = Datos_personales()
            bdLegajo = Legajo_empleado()

            if request.POST['dom'] == 'list':
                bdDatosP.domicilio_id = request.POST['Domicilio']
            else:
                if request.POST['agregar_domicilio'].strip() != '':
                    new_domicilio = request.POST['agregar_domicilio'].strip()
                    
                    if not Domicilio.objects.filter(localizacion=new_domicilio).exists():
                        bdDomic = Domicilio(localizacion=new_domicilio)
                        bdDomic.save()

                        bdDatosP.domicilio_id = bdDomic.id
                    else:
                        domicilio = Domicilio.objects.get(localizacion=new_domicilio)

                        bdDatosP.domicilio_id = domicilio.id




            if request.POST['Telefono'] != '':
                bdContacto.telefono = request.POST['Telefono']

            if request.POST['Correo'] != '':
                bdContacto.correo = request.POST['Correo']

            if request.POST['Telefono'] != '' or request.POST['Correo'] != '':
                bdContacto.save()
            

            bdDatosP.nombre = request.POST['Nombre']
            bdDatosP.apellido = request.POST['Apellido']

            if request.POST['Telefono'] != '' or request.POST['Correo'] != '':
                #contact = Contacto.objects.get(telefono=request.POST['Telefono'],correo=request.POST['Correo'])
                bdDatosP.contacto_id = bdContacto.id
            
            bdDatosP.fecha_nac = request.POST['Fecha_Nac']
            bdDatosP.save()

            bdLegajo.antiguedad = request.POST['Fecha_Ing']
            bdLegajo.salario = request.POST['Salario']
            bdLegajo.save()


            bdPersona.datos_personales_id = bdDatosP.id
            bdPersona.tipo_persona_id = request.POST['Tipo_Persona']
            bdPersona.legajo_empleado_id = bdLegajo.id

            bdPersona.save()

            stat = "Se ingreso correctamente el empleado"
        else:
            stat = "El empleado ya existe"


    return render(request,'App/agregar_empleado.html',{'Domicilios':bdDomicilio,'TiposPersona':bdTipoPersona,'Estado':stat})
    



def modificar_empleado(request):
    bdDomicilio = Domicilio.objects.all()
    bdTipoPersona = Tipo_persona.objects.all()
    Persona = ''

    stat = ""

    if request.method == "GET":
        if "idpersona" in request.GET:
            Persona = Personas.objects.get(id=request.GET['idpersona'])




    if request.method == "POST":

        idper = request.POST['id']
        bdPersona = Personas.objects.get(id=idper)

        if Datos_personales.objects.filter(nombre=request.POST['Nombre'],apellido=request.POST['Apellido'], fecha_nac=request.POST['Fecha_Nac']).exists():
            comp = Datos_personales.objects.get(nombre=request.POST['Nombre'],apellido=request.POST['Apellido'], fecha_nac=request.POST['Fecha_Nac'])
            comp = comp.id
        else:
            comp = bdPersona.datos_personales.id

        

        if comp == bdPersona.datos_personales.id:
            

            #Modificar Nombre,Apellido,Fecha_nac
            datos = Datos_personales.objects.get(id=bdPersona.datos_personales_id)

            if request.POST['dom'] == 'list':
                
                datos.domicilio_id = request.POST['Domicilio']

                #bdPersona.datos_personales.domicilio_id = request.POST['Domicilio']
            else:
                if request.POST['agregar_domicilio'].strip() != '':
                    lista = []
                    new_domicilio = request.POST['agregar_domicilio'].strip()

                    for i in bdDomicilio:
                        lista.append(i)
                    
                    if not new_domicilio in lista:
                        bdDomic = Domicilio(localizacion=new_domicilio)
                        bdDomic.save()

                        datos = Datos_personales.objects.get(id=bdPersona.datos_personales_id)
                        datos.domicilio_id = bdDomic.id

                        #bdPersona.datos_personales.domicilio_id = bdDomic.id
                    else:
                        domicilio = Domicilio.objects.get(localizacion=new_domicilio)

                        datos = Datos_personales.objects.get(id=bdPersona.datos_personales_id)
                        datos.domicilio_id = domicilio.id

                        #bdPersona.datos_personales.domicilio_id = domicilio.id



            
            if request.POST['Telefono'] != '' or request.POST['Correo'] != '':
                if not Contacto.objects.filter(id=bdPersona.datos_personales.contacto_id).exists():

                    contacto = Contacto()

                    if request.POST['Telefono'] != '':
                        contacto.telefono = request.POST['Telefono']
                    else:
                        contacto.telefono = None

                    if request.POST['Correo'] != '':
                        contacto.correo = request.POST['Correo'].strip()
                    else:
                        contacto.correo = ''

                    contacto.save()

                    datos.contacto_id = contacto.id
                    

                else:
                    contacto = Contacto.objects.get(id=bdPersona.datos_personales.contacto_id)

                    if request.POST['Telefono'] != '':
                        contacto.telefono = request.POST['Telefono']
                    else:
                        contacto.telefono = None
                    if request.POST['Correo'] != '':
                        contacto.correo = request.POST['Correo'].strip()
                    else:
                        contacto.correo = ''
                    
                    contacto.save()

            datos.nombre = request.POST['Nombre']
            datos.apellido = request.POST['Apellido']
            datos.fecha_nac =  request.POST['Fecha_Nac']

            datos.save()


            bdPersona.tipo_persona_id = request.POST['Tipo_Persona']
            bdPersona.save()

            legajo = Legajo_empleado.objects.get(id=bdPersona.legajo_empleado_id)
            legajo.salario = request.POST['Salario']
            legajo.fecha_ing = request.POST['Fecha_Ing']
            legajo.save()

            stat = "Los datos se modificaron exitosamente"
        else:
            stat = "El empleado ya existe"






    return render(request,'App/modificar_empleado.html',{
        'Persona':Persona,
        'Domicilios':bdDomicilio,
        'TiposPersonas':bdTipoPersona,
        'Estado':stat
        })
    
