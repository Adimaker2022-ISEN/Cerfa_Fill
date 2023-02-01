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
#def int_to_words(n):
    if number == 0:
        return "zéro"
    
    if number < 0:
        return "Error"
    
    units = ["", "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf", "dix",
             "onze", "douze", "treize", "quatorze", "quinze", "seize", "dix-sept", "dix-huit", "dix-neuf"]
    tens = ["", "", "vingt", "trente", "quarante", "cinquante", "soixante", "soixante-dix", "quatre-vingt", "quatre-vingt-dix"]
    thousands = ["", "mille", "deux mille", "trois mille", "quatre mille", "cinq mille", "six mille", "sept mille", "huit mille", "neuf mille"]
    
    if number < 20:
        return units[number]
    
    if number < 100:
        tens_val = number // 10
        units_val = number % 10
        tens_str = tens[tens_val]
        units_str = units[units_val]
        if tens_val == 7 or tens_val == 9:
            return tens_str + "-" + units_str
        else:
            return tens_str + " " + units_str
        
    if number < 1000:
        hundreds = number // 100
        
        remainder = number % 100
        if hundreds ==1:
            if remainder == 0:
                return "cent "
            else:
                return " cent " + convert_int_en_toutte_lettre(remainder)
        else:      
            if remainder == 0:
                return convert_int_en_toutte_lettre(hundreds) + " cent "  
            else:
                return convert_int_en_toutte_lettre(hundreds) + " cent " + convert_int_en_toutte_lettre(remainder)
        
    if number < 100000:
        thousands_val = number // 1000
        remainder = number % 1000
        if remainder == 0:
            return thousands[thousands_val]
        else:
            return thousands[thousands_val] + " " + convert_int_en_toutte_lettre(remainder)




# Variables pour la section "Bénéficiaire des versements" à chercher dans la BDD une fois qu'elle est fonctionnelle
asso_nom = "Les 111 des Arts Lille"
asso_nb_rue = 27
asso_nom_rue = "Rue Jean Bart"
asso_CP = "59000" #Code postal
asso_commune = "Lille"


id_cerfa = 124

# Variables pour la section "Donateur" à chercher dans la BDD une fois qu'elle est fonctionnelle
donateur_nom = 'Doe'
donateur_prenoms = 'John'
donateur_Adresse = '55 rue de rue ' # N° + Rue
donateur_CP = 59450 #code postal
donateur_commune = 'Tourcoing'



# Variables pour la section "dons" à récupérer depuis la BDD
don_montant = 9999
don_montant_toute_lettre = convert_int_en_toutte_lettre(don_montant)
don_datte_versement = "date"

forme_du_don = "declaration_de_don_manuel" # acte_authentique || acte_sous_seing_prive || declaration_de_don_manuel || autres
nature_du_don = "numeraire" # numeraire || titres_de_societes_cotes || autres
mode_de_versement = "cheque" # espece || cheque || cb


# Date et signature
date_us = datetime.date(datetime.now())
date_ue = date_us.strftime("%d-%m-%Y")
date_annee = date_us.strftime("%Y")

# Fichiers d'entrée
reader = PdfReader("data/titre_dons_organisme_interet_general.pdf")
writer = PdfWriter()

# Importe des pages (note : il faut toujours importer toutes les pages même si l’on ne les modifie pas, commence à 0)
writer.add_page(reader.pages[0])
fields = reader.get_form_text_fields()

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

    # Coche la case "Association..." || Attention il existe deux valeurs communes Yes et On.
    # Pour le savoir, il faut aller dans un navigateur et inspecter la case. exportvalue='On' ou Yes
    writer.update_page_form_field_values(
        writer.pages[0], {"Oeuvre ou organisme dintérêt général": "On"}
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

    # Casses à cocher forme du don
    match forme_du_don:
        case "acte_authentique":
            print("acte_authentique")
            writer.update_page_form_field_values(
                writer.pages[1], {"Acte authentique": "On"}
            )
        case "acte_sous_seing_prive":
            print("acte_sous_seing_prive")
            writer.update_page_form_field_values(
                writer.pages[1], {"Acte sous seing privé": "On"}
            )        
        case "declaration_de_don_manuel":
            print("declaration_de_don_manuel")
            writer.update_page_form_field_values(
                writer.pages[1], {"Déclaration de don manuel": "On"}
            )
        case "autres":
            print("autres")
            writer.update_page_form_field_values(
                writer.pages[1], {"Autres": "On"}
            )
        case _:
            print("Error")

    # Casses à cocher nature du don
    match nature_du_don:
        case "numeraire":
            print("numeraire")
            writer.update_page_form_field_values(
                writer.pages[1], {"Numéraire": "On"}
            )
        case "titres_de_societes_cotes":
            print("titres_de_societes_cotes")
            writer.update_page_form_field_values(
                writer.pages[1], {"Titres de sociétés cotés": "On"}
            )        
        case "autres":
            print("autres")
            writer.update_page_form_field_values(
                writer.pages[1], {"Autres 4": "On"}
            )
        case _:
            print("Error")

    # Casses à cocher mode de versement
    match mode_de_versement:
        case "espece":
            print("espece")
            writer.update_page_form_field_values(
                writer.pages[1], {"Remise despèces": "On"}
            )
        case "cheque":
            print("cheque")
            writer.update_page_form_field_values(
                writer.pages[1], {"Chèque": "On"}
            )        
        case "cb":
            print("cb")
            writer.update_page_form_field_values(
                writer.pages[1], {"Virement prélèvement carte bancaire": "On"}
            )
        case _:
            print("Error")



    writer.update_page_form_field_values(
        writer.pages[1],{"date5": date_ue}
    )


fill_cerfa()

# Crée et enregistre le PDF "CERFA à imprimé n°XXX.pdf".
with open("data/CERFA N°"+  str(id_cerfa)+ " "  +donateur_prenoms + " " + donateur_nom+ ".pdf", "wb") as output_stream:
    writer.write(output_stream)
    meta = reader.metadata