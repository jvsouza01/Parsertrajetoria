package com.enem.parser.service;

import com.enem.parser.model.*;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.*;

@Service
public class EnemIngestionRunner {

    private final ItensProvaCsvParser csvParser;
    private final QuestaoTextExtractor textExtractor;
    private final QuestaoImageExtractor imageExtractor;
    private final CadernoMapper cadernoMapper;
    private final BackendSenderService backendSenderService;
    private final ObjectMapper objectMapper;

    @Autowired
    public EnemIngestionRunner(
            ItensProvaCsvParser csvParser,
            QuestaoTextExtractor textExtractor,
            QuestaoImageExtractor imageExtractor,
            CadernoMapper cadernoMapper,
            BackendSenderService backendSenderService) {
        this.csvParser = csvParser;
        this.textExtractor = textExtractor;
        this.imageExtractor = imageExtractor;
        this.cadernoMapper = cadernoMapper;
        this.backendSenderService = backendSenderService;
        this.objectMapper = new ObjectMapper().enable(SerializationFeature.INDENT_OUTPUT);
    }

    public List<ParsedQuestaoResult> executarIngestao(File csvFile, File defaultPdfFile) throws IOException {
        System.out.println("=== INICIANDO PARSER DE INGESTÃO ENEM (COM FILTRAGEM ESTRITA) ===");
        System.out.println("Lendo CSV: " + csvFile.getAbsolutePath());

        List<ItemMeta> itens = csvParser.parse(csvFile);
        System.out.println("Total de itens deduplicados carregados do CSV: " + itens.size());

        List<ParsedQuestaoResult> resultados = new ArrayList<>();

        Path outputDir = Paths.get("output");
        Path imagesDir = outputDir.resolve("images");
        Files.createDirectories(imagesDir);

        Map<String, PDDocument> pdfCache = new HashMap<>();
        Map<String, List<QuestaoTextExtractor.QuestionHeaderPos>> indexCache = new HashMap<>();

        File baseDir = csvFile.getParentFile() != null && csvFile.getParentFile().getParentFile() != null
                ? csvFile.getParentFile().getParentFile().getParentFile()
                : new File(".");

        try {
            int processadosSucesso = 0;
            int requeremRevisao = 0;
            int ignoradosSemPdf = 0;

            for (ItemMeta meta : itens) {
                int dia = resolveDiaPorArea(meta.sgArea());
                String expectedPdfName = cadernoMapper.resolvePdfFileName(meta.txCor(), dia);

                File targetPdfFile = null;
                if (expectedPdfName != null) {
                    targetPdfFile = new File(baseDir, expectedPdfName);
                    if (!targetPdfFile.exists()) {
                        targetPdfFile = new File(".", expectedPdfName);
                    }
                }

                if ((targetPdfFile == null || !targetPdfFile.exists()) && defaultPdfFile != null && defaultPdfFile.exists()) {
                    if (isPdfCompatibleWithItem(defaultPdfFile.getName(), meta.txCor(), dia)) {
                        targetPdfFile = defaultPdfFile;
                    }
                }

                if (targetPdfFile == null || !targetPdfFile.exists()) {
                    ignoradosSemPdf++;
                    continue;
                }

                String pdfKey = targetPdfFile.getName();
                if (!pdfCache.containsKey(pdfKey)) {
                    System.out.println("Carregando PDF: " + pdfKey);
                    PDDocument doc = PDDocument.load(targetPdfFile);
                    pdfCache.put(pdfKey, doc);
                    indexCache.put(pdfKey, textExtractor.indexarQuestoes(doc));
                }

                PDDocument docToUse = pdfCache.get(pdfKey);
                List<QuestaoTextExtractor.QuestionHeaderPos> indexToUse = indexCache.get(pdfKey);

                Bounds bounds = textExtractor.localizarQuestao(docToUse, indexToUse, meta.coPosicao(), meta.tpLingua());
                if (bounds == null) {
                    continue;
                }

                String textoBruto = textExtractor.extrairTexto(docToUse, bounds);
                QuestaoTextExtractor.ParsedTextResult parsedText = textExtractor.parseTextoEAlternativas(textoBruto, meta.txGabarito());

                byte[] imagemBytes = imageExtractor.extrairImagemDaQuestao(docToUse, bounds);
                String imagemPathStr = null;
                if (imagemBytes.length > 0) {
                    File imgFile = imagesDir.resolve(meta.coItem() + ".png").toFile();
                    try (FileOutputStream fos = new FileOutputStream(imgFile)) {
                        fos.write(imagemBytes);
                    }
                    imagemPathStr = imgFile.getCanonicalPath();

                    // Copia a imagem também para o frontend em trajetoria-web/public/images/
                    try {
                        Path webPublicImagesDir = Paths.get("..", "tragetoria_full", "trajetoria-web", "public", "images");
                        Files.createDirectories(webPublicImagesDir);
                        Files.copy(imgFile.toPath(), webPublicImagesDir.resolve(imgFile.getName()), java.nio.file.StandardCopyOption.REPLACE_EXISTING);
                    } catch (Exception ignored) {}
                }

                QuestaoPropria q = new QuestaoPropria();
                q.setIdOrigem(meta.coItem());
                q.setFonte("ENEM");
                q.setMateria(meta.sgArea());
                q.setCoHabilidade(meta.coHabilidade());
                q.setPosicao(meta.coPosicao());
                q.setEnunciado(parsedText.enunciado());
                q.setAlternativas(parsedText.alternativas());
                q.setImagemUrl(imagemPathStr);
                q.setPrecisaRevisaoManual(parsedText.precisaRevisao());

                if (parsedText.precisaRevisao()) {
                    requeremRevisao++;
                } else {
                    processadosSucesso++;
                }

                resultados.add(new ParsedQuestaoResult(q, textoBruto, imagemBytes, bounds, parsedText.motivoRevisao()));
            }

            System.out.printf("=== PROCESSAMENTO CONCLUÍDO (FILTRAGEM VALIDADA) ===%n");
            System.out.printf("Total CSV: %d | Extraídas do PDF correto: %d | Sucesso: %d | Revisão: %d | Ignorados (Sem PDF): %d%n",
                    itens.size(), resultados.size(), processadosSucesso, requeremRevisao, ignoradosSemPdf);

            // Exportar JSON com apenas as QuestaoPropria efetivamente extraídas dos PDFs corretos
            List<QuestaoPropria> apenasQuestoes = resultados.stream().map(ParsedQuestaoResult::questao).toList();
            File jsonFile = outputDir.resolve("questoes_extraidas.json").toFile();
            objectMapper.writeValue(jsonFile, apenasQuestoes);
            System.out.println("Resultado filtrado e validado salvo em: " + jsonFile.getAbsolutePath());

            // Gerar Payload exatamente na estrutura esperada pela API Backend (POST /api/admin/ingestao/questoes)
            List<BackendIngestionPayload> apiPayloads = backendSenderService.formatPayload(resultados);
            File payloadFile = backendSenderService.savePayloadJson(apiPayloads);

            System.out.println("Formato para API gerado com sucesso em: " + payloadFile.getAbsolutePath());

        } finally {
            for (PDDocument doc : pdfCache.values()) {
                doc.close();
            }
        }

        return resultados;
    }

    private int resolveDiaPorArea(String area) {
        if (area == null) return 1;
        String a = area.trim().toUpperCase();
        if (a.equals("CN") || a.equals("MT")) {
            return 2;
        }
        return 1;
    }

    private boolean isPdfCompatibleWithItem(String pdfFileName, String corItem, int diaItem) {
        if (pdfFileName == null) return false;
        String upperName = pdfFileName.toUpperCase();
        boolean matchesDia = upperName.contains("D" + diaItem);
        Integer numCaderno = cadernoMapper.getNumeroCaderno(corItem, diaItem);
        boolean matchesCaderno = (numCaderno != null) && upperName.contains("CD" + numCaderno);
        return matchesDia && matchesCaderno;
    }
}
