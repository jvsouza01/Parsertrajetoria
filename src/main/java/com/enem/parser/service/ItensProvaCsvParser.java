package com.enem.parser.service;

import com.enem.parser.model.ItemMeta;
import org.springframework.stereotype.Component;

import java.io.*;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.util.*;

@Component
public class ItensProvaCsvParser {

    public List<ItemMeta> parse(File csvFile) throws IOException {
        Map<String, ItemMeta> porItem = new LinkedHashMap<>(); // dedupe por CO_ITEM

        // UTF-8 default, fallback to ISO-8859-1 if needed
        Charset encoding = StandardCharsets.UTF_8;

        try (BufferedReader reader = new BufferedReader(
                new InputStreamReader(new FileInputStream(csvFile), encoding))) {

            String headerLine = reader.readLine();
            if (headerLine == null) {
                return Collections.emptyList();
            }

            // Remove UTF-8 BOM if present
            if (headerLine.startsWith("\uFEFF")) {
                headerLine = headerLine.substring(1);
            }

            String[] headers = headerLine.split(";");
            Map<String, Integer> colMap = new HashMap<>();
            for (int i = 0; i < headers.length; i++) {
                colMap.put(headers[i].trim().toUpperCase(), i);
            }

            int idxPosicao = colMap.getOrDefault("CO_POSICAO", 0);
            int idxArea = colMap.getOrDefault("SG_AREA", 1);
            int idxItem = colMap.getOrDefault("CO_ITEM", 2);
            int idxGabarito = colMap.getOrDefault("TX_GABARITO", 3);
            int idxHabilidade = colMap.getOrDefault("CO_HABILIDADE", 4);
            int idxCor = colMap.getOrDefault("TX_COR", 10);
            int idxProva = colMap.getOrDefault("CO_PROVA", 11);
            int idxLingua = colMap.getOrDefault("TP_LINGUA", 12);

            String linha;
            while ((linha = reader.readLine()) != null) {
                if (linha.isBlank()) continue;
                String[] col = linha.split(";", -1);

                if (col.length <= idxItem) continue;

                String coItem = col[idxItem].trim();
                if (coItem.isEmpty()) continue;

                int coPosicao = 0;
                try {
                    coPosicao = Integer.parseInt(col[idxPosicao].trim());
                } catch (NumberFormatException ignored) {}

                String sgArea = col.length > idxArea ? col[idxArea].trim() : "";
                String txGabarito = col.length > idxGabarito ? col[idxGabarito].trim() : "";
                String coHabilidade = col.length > idxHabilidade ? col[idxHabilidade].trim() : "";
                String txCor = col.length > idxCor ? col[idxCor].trim() : "";
                String coProva = col.length > idxProva ? col[idxProva].trim() : "";
                String tpLingua = col.length > idxLingua ? col[idxLingua].trim() : "";

                porItem.putIfAbsent(coItem, new ItemMeta(
                    coItem,
                    sgArea,
                    txGabarito,
                    coHabilidade,
                    coPosicao,
                    txCor,
                    coProva,
                    tpLingua
                ));
            }
        }

        return new ArrayList<>(porItem.values());
    }
}
