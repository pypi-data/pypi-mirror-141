from typing import Dict, Union

import aiohttp
import requests

__all__ = ("KoronavirusVeriHatasi", "korona", "async_korona")

KoronavirusVerisi = Dict[str, Union[float, int, str]]
sozluk: Dict[str, str] = {
    "updated": "son_güncelleme",
    "cases": "vaka",
    "todayCases": "bugünkü_vaka",
    "deaths": "ölüm",
    "todayDeaths": "bugünkü_ölüm",
    "recovered": "iyileşen",
    "todayRecovered": "bugünkü_iyileşen",
    "active": "aktif_vaka",
    "critical": "kritik",
    "casesPerOneMillion": "milyon_başı_vaka",
    "deathsPerOneMillion": "milyon_başı_ölüm",
    "tests": "test",
    "testsPerOneMillion": "milyon_başı_test",
    "population": "nüfus",
    "continent": "kıta",
}
URL = "https://disease.sh/v3/covid-19/countries/{ulke}?yesterday=0&twoDaysAgo=0"


class KoronavirusVeriHatasi(BaseException):
    def __init__(self, response) -> None:
        super().__init__(f"Bir hata oluştu: {response['message']}")


def turkcelestir(data: KoronavirusVerisi) -> KoronavirusVerisi:
    turkce_data = {}
    for key in data.keys():
        try:
            turkce_data[sozluk[key]] = data[key]
        except KeyError:
            continue

    return turkce_data


def korona(ulke: str = "Turkey") -> KoronavirusVerisi:
    response = requests.get(URL.format(ulke=ulke))
    r = response.json()
    if response.status_code != 200:
        raise KoronavirusVeriHatasi(r)

    return turkcelestir(r)


async def async_korona(ulke: str = "Turkey") -> KoronavirusVerisi:
    async with aiohttp.ClientSession() as ses:
        response = await ses.get(URL.format(ulke=ulke))
    r = await response.json()
    if response.status != 200:
        raise KoronavirusVeriHatasi(r)

    return turkcelestir(r)
