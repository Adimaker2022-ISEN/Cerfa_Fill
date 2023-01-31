# Cerfa_Fill

## Comment manipuler des fichiers PDF

Ce repository héberge des exemples de codes qui permettent de remplir le CERFA

### Extensions recommandées

- vscode-pdf : cette extension permet de voir des fichiers PDF sans avoir à sortir de VsCode

## Installation de la librairie *pypedf*

    pip install pypdf

> ⚠️ Il existe PyPDF2. ATENTION le projet N’EST PLUS MAINTENU et ne doit pas être utilisé

## Utilisation

Dans un fichier python déclare

    from  pypdf  import  PdfReader
	from  pypdf  import  PdfWriter

*PdfReader* est utilisé pour récupérer des informations dans un fichier PDF (nombre de pages, auteur...)
*PdfWriter* est utilisé pour créer et faire des ajouts à un fichier PDF (ajout d'une page, remplissages de champs interactifs...)

### Manipulation Metadata

#### Lecture de Metadata

    from pypdf import PdfReader

    reader = PdfReader("example.pdf")

    meta = reader.metadata

    print(len(reader.pages))

    print(meta.author)
    print(meta.creator)
    print(meta.title)
Le code ci-dessus permet d'écrire dans le terminal certaines des metadata (note elles peuvent avoir la valeur*None*)

### Manipulation de formulaires

La librairie permet aussi de remplir les champs interactifs d'un fichier PDF

    from  pypdf  import  PdfReader
    from  pypdf  import  PdfWriter

    # Fichier d'entrée
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
    with  open("data/CERFA a imprimer n°XXX.pdf", "wb") as  output_stream:
	    writer.write(output_stream)
Le programme ci-dessus modifie les champs :

1. Numéro dordre du reçu
2. N
3. Rue

![image](https://user-images.githubusercontent.com/46867831/211910681-a37a6224-19ad-4dc0-8e11-da6207e336dd.png)

![image](https://user-images.githubusercontent.com/46867831/211910854-64a19a50-b5ab-4ead-8b89-c23b3a10d82a.png)

## Casses a cocher
Il existe plusieurs standards pour signaler qu'une casse est cocher ou vrai. Pour savoir la quelle utiliser : Ouvrir le pdf dans un navigateur -> inspecter l'éllément -> Sélectionez la case a coher

![Code_PCNx8zMcFG](https://user-images.githubusercontent.com/46867831/215884924-92c7107d-2966-4157-ac76-dada14beb9e0.png)
1. Clé de validation
2. Le nom du champ

Exemple:
//
writer.update_page_form_field_values(
	writer.pages[1], {"Case1": "On"}
)
//
Le code ci-dessus assume que 1. La clée de validation est "On" (Note : elle peut être aussi "Yes") 2. le nom du cham est "Case1"

### ToDo :

- [ ] Remplir des champs d'images (pour la signature)
- [x] Remplir des champs à cocher [x] [ ]

Auteur : Antoine Chatelain 12/01/2023
