package com.enem.parser.service;

import com.enem.parser.model.ItemMeta;
import org.junit.jupiter.api.Test;

import java.io.File;
import java.io.IOException;
import java.util.List;

public class FilterTest {

    @Test
    void testFilterForDia1Branca() throws IOException {
        File csvFile = new File("microdados_enem_2025/DADOS/ITENS_PROVA_2025.csv");
        ItensProvaCsvParser parser = new ItensProvaCsvParser();
        List<ItemMeta> items = parser.parse(csvFile);

        List<ItemMeta> dia1Branca = items.stream()
                .filter(i -> "BRANCA".equalsIgnoreCase(i.txCor()))
                .filter(i -> "LC".equalsIgnoreCase(i.sgArea()) || "CH".equalsIgnoreCase(i.sgArea()))
                .toList();

        System.out.println("Items matching BRANCA and (LC or CH): " + dia1Branca.size());
        dia1Branca.forEach(i -> System.out.println("Pos: " + i.coPosicao() + " | Area: " + i.sgArea() + " | Item: " + i.coItem() + " | Gabarito: " + i.txGabarito()));
    }
}
