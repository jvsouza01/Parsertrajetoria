package com.enem.parser.service;

import com.enem.parser.model.Bounds;
import org.apache.pdfbox.rendering.PDFRenderer;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.pdmodel.PDPage;
import org.springframework.stereotype.Component;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.ByteArrayOutputStream;
import java.io.IOException;

@Component
public class QuestaoImageExtractor {

    public byte[] extrairImagemDaQuestao(PDDocument doc, Bounds bounds) throws IOException {
        if (bounds == null) return new byte[0];

        PDPage page = doc.getPage(bounds.pagina() - 1);

        // Verifica se há figuras especificamente dentro do intervalo Y (yInicio a yFim) da questão
        boolean possuiFigura = temImagemNoIntervaloY(page, bounds);

        if (!possuiFigura) {
            return new byte[0]; // Retorna vazio caso a figura pertença a outra questão da mesma página
        }

        PDFRenderer renderer = new PDFRenderer(doc);
        // Render página em 300 DPI para alta nitidez
        BufferedImage pagina = renderer.renderImageWithDPI(bounds.pagina() - 1, 300);

        float escala = 300f / 72f; // PDF ponto base = 72 DPI
        int xInicioPx = Math.max(0, (int) (bounds.xInicio() * escala));
        int larguraPx = (int) ((bounds.xFim() - bounds.xInicio()) * escala);
        int yInicioPx = Math.max(0, (int) (bounds.yInicio() * escala));
        int alturaPx = (int) ((bounds.yFim() - bounds.yInicio()) * escala);

        if (xInicioPx >= pagina.getWidth() || yInicioPx >= pagina.getHeight()) {
            return new byte[0];
        }

        if (xInicioPx + larguraPx > pagina.getWidth()) {
            larguraPx = pagina.getWidth() - xInicioPx;
        }

        if (yInicioPx + alturaPx > pagina.getHeight()) {
            alturaPx = pagina.getHeight() - yInicioPx;
        }

        if (larguraPx <= 0 || alturaPx <= 0) {
            return new byte[0];
        }

        BufferedImage recorte = pagina.getSubimage(xInicioPx, yInicioPx, larguraPx, alturaPx);

        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        ImageIO.write(recorte, "png", baos);
        return baos.toByteArray();
    }

    private boolean temImagemNoIntervaloY(PDPage page, Bounds bounds) {
        try {
            final boolean[] encontrou = new boolean[]{false};
            org.apache.pdfbox.contentstream.PDFGraphicsStreamEngine engine =
                new org.apache.pdfbox.contentstream.PDFGraphicsStreamEngine(page) {
                    @Override
                    public void drawImage(org.apache.pdfbox.pdmodel.graphics.image.PDImage pdImage) throws IOException {
                        org.apache.pdfbox.util.Matrix ctm = getGraphicsState().getCurrentTransformationMatrix();
                        float yPdf = ctm.getTranslateY();
                        float hPdf = Math.abs(ctm.getScalingFactorY());
                        float pageHeight = page.getMediaBox().getHeight();
                        float yTopPdfbox = pageHeight - yPdf - hPdf;
                        float yBottomPdfbox = pageHeight - yPdf;

                        if (yBottomPdfbox >= (bounds.yInicio() - 10f) && yTopPdfbox <= (bounds.yFim() + 10f)) {
                            encontrou[0] = true;
                        }
                    }
                    @Override public void appendRectangle(java.awt.geom.Point2D p0, java.awt.geom.Point2D p1, java.awt.geom.Point2D p2, java.awt.geom.Point2D p3) {}
                    @Override public void clip(int windingRule) {}
                    @Override public void moveTo(float x, float y) {}
                    @Override public void lineTo(float x, float y) {}
                    @Override public void curveTo(float x1, float y1, float x2, float y2, float x3, float y3) {}
                    @Override public java.awt.geom.Point2D getCurrentPoint() { return new java.awt.geom.Point2D.Float(0, 0); }
                    @Override public void closePath() {}
                    @Override public void endPath() {}
                    @Override public void strokePath() {}
                    @Override public void fillPath(int windingRule) {}
                    @Override public void fillAndStrokePath(int windingRule) {}
                    @Override public void shadingFill(org.apache.pdfbox.cos.COSName shadingName) {}
                };
            engine.processPage(page);
            return encontrou[0];
        } catch (Exception e) {
            return false;
        }
    }
}
