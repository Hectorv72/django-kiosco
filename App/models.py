from django.db import models
#from django import forms

# Create your models here.

#funciones
#def subir_archivo(instance, filename):
#	return 'files/%s'% instance.nom_foro +'/%s'% filename

#Campos


#Articulos
class Rubros(models.Model):
    descripcion = models.CharField(max_length=30)

    def __str__(self):
        return self.descripcion


class Articulos(models.Model):
    nombre_art = models.CharField(max_length=30)
    precio = models.IntegerField()
    rubro = models.ForeignKey(Rubros, on_delete=models.SET_NULL,null=True)
    stock = models.IntegerField()

    def __str__(self):
        return self.nombre_art



#Persona

class Domicilio(models.Model):
    localizacion = models.CharField(max_length=50)

    def __str__(self):
        return self.localizacion


class Contacto(models.Model):
    telefono = models.IntegerField(null = True)
    correo = models.CharField(max_length=50, null = True)

    def __str__(self):
        return self.correo


class Datos_personales(models.Model):
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    fecha_nac = models.DateField()
    domicilio = models.ForeignKey(Domicilio, on_delete=models.CASCADE)
    contacto = models.ForeignKey(Contacto, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str( str(self.nombre) + " " + str(self.apellido))
        

class Tipo_persona(models.Model):
    descripcion = models.CharField(max_length=30)

    def __str__(self):
        return self.descripcion


class Legajo_empleado(models.Model):
    antiguedad = models.DateField()
    salario = models.IntegerField()

    def __str__(self):
        return str( str(self.antiguedad) + "($" + str(self.salario) + ")" )


class Personas(models.Model):
    datos_personales = models.ForeignKey(Datos_personales, on_delete=models.CASCADE)
    tipo_persona = models.ForeignKey(Tipo_persona, on_delete=models.CASCADE)
    legajo_empleado = models.ForeignKey(Legajo_empleado, on_delete=models.CASCADE)

    def __str__(self):
        return str( str(self.datos_personales.nombre) + " " + str(self.datos_personales.apellido))




#Ventas y factura

class Det_factura(models.Model):
    precio = models.IntegerField()
    fecha_compra = models.DateField()
    cant_compra = models.IntegerField()
    tipo_persona = models.ForeignKey(Tipo_persona, on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return str(self.fecha_compra)


class Facturas(models.Model):
    articulo = models.ForeignKey(Articulos, on_delete=models.SET_NULL,null=True)
    descripcion = models.CharField(max_length=50)
    detalle = models.ForeignKey(Det_factura, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.descripcion


class Det_venta(models.Model):
    articulo = models.ForeignKey(Articulos, on_delete=models.SET_NULL,null=True)
    fecha_venta = models.DateField()
    precio = models.IntegerField()
    cant_venta = models.IntegerField()

    def __str__(self):
        return str(self.fecha_venta)



class Ventas(models.Model):
    factura = models.ForeignKey(Facturas, on_delete=models.CASCADE)
    det_venta = models.ForeignKey(Det_venta, on_delete=models.CASCADE)
    persona = models.ForeignKey(Personas, on_delete=models.CASCADE)
    
    def __str__(self):
        return str( str(self.persona) + "(" + str(self.det_venta.fecha_venta) + ")" )

#class Persona(models.Model):
    #datos_personales = ForeignKey(Rubros, on_delete=models.CASCADE)
