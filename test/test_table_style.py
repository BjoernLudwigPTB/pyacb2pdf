from PdfVisualisation.TableStyle import TableStyle
from pytest import fixture, approx


@fixture
def table_style():
    return TableStyle()


def test_column_widths(table_style):
    assert sum(table_style.column_widths) == approx(table_style.table_width)
