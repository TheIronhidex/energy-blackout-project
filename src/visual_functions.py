import matplotlib.pyplot as plt
from pylab import mpl
import math

# Ajuste lineal unario
# Los datos de ajuste utilizados son xi = 1,2,3,4,5,6,7
# El valor correspondiente de la función correspondiente yi = 0.5,2.5,2,4,3.5,6,5.5

# Completar el cálculo de los parámetros de la curva de ajuste

def liner_fitting(data_x,data_y):
    size = len(data_x)
    i=0
    sum_xy=0
    sum_y=0
    sum_x=0
    sum_sqare_x=0
    average_x=0
    average_y=0
    while i<size:
        sum_xy+=data_x[i]*data_y[i]
        sum_y+=data_y[i]
        sum_x+=data_x[i]
        sum_sqare_x+=data_x[i]*data_x[i]
        i+=1
    average_x=sum_x/size
    average_y=sum_y/size
    return_k=(size*sum_xy-sum_x*sum_y)/(size*sum_sqare_x-sum_x*sum_x)
    return_b=average_y-average_x*return_k
    return [return_k,return_b]
 
# Después de completar el cálculo del valor de función correspondiente en la curva

def calculate_lin(data_x,k,b):
    datay=[]
    for x in data_x:
        datay.append(k*x+b)
    return datay
 
# Finalizar dibujo de función
def draw_lin(data_x,data_y_new,data_y_old):
    plt.plot (data_x, data_y_new, label = "test", color = "black")
    plt.scatter (data_x, data_y_old, label = "discrete data")
    mpl.rcParams['axes.unicode_minus'] = False
    plt.title ("Datos de ajuste lineal de una variable")
    plt.legend(loc="upper left")
    plt.show()

#Completar el cálculo de las variables correspondientes antes del cálculo de parámetros de la curva ajustada
def polynomial_fitting(data_x,data_y):
    size=len(data_x)
    i=0
    sum_x = 0
    sum_sqare_x =0
    sum_third_power_x = 0
    sum_four_power_x = 0
    average_x = 0
    average_y = 0
    sum_y = 0
    sum_xy = 0
    sum_sqare_xy = 0
    while i<size:
        sum_x += data_x[i]
        sum_y += data_y[i]
        sum_sqare_x += math.pow(data_x[i],2)
        sum_third_power_x +=math.pow(data_x[i],3)
        sum_four_power_x +=math.pow(data_x[i],4)
        sum_xy +=data_x[i]*data_y[i]
        sum_sqare_xy +=math.pow(data_x[i],2)*data_y[i]
        i += 1
    average_x=sum_x/size
    average_y=sum_y/size
    return [[size, sum_x, sum_sqare_x, sum_y]
        , [sum_x, sum_sqare_x, sum_third_power_x, sum_xy]
        , [sum_sqare_x,sum_third_power_x,sum_four_power_x,sum_sqare_xy]]
 
#Completar el cálculo de los parámetros de la curva de ajuste
# Al resolver la ecuación, use el método de eliminación gaussiano para calcular el valor del parámetro correspondiente

def calculate_parameter(data):
    #i se usa para controlar elementos de columna, línea es un elemento de línea, j se usa para controlar el número de bucles y los datos se usan para almacenar variables locales. Guardar el valor modificado
    i = 0
    j = 0
    line_size = len(data)
    #Convierta el determinante al determinante triangular superior
    while j < line_size-1:
        line = data[j]
        temp = line[j]
        templete=[]
        for x in line:
            x=x/temp
            templete.append(x)
        data[j]=templete
        #flag sign el número de líneas que deben eliminarse
        flag = j+1
        while flag < line_size:
            templete1 = []
            temp1=data[flag][j]
            i = 0
            for x1 in data[flag]:
                if x1!=0:
                   x1 = x1-(temp1*templete[i])
                   templete1.append(x1)
                else:
                   templete1.append(0)
                i += 1
            data[flag] = templete1
            flag +=1
        j += 1
 
 
         #Buscando el valor del parámetro correspondiente
 
    parameters=[]
    i=line_size-1
         #j Identificación menos el número de elementos
         #flag_rolIdentifique qué columna excepto
    flag_j=0
    rol_size=len(data[0])
    flag_rol=rol_size-2
         #Obtener la cantidad de soluciones
    while i>=0:
        operate_line = data[i]
        if i==line_size-1:
            parameter=operate_line[rol_size-1]/operate_line[flag_rol]
            parameters.append(parameter)
        else:
            flag_j=(rol_size-flag_rol-2)
            temp2=operate_line[rol_size-1]
                         #result_flag es la bandera para acceder a la solución que se ha resuelto
            result_flag=0
            while flag_j>0:
                temp2-=operate_line[flag_rol+flag_j]*parameters[result_flag]
                result_flag+=1
                flag_j-=1
            parameter=temp2/operate_line[flag_rol]
            parameters.append(parameter)
        flag_rol-=1
        i-=1
    return parameters
 
#Calcular el valor de la curva ajustada
def calculate_bin(data_x,parameters):
    datay=[]
    for x in data_x:
        datay.append(parameters[2]+parameters[1]*x+parameters[0]*x*x)
    return datay
 
 
 
#Finalizar dibujo de función
def draw_bin(data_x,data_y_new,data_y_old):
    plt.plot (data_x, data_y_new, label = "curva de ajuste", color = "black")
    plt.scatter (data_x, data_y_old, label = "datos discretos")
    mpl.rcParams['axes.unicode_minus'] = False
    plt.title ("Datos de ajuste polinomial de una variable")
    plt.legend(loc="upper left")
    plt.show()