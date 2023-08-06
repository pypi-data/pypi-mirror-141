import datetime
import json
from typing import Optional

import requests

BASE_URL = (
    "https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes"
    "/PreciosCarburantes"
    "/EstacionesTerrestres/{filters}#response-json"
)


class CarbuAPI:
    def build_url(self, *, codprov: Optional[str] = None):
        filters = {}
        if codprov:
            filters["FiltroProvincia"] = codprov

        filtersstr = "/".join([f"{k}/{v}" for (k, v) in filters.items()])

        return BASE_URL.format(filters=filtersstr)

    def fetch(self, url):
        return requests.get(url).text

    def parse(self, buff):
        data = json.loads(buff)
        meta = {
            "Date": datetime.datetime.strptime(data["Fecha"], "%d/%m/%Y %H:%M:%S"),
            "Advisory": data.get("Nota"),
        }

        prices = [self.parse_item(x) for x in data["ListaEESSPrecio"]]

        return {"Meta": meta, "Prices": prices}

    def query(self, *, codprov: Optional[str] = None):
        url = self.build_url(codprov=codprov)
        buffer = self.fetch(url)
        data = self.parse(buffer)

        if data.get("ResultadoConsulta", "").upper() != "OK":
            raise DataError()

    def parse_item(self, item):
        def _float(s):
            return float(s.replace(",", "."))

        # Get prices keys
        prices_keys = [k for k in item if k.lower().startswith("precio")]

        # Extract products
        products = [(k, item.pop(k)) for k in prices_keys]

        # Fix data
        products = [
            (name[7:], _float(value) if value else None) for (name, value) in products
        ]

        # Get longuitude keys
        lngkeys = [k for k in item if k.lower().startswith("longitud")]
        lngkeys = list(sorted(lngkeys, key=lambda x: len(x)))
        longuitude = item[lngkeys[0]]

        for k in lngkeys:
            del item[k]

        ret = {
            "Station": item.pop("Rótulo", None),
            "Products": dict(products),
            "Location": {
                "Latitude": _float(item.pop("Latitud")),
                "Longuitude": _float(longuitude),
                "City": item.pop("Municipio").capitalize(),  # Localidad?
                "Province": item.pop("Provincia").capitalize(),
                "Address": item.pop("Dirección").capitalize(),
            },
            "Misc": item,
        }

        return ret


class _BaseError(Exception):
    pass


class DataError(_BaseError):
    pass
