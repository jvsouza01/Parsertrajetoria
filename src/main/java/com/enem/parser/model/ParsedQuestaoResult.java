package com.enem.parser.model;

public record ParsedQuestaoResult(
    QuestaoPropria questao,
    String textoBruto,
    byte[] imagemBytes,
    Bounds bounds,
    String erroOuAviso
) {}
