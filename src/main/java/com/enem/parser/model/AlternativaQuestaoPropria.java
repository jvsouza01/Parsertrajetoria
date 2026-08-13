package com.enem.parser.model;

public class AlternativaQuestaoPropria {
    private String letra;
    private String texto;
    private boolean isCorreta;

    public AlternativaQuestaoPropria() {}

    public AlternativaQuestaoPropria(String letra, String texto, boolean isCorreta) {
        this.letra = letra;
        this.texto = texto;
        this.isCorreta = isCorreta;
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
        return isCorreta;
    }

    public void setCorreta(boolean correta) {
        isCorreta = correta;
    }
}
