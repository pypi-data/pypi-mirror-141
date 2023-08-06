BOOKING_API_URL = "https://www.ryanair.com/api/booking/v4/en-gb/availability"

import requests


def example_call():

    params = dict(
        ADT=2,  # numero di passeggeri ADULTI
        CHD=0,  # numero di passeggeri BAMBINI
        DateIn="",  # !! DATA VOLO RITORNO !! Se non specificato, il volo si intende automaticamente di sola andata
        DateOut="2022-6-20",  # !! DATA VOLO ANDATA !!
        Destination="MXP",  # AEROPORTO DESTINAZIONE
        Disc=0,  # !! UNKNOWN
        INF=0,  # !! UNKNOWN
        Origin="SUF",  # AEROPORTO ORIGINE
        TEEN=0,
        promoCode="",  # PROMO CODE
        IncludeConnectingFlights="false",  # SPECIFY THE ROUTE
        FlexDaysBeforeIn=2,  # Same as 'FlexDaysBeforeOut'
        FlexDaysIn=2,  # Same as 'FlexDaysOut'
        RoundTrip="true",
        FlexDaysBeforeOut=2,  # INDICA IL NUMERO DI QUANTI GIORNI PRIMA SI VUOLE RICEVERE INFORMAZIONI
        FlexDaysOut=2,  # INDICA IL NUMERO DI QUANTI GIORNI DOPO SI VUOLE RICEVERE INFORMAZIONI
        ToUs="AGREED",  # !! UNKNOWN
    )

    resp = requests.get(url=BOOKING_API_URL, params=params)
    data = resp.json()

    # dati voli andata
    outTrip = data["trips"][0]  # dati del viaggio
    outTripDates = outTrip["dates"]  # ritorna un array con le date dei voli

    for date in outTripDates:
        print(date["dateOut"])  # la data relativa ai voli
        flights = date["flights"]  # lista dei voli disponibili per quella data

        for flight in flights:
            print(flight["faresLeft"])  # nr di posti ADT rimanenti  (-1 significa indefiniti)
            print(flight["flightKey"])  # stringa volo
            print(flight["operatedBy"])  # da chi viene operato il volo
            print(flight["flightNumber"])  # numero volo
            print(flight["duration"])  # durata del volo

            # timeUTC = flight["timeUTC"]
            # print(timeUTC[0])  # orario di partenza
            # print(timeUTC[1])  # orario d'arrivo

            fares = flight["regularFare"]["fares"]  # lista tariffe

            for fare in fares:
                print(fare["type"])  # tipo della tariffa (adullto/bambino)
                print(fare["amount"])  # costo della tariffa
                print(fare["count"])  # numero di posti a tale prezzo
                # fare["hasDiscount"] # indica se scontato o no
                # fare["publishedFare"] # tariffa pubblicata (?)
                # fare["hasPromoDiscount"] # indica se ci sono delle promozioni attive su tale tariffa

    # dati voli ritorno
    if len(data["trips"]) > 1:
        inTrip = data["trips"][1]
        inTripDates = inTrip["dates"]  # ritorna un array con le date dei voli
    else:
        inTripDates = []

    for date in inTripDates:
        print(date["dateOut"])  # la data relativa ai voli
        flights = date["flights"]  # lista dei voli disponibili per quella data

        for flight in flights:
            print(flight["faresLeft"])  # nr di posti ADT rimanenti  (-1 significa indefiniti)
            print(flight["flightKey"])  # stringa volo
            print(flight["operatedBy"])  # da chi viene operato il volo
            print(flight["flightNumber"])  # numero volo
            print(flight["duration"])  # durata del volo

            # timeUTC = flight["timeUTC"]
            # print(timeUTC[0])  # orario di partenza
            # print(timeUTC[1])  # orario d'arrivo

            fares = flight["regularFare"]["fares"]  # lista tariffe

            for fare in fares:
                print(fare["amount"])  # costo della tariffa
                print(fare["count"])  # numero di posti a tale prezzo
                # fare["hasDiscount"] # indica se scontato o no
                # fare["publishedFare"] # tariffa pubblicata (?)
                # fare["hasPromoDiscount"] # indica se ci sono delle promozioni attive su tale tariffa
