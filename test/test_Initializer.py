import pytest

from Core.Initializer import Initializer


@pytest.fixture
def download():
    from Core.Downloader import Downloader
    dl = Downloader('https://alpinclub-berlin.de/kv/kursdaten.xml')
    dl.download('input/kursdaten.xml')


def test_initializer_init():
    Initializer()


def test_initializer_build(download):
    from Core.Parser import Signature

    input_folder = 'input/'
    xml_filename = 'kursdaten.xml'
    input_path = input_folder + xml_filename
    properties_filename = 'kursdaten_prop.properties'
    properties_path = input_folder + properties_filename
    output_folder = 'output/'
    output_filename = 'kursdaten.pdf'
    output_path = output_folder + output_filename
    init = Initializer()
    init.build(input_path, output_path, properties_path, Signature.AUTO_DATE)