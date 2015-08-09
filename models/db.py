#@PydevCodeAnalysisIgnore

import datetime

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
T.set_current_languages('de', 'de-de')
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
   Field('strasse', label=T('Straße'),
         requires = IS_NOT_EMPTY()),
   Field('plz',
         requires = IS_NOT_EMPTY(error_message=T('Bitte eine Postleitzahl eingeben')), 
         label=T('PLZ')),
   Field('ort',
         requires = IS_NOT_EMPTY(error_message=T('Bitte einen Ort eingeben')), 
         label=T('Ort')),
   Field('geburtsdatum', 'date',
         requires = IS_DATE(format='%d.%m.%Y'),
         label=T('Geburtsdatum')),
   Field('kind', 'boolean', 
         label=T('Kind bis 12 Jahre')),
   Field('vegetarier', 'boolean', 
         label=T('Vegetarier')),
   Field('mitglied', 'boolean',
         label=T('Mitglied im KdG bzw. KLM')),
   Field('bezirk',
         label=T('Bezirk (falls Mitglied)')),
   Field('spieler', 'boolean', 
         label=T('Ich spiele mit')),
   Field('mannschaft',
         label=T('Name der Mannschaft')),
   Field('mannschaft_gesucht', 'boolean', 
         label=T('Ich suche noch eine Mannschaft')),                                                   
   Field('anreise', 'date',
         requires = IS_DATE(format='%d.%m.%Y'),
         default=datetime.date(2015, 4, 3),
         label=('Anreise')),
   Field('abreise', 'date',
         requires = IS_DATE(format='%d.%m.%Y'),
         default=datetime.date(2015, 4, 6),
         label=('Abreise')),
   Field('unterkunft',
         label=('Name/Anschrift der Unterkunft in Leipzig')),
   Field('fr_bierstuben', 'boolean', 
         label=T('Abends Begrüßung in „Wenzel Prager Bierstuben“')),
   Field('sa_flughafen', 'boolean', 
         label=T('Vormittags Option 1: Führung Flughafen')),
   Field('sa_kletterhalle', 'boolean', 
         label=T('Vormittags Option 2: Schnupperkurs Kletterhalle')),
   Field('sa_rathaus', 'boolean', 
         label=T('Nachmittags Option 1: Führung Altes Rathaus')),
   Field('sa_krimitour', 'boolean', 
         label=T('Nachmittags Option 2: Krimi-Tour')),
   Field('sa_abendessen', 'boolean', 
         label=T('Abends Essen im „Thüringer Hof“')),
   Field('so_spieler', 'boolean', 
         label=T('Volleyballturnier als Spieler (Mittagessen, Getränk, Startgebühr)')),
   Field('so_zuschauer', 'boolean', 
         label=T('Volleyballturnier als Zuschauer (Mittagessen, Getränk)')),
   Field('so_party', 'boolean', 
         label=T('Abends Party mit Buffet und Disko')),
   Field('mo_verabschiedung', 'boolean', 
         label=T('Vormittags Verabschiedung')),
   Field('kommentar', 'text',
         label=T("Kommentar")),
   Field('bedingungen', 'boolean', 
         requires = IS_EQUAL_TO('on', error_message=T('Bitte akzeptieren')),
         label=XML(T('Ich akzeptiere die %s' % A('Teilnahmebedingungen',_href='http://ostervolleyballturnier.de/?page_id=73',_target='blank')))),
   Field('anmeldedatum', 'datetime',
         default=request.now, writable=False, readable=False),
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
    child = T("Kinder bis 12 Jahre", lazy=False)
    member = T("Mitglieder", lazy=False)
    
    def __init__(self, price_adult, price_member=None, price_child=None):
        self.price_adult = price_adult
        self.price_child = price_child
        self.price_member= price_member
        
    @staticmethod
    def val_to_string(val):
        if val:
            return '%.2f €' % val
        return T('auf eigene Kosten', lazy=False)
    
    def __str__(self):
        if (self.price_child is None) and (self.price_member is None):
            return Price.val_to_string(self.price_adult)
        return "%.2f €, %s %.2f €, %s %.2f €" % (self.price_adult, Price.member, self.price_member, Price.child, self.price_child)
    
    def get_val(self, member=False, child=False):
        if child and self.price_child is not None:
            return self.price_child;
        if member and self.price_member is not None:
            return self.price_member;
        return self.price_adult
    

db.anmeldung.fr_bierstuben.preis = Price(0)
db.anmeldung.sa_flughafen.preis = Price(15, 13.5, 6)
db.anmeldung.sa_kletterhalle.preis = Price(25, 22.5, 13)
db.anmeldung.sa_rathaus.preis = Price(12, 10.8, 3)
db.anmeldung.sa_krimitour.preis = Price(12, 10.8, 3)
db.anmeldung.sa_abendessen.preis = Price(0)
db.anmeldung.so_spieler.preis = Price(12, 10.8, 6)
db.anmeldung.so_zuschauer.preis = Price(8, 7, 4)
db.anmeldung.so_party.preis = Price(40, 36, 15)
db.anmeldung.mo_verabschiedung.preis = Price(0)

db.anmeldung.bedingungen.comment = T("Teilnahme auf eigene Gefahr")
     
# Max. Anzahl Teilnehmer
db.anmeldung.sa_flughafen.limit = (29, T('Führung Flughafen ist leider ausgebucht. Interesse an Warteliste bitte unten im Kommentar vermerken'))
db.anmeldung.sa_rathaus.limit = (24, T('Führung Altes Rathaus ist leider ausgebucht. Interesse an Warteliste bitte unten im Kommentar vermerken'))
db.anmeldung.sa_krimitour.limit = (28, T('Krimi-Tour ist leider ausgebucht. Interesse an Warteliste bitte unten im Kommentar vermerken'))
db.anmeldung.spieler.limit = (32, T('Max. Anzahl an Spielern erreicht. Interesse an Warteliste bitte unten im Kommentar vermerken'))
         

veranstaltungen=('fr_bierstuben',
                 'sa_flughafen',
                 'sa_kletterhalle',
                 'sa_rathaus',
                 'sa_krimitour',
                 'sa_abendessen',
                 'so_spieler',
                 'so_zuschauer',
                 'so_party',
                 'mo_verabschiedung')

 
def gesamtpreis(vars):
    betrag=0
    for k in vars:
        if hasattr(db.anmeldung[k],'preis'):
            if vars[k]:
                betrag += db.anmeldung[k].preis.get_val(vars.mitglied, vars.kind)

    return betrag


    





