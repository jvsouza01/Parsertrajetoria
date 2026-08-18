package com.enem.parser.model;

import com.fasterxml.jackson.annotation.JsonInclude;
import java.util.List;

@JsonInclude(JsonInclude.Include.NON_NULL)
public class BackendIngestionPayload {
    private String idOrigem;
    private String fonte = "CONCURSO"; // "CONCURSO", "ENEM", "PROPRIA"
    private String banca = "UNEB";
    private String orgao = "Polícia Militar da Bahia - PMBA";
    private String cargo = "Oficial da PM (CFOPM) - Caderno 1";
    private int ano = 2025;
    private String materiaNome;
    private String dificuldade = "MODERADO"; // "FACIL", "MODERADO", "DIFICIL"
    private String enunciado;
    private String imagemUrl = null;
    private List<AlternativaPayload> alternativas;

    public BackendIngestionPayload() {}

    public BackendIngestionPayload(
            String idOrigem,
            String fonte,
            String banca,
            String orgao,
            String cargo,
            int ano,
            String materiaNome,
            String dificuldade,
            String enunciado,
            String imagemUrl,
            List<AlternativaPayload> alternativas) {
        this.idOrigem = idOrigem;
        this.fonte = fonte;
        this.banca = banca;
        this.orgao = orgao;
        this.cargo = cargo;
        this.ano = ano;
        this.materiaNome = materiaNome;
        this.dificuldade = dificuldade;
        this.enunciado = enunciado;
        this.imagemUrl = imagemUrl;
        this.alternativas = alternativas;
    }

    public String getIdOrigem() {
        return idOrigem;
    }

    public void setIdOrigem(String idOrigem) {
        this.idOrigem = idOrigem;
    }

    public String getFonte() {
        return fonte;
    }

    public void setFonte(String fonte) {
        this.fonte = fonte;
    }

    public String getBanca() {
        return banca;
    }

    public void setBanca(String banca) {
        this.banca = banca;
    }

    public String getOrgao() {
        return orgao;
    }

    public void setOrgao(String orgao) {
        this.orgao = orgao;
    }

    public String getCargo() {
        return cargo;
    }

    public void setCargo(String cargo) {
        this.cargo = cargo;
    }

    public int getAno() {
        return ano;
    }

    public void setAno(int ano) {
        this.ano = ano;
    }

    public String getMateriaNome() {
        return materiaNome;
    }

    public void setMateriaNome(String materiaNome) {
        this.materiaNome = materiaNome;
    }

    public String getDificuldade() {
        return dificuldade;
    }

    public void setDificuldade(String dificuldade) {
        this.dificuldade = dificuldade;
    }

    public String getEnunciado() {
        return enunciado;
    }

    public void setEnunciado(String enunciado) {
        this.enunciado = enunciado;
    }

    public String getImagemUrl() {
        return imagemUrl;
    }

    public void setImagemUrl(String imagemUrl) {
        this.imagemUrl = imagemUrl;
    }

    public List<AlternativaPayload> getAlternativas() {
        return alternativas;
    }

    public void setAlternativas(List<AlternativaPayload> alternativas) {
        this.alternativas = alternativas;
    }

    public static class AlternativaPayload {
        private String letra;
        private String texto;
        private boolean correta;

        public AlternativaPayload() {}

        public AlternativaPayload(String letra, String texto, boolean correta) {
            this.letra = letra;
            this.texto = texto;
            this.correta = correta;
        }

        public String getLetra() {
            return letra;
        }

        public void setLetra(String letra) {
            this.letra = letra;
        }

        public String getTexto() {
            return texto;
        }

        public void setTexto(String texto) {
            this.texto = texto;
        }

        public boolean isCorreta() {
            return correta;
        }

        public void setCorreta(boolean correta) {
            this.correta = correta;
        }
    }
}
