import re

from support.entities.tempfile import TempFile
from support.utilities import pdf_utility, qr_decoder


class CheckDataExtractor:

    _path = None

    _text = None

    def __init__(self, path: str):
        self._path = path
        self._text = pdf_utility.extract_text(path)

    def get_all_data(self) -> dict:
        return dict(company_name=self.company_name, pn=self.pn, sn=self.sn, location=self.location,
                    condition=self.condition, receiver=self.receiver, uom=self.uom, exp_date=self.exp_date, po=self.po,
                    cert_source=self.cert_source, rec_date=self.rec_date, mfg=self.mfg, batch=self.batch, dom=self.dom,
                    remark=self.remark, lot=self.lot, tagged_by=self.qr_data, qty=self.qty, notes=self.notes)

    @property
    def qr_data(self):
        tmp = TempFile("temp.jpg")
        pdf_utility.convert_pdf_to_jpg(self._path, tmp.path)
        data = qr_decoder.decode(tmp.path).raw
        tmp.close()
        return data

    @property
    def company_name(self):
        return self._text.split("\n")[0]

    @property
    def pn(self):
        return self.__get_value("PN", "SN")

    @property
    def sn(self):
        return self.__get_value("SN", "DESCRIPTION")

    @property
    def description(self):
        return self.__get_value("DESCRIPTION", "LOCATION")

    @property
    def location(self):
        return self.__get_value("LOCATION", "CONDITION")

    @property
    def condition(self):
        return self.__get_value("CONDITION", "RECEIVER")

    @property
    def receiver(self):
        return self.__get_value("RECEIVER", "UOM")

    @property
    def uom(self):
        return self.__get_value("UOM", "EXP DATE")

    @property
    def exp_date(self):
        return self.__get_value("EXP DATE", "PO")

    @property
    def po(self):
        return self.__get_value("PO", "CERT SOURCE")

    @property
    def cert_source(self):
        return self.__get_value("CERT SOURCE", "REC.DATE")

    @property
    def rec_date(self):
        return self.__get_value("REC.DATE", "MFG")

    @property
    def mfg(self):
        return self.__get_value("MFG", "BATCH")

    @property
    def batch(self):
        return self.__get_value("BATCH", "DOM")

    @property
    def dom(self):
        return self.__get_value("DOM", "REMARK")

    @property
    def remark(self):
        return self.__get_value("REMARK", "LOT")

    @property
    def lot(self):
        return self.__get_value("LOT", "TAGGED BY")

    @property
    def qty(self):
        return self.__get_value("Qty", "NOTES")

    @property
    def notes(self):
        return self.__get_value("NOTES", "(\n.*)+")

    def __get_value(self, key: str, next_key: str):
        return re.search(f"{key}#?\s?:.*\n*{next_key}", self._text)[0].split(next_key)[0].split(":")[1].strip()
