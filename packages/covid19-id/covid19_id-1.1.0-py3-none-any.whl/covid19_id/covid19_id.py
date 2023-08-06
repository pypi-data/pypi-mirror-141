import cattr

from covid19_id.utils import _get_data, register_hooks
from . import UpdateCovid19
from . import DataProvinsi
from . import PemeriksaanVaksinasi
from . import Data

register_hooks()


def get_update(
    url: str = "https://data.covid19.go.id/public/api/update.json",
) -> UpdateCovid19:
    data = _get_data(url)
    return cattr.structure(data, UpdateCovid19)


def get_prov(
    url: str = "https://data.covid19.go.id/public/api/prov.json",
) -> DataProvinsi:
    data = _get_data(url)
    return cattr.structure(data, DataProvinsi)


def get_pemeriksaan_vaksinasi(
    url: str = "https://data.covid19.go.id/public/api/pemeriksaan-vaksinasi.json",
) -> PemeriksaanVaksinasi:
    data = _get_data(url)
    return cattr.structure(data, PemeriksaanVaksinasi)


def get_data(
    url: str = "https://data.covid19.go.id/public/api/data.json",
) -> Data:
    data = _get_data(url)
    return cattr.structure(data, Data)
