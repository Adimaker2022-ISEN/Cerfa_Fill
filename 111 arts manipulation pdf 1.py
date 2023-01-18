from pypdf import PdfReader
from pypdf import PdfWriter

# Variables pour la section "Bénéficiaire des versements" a chercher dans la BDD une fois qu'elle est fonctionelle
aso_nom = "111 arts"
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
don_montant = 30
don_montant_toute_lettre = "Trente"+"€"
don_datte_versement = 'Doday'

# Fichiers d'entrée
reader = PdfReader("data/titre_dons_organisme_interet_general.pdf")
writer = PdfWriter()

# Importe des pages (note il faut toujours importer toutes les pages, commence a 0)
writer.add_page(reader.pages[0])
fields = reader.get_form_text_fields()
print(fields)
writer.add_page(reader.pages[1])


def coche_case(nom_case):
    for field in fields:
        if field.startswith(nom_case):
            fields[field] = '/Yes'
            break

def fill_cerfa():

    # Bénéficiaire des versements Page 1
    writer.update_page_form_field_values(
        writer.pages[0], {"Numéro dordre du reçu":  id_cerfa}
    )

    writer.update_page_form_field_values(
        writer.pages[0], {"N": asso_nb_rue}
    )
    writer.update_page_form_field_values(
        writer.pages[0], {"Rue":  asso_nom_rue}
    )
    
    # Case a cocher
    #writer.update_page_form_field_values(
    #    writer.pages[0], {"Association ou fondation reconnue dutilité publique par décret en date du":  "d"}
    #)
    coche_case("Association ou fondation reconnue dutilité publique par décret en date du")

    writer.update_page_form_field_values(
        writer.pages[0], {"date1":  asso_date_pub_journal_officiel}
    )
    writer.update_page_form_field_values(
        writer.pages[0], {"date2":  asso_date_pub_journal_officiel}
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



fill_cerfa()

# crée et enregistre le PDF "CERFA a imprimer n°XXX.pdf".
with open("data/CERFA N°"+  str(id_cerfa)+ " "  +donateur_prenoms + " " + donateur_nom+ ".pdf", "wb") as output_stream:
    writer.write(output_stream)

    meta = reader.metadata
    
    print(len(reader.pages))
    
  
#    print(meta.author)
#    print(meta.creator)
#    print(meta.producer)
#    print(meta.subject)
#    print(meta.title)

