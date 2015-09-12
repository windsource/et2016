import geb.Browser
import geb.Page

import org.junit.Test


class CreatePage extends Page{
	static url = "create"
	
	static at = {
		$("h2").text() == "Anmeldung zum Europatreffen 2016"
	}
	
	static content = {
		vorname { $("form#create_form").vorname() }
		nachname { $("form#create_form").nachname() }
		email { $("form#create_form").email() }
		telefon { $("form#create_form").telefon() }
		strasse { $("form#create_form").strasse() }
		ort { $("form#create_form").ort() }
		geburtsdatum { $("form#create_form").geburtsdatum() }
		plz { $("form#create_form").plz() }
		land { $("form#create_form").land() }
		vegetarier { $("form#create_form").vegetarier() }
		mitglied { $("form#create_form").mitglied() }
		bezirk { $("form#create_form").bezirk() }
		so_barfuesser { $("form#create_form").so_barfuesser() }
		mo_wuerzburg { $("form#create_form").mo_wuerzburg() }		
		di_reichsparteitag { $("form#create_form").di_reichsparteitag() }
		di_dokuzentrum { $("form#create_form").di_dokuzentrum() }
		di_rangierbahnhof { $("form#create_form").di_rangierbahnhof() }
		di_kino { $("form#create_form").di_kino() }
		mi_wanderung { $("form#create_form").mi_wanderung() }
		mi_essen_wanderung { $("form#create_form").mi_essen_wanderung() }
		mi_tiergarten { $("form#create_form").mi_tiergarten() }
		mi_poolparty { $("form#create_form").mi_poolparty() }
		do_minigolf { $("form#create_form").do_minigolf() }
		do_partyschiff { $("form#create_form").do_partyschiff() }
		fr_regensburg { $("form#create_form").fr_regensburg() }
		fr_essen { $("form#create_form").fr_essen() }
		sa_stadtfuehrung { $("form#create_form").sa_stadtfuehrung() }
		sa_ball { $("form#create_form").sa_ball() }
		so_verabschiedung { $("form#create_form").so_verabschiedung() }
		kommentar { $("form#create_form").kommentar() }
		bedingungen { $("form#create_form").bedingungen() }
		
		nextButton { $("input.btn", type: "submit") }
	}
	
}

class ConfirmPage extends Page {
	static url = "confirm"

	static at = {
		$("h2").text() == "Bitte prüfe die Daten und bestätige sie unten"
	}

	static content = {
		gesamtpreis { $("h3", text: startsWith("Gesamtpreis")) }
		confirmButton { $("input.btn", type: "submit") }
	}

}

class PrintConfirmationPage extends Page {
	static url = "printConfirmation"
	
	static at = {
		$("h3").text() == "Die Anmeldung ist erfolgt!"
	}

}

	
class PersonalData extends GroovyTestCase {

	def myBaseUrl = "http://127.0.0.1:8000/et2016/default/"
	
	void fillPersonalData(page) {
		page.with {
			vorname.value "Max"
			nachname.value "Chaplin"
			email.value "charly@sadgagfsgfh.de"
			telefon.value "0911 1234567"
			strasse.value "Hollywoodstr. 5"
			ort.value "Los Angelos"
			plz.value "98765"		
			geburtsdatum.value "4.4.1971"
		}		
	}
	
	@Test
	void testDeBasicRegistration() {
		Browser.drive {
			setBaseUrl(myBaseUrl)
			to CreatePage
			fillPersonalData(page)
			
			page.kommentar.value "Ich komme gern!"
			page.bedingungen.value "on"
			
			page.nextButton.click()
			
			page ConfirmPage
			verifyAt()
					
			assertTrue page.gesamtpreis.text() == "Gesamtpreis: 0.00 €"
			
			$("input", value:"Daten absenden").click()
			
			assert $("h3").text() == "Die Anmeldung ist erfolgt!"
		
		}.clearCookies()		
	}
	
	@Test
	void testConditionsNotAccepted() {
		Browser.drive {
			setBaseUrl(myBaseUrl)
			to CreatePage
			fillPersonalData(page)
						
			page.nextButton.click()
			
			page CreatePage
			verifyAt()
			
			page.bedingungen.value "on"
			
			page.nextButton.click()
			
			page ConfirmPage
			verifyAt()
		}.clearCookies()
	}

	@Test
	void testMondayPriceAdult() {
		Browser.drive {
			setBaseUrl(myBaseUrl)
			to CreatePage
			fillPersonalData(page)
			
			page.geburtsdatum.value "1.1.1970"

			page.mo_wuerzburg.value "on"
			
			page.do_minigolf.value "on"

			page.bedingungen.value "on"
			
			page.nextButton.click()
			
			page ConfirmPage
			verifyAt()
			
			assertTrue page.gesamtpreis.text() == "Gesamtpreis: 82.00 €"			

			page.confirmButton.click()
			
			page PrintConfirmationPage
			verifyAt()
		}.clearCookies()
	}
	
	@Test
	void testMondayPriceChild16() {
		Browser.drive {
			setBaseUrl(myBaseUrl)
			to CreatePage
			fillPersonalData(page)
			
			page.geburtsdatum.value "1.6.2000"

			page.mo_wuerzburg.value "on"

			page.do_minigolf.value "on"

			page.bedingungen.value "on"
			
			page.nextButton.click()
			
			page ConfirmPage
			verifyAt()
			
			assertTrue page.gesamtpreis.text() == "Gesamtpreis: 61.00 €"

			page.confirmButton.click()
			
			page PrintConfirmationPage
			verifyAt()
		}.clearCookies()
	}
	
	@Test
	void testMondayPriceChild12() {
		Browser.drive {
			setBaseUrl(myBaseUrl)
			to CreatePage
			fillPersonalData(page)
			
			page.geburtsdatum.value "1.6.2004"

			page.mo_wuerzburg.value "on"

			page.do_minigolf.value "on"

			page.bedingungen.value "on"
			
			page.nextButton.click()
			
			page ConfirmPage
			verifyAt()
			
			assertTrue page.gesamtpreis.text() == "Gesamtpreis: 46.00 €"

			page.confirmButton.click()
			
			page PrintConfirmationPage
			verifyAt()
		}.clearCookies()
	}

	@Test
	void testMondayPriceChild6() {
		Browser.drive {
			setBaseUrl(myBaseUrl)
			to CreatePage
			fillPersonalData(page)
			
			page.geburtsdatum.value "1.6.2010"

			page.mo_wuerzburg.value "on"

			page.do_minigolf.value "on"

			page.bedingungen.value "on"
			
			page.nextButton.click()
			
			page ConfirmPage
			verifyAt()
			
			assertTrue(page.gesamtpreis.text() == "Gesamtpreis: 38.00 €")

			page.confirmButton.click()
			
			page PrintConfirmationPage
			verifyAt()
		}.clearCookies()
	}

	@Test
	void testFullTest() {
		Browser.drive {
			setBaseUrl(myBaseUrl)
			to CreatePage
			
			page.with {
				vorname.value "Billy"
				nachname.value "Idol"
				email.value "billy@sadgagfsgfh.de"
				telefon.value "0911 1234567"
				strasse.value "Hollywoodstr. 5"
				ort.value "Zürich"
				plz.value "CH-1234"
				geburtsdatum.value "4.4.1971"
				land.value "Switzerland"
				
				vegetarier.value "on"
				mitglied.value "on"
				bezirk.value "Basel"
								
				so_barfuesser.value "on"
				mo_wuerzburg.value "on"
				di_reichsparteitag.value "on"
				di_dokuzentrum.value "on"
				di_kino.value "on"
				mi_wanderung.value "on"
				mi_essen_wanderung.value "2"
				mi_poolparty.value "on"
				do_minigolf.value "on"
				do_partyschiff.value "on"
				fr_regensburg.value "on"
				fr_essen.value "1"
				sa_stadtfuehrung.value "on"
				sa_ball.value "on"
				so_verabschiedung.value "on"
			}
	
			page.bedingungen.value "on"
			
			page.nextButton.click()
			
			page ConfirmPage
			verifyAt()
			
			assertTrue(page.gesamtpreis.text() == "Gesamtpreis: 330.50 €")
			
			page.confirmButton.click()
			
			page PrintConfirmationPage
			verifyAt()

		}.clearCookies()
	}

}