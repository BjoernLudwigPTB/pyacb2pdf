from typing import List

import warnings

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase.pdfmetrics import registerFont, registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.platypus.flowables import KeepTogether
from reportlab.platypus.tables import Table

from PdfVisualisation.TableStyle import TableStyle
from model.tables.Creator import Creator
from model.tables.TableBuilder import TableBuilder


class Parser:

    _elements: List[KeepTogether]

    def __init__(self, properties, elements=[]):
        """
        XML parser to extract all interesting information from xml-data.

        :param str properties: path to the properties file
        :param List[KeepTogether] elements: optional elements to populate the Parser
        """
        self._elements = elements
        self._creator = Creator()
        self._table_styles = TableStyle()
        Parser._set_font_family()
        self._styles = self._style()
        self._table_manager = TableBuilder(properties, self._styles)

    @staticmethod
    def _style():
        """ Set the resulting tables' styling

        Do all the customization of styling regarding margins, fonts,
        fontsizes, etc..

        :returns: the created StyleSheet object
        :rtype: reportlab.lib.styles.StyleSheet1
        """
        # Get custom_styles for all headings, texts, etc. from sample
        custom_styles = getSampleStyleSheet()
        # Overwrite the sample styles according to our needs. TODO this should be provided in the properties file
        custom_styles.get("Normal").fontSize = 7
        custom_styles.get("Normal").leading = custom_styles["Normal"].fontSize * 1.2
        custom_styles.get("Normal").fontName = "NewsGothBT"
        custom_styles.get("Italic").fontSize = custom_styles["Normal"].fontSize
        custom_styles.get("Italic").leading = custom_styles["Italic"].fontSize * 1.2
        custom_styles.get("Italic").fontName = "NewsGothBT_Italic"
        custom_styles.get("Heading1").fontSize = 12
        custom_styles.get("Heading1").alignment = 1
        custom_styles.get("Heading1").leading = custom_styles["Heading1"].fontSize * 1.2
        custom_styles.get("Heading1").fontName = "NewsGothBT_Bold"
        custom_styles.get("Heading2").fontSize = custom_styles["Normal"].fontSize
        custom_styles.get("Heading2").alignment = 1
        custom_styles.get("Heading2").leading = custom_styles["Heading2"].fontSize * 1.2
        custom_styles.get("Heading2").fontName = "NewsGothBT_Bold"
        return custom_styles

    @staticmethod
    def _set_font_family():
        """
        Register the desired font with `reportlab` to make sure that
        `<i></i>` and `<b></b>` work well.

        TODO this is much to hard coded and needs some serious refactoring
        """
        registerFont(TTFont("NewsGothBT", "PdfVisualisation/NewsGothicBT-Roman.ttf"))
        registerFont(
            TTFont("NewsGothBT_Bold", "PdfVisualisation/NewsGothicBT-Bold.ttf")
        )
        registerFont(
            TTFont("NewsGothBT_Italic", "PdfVisualisation/NewsGothicBT-Italic.ttf")
        )
        registerFont(
            TTFont(
                "NewsGothBT_BoldItalic", "PdfVisualisation/NewsGothicBT-BoldItalic.ttf"
            )
        )
        registerFontFamily(
            "NewsGothBT",
            normal="NewsGothBT",
            bold="NewsGothBT_Bold",
            italic="NewsGothBT_Italic",
            boldItalic="NewsGothBT_BoldItalic",
        )

    @staticmethod
    def _concatenate_tags_content(item, item_tags, separator=" - "):
        """ Form one string from the content of a list of an items XML tags content

        Form a string of the content for all desired item tags by concatenating them
        together with a separator. This is especially necessary, since
        :py:mod:`reportlab.platypus.Paragraph` cannot handle `None`s as texts.

        :param xml.etree.ElementTree.Element item: the item from where
            the texts shall be extracted
        :param List[str] item_tags: list of all tags for which the
            descriptive texts is wanted, even if it is just one
        :param str separator: the separator in between the concatenated texts
        :returns: concatenated, separated texts of all tags for the current event
        :rtype: str
        """
        event_data_string = ""
        for tag in item_tags:
            data_string = item.findtext(tag)
            if data_string:
                if event_data_string:
                    event_data_string += separator + data_string
                else:
                    event_data_string = data_string
        return event_data_string

    @staticmethod
    def _parse_prerequisites(personal, material, financial, offers):
        """
        Determine all prerequisites and assemble a string accordingly.

        :param str material: material prerequisite xml text
        :param str personal: personal prerequisite xml text
        :param str financial: financial prerequisite xml text
        :param str offers: xml text of what is included in the price
        :returns: the text to insert in prerequisite column
        the current event
        :rtype: str
        """
        if personal:
            personal_string = "a) " + personal + "<br/>"
        else:
            personal_string = "a) keine <br/>"

        if material:
            material_string = "b) " + material + "<br/>"
        else:
            material_string = "b) keine <br/>"

        if financial:
            financial_string = "c) " + financial + " € (" + offers + ")"
        else:
            financial_string = "c) keine"
        return personal_string + material_string + financial_string

    @staticmethod
    def _parse_date(date):
        """
        Determine the correct date for printing.

        :param str date: xml tag for relevant date.
        :returns: the text to insert in date column of the current event
        :rtype: str
        """
        if "2099" in date:
            date_string = "auf Anfrage"
        elif date:
            date_string = (
                date.replace("00:00", "")
                .replace("2020", "20")
                .replace("2019", "19")
                .replace("2018", "18")
            )
        else:
            date_string = ""
        return date_string

    @staticmethod
    def _parse_description(name, name2, description, url):
        """
        Concatenate the description and the url if provided.

        :param str name: the short name for the event
        :param str name2: the short name number two for the event
        :param str description: the descriptive text
        :param str url: the trainer's homepage url
        :returns: the full description including url if provided
        :rtype: str
        """
        if name:
            full_description = "<b>" + name + "</b>"
        else:
            full_description = ""

        if name2:
            full_description += " - " + name2

        if description:
            full_description += " - " + description

        if url:
            full_description += " Mehr Infos unter: " + url + "."

        return full_description

    def collect_xml_data(self, events):
        """
        Traverse the parsed xml data and gather collected event data. Pass
        event data to table_manager and get collected data back.

        :param List[xml.etree.ElementTree.Element] events: a list of the
            events from which the texts shall be extracted into a nicely
            formatted row of a table to insert in print out `_elements`
        :returns: all table rows containing the relevant event data
        :rtype: List[KeepTogether]
        """
        if events is not None:
            for event in events:
                categories = self.get_event_categories(event)
                self._table_manager.distribute_event(
                    self.collect_event_data(event), categories
                )
            subtable_elements = self._table_manager.collect_subtables()
            for subtable_element in subtable_elements:
                self._elements.append(KeepTogether(subtable_element))
            return self._elements
        else:
            warnings.warn("There were no items to print.", RuntimeWarning)

    def collect_event_data(self, event):
        """
        Extract interesting information from event and append them to print
        out data in `_elements`.

        :param xml.etree.ElementTree.Element event: the event from which the texts shall
            be extracted into a nicely formatted row of a table to insert in print out
            `_elements`
        :returns: single row table containing all relevant event data
        :rtype: Table
        """
        if event is not None:
            styles = self._styles
            columns_to_print = [
                Paragraph(
                    Parser._concatenate_tags_content(event, ["Kursart"]),
                    styles["Normal"],
                ),
                Paragraph(
                    Parser._parse_date(
                        self._concatenate_tags_content(
                            event, ["TerminDatumVon1", "TerminDatumBis1"]
                        )
                    ),
                    styles["Normal"],
                ),
                Paragraph(
                    Parser._concatenate_tags_content(event, ["Ort1"]), styles["Normal"]
                ),
                Paragraph(
                    Parser._concatenate_tags_content(event, ["Kursleiter"]),
                    styles["Normal"],
                ),
                Paragraph(
                    Parser._parse_description(
                        Parser._concatenate_tags_content(event, ["Bezeichnung"]),
                        Parser._concatenate_tags_content(event, ["Bezeichnung2"]),
                        Parser._concatenate_tags_content(event, ["Beschreibung"]),
                        Parser._concatenate_tags_content(event, ["TrainerURL"]),
                    ),
                    styles["Normal"],
                ),
                Paragraph(
                    Parser._concatenate_tags_content(event, ["Zielgruppe"]),
                    styles["Normal"],
                ),
                Paragraph(
                    Parser._parse_prerequisites(
                        Parser._concatenate_tags_content(event, ["Voraussetzung"]),
                        Parser._concatenate_tags_content(event, ["Ausruestung"]),
                        Parser._concatenate_tags_content(event, ["Kurskosten"]),
                        Parser._concatenate_tags_content(event, ["Leistungen"]),
                    ),
                    styles["Normal"],
                ),
            ]
            event = self._creator.create_fixedwidth_table(
                [columns_to_print],
                self._table_styles.get_column_widths(),
                self._table_styles.normal,
            )
            return event
        else:
            warnings.warn("No events found.", RuntimeWarning)

    @staticmethod
    def get_event_categories(event):
        """
        Construct a list of categories from the string gathered out of the xml.

        :param xml.etree.ElementTree.Element event: event for which the categories are
            needed
        :returns: the list of the categories
        :rtype: List[str]
        """
        categories = Parser._concatenate_tags_content(event, ["Kategorie"])
        return categories.split(", ")
