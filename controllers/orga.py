# -*- coding: utf-8 -*-
#@PydevCodeAnalysisIgnore

import datetime

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
    
    for v in veranstaltungen + ('vegetarier', 'unterkunft'):
        label=db.anmeldung[v].label
        value = ''
        if (v=='mo_wuerzburg'):
            value = 'Insgesamt : ' + str(db(db.anmeldung[v]==True).count()) + '<br />'
            max_date = Price.referenceDate - datetime.timedelta(days=365*16)
            value += 'Erwachsene : ' + str(db((db.anmeldung[v]==True) & (db.anmeldung.geburtsdatum <= max_date)).count()) + '<br />'
            min_date = max_date
            max_date = Price.referenceDate - datetime.timedelta(days=365*12)
            value += 'Kind bis 16 J. : ' + str(db((db.anmeldung[v]==True) & (db.anmeldung.geburtsdatum > min_date) & (db.anmeldung.geburtsdatum <= max_date)).count()) + '<br />'
            min_date = max_date
            max_date = Price.referenceDate - datetime.timedelta(days=365*6)
            value += 'Kind bis 12 J. : ' + str(db((db.anmeldung[v]==True) & (db.anmeldung.geburtsdatum > min_date) & (db.anmeldung.geburtsdatum <= max_date)).count()) + '<br />'
            min_date = max_date
            value += 'Kind bis 6 J. : ' + str(db((db.anmeldung[v]==True) & (db.anmeldung.geburtsdatum > min_date)).count())
        elif (v=='mi_essen_wanderung'):
            count = db.anmeldung[v].count()
            for row in db(db.anmeldung.mi_wanderung==True).select(db.anmeldung[v], count, groupby=db.anmeldung[v]):
                value += db.anmeldung[v].represent(row.anmeldung[v], None) + ' : ' + str(row[count]) + '<br />'
        elif (v=='fr_essen'):
            count = db.anmeldung[v].count()
            for row in db(db.anmeldung.fr_regensburg==True).select(db.anmeldung[v], count, groupby=db.anmeldung[v]):
                value += db.anmeldung[v].represent(row.anmeldung[v], None) + ' : ' + str(row[count]) + '<br />'
        elif (v=='do_minigolf'):
            value = 'Insgesamt : ' + str(db(db.anmeldung[v]==True).count()) + '<br />'
            max_date = Price.referenceDate - datetime.timedelta(days=365*12)
            value += 'Erwachsene : ' + str(db((db.anmeldung[v]==True) & (db.anmeldung.geburtsdatum <= max_date)).count()) + '<br />'
            min_date = max_date
            value += 'Kind bis 12 J. : ' + str(db((db.anmeldung[v]==True) & (db.anmeldung.geburtsdatum > min_date)).count())
        elif (db.anmeldung[v].type == 'boolean'):
            value = db(db.anmeldung[v]==True).count()
        elif (db.anmeldung[v].type == 'integer'):
            count = db.anmeldung[v].count()
            for row in db().select(db.anmeldung[v], count, groupby=db.anmeldung[v]):
                value += db.anmeldung[v].represent(row.anmeldung[v], None) + ' : ' + str(row[count]) + '<br />'
        else:
            value = '??'
        eventlist.append((label, value))
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
                  subject='Europatreffen 2016: Bestätigung der Zahlung / Confirmation of payment',
                  message=message,
                  cc=['anmeldung@europatreffen2016.eu']
                  )
        
        redirect(URL("payment"))
        
    return dict(form=form)
    
@auth.requires_membership('orgateam')
def birthdays():
    response.subtitle = 'Geburtstage während des Europatreffens'
    return dict()

@auth.requires_membership('orgateam')
def districtGroups():
    count=db.anmeldung.bezirk.count()
    rows = db().select(db.anmeldung.bezirk, 
                       count,
                       orderby=db.anmeldung.bezirk,
                       groupby=db.anmeldung.bezirk)
    return dict(rows=rows)

@auth.requires_membership('orgateam')
def countries():
    count=db.anmeldung.land.count()
    rows = db().select(db.anmeldung.land, 
                       count,
                       orderby=~count,
                       groupby=db.anmeldung.land)
    return dict(rows=rows)

@auth.requires_membership('orgateam')
def verlauf():
    response.view = 'orga/statistics.html'
    return dict(url=URL('statistik','anmeldungen'))

# Review personal data
@auth.requires_membership('orgateam')
def personalData():
    response.subtitle = 'Persönliche Daten'
    db.anmeldung.sprache.readable = True
    db.anmeldung.sprache.writable = True
    grid = SQLFORM.grid(db.anmeldung, create=False,
                        fields=[db.anmeldung.vorname, db.anmeldung.nachname, db.anmeldung.email, 
                                db.anmeldung.bezirk, db.anmeldung.kommentar],
                        maxtextlength=100,
                        paginate=500,
                        deletable=auth.has_membership('darfalles'),
                        editable=auth.has_membership('darfalles'))
    return dict(grid=grid)
