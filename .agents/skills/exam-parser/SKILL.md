---
name: exam-parser
description: Diretrizes de engenharia de prompt, esquemas de dados de bancas brasileiras, transcrição multimodal de PDFs com Gemini, tratamento de textos de apoio e imagens.
---

# Skill: Parser e Ingestão de Provas de Concursos com IA Multimodal

Esta skill documenta os padrões oficiais de produção, esquemas JSON, engenharia de prompt e pipeline de transcrição de provas de concursos e vestibulares para a plataforma **Trajetória** (`POST /api/admin/ingestao/questoes` e `AIServiceImpl.java`).

---

## 1. Arquitetura do Pipeline

```mermaid
graph TD
    PDF[PDF da Prova] --> Slicer[Chunking de Páginas (2 a 3 págs)]
    Slicer --> Multimodal[Gemini Multimodal (PDF Nativo em Base64)]
    Multimodal --> Schema[Structured Outputs (response_schema)]
    Schema --> Dedup[Deduplicação & Junção por Posição]
    Dedup --> Gabarito[Cruzamento com Gabarito Oficial]
    Gabarito --> PlatformJSON[JSON IngestaoQuestaoInput da Trajetória]
```

---

## 2. Grade Canônica Oficial de Matérias & Aliases

O backend da Trajetória possui um catálogo canônico rigoroso. O parser deve utilizar os nomes canônicos ou enviar `materiaNome: null` para classificação automática:

| Nome Canônico Oficial | Aliases Suportados no Backend |
| :--- | :--- |
| **Língua Portuguesa** | Português, Gramática, Língua Portuguesa e Literatura, Interpretação de Texto |
| **Inglês** | Língua Inglesa, Língua Estrangeira - Inglês, Língua Estrangeira (Inglês) |
| **Espanhol** | Língua Espanhola, Língua Estrangeira - Espanhol, Língua Estrangeira (Espanhol) |
| **Matemática** | Matemática, Raciocínio Lógico, Matemática e RLM, RLM |
| **História** | História Geral, História do Brasil, História da Bahia |
| **Geografia** | Geografia Geral, Geografia do Brasil, Geografia da Bahia |
| **Física** | Física |
| **Química** | Química |
| **Biologia** | Biologia, Ciências Biológicas |
| **Filosofia** | Filosofia |
| **Sociologia** | Sociologia |
| **Direito Constitucional** | Direito Constitucional, Noções de Direito Constitucional, Direitos Humanos |
| **Direito Administrativo** | Direito Administrativo, Noções de Direito Administrativo |
| **Direito Penal** | Direito Penal, Direito Penal Militar |
| **Direito Processual Penal** | Processo Penal, Direito Processual Penal Militar |
| **Legislação Institucional** | Legislação da PM-BA, Estatuto dos Policiais Militares, Igualdade Racial e de Gênero |
| **Informática** | Noções de Informática, Tecnologia da Informação, TI |

> [!IMPORTANT]
> **Regra de Ouro do `materiaNome: null`**:
> Se o PDF não tiver cabeçalho explícito de seção ou se houver dúvida, **o parser DEVE enviar `materiaNome: null`**.
> Quando o backend recebe `materiaNome: null`, ele dispara o método `AIService.classificarQuestaoCompleta` com o catálogo global, atingindo **confiança > 95% e aprovação automática (`APROVADO_AUTO`)**. Nunca force `"Geral"` nem herde a matéria do bloco anterior!

---

## 3. Configurações Obrigatórias da API Gemini

1. **`response_schema` (Structured Outputs)**:
   - Força a árvore JSON determinística na geração de tokens (`materiaNome`, `assunto`, `textoBase`, `enunciado`, `alternativas`, `temImagem`, etc.).
2. **`system_instruction`**:
   - Isola o papel de transcrição literal estrita.
   - Proíbe explicitamente resumos, abreviações ou omissões de alternativas.
   - Orienta a identificação de idioma (questão em inglês ➔ `"Inglês"`, questão em espanhol ➔ `"Espanhol"`).
3. **`temperature: 0.0`**:
   - Elimina alucinações e garante transcrição determinística.
4. **Chunking de Páginas (2 a 3 páginas por chamada)**:
   - Evita estouro de limites de saída (`maxOutputTokens`) e rate limits (TPM/429).
5. **Cascata de Modelos com Fallback**:
   - Ordem recomendada: `gemini-3.1-flash-lite`, `gemini-3.5-flash`, `gemini-3.7-flash`, `gemini-flash-latest`.

---

## 4. Diretrizes de Prompts: Textos de Apoio e Imagens

### Textos de Apoio Compartilhados (`textoBase`)
* Quando o caderno contiver textos como *"Para as questões de 1 a 4, considere o texto..."*:
  - O texto integral da obra/fragmento deve ser extraído no campo `textoBase`.
  - O campo `enunciado` deve conter apenas o comando/pergunta central da questão.
  - O backend da Trajetória renderiza o `textoBase` perfeitamente no topo e o utiliza para contextualizar a IA.

### Imagens de Questões (`imagemUrl`)
* O backend espera URLs públicas HTTPS em `imagemUrl`.
* `temImagem: true` se a questão contiver imagem/figura.
* `descricaoImagem`: descrição textual detalhada da imagem gerada pelo modelo multimodal.

---

## 5. Esquema Oficial do JSON de Ingestão (`IngestaoQuestaoInput`)

```json
[
  {
    "idOrigem": "UNEB_2025_VESTIBULAR_Q19",
    "posicao": 19,
    "fonte": "VESTIBULAR",
    "banca": "UNEB",
    "orgao": "UNEB",
    "cargo": "Vestibular Geral",
    "ano": 2025,
    "materiaNome": "Inglês",
    "assunto": null,
    "textoBase": "Effective strategies for studying and improving language skills...",
    "enunciado": "Which of the following statements best describes an effective approach for studying languages?",
    "imagemUrl": null,
    "temImagem": false,
    "descricaoImagem": null,
    "gabaritoOficial": "B",
    "anulada": false,
    "alternativas": [
      { "letra": "A", "texto": "Relying solely on textbook exercises...", "correta": false },
      { "letra": "B", "texto": "Engaging with authentic materials...", "correta": true },
      { "letra": "C", "texto": "Memorizing long lists of vocabulary...", "correta": false },
      { "letra": "D", "texto": "Language learners should never...", "correta": false },
      { "letra": "E", "texto": "Practicing only speaking and listening...", "correta": false }
    ]
  }
]
```
