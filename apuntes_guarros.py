"""
# CONSEJOS
## Organizacion de codigo (modularizacion)
- crear archivos "utils"
En esta carpeta, en los archivos va a haber un fichero "XXX_utils.py" que va a tener las funciones de ese ambito
Esto sería algo así como
    + Crear una carpeta utils
    + Meter en ella fichero charts_utils.py (contiene funciones de gráficos)
    + Meter en ella fichero data_utils.py (contiene funciones de ETL)
Una función a poner en un fichero "utils" seria cualquier funcion que hace algún cálculo complejo y NO crea una página

- crear archivos "page"
En esta carpeta , los archivos son el código que genera cada una de las páginas de la app
EJEMPLO:
    + pages (carpeta)
        + home_page.py
        + other_page.py
Estos archivos, su "main" sería generar un metodo llamado "layout" (distribución) que debería de devolver la distribución
de la página que representa este archivo
PARA CAMBIAR DE LAYOUT se utiliza el componente de la librería DCC llamado link (dcc.Link entiendo que sería), esto cambia la URL sin recargar la página
LUEGO se utliza el componente de DCC llamado location (dcc.Location entiendo que sería) que lee como input el link en un Callback
LA FORMA MÁS SIMPLE AHORA es utilizar la feature Dash Pages


## Code formatters (Readability)
- Utilizar un Python formatter. Ellos usan uno llamado "black"





# Consejos / tutorial de Bootstrap + Dash Plotly        https://www.youtube.com/watch?v=0mfIK8zxUds
- UTILIZAR
    app.layout = dbc.Container()
EN LUGAR DE
    app.layout = html.Div()

- Dentro de lo anterior, lo primero a declarar son los ROWs  y luego dentro de los ROWs, los COLs
Dentro de los COLS, directamente ponemos el componente
Los ROWs a parte del atributo CHILDREN tienen un atributo llamado NO_GUTTERS, que si lo pones a TRUE hace que las COLUMNAS HIJAS NO TENGAN NINGUN TIPO DE SEPARACION ENTRE ELLAS

Los COLS a parte del atributo CHILDREN tienen un atributo llamado WIDTH  que puede ser de hasta 12. (indica el nº de columnas a ocupar)
EJ:
    width = 4
    width = {'size': 4}
    width = {'size': 4, 'offset':1}
    width = {'size': 4, 'offset':1, 'order':2} # La clave ORDER hace que Col esté en 2 posición respecto a los otros, se utiliza para no tener que escribir en orden los componentes

- Si quiero darle estilos asignando una clase, usao las clases de bootstrap natural. Si quiero poner más de una, ponerlas separadas por espacio NO POR COMA
-
"""

"""
# PRINCIPIOS DE DASH

Habría que dividir el proyecto en 3 secciones principales
    - Una para preparar los datos
    - Otra para preparar los componentes y aspecto de la página 
    - Otra para dar el comportamiento a las cosas (esto es con los callbacks)

# Princpios de los callbacks
Los callbacks son metodos normales con un decoratos
Recibe 2 listas
    - Outputs --> Puede tener N componentes PERO al finalizar el metodo y poner RETURN el número de elementos
    a devolver han de ser los mismos Y EN EL MISMO ORDEN QUE LOS QUE PUSE
    - Inputs --> Puede tener N componentes PERO han de ser los mismos que los argumentos que recibe el metodo 
    al que se le ha puesto el decorator

Estas listas tienen como elementos OBJETOS Output o Input, en funcion de lo que tenga que tener la lista
Ambos tienen los mismos argumentos
    - component_id -> ID del componenten en el que tiene que escribir (si es OUTPUT) o del que recibe cosas (si es INPUT)
    - component_property -> nombre de la propiedad del elemento al que apunta. 
    SOBREESCRIBE (OVERWRITE, no APPEND) el valor en esa propiedad (si es OUTPUT) o coge los datos de esa (Si es IPNUT)
    Puede coger / volcar datos EN CUALQUIER PROPIEDAD DEL COMPONENTE


# Buenas practicas a la hora de manejar los datos
- Hacer una copia del DF inicial y luego ya hacer los filtros, agrupaciones, sumas... 

"""

"""
# OBJETIVO INICIAL: 
crear una página que tenga la diversificacion de mi cartera
Esta diversificación ha de ser por 2 criterios, dinero invertido y valor del stock

Se tiene que crear una página solo con 4 criterios de diversificación:
    - Por empresa
    - Por sector
    - Por pais
    - Por moneda
Y esto es calcular los pesos por los criterios dichos.
Se ha de poder cambiar los pesos cambiando en un DROPDOWN el criterio que indica el peso

Los datos han de leerse de mi cuenta de Google
Tengo que crear un .exe que me abra el Cuadro de Mando

UNA VEZ HECHO ESTO, ya nos podemos poner creativos intentando crear páginas

# DISEÑO INICIAL
Quiero una página que tiene un DIV principal
Este DIV principal se va a dividir en 5
    - Uno que será la primera fila y que cogerá toda la página en la parte superior (Aquí pondre el Título, el dropdown y las notas)
    - En la siguiente fila, tendré que dividirla en 2 y el lado izquierdo será para uno de los criterios y el derecho para el otro 
    - En la siguiente fila, tendré que dividirla en 2 y el lado izquierdo será para uno de los criterios y el derecho para el otro 

 Cada uno de los DIVs con para mostrar la diversificación consistirá en 2 elementos
    - Una tabla
    - Un gráfico de tarta

Los DIVs y la distancia y tamaño de los elementos entre ellos HAN DE SER DINÁMICOS
"""

"""
posibles colores
#3f4057 ---"claro"
#292a3e ---"oscuro"

"""


