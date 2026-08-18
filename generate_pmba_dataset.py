import json
import os

# Dados estruturados com atribuição legal obrigatória, conteúdo, taxonomia e gabarito oficial

banca = "UNEB"
orgao = "Polícia Militar da Bahia - PMBA"
cargo = "Oficial da PM (CFOPM) - Caderno 1"
ano = 2025
fonte = "Concurso Público"

texto_base_portugues = """Menino e celular à mesa
Enquanto almoçava tranquilamente meu arroz-com-feijão no restaurante, a paz foi interrompida. Um menino de cerca de 8 anos entrou correndo, seguido pela avó ofegante. O pequeno atraiu atenções imediatas graças à sua desenvoltura social.
Ele gritava, esbarrava nas pessoas, mexia em tudo, quase derrubando as panelas. Demonstrava o que educadores modernos chamam de "hiperatividade" e os antigos de "falta de limites". Ansiosa, a avó tentou acalmá-lo:
− Querido, prefere esta mesa ou aquela?
Sem responder, ele testava a estabilidade das mesas com empurrões. Finalmente, sentou-se, pegou o celular e iniciou uma ruidosa batalha virtual contra monstros. A avó insistiu:
− Posso pegar batatinha ou macarrãozinho?
Sem resposta, o menino ignorava o mundo real, focado no jogo. A avó tentou alimentá-lo, mas ele rejeitou. A situação mudou quando o inesperado aconteceu: um Avatar Prateado emergiu do jogo, materializando-se ao lado do menino.
Com voz firme, repreendeu-o:
− Menino cheio de frescuras! Respeite sua avó e coma direitinho!
Assustado, o garoto desligou o celular, pegou o garfo e começou a comer. A avó suspirou aliviada, enquanto os presentes aplaudiam o improvável herói. O Avatar, com um gesto de despedida, pagou a conta com cartão de débito e sumiu em um rastro de luz, deixando para trás uma refeição finalmente tranquila.
Mais uma missão cumprida.
Fernando Fabbrini - Texto Adaptado
https://www.otempo.com.br/opiniao/fernando-fabbrini/2025/1/2/menino-e-celular-a-mesa"""

questoes_raw = [
    # --- Língua Portuguesa (Q01 a Q20) ---
    {
        "posicao": 1,
        "disciplina": "Língua Portuguesa",
        "areaConhecimento": "Linguagens",
        "assunto": "Tipologia Textual / Tipos de Discurso (Direto, Indireto e Indireto Livre)",
        "dificuldade": "MEDIO",
        "textoBase": texto_base_portugues,
        "enunciado": 'No trecho "− Menino cheio de frescuras! Respeite sua avó e coma direitinho!", verifica-se a utilização de discurso direto. Já no restante do texto, é possível identificar, principalmente, o emprego de:',
        "gabaritoOficial": "E",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "Discurso indireto, com predomínio de marcadores explícitos para as falas dos personagens."},
            {"letra": "B", "texto": "Discurso direto, que predomina em todo o texto, marcando a intervenção dos personagens."},
            {"letra": "C", "texto": "Discurso direto, ao fundir a fala dos personagens com a perspectiva do narrador e do interlocutor."},
            {"letra": "D", "texto": "Discurso indireto livre, que utiliza aspas e outros elementos para delimitar as falas."},
            {"letra": "E", "texto": "Discurso indireto, quando o narrador apresenta as ações e falas dos personagens com intermediários interpretativos."}
        ]
    },
    {
        "posicao": 2,
        "disciplina": "Língua Portuguesa",
        "areaConhecimento": "Linguagens",
        "assunto": "Sintaxe / Emprego do Sinal Indicativo de Crase",
        "dificuldade": "FACIL",
        "textoBase": texto_base_portugues,
        "enunciado": 'Com base no trecho "O pequeno atraiu atenções imediatas graças à sua desenvoltura social", analise o uso da crase no contexto apresentado e assinale a alternativa correta.',
        "gabaritoOficial": "C",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "O uso da crase em \"à sua desenvoltura social\" é inadequado, pois a preposição \"graças\" não exige complemento regido de preposição."},
            {"letra": "B", "texto": "O uso da crase em \"à sua desenvoltura social\" é obrigatório, porque a preposição \"a\", exigida pela regência do termo \"graças\", encontra o artigo definido \"a\" que acompanha o substantivo \"desenvoltura\"."},
            {"letra": "C", "texto": "A crase em \"à sua desenvoltura social\" é facultativa, uma vez que, antes de pronomes possessivos no singular, o uso do artigo definido pode variar conforme a preferência do emissor."},
            {"letra": "D", "texto": "O uso da crase em \"à sua desenvoltura social\" é incorreto, pois não se aplica crase antes de pronomes possessivos, mesmo que antecedam um substantivo."},
            {"letra": "E", "texto": "Não há possibilidade de ocorrência de crase em \"à sua desenvoltura social\", já que o substantivo \"desenvoltura\" não aceita o artigo definido \"a\"."}
        ]
    },
    {
        "posicao": 3,
        "disciplina": "Língua Portuguesa",
        "areaConhecimento": "Linguagens",
        "assunto": "Sintaxe / Concordância Verbal e Nominal",
        "dificuldade": "FACIL",
        "textoBase": texto_base_portugues,
        "enunciado": 'Com base no trecho "O pequeno atraiu atenções imediatas graças à sua desenvoltura social" e nas normas de concordância verbal e nominal, analise a alternativa correta sobre a concordância aplicada:',
        "gabaritoOficial": "E",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "Há erro de concordância verbal, pois o verbo \"atraiu\" deveria estar no plural para concordar com \"atenções imediatas\"."},
            {"letra": "B", "texto": "O verbo \"atraiu\" está corretamente no singular, mas o adjetivo \"imediatas\" deveria estar no singular, para concordar com \"atenção\", que é singular."},
            {"letra": "C", "texto": "A concordância verbal e nominal está incorreta, pois \"atraiu\" deveria concordar com \"atenções\", e \"imediatas\" deveria concordar com \"desenvoltura\"."},
            {"letra": "D", "texto": "Há erro de concordância nominal, pois o adjetivo \"imediatas\" deveria concordar com \"desenvoltura\", que está no singular."},
            {"letra": "E", "texto": "A concordância verbal e nominal está correta, pois o verbo \"atraiu\" concorda com o sujeito \"o pequeno\" no singular, e o adjetivo \"imediatas\" concorda com o substantivo \"atenções\", também no plural."}
        ]
    },
    {
        "posicao": 4,
        "disciplina": "Língua Portuguesa",
        "areaConhecimento": "Linguagens",
        "assunto": "Morfossintaxe / Colocação Pronominal (Próclise, Ênclise e Mesóclise)",
        "dificuldade": "MEDIO",
        "textoBase": texto_base_portugues,
        "enunciado": 'Com base na frase "Finalmente, sentou-se, pegou o celular e iniciou uma ruidosa batalha virtual contra monstros", analise o uso do pronome oblíquo "se" e sua posição na oração, considerando as regras de colocação pronominal na Língua Portuguesa. Assinale a alternativa correta.',
        "gabaritoOficial": "C",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "A posição do pronome em \"sentou-se\" é opcional, podendo ser utilizada tanto a ênclise quanto a próclise, já que o advérbio \"Finalmente\" não exerce força de atração suficiente."},
            {"letra": "B", "texto": "O pronome \"se\" em \"sentou-se\" deveria estar em mesóclise, já que o verbo está no futuro do presente, condição obrigatória para a colocação pronominal."},
            {"letra": "C", "texto": "O uso da ênclise em \"sentou-se\" está correto, pois a colocação pronominal após um advérbio seguido de vírgula permite a posição enclítica do pronome."},
            {"letra": "D", "texto": "O uso da ênclise em \"sentou-se\" está correto, pois o verbo está no início da oração, condição que faculta a posição enclítica do pronome oblíquo."},
            {"letra": "E", "texto": "A ênclise em \"sentou-se\" está incorreta, uma vez que, após o advérbio \"Finalmente\", o pronome deveria estar posicionado como próclise devido à atração do advérbio."}
        ]
    },
    {
        "posicao": 5,
        "disciplina": "Língua Portuguesa",
        "areaConhecimento": "Linguagens",
        "assunto": "Ortografia / Regras de Acentuação Gráfica",
        "dificuldade": "FACIL",
        "textoBase": texto_base_portugues,
        "enunciado": 'Em relação às palavras acentuadas no trecho: "Assustado, o garoto desligou o celular, pegou o garfo e começou a comer. A avó suspirou aliviada, enquanto os presentes aplaudiam o improvável herói. O Avatar, com um gesto de despedida, pagou a conta com cartão de débito e sumiu em um rastro de luz, deixando para trás uma refeição finalmente tranquila." É INCORRETO afirmar que:',
        "gabaritoOficial": "B",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "A palavra \"avó\" é acentuada por ser uma oxítona terminada em \"O\", seguindo a regra das oxítonas terminadas em -o."},
            {"letra": "B", "texto": "A palavra \"trás\" é acentuada por ser uma oxítona termina em \"A\" (seguida de s), que diz que as palavras oxítonas terminadas em \"a\" são acentuadas graficamente."},
            {"letra": "C", "texto": "A palavra \"débito\" é acentuada por ser uma proparoxítona, seguindo a regra que diz que todas as proparoxítonas são acentuadas."},
            {"letra": "D", "texto": "A palavra \"herói\" é acentuada por ser uma oxítona terminada em -ói, seguindo a regra das oxítonas terminadas em \"éi\", \"éu\" e \"ói\" (ditongos abertos)."},
            {"letra": "E", "texto": "A palavra \"improvável\" é acentuada por ser uma paroxítona terminada em \"L\", que exige acento gráfico."}
        ]
    },
    {
        "posicao": 6,
        "disciplina": "Língua Portuguesa",
        "areaConhecimento": "Linguagens",
        "assunto": "Morfossintaxe / Classes de Palavras e Orações Subordinadas",
        "dificuldade": "MEDIO",
        "textoBase": texto_base_portugues,
        "enunciado": 'Com base no texto "Menino e celular à mesa", analise as ocorrências de palavras de relação intervocabular e interoracional e assinale a alternativa que apresenta a classificação correta das preposições e conjunções empregadas no excerto.',
        "gabaritoOficial": "D",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "Em \"A avó suspirou aliviada, enquanto os presentes aplaudiam o improvável herói\", a conjunção \"enquanto\" é coordenativa adversativa, marcando contraste entre as ações descritas."},
            {"letra": "B", "texto": "Em \"Ansiosa, a avó tentou acalmá-lo\", a palavra \"a\" é uma preposição que estabelece relação de posse entre a avó e o menino."},
            {"letra": "C", "texto": "No segmento \"Sem responder, ele testava a estabilidade das mesas com empurrões\", a conjunção \"com\" é empregada para indicar o meio utilizado pelo menino ao interagir com as mesas."},
            {"letra": "D", "texto": "No trecho \"Demonstrava o que educadores modernos chamam de 'hiperatividade'\", a conjunção \"que\" introduz uma oração subordinada substantiva objetiva direta, completando o sentido do verbo \"demonstrava\"."},
            {"letra": "E", "texto": "Em \"Enquanto almoçava tranquilamente meu arroz-com-feijão no restaurante\", a conjunção \"enquanto\" é subordinativa aditiva, indicando a simultaneidade de ações no contexto."}
        ]
    },
    {
        "posicao": 7,
        "disciplina": "Língua Portuguesa",
        "areaConhecimento": "Linguagens",
        "assunto": "Morfologia / Advérbios e Circunstâncias Adverbiais",
        "dificuldade": "FACIL",
        "textoBase": texto_base_portugues,
        "enunciado": 'Com base no texto "Menino e celular à mesa", assinale a alternativa que identifica corretamente o uso de advérbios e suas circunstâncias presentes no excerto.',
        "gabaritoOficial": "C",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "\"Ansiosa, a avó tentou acalmá-lo\" contém um advérbio que expressa intensidade, descrevendo o estado emocional da avó diante da situação caótica."},
            {"letra": "B", "texto": "\"A avó tentou alimentá-lo, mas ele rejeitou\" utiliza um advérbio que indica circunstância de negação, evidenciando a recusa da criança em interagir com o mundo real."},
            {"letra": "C", "texto": "\"Finalmente, sentou-se, pegou o celular e iniciou uma ruidosa batalha virtual contra monstros\" contém um advérbio que exprime circunstância de tempo, marcando a conclusão de uma sequência de ações."},
            {"letra": "D", "texto": "\"Sem responder, ele testava a estabilidade das mesas com empurrões\" apresenta dois advérbios que indicam negação e dúvida, reforçando a hesitação do menino diante das perguntas da avó."},
            {"letra": "E", "texto": "\"Enquanto almoçava tranquilamente meu arroz-com-feijão no restaurante\" apresenta dois advérbios que indicam, respectivamente, circunstâncias de tempo e intensidade."}
        ]
    },
    {
        "posicao": 8,
        "disciplina": "Língua Portuguesa",
        "areaConhecimento": "Linguagens",
        "assunto": "Compreensão e Interpretação de Texto",
        "dificuldade": "FACIL",
        "textoBase": texto_base_portugues,
        "enunciado": 'Com base no texto, o comportamento do menino pode ser interpretado como reflexo de:',
        "gabaritoOficial": "D",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "Uma criança comum que busca atenção excessiva devido à negligência parental."},
            {"letra": "B", "texto": "Um exemplo da influência de modelos de comportamentos modernos sobre os mais velhos."},
            {"letra": "C", "texto": "Um reflexo natural de crianças expostas a jogos eletrônicos desde cedo."},
            {"letra": "D", "texto": "Uma ausência de limites na educação familiar, evidenciada pela dificuldade de imposição de autoridade por parte da avó."},
            {"letra": "E", "texto": "Uma personalidade criativa que não se adapta às normas sociais tradicionais."}
        ]
    },
    {
        "posicao": 9,
        "disciplina": "Língua Portuguesa",
        "areaConhecimento": "Linguagens",
        "assunto": "Sintaxe / Termos Integrantes e Acessórios da Oração (Predicativo)",
        "dificuldade": "MEDIO",
        "textoBase": texto_base_portugues,
        "enunciado": 'Assinale a alternativa cuja palavra em destaque NÃO está exercendo a função de predicativo.',
        "gabaritoOficial": "B",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "Ansiosa, a avó tentou acalmá-lo."},
            {"letra": "B", "texto": "O pequeno atraiu atenções imediatas graças à sua desenvoltura social."},
            {"letra": "C", "texto": "A avó suspirou aliviada, enquanto os presentes aplaudiam o improvável herói."},
            {"letra": "D", "texto": "Assustado, o garoto desligou o celular, pegou o garfo e começou a comer."},
            {"letra": "E", "texto": "Enquanto almoçava tranquilamente meu arroz-com-feijão no restaurante, a paz foi interrompida."}
        ]
    },
    {
        "posicao": 10,
        "disciplina": "Língua Portuguesa",
        "areaConhecimento": "Linguagens",
        "assunto": "Morfologia / Verbos (Tempos, Modos e Aspecto Verbal)",
        "dificuldade": "MEDIO",
        "textoBase": texto_base_portugues,
        "enunciado": 'Com base no texto "Menino e celular à mesa", de Fernando Fabbrini, analise as alternativas abaixo e assinale a opção que apresenta uma afirmativa correta sobre a flexão verbal, considerando a concordância, o tempo verbal e o aspecto das ações descritas:\n"...A situação mudou quando o inesperado aconteceu: um Avatar Prateado emergiu do jogo, materializando-se ao lado do menino. Com voz firme, repreendeu-o: − Menino cheio de frescuras! Respeite sua avó e coma direitinho!"',
        "gabaritoOficial": "A",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "Mudou e aconteceu − flexão no pretérito perfeito, indicando ações pontuais e concluídas no passado."},
            {"letra": "B", "texto": "Mudou e respeite − flexão no pretérito perfeito e no presente do indicativo, com ações que indicam uma mudança e uma instrução atual."},
            {"letra": "C", "texto": "Repreendeu-o e coma − flexão no pretérito perfeito e no presente do subjuntivo, indicando uma ação concluída e uma ação que depende de cumprimento."},
            {"letra": "D", "texto": "Repreendeu-o e respeite − flexão no pretérito perfeito e no presente do indicativo, com ações que se complementam na sequência temporal."},
            {"letra": "E", "texto": "Emergiu e materializando-se − flexão no pretérito perfeito e no gerúndio, respectivamente, indicando uma ação pontual e uma ação contínua."}
        ]
    },
    {
        "posicao": 11,
        "disciplina": "Língua Portuguesa",
        "areaConhecimento": "Linguagens",
        "assunto": "Semântica / Antonímia e Relações de Significado",
        "dificuldade": "FACIL",
        "textoBase": texto_base_portugues,
        "enunciado": 'Com base no texto "Menino e celular à mesa", de Fernando Fabbrini, analise as alternativas abaixo e assinale a opção em que o termo destacado possui uma relação de antonímia (oposição de sentidos) em relação ao seu contexto imediato:\n"...a paz foi interrompida. Um menino de cerca de 8 anos entrou correndo, seguido pela avó ofegante. O pequeno atraiu atenções imediatas graças à sua desenvoltura social."',
        "gabaritoOficial": "C",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "Atraiu e Retraiu, apesar de apresentarem certa oposição em seus significados, não expressam uma relação direta de contrariedade exata."},
            {"letra": "B", "texto": "Paz e Perspicácia, já que paz implica ausência de conflito e atenta refere-se a uma atitude de vigilância, contrária ao repouso."},
            {"letra": "C", "texto": "Ofegante e tranquila, uma vez que a tranquilidade está relacionada à calma, enquanto ofegante remete à agitação."},
            {"letra": "D", "texto": "Imediatas e iminentes, porque pertencem a campos semânticos diferentes e não expressam uma oposição direta."},
            {"letra": "E", "texto": "Interrompida e recuperada, pois um termo descreve uma ação interrompida e o outro implica continuidade ou fluidez."}
        ]
    },
    {
        "posicao": 12,
        "disciplina": "Língua Portuguesa",
        "areaConhecimento": "Linguagens",
        "assunto": "Sintaxe / Período Composto por Coordenação (Orações Adversativas)",
        "dificuldade": "FACIL",
        "textoBase": texto_base_portugues,
        "enunciado": 'Com base no trecho "A avó tentou alimentá-lo, mas ele rejeitou" e considerando os conceitos de coordenação e subordinação, analise a alternativa correta:',
        "gabaritoOficial": "A",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "O uso da conjunção \"mas\" caracteriza uma oração coordenada adversativa, pois estabelece uma relação de contraste entre as ações descritas nas orações."},
            {"letra": "B", "texto": "A conjunção \"mas\" estabelece uma relação de coordenação explicativa, pois a segunda oração explica o motivo da primeira."},
            {"letra": "C", "texto": "A conjunção \"mas\" é utilizada para estabelecer uma relação de subordinação consecutiva, indicando o resultado da ação da avó."},
            {"letra": "D", "texto": "A conjunção \"mas\" estabelece uma relação de subordinação causal entre as orações, indicando a causa da rejeição do menino à alimentação oferecida pela avó."},
            {"letra": "E", "texto": "O uso da conjunção \"mas\" caracteriza uma oração subordinada adversativa, já que a segunda oração expressa oposição à primeira."}
        ]
    },
    {
        "posicao": 13,
        "disciplina": "Língua Portuguesa",
        "areaConhecimento": "Linguagens",
        "assunto": "Interpretação Textual / Recursos Expressivos e Humor",
        "dificuldade": "FACIL",
        "textoBase": texto_base_portugues,
        "enunciado": 'O humor do texto está sustentado, principalmente, na:',
        "gabaritoOficial": "A",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "Solução fantasiosa e inusitada para resolver uma situação cotidiana problemática."},
            {"letra": "B", "texto": "Utilização de termos exagerados para descrever ações triviais de uma criança."},
            {"letra": "C", "texto": "Personificação do Avatar como um ser que atua como mediador familiar."},
            {"letra": "D", "texto": "Comparação entre os valores antigos e modernos na criação de crianças."},
            {"letra": "E", "texto": "Crítica explícita à falta de educação das crianças na atualidade."}
        ]
    },
    {
        "posicao": 14,
        "disciplina": "Língua Portuguesa",
        "areaConhecimento": "Linguagens",
        "assunto": "Interpretação Textual / Intencionalidade Discursiva",
        "dificuldade": "FACIL",
        "textoBase": texto_base_portugues,
        "enunciado": 'De acordo com o texto, a aparição do Avatar Prateado tem como objetivo principal:',
        "gabaritoOficial": "A",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "Despertar no garoto a importância de seguir as regras sociais por meio de um susto."},
            {"letra": "B", "texto": "Criticar os jogos virtuais como uma prática prejudicial às crianças."},
            {"letra": "C", "texto": "Divertir o garoto com elementos fantasiosos durante a refeição."},
            {"letra": "D", "texto": "Mostrar aos adultos presentes a necessidade de supervisão mais rígida."},
            {"letra": "E", "texto": "Ensinar à avó como lidar com crianças hiperativas e desobedientes."}
        ]
    },
    {
        "posicao": 15,
        "disciplina": "Língua Portuguesa",
        "areaConhecimento": "Linguagens",
        "assunto": "Pontuação / Emprego dos Dois-Pontos",
        "dificuldade": "FACIL",
        "textoBase": texto_base_portugues,
        "enunciado": 'No trecho "A situação mudou quando o inesperado aconteceu: um Avatar Prateado emergiu do jogo, materializando-se ao lado do menino.", a utilização dos dois-pontos tem como objetivo:',
        "gabaritoOficial": "D",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "Sinalizar uma pausa enfática para provocar suspense na leitura."},
            {"letra": "B", "texto": "Separar dois períodos independentes, reforçando a ideia de causalidade."},
            {"letra": "C", "texto": "Apresentar uma contrariedade para a ação descrita na primeira parte da frase."},
            {"letra": "D", "texto": "Introduzir uma explicação ou detalhamento do elemento descrito como \"o inesperado\"."},
            {"letra": "E", "texto": "Indicar uma citação direta do narrador sobre os acontecimentos ao longo do texto."}
        ]
    },
    {
        "posicao": 16,
        "disciplina": "Língua Portuguesa",
        "areaConhecimento": "Linguagens",
        "assunto": "Sintaxe / Estrutura do Período Composto",
        "dificuldade": "MEDIO",
        "textoBase": texto_base_portugues,
        "enunciado": 'Analise o trecho a seguir:\n"Enquanto almoçava tranquilamente meu arroz-com-feijão no restaurante, a paz foi interrompida. Um menino de cerca de 8 anos entrou correndo, seguido pela avó ofegante. O pequeno atraiu atenções imediatas graças à sua desenvoltura social. Ele gritava, esbarrava nas pessoas, mexia em tudo, quase derrubando as panelas. Demonstrava o que educadores modernos chamam de \"hiperatividade\" e os antigos de \"falta de limites\"..."\nAssinale a alternativa que apresenta uma afirmação correta:',
        "gabaritoOficial": "D",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "A frase \"O pequeno atraiu atenções imediatas graças à sua desenvoltura social\" é um período composto por coordenação, pois há uma relação de dependência entre as orações."},
            {"letra": "B", "texto": "\"A avó tentou acalmá-lo\" é uma oração coordenada sindética, pois tem relação de dependência com a oração anterior e está ligada pela conjunção \"e\"."},
            {"letra": "C", "texto": "A oração \"Enquanto almoçava tranquilamente meu arroz-com-feijão no restaurante\" é subordinada adverbial, pois a oração principal indica a circunstância da ação expressa pela oração subordinada."},
            {"letra": "D", "texto": "\"Ele gritava, esbarrava nas pessoas, mexia em tudo, quase derrubando as panelas\" é composta por orações coordenadas, pois as ações expressas são independentes, ligadas por vírgulas."},
            {"letra": "E", "texto": "\"O pequeno atraiu atenções imediatas graças à sua desenvoltura social\" possui uma oração subordinada substantiva objetiva direta, com o verbo \"atraiu\" regendo o objeto direto \"atenções imediatas graças à sua desenvoltura social\"."}
        ]
    },
    {
        "posicao": 17,
        "disciplina": "Língua Portuguesa",
        "areaConhecimento": "Linguagens",
        "assunto": "Sintaxe / Regência Verbal e Transitividade",
        "dificuldade": "FACIL",
        "textoBase": texto_base_portugues,
        "enunciado": 'Com base na frase "O pequeno atraiu atenções imediatas graças à sua desenvoltura social" e nas normas de regência verbal da Língua Portuguesa, analise o uso do verbo "atrair" e sua relação com os complementos verbais. Assinale a alternativa correta:',
        "gabaritoOficial": "D",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "O verbo \"atrair\" é intransitivo, sendo \"atenções imediatas\" um adjunto adverbial que complementa o sentido do verbo."},
            {"letra": "B", "texto": "O verbo \"atrair\" exige obrigatoriamente a presença de uma preposição para introduzir seu complemento, o que invalida o uso de \"atenções imediatas\" como objeto direto."},
            {"letra": "C", "texto": "O verbo \"atrair\", na frase apresentada, está mal empregado, pois deveria ser seguido de uma expressão iniciada por preposição para estar em conformidade com a regência normativa."},
            {"letra": "D", "texto": "O verbo \"atrair\" é transitivo direto, e sua regência exige um objeto direto, como ocorre na frase apresentada, em que \"atenções imediatas\" desempenha essa função."},
            {"letra": "E", "texto": "O verbo \"atrair\" admite dupla regência, podendo ser transitivo direto ou indireto, dependendo do contexto, mas na frase apresentada, ele funciona como verbo transitivo direto."}
        ]
    },
    {
        "posicao": 18,
        "disciplina": "Língua Portuguesa",
        "areaConhecimento": "Linguagens",
        "assunto": "Redação Oficial / Ofício e Memorando",
        "dificuldade": "MEDIO",
        "textoBase": None,
        "enunciado": 'Entre os documentos mais utilizados na comunicação oficial estão o ofício e o memorando, que, embora compartilhem algumas semelhanças, apresentam diferenças quanto à finalidade, à forma de tramitação e ao nível hierárquico entre os interlocutores. Com base nessa temática, analise as alternativas abaixo e assinale a correta:',
        "gabaritoOficial": "D",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "O memorando é um documento formal que deve ser utilizado para comunicar informações sigilosas, enquanto o ofício é um documento menos formal, utilizado para assuntos administrativos gerais."},
            {"letra": "B", "texto": "O ofício é um documento utilizado exclusivamente para tratar de assuntos administrativos internos, enquanto o memorando deve ser usado apenas para enviar solicitações formais externas."},
            {"letra": "C", "texto": "O ofício é utilizado para comunicações internas dentro de uma organização, enquanto o memorando é destinado a comunicações externas, entre diferentes órgãos públicos ou empresas."},
            {"letra": "D", "texto": "O ofício é um documento formal utilizado para comunicações externas, geralmente enviado a órgãos ou entidades diferentes, enquanto o memorando é utilizado para comunicações internas e de caráter mais informal dentro de uma mesma instituição."},
            {"letra": "E", "texto": "O ofício e o memorando são utilizados indistintamente, pois ambos servem para comunicar informações de interesse de um órgão público a outro, sem qualquer distinção em seu uso."}
        ]
    },
    {
        "posicao": 19,
        "disciplina": "Língua Portuguesa",
        "areaConhecimento": "Linguagens",
        "assunto": "Redação Oficial / Princípios da Redação Técnica (Impessoalidade e Objetividade)",
        "dificuldade": "MEDIO",
        "textoBase": None,
        "enunciado": 'Assinale a alternativa que está diretamente relacionada à Redação técnica (oficial):',
        "gabaritoOficial": "D",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "Caracteriza-se pelo uso de uma linguagem mais subjetiva e criativa, enquanto a redação estilística se baseia em normas rígidas e impessoais, buscando objetividade e clareza."},
            {"letra": "B", "texto": "Possui uma estrutura de linguagem mais formal, mas não exige a utilização de termos técnicos. A redação estilística, por sua vez, segue regras rigorosas de objetividade e clareza, com vocabulário simplificado e sem elementos subjetivos."},
            {"letra": "C", "texto": "Foca na transmissão clara e precisa de informações, com foco na objetividade e no uso de uma linguagem simples e direta. A redação estilística, por sua vez, utiliza uma linguagem informal e expressiva, com liberdade estilística e recursos como metáforas e adjetivos poéticos."},
            {"letra": "D", "texto": "É marcada por um vocabulário especializado e impessoal, com foco em transmitir informações de maneira clara e objetiva. Já a redação estilística privilegia a expressão artística, buscando mais originalidade e subjetividade na escolha de palavras e na construção de frases."},
            {"letra": "E", "texto": "Pode fazer uso de figuras de linguagem para tornar o texto mais expressivo, enquanto a redação estilística deve ser impessoal e direta, sem espaço para subjetividades ou interpretações."}
        ]
    },
    {
        "posicao": 20,
        "disciplina": "Língua Portuguesa",
        "areaConhecimento": "Linguagens",
        "assunto": "Redação Oficial / Correspondência Oficial",
        "dificuldade": "FACIL",
        "textoBase": None,
        "enunciado": 'A correspondência oficial é um instrumento fundamental para a comunicação entre órgãos públicos, entre esses e particulares ou mesmo entre autoridades, sendo regulamentada por normas específicas que garantem uniformidade, clareza e objetividade. Nesse contexto, analise as alternativas a seguir e assinale a correta:',
        "gabaritoOficial": "C",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "Correspondência oficial se refere à comunicação entre órgãos privados, visando principalmente à troca de informações financeiras. Dentre os tipos de documentos, destacam-se o ofício, relatório e o cartão-postal."},
            {"letra": "B", "texto": "Correspondência oficial refere-se a qualquer tipo de documento utilizado exclusivamente para assuntos pessoais, e seus principais tipos incluem bilhetes, convites e telegramas."},
            {"letra": "C", "texto": "A correspondência oficial é definida como qualquer comunicação escrita emitida no âmbito de órgãos públicos, com o objetivo de transmitir informações de interesse público, sendo seus principais tipos: ofício, circular, memorando e e-mail institucional."},
            {"letra": "D", "texto": "Correspondência oficial é toda comunicação feita entre empresas privadas, com caráter pessoal e informativo. Os principais documentos dessa categoria são os contratos e cartas de intenção."},
            {"letra": "E", "texto": "Correspondência oficial é qualquer tipo de comunicação realizada entre pessoas físicas ou jurídicas, independente de sua formalidade, sendo os tipos mais comuns: carta, memorando e relatório."}
        ]
    },

    # --- Língua Inglesa (Q21 a Q25) ---
    {
        "posicao": 21,
        "disciplina": "Língua Inglesa",
        "areaConhecimento": "Linguagens",
        "assunto": "Grammar / Countable and Uncountable Nouns",
        "dificuldade": "FACIL",
        "textoBase": None,
        "enunciado": 'In English grammar, nouns are frequently categorized based on their ability to be counted as separate units or not. Countable nouns can generally appear in both singular and plural forms, and they can be modified by numbers. They are often preceded by articles such as "a" or "an" when referring to a single item. Uncountable nouns, conversely, do not usually take plural forms and cannot be paired directly with numbers in standard usage. Choose the one that is traditionally regarded as an uncountable noun in English:',
        "gabaritoOficial": "E",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "Car."},
            {"letra": "B", "texto": "Orange."},
            {"letra": "C", "texto": "Book."},
            {"letra": "D", "texto": "Onion."},
            {"letra": "E", "texto": "Milk."}
        ]
    },
    {
        "posicao": 22,
        "disciplina": "Língua Inglesa",
        "areaConhecimento": "Linguagens",
        "assunto": "Grammar / Adverbs (Word Order and Sentence Structure)",
        "dificuldade": "MEDIO",
        "textoBase": None,
        "enunciado": 'Imagine you are helping a friend write a short paragraph for a storytelling competition. The paragraph needs to incorporate various adverbs to provide a detailed picture of the situation. After reviewing an initial draft, you notice that adverbs of manner, place, time, and degree should be used carefully to enhance clarity and coherence. Analyze these sentences to determine which one best places the different adverbs (manner, place, time, and degree) in a grammatically correct and coherent manner.',
        "gabaritoOficial": "E",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "He spoke carefully library very today."},
            {"letra": "B", "texto": "Spoke he carefully too, library it is today."},
            {"letra": "C", "texto": "Today, he spoke library carefully very."},
            {"letra": "D", "texto": "He carefully library spoke too late."},
            {"letra": "E", "texto": "He spoke very carefully in the library today."}
        ]
    },
    {
        "posicao": 23,
        "disciplina": "Língua Inglesa",
        "areaConhecimento": "Linguagens",
        "assunto": "Reading Comprehension / Dialogue Analysis and Inferences",
        "dificuldade": "FACIL",
        "textoBase": "Consider the dialogue below:\nJake: I can't decide if I should attend the meeting or not. My manager said it's optional, but it's quite important for the future of the project.\nLiz: I think you should definitely go. It might not be mandatory, but you'll learn a lot, and your input is valuable.\nJake: I guess you're right. I'll see if I can rearrange my schedule.\nLiz: That would be wise. It could show your commitment.",
        "enunciado": "Based on the dialogue, which of the following statements best describes Jake's feelings about attending the meeting?",
        "gabaritoOficial": "A",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "He is initially uncertain but seems willing to attend after Liz's advice."},
            {"letra": "B", "texto": "He has already attended the meeting and found it unproductive."},
            {"letra": "C", "texto": "He believes attending the meeting is unnecessary and a waste of time."},
            {"letra": "D", "texto": "He is enthusiastic and has already confirmed his attendance."},
            {"letra": "E", "texto": "He is completely opposed to the idea of attending."}
        ]
    },
    {
        "posicao": 24,
        "disciplina": "Língua Inglesa",
        "areaConhecimento": "Linguagens",
        "assunto": "Vocabulary / Synonyms and Antonyms",
        "dificuldade": "FACIL",
        "textoBase": "Below are five pairs of words. Some pairs are synonyms, and others are antonyms. Identify which pairs are synonyms:\n(1) Expand − Enlarge\n(2) Timid − Bold\n(3) Fear − Terror\n(4) Accurate − Exact\n(5) Deep − Shallow",
        "enunciado": "Select the CORRECT alternative.",
        "gabaritoOficial": "B",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "Only (2) and (5)"},
            {"letra": "B", "texto": "(1), (3), and (4)"},
            {"letra": "C", "texto": "Only (1) and (4)"},
            {"letra": "D", "texto": "Only (1) and (3)"},
            {"letra": "E", "texto": "(1), (2), (3), and (4)"}
        ]
    },
    {
        "posicao": 25,
        "disciplina": "Língua Inglesa",
        "areaConhecimento": "Linguagens",
        "assunto": "Grammar / Prepositions and Dependent Prepositions",
        "dificuldade": "FACIL",
        "textoBase": None,
        "enunciado": 'Consider the sentence below:\n"I\'m not very good ____ math."\nSelect the correct preposition to complete the following sentence:',
        "gabaritoOficial": "C",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "about"},
            {"letra": "B", "texto": "in"},
            {"letra": "C", "texto": "at"},
            {"letra": "D", "texto": "for"},
            {"letra": "E", "texto": "on"}
        ]
    },

    # --- Ciências Humanas (Q26 a Q45) ---
    {
        "posicao": 26,
        "disciplina": "Ciências Humanas",
        "areaConhecimento": "Ciências Humanas",
        "assunto": "História do Brasil / Brasil Colônia (Economia, Pecuária e Expansão Territorial)",
        "dificuldade": "MEDIO",
        "textoBase": None,
        "enunciado": "A expansão territorial do Brasil Colônia está frequentemente associada à mineração, mas a pecuária desempenhou um papel igualmente crucial. Sobre esse assunto, julgue as sentenças abaixo como VERDADEIRAS ou FALSAS.\n1.(__)O couro era um subproduto altamente valorizado, utilizado na fabricação de utensílios como botas, selas, arreios, bolsas e até correias para os engenhos. Esse material tornou-se uma importante mercadoria de exportação.\n2.(__)A pecuária desempenhou um papel essencial na expansão territorial e na consolidação do Brasil Colônia, especialmente em áreas menos aptas para a produção de açúcar, como as regiões centro-oeste e as planícies do sul.\n3.(__)A pecuária foi essencial para fornecer carne bovina e derivados, como leite e queijo, às populações coloniais, especialmente em áreas de mineração e em núcleos urbanos.\nA sequência CORRETA é:",
        "gabaritoOficial": "E",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "1.V, 2.F, 3.V."},
            {"letra": "B", "texto": "1.F, 2.V, 3.F."},
            {"letra": "C", "texto": "1.V, 2.F, 3.F."},
            {"letra": "D", "texto": "1.F, 2.V, 3.V."},
            {"letra": "E", "texto": "1.V, 2.V, 3.V."}
        ]
    },
    {
        "posicao": 27,
        "disciplina": "Ciências Humanas",
        "areaConhecimento": "Ciências Humanas",
        "assunto": "História do Brasil / Desenvolvimento Científico e Instituições no Século XX",
        "dificuldade": "MEDIO",
        "textoBase": None,
        "enunciado": "O desenvolvimento científico no Brasil no século XX foi marcado por avanços significativos e desafios estruturais. Durante esse período, diversas instituições foram criadas para fomentar a pesquisa, formar recursos humanos e promover a inovação em setores estratégicos. Sobre o desenvolvimento científico no Brasil no século XX, é correto afirmar que:",
        "gabaritoOficial": "C",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "A criação do Conselho Nacional de Desenvolvimento Científico e Tecnológico (CNPq) e da Embrapa ocorreu no mesmo período, ambos voltados para o avanço das ciências sociais."},
            {"letra": "B", "texto": "O Brasil priorizou, ao longo do século, o desenvolvimento de tecnologias próprias, com grande independência em relação às inovações estrangeiras."},
            {"letra": "C", "texto": "A Universidade de São Paulo (USP), fundada na década de 1930, foi um marco na formação de pesquisadores e na consolidação da ciência nacional."},
            {"letra": "D", "texto": "O financiamento da pesquisa científica no Brasil sempre foi equilibrado e distribuído de forma igualitária entre as regiões do país."},
            {"letra": "E", "texto": "A expansão da Petrobras e do Programa Nuclear Brasileiro nas décadas de 1960 e 1970 representou uma tentativa de diversificar a produção agrícola."}
        ]
    },
    {
        "posicao": 28,
        "disciplina": "Ciências Humanas",
        "areaConhecimento": "Ciências Humanas",
        "assunto": "Geografia do Brasil / Relação Cidade-Campo, Modernização Agrícola e Urbanização",
        "dificuldade": "MEDIO",
        "textoBase": None,
        "enunciado": "A relação cidade-campo sofreu diversas transformações ao longo da história, especialmente com o avanço da industrialização e do desenvolvimento tecnológico, que influenciaram a dinâmica econômica e social do espaço rural e urbano. Sobre esse tema, analise as afirmativas:\nI.A revolução tecnológica e os avanços na agricultura mecanizada permitiram o aumento da produtividade no campo, mas resultaram na concentração de terras e no êxodo rural.\nII.O processo de industrialização nas regiões metropolitanas ampliou a oferta de empregos, atraindo grande parte da força de trabalho rural e gerando a urbanização acelerada no Brasil, especialmente no século XX.\nIII.A desconcentração industrial no Brasil, promovida a partir da década de 1990, contribuiu para uma relação mais equilibrada entre áreas urbanas e rurais, favorecendo a diversificação da economia no interior do país.\nIV.As áreas rurais, com o avanço das tecnologias de informação e comunicação, permanecem isoladas das redes globais de produção e consumo, mantendo-se economicamente independentes dos centros urbanos.\nAssinale a alternativa CORRETA:",
        "gabaritoOficial": "B",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "I, II, III e IV estão corretas."},
            {"letra": "B", "texto": "Somente as afirmativas I, II e III estão corretas."},
            {"letra": "C", "texto": "Somente as afirmativas II, III e IV estão corretas."},
            {"letra": "D", "texto": "Somente as afirmativas I e II estão corretas."},
            {"letra": "E", "texto": "Somente as afirmativas I, III e IV estão corretas."}
        ]
    },
    {
        "posicao": 29,
        "disciplina": "Ciências Humanas",
        "areaConhecimento": "Ciências Humanas",
        "assunto": "História do Brasil / Nova República (Economia e Plano Cruzado)",
        "dificuldade": "FACIL",
        "textoBase": None,
        "enunciado": "Em meados da década de 1980, o Brasil enfrentava uma grave crise econômica, marcada por níveis alarmantes de hiperinflação que corroíam o poder de compra da população. Para enfrentar essa situação, foi implementado um plano econômico que introduziu uma nova moeda nacional, buscando estabilizar os preços. Além disso, o plano congelou preços e salários, tentando evitar aumentos descontrolados e especulativos. Outra medida foi a criação de um índice que reajustava periodicamente os salários para proteger os trabalhadores da inflação acumulada. Embora inicialmente tenha recebido apoio popular, o plano começou a enfrentar problemas devido ao desabastecimento de produtos e ao descumprimento do congelamento por parte de setores econômicos. Como resultado, as medidas perderam credibilidade, e a inflação voltou com força pouco tempo depois. Nesse sentido, estamos falando do:",
        "gabaritoOficial": "D",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "Plano Bresser."},
            {"letra": "B", "texto": "Plano Collor I."},
            {"letra": "C", "texto": "Plano Real."},
            {"letra": "D", "texto": "Plano Cruzado."},
            {"letra": "E", "texto": "Plano Verão."}
        ]
    },
    {
        "posicao": 30,
        "disciplina": "Ciências Humanas",
        "areaConhecimento": "Ciências Humanas",
        "assunto": "Geografia Geral e Ambiental / Recursos Naturais e Desigualdades Socioambientais",
        "dificuldade": "MEDIO",
        "textoBase": None,
        "enunciado": "Analise as afirmativas abaixo sobre a relação entre a sociedade e a natureza, os recursos naturais e a sobrevivência humana no mundo, considerando desigualdades na apropriação desses recursos:\nI.A Amazônia, reconhecida como uma das maiores reservas de biodiversidade do mundo, também desempenha um papel crucial como reguladora climática global, mas sua exploração intensa gera consequências ambientais e sociais, incluindo a exclusão de comunidades tradicionais.\nII.O acesso desigual a recursos hídricos no Brasil evidencia disparidades sociais e regionais. Com o semiárido nordestino enfrentando desafios históricos para garantir o abastecimento regular de água.\nIII.A transição energética global, marcada pela busca por fontes renováveis como a energia solar e eólica, é liderada exclusivamente pelos países mais desenvolvidos, enquanto os países em desenvolvimento continuam dependentes de combustíveis fósseis.\nIV.No mundo, as práticas de sobrepesca, especialmente em oceanos como o Pacífico, têm impactado negativamente a sobrevivência de comunidades pesqueiras, além de causar o desequilíbrio nos ecossistemas marinhos.\nAssinale a alternativa CORRETA:",
        "gabaritoOficial": "E",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "Somente as afirmativas II, III e IV estão corretas."},
            {"letra": "B", "texto": "I, II, III e IV estão corretas."},
            {"letra": "C", "texto": "Somente as afirmativas I, III e IV estão corretas."},
            {"letra": "D", "texto": "Somente as afirmativas I, II e III estão corretas."},
            {"letra": "E", "texto": "Somente as afirmativas I, II e IV estão corretas."}
        ]
    },
    {
        "posicao": 31,
        "disciplina": "Ciências Humanas",
        "areaConhecimento": "Ciências Humanas",
        "assunto": "História Geral / Idade Moderna (Reforma Protestante e Calvinismo)",
        "dificuldade": "FACIL",
        "textoBase": None,
        "enunciado": "O Calvinismo, uma das vertentes do Protestantismo surgida durante a Reforma Protestante no século XVI, destacou-se por sua organização doutrinal. Sob a liderança de João Calvino, essa corrente teológica teve grande impacto na organização social e econômica de comunidades reformadas, influenciando práticas culturais e políticas. Sobre o Calvinismo, é correto afirmar que:",
        "gabaritoOficial": "C",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "Rejeitava totalmente as Escrituras como base da fé, propondo uma espiritualidade fundamentada na tradição oral e nos líderes da igreja."},
            {"letra": "B", "texto": "Foi amplamente rejeitado em países como Suíça e Países Baixos, mas encontrou aceitação na Espanha e em Portugal devido à forte influência católica."},
            {"letra": "C", "texto": "Introduziu o conceito de predestinação, segundo o qual Deus, desde a eternidade, escolheu quem será salvo, independentemente das ações humanas."},
            {"letra": "D", "texto": "Defendia a total liberdade do indivíduo para alcançar a salvação, enfatizando a separação completa entre religião e vida pública."},
            {"letra": "E", "texto": "Proibia qualquer forma de organização comunitária religiosa, defendendo a centralização do poder na figura de um único líder espiritual."}
        ]
    },
    {
        "posicao": 32,
        "disciplina": "Ciências Humanas",
        "areaConhecimento": "Ciências Humanas",
        "assunto": "História Antiga / Civilizações Clássicas (Etruscos e Península Itálica)",
        "dificuldade": "MEDIO",
        "textoBase": None,
        "enunciado": "Os etruscos, uma das civilizações mais influentes da Península Itálica, prosperaram entre os séculos IX e III a.C., antes da consolidação do poder romano. Sua cultura deixou um legado significativo em aspectos como religião, arquitetura e organização social, influenciando diretamente a civilização romana. Sobre esse assunto, é correto afirmar que:",
        "gabaritoOficial": "E",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "Os etruscos foram assimilados culturalmente pelos gregos antes da expansão romana, o que explica a falta de registros arqueológicos etruscos."},
            {"letra": "B", "texto": "Os etruscos eram conhecidos por sua estrutura política centralizada, liderada por um único rei que governava toda a Etrúria."},
            {"letra": "C", "texto": "Os etruscos introduziram o conceito de república na Península Itálica, que posteriormente foi adotado pelos romanos."},
            {"letra": "D", "texto": "Os etruscos praticavam um politeísmo semelhante ao dos gregos, mas rejeitavam rituais religiosos e a construção de templos."},
            {"letra": "E", "texto": "Os etruscos adaptaram o alfabeto fenício para desenvolver sua própria escrita, mas muitos aspectos de seu idioma permanecem um mistério para os pesquisadores."}
        ]
    },
    {
        "posicao": 33,
        "disciplina": "Ciências Humanas",
        "areaConhecimento": "Ciências Humanas",
        "assunto": "Geografia da População / Dinâmica Demográfica e Migrações",
        "dificuldade": "MEDIO",
        "textoBase": None,
        "enunciado": "Sobre os fundamentos econômicos, sociais e políticos que influenciam a mobilidade espacial e o crescimento demográfico no mundo, analise as afirmativas:\nI.A migração internacional tem sido um fenômeno constante em busca de melhores condições econômicas, mas enfrenta crescentes barreiras em virtude de políticas migratórias mais restritivas.\nII.O crescimento populacional nos países desenvolvidos continua a superar os índices registrados em países subdesenvolvidos, devido à urbanização avançada e à alta taxa de natalidade.\nIII.A mobilidade espacial interna no Brasil está diretamente associada à desigualdade regional, com fluxos migratórios concentrados em direção às regiões Sul e Sudeste, historicamente mais industrializadas.\nIV.A estagnação demográfica em algumas nações desenvolvidas tem resultado na implementação de políticas que incentivam a imigração para suprir a demanda por mão de obra e equilibrar o sistema previdenciário.\nAssinale a alternativa CORRETA:",
        "gabaritoOficial": "B",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "Somente as afirmativas II, III e IV estão corretas."},
            {"letra": "B", "texto": "Somente as afirmativas I, III e IV estão corretas."},
            {"letra": "C", "texto": "I, II, III e IV estão corretas."},
            {"letra": "D", "texto": "Somente as afirmativas I e III estão corretas."},
            {"letra": "E", "texto": "Somente as afirmativas II e IV estão corretas."}
        ]
    },
    {
        "posicao": 34,
        "disciplina": "Ciências Humanas",
        "areaConhecimento": "Ciências Humanas",
        "assunto": "Geografia Urbana e Regional / Políticas Territoriais e Gestão do Espaço",
        "dificuldade": "FACIL",
        "textoBase": None,
        "enunciado": "Em um contexto de crescente urbanização e desigualdade regional, o papel do Estado nas políticas territoriais tem se tornado cada vez mais central para promover o desenvolvimento equilibrado e a justiça social. O Estado, ao formular políticas públicas voltadas para a gestão do território, pode influenciar diretamente a distribuição dos recursos, o uso da terra e as condições de vida das populações. Dentre as alternativas a seguir, assinale a que apresenta a principal função das políticas territoriais adotadas pelo Estado em relação à equidade e ao desenvolvimento sustentável.",
        "gabaritoOficial": "C",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "As políticas territoriais devem priorizar a centralização das decisões políticas nas grandes metrópoles, deixando os territórios rurais e periferias com pouca intervenção do Estado, para estimular a livre iniciativa e o crescimento econômico desregulado."},
            {"letra": "B", "texto": "O Estado deve atuar com políticas territoriais focadas exclusivamente na redução dos impactos ambientais nas áreas urbanas, deixando as áreas rurais e os pequenos municípios sem a necessidade de regulação ou intervenção."},
            {"letra": "C", "texto": "As políticas territoriais devem promover a redistribuição equitativa dos recursos naturais e da infraestrutura entre diferentes regiões, com o objetivo de reduzir as disparidades entre as áreas centrais e periféricas, assegurando o desenvolvimento sustentável e a justiça social."},
            {"letra": "D", "texto": "O papel do Estado nas políticas territoriais é garantir a concentração das atividades econômicas em áreas metropolitanas, uma vez que a densidade populacional e a infraestrutura urbana são fatores que contribuem para o crescimento acelerado e sustentável da economia nacional."},
            {"letra": "E", "texto": "A principal função das políticas territoriais é fomentar a especulação imobiliária nas grandes cidades, incentivando a construção de grandes empreendimentos para impulsionar o crescimento do mercado financeiro, sem considerar as necessidades das populações locais."}
        ]
    },
    {
        "posicao": 35,
        "disciplina": "Ciências Humanas",
        "areaConhecimento": "Ciências Humanas",
        "assunto": "Geopolítica e Meio Ambiente / Crise Hídrica e Mudanças Climáticas Globais",
        "dificuldade": "FACIL",
        "textoBase": None,
        "enunciado": "A sobrevivência humana está intimamente ligada à relação com os mecanismos naturais e à distribuição desigual dos recursos naturais no planeta. Essa desigualdade reflete-se tanto nos níveis de acesso quanto nos impactos ambientais decorrentes do uso dos recursos. Um exemplo recente disso está na emergência climática, que vem agravando problemas socioeconômicos em regiões vulneráveis, exacerbando situações de insegurança alimentar, hídrica e energética. Considere os seguintes cenários associados a essa relação desigual:",
        "gabaritoOficial": "E",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "O acesso limitado ao petróleo nos países do Oriente Médio, que enfrentam crises econômicas devido à escassez desse recurso estratégico."},
            {"letra": "B", "texto": "O crescimento significativo das reservas de água potável em países da América Latina devido ao degelo nas cordilheiras, garantindo maior segurança hídrica na região."},
            {"letra": "C", "texto": "A intensificação das secas em áreas subtropicais, como o sul da Espanha e da Itália, prejudicando a produção agrícola e impulsionando a dependência alimentar de importações externas."},
            {"letra": "D", "texto": "A abundância de alimentos no sul da Ásia devido às inundações sazonais provocadas pelo aumento do nível do mar, garantindo safra recorde em culturas como o arroz."},
            {"letra": "E", "texto": "A crise hídrica na região do Chifre da África, exacerbada por conflitos armados e mudanças climáticas, deixando milhões de pessoas em situação de vulnerabilidade extrema."}
        ]
    },
    {
        "posicao": 36,
        "disciplina": "Ciências Humanas",
        "areaConhecimento": "Ciências Humanas",
        "assunto": "História Medieval / As Cruzadas e o Comércio Oriente-Ocidente",
        "dificuldade": "FACIL",
        "textoBase": None,
        "enunciado": "As Cruzadas, expedições militares iniciadas no século XI sob a liderança da Igreja Católica, tiveram como objetivo declarado a recuperação de territórios sagrados, especialmente Jerusalém, das mãos dos muçulmanos. No entanto, além de seu caráter religioso, elas também foram marcadas por outros interesses. Considerando o contexto histórico, é correto afirmar que as Cruzadas:",
        "gabaritoOficial": "B",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "Impuseram domínio militar completo dos cristãos no Oriente Médio, garantindo controle contínuo sobre a Terra Santa até o final da Idade Média."},
            {"letra": "B", "texto": "Foram responsáveis por estimular o comércio entre o Oriente e o Ocidente, promovendo trocas culturais e contribuindo para o Renascimento europeu."},
            {"letra": "C", "texto": "Resultaram na unificação definitiva do cristianismo na Europa, eliminando as tensões entre católicos e ortodoxos após a reconquista de Jerusalém."},
            {"letra": "D", "texto": "Consolidaram o poder político dos reis europeus, que usaram as expedições como forma de controlar diretamente os territórios conquistados no Oriente Médio."},
            {"letra": "E", "texto": "Representaram uma tentativa de conversão forçada de muçulmanos ao cristianismo, para além de motivações econômicas ou políticas."}
        ]
    },
    {
        "posicao": 37,
        "disciplina": "Ciências Humanas",
        "areaConhecimento": "Ciências Humanas",
        "assunto": "História Contemporânea / Primeira Guerra Mundial (Causas e Antecedentes)",
        "dificuldade": "FACIL",
        "textoBase": None,
        "enunciado": "A Primeira Guerra Mundial (1914-1918), conhecida como a Grande Guerra, marcou uma das mais devastadoras e transformadoras épocas da história moderna. O conflito envolveu as principais potências europeias, divididas entre a Tríplice Entente e a Tríplice Aliança, e foi impulsionado por diversos fatores, EXCETO:",
        "gabaritoOficial": "E",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "A corrida armamentista, que levou ao desenvolvimento de arsenais militares sofisticados e ao aumento das tensões entre as potências europeias."},
            {"letra": "B", "texto": "O sistema de alianças, que criou blocos militares como a Tríplice Entente e a Tríplice Aliança, aumentando o risco de escalada de conflitos regionais para um conflito global."},
            {"letra": "C", "texto": "O nacionalismo exacerbado, que gerou rivalidades entre nações e fomentou movimentos de unificação e independência."},
            {"letra": "D", "texto": "As rivalidades imperialistas, especialmente disputas por territórios na África e na Ásia, que intensificaram os conflitos entre os países europeus."},
            {"letra": "E", "texto": "O movimento pacifista crescente entre as potências europeias, que buscava impedir a eclosão de guerras por meio de tratados e conferências."}
        ]
    },
    {
        "posicao": 38,
        "disciplina": "Ciências Humanas",
        "areaConhecimento": "Ciências Humanas",
        "assunto": "História do Brasil / Primeiro Reinado (Independência, D. Pedro I e Constituição de 1824)",
        "dificuldade": "MEDIO",
        "textoBase": None,
        "enunciado": "O Primeiro Reinado do Brasil foi o período em que Dom Pedro I governou como imperador, logo após a Proclamação da Independência, em 7 de setembro de 1822, até sua abdicação em 7 de abril de 1831. Esse período foi marcado por desafios políticos, econômicos e sociais, que moldaram os primeiros anos do Brasil como nação independente. Acerca desse assunto, julgue as frases abaixo.\nI.Após a ruptura com Portugal, Dom Pedro I enfrentou a tarefa de consolidar a independência brasileira, que não foi imediatamente reconhecida por todas as províncias nem pelas potências internacionais. Algumas regiões, como o Grão-Pará e a Bahia, resistiram ao novo governo, alinhando-se a Portugal. Foi necessário o uso de força militar para assegurar a unidade territorial e afirmar a soberania brasileira.\nII.Uma das principais realizações do Primeiro Reinado foi a elaboração da Constituição de 1824, a primeira carta constitucional do Brasil. Instituída de maneira democrática, a Constituição estabeleceu o regime monárquico constitucional e o poder moderador, uma atribuição do imperador para arbitrar conflitos entre os outros poderes.\nIII.O Primeiro Reinado enfrentou severos problemas econômicos. O Brasil herdou dívidas de Portugal, e o reconhecimento da independência pelas potências estrangeiras, como a Inglaterra, veio acompanhado de exigências onerosas, como a manutenção de privilégios comerciais britânicos.\nEstá(ão) CORRETA(S) a(s) seguinte(s) proposição(ões).",
        "gabaritoOficial": "D",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "Apenas II e III."},
            {"letra": "B", "texto": "Apenas I."},
            {"letra": "C", "texto": "Apenas III."},
            {"letra": "D", "texto": "Apenas I e III."},
            {"letra": "E", "texto": "Apenas II."}
        ]
    },
    {
        "posicao": 39,
        "disciplina": "Ciências Humanas",
        "areaConhecimento": "Ciências Humanas",
        "assunto": "História do Brasil / República Velha (Guerra de Canudos e Narrativa Historiográfica)",
        "dificuldade": "MEDIO",
        "textoBase": None,
        "enunciado": "A Guerra de Canudos, ocorrida no sertão da Bahia entre 1896 e 1897, foi um conflito que opôs o Exército Brasileiro à comunidade liderada por Antônio Conselheiro. Na época, o discurso oficial militar descrevia Canudos como um foco de fanatismo religioso e ameaça à ordem republicana, justificando a violência empregada contra seus habitantes. Em 1997, o jornal Folha de S.Paulo reinterpretou esse episódio histórico, adotando uma visão que contrasta com a narrativa militar. Segundo a análise do discurso da Folha, o conflito foi retratado como uma supressão injusta de uma comunidade marginalizada, revelando um esforço para reconstruir a memória histórica de maneira mais inclusiva e questionadora. Considerando essa abordagem, pode-se afirmar que o discurso da Folha de S.Paulo buscava:",
        "gabaritoOficial": "D",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "Promover uma abordagem neutra e desinteressada sobre Canudos, para além de interferir na construção da memória coletiva nacional."},
            {"letra": "B", "texto": "Adotar uma visão historiográfica e técnica, ignorando as implicações identitárias e sociais associadas ao conflito."},
            {"letra": "C", "texto": "Validar integralmente a versão oficial do Exército Brasileiro, reforçando os valores republicanos associados à guerra."},
            {"letra": "D", "texto": "Apresentar uma perspectiva crítica que desafia a narrativa oficial do Exército, destacando Canudos como uma resistência social à exclusão e opressão."},
            {"letra": "E", "texto": "Construir uma memória histórica que desqualifica a atuação de Antônio Conselheiro, alinhando-se à versão militar de fanatismo e desordem social."}
        ]
    },
    {
        "posicao": 40,
        "disciplina": "Ciências Humanas",
        "areaConhecimento": "Ciências Humanas",
        "assunto": "História do Brasil / Brasil Colônia (Conjuração Baiana / Revolta dos Alfaiates)",
        "dificuldade": "MEDIO",
        "textoBase": None,
        "enunciado": "A Conjuração Baiana, também conhecida como Revolta dos Alfaiates, foi um movimento de caráter separatista, ocorrido em 1798, em Salvador, Bahia, durante o período colonial brasileiro. Sobre esse assunto, julgue as sentenças abaixo como VERDADEIRAS ou FALSAS:\n1.(__)Inspirada pelos ideais iluministas e pelos ventos da Revolução Francesa, a conjuração teve como principais objetivos a independência do Brasil, a proclamação de uma república e a igualdade social. Diferentemente da Inconfidência Mineira, a Conjuração Baiana foi um movimento popular, com significativa participação de alfaiates, soldados, negros libertos, escravizados e pequenos comerciantes.\n2.(__)A revolta teve origem no descontentamento com as desigualdades sociais, a exploração econômica da colônia e a opressão das camadas mais pobres pela Coroa Portuguesa. Os líderes, como João de Deus do Nascimento, Luiz Gonzaga das Virgens e Manoel Faustino, defendiam não apenas a independência política, mas também medidas para combater a pobreza, como a abolição da escravidão e a redução dos impostos. Esses ideais eram divulgados por meio de panfletos e reuniões secretas, ganhando apoio entre os setores mais marginalizados da população.\n3.(__)Apesar de sua relevância, a Conjuração Baiana foi descoberta antes de sua concretização. O movimento foi duramente reprimido pelas autoridades coloniais, resultando na prisão e execução de seus principais líderes em praça pública, como forma de desencorajar novas revoltas. Contudo, a Conjuração Baiana deixou um importante legado histórico, ao evidenciar a insatisfação popular com o sistema colonial e ao demonstrar a presença de ideias republicanas e abolicionistas no Brasil do século XVIII.\nA sequência CORRETA é:",
        "gabaritoOficial": "D",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "1.V, 2.F, 3.F."},
            {"letra": "B", "texto": "1.F, 2.V, 3.V."},
            {"letra": "C", "texto": "1.F, 2.F, 3.V."},
            {"letra": "D", "texto": "1.V, 2.V, 3.V."},
            {"letra": "E", "texto": "1.F, 2.V, 3.F."}
        ]
    },
    {
        "posicao": 41,
        "disciplina": "Ciências Humanas",
        "areaConhecimento": "Ciências Humanas",
        "assunto": "Geografia Ambiental / Mudanças Climáticas e Impactos Socioeconômicos",
        "dificuldade": "FACIL",
        "textoBase": None,
        "enunciado": "As mudanças climáticas intensificadas pela ação antrópica estão agravando desigualdades socioeconômicas em diversas partes do mundo. Regiões economicamente menos desenvolvidas frequentemente são mais vulneráveis, pois têm menor capacidade de mitigação e adaptação aos fenômenos climáticos. Entre os exemplos de consequências desses fenômenos, destaca-se:",
        "gabaritoOficial": "E",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "O agravamento das secas em áreas subtropicais, como o sul da Espanha e da Itália, afetando a produção agrícola e aumentando a dependência alimentar de importações externas."},
            {"letra": "B", "texto": "O crescimento na oferta de terras agricultáveis em regiões equatoriais devido ao avanço do desmatamento."},
            {"letra": "C", "texto": "O aumento da disponibilidade hídrica no Nordeste do Brasil devido ao aquecimento global."},
            {"letra": "D", "texto": "A diminuição da frequência de tempestades tropicais nas áreas litorâneas do Oceano Índico."},
            {"letra": "E", "texto": "A elevação do nível do mar, afetando especialmente pequenas ilhas e regiões costeiras de países em desenvolvimento."}
        ]
    },
    {
        "posicao": 42,
        "disciplina": "Ciências Humanas",
        "areaConhecimento": "Ciências Humanas",
        "assunto": "Geografia do Brasil / Regionalização e Desenvolvimento Desigual e Combinado",
        "dificuldade": "MEDIO",
        "textoBase": None,
        "enunciado": "O Brasil, devido à sua vasta extensão territorial, diversidade econômica e características sociais distintas, apresenta um quadro de desenvolvimento desigual, que se reflete tanto nas dinâmicas regionais quanto nas políticas públicas adotadas para mitigar tais desigualdades. No entanto, a ideia de \"desenvolvimento desigual e combinado\" ajuda a entender como as diferentes regiões do país convivem com processos simultâneos de desenvolvimento e atraso, mas com inter-relações que muitas vezes cruzam as fronteiras regionais. Considerando esse contexto, assinale a alternativa que melhor explica o conceito de desenvolvimento desigual e combinado no Brasil e suas implicações para a regionalização do território.",
        "gabaritoOficial": "D",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "A regionalização do Brasil é marcada por uma uniformidade no desenvolvimento das diversas regiões, o que implica em políticas públicas que devem ser unificadas para garantir o mesmo nível de crescimento econômico e social em todo o território nacional, sem levar em conta as peculiaridades regionais."},
            {"letra": "B", "texto": "O desenvolvimento desigual e combinado no Brasil pode ser entendido como a coexistência de regiões altamente industrializadas, como o Sudeste, e áreas predominantemente rurais, como o Norte, sem qualquer interdependência entre essas regiões, o que torna as políticas públicas voltadas exclusivamente para cada uma delas, sem articulação."},
            {"letra": "C", "texto": "O desenvolvimento desigual e combinado no Brasil pode ser compreendido como a persistência de um modelo de crescimento concentrado nas regiões mais desenvolvidas, enquanto outras, como o Norte e o Nordeste, enfrentam um crescimento estagnado, sem qualquer influência ou interação das regiões mais avançadas, o que perpetua a desigualdade."},
            {"letra": "D", "texto": "As regiões brasileiras, embora apresentem níveis de desenvolvimento e modernização distintos, estão interconectadas por fluxos econômicos e sociais que configuram um processo de desenvolvimento desigual, mas combinado, onde as transformações de uma região impactam diretamente o desenvolvimento de outras, acelerando processos de urbanização e industrialização."},
            {"letra": "E", "texto": "O conceito de desenvolvimento desigual e combinado no Brasil descreve uma realidade onde o Norte e o Nordeste são completamente isolados do restante do país, sendo mais dependentes de modelos de desenvolvimento agrário e menos afetados por dinâmicas urbanas e industriais, o que limita as interações inter-regionais."}
        ]
    },
    {
        "posicao": 43,
        "disciplina": "Ciências Humanas",
        "areaConhecimento": "Ciências Humanas",
        "assunto": "Geopolítica / Globalização, Neoliberalismo e Relações Centro-Periferia",
        "dificuldade": "MEDIO",
        "textoBase": None,
        "enunciado": "Nas últimas décadas, o mundo globalizado presenciou um aumento na interdependência entre os países, mas esse fenômeno ocorreu de forma desigual, reforçando relações de dominação e subordinação político-econômica. Em países periféricos, a adoção de políticas neoliberais, como a abertura irrestrita ao capital estrangeiro e a privatização de setores estratégicos, resultou em uma dependência econômica significativa em relação aos países centrais. Enquanto isso, as organizações internacionais, como o FMI e o Banco Mundial, passaram a desempenhar papéis cada vez mais influentes na formulação de políticas econômicas em nações menos desenvolvidas, muitas vezes em detrimento de sua autonomia. Diante desse contexto, qual das alternativas melhor exemplifica as dinâmicas de dominação e subordinação observadas entre países centrais e periféricos?",
        "gabaritoOficial": "B",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "A priorização de políticas públicas que promovem o desenvolvimento igualitário entre países do hemisfério Norte e Sul."},
            {"letra": "B", "texto": "A aplicação de políticas neoliberais em países periféricos, que intensificaram a dependência econômica em relação aos países centrais."},
            {"letra": "C", "texto": "A expansão das megacidades nos países desenvolvidos, que se deu sem impactos negativos nos espaços periféricos."},
            {"letra": "D", "texto": "O equilíbrio econômico entre diferentes nações promovido pela globalização, fortalecendo os Estados nacionais de forma uniforme."},
            {"letra": "E", "texto": "O fortalecimento da economia agrícola dos países subdesenvolvidos, garantido pela autodeterminação econômica sem intervenção externa."}
        ]
    },
    {
        "posicao": 44,
        "disciplina": "Ciências Humanas",
        "areaConhecimento": "Ciências Humanas",
        "assunto": "Geografia Agrária e Urbana / Agricultura de Precisão e Redes Produtivas",
        "dificuldade": "MEDIO",
        "textoBase": None,
        "enunciado": "Com o avanço das tecnologias no âmbito da agricultura e das cidades, o desenvolvimento tecnológico tem gerado transformações significativas tanto na organização do espaço urbano quanto rural. Nas últimas décadas, a introdução de tecnologias de ponta no campo, como a agricultura de precisão, tem proporcionado maior eficiência na produção, mas também traz implicações tanto no espaço rural quanto nos fluxos globais de consumo e produção. As inovações tecnológicas impulsionam a interconexão das áreas rurais com as redes produtivas globais, alterando a estrutura econômica e as dinâmicas sociais em locais que antes tinham economias predominantemente autossuficientes.\nAlém disso, a urbanização acelerada e a construção de grandes infraestruturas têm modificado a forma como as cidades lidam com o crescente número de habitantes. No campo, a introdução de tecnologias de automação e monitoramento tem permitido uma maior produtividade e integração com as redes globais de mercado, mas também ocasiona uma intensificação da desigualdade e dos impactos ambientais. De forma geral, o desenvolvimento tecnológico está redesenhando o espaço global, o que implica não apenas na intensificação da urbanização, mas também na mudança nas práticas produtivas e nas relações socioeconômicas entre cidade e campo. Com base nesse contexto, qual alternativa abaixo melhor descreve o impacto das práticas tecnológicas no setor rural e sua inserção nas redes globais de produção?",
        "gabaritoOficial": "A",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "A agricultura de precisão e as tecnologias de automação no campo aumentam a produtividade rural, mas também contribuem para a maior interconexão das áreas rurais com as redes globais de consumo e produção."},
            {"letra": "B", "texto": "A intensificação do uso de tecnologias tradicionais nas áreas rurais, focando no aumento da produção sem qualquer preocupação com as interações econômicas globais, mantendo a economia rural isolada e autossuficiente."},
            {"letra": "C", "texto": "A modernização das grandes cidades, através da expansão de sua infraestrutura urbana e o aumento das condições de vida nas periferias, que gradualmente vão se conectando ao restante da cidade. Embora a tecnologia seja mais presente nas áreas urbanas, a melhoria nas periferias não se reflete no setor rural."},
            {"letra": "D", "texto": "A desconexão das áreas rurais das cadeias produtivas globais, onde a crescente dependência dos mercados internos cria uma economia rural mais autossuficiente e desvinculada das grandes economias internacionais."},
            {"letra": "E", "texto": "A diminuição do papel do setor rural nas economias periféricas, com uma crescente tendência de que as regiões metropolitanas concentrem a produção e o consumo, de modo que as práticas tecnológicas urbanas desconsideram as zonas rurais."}
        ]
    },
    {
        "posicao": 45,
        "disciplina": "Ciências Humanas",
        "areaConhecimento": "Ciências Humanas",
        "assunto": "Geopolítica / Recursos Naturais Estratégicos (Mineração, Terras Raras e Energia)",
        "dificuldade": "MEDIO",
        "textoBase": None,
        "enunciado": "Sobre as desigualdades na distribuição e apropriação dos recursos naturais no mundo, considere as afirmativas:\nI.Os países do Hemisfério Norte concentram a maior parte das reservas globais de petróleo, o que lhes permite dominar o mercado energético internacional.\nII.A exploração mineral em países africanos tem gerado riquezas concentradas em grandes corporações multinacionais, enquanto as comunidades locais frequentemente permanecem em condições de pobreza extrema.\nIII.A exploração de terras raras, usadas na fabricação de dispositivos tecnológicos, está amplamente concentrada na China, que domina a produção global desses minerais.\nIV.Os impactos ambientais gerados pela produção de energia hidrelétrica, como inundações de grandes áreas e deslocamento de populações, frequentemente são ignorados em discursos sobre sustentabilidade.\nAssinale a alternativa CORRETA:",
        "gabaritoOficial": "D",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "Somente as afirmativas I e II estão corretas."},
            {"letra": "B", "texto": "Somente as afirmativas I, III e IV estão corretas."},
            {"letra": "C", "texto": "Somente as afirmativas I, II e IV estão corretas."},
            {"letra": "D", "texto": "Somente as afirmativas II, III e IV estão corretas."},
            {"letra": "E", "texto": "I, II, III e IV estão corretas."}
        ]
    },

    # --- Matemática (Q46 a Q55) ---
    {
        "posicao": 46,
        "disciplina": "Matemática",
        "areaConhecimento": "Matemática",
        "assunto": "Análise Combinatória / Permutação com Repetição (Anagramas)",
        "dificuldade": "FACIL",
        "textoBase": None,
        "enunciado": 'Em uma competição de palavras, um desafio consiste em formar todas as combinações possíveis com as letras de uma palavra específica. A palavra escolhida foi "CASA", que possui letras repetidas. Quantos anagramas distintos podem ser formados utilizando todas as letras dessa palavra?',
        "gabaritoOficial": "E",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "36"},
            {"letra": "B", "texto": "72"},
            {"letra": "C", "texto": "24"},
            {"letra": "D", "texto": "48"},
            {"letra": "E", "texto": "12"}
        ]
    },
    {
        "posicao": 47,
        "disciplina": "Matemática",
        "areaConhecimento": "Matemática",
        "assunto": "Estatística / Média Aritmética Simples",
        "dificuldade": "FACIL",
        "textoBase": None,
        "enunciado": "Durante uma pesquisa estatística, um analista precisa calcular a média dos valores coletados em um experimento. Os números registrados foram 5, 10, 15 e 20. Qual é a média desses valores?",
        "gabaritoOficial": "A",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "12,5"},
            {"letra": "B", "texto": "20"},
            {"letra": "C", "texto": "17,5"},
            {"letra": "D", "texto": "10"},
            {"letra": "E", "texto": "15"}
        ]
    },
    {
        "posicao": 48,
        "disciplina": "Matemática",
        "areaConhecimento": "Matemática",
        "assunto": "Aritmética / Frações e Proporções (Questão Anulada)",
        "dificuldade": "FACIL",
        "textoBase": None,
        "enunciado": "Em um jantar, uma pizza foi dividida em partes iguais para que todos pudessem se servir. Uma pessoa comeu 3/5 da pizza total e, dos pedaços restantes, decidiu embalar metade para levar para casa e dar a outra metade para um amigo. Considerando essa divisão, quanto da pizza ainda restará na mesa ao final do jantar?",
        "gabaritoOficial": "ANULADA",
        "anulada": True,
        "alternativas": [
            {"letra": "A", "texto": "2/5"},
            {"letra": "B", "texto": "1/5"},
            {"letra": "C", "texto": "3/10"},
            {"letra": "D", "texto": "1/10"},
            {"letra": "E", "texto": "1/7"}
        ]
    },
    {
        "posicao": 49,
        "disciplina": "Matemática",
        "areaConhecimento": "Matemática",
        "assunto": "Matemática Financeira / Juros Simples e Montante",
        "dificuldade": "FACIL",
        "textoBase": None,
        "enunciado": "Uma loja planeja investir R$ 1.000,00 em um fundo que rende juros simples de 5% ao mês para cobrir despesas sazonais no futuro. Após 4 meses, o gerente financeiro verificará o montante disponível para reinvestir no negócio. Qual será o valor acumulado ao final desse período?",
        "gabaritoOficial": "C",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "R$ 1.500,00"},
            {"letra": "B", "texto": "R$ 1.300,00"},
            {"letra": "C", "texto": "R$ 1.200,00"},
            {"letra": "D", "texto": "R$ 1.250,00"},
            {"letra": "E", "texto": "R$ 1.100,00"}
        ]
    },
    {
        "posicao": 50,
        "disciplina": "Matemática",
        "areaConhecimento": "Matemática",
        "assunto": "Conjuntos Numéricos / Números Reais e Irracionais",
        "dificuldade": "FACIL",
        "textoBase": None,
        "enunciado": "Os conjuntos numéricos abrangem diferentes classificações, como naturais, inteiros, racionais e irracionais, cada um com características distintas que os definem. Com base nessa divisão, identifique a alternativa que apresenta um número pertencente ao conjunto dos números irracionais.",
        "gabaritoOficial": "E",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "2+3i"},
            {"letra": "B", "texto": "1/2"},
            {"letra": "C", "texto": "-3"},
            {"letra": "D", "texto": "8"},
            {"letra": "E", "texto": "√2"}
        ]
    },
    {
        "posicao": 51,
        "disciplina": "Matemática",
        "areaConhecimento": "Matemática",
        "assunto": "Trigonometria / Relação Fundamental da Trigonometria",
        "dificuldade": "FACIL",
        "textoBase": None,
        "enunciado": "Durante uma aula de trigonometria, o professor pediu aos alunos que analisassem ângulos em múltiplos de 90º e suas respectivas razões trigonométricas.\nSabendo que sin(45º)=cos(45º)=√(2/2), qual é o valor de sin²(45º)+cos²(45º)?",
        "gabaritoOficial": "E",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "√2"},
            {"letra": "B", "texto": "√(2/2)"},
            {"letra": "C", "texto": "√(1/2)"},
            {"letra": "D", "texto": "0"},
            {"letra": "E", "texto": "1"}
        ]
    },
    {
        "posicao": 52,
        "disciplina": "Matemática",
        "areaConhecimento": "Matemática",
        "assunto": "Geometria Plana / Cálculo de Área de Figuras Planas (Triângulo)",
        "dificuldade": "FACIL",
        "textoBase": None,
        "enunciado": "Um engenheiro está projetando a fachada de um edifício e precisa calcular a área de um triângulo decorativo para definir a quantidade de material necessário. A base desse triângulo mede 8 cm e sua altura é de 5 cm. Qual é a área dessa figura?",
        "gabaritoOficial": "C",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "70 cm²"},
            {"letra": "B", "texto": "30 cm²"},
            {"letra": "C", "texto": "20 cm²"},
            {"letra": "D", "texto": "50 cm²"},
            {"letra": "E", "texto": "40 cm²"}
        ]
    },
    {
        "posicao": 53,
        "disciplina": "Matemática",
        "areaConhecimento": "Matemática",
        "assunto": "Funções / Função Quadrática (Cálculo de Valor Numérico)",
        "dificuldade": "FACIL",
        "textoBase": None,
        "enunciado": "Uma empresa está analisando uma função quadrática que modela o custo de produção, onde f(x)=x² - 4x + 3 sendo x a quantidade de itens produzidos em centenas. Para uma produção de 300 itens (x=3), qual é o custo correspondente representado por f(3)?",
        "gabaritoOficial": "E",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "-1"},
            {"letra": "B", "texto": "1"},
            {"letra": "C", "texto": "3"},
            {"letra": "D", "texto": "4"},
            {"letra": "E", "texto": "0"}
        ]
    },
    {
        "posicao": 54,
        "disciplina": "Matemática",
        "areaConhecimento": "Matemática",
        "assunto": "Álgebra Linear / Sistemas Lineares (Classificação e Soluções)",
        "dificuldade": "FACIL",
        "textoBase": None,
        "enunciado": "Em uma fábrica, dois setores precisam compartilhar recursos de maneira que o total de recursos alocados, representado por x+y=6, seja distribuído igualmente entre os dois setores. Além disso, uma auditoria verificou que a alocação dobrada desses recursos, representada por 2x+2y=12, também precisa ser validada. Considerando o contexto, quantas soluções existem para esse sistema de equações?",
        "gabaritoOficial": "B",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "Nenhuma."},
            {"letra": "B", "texto": "Infinitas."},
            {"letra": "C", "texto": "Dez."},
            {"letra": "D", "texto": "Duas."},
            {"letra": "E", "texto": "Uma."}
        ]
    },
    {
        "posicao": 55,
        "disciplina": "Matemática",
        "areaConhecimento": "Matemática",
        "assunto": "Polinômios / Valor Numérico de Polinômios",
        "dificuldade": "FACIL",
        "textoBase": None,
        "enunciado": "Em muitas situações, funções polinomiais são usadas para modelar fenômenos ou calcular valores específicos com base em uma variável. Considerando o polinômio P(x)=x³ - 2x² + x. Qual é o valor de P(2)?",
        "gabaritoOficial": "B",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "4"},
            {"letra": "B", "texto": "2"},
            {"letra": "C", "texto": "10"},
            {"letra": "D", "texto": "8"},
            {"letra": "E", "texto": "12"}
        ]
    },

    # --- Informática (Q56 a Q60) ---
    {
        "posicao": 56,
        "disciplina": "Informática",
        "areaConhecimento": "Informática",
        "assunto": "Redes de Computadores / Internet, Intranet e Extranet",
        "dificuldade": "FACIL",
        "textoBase": None,
        "enunciado": "Com o crescimento da conectividade digital, a internet e a intranet desempenham papéis cruciais no ambiente corporativo e pessoal, facilitando o compartilhamento de informações e a comunicação. Além disso, uma série de tecnologias, ferramentas e aplicativos estão disponíveis para otimizar o uso dessas redes. Sobre esse assunto, assinale a alternativa CORRETA.",
        "gabaritoOficial": "B",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "Ferramentas de comunicação como e-mails e chats são exclusivas da Internet, não sendo aplicáveis à intranet."},
            {"letra": "B", "texto": "A intranet é uma rede privada que funciona de forma semelhante à internet, mas com a limitação de acesso apenas a usuários autorizados dentro de uma organização, enquanto a Internet é uma rede pública."},
            {"letra": "C", "texto": "Aplicativos como o Google Drive, que permitem o armazenamento e o compartilhamento de arquivos, são exclusivamente utilizados em redes intranet, não podendo ser acessados via Internet."},
            {"letra": "D", "texto": "A principal diferença entre a Internet e a intranet é que a intranet não oferece possibilidade de navegação em sites externos, enquanto a Internet é uma rede exclusivamente interna."},
            {"letra": "E", "texto": "A internet é utilizada apenas para fins de entretenimento, enquanto a intranet é voltada exclusivamente para o uso corporativo e profissional."}
        ]
    },
    {
        "posicao": 57,
        "disciplina": "Informática",
        "areaConhecimento": "Informática",
        "assunto": "Arquitetura e Hardware / Memórias (Cache, RAM, ROM)",
        "dificuldade": "FACIL",
        "textoBase": None,
        "enunciado": "No contexto dos sistemas de computação, há um tipo de memória de alta velocidade integrada ao processador que tem como função armazenar temporariamente dados frequentemente acessados. Isso permite que o processador reduza o tempo de acesso a informações, aumentando significativamente o desempenho do sistema. Essa memória é conhecida como:",
        "gabaritoOficial": "A",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "Cache."},
            {"letra": "B", "texto": "Memória ROM."},
            {"letra": "C", "texto": "Armazenamento em Nuvem."},
            {"letra": "D", "texto": "Memória RAM."},
            {"letra": "E", "texto": "Threads."}
        ]
    },
    {
        "posicao": 58,
        "disciplina": "Informática",
        "areaConhecimento": "Informática",
        "assunto": "Suítes de Escritório / Microsoft Word (Controlar Alterações)",
        "dificuldade": "FACIL",
        "textoBase": None,
        "enunciado": "Considere que você esteja elaborando um relatório extenso no Microsoft Word em colaboração com diversos colegas. Vocês precisam revisar conteúdos, sugerir mudanças e fazer observações de forma organizada, sem que essas edições se percam ou sejam aplicadas diretamente no texto final. Dessa forma, todos podem visualizar quem alterou o quê, decidir se aceitam ou rejeitam determinadas modificações e ainda trocar comentários sobre possíveis melhorias. Qual recurso do Word permite acompanhar em detalhe cada mudança feita no documento, facilitando a revisão colaborativa e permitindo que múltiplos revisores trabalhem no mesmo arquivo?",
        "gabaritoOficial": "D",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "Inserir Referências Cruzadas."},
            {"letra": "B", "texto": "Localizar e Substituir."},
            {"letra": "C", "texto": "Ferramenta de Tabelas."},
            {"letra": "D", "texto": "Controlar Alterações."},
            {"letra": "E", "texto": "Painel de Navegação."}
        ]
    },
    {
        "posicao": 59,
        "disciplina": "Informática",
        "areaConhecimento": "Informática",
        "assunto": "Segurança da Informação / Malwares (Ransomware, Spyware, Worm, Trojan)",
        "dificuldade": "FACIL",
        "textoBase": None,
        "enunciado": "Uma empresa de médio porte relatou recentemente um incidente de segurança em que vários computadores de seu parque tecnológico foram subitamente bloqueados. De acordo com relatos, os arquivos essenciais para a operação (bancos de dados de clientes, planilhas financeiras e documentos de projetos) foram criptografados, tornando-se inacessíveis. Além disso, uma mensagem exibida nas telas dos usuários exigia o pagamento de uma quantia em criptomoeda como resgate para a liberação dos dados. Diante desse cenário, qual é o tipo de malware que tem como principal característica criptografar arquivos e solicitar um pagamento para que a vítima recupere o acesso a essas informações?",
        "gabaritoOficial": "D",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "Keylogger."},
            {"letra": "B", "texto": "Worm."},
            {"letra": "C", "texto": "Cavalo de Troia."},
            {"letra": "D", "texto": "Ransomware."},
            {"letra": "E", "texto": "Spyware."}
        ]
    },
    {
        "posicao": 60,
        "disciplina": "Informática",
        "areaConhecimento": "Informática",
        "assunto": "Segurança da Informação / Certificação e Assinatura Digital (ICP-Brasil)",
        "dificuldade": "MEDIO",
        "textoBase": None,
        "enunciado": "No mundo digital moderno, a proteção da integridade e autenticidade das informações tornou-se uma prioridade, especialmente com o crescente uso de transações online, troca de documentos e interações virtuais. Nesse contexto, a certificação digital e a assinatura digital desempenham um papel fundamental para garantir a segurança, a veracidade e a confiabilidade dos dados em ambientes eletrônicos. Sobre esse assunto, julgue as sentenças abaixo como VERDADEIRAS ou FALSAS:\n1.(__)A assinatura digital é um mecanismo de segurança utilizado para autenticar a identidade de uma pessoa ou entidade em transações realizadas pela intranet. Funciona por meio de um sistema de chaves criptográficas privadas, que garantem a autenticidade e a integridade das informações trocadas em plataformas analógicas.\n2.(__)A certificação digital é uma técnica criptográfica utilizada para garantir a autoria, integridade e repúdio de um documento eletrônico. Ao contrário de uma certificação manuscrita, que pode ser facilmente falsificada, ela é baseada em um sistema de criptografia simétrica e está intimamente ligada à identidade do assinante.\n3.(__)A certificação digital é emitida por uma Autoridade Certificadora (AC), uma entidade de confiança, que valida a identidade do solicitante e emite um certificado digital. Esse certificado é um arquivo eletrônico que contém informações sobre a identidade do titular, como nome, CPF ou CNPJ, e a chave pública do titular.\nA sequência CORRETA é:",
        "gabaritoOficial": "C",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "1.V, 2.F, 3.V."},
            {"letra": "B", "texto": "1.V, 2.F, 3.F."},
            {"letra": "C", "texto": "1.F, 2.F, 3.V."},
            {"letra": "D", "texto": "1.F, 2.V, 3.V."},
            {"letra": "E", "texto": "1.V, 2.V, 3.F."}
        ]
    },

    # --- Direito (Q61 a Q80) ---
    {
        "posicao": 61,
        "disciplina": "Direito",
        "areaConhecimento": "Direito",
        "assunto": "Direito Processual Penal Militar / Inquérito Policial Militar (Finalidade e Atribuições)",
        "dificuldade": "FACIL",
        "textoBase": None,
        "enunciado": "Durante uma operação de patrulha, um soldado foi acusado de cometer um abuso de autoridade contra um civil, sendo instaurado um inquérito policial militar para apuração dos fatos. Considerando as normas do Direito Processual Penal Militar, qual é a principal finalidade desse inquérito?",
        "gabaritoOficial": "A",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "Investigar crimes militares e formar a base para a denúncia."},
            {"letra": "B", "texto": "Gerar relatórios administrativos de conduta."},
            {"letra": "C", "texto": "Solucionar conflitos internos nas corporações militares."},
            {"letra": "D", "texto": "Processar os militares por infrações administrativas."},
            {"letra": "E", "texto": "Aplicar sanções aos crimes cometidos por civis contra militares."}
        ]
    },
    {
        "posicao": 62,
        "disciplina": "Direito",
        "areaConhecimento": "Direito",
        "assunto": "Direito Constitucional / Forças Armadas e Segurança Pública (Art. 142 CF/88)",
        "dificuldade": "FACIL",
        "textoBase": None,
        "enunciado": "Durante uma aula de formação para militares estaduais, o instrutor destacou a importância das Forças Armadas no sistema constitucional brasileiro. Ele explicou que essas instituições possuem uma missão específica, prevista na Constituição Federal, para garantir a segurança do país em situações excepcionais, como ameaças externas ou grave comprometimento da ordem interna. Qual é a principal missão das Forças Armadas, segundo a Constituição Federal?",
        "gabaritoOficial": "E",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "Legislar sobre segurança interna."},
            {"letra": "B", "texto": "Fiscalizar o cumprimento de normas ambientais."},
            {"letra": "C", "texto": "Promover políticas públicas de segurança."},
            {"letra": "D", "texto": "Coordenar as ações das polícias militares."},
            {"letra": "E", "texto": "Garantir a soberania nacional e a Lei e a ordem."}
        ]
    },
    {
        "posicao": 63,
        "disciplina": "Direito",
        "areaConhecimento": "Direito",
        "assunto": "Direito Processual Penal / Provas (Exame de Corpo de Delito - Art. 158 CPP)",
        "dificuldade": "FACIL",
        "textoBase": None,
        "enunciado": "Durante uma ocorrência envolvendo agressão física em um bairro residencial, o Soldado Paulo atendeu a vítima, que apresentava sinais visíveis de lesão corporal. Ao registrar o boletim de ocorrência, ele destacou que seria necessário realizar um exame de corpo de delito para confirmar a natureza e extensão das lesões. Nessa situação, de acordo com o Código de Processo Penal, o exame de corpo de delito é:",
        "gabaritoOficial": "B",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "Facultativo, dependendo do pedido da vítima."},
            {"letra": "B", "texto": "Obrigatório, salvo se não houver vestígios."},
            {"letra": "C", "texto": "Realizado apenas em casos de morte."},
            {"letra": "D", "texto": "Dispensável se houver testemunhas."},
            {"letra": "E", "texto": "Opcional, a critério da autoridade policial."}
        ]
    },
    {
        "posicao": 64,
        "disciplina": "Direito",
        "areaConhecimento": "Direito",
        "assunto": "Direito Penal Militar / Crimes Militares em Espécie (Embriaguez em Serviço - Art. 202 CPM)",
        "dificuldade": "FACIL",
        "textoBase": None,
        "enunciado": "O Cabo Roberto foi flagrado em serviço apresentando sinais evidentes de embriaguez, comprovados por exame técnico. De acordo com o Código Penal Militar, essa conduta configura:",
        "gabaritoOficial": "B",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "Motim."},
            {"letra": "B", "texto": "Embriaguez em serviço."},
            {"letra": "C", "texto": "Deserção."},
            {"letra": "D", "texto": "Insubordinação."},
            {"letra": "E", "texto": "Desrespeito a símbolo nacional."}
        ]
    },
    {
        "posicao": 65,
        "disciplina": "Direito",
        "areaConhecimento": "Direito",
        "assunto": "Direito Processual Penal / Prisão em Flagrante (Espécies de Flagrante - Flagrante Próprio)",
        "dificuldade": "FACIL",
        "textoBase": None,
        "enunciado": "Durante um patrulhamento, o Soldado Antônio avistou um indivíduo tentando arrombar a porta de um comércio. O suspeito foi detido no momento da tentativa de invasão. Qual tipo de flagrante foi configurado nessa situação?",
        "gabaritoOficial": "A",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "Flagrante próprio."},
            {"letra": "B", "texto": "Flagrante diferido."},
            {"letra": "C", "texto": "Flagrante impróprio."},
            {"letra": "D", "texto": "Flagrante forjado."},
            {"letra": "E", "texto": "Flagrante presumido."}
        ]
    },
    {
        "posicao": 66,
        "disciplina": "Direito",
        "areaConhecimento": "Direito",
        "assunto": "Direitos Humanos / Convenção Internacional sobre Discriminação Racial",
        "dificuldade": "FACIL",
        "textoBase": None,
        "enunciado": "A Convenção Internacional sobre a Eliminação de Todas as Formas de Discriminação Racial proíbe práticas discriminatórias baseadas em:",
        "gabaritoOficial": "E",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "Religião e orientação sexual."},
            {"letra": "B", "texto": "Deficiência física ou mental."},
            {"letra": "C", "texto": "Afiliações políticas."},
            {"letra": "D", "texto": "Condições socioeconômicas."},
            {"letra": "E", "texto": "Origem étnica ou racial."}
        ]
    },
    {
        "posicao": 67,
        "disciplina": "Direito",
        "areaConhecimento": "Direito",
        "assunto": "Direito Penal / Crimes Contra a Pessoa (Crime de Ameaça - Art. 147 CP)",
        "dificuldade": "FACIL",
        "textoBase": None,
        "enunciado": 'O Soldado Roberto, durante uma discussão com um cidadão que questionava uma abordagem, afirmou que "quebraria todos os dentes" do indivíduo se ele continuasse a reclamar. O cidadão, temendo pela sua integridade física, cessou imediatamente qualquer questionamento. Qual crime foi cometido pelo Soldado Roberto?',
        "gabaritoOficial": "A",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "Ameaça."},
            {"letra": "B", "texto": "Injúria."},
            {"letra": "C", "texto": "Difamação."},
            {"letra": "D", "texto": "Calúnia."},
            {"letra": "E", "texto": "Constrangimento ilegal."}
        ]
    },
    {
        "posicao": 68,
        "disciplina": "Direito",
        "areaConhecimento": "Direito",
        "assunto": "Direito Penal / Crimes Contra a Paz Pública (Incitação ao Crime - Art. 286 CP)",
        "dificuldade": "MEDIO",
        "textoBase": None,
        "enunciado": 'Durante um protesto contra a construção de um empreendimento público, um manifestante utilizou um megafone para conclamar os participantes a incendiar prédios do governo local, argumentando que era a única forma de "chamar a atenção das autoridades". Com base no Código Penal, a conduta do manifestante configura:',
        "gabaritoOficial": "C",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "Apologia de crime."},
            {"letra": "B", "texto": "Constrangimento ilegal."},
            {"letra": "C", "texto": "Incitação ao crime."},
            {"letra": "D", "texto": "Ameaça."},
            {"letra": "E", "texto": "Desacato."}
        ]
    },
    {
        "posicao": 69,
        "disciplina": "Direito",
        "areaConhecimento": "Direito",
        "assunto": "Legislação Extravagante / Abuso de Autoridade (Lei 13.869/2019 - Prisão para Averiguação)",
        "dificuldade": "FACIL",
        "textoBase": None,
        "enunciado": 'O Comandante de uma operação determinou a prisão de um suspeito sem flagrante ou ordem judicial, apenas para "averiguações". Essa conduta caracteriza:',
        "gabaritoOficial": "C",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "Ato regular de poder discricionário."},
            {"letra": "B", "texto": "Prisão disciplinar."},
            {"letra": "C", "texto": "Abuso de autoridade."},
            {"letra": "D", "texto": "Exercício legítimo do poder de polícia."},
            {"letra": "E", "texto": "Detenção preventiva."}
        ]
    },
    {
        "posicao": 70,
        "disciplina": "Direito",
        "areaConhecimento": "Direito",
        "assunto": "Direito Penal Militar / Crimes Contra o Serviço Militar (Abandono de Posto - Art. 195 CPM)",
        "dificuldade": "FACIL",
        "textoBase": None,
        "enunciado": "Durante uma patrulha noturna, o Cabo Luiz deixou seu posto antes do horário estipulado. Minutos depois, foi encontrado em um bar próximo, alegando que sua ausência não comprometeria a missão. Qual o crime descrito no Código Penal Militar foi cometido pelo Cabo Luiz?",
        "gabaritoOficial": "A",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "Crime de abandono de posto."},
            {"letra": "B", "texto": "Crime de descumprimento de missão."},
            {"letra": "C", "texto": "Crime de deserção."},
            {"letra": "D", "texto": "Crime de insubmissão."},
            {"letra": "E", "texto": "Crime de insubordinação."}
        ]
    },
    {
        "posicao": 71,
        "disciplina": "Direito",
        "areaConhecimento": "Direito",
        "assunto": "Direito Administrativo / Princípios da Administração Pública (Questão Anulada)",
        "dificuldade": "FACIL",
        "textoBase": None,
        "enunciado": "O Soldado Pedro recebeu ordens para usar um veículo público em caráter particular para transportar materiais pessoais de um superior. Ao recusar o pedido, argumentou que a ordem violava princípios da administração pública. Qual princípio foi corretamente invocado pelo Soldado?",
        "gabaritoOficial": "ANULADA",
        "anulada": True,
        "alternativas": [
            {"letra": "A", "texto": "Princípio da publicidade."},
            {"letra": "B", "texto": "Princípio da eficiência."},
            {"letra": "C", "texto": "Princípio da impessoalidade."},
            {"letra": "D", "texto": "Princípio da moralidade."},
            {"letra": "E", "texto": "Princípio da legalidade."}
        ]
    },
    {
        "posicao": 72,
        "disciplina": "Direito",
        "areaConhecimento": "Direito",
        "assunto": "Direito Penal Militar / Crimes Contra a Autoridade Militar (Insubordinação - Art. 163 CPM)",
        "dificuldade": "FACIL",
        "textoBase": None,
        "enunciado": "Em uma reunião operacional, o Soldado Cláudio se recusou a cumprir uma ordem direta de seu superior hierárquico, alegando que discordava da estratégia apresentada. Qual crime militar foi cometido?",
        "gabaritoOficial": "B",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "Abandono de posto."},
            {"letra": "B", "texto": "Insubordinação."},
            {"letra": "C", "texto": "Motim."},
            {"letra": "D", "texto": "Deserção."},
            {"letra": "E", "texto": "Desacato."}
        ]
    },
    {
        "posicao": 73,
        "disciplina": "Direito",
        "areaConhecimento": "Direito",
        "assunto": "Direito Constitucional / Princípios Fundamentais (Art. 1º a 4º CF/88)",
        "dificuldade": "FACIL",
        "textoBase": None,
        "enunciado": "Os princípios fundamentais da Constituição Federal de 1988 são os pilares que sustentam o ordenamento jurídico e orientam a atuação estatal. Qual dos itens abaixo representa corretamente um desses princípios?",
        "gabaritoOficial": "C",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "Extinção da diversidade cultural."},
            {"letra": "B", "texto": "Centralização do poder em nível federal."},
            {"letra": "C", "texto": "Soberania nacional."},
            {"letra": "D", "texto": "Separação absoluta entre Estado e sociedade."},
            {"letra": "E", "texto": "Subordinação dos Estados ao governo central."}
        ]
    },
    {
        "posicao": 74,
        "disciplina": "Direito",
        "areaConhecimento": "Direito",
        "assunto": "Direito Penal Militar / Deserção (Art. 187 CPM)",
        "dificuldade": "FACIL",
        "textoBase": None,
        "enunciado": "O Soldado Almeida, sem autorização, ausentou-se de seu posto por mais de oito dias consecutivos, alegando problemas pessoais. Ao ser encontrado, ele afirmou que pretendia retornar quando resolvesse suas questões pessoais. Qual medida deve ser adotada contra o Soldado Almeida?",
        "gabaritoOficial": "A",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "Instauração de inquérito policial militar por deserção."},
            {"letra": "B", "texto": "Enquadramento por descumprimento de missão."},
            {"letra": "C", "texto": "Condução coercitiva para retorno imediato ao serviço."},
            {"letra": "D", "texto": "Instauração de processo por insubordinação."},
            {"letra": "E", "texto": "Aplicação de sanção administrativa por abandono de posto."}
        ]
    },
    {
        "posicao": 75,
        "disciplina": "Direito",
        "areaConhecimento": "Direito",
        "assunto": "Direito Constitucional / Organização do Estado (Competências da União - Art. 21 CF/88)",
        "dificuldade": "MEDIO",
        "textoBase": None,
        "enunciado": "Em uma operação conjunta entre estados vizinhos, foi necessário delimitar as competências de cada ente. Segundo a Constituição Federal, qual das opções abaixo é uma competência exclusiva da União?",
        "gabaritoOficial": "D",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "Estabelecer normas gerais de saúde pública."},
            {"letra": "B", "texto": "Legislar sobre trânsito e transporte."},
            {"letra": "C", "texto": "Exercer o poder de polícia ambiental."},
            {"letra": "D", "texto": "Declarar guerra e celebrar a paz."},
            {"letra": "E", "texto": "Organizar e prestar serviços de segurança pública."}
        ]
    },
    {
        "posicao": 76,
        "disciplina": "Direito",
        "areaConhecimento": "Direito",
        "assunto": "Direito Penal / Crimes Contra a Dignidade Sexual (Assédio Sexual - Art. 216-A CP)",
        "dificuldade": "FACIL",
        "textoBase": None,
        "enunciado": "Durante uma reunião de trabalho, um superior hierárquico fez comentários de cunho sexual direcionados a uma subordinada, constrangendo-a. Essa conduta configura:",
        "gabaritoOficial": "E",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "Ameaça."},
            {"letra": "B", "texto": "Constrangimento ilegal."},
            {"letra": "C", "texto": "Injúria."},
            {"letra": "D", "texto": "Corrupção passiva."},
            {"letra": "E", "texto": "Assédio sexual."}
        ]
    },
    {
        "posicao": 77,
        "disciplina": "Direito",
        "areaConhecimento": "Direito",
        "assunto": "Direito Penal Militar / Crimes Contra a Autoridade Militar (Desacato a Superior - Art. 298 CPM)",
        "dificuldade": "FACIL",
        "textoBase": None,
        "enunciado": 'Durante uma inspeção no quartel, o Sargento Torres repreendeu verbalmente o Soldado Lima por atrasos constantes. Incomodado com a reprimenda, o Soldado respondeu em voz alta: "Você só sabe falar, mas não faz nada de útil por aqui!", provocando risos entre os presentes. Qual crime foi cometido pelo Soldado Lima?',
        "gabaritoOficial": "A",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "Desacato."},
            {"letra": "B", "texto": "Insultos à honra."},
            {"letra": "C", "texto": "Difamação."},
            {"letra": "D", "texto": "Insubordinação."},
            {"letra": "E", "texto": "Desobediência."}
        ]
    },
    {
        "posicao": 78,
        "disciplina": "Direito",
        "areaConhecimento": "Direito",
        "assunto": "Direito Constitucional Estadual / Justiça Militar Estadual (Competência Art. 125 CF/88)",
        "dificuldade": "FACIL",
        "textoBase": None,
        "enunciado": "Durante uma operação para reprimir crimes em uma área de fronteira estadual, um policial militar foi acusado de cometer uma infração no exercício de suas funções. Considerando as competências previstas na Constituição do Estado da Bahia, qual é a principal função da Justiça Militar estadual nesse contexto?",
        "gabaritoOficial": "E",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "Julgar crimes comuns cometidos por militares estaduais."},
            {"letra": "B", "texto": "Resolver conflitos administrativos internos das corporações militares."},
            {"letra": "C", "texto": "Coordenar ações de segurança pública."},
            {"letra": "D", "texto": "Proteger a soberania nacional."},
            {"letra": "E", "texto": "Processar e julgar os policiais militares e bombeiros militares nos crimes militares definidos em Lei."}
        ]
    },
    {
        "posicao": 79,
        "disciplina": "Direito",
        "areaConhecimento": "Direito",
        "assunto": "Direito Processual Penal Militar / Prisão em Flagrante Delito (Dever Legal de Agir)",
        "dificuldade": "FACIL",
        "textoBase": None,
        "enunciado": "O Tenente André flagrou um Soldado agredindo fisicamente outro militar durante o serviço. Nesse caso, qual medida deve ser adotada imediatamente?",
        "gabaritoOficial": "A",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "Efetuar a prisão em flagrante do agressor."},
            {"letra": "B", "texto": "Repreender o agressor verbalmente."},
            {"letra": "C", "texto": "Registrar o fato apenas para fins administrativos."},
            {"letra": "D", "texto": "Determinar o preenchimento de um relatório de ocorrência."},
            {"letra": "E", "texto": "Notificar o superior hierárquico e aguardar ordens."}
        ]
    },
    {
        "posicao": 80,
        "disciplina": "Direito",
        "areaConhecimento": "Direito",
        "assunto": "Direitos Humanos / Declaração Universal dos Direitos Humanos (Limites aos Direitos Fundamentais)",
        "dificuldade": "FACIL",
        "textoBase": None,
        "enunciado": "Durante um treinamento sobre ética e direitos humanos, o Tenente Gustavo explicou que a liberdade de expressão é um direito fundamental. No entanto, ele reforçou que esse direito não é absoluto. De acordo com a Declaração Universal dos Direitos Humanos, qual das situações abaixo pode justificar a limitação desse direito?",
        "gabaritoOficial": "D",
        "anulada": False,
        "alternativas": [
            {"letra": "A", "texto": "A realização de um discurso contrário a políticas públicas vigentes."},
            {"letra": "B", "texto": "A divulgação de notícias contrárias ao interesse do governo."},
            {"letra": "C", "texto": "A expressão de opiniões contrárias a um grupo majoritário."},
            {"letra": "D", "texto": "A publicação de materiais que incitem ódio racial e violência."},
            {"letra": "E", "texto": "A crítica ao governo local durante uma manifestação pública."}
        ]
    }
]

# Montagem do Formato 1: Questões Estruturadas (Modelo Interno Trajetória / Compliance)
questoes_formatadas = []
# Montagem do Formato 2: Payload Direto para a API de Ingestão do Backend (POST /api/admin/ingestao/questoes)
payloads_api = []

for q in questoes_raw:
    pos_str = f"{q['posicao']:02d}"
    id_origem = f"PMBA_CFOPM_2025_Q{pos_str}"
    
    # Formato 1 - Estrutura Rica / Compliance
    item_completo = {
        "idOrigem": id_origem,
        "atribuicao": {
            "banca": banca,
            "orgao": orgao,
            "cargo": cargo,
            "ano": ano,
            "fonte": fonte
        },
        "conteudo": {
            "posicao": q["posicao"],
            "tipoQuestao": "MULTIPLA_ESCOLHA",
            "textoBase": q["textoBase"],
            "enunciado": q["enunciado"],
            "imagemUrl": None,
            "gabaritoOficial": q["gabaritoOficial"],
            "anulada": q["anulada"],
            "alternativas": [
                {
                    "letra": alt["letra"],
                    "texto": alt["texto"],
                    "correta": (alt["letra"] == q["gabaritoOficial"])
                }
                for alt in q["alternativas"]
            ]
        },
        "classificacao": {
            "disciplina": q["disciplina"],
            "areaConhecimento": q["areaConhecimento"],
            "assunto": q["assunto"],
            "dificuldade": q["dificuldade"]
        },
        "comentarios": {
            "explicacaoIa": None,
            "permiteComentarioTerceiros": False
        }
    }
    questoes_formatadas.append(item_completo)

    # Formato 2 - DTO do BackendIngestionPayload
    dto_backend = {
        "idOrigem": id_origem,
        "fonte": fonte,
        "banca": banca,
        "orgao": orgao,
        "cargo": cargo,
        "ano": ano,
        "materiaNome": q["disciplina"],
        "areaConhecimento": q["areaConhecimento"],
        "assunto": q["assunto"],
        "dificuldade": q["dificuldade"],
        "tipoQuestao": "MULTIPLA_ESCOLHA",
        "gabaritoOficial": q["gabaritoOficial"],
        "anulada": q["anulada"],
        "posicao": q["posicao"],
        "textoBase": q["textoBase"],
        "enunciado": q["enunciado"],
        "imagemUrl": None,
        "statusRevisao": "APROVADO_AUTO",
        "alternativas": [
            {
                "letra": alt["letra"],
                "texto": alt["texto"],
                "correta": (alt["letra"] == q["gabaritoOficial"])
            }
            for alt in q["alternativas"]
        ]
    }
    payloads_api.append(dto_backend)

output_dir = r"C:\Users\luisd\.gemini\antigravity\scratch\Parsertrajetoria\output"
os.makedirs(output_dir, exist_ok=True)

file1 = os.path.join(output_dir, "pmba_cfo_2025_questoes.json")
with open(file1, "w", encoding="utf-8") as f:
    json.dump(questoes_formatadas, f, ensure_ascii=False, indent=2)

file2 = os.path.join(output_dir, "pmba_cfo_2025_payload_api.json")
with open(file2, "w", encoding="utf-8") as f:
    json.dump(payloads_api, f, ensure_ascii=False, indent=2)

print(f"Sucesso! {len(questoes_formatadas)} questoes geradas.")
print(f"Arquivo 1 (Estrutura Completa de Conformidade): {file1}")
print(f"Arquivo 2 (Payload Ingestao Backend API): {file2}")
