package com.enem.parser;

import com.enem.parser.service.EnemIngestionRunner;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import java.io.File;

@SpringBootApplication
public class Application implements CommandLineRunner {

    private final EnemIngestionRunner ingestionRunner;

    @Autowired
    public Application(EnemIngestionRunner ingestionRunner) {
        this.ingestionRunner = ingestionRunner;
    }

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }

    @Override
    public void run(String... args) throws Exception {
        File csvFile = new File("microdados_enem_2025/DADOS/ITENS_PROVA_2025.csv");
        File pdfFile = new File("2025_PV_impresso_D1_CD3.pdf");

        if (!csvFile.exists()) {
            System.err.println("Arquivo CSV não encontrado em: " + csvFile.getAbsolutePath());
            return;
        }

        if (!pdfFile.exists()) {
            System.err.println("Arquivo PDF não encontrado em: " + pdfFile.getAbsolutePath());
            return;
        }

        ingestionRunner.executarIngestao(csvFile, pdfFile);
    }
}
