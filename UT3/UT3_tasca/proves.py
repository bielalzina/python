import datetime

# AVUI
print("AVUI")

data=datetime.datetime.now()
print(data)
diaSetmana=int(data.strftime("%w"))
print(type(diaSetmana))
print(diaSetmana)
diaIniciSetmana=data-datetime.timedelta(days=(diaSetmana-1))
print(diaIniciSetmana)
print(diaIniciSetmana.strftime("%Y-%m-%d"))
print()


# DILLUNS
print("DILLUNS")
data=datetime.datetime(2022,12,12)
print(data)
diaSetmana=int(data.strftime("%w"))
print(type(diaSetmana))
print(diaSetmana)
diaIniciSetmana=data-datetime.timedelta(days=(diaSetmana-1))
print(diaIniciSetmana)
print(diaIniciSetmana.strftime("%Y-%m-%d"))
print()


# DIMARTS
print("DIMARTS")
data=datetime.datetime(2022,12,13)
print(data)
diaSetmana=int(data.strftime("%w"))
print(type(diaSetmana))
print(diaSetmana)
diaIniciSetmana=data-datetime.timedelta(days=(diaSetmana-1))
print(diaIniciSetmana)
print(diaIniciSetmana.strftime("%Y-%m-%d"))
print()


# DIMECRES
print("DIMECRES")
data=datetime.datetime(2022,12,14)
print(data)
diaSetmana=int(data.strftime("%w"))
print(type(diaSetmana))
print(diaSetmana)
diaIniciSetmana=data-datetime.timedelta(days=(diaSetmana-1))
print(diaIniciSetmana)
print(diaIniciSetmana.strftime("%Y-%m-%d"))
print()


# DIJOUS
print("DIJOUS")
data=datetime.datetime(2022,12,15)
print(data)
diaSetmana=int(data.strftime("%w"))
print(type(diaSetmana))
print(diaSetmana)
diaIniciSetmana=data-datetime.timedelta(days=(diaSetmana-1))
print(diaIniciSetmana)
print(diaIniciSetmana.strftime("%Y-%m-%d"))
print()


# DIVENDRES
print("DIVENDRES")
data=datetime.datetime(2022,12,16)
print(data)
diaSetmana=int(data.strftime("%w"))
print(type(diaSetmana))
print(diaSetmana)
diaIniciSetmana=data-datetime.timedelta(days=(diaSetmana-1))
print(diaIniciSetmana)
print(diaIniciSetmana.strftime("%Y-%m-%d"))
print()


# DISSABTE
print("DISSABTE")
data=datetime.datetime(2022,12,17)
print(data)
diaSetmana=int(data.strftime("%w"))
print(type(diaSetmana))
print(diaSetmana)
diaIniciSetmana=data-datetime.timedelta(days=(diaSetmana-1))
print(diaIniciSetmana)
print(diaIniciSetmana.strftime("%Y-%m-%d"))
print()

# DIUMENGE
print("DIUMENGE")
data=datetime.datetime(2022,12,18)
print(data)
diaSetmana=int(data.strftime("%w"))
print(type(diaSetmana))
print(diaSetmana)
if diaSetmana==0:
    diaIniciSetmana=data-datetime.timedelta(days=6)
else:
    diaIniciSetmana=data-datetime.timedelta(days=(diaSetmana-1))
print(diaIniciSetmana)
print(diaIniciSetmana.strftime("%Y-%m-%d"))
diaFiSetmana=diaIniciSetmana+datetime.timedelta(days=4)
print(diaFiSetmana)
print(diaFiSetmana.strftime("%Y-%m-%d"))
diaFiSetmanaSQL=diaIniciSetmana+datetime.timedelta(days=5)
print(diaFiSetmanaSQL)
print(diaFiSetmanaSQL.strftime("%Y-%m-%d"))
print()

for fila in range (0,5):
    print("fila: "+str(fila))
    for columna in range (0,6):
        print("columna: "+str(columna))



# NOMES DATA
print("NOMES DATA")

data=datetime.datetime.now()
print(data)
nomesData=data.date()
print(nomesData)