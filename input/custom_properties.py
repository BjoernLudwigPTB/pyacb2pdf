from .properties import Column, SubtableSetting

pagesize = (178.0, 134.0)
rows_xmltag = "kurs"
identifier_xmltag = [
    "TerminDatumVon1",
    "TerminDatumBis1",
    "TerminDatumVon2",
    "TerminDatumBis2",
    "TerminDatumVon3",
    "TerminDatumBis3",
]
sort_xmltag = "TerminDatumVon1"
table_title = "Ausbildungs- und Fahrtenprogramm 2021"
columns = [
    Column(label="Art", tag=["Kursart"], width=7.2),
    Column(
        label="Datum",
        tag=[
            "TerminDatumVon1",
            "TerminDatumBis1",
            "TerminDatumVon2",
            "TerminDatumBis2",
            "TerminDatumVon3",
            "TerminDatumBis3",
        ],
        width=11.5,
    ),
    Column(label="Ort", tag=["Ort1"], width=18.7),
    Column(label="Leitung", tag=["Kursleiter"], width=14.5),
    Column(
        label="Beschreibung",
        tag=["Bezeichnung", "Bezeichnung2", "Beschreibung"],
        width=60.9,
    ),
    Column(label="Zielgruppe", tag=["Zielgruppe"], width=18),
    Column(
        label="Voraussetzungen<br/>a) persönliche | b) " "materielle | c) finanzielle",
        tag=["Voraussetzung", "Ausruestung", "Kurskosten", "Leistungen"],
        width=47,
    ),
]
filter_xmltag = "Kategorie"
subtable_settings = (
    SubtableSetting(
        label="Wandern im Hoch- und Mittelgebirge",
        include=[["Hochgebirge", "Mittelgebirge"], ["Wandern"]],
    ),
    SubtableSetting(
        label="Klettern und Bouldern im Mittelgebirge",
        include=[["Mittelgebirge"], ["Klettern", "Bouldern", "Höhle"]],
    ),
    SubtableSetting(
        label="Ausbildung, Wandern und Klettern in Berlin",
        include=[["in Berlin"], ["Ausbildung", "Wandern", "Klettern"]],
    ),
    SubtableSetting(label="Mountainbiken", include=[["Mountainbiken"]]),
    SubtableSetting(
        label="Ski, Bergsteigen, Hochtouren und Klettern im Hochgebirge",
        include=[
            ["Hochgebirge"],
            ["Bergsteigen", "Hochtouren", "Höhle", "Klettern", "Klettersteig", "Ski"],
        ],
    ),
    SubtableSetting(label="Veranstaltungen für Familien", include=[["Familie"]]),
    SubtableSetting(label="Jugendgruppen und -events", include=[["Jugend"]]),
)
