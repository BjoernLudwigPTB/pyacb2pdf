from pytest import fixture, approx

from pyxml2pdf.PdfVisualisation.TableStyle import TableStyle


@fixture
def table_style():
    return TableStyle()


def test_column_widths(table_style):
    assert sum(table_style.column_widths) == approx(table_style.table_width)
