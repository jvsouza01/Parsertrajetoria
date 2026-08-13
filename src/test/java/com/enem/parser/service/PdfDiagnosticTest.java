package com.enem.parser.service;

import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.text.PDFTextStripper;
import org.apache.pdfbox.text.TextPosition;
import org.junit.jupiter.api.Test;

import java.io.File;
import java.io.IOException;
import java.util.List;

public class PdfDiagnosticTest {

    @Test
    void testWriteStringChunks() throws IOException {
        File pdfFile = new File("2025_PV_impresso_D1_CD3.pdf");
        if (!pdfFile.exists()) return;

        try (PDDocument doc = PDDocument.load(pdfFile)) {
            PDFTextStripper stripper = new PDFTextStripper() {
                @Override
                protected void writeString(String text, List<TextPosition> textPositions) throws IOException {
                    if (text.contains("QUEST")) {
                        System.out.println("WRITE_STRING CHUNK: [" + text + "] at page " + getCurrentPageNo() + " Y: " + (textPositions.isEmpty() ? 0 : textPositions.get(0).getY()));
                    }
                    super.writeString(text, textPositions);
                }
            };
            stripper.setSortByPosition(true);
            stripper.setStartPage(2);
            stripper.setEndPage(3);
            stripper.getText(doc);
        }
    }
}
