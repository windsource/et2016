# -*- coding: utf-8 -*-
#@PydevCodeAnalysisIgnore

#########################################################################
## This controller provides functionality for the orga team only.
#########################################################################

# Show available options
@auth.requires_membership('orgateam')
def index():
    redirect(URL('list'))


# Show list of participants
@auth.requires_membership('orgateam')
def list():
    response.subtitle = 'Teilnehmerliste'
    db.anmeldung.anmeldedatum.readable = True
    db.anmeldung.betrag.readable = True
    db.anmeldung.betrag.writable = True
    db.anmeldung.bezahlt.readable = True
    db.anmeldung.bezahlt.writable = True
    db.anmeldung.zahlungsdatum.readable = True
    db.anmeldung.zahlungsdatum.writable = True
    db.anmeldung.sprache.readable = True
    db.anmeldung.sprache.writable = True
    grid = SQLFORM.grid(db.anmeldung, create=False,
                        deletable=auth.has_membership('darfalles'),
                        editable=auth.has_membership('darfalles'))
    return dict(grid=grid)

# Show number of participants for each event
@auth.requires_membership('orgateam')
def events():
    response.subtitle = 'Veranstaltungen'
    eventlist = []

    teilnehmer = db(db.anmeldung).count()
    gesamtSoll = 0
    gesamtIst  = 0
    
    for v in veranstaltungen + ('vegetarier'):
        label=db.anmeldung[v].label
        countAdult=db((db.anmeldung[v]==True) & (db.anmeldung.kind==False)).count()
        countChild=db((db.anmeldung[v]==True) & (db.anmeldung.kind==True)).count()
        eventlist.append((label,countAdult+countChild,countAdult,countChild))
        
    return locals()

# Show the payments for each participant
@auth.requires_membership('orgateam')
def payment():
    response.subtitle = 'Zahlungen'
    rows = db().select(db.anmeldung.ALL)
    return locals()

# Change payment for a single participant
@auth.requires(auth.has_membership('darfalles') or auth.has_membership('kasse'))
def changePayment():
    response.subtitle = 'Zahlung ändern'
    record = db.anmeldung(request.args(0)) or redirect(URL('index'))
    db.anmeldung.vorname.writable = False
    db.anmeldung.nachname.writable = False
    db.anmeldung.betrag.readable = True
    db.anmeldung.betrag.writable = False
    db.anmeldung.bezahlt.readable = True
    db.anmeldung.bezahlt.writable = True
    db.anmeldung.zahlungsdatum.readable = True
    db.anmeldung.zahlungsdatum.writable = True

    form=SQLFORM(db.anmeldung, record, 
                 fields=['vorname', 'nachname', 'betrag', 
                         'bezahlt', 'zahlungsdatum'])

    if form.process().accepted:
        context = dict(vorname=record.vorname,
                       nachname=record.nachname,
                       bezahlt=form.vars.bezahlt)
        message = response.render('orga/confirmPaymentMail.txt', context)
        mail.send(record.email,
                  subject='Ostervolleyballturnier 2015: Bestätigung der Zahlung',
                  message=message,
                  cc=['anmeldung@ostervolleyballturnier.de']
                  )
        
        redirect(URL("payment"))
        
    return dict(form=form)
    
@auth.requires_membership('orgateam')
def birthdays():
    response.subtitle = 'Geburtstage während des Ostertreffens'
    return dict()

@auth.requires_membership('orgateam')
def bezirke():
    response.view = 'orga/statistics.html'
    return dict(url=URL('statistik','bezirke'))

@auth.requires_membership('orgateam')
def verlauf():
    response.view = 'orga/statistics.html'
    return dict(url=URL('statistik','anmeldungen'))
