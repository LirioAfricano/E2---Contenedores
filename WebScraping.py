from bs4 import BeautifulSoup
import os
import openpyxl
import pandas
import re
import requests
import urllib.request
import xlsxwriter

def Todo(opc):
    ##############################
    #Creacion de el Subdirectorio#
    ##############################
    dir = input("\nEscribe el nombre del directorio: ")
    if os.path.isdir(dir):
        print("El directorio existe")
        exit()
    else:
        os.system("mkdir " + dir)                                               #creacion de directorio con el nombre almacenado en dir
        
        
        ############################################################################################################################################################################
        ############################################################################################################################################################################
        ##Webscraping, uso de Openweather y creacion de un archivo Excel con la informacion almacenada (Basicamente todo los puntos que faltan que no estan en los otros archivos)##
        ############################################################################################################################################################################
        ############################################################################################################################################################################
        
        
        ##########################################################################
        #Lectura de las urls del archivo .txt para la obtencion de la informacion#
        ##########################################################################
        f = open(opc, 'r')
        lines = [line for line in f.readlines()]                                        #linea por linea va almacenandolo en una lista
        lines = ' '.join(lines).replace('\n','').split()                                #remueve el "\n" que viene al final del url
        for i in lines:                                                                 #ciclo for para que vaya ciclando por todos los elementos de la lista
                page = requests.get(i)                                                  #hace un request con el url         
                print('\nHTML Status Code: ', page.status_code, '\n')                   #imprime el codigo de estatus html
                soup = BeautifulSoup(page.content,"html.parser")
                

                #######################
                #Expresiones Regulares#
                #######################
                ListaDeCorreos = re.findall('\S+@\S+', str(soup))                       #expresion regular para encontrar el correo, generar una lista
                correo = ListaDeCorreos[0]                                              #obtenemos el primer objeto de la lista en el cual se encuentra el correo con alguna basura de texto al inicio
                SoloElCorreo = correo[13:-1]                                            #hacemos slicing para remover el texto indeseado y obtener el correo
                
                
                ####################################
                #Obtencion del titulo de la noticia#
                ####################################
                BusquedaDeTitulos = soup.find_all('h3', class_ = 'gdlr-blog-title')     #busca en la pagina web el tag html "h3" de la clase "gdlr-blog-title"
                TituloDeLaNoticia = list()                                              #lista donde almacenaremos los titulos de la noticia
                count = 0                                                               #contador igual a 0
                for i in BusquedaDeTitulos:                                             #iterara todas las BusquedaDeTitulos que encontro
                    if count < 3:                                                       #en el ciclo solamente guardaremos los primeros tres titulos de las noticias
                        TituloDeLaNoticia.append(i.text)                                #se adjuntara solamente al texto
                    else:
                        break                                                           #termina el ciclo
                    count += 1                                                          #incremento del contador en 1
                #print(TituloDeLaNoticia,'\n')                                          #imprime la lista y la longitud de esta
                
                
                ###################################
                #Obtencion del texto de la noticia#
                ###################################
                BusquedaDeTexto = soup.find_all('div', class_ = 'gdlr-blog-content')    #busca en la pagina web el tag html "div" de la clase "gdlr-blog-content"
                TextoDeLaNoticia = list()                                               #lista donde almacenaremos el resumen de la noticia
                count = 0                                                               #contador igual a 0
                for i in BusquedaDeTexto:                                               #iterara todas las BusquedaDeTexto que encontro
                    if count < 3:                                                       #en el ciclo solamente guardaremos las primeras tres descripciones de las noticias
                        TextoDeLaNoticia.append(i.text)                                 #se hara un append solamente al texto
                    else:                                                               
                        break                                                           #termina el ciclo
                    count += 1                                                          #incremento del contador en 1
                #print(TextoDeLaNoticia,'\n')                                           #imprime la lista y la longitud de esta
                
                
                ############################################
                #Obtencion de los texto de la tabla general#
                ############################################
                TablaGeneral = list()
                NombreEquipo = list()                                                   #listas donde almacenaremos los titulos de la noticia
                PG = list()
                PE = list()
                PP = list()
                Puntos = list()
                
                BusquedaPuntos = soup.find_all('td')                                    #busca en la pagina web el tag html "td" de la clase "gdlr-table-team"
                for i in BusquedaPuntos:                                                #iterara todas las BusquedaPuntos que encontro
                    TablaGeneral.append(i.text)                                         #se hara un append solamente al texto

                NombreEquipo = TablaGeneral[0:75:5]
                PG = TablaGeneral[1:75:5]
                PE = TablaGeneral[2:75:5]                                               #se hace slicing para obtener los datos especificos y almacenarlos en la lista especifica
                PP = TablaGeneral[3:75:5]
                Puntos = TablaGeneral[4:75:5]
                
                #print(NombreEquipo,'\n',PG,'\n',PE,'\n',PP,'\n', Puntos,'\n')
                
                
                ###############################################################################
                #Obtencion de las imagenes de la noticias e imagenes de los equipos de la liga#
                ###############################################################################
                URLImagenDeLaNoticia = list()                                           #lista donde almacenaremos la imagen de la noticia
                count = 1
                for i in soup.find_all('img'):                                          #ciclo donde busca todas las imagenes en soup
                    if count < 4:                                                       #condicional el cual iterara tres veces para agarrar las primeras tres imagenes de las noticias
                        if i['src'].endswith("750x360.jpg") == True:                    #condicional que busca la url o urls que terminen con "750x360.jpg" para descargar solamente esas (queremos descargar solamente esas porque son las miniaturas de las noticias que agarramos)
                            src = i.get('src')                                          #obtiene el tag source donde esta el link de la imagen
                            NombreCompleto = "Noticia" + str(count) + ".jpg"            #asignacion de nombre y tipo de archivo a la imagen
                            Destino = dir + "/" + NombreCompleto                        #creacion del destino usando dir y el nombre
                            urllib.request.urlretrieve(src, Destino)                    #recupera la imagen y la coloca en destino
                            URLImagenDeLaNoticia.append(src)                            #adjunta la url a la lista
                            count += 1
                
                URLLogosLiga = list()                                                                                       #lista donde almacenaremos la imagen de la noticia
                count = 1                                                                                                   #contador = 1
                for i in soup.find_all('img'):                                                                              #ciclo donde busca todas las imagenes en soup
                    if count < 17:                                                                                          #ciclo el cual iterara 16 veces para obtener el logo del equipo que haremos Webscraping y de los 16 equipos de la liga sanmarinense
                        if i['src'].startswith("http://www.trepenne.com/wp-content/uploads/201") == True:                   #condicional que busca en el url que termine con "750x360.jpg" para descargar solamente esas (queremos descargar solamente esas porque son las miniaturas de las noticias que agarramos)
                            srcc = i.get('src')                                                                             #obtiene el tag source donde esta el link de la imagen
                            if count == 1:                                                                                  #hicimos esta condicional porque si no lo haciamos tendriamos en las imagenes de la tabla general el logo repetido del equipo de S.P. Tre Penne
                                NombreCompletoo = "S.P. Tre Penne.png"                                                      #asignacion de nombre y tipo de archivo a la imagen
                                Destinoo = dir + "/" + NombreCompletoo                                                      #creacion del destino usando dir y el nombre
                                urllib.request.urlretrieve(srcc, Destinoo)                                                  #recupera la imagen y la coloca en destino
                            else:
                                NombreCompletoo = "Logo" + str(count - 1) + ".png"                                          #asignacion de nombre y tipo de archivo a la imagen
                                Destinoo = dir + "/" + NombreCompletoo                                                      #creacion del destino usando dir y el nombre
                                urllib.request.urlretrieve(srcc, Destinoo)                                                  #agarra el archivo
                                URLLogosLiga.append(srcc)                                                                   #adjunta el url a la lista
                            count += 1
                    else:
                        break
                #print(URLImagenDeLaNoticia,'\n\n',URLLogosLiga,'\n')
        f.close()


        #############
        #Openweather#
        #############
        
        #creacion de lista con las urls con los lugares donde jugaran (3 lugares)
        url = ['http://api.openweathermap.org/data/2.5/weather?q=Domagnano,SM&appid=6df668897ea3c086709fe9da419f9521&units=metric', 'http://api.openweathermap.org/data/2.5/weather?q=Castello di San Marino Città,SM&appid=6df668897ea3c086709fe9da419f9521&units=metric', 'http://api.openweathermap.org/data/2.5/weather?q=Castello di San Marino Città,SM&appid=6df668897ea3c086709fe9da419f9521&units=metric']
        Factores = ["Ciudad", "Pais", "Temperatura", "Velocidad del Viento", "Latitud", "Longitud", "Descripcion"] #lista de descripciones del clima
        ClimaPartido1 = list()
        ClimaPartido2 = list()  #listas donde se almacenaran los datos del tiempo de los partidos
        ClimaPartido3 = list()
        
        count = 1                                                       #contador comineza en 1
        for i in url:                                                   #iteraremos todos los urls para extraer los datos que estan en formato JSON
            if count < 4:
                res = requests.get(i)                                   #pagina por pagina se hara el request a la url
                data = res.json()                                       #sacamos la informacion que esta en formato JSON del clima

                #aqui asignaremos los valores especificos que sacamos de la url para luego asignalos a la correspondiente lista
                city = data['name']
                country = data['sys']['country']
                temp = data['main']['temp']
                wind_speed = data['wind']['speed']
                latitude = data['coord']['lat']
                longitude = data['coord']['lon']
                description = data['weather'][0]['description']

                #condicional el cual dependiendo de la iteracion guardara en la lista especificada
                if count == 1:
                    ClimaPartido1.extend((city, country, temp, wind_speed, latitude, longitude, description))
                if count == 2:
                    ClimaPartido2.extend((city, country, temp, wind_speed, latitude, longitude, description))
                if count == 3:
                    ClimaPartido3.extend((city, country, temp, wind_speed, latitude, longitude, description))
            else:
                break
            count += 1
        #print(Factores,'\n',Clima1,'\n',Clima2,'\n',Clima3,'\n')


        ##############################################
        #Creacion de Dataframes y exportacion a Excel#
        ##############################################
        dfNoticias = pandas.DataFrame({"Titulo":TituloDeLaNoticia,"Resumen":TextoDeLaNoticia,"Imagen":URLImagenDeLaNoticia,"Informacion":SoloElCorreo})  #crea el dataframe de las noticias
        print(dfNoticias,'\n')
        
        dfTablaGeneral = pandas.DataFrame({"Equipo":NombreEquipo, "Logo":URLLogosLiga, "Partidos Ganados":PG, "Partidos Empatados":PE, "Partidos Perdidos":PP ,"Puntos":Puntos}, index = list(range(1,16))) #crea el dataframe de la tabla general
        print(dfTablaGeneral,'\n')
        
        dfClima = pandas.DataFrame({"":Factores, "Tre Penne Vs. Cosmos":ClimaPartido1, "Virtus Vs. Tre Penne":ClimaPartido2, "Tre Penne Vs. Domagnano":ClimaPartido3})  #crea el dataframe del clima
        print(dfClima,'\n')
        
        dflist = [dfNoticias, dfTablaGeneral, dfClima]  #crea una lista con los dataframes
        Excelwriter = pandas.ExcelWriter(dir + '/Output.xlsx', engine="xlsxwriter")   #con la funcion ExcelWriter escribiremos los dataframes a Excel
        for i, df in enumerate(dflist):     #aqui iterara la lista de los dataframes y por cada uno de estos creara su correspondida hoja donde se escribira
            df.to_excel(Excelwriter, sheet_name="Hoja" + str(i+1),index=False)
        Excelwriter.save()
