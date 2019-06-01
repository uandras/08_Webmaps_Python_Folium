import pandas as pd
import folium as flm

df1=pd.read_csv("Volcanoes.txt")
map=flm.Map(location=[40.796829, -73.972661],zoom_start=6)#777 west end avenue...:-)
#create a map object
# Approach 1: add features to the map object:
#for i,j,k in zip(df1["LAT"],df1["LON"],df1["NAME"]):
#    map.add_child(flm.Marker(location=[i,j],popup=k, icon=flm.Icon(color="red")))

# Approach 2: create a feature group, and add feature(s) to this, then add featuregroup to map object (easier layering, better readable code)
# fg=flm.FeatureGroup(name="Volcanoes")
# for i,j,k in zip(df1["LAT"],df1["LON"],df1["NAME"]):
#     fg.add_child(flm.Marker(location=[i,j],popup=k, icon=flm.Icon(color="purple")))
# map.add_child(fg)
# map.save("Map1.html")

# popups with html
html = """<h4>Volcano information:</h4>
<p>Name: %s</p>
<p>Height: %s m</p>
"""
fg2=flm.FeatureGroup(name="Volcanoes")
for i,j,k,l in zip(df1["LAT"],df1["LON"],df1["NAME"],df1["ELEV"]):
    iframe=flm.IFrame(html=html %(k,str(l)),width=200,height=100)
    if l<2000:
        col="green"
    elif l<3000:
        col="orange"
    else :
        col="red"
    fg2.add_child(flm.Marker(location=[i,j],popup=flm.Popup(iframe),tooltip=k, icon=flm.Icon(color=col)))

# adding a json polygon layer
# a data-nak egy file object-ből beolvasott string-et kell átadni
# style_function-nal tudunk pl. színezni, lambda fv-ek segítségével
fg3=flm.FeatureGroup(name="Polygons")
fg3.add_child(flm.GeoJson(data=open("world.json","r",encoding="utf-8-sig").read(),
                          style_function=lambda x:{"fillColor":"green" if x["properties"]["POP2005"]<1000000
                                                   else "orange" if 10000000<=x["properties"]["POP2005"]<40000000
                                                   else "red"}))
map.add_child(fg2)
map.add_child(fg3)

# adding layer control to the map
# MUST BE AFTER feature group added already to the map
map.add_child(flm.LayerControl())

map.save("Map1_htmlpopup.html")
