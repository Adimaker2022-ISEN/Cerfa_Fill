from pypdf import PdfReader
from pypdf import PdfWriter
from datetime import datetime

def convert_decimal_en_toutte_lettre(number):
    number = round(number, 2)
    int_part = int(number)
    decimal_part = int((number - int_part) * 100)
    int_part_text = convert_int_en_toutte_lettre(int_part)
    decimal_part_text = convert_int_en_toutte_lettre(decimal_part)
    return int_part_text + ", " + decimal_part_text + " Euros"

def convert_int_en_toutte_lettre(number): # fontion
    ones = ["", "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf", "dix", "onze", "douze", "treize", "quatorze", "quinze", "seize", "dix-sept", "dix-huit", "dix-neuf"]
    tens = ["", "", "vingt", "trente", "quarante", "cinquante", "soixante", "soixante-dix", "quatre-vingt", "quatre-vingt-dix"]
    if number < 20:
        return ones[number]
    if number < 100:
        if number % 10 == 0:
            return tens[number // 10]
        elif number // 10 == 7 or number // 10 == 9:
            if number % 10 == 1:
                return tens[number // 10] + "-et-" + ones[number % 10]
            else:
                return tens[number // 10] + "-" + ones[number % 10]
        else:
            return tens[number // 10] + "-" + ones[number % 10]
    if number < 1000:
        if number % 100 == 0:
            return ones[number // 100] + " cent"
        else:
            return ones[number // 100] + " cent " + convert_int_en_toutte_lettre(number % 100)
    if number < 1000000:
        if number % 1000 == 0:
            return convert_int_en_toutte_lettre(number // 1000) + " mille"
        else:
            return convert_int_en_toutte_lettre(number // 1000) + " mille " + convert_int_en_toutte_lettre(number % 1000)
    if number < 1000000000:
        if number % 1000000 == 0:
            return convert_int_en_toutte_lettre(number // 1000000) + " million"
        else:
            return convert_int_en_toutte_lettre(number // 1000000) + " million " + convert_int_en_toutte_lettre(number % 1000000)
    return convert_int_en_toutte_lettre(number // 1000000000) + " milliard" + ('' if number % 1000000000 == 0 else ' ' + convert_int_en_toutte_lettre(number % 1000000000))




# Variables pour la section "Bénéficiaire des versements" a chercher dans la BDD une fois qu'elle est fonctionelle
asso_nom = "111 arts"
asso_nb_rue = 12
asso_nom_rue = "rue de rue"
asso_CP = "59000" #Code postal
asso_commune = "lille"

asso_date_pub_journal_officiel = "12/15/1234"
asso_date_reco_utilite_publique = "11/15/1234"


id_cerfa = 324

# Variables pour la section "Donateur" a chercher dans la BDD une fois qu'elle est fonctionelle
donateur_nom = 'Doe'
donateur_prenoms = 'John'
donateur_Adresse = '55 rue de rue ' # N° + Rue
donateur_CP = 59450 #code postal
donateur_commune = 'Tourcoing'



# Variables dons a récupérer depuis la DB
don_montant = 0
don_montant_toute_lettre = convert_decimal_en_toutte_lettre(don_montant)
don_datte_versement = "date"
print(convert_decimal_en_toutte_lettre(don_montant))
# Date et signature
date_us = datetime.date(datetime.now())
date_ue = date_us.strftime("%d-%m-%Y")


# Fichiers d'entrée
reader = PdfReader("data/titre_dons_organisme_interet_general.pdf")
writer = PdfWriter()

# Importe des pages (note il faut toujours importer toutes les pages même si on ne les modifie pas, commence a 0)
writer.add_page(reader.pages[0])
fields = reader.get_form_text_fields()
print(fields)
writer.add_page(reader.pages[1])


def fill_cerfa():

    

    # Bénéficiaire des versements Page 1
    writer.update_page_form_field_values(
        writer.pages[0], {"Numéro dordre du reçu":  id_cerfa}
    )

    writer.update_page_form_field_values(
        writer.pages[0], {"Adresse":  asso_nom}
    )

    writer.update_page_form_field_values(
        writer.pages[0], {"N": asso_nb_rue}
    )

    writer.update_page_form_field_values(
        writer.pages[0], {"Rue":  asso_nom_rue}
    )
    
    writer.update_page_form_field_values(
        writer.pages[0], {"Code Postal":  asso_CP}
    )
    
    writer.update_page_form_field_values(
        writer.pages[0], {"Commune":  asso_commune}
    )

    # Donateur Page 2
    writer.update_page_form_field_values(
        writer.pages[1],{"Nom": donateur_nom}
    )

    writer.update_page_form_field_values(
        writer.pages[1],{"Prénoms": donateur_prenoms}
    )

    writer.update_page_form_field_values(
        writer.pages[1],{"Adresse_2": donateur_Adresse}
    )

    writer.update_page_form_field_values(
        writer.pages[1],{"Code Postal_2": donateur_CP}
    )

    writer.update_page_form_field_values(
        writer.pages[1],{"Commune_2": donateur_commune}
    )

    # Don Page 2
    writer.update_page_form_field_values(
        writer.pages[1],{"Euros": don_montant}
    )
    writer.update_page_form_field_values(
        writer.pages[1],{"Somme en toutes lettres": don_montant_toute_lettre}
    )
    writer.update_page_form_field_values(
        writer.pages[1],{"date4": don_datte_versement}
    )
    writer.update_page_form_field_values(
        writer.pages[1],{"date5": date_ue}
    )




fill_cerfa()

# crée et enregistre le PDF "CERFA a imprimer n°XXX.pdf".
with open("data/CERFA N°"+  str(id_cerfa)+ " "  +donateur_prenoms + " " + donateur_nom+ ".pdf", "wb") as output_stream:
    writer.write(output_stream)
    meta = reader.metadata