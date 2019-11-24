from typing import List


class Sorter:
    """Provides a method to sort from xml extracted data by a tag containing a date

    We took `effbot.org <http://effbot.org/zone/element-sort.htm>`_ and adapted the
    code to our needs of sorting a list of :py:class:`xml.etree.ElementTree.Element`
    by the texts of one of their tags containing a string representation of a date.

    :param List[xml.etree.ElementTree.Element] courses: events that where extracted
        from an xml source
    """

    def __init__(self, courses):
        self._courses = courses

    def sort_parsed_xml(self, keys):
        """Sort a list of :py:class:`xml.etree.ElementTree.Element` by their date

        Taken from `effbot.org <http://effbot.org/zone/element-sort.htm>`_ and
        adapted. The sorting will be done in the order of the keys.

        :param List[str] keys: a list of xml tags which contain the
            data
        """

        def get_key(course):
            return tuple(course.findtext(key) for key in keys)

        self._courses[:] = sorted(self._courses, key=get_key)
        return self._courses[:]
