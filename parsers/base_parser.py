import re
import html

class BaseExamParser:
    """Classe base para todos os parsers de bancas de concursos e vestibulares."""

    def __init__(self, metadata=None):
        self.metadata = metadata or {}
        self.banca = self.metadata.get("banca", "OUTRA")
        self.orgao = self.metadata.get("orgao", "")
        self.cargo = self.metadata.get("cargo", "")
        self.ano = int(self.metadata.get("ano", 2025)) if str(self.metadata.get("ano", "")).isdigit() else 2025
        self.fonte = self.metadata.get("fonte", "CONCURSO")

    def clean_text(self, text):
        """Limpa ruídos de extração de PDF mantendo quebras de parágrafo significativas."""
        if not text:
            return ""
        # Normaliza quebras de linha e caracteres especiais
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        # Remove caracteres de controle estranhos exceto tabs e newlines
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
        # Substitui traços/hífens especiais
        text = text.replace('−', '-').replace('–', '-').replace('—', '-')
        # Remove espaços múltiplos horizontais
        text = re.sub(r'[ \t]+', ' ', text)
        return text.strip()

    def parse_pdf(self, pdf_path_or_stream, gabarito_map=None, disciplina_map=None):
        """Método principal a ser implementado por cada parser específico."""
        raise NotImplementedError("Cada parser de banca deve implementar parse_pdf.")

    def format_to_payload(self, questoes):
        """Converte a lista de dicionários internos para o formato oficial IngestaoQuestaoInput da API Trajetória."""
        payload = []
        for q in questoes:
            pos = q.get("posicao") or q.get("pos", 1)
            pos_str = f"{int(pos):02d}"
            
            # Gera ID de origem padronizado
            banca_clean = re.sub(r'[^A-Z0-9]', '', self.banca.upper()) or "GEN"
            cargo_clean = re.sub(r'[^A-Z0-9]', '_', self.cargo.upper())[:15] if self.cargo else "PROVA"
            id_origem = q.get("idOrigem") or f"{banca_clean}_{self.ano}_{cargo_clean}_Q{pos_str}"
            
            # Enunciado e Texto-base
            enunciado = q.get("enunciado", "").strip()
            texto_base = q.get("textoBase") or q.get("base") or q.get("textoApoio") or ""
            texto_base_str = str(texto_base).strip() if texto_base else None

            # Alternativas
            alts_raw = q.get("alternativas", [])
            alternativas = []
            gab_oficial = str(q.get("gabaritoOficial") or q.get("gab", "")).upper()
            is_anulada = q.get("anulada", False) or (gab_oficial in ["*", "X", "T", "ANULADA"])

            for alt in alts_raw:
                if isinstance(alt, tuple) or isinstance(alt, list):
                    letra = str(alt[0]).upper()
                    texto_alt = str(alt[1]).strip()
                elif isinstance(alt, dict):
                    letra = str(alt.get("letra", "")).upper()
                    texto_alt = str(alt.get("texto", "")).strip()
                else:
                    continue

                is_correta = False if is_anulada else (letra == gab_oficial)
                alternativas.append({
                    "letra": letra,
                    "texto": texto_alt,
                    "correta": is_correta
                })

            materia_raw = q.get("materia") or q.get("disciplina") or q.get("materiaNome")
            materia_final = str(materia_raw).strip() if materia_raw and str(materia_raw).strip() not in ["", "null", "None", "Geral"] else None

            payload.append({
                "idOrigem": id_origem,
                "posicao": int(pos),
                "fonte": self.fonte,
                "banca": self.banca,
                "orgao": self.orgao if self.orgao else None,
                "cargo": self.cargo if self.cargo else None,
                "ano": self.ano,
                "materiaNome": materia_final,
                "assunto": q.get("assunto") or None,
                "textoBase": texto_base_str,
                "enunciado": enunciado,
                "imagemUrl": q.get("imagemUrl", None),
                "temImagem": bool(q.get("temImagem", False)),
                "descricaoImagem": q.get("descricaoImagem"),
                "gabaritoOficial": gab_oficial if not is_anulada else "*",
                "anulada": is_anulada,
                "alternativas": alternativas
            })

        return payload
