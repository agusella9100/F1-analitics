############ Ejemplos introductorios de la libreria Fastf1 y visualización de datos ###########

'''
Ejemplos de como cargar los datos, visulaizar los campos de leventos dentro del dataset
/ dataframe de pandas de fastf1. Para dejarlo simple voy a solo usar los datos de la sesion de Baku 2024 "gran premio de azerbayan"
'''


#Importacion de librerias a utilizar ###################################
from pathlib import Path
import fastf1 as dbf1
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection


# Crear la carpeta de cache en la raíz del proyecto (proyecto/`cache`)
cache_dir = Path(__file__).resolve().parent.parent / 'cache'
cache_dir.mkdir(parents=True, exist_ok=True)
# Habilitar cache apuntando al directorio creado
dbf1.Cache.enable_cache(str(cache_dir))



#session = dbf1.get_session(2021, 7, 'Q')  # 7ma carrera, sesión de clasificación
#print(session.name)  # 'Qualifying'
#print(session.date)  # fecha y hora

# Obtengo el evento o mas facil de interpretar, el GP o fin de semana, quiero el de baku 2024
gp_bk24 = dbf1.get_event(2024,"baku")
print(f"El GP seleccionado es el de {gp_bk24['EventName']}")

# ahora cargo los resultados de la carrera principal a partir del evento

session = gp_bk24.get_race()
session.load()  # Cargo los datos de la sesión
print(session.results.columns)
print(session.results.iloc[0:10][['Abbreviation', 'Time', 'Position', 'Points']])  # Muestro las primeras 10 filas con columnas seleccionadas

# vueltas de la sesion
laps = session.laps
print(laps.columns)

#ahora veo las vueltas de Colapinto.
laps_colapinto = laps.pick_driver('COL')

#saco la telemetria
telemetria_colapinto = laps_colapinto.get_telemetry()
tlm_c_x = telemetria_colapinto['X']
tlm_c_y = telemetria_colapinto['Y']
tlm_c_speed = telemetria_colapinto['Speed']  # Velocidad en km/h Con este valor voy a graduar los colores de velocidad.
tlm_c_brake = telemetria_colapinto['Brake']  # Valor booleano de si está frenando o no

# genero segmentos para poder colorear la linea segun velocidad
nodos = np.array([tlm_c_x, tlm_c_y]).T.reshape(-1, 1, 2) # las dimensiones son (N, 1, 2), lo hago una tupla
segmentos = np.concatenate([nodos[:-1], nodos[1:]], axis=1) # la cantidad de segmentos son N-1


#hago la figura para plotear

fig, ax = plt.subplots(sharex=True, sharey=True, figsize=(12, 6.75))
fig.suptitle(f' {session.event} - COL - Speed', size=24, y=0.97)

# Adjust margins and turn of axis
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.12)
ax.axis('off')


# After this, we plot the data itself.
# Create background track line
ax.plot(tlm_c_x, tlm_c_y,
        color='black', linestyle='-', linewidth=16, zorder=0)

# Normalizo segun velocidades de colapa para hacer la graduacion de colores de 0 a 1
colormap = mpl.cm.plasma
norm = plt.Normalize(tlm_c_speed.min(), tlm_c_speed.max())
lc = LineCollection(segmentos, cmap=colormap, norm=norm,
                    linestyle='-', linewidth=5)

# Set the values used for colormapping
lc.set_array(tlc_c_speed)

# Merge all line segments together
line = ax.add_collection(lc)


# Finally, we create a color bar as a legend.
cbaxes = fig.add_axes([0.25, 0.05, 0.5, 0.05])
normlegend = mpl.colors.Normalize(vmin=color.min(), vmax=color.max())
legend = mpl.colorbar.ColorbarBase(cbaxes, norm=normlegend, cmap=colormap,
                                   orientation="horizontal")


# Show the plot
plt.show()