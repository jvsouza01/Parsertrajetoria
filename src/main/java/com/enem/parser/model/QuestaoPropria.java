package com.enem.parser.model;

import java.util.ArrayList;
import java.util.List;

public class QuestaoPropria {
    private String idOrigem; // coItem
    private String fonte = "ENEM";
    private String materia; // sgArea (LC, CH, CN, MT)
    private String coHabilidade;
    private int posicao;
    private String enunciado;
    private String imagemUrl;
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

    public String getMateria() {
        return materia;
    }

    public void setMateria(String materia) {
        this.materia = materia;
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
