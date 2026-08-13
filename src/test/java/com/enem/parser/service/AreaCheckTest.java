package com.enem.parser.service;

import com.enem.parser.model.ItemMeta;
import org.junit.jupiter.api.Test;

import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class AreaCheckTest {

    @Test
    void inspectAreasAndColors() throws IOException {
        File csvFile = new File("microdados_enem_2025/DADOS/ITENS_PROVA_2025.csv");
        ItensProvaCsvParser parser = new ItensProvaCsvParser();
        List<ItemMeta> items = parser.parse(csvFile);

        System.out.println("Total deduplicated items: " + items.size());

        Map<String, Long> areaCounts = items.stream()
                .collect(Collectors.groupingBy(ItemMeta::sgArea, Collectors.counting()));
        System.out.println("=== ITEM COUNTS BY SG_AREA ===");
        areaCounts.forEach((area, count) -> System.out.println(area + ": " + count));

        Map<String, Long> colorCounts = items.stream()
                .collect(Collectors.groupingBy(ItemMeta::txCor, Collectors.counting()));
        System.out.println("=== ITEM COUNTS BY TX_COR ===");
        colorCounts.forEach((color, count) -> System.out.println(color + ": " + count));
    }
}
