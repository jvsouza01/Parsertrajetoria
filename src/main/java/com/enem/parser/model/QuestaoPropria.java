package com.enem.parser.model;

import java.util.ArrayList;
import java.util.List;

public class QuestaoPropria {
    private String idOrigem; // ex: PMBA_CFOPM_2025_Q01 ou coItem ENEM
    private String fonte = "CONCURSO"; // "CONCURSO", "ENEM", "VESTIBULAR"
    private String banca = "UNEB";
    private String orgao = "Polícia Militar da Bahia - PMBA";
    private String cargo = "Oficial da PM (CFOPM)";
    private int ano = 2025;
    private String materia; // ex: "Língua Portuguesa", "Direito", "Matemática", "LC", "CH"
    private String areaConhecimento; // ex: "Linguagens", "Ciências Humanas", "Direito", "Matemática", "Informática"
    private String assunto; // ex: "Crase", "Direito Penal Militar - Deserção", "Funções Polinomiais"
    private String dificuldade = "MEDIO"; // "FACIL", "MEDIO", "DIFICIL"
    private String tipoQuestao = "MULTIPLA_ESCOLHA"; // "MULTIPLA_ESCOLHA", "CERTO_ERRADO", "DISCURSIVA"
    private String coHabilidade;
    private int posicao;
    private String textoBase; // Texto de apoio/motivação que serve de base para o item
    private String enunciado;
    private String imagemUrl;
    private String gabaritoOficial;
    private boolean anulada = false;
    private boolean precisaRevisaoManual;
    private List<AlternativaQuestaoPropria> alternativas = new ArrayList<>();

    public QuestaoPropria() {}

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

    public String getMateria() {
        return materia;
    }

    public void setMateria(String materia) {
        this.materia = materia;
    }

    public String getAreaConhecimento() {
        return areaConhecimento;
    }

    public void setAreaConhecimento(String areaConhecimento) {
        this.areaConhecimento = areaConhecimento;
    }

    public String getAssunto() {
        return assunto;
    }

    public void setAssunto(String assunto) {
        this.assunto = assunto;
    }

    public String getDificuldade() {
        return dificuldade;
    }

    public void setDificuldade(String dificuldade) {
        this.dificuldade = dificuldade;
    }

    public String getTipoQuestao() {
        return tipoQuestao;
    }

    public void setTipoQuestao(String tipoQuestao) {
        this.tipoQuestao = tipoQuestao;
    }

    public String getCoHabilidade() {
        return coHabilidade;
    }

    public void setCoHabilidade(String coHabilidade) {
        this.coHabilidade = coHabilidade;
    }

    public int getPosicao() {
        return posicao;
    }

    public void setPosicao(int posicao) {
        this.posicao = posicao;
    }

    public String getTextoBase() {
        return textoBase;
    }

    public void setTextoBase(String textoBase) {
        this.textoBase = textoBase;
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

    public String getGabaritoOficial() {
        return gabaritoOficial;
    }

    public void setGabaritoOficial(String gabaritoOficial) {
        this.gabaritoOficial = gabaritoOficial;
    }

    public boolean isAnulada() {
        return anulada;
    }

    public void setAnulada(boolean anulada) {
        this.anulada = anulada;
    }

    public boolean isPrecisaRevisaoManual() {
        return precisaRevisaoManual;
    }

    public void setPrecisaRevisaoManual(boolean precisaRevisaoManual) {
        this.precisaRevisaoManual = precisaRevisaoManual;
    }

    public List<AlternativaQuestaoPropria> getAlternativas() {
        return alternativas;
    }

    public void setAlternativas(List<AlternativaQuestaoPropria> alternativas) {
        this.alternativas = alternativas;
    }
}
