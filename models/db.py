#@PydevCodeAnalysisIgnore

import datetime
from applications.et2016.modules.countries import *

db = DAL(*DAL_ARGS, **DAL_KEYWORDS)


from gluon.tools import *
#auth = Auth(db,cas_provider = 'https://apps.windfeuer.de/signon/default/user/cas')
auth = Auth(db)
auth.define_tables()
auth.settings.actions_disabled.append('register')

crud = Crud(db)

mail = Mail()
mail.settings.server = MAIL_SERVER
mail.settings.sender = MAIL_SENDER
mail.settings.login = MAIL_LOGIN

#########################################################################
## language settings
#########################################################################
try:
    # the following call causes an exeption if the language file given by the accepted browser languages is not found
    # we have to catch it
    T.set_current_languages('de', 'de-de')
except:
    pass
if request.vars['lang'] is not None:
    session.language = request.vars['lang']
if session.language is not None:
    T.force(session.language)


db.define_table('anmeldung',
   Field('vorname',
         requires = IS_NOT_EMPTY(error_message=T('Bitte einen Vornamen eingeben')),
         label=T('Vorname')),
   Field('nachname',
         requires = IS_NOT_EMPTY(error_message=T('Bitte einen Nachnamen eingeben')),
         label=T('Nachname')),
   Field('email',
         requires = IS_EMAIL(error_message=T('Bitte eine Emailadresse eingeben')),
         label=T('Email')),
   Field('telefon',
         requires = IS_NOT_EMPTY(error_message=T('Bitte eine Mobiltelefonnummer eingeben')),
         label=T('Mobiltelefon')),
   Field('strasse', label=T('Straße und Hausnummer'),
         requires = IS_NOT_EMPTY(error_message=T('Bitte eine Straße eingeben'))),
   Field('plz',
         requires = IS_NOT_EMPTY(error_message=T('Bitte eine Postleitzahl eingeben')),
         label=T('PLZ')),
   Field('ort',
         requires = IS_NOT_EMPTY(error_message=T('Bitte einen Ort eingeben')),
         label=T('Ort')),
   Field('land',
         default = 'Germany',
         requires = IS_IN_SET(COUNTRIES),
         label=T('Land')),
   Field('geburtsdatum', 'date',
         requires = IS_DATE(format='%d.%m.%Y'),
         label=T('Geburtsdatum')),
   Field('vegetarier', 'boolean',
         label=T('Vegetarier')),
   Field('mitglied', 'boolean',
         label=T('Mitglied im KdG bzw. KLM')),
   Field('bezirk',
         label=T('Bezirk (falls Mitglied)')),
   Field('unterkunft', 'integer',
         default=0,
         label=T('Unterkunft (nur Info, hier keine Buchung)')),

   Field('so_barfuesser', 'boolean',
         label=T('Begrüßung im "Barfüßer"')),

   Field('mo_wuerzburg', 'boolean',
         label=T('Tagesausflug nach Würzburg')),

   Field('di_reichsparteitag', 'boolean',
         label=T('Rundgang Reichsparteitagsgelände')),
   Field('di_reichsparteitag_gruppe',
         writable=False, readable=False, label="Gruppe Reichsparteitag",
         requires = IS_EMPTY_OR(IS_IN_SET(['10:00 en', '10:00 de', '13:00 de', '13:30 de'], zero=None))),                                
   Field('di_dokuzentrum', 'boolean',
         label=T('Dokumentationszentrum Reichsparteitagsgelände')),
   Field('di_dokuzentrum_gruppe',
         writable=False, readable=False, label="Gruppe Dokuzentrum",
         requires = IS_EMPTY_OR(IS_IN_SET(['10:00 de', '10:15 de', '13:00 de', '13:30 en', '13:45 de']))),
   Field('di_rangierbahnhof', 'boolean',
         label=T('Nürnberger Rangierbahnhof')),
   Field('di_kino', 'boolean',
         label=T('Kino der etwas anderen Art')),

   Field('mi_wanderung', 'boolean',
         label=T('Wanderung')),
   Field('mi_essen_wanderung', 'integer',
         default=0,
         label=T('Essensauswahl Wanderung (Zahlung vor Ort)')),
   Field('mi_tiergarten', 'boolean',
         label=T('Tiergarten')),
   Field('mi_poolparty', 'boolean',
         label=T('Poolparty')),

   Field('do_minigolf', 'boolean',
         label=T('3D Schwarzlicht Minigolf')),
   Field('do_zeit_minigolf', 'list:string',
         label=T('Zeitauswahl 3D Schwarzlicht Minigolf (mehrere möglich)'),
         requires = IS_IN_SET(['9:30', '11:30', '13:30'], multiple=True)),
   Field('do_partyschiff', 'boolean',
         label=T('Partyschiff')),

   Field('fr_regensburg', 'boolean',
         label=T('Tagesausflug nach Regensburg')),
   Field('fr_essen', 'integer',
         default=0,
         label=T('Essensauswahl (Zahlung vor Ort)')),

   Field('sa_stadtfuehrung', 'boolean',
         label=T('Große Stadtführung')),
   Field('sa_stadtfuehrung_gruppe',
         writable=False, readable=False, label="Gruppe Stadtführung",
         requires = IS_EMPTY_OR(IS_IN_SET(['10:00 de Gruppe 1', '10:00 de Gruppe 2', '10:30 en', '10:30 de', '11:00 de Gruppe 1', '11:00 de Gruppe 2'], zero=None))),
   Field('sa_ball', 'boolean',
         label=T('Ball')),

   Field('so_verabschiedung', 'boolean',
         label=T('Verabschiedung')),

   Field('kommentar', 'text',
         label=T("Kommentar")),
   Field('bedingungen', 'boolean',
         requires = IS_EQUAL_TO('on', error_message=T('Bitte akzeptieren')),
         label=XML(T('Ich akzeptiere die %s' % A('Teilnahmebedingungen',_href='http://europatreffen2016.eu/index.php/de/anmeldung/teilnahmebedingungen',_target='blank')))),
   Field('anmeldedatum', 'datetime',
         default=request.now, writable=False, readable=False),
   Field('sprache',
         default=session.language if session.language is not None else "de", writable=False, readable=False),
   Field('betrag', 'decimal(9,2)',
         writable=False, readable=False, label="Soll"),
   Field('bezahlt', 'decimal(9,2)',
         default=0, writable=False, readable=False, label="Ist"),
   Field('zahlungsdatum', 'date',
         writable=False, readable=False,
         ),

   format = '%(vorname)s %(nachname)s')


class Price(object):
    """ Keeps the price for adults and optional for members and children """
    child16 = T("Kinder bis 16 J.", lazy=False)
    child12 = T("Kinder bis 12 J.", lazy=False)
    child6 = T("Kinder bis 6 J.", lazy=False)
    referenceDate = datetime.date(2016,5,1)

    def __init__(self, price_adult, price_child16=None, price_child12=None, price_child6=None, price_text=None):
        self.price_adult = price_adult
        self.price_child16 = price_child16
        self.price_child12 = price_child12
        self.price_child6 = price_child6
        self.price_text = price_text

    @staticmethod
    def val_to_string(val):
        if val:
            return '%.2f €' % val
        return T('auf eigene Kosten', lazy=False)

    def __str__(self):
        if ( self.price_text is not None):
            return self.price_text
        elif (self.price_child16 is None):
            return Price.val_to_string(self.price_adult)
        return "%.2f €, %s %.2f €, %s %.2f €, %s %.2f €" % (self.price_adult, Price.child16, self.price_child16, Price.child12, self.price_child12, Price.child6, self.price_child6)

    def get_val(self, dateOfBirth):
        delta = self.referenceDate - dateOfBirth
        age = delta.days / 365
        if age < 6 and self.price_child6 is not None:
            return self.price_child6
        elif age < 12 and self.price_child12 is not None:
            return self.price_child12
        elif age < 16 and self.price_child16 is not None:
            return self.price_child16
        else:
            return self.price_adult


db.anmeldung.mi_essen_wanderung.names = [T('Kein Mittagessen'),
                                         T('Fränkischer Sauerbraten mit 2 Klößen und Rotkohl 7,80 €'),
                                         T('Rinderroulade mit 2 Klößen und Rotkohl 7,80 €'),
                                         T('Schweineschnitzel mit Kartoffelsalat und Salat 8 €'),
                                         T('Schweinelende in Cognacsoße und Salat 11 €'),
                                         T('Scholle gebacken mit Kartoffeln und Salat 6,50 €'),
                                         T('Käsespätzle 5 €'),
                                         T('Großer Salat mit Putenbruststreifen 6 €')]
db.anmeldung.mi_essen_wanderung.requires = IS_IN_SET(map(lambda s: str(s), range(0, len(db.anmeldung.mi_essen_wanderung.names))), db.anmeldung.mi_essen_wanderung.names)
db.anmeldung.mi_essen_wanderung.represent = lambda v, r: db.anmeldung.mi_essen_wanderung.names[int(v)]

db.anmeldung.fr_essen.names = [T('Kein Abendessen'),
                               T('Hähnchenbrust mit Kartoffelgratin und Gemüse 12,80 €'),
                               T('Seehecht mit Kräuterreis und Gemüse 13,90 €'),
                               T('Mit Spinat gefüllte Nudelteigtaschen auf Gemüse-Tomaten-Ragout 10,80 €'),
                               T('Für Kinder: Paniertes Knusperschnitzel mit Pommes Frites 5,80 €')]
db.anmeldung.fr_essen.requires = IS_IN_SET(map(lambda s: str(s), range(0, len(db.anmeldung.fr_essen.names))), db.anmeldung.fr_essen.names)
db.anmeldung.fr_essen.represent = lambda v, r: db.anmeldung.fr_essen.names[int(v)]

db.anmeldung.unterkunft.names = [T('Sonstige'), T('Acom Nürnberg'), T('Ibis Nürnberg Hauptbahnhof'), T('A&O Nürnberg Hauptbahnhof')]
db.anmeldung.unterkunft.requires = IS_IN_SET(map(lambda s: str(s), range(0, len(db.anmeldung.unterkunft.names))), db.anmeldung.unterkunft.names)
db.anmeldung.unterkunft.represent = lambda v, r: db.anmeldung.unterkunft.names[int(v)]

db.anmeldung.so_barfuesser.preis = Price(0)
db.anmeldung.mo_wuerzburg.preis = Price(76, 55, 46, 38)
db.anmeldung.di_reichsparteitag.preis = Price(6.50)
db.anmeldung.di_dokuzentrum.preis = Price(6.50)
db.anmeldung.di_rangierbahnhof.preis = Price(6.50)
db.anmeldung.di_kino.preis = Price(9.00)
db.anmeldung.mi_wanderung.preis = Price(19)
db.anmeldung.mi_essen_wanderung.preis = Price(0)
db.anmeldung.mi_tiergarten.preis = Price(0)
db.anmeldung.mi_poolparty.preis = Price(30)
db.anmeldung.do_minigolf.preis = Price(6,6,0,0, T('6.00 €, Kinder unter 12 Jahren umsonst', lazy=False))
db.anmeldung.do_partyschiff.preis = Price(58)
db.anmeldung.fr_regensburg.preis = Price(45)
db.anmeldung.fr_essen.preis = Price(0)
db.anmeldung.sa_stadtfuehrung.preis = Price(6.5)
db.anmeldung.sa_ball.preis = Price(68)
db.anmeldung.so_verabschiedung.preis = Price(0)

db.anmeldung.bedingungen.comment = T("Teilnahme auf eigene Gefahr")
db.anmeldung.geburtsdatum.comment = T("Wird für Preisberechnung und Busunternehmen benötigt.")


# Max. Anzahl Teilnehmer
db.anmeldung.di_kino.limit = (99, T('Kino ist leider ausgebucht'))
db.anmeldung.mi_wanderung.limit = (140, T('Wanderung ist leider ausgebucht'))
db.anmeldung.sa_stadtfuehrung.limit = (180, T('Stadtführung ist leider ausgebucht'))
#db.anmeldung.sa_rathaus.limit = (24, T('Führung Altes Rathaus ist leider ausgebucht. Interesse an Warteliste bitte unten im Kommentar vermerken'))
#db.anmeldung.sa_krimitour.limit = (28, T('Krimi-Tour ist leider ausgebucht. Interesse an Warteliste bitte unten im Kommentar vermerken'))


veranstaltungen=('so_barfuesser',
                 'mo_wuerzburg',
                 'di_reichsparteitag',
                 'di_dokuzentrum',
                 'di_rangierbahnhof',
                 'di_kino',
                 'mi_wanderung',
                 'mi_essen_wanderung',
                 'mi_tiergarten',
                 'mi_poolparty',
                 'do_minigolf',
                 'do_partyschiff',
                 'fr_regensburg',
                 'fr_essen',
                 'sa_stadtfuehrung',
                 'sa_ball',
                 'so_verabschiedung')


def gesamtpreis(vars):
    betrag=0
    for k in vars:
        if hasattr(db.anmeldung[k],'preis'):
            if vars[k]:
                betrag += db.anmeldung[k].preis.get_val(vars.geburtsdatum)

    return betrag

konto = T('IBAN: DE32830654080004885651, BIC: GENODEF1SLR, Skatbank')
