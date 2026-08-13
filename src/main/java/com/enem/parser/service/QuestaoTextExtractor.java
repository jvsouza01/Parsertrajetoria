package com.enem.parser.service;

import com.enem.parser.model.AlternativaQuestaoPropria;
import com.enem.parser.model.Bounds;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.pdmodel.PDPage;
import org.apache.pdfbox.text.PDFTextStripper;
import org.apache.pdfbox.text.PDFTextStripperByArea;
import org.apache.pdfbox.text.TextPosition;
import org.springframework.stereotype.Component;

import java.awt.geom.Rectangle2D;
import java.io.IOException;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Component
public class QuestaoTextExtractor {

    public record QuestionHeaderPos(int numeroQuestao, int pagina, float x, float y, int coluna) {}

    /**
     * Encontra todas as ocorrências de "QUESTÃO NN" no PDF ordenadas por página e Y, identificando a coluna.
     */
    public List<QuestionHeaderPos> indexarQuestoes(PDDocument doc) throws IOException {
        List<QuestionHeaderPos> posicoes = new ArrayList<>();

        PDFTextStripper stripper = new PDFTextStripper() {
            @Override
            protected void writeString(String text, List<TextPosition> textPositions) throws IOException {
                Matcher m = Pattern.compile("QUEST[A-Z\\uFFFD\\u00C0-\\u00FF\\?\\s]*?\\s*(\\d{1,3})", Pattern.CASE_INSENSITIVE).matcher(text);
                if (m.find() && !textPositions.isEmpty()) {
                    float x = textPositions.get(0).getX();
                    float y = textPositions.get(0).getY();
                    int num = Integer.parseInt(m.group(1));
                    int coluna = (x < 295f) ? 1 : 2;
                    posicoes.add(new QuestionHeaderPos(num, getCurrentPageNo(), x, y, coluna));
                }
                super.writeString(text, textPositions);
            }
        };
        stripper.setSortByPosition(true);
        stripper.getText(doc);

        return posicoes;
    }

    /**
     * Localiza os limites (X, Y e Coluna) de uma questão específica no PDF.
     */
    public Bounds localizarQuestao(PDDocument doc, List<QuestionHeaderPos> posicoesIndexadas, int numeroQuestao) throws IOException {
        return localizarQuestao(doc, posicoesIndexadas, numeroQuestao, null);
    }

    public Bounds localizarQuestao(PDDocument doc, List<QuestionHeaderPos> posicoesIndexadas, int numeroQuestao, String tpLingua) throws IOException {
        List<QuestionHeaderPos> matches = new ArrayList<>();
        for (QuestionHeaderPos p : posicoesIndexadas) {
            if (p.numeroQuestao() == numeroQuestao) {
                matches.add(p);
            }
        }

        if (matches.isEmpty()) {
            return null; // Questão não encontrada no PDF
        }

        int targetIndex = 0;
        if ("1".equals(tpLingua) && numeroQuestao <= 5 && matches.size() > 1) {
            targetIndex = 1; // 2ª ocorrência para a opção em Espanhol
        }

        QuestionHeaderPos atual = matches.get(targetIndex);
        QuestionHeaderPos proxima = null;

        int idxInPos = posicoesIndexadas.indexOf(atual);
        if (idxInPos != -1 && idxInPos + 1 < posicoesIndexadas.size()) {
            proxima = posicoesIndexadas.get(idxInPos + 1);
        }

        int pagina = atual.pagina();
        int coluna = atual.coluna();
        // Margem de segurança morta nas bordas para capturar alternativas A-E e descartar a coluna vizinha
        float xInicio = (coluna == 1) ? 18f : 292f;
        float xFim = (coluna == 1) ? 285f : 565f;

        float yInicio = Math.max(50f, atual.y() - 15f);

        PDPage page = doc.getPage(pagina - 1);
        float pageHeight = page.getMediaBox().getHeight();
        float maxY = pageHeight - 45f; // Margem de segurança para ignorar rodapés do ENEM

        float yFim;
        if (proxima != null && proxima.pagina() == pagina && proxima.coluna() == coluna) {
            yFim = Math.min(proxima.y() - 5f, maxY);
        } else {
            yFim = maxY;
        }

        return new Bounds(pagina, xInicio, xFim, yInicio, yFim, coluna);
    }

    /**
     * Extrai o texto bruto entre dois limites verticais e horizontais de uma página.
     */
    public String extrairTexto(PDDocument doc, Bounds bounds) throws IOException {
        if (bounds == null) return "";

        PDFTextStripperByArea stripper = new PDFTextStripperByArea();
        stripper.setSortByPosition(true);

        PDPage page = doc.getPage(bounds.pagina() - 1);
        float width = bounds.xFim() - bounds.xInicio();
        float height = Math.max(10f, bounds.yFim() - bounds.yInicio());

        Rectangle2D area = new Rectangle2D.Float(bounds.xInicio(), bounds.yInicio(), width, height);
        stripper.addRegion("questao", area);
        stripper.extractRegions(page);

        String text = stripper.getTextForRegion("questao");
        return limparTexto(text);
    }

    public String limparTexto(String raw) {
        if (raw == null) return "";
        String text = raw
                .replaceAll("(?s)(?i)ENEM\\s*2025.*", "")
                .replaceAll("(?s)(?i)ENEN\\s*2025.*", "")
                .replaceAll("(?s)(?i).*?LINGUAGENS,?\\s+CÓDIGOS\\s+E\\s+SUAS\\s+TECNOLOGIAS.*", "")
                .replaceAll("(?s)(?i).*?CIÊNCIAS\\s+HUMANAS\\s+E\\s+SUAS\\s+TECNOLOGIAS.*", "")
                .replaceAll("(?m)^\\s*\\d{5,}\\w*\\.indb.*", "")
                .replaceAll("(?m)^\\s*\\*\\d+\\s*CADERNO.*", "")
                .replaceAll("(?m)^\\s*\\d+\\s+\\|.*", "")
                .replaceAll("(?m)\\s+[a-zA-Z]$", "") // Remove caracteres soltos vazados no fim de linha
                .trim();
        // Remove cabeçalhos de questão como "QUESTÃO 04", "QUESTãO 04", "QU\r\n" do início do texto
        text = text.replaceFirst("(?s)(?i)^\\s*QUEST[A-Z\\uFFFD\\u00C0-\\u00FF\\?\\s]*?\\s*\\d{1,3}\\s*", "").trim();
        text = text.replaceFirst("(?s)(?i)^\\s*QU[\\r\\n\\s]+", "").trim();
        return text;
    }

    /**
     * Separa o enunciado e as alternativas (A-E) a partir do texto bruto extraído.
     */
    public ParsedTextResult parseTextoEAlternativas(String textoBruto, String gabaritoCorreto) {
        if (textoBruto == null || textoBruto.isBlank()) {
            return new ParsedTextResult("", Collections.emptyList(), true, "Texto bruto vazio");
        }

        Pattern altPattern = Pattern.compile("(?m)^\\s*([A-E])\\s*[\n\r\t ]+(.+)");
        Matcher matcher = altPattern.matcher(textoBruto);

        List<int[]> matches = new ArrayList<>();
        List<String> letras = new ArrayList<>();

        while (matcher.find()) {
            matches.add(new int[]{matcher.start(), matcher.end()});
            letras.add(matcher.group(1));
        }

        if (matches.size() >= 5) {
            int primeiroIndexAlt = matches.get(0)[0];
            String enunciado = limparTexto(textoBruto.substring(0, primeiroIndexAlt)).trim();

            List<AlternativaQuestaoPropria> alternativas = new ArrayList<>();
            for (int i = 0; i < matches.size(); i++) {
                String letra = letras.get(i);
                int startTexto = matches.get(i)[0];
                int endTexto = (i + 1 < matches.size()) ? matches.get(i + 1)[0] : textoBruto.length();

                String textoAlternativa = textoBruto.substring(startTexto, endTexto).trim();
                textoAlternativa = textoAlternativa.replaceFirst("^\\s*[A-E]\\s*[\n\r\t ]*", "").trim();
                textoAlternativa = limparTexto(textoAlternativa);

                boolean isCorreta = gabaritoCorreto != null && gabaritoCorreto.equalsIgnoreCase(letra);
                alternativas.add(new AlternativaQuestaoPropria(letra, textoAlternativa, isCorreta));
            }

            return new ParsedTextResult(enunciado, alternativas, false, null);
        }

        // Fallback: Tentar divisão flexível caso haja formatação alternativa
        List<AlternativaQuestaoPropria> altsFallback = extrairAlternativasFallback(textoBruto, gabaritoCorreto);
        if (altsFallback.size() == 5) {
            String enunciado = extrairEnunciadoFallback(textoBruto);
            return new ParsedTextResult(enunciado, altsFallback, false, null);
        }

        return new ParsedTextResult(textoBruto, Collections.emptyList(), true,
                "Encontradas " + matches.size() + " alternativas via regex. Requer revisão manual.");
    }

    private List<AlternativaQuestaoPropria> extrairAlternativasFallback(String texto, String gabaritoCorreto) {
        List<AlternativaQuestaoPropria> list = new ArrayList<>();
        String[] letras = {"A", "B", "C", "D", "E"};
        for (int i = 0; i < letras.length; i++) {
            String current = letras[i];
            String next = (i + 1 < letras.length) ? letras[i + 1] : null;

            int idxCurrent = encontrarPosicaoLetra(texto, current);
            if (idxCurrent == -1) return Collections.emptyList();

            int idxNext = (next != null) ? encontrarPosicaoLetra(texto, next) : texto.length();
            if (idxNext <= idxCurrent) return Collections.emptyList();

            String altContent = texto.substring(idxCurrent, idxNext).trim();
            altContent = altContent.replaceFirst("^\\s*" + current + "\\s*", "").trim();
            altContent = limparTexto(altContent);

            boolean isCorreta = gabaritoCorreto != null && gabaritoCorreto.equalsIgnoreCase(current);
            list.add(new AlternativaQuestaoPropria(current, altContent, isCorreta));
        }
        return list;
    }

    private int encontrarPosicaoLetra(String texto, String letra) {
        Matcher m = Pattern.compile("(?m)^\\s*" + letra + "\\s+").matcher(texto);
        if (m.find()) {
            return m.start();
        }
        return -1;
    }

    private String extrairEnunciadoFallback(String texto) {
        Matcher m = Pattern.compile("(?m)^\\s*A\\s+").matcher(texto);
        if (m.find()) {
            return limparTexto(texto.substring(0, m.start())).trim();
        }
        return limparTexto(texto);
    }

    public record ParsedTextResult(
        String enunciado,
        List<AlternativaQuestaoPropria> alternativas,
        boolean precisaRevisao,
        String motivoRevisao
    ) {}
}
