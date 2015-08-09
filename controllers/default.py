# -*- coding: utf-8 -*-
#@PydevCodeAnalysisIgnore

import datetime

def index():
    redirect(URL('create'))

def create():
    response.menu = None

    db.anmeldung.unterkunft.comment = T("Eine Übernachtung in der Halle ist leider nicht möglich.")

    col3 = {}
    limit_erreicht = {}
    for f in db.anmeldung:
        if hasattr(f, 'preis'):
            col3[f.name] = f.preis
        elif hasattr(f, 'comment'):
            col3[f.name] = f.comment
        if hasattr(f, 'limit'):
            if db(f==True).count() >= f.limit[0]:
                limit_erreicht[f.name] = True
                f.label = f.limit[1]                        
    
    form=SQLFORM(db.anmeldung, 
                 formstyle="divs", 
                 submit_button = T('Weiter'),
                 col3 = col3,
                 _id = "create_form")

    if not session.vars is None:
        form.vars = session.vars
        for k in form.vars:
            if isinstance(form.vars[k], datetime.date):
                form.vars[k] = form.vars[k].strftime(T("%d.%m.%Y", lazy=False))
                 
    if form.validate():
        session.vars = form.vars
        session.vars.betrag = gesamtpreis(session.vars)
        redirect(URL("confirm"))
            
    return dict(form=form, limit_erreicht=limit_erreicht)

def confirm():
    if session.vars == None:
        # After the confirmation has been printed, the back button has been used
        redirect('http://www.ostervolleyballturnier.de')
        
    form=FORM(INPUT(_type='submit', _value=T('Daten absenden')))
    form.add_button(T("Korrigieren"),URL("create"))
    
    if form.accepts(request,session):
        db.anmeldung[0] = session.vars; # insert in DB
        
        context = dict(vars=session.vars)
        message = response.render('default/confirmRegistrationMail.html', context)
        mail.send(session.vars.email,
                  subject= T("Anmeldung von %(vorname)s %(nachname)s zum Ostervolleyballturnier 2015") % session.vars,
                  message=message,
                  cc=['anmeldung@ostervolleyballturnier.de']
                  )

        redirect(URL("printConfirmation"))
    return dict(form=form);

def printConfirmation():
    vars = session.vars
    session.vars = None;
    return (dict(vars=vars))

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
