# -*- coding: utf-8 -*-
#@PydevCodeAnalysisIgnore

import pygal
from pygal.style import CleanStyle

import datetime
 
PYGAL_CONFIG = dict(js = [URL('static', 'js/pygal/svg.jquery.js', scheme=True, host=True), 
                          URL('static', 'js/pygal/pygal-tooltips.js', scheme=True, host=True)])

@auth.requires_membership('orgateam')
def bezirke():
    response.headers['Content-Type']='image/svg+xml'
    count=db.anmeldung.bezirk.count()
    rows = db().select(db.anmeldung.bezirk, 
                       count,
                       orderby=db.anmeldung.bezirk,
                       groupby=db.anmeldung.bezirk)
    bezirke = []
    anmeldungen = []
    for row in rows:
        bezirke.append(row['anmeldung.bezirk'].decode('utf-8'))
        anmeldungen.append({'value':row['COUNT(anmeldung.bezirk)'], 
                            'xlink': {'href': URL('orga','list', vars=dict(keywords='anmeldung.bezirk="'+row['anmeldung.bezirk']+'"')), 'target': '_top'}})
        
    bar_chart = pygal.HorizontalBar(order_min=-1, 
                                    show_legend=False,
                                    height=400,
                                    style=CleanStyle,
                                    **PYGAL_CONFIG)
    bar_chart.title = "Anmeldungen pro Bezirk"
    bar_chart.x_labels = reversed(bezirke)
    bar_chart.add('Anmeldungen', reversed(anmeldungen))
    return bar_chart.render()

@auth.requires_membership('orgateam')
def anmeldungen():
    response.headers['Content-Type']='image/svg+xml'
    
    rows=db(db.anmeldung).select(db.anmeldung.anmeldedatum)
    dateList = []
    for (i,row) in enumerate(rows,1):
        theDate = row.anmeldedatum.date()
        theDate.__format__("%d.%m.%Y")
        if len(dateList)==0 or dateList[-1][0] != theDate:
            dateList.append((theDate,i))
        else:
            dateList = dateList[0:-1] + [(theDate,i)]
        
    datey = pygal.DateY(x_label_rotation=20, show_legend=False, height=400, style=CleanStyle, **PYGAL_CONFIG)
    datey.title = "Anmeldungen im zeitlichen Verlauf"
    datey.add("Anmeldungen", dateList)
    return datey.render()
   
  
