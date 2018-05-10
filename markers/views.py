from django.shortcuts import render
import requests
from django.http import HttpResponse

import xml.etree.cElementTree as et
import pandas as pd
import json as json

import datetime as dt
import pdb
import PIL,PIL.Image
import io
import pylab


import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import pygal
from pygal.style import Style
import os
import webbrowser




xml_path = "E:\python\zips\maps\osi_pi_new.xml"

parsedXML = et.parse( xml_path)
print(parsedXML)

def getvalueofnode(node):
    #return node text or None
    return node.text if node is not None else None

def read_xml():
    dfcols = ['Time', 'Temp', 'Lat','Long']
    df_xml = pd.DataFrame(columns=dfcols)
    
    df_json_cols = ['Tag','Lat','Long']
    df_json_xml = pd.DataFrame(columns=df_json_cols)
    
    l_tag_dict = {}

    for node in parsedXML.getroot():
        tag = node.find('Tag')
        time = node.find('Time')
        temp = node.find('Temperature')
        lat = node.find('Latitude')
        long = node.find('Longitude')
              
        tag_val =  getvalueofnode(tag)
        
        pd_series =  pd.Series([getvalueofnode(time),
                       getvalueofnode(temp),    getvalueofnode(lat), 
                       getvalueofnode(long)], index=dfcols)
       
        
        if tag_val in l_tag_dict:
            l_tag_dict[tag_val] = l_tag_dict[tag_val].append( pd_series ,ignore_index=True)
            
          
        else:
            l_tag_dict[tag_val] = pd.DataFrame(columns=dfcols)
            l_tag_dict[tag_val] = l_tag_dict[tag_val].append( pd_series,ignore_index=True)
            df_json_xml = df_json_xml.append(
                     pd.Series([getvalueofnode(tag), getvalueofnode(lat),
                       getvalueofnode(long)], index=df_json_cols),
                    ignore_index=True)
       
    return l_tag_dict, df_json_xml  
    

def displaygraph(df_xml):
    graph = pygal.Line(x_label_rotation=-20)
    graph.title='Tempature over Time' 
    graph.x_labels = pd.to_datetime(df_xml['Time']) 
    graph.add('Temp', pd.to_numeric(df_xml['Temp']) ) 
    #graph.colors = '#53A0E8'
    graph_data = graph.render_data_uri()
    
    return graph_data


def bargraphdata(df_xml):
    # custom_style = Style(
    #         colors=('#B256AF','#A181A0','#511FA8','#2C3BC7','#E80080', '#404040', '#9BC850','#463636','#4AB31D','#1E1F2A','#82859E'))
    custom_style = Style(
        colors=('#E853A0', '#E8537A', '#E95355', '#E87653', '#E89B53'))
    graph = pygal.Bar(fill=True, interpolate='cubic',x_label_rotation=-20, style=custom_style)
    

    graph.x_labels = pd.to_datetime(df_xml['Time']) 
    graph.add('Temp', pd.to_numeric(df_xml['Temp']) ) 
    graph_data = graph.render_data_uri()
    
    return graph_data



def home(request):
    xml_dict,df_json_xml  = read_xml()
    jsonDf = df_json_xml.to_json(orient='records')

    if request.method == "POST":
        tag_name = request.POST['tag_name']
        
    else:
        tag_name = 'CDT154'
        
    graph_data = displaygraph(xml_dict[tag_name])
    bargraph = bargraphdata(xml_dict[tag_name])

    return render(request, 'markers/index.html',     {  'xml_df': jsonDf,
                                                        'graphdata' :  graph_data,  
                                                        'tag_value':tag_name,
                                                        'bargraph' : bargraph,                                                      
                                                        'api_key': 'AIzaSyCp4hT94RNU8pfidFmArTA-2G9oyWHnrUY'})
        
























































''' def displaygraph(request):

    df_xml  = read_xml()
   
    t = pd.to_datetime(df_xml['Time'])
 
    s = pd.to_numeric(df_xml['Temp'])
    plot(t, s, linewidth=1.0)
    xlabel('time (s)')
    ylabel('Temp (C)')
    title('Temperature Vs Time Graph')
    grid(True)  
    buffer = io.BytesIO()
    canvas = pylab.get_current_fig_manager().canvas
    canvas.draw()
    pilImage = PIL.Image.frombytes("RGB", canvas.get_width_height(), canvas.tostring_rgb())
    pilImage.save(buffer, "PNG")
    pylab.close() 
    response = HttpResponse(buffer.getvalue(), content_type="image/png")
    return response '''
