from reportlab.lib import colors
from reportlab.platypus import Paragraph

from PdfVisualisation.Styles import Styles
from PdfVisualisation.TableStyle import TableStyle
from model.tables.Creator import Creator
from model.tables.EventTable import EventTable


class TableBuilder:
    def __init__(self, properties, styles):
        self._styles = styles
        self._creator = Creator()
        self._prop = properties
        self._settings = self._parse_properties()
        self._table_styles = TableStyle()
        self._course = None
        self._subtables = self.create_subtables()

    @staticmethod
    def _parse_properties():
        """
        Extract all configuration information from properties file and set
        up a dict containing all this information. Later at least it will
        extract it... TODO extract actual information with something like
        settings = open(properties).read().split("\n")
        settings_dict = dict()
        properties = self._prop
        :return List(List(str)): the list with all configuration data out of
            properties file
        """

        return [[
            'Wandern im Hoch - und Mittelgebirge', [
                'Hochgebirge', 'Mittelgebirge'], [
                'Wandern']], [
            'Klettern und Bouldern im Mittelgebirge', [
                'Mittelgebirge'], [
                'Klettern', 'Bouldern']], [
            'Ausbildung, Wandern und Klettern in Berlin', [
                'in Berlin'], [
                'Grundlagenkurs', 'Wandern', 'Klettern']], [
            'Mountainbiken', [
                'in Berlin', 'Hochgebirge', 'Mittelgebirge'], [
                'Mountainbiken']], [
            'Bergsteigen, Hochtouren und Klettern im Hochgebirge', [
                'Hochgebirge'], [
                'Bergsteigen', 'Hochtouren', 'Klettern']], [
            'Veranstaltungen für Familien', [
                'in Berlin', 'Hochgebirge', 'Mittelgebirge'], [
                'Familie']], [
            'Jugendgruppen und -events', [
                'in Berlin', 'Hochgebirge', 'Mittelgebirge'], [
                'Jugend']]]

    def create_subtables(self):
        """
        Create subtables for all different kinds of events.

        :return list[EventTable]: contains a list with all event tables to be
            able to brows through them
        """

        event_tables = []
        for heading in self._settings:
            event_table = EventTable(heading[0], heading[1], heading[2])
            headers = self.make_headers(heading[0])
            for header in headers:
                event_table.add_event(header)
            event_tables.append(event_table)
        return event_tables

    def make_headers(self, main_header):
        """
        Create the beginning of a subtable with the main and the subheaders.

        :param str main_header: the name of the main table section to attach
            the headers to
        :return List[reportlab.platypus.Table]: two line table with all headers
            needed
        """
        headers = [self._creator.create_table_fixed([[Paragraph(
            main_header, self._styles['Heading1'])]],
            self._table_styles.table_width,
            next(self._table_styles.heading_iterator, Styles.background(
                colors.crimson)))]
        headings = ['Art', 'Datum', 'Ort', 'Leitung', 'Beschreibung',
                    'Zielgruppe',
                    'Voraussetzungen', 'mehr Infos unter']
        columns = []

        for heading in headings:
            columns.append(Paragraph(heading, self._styles['Heading2']))
        headers.append(self._creator.create_table_fixed(
            [columns], self._table_styles.column_widths,
            self._table_styles.sub_heading))
        return headers

    def collect_subtables(self):
        aggregated_subtables = []
        for table in self._subtables:
            for element in table.get_elements():
                aggregated_subtables.append(element)
        return aggregated_subtables

    def distribute_events(self, event, categories):
        set_of_cats = set(categories)
        for subtable in self._subtables:
            _locations = subtable.get_locations()
            _activities = subtable.get_activities()
            if set_of_cats.intersection(_activities):
                if set_of_cats.intersection(_locations):
                    subtable.add_event(event)
