from parsers.base_parser import BaseExamParser
from parsers.fcc_parser import FCCParser
from parsers.ibfc_parser import IBFCParser
from parsers.uneb_parser import UNEBParser
from parsers.cebraspe_parser import CebraspeParser
from parsers.generic_parser import GenericExamParser
from parsers.gabarito_extractor import GabaritoExtractor

class ExamParserFactory:
    """Fábrica de parsers que seleciona o motor ideal baseado na banca escolhida."""

    @staticmethod
    def get_parser(banca_name, metadata=None):
        metadata = metadata or {}
        b = str(banca_name or "").strip().upper()
        metadata["banca"] = banca_name or "OUTRA"

        if "FCC" in b or "CARLOS CHAGAS" in b:
            return FCCParser(metadata)
        elif "IBFC" in b:
            return IBFCParser(metadata)
        elif "UNEB" in b:
            return UNEBParser(metadata)
        elif "CEBRASPE" in b or "CESPE" in b:
            return CebraspeParser(metadata)
        else:
            return GenericExamParser(metadata)
