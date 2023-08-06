from dtamg_py.utils import extract_resources
from unittest.mock import Mock
from frictionless import Package

descriptor = {
  "profile": "data-package", "name": "reprex",
  "resources": [
    {"name": "dm_unidade_orc", "path": "dm_unidade_orc.csv"},
    {"name": "ft_receita_v2018", "path": "ft_receita_v2018.csv"},
    {"name": "ft_convenio_entrada", "path": "ft_convenio_entrada.csv"},
  ]
}

datapackage = Package(descriptor)

datapackage.resources

def test_extract_resources():



# def test_is_dataset_published_exception(mocked):
#     mocked.side_effect = Exception()
#     with pytest.raises(Exception):
#         is_dataset_published(ckan, 'reprex')