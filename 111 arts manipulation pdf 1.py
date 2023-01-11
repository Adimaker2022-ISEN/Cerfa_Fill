from pypdf import PdfReader
from pypdf import PdfWriter

# Fichiers d'entrée
reader = PdfReader("data/titre_dons_organisme_interet_general.pdf")
writer = PdfWriter()


writer.add_page(reader.pages[0])
writer.add_page(reader.pages[1])

fields = reader.get_fields()
print(fields)


writer.update_page_form_field_values(
    writer.pages[0], {"Numéro dordre du reçu": "ADIMAKER"}
)

writer.update_page_form_field_values(
    writer.pages[0], {"N": "18"}
)
writer.update_page_form_field_values(
    writer.pages[0], {"Rue": "Rue Saint-Jean-Baptiste de la Salle"}
)
# crée et enregistre le PDF "CERFA a imprimer n°XXX.pdf".
with open("data/CERFA a imprimer n°XXX.pdf", "wb") as output_stream:
    writer.write(output_stream)

    meta = reader.metadata
    
    print(len(reader.pages))
    
    
    print(meta.author)
    print(meta.creator)
    print(meta.producer)
    print(meta.subject)
    print(meta.title)