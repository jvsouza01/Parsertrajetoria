package com.enem.parser.service;

import com.enem.parser.model.ItemMeta;
import org.junit.jupiter.api.Test;
import java.io.File;
import java.io.IOException;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class ItensProvaCsvParserTest {

    @Test
    void testParseCsv() throws IOException {
        File csvFile = new File("microdados_enem_2025/DADOS/ITENS_PROVA_2025.csv");
        assertTrue(csvFile.exists(), "CSV file must exist");

        ItensProvaCsvParser parser = new ItensProvaCsvParser();
        List<ItemMeta> items = parser.parse(csvFile);

        assertNotNull(items);
        assertFalse(items.isEmpty(), "Parsed items list should not be empty");

        ItemMeta firstItem = items.get(0);
        assertNotNull(firstItem.coItem());
        assertNotNull(firstItem.sgArea());
        assertNotNull(firstItem.txGabarito());
    }
}
