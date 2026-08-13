package com.enem.parser.service;

import org.springframework.stereotype.Component;

import java.util.Map;

@Component
public class CadernoMapper {

    // Dia 1: LC + CH. Confirmado: CD3 = BRANCA
    private static final Map<String, Integer> CADERNO_POR_COR_DIA1 = Map.of(
        "AZUL", 1,
        "AMARELA", 2,
        "BRANCA", 3,
        "ROSA", 4
    );

    // Dia 2: CN + MT.
    private static final Map<String, Integer> CADERNO_POR_COR_DIA2 = Map.of(
        "AMARELA", 5,
        "CINZA", 6,
        "AZUL", 7,
        "ROSA", 8
    );

    public Integer getNumeroCaderno(String cor, int dia) {
        if (cor == null) return null;
        String normalizedCor = cor.trim().toUpperCase();
        if (dia == 1) {
            return CADERNO_POR_COR_DIA1.get(normalizedCor);
        } else if (dia == 2) {
            return CADERNO_POR_COR_DIA2.get(normalizedCor);
        }
        return null;
    }

    public String resolvePdfFileName(String cor, int dia) {
        Integer cd = getNumeroCaderno(cor, dia);
        if (cd == null) {
            return null;
        }
        return String.format("2025_PV_impresso_D%d_CD%d.pdf", dia, cd);
    }
}
