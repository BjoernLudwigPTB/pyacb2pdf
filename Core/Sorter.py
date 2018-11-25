class Sorter:
    # Taken from [http://effbot.org/zone/element-sort.htm
    # ](http://effbot.org/zone/element-sort.htm) and adapted.

    def __init__(self, doc, courses):
        self._doc = doc
        self._courses = courses

    def sort_parsed_xml(self, sort_key):
        def get_key(course):
            return course.findtext(sort_key)

        self._courses[:] = sorted(self._courses, key=get_key)
        return self._courses[:]
