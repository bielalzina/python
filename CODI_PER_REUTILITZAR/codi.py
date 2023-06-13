import datetime

# DATETIME TO STR ("%d-%m-%Y")


def datetimeToStrDMY(data):
    dataStr = data.strftime("%d-%m-%Y")
    return dataStr

# DATETIME TO STR ("%Y-%m-%d")


def datetimeToStrYMD(data):
    dataStr = data.strftime("%Y-%m-%d")
    return dataStr

# DATA STR A OBJECTE DATETIME ("%d-%m-%Y")


def strToDatetimeDMY(data):
    dataObj = datetime.datetime.strptime(data, '%d-%m-%Y')
    return dataObj

# DATA STR A OBJECTE DATETIME ("%Y-%m-%d")


def strToDatetimeYMD(data):
    dataObj = datetime.datetime.strptime(data, '%Y-%m-%D')
    return dataObj

# DATES


avui = datetime.date.today()
dilluns = avui-datetime.timedelta(days=avui.weekday())
divendres = dilluns+datetime.timedelta(days=4)
print(type(avui))
print(avui)
print(dilluns)
print(divendres)
###
print("*** STR D-M-Y ***")
avuiStrDMY = datetimeToStrDMY(avui)
dillunsStrDMY = datetimeToStrDMY(dilluns)
divendresStrDMY = datetimeToStrDMY(divendres)
print(type(avuiStrDMY))
print(avuiStrDMY)
print(dillunsStrDMY)
print(divendresStrDMY)
###
print("*** STR Y-M-D ***")
avuiStrYMD = datetimeToStrYMD(avui)
dillunsStrYMD = datetimeToStrYMD(dilluns)
divendresStrYMD = datetimeToStrYMD(divendres)
print(type(avuiStrYMD))
print(avuiStrYMD)
print(dillunsStrYMD)
print(divendresStrYMD)
###
print("*** DATETIME ***")
avuiObj = strToDatetimeDMY(avuiStrDMY)
dillunsObj = strToDatetimeDMY(dillunsStrDMY)
divendresObj = strToDatetimeDMY(divendresStrDMY)
print(type(avuiObj))
print(avuiObj)
print(dillunsObj)
print(divendresObj)
###
print("*** WEEKDAY() ***")
dataSTR = "09/06/2023"
print(dataSTR)
dataOBJ = datetime.datetime.strptime(dataSTR, '%d/%m/%Y')
print(type(dataOBJ))
print(dataOBJ)
print(dataOBJ.weekday())
print("OBTENIM DATA DILLUNS A PARTIR DE LA DATA ANTERIOR")
dillunsOBJ = dataOBJ-datetime.timedelta(days=dataOBJ.weekday())
print(dillunsOBJ)
print(dillunsOBJ.weekday())

print()
print("***************************************")
print()

for fila in range(0, 5):
    for columna in range(0, 6):
        print("fila: "+str(fila)+" - columna: "+str(columna))
    print("----------------------")

print()


# PASSAM RESPOSTA QUERY A ARRAY
llistaReserves = [
    {'data': datetime.datetime(2023, 6, 5, 15, 0),
     'tipo': 'Coberta',
     'nom': 'Miquel',
     'llinatges': 'Mir'},
    {'data': datetime.datetime(2023, 6, 5, 16, 0),
     'tipo': 'Coberta',
     'nom': 'Miquel',
     'llinatges': 'Mir'},
    {'data': datetime.datetime(2023, 6, 9, 17, 0),
     'tipo': 'Coberta',
     'nom': 'Miquel',
     'llinatges': 'Mir'},
    {'data': datetime.datetime(2023, 6, 7, 16, 0),
     'tipo': 'Coberta',
     'nom': 'Miquel',
     'llinatges': 'Mir'},
    {'data': datetime.datetime(2023, 6, 8, 19, 0),
     'tipo': 'Coberta',
     'nom': 'Miquel',
     'llinatges': 'Mir'},
    {'data': datetime.datetime(2023, 6, 6, 15, 0),
     'tipo': 'Coberta',
     'nom': 'Joana',
     'llinatges': 'Pons'},
    {'data': datetime.datetime(2023, 6, 6, 18, 0),
     'tipo': 'Exterior',
     'nom': 'Joana',
     'llinatges': 'Pons'},
    {'data': datetime.datetime(2023, 6, 5, 15, 0),
     'tipo': 'Exterior',
     'nom': 'Laura ',
     'llinatges': 'Gonzalez'}
]


for reserva in llistaReserves:
    print(reserva['data'])
    print(reserva['data'].weekday())
    print(reserva['data'].hour)

print()

vector = []
for registre in range(0, 5):
    registreTemp = []
    for camp in range(0, 6):
        campTemp = ""
        for reserva in llistaReserves:
            if reserva['data'].weekday() == registre and reserva['data'].hour == camp+15:
                campTemp = campTemp + reserva['nom']+" "+reserva['llinatges']
                campTemp = campTemp + " ["+reserva['tipo']+"] "
        registreTemp.append(campTemp)
    vector.append(registreTemp)

print(vector)
