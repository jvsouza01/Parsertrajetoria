package com.enem.parser.model;

/**
 * Bounds within a PDF document page.
 * Note: pagina is 1-indexed (1 = first page).
 * yInicio and yFim are vertical PDF coordinates (in points, origin top-left in PDFTextStripper).
 */
public record Bounds(int pagina, float xInicio, float xFim, float yInicio, float yFim, int coluna) {
    public Bounds(int pagina, float yInicio, float yFim) {
        this(pagina, 0f, 595f, yInicio, yFim, 0);
    }
}

