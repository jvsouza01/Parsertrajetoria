package com.enem.parser.service;

import com.enem.parser.model.BackendIngestionPayload;
import com.enem.parser.model.ParsedQuestaoResult;
import com.enem.parser.model.QuestaoPropria;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.File;
import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

@Service
public class BackendSenderService {

    private final ObjectMapper objectMapper;
    private final HttpClient httpClient;

    @Autowired
    public BackendSenderService() {
        this.objectMapper = new ObjectMapper().enable(SerializationFeature.INDENT_OUTPUT);
        this.httpClient = HttpClient.newHttpClient();
    }

    public List<BackendIngestionPayload> formatPayload(List<ParsedQuestaoResult> resultados) {
        List<BackendIngestionPayload> list = new ArrayList<>();

        for (ParsedQuestaoResult res : resultados) {
            QuestaoPropria q = res.questao();
            BackendIngestionPayload p = new BackendIngestionPayload();
            p.setIdOrigem("ENEM_2025_" + q.getIdOrigem());
            p.setFonte("ENEM");
            p.setBanca("INEP");
            p.setAno(2025);
            p.setMateriaNome(mapMateria(q.getMateria(), q.getPosicao()));
            p.setEnunciado(q.getEnunciado());
            String imgUrl = null;
            if (q.getImagemUrl() != null && !q.getImagemUrl().isBlank()) {
                File imgFile = new File(q.getImagemUrl());
                imgUrl = "images/" + imgFile.getName();
            }

            p.setImagemUrl(imgUrl);
            // Garante visibilidade imediata no filtro de Banco de Questoes dos Alunos
            p.setStatusRevisao("APROVADO_AUTO");

            List<BackendIngestionPayload.AlternativaPayload> alts = q.getAlternativas().stream()
                    .map(a -> new BackendIngestionPayload.AlternativaPayload(a.getLetra(), a.getTexto(), a.isCorreta()))
                    .toList();
            p.setAlternativas(alts);

            list.add(p);
        }

        return list;
    }

    public File savePayloadJson(List<BackendIngestionPayload> payloads) throws IOException {
        Path outputDir = Paths.get("output");
        File file = outputDir.resolve("questoes_payload_api.json").toFile();
        objectMapper.writeValue(file, payloads);
        System.out.println("Payload formatado para API salvo em: " + file.getAbsolutePath());
        return file;
    }

    public boolean sendToBackendApi(List<BackendIngestionPayload> payloads, String bearerToken) {
        String apiUrl = "http://localhost:8080/api/admin/ingestao/questoes";
        try {
            String jsonString = objectMapper.writeValueAsString(payloads);

            HttpRequest.Builder reqBuilder = HttpRequest.newBuilder()
                    .uri(URI.create(apiUrl))
                    .header("Content-Type", "application/json")
                    .POST(HttpRequest.BodyPublishers.ofString(jsonString));

            if (bearerToken != null && !bearerToken.isBlank()) {
                reqBuilder.header("Authorization", "Bearer " + bearerToken);
            }

            HttpRequest request = reqBuilder.build();
            HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());

            System.out.println("Status HTTP da API: " + response.statusCode());
            System.out.println("Resposta da API: " + response.body());

            return response.statusCode() == 200 || response.statusCode() == 201;

        } catch (Exception e) {
            System.err.println("Erro ao conectar à API de Ingestão: " + e.getMessage());
            return false;
        }
    }

    private String mapMateria(String area, int posicao) {
        if (area == null) return "Linguagens";
        String a = area.trim().toUpperCase();
        if ("LC".equals(a)) {
            return "Linguagens";
        } else if ("CH".equals(a)) {
            return "Ciências Humanas";
        } else if ("CN".equals(a)) {
            return "Ciências da Natureza";
        } else if ("MT".equals(a)) {
            return "Matemática";
        }
        return "Linguagens";
    }
}
