import json
import os

banca = "IBFC"
orgao = "Polícia Militar da Bahia - PMBA"
cargo = "Aluno Soldado da PM - Caderno 01"
ano = 2019
fonte = "CONCURSO"

texto_verissimo = """Segurança
Luis Fernando Veríssimo
O ponto de venda mais forte do condomínio era a sua segurança. Havia as mais belas casas, os jardins, os playgrounds, as piscinas, mas havia, acima de tudo, segurança. Toda a área era cercada por um muro alto. Havia um portão principal com muitos guardas que controlavam tudo por um circuito fechado de TV. Só entravam no condomínio os proprietários e visitantes devidamente identificados e crachados. Mas os assaltos começaram assim mesmo. Os ladrões pulavam os muros. Os condôminos decidiram colocar torres com guardas ao longo do muro alto. Nos quatro lados. [...] Agora não só os visitantes eram obrigados a usar crachá. Os proprietários e seus familiares também. Não passava ninguém pelo portão sem se identificar para a guarda. Nem as babás. Nem os bebês. Mas os assaltos continuaram. Decidiram eletrificar os muros. Houve protestos, mas no fim todos concordaram. O mais importante era a segurança. Quem tocasse no fio de alta tensão em cima do muro morreria eletrocutado. Se não morresse, atrairia para o local um batalhão de guardas com ordens de atirar para matar. Mas os assaltos continuaram.
Grades nas janelas de todas as casas. Era o jeito. Mesmo se os ladrões ultrapassassem os altos muros, [...] não conseguiriam entrar nas casas. Todas as janelas foram engradadas. Mas os assaltos continuaram. Foi feito um apelo para que as pessoas saíssem de casa o mínimo possível. Dois assaltantes tinham entrado no condomínio no banco de trás do carro de um proprietário, com um revólver apontado para a sua nuca. Assaltaram a casa, depois saíram no carro roubado, com crachás roubados. [...]
Foi reforçada a guarda. Construíram uma terceira cerca. As famílias de mais posses, com mais coisas para serem roubadas, mudaram-se para uma chamada área de segurança máxima. E foi tomada uma medida extrema. Ninguém pode entrar no condomínio. Ninguém. Visitas, só num local predeterminado pela guarda, sob sua severa vigilância e por curtos períodos. E ninguém pode sair. Agora, a segurança é completa. Não tem havido mais assaltos. Ninguém precisa temer pelo seu patrimônio. Os ladrões que passam pela calçada só conseguem espiar através do grande portão de ferro e talvez avistar um ou outro condômino agarrado às grades da sua casa, olhando melancolicamente para a rua. [...]"""

questoes = [
    # Língua Portuguesa (Q01 a Q10)
    {
        "pos": 1, "materia": "Língua Portuguesa", "dif": "FACIL", "base": texto_verissimo,
        "enunc": "De acordo com o texto, assinale a alternativa correta.",
        "gab": "*", # Anulada
        "alts": [
            ("A", "O texto discorre sobre um condomínio que ainda sofre uma série de assaltos por não haver um trabalho eficiente na segurança."),
            ("B", "Dois assaltantes entraram no condomínio no banco de trás do carro de um proprietário e remitiram seus bens."),
            ("C", "Infere-se do texto que há uma relevante crítica às prestações de serviço de segurança oferecidas em condomínios."),
            ("D", "No portão mais ínfero, existiam muitos guardas que controlavam tudo por um circuito fechado de TV."),
            ("E", "Os assaltos continuaram no condomínio porque a segurança apresentou um serviço falho e exímio.")
        ]
    },
    {
        "pos": 2, "materia": "Língua Portuguesa", "dif": "FACIL", "base": texto_verissimo,
        "enunc": "A tipologia textual se relaciona com a estrutura e aspectos linguísticos de como um texto se apresenta; já os gêneros textuais são formações advindas de contextos culturais e históricos e possuem função social específica. Quanto ao gênero do texto “Segurança”, assinale a alternativa correta.",
        "gab": "B",
        "alts": [("A", "Narração."), ("B", "Crônica."), ("C", "Anedota."), ("D", "Relato."), ("E", "Fábula.")]
    },
    {
        "pos": 3, "materia": "Língua Portuguesa", "dif": "FACIL", "base": texto_verissimo,
        "enunc": "Analise as afirmativas abaixo e assinale a alternativa correta.\nI. O vocábulo “condomínio” recebe acento agudo porque é uma oxítona terminada em ditongo.\nII. Já o vocábulo “condômino” recebe acento circunflexo porque todas as proparoxítonas devem receber este acento.\nIII. O vocábulo “possível” recebe acento agudo porque é uma paroxítona terminada em “l”.",
        "gab": "A",
        "alts": [
            ("A", "Apenas a afirmativa III está correta."),
            ("B", "Apenas as afirmativas I e III estão corretas."),
            ("C", "Apenas a afirmativa I está correta."),
            ("D", "Apenas as afirmativas II e III estão corretas."),
            ("E", "Apenas a afirmativa II está correta.")
        ]
    },
    {
        "pos": 4, "materia": "Língua Portuguesa", "dif": "MEDIO", "base": texto_verissimo,
        "enunc": "A vírgula exerce inúmeras funções na comunicação escrita. Analise as justificativas para o seu uso, nas alternativas abaixo, e assinale a incorreta.",
        "gab": "E",
        "alts": [
            ("A", "“Havia as mais belas casas, os jardins, os playgrounds, as piscinas,” [...] É obrigatório o uso da vírgula para separar termos com funções semelhantes."),
            ("B", "“Agora, a segurança é completa”. É facultativo o uso da vírgula para separar adjuntos adverbiais, de pouca extensão, antepostos."),
            ("C", "“Houve protestos, mas no fim todos concordaram”. É obrigatório o uso da vírgula para separar orações coordenadas sindéticas adversativas."),
            ("D", "“Mesmo se os ladrões ultrapassassem os altos muros, não conseguiriam entrar nas casas”. É recomendável o uso da vírgula para separar orações subordinadas adverbiais condicionais quando vierem antes da principal."),
            ("E", "“Se não morresse, atrairia para o local um batalhão de guardas”. É obrigatório o uso da vírgula para separar verbos com tempos e modos diferentes.")
        ]
    },
    {
        "pos": 5, "materia": "Língua Portuguesa", "dif": "FACIL", "base": texto_verissimo,
        "enunc": "Observe o enunciado extraído do texto: “Nem as babás. Nem os bebês”. Assinale a alternativa que apresenta a correta classificação da conjunção em destaque.",
        "gab": "D",
        "alts": [("A", "coordenativa negativa."), ("B", "coordenativa explicativa."), ("C", "coordenativa conclusiva."), ("D", "coordenativa aditiva."), ("E", "coordenativa causal.")]
    },
    {
        "pos": 6, "materia": "Língua Portuguesa", "dif": "FACIL", "base": texto_verissimo,
        "enunc": "O vocábulo “mas” aparece repetidas vezes no texto. Assinale a alternativa que apresenta corretamente sua relação estabelecida dentro do corpo textual.",
        "gab": "C",
        "alts": [("A", "consequência."), ("B", "causa."), ("C", "adversidade."), ("D", "explicação."), ("E", "adição.")]
    },
    {
        "pos": 7, "materia": "Língua Portuguesa", "dif": "MEDIO", "base": texto_verissimo,
        "enunc": "Analise as afirmativas abaixo e dê valores Verdadeiro (V) ou Falso (F).\n( ) O texto possui narrador onisciente em 1ª pessoa.\n( ) “Toda a área era cercada por um muro alto.” O enunciado anterior está escrito na voz passiva.\n( ) O título do texto sugere proteção e isto é refutado ao longo da obra.\nAssinale a alternativa que apresenta a sequência correta de cima para baixo.",
        "gab": "E",
        "alts": [("A", "F, F, V."), ("B", "V, F, F."), ("C", "F, V, F."), ("D", "V, V, F."), ("E", "F, V, V.")]
    },
    {
        "pos": 8, "materia": "Língua Portuguesa", "dif": "FACIL", "base": None,
        "enunc": "Quanto às normas para o uso do acento grave, assinale a alternativa correta.",
        "gab": "C",
        "alts": [
            ("A", "Os médicos atenderão nas salas de 1 à 5."),
            ("B", "Desde às duas horas estou no ponto."),
            ("C", "Eu assisti à cerimônia do casamento de minha sobrinha."),
            ("D", "As encomendas já foram repassadas à todas as escolas."),
            ("E", "A moça vai à pé todos os dias para o trabalho.")
        ]
    },
    {
        "pos": 9, "materia": "Língua Portuguesa", "dif": "FACIL", "base": None,
        "enunc": "Assinale a alternativa que apresenta uma palavra grafada de forma incorreta.",
        "gab": "D",
        "alts": [
            ("A", "A mesa de pingue-pongue está desmontada."),
            ("B", "Há de ser um super-homem para dar conta de tudo isto."),
            ("C", "O exército nacional decidiu contra-atacar."),
            ("D", "É preciso ser muito cara-de-pau para fingir tão bem."),
            ("E", "Não havia mais lugares no micro-ônibus.")
        ]
    },
    {
        "pos": 10, "materia": "Língua Portuguesa", "dif": "FACIL", "base": None,
        "enunc": "A fala do personagem da esquerda diz respeito ao sinal de _____ que foi abolido com o novo acordo ortográfico, assim como também o _____ das palavras destacadas na fala do personagem da direita.",
        "gab": "B",
        "alts": [
            ("A", "dois pontos / travessão."),
            ("B", "trema / hífen."),
            ("C", "reticências / traço."),
            ("D", "dois pontos / hífen."),
            ("E", "reticências / travessão.")
        ]
    },

    # Raciocínio Lógico (Q11 a Q18)
    {
        "pos": 11, "materia": "Raciocínio Lógico", "dif": "FACIL", "base": None,
        "enunc": "Observe a disjunção: “Marcelo não gosta de futebol ou Bruno não gosta de natação”, assinale a alternativa correta que apresenta a negação dessa disjunção.",
        "gab": "D",
        "alts": [
            ("A", "Marcelo gosta de futebol e Bruno não gosta de natação"),
            ("B", "Marcelo gosta de futebol se e somente se Bruno gosta de natação"),
            ("C", "Ou Marcelo gosta de futebol ou Bruno gosta de natação"),
            ("D", "Marcelo gosta de futebol e Bruno gosta de natação"),
            ("E", "Marcelo não gosta de futebol e Bruno não gosta de natação")
        ]
    },
    {
        "pos": 12, "materia": "Raciocínio Lógico", "dif": "MEDIO", "base": None,
        "enunc": "Em uma prateleira de uma biblioteca, deseja-se dispor 4 livros de maneiras distintas. Sabendo que a prateleira possui 10 espaços em que os livros podem ser colocados, assinale a alternativa que apresenta corretamente a quantidade de maneiras que esses livros podem ser dispostos nessa prateleira.",
        "gab": "B",
        "alts": [("A", "3628800"), ("B", "5040"), ("C", "151200"), ("D", "720"), ("E", "24")]
    },
    {
        "pos": 13, "materia": "Raciocínio Lógico", "dif": "MEDIO", "base": None,
        "enunc": "Uma loja de eletroeletrônicos decide realizar o sorteio de dois brindes para os clientes que comprarem um televisor. No total, 200 clientes realizaram a compra de televisor e concorreram aos brindes, sendo 120 mulheres e 80 homens. Considerando que ao ganhar um brinde não se pode concorrer a outro brinde, assinale a alternativa que apresenta corretamente a probabilidade de que os ganhadores sejam um homem e uma mulher.",
        "gab": "*", # Anulada
        "alts": [("A", "50/199"), ("B", "1/4"), ("C", "9/40"), ("D", "48/199"), ("E", "6/25")]
    },
    {
        "pos": 14, "materia": "Raciocínio Lógico", "dif": "FACIL", "base": None,
        "enunc": "Considere a proposição: “Todo pesquisador é estudioso.” Assinale a alternativa que não apresenta uma negação da proposição anterior.",
        "gab": "E",
        "alts": [
            ("A", "Existe algum pesquisador que não é estudioso"),
            ("B", "Algum pesquisador não é estudioso"),
            ("C", "Pelo menos um pesquisador não é estudioso"),
            ("D", "Existe pesquisador que não é estudioso"),
            ("E", "Nenhum pesquisador é estudioso")
        ]
    },
    {
        "pos": 15, "materia": "Raciocínio Lógico", "dif": "MEDIO", "base": None,
        "enunc": "Analise a proposição composta a seguir: “Maria viaja para o Rio de Janeiro se e somente se Fernando viaja para São Paulo”. Assinale a alternativa que apresenta a negação dessa proposição composta.",
        "gab": "*", # Anulada
        "alts": [
            ("A", "Maria não viaja para o Rio de Janeiro ou Fernando não viaja para São Paulo"),
            ("B", "Maria não viaja para o Rio de Janeiro e Fernando não viaja para São Paulo"),
            ("C", "Ou Maria viaja para o Rio de Janeiro ou Fernando viaja para São Paulo"),
            ("D", "Ou Maria não viaja para o Rio de Janeiro ou Fernando não viaja para São Paulo"),
            ("E", "Maria não viaja para o Rio de Janeiro ou Fernando viaja para São Paulo")
        ]
    },
    {
        "pos": 16, "materia": "Raciocínio Lógico", "dif": "MEDIO", "base": None,
        "enunc": "Observe as duas proposições P e Q apresentadas a seguir:\nP: Ana é engenheira.\nQ: Bianca é arquiteta.\nConsidere que Ana é engenheira somente se Bianca é arquiteta e, assinale a alternativa correta.",
        "gab": "B",
        "alts": [
            ("A", "Ana ser engenheira não implica Bianca ser arquiteta"),
            ("B", "Ana ser engenheira é condição suficiente para Bianca ser arquiteta"),
            ("C", "Uma condição necessária para Bianca ser arquiteta é Ana ser engenheira"),
            ("D", "Ana é engenheira se e somente se Bianca não é arquiteta"),
            ("E", "Uma condição necessária para Bianca ser arquiteta é Ana não ser engenheira")
        ]
    },
    {
        "pos": 17, "materia": "Raciocínio Lógico", "dif": "FACIL", "base": None,
        "enunc": "Conjunções são proposições compostas em que há a presença do conectivo “e” e podem ser representadas pelo símbolo “∧”. Sendo assim, assinale a alternativa correta.",
        "gab": "B",
        "alts": [
            ("A", "Se P é verdadeira e Q é verdadeira, então P ∧ Q é falsa"),
            ("B", "Se P é verdadeira e Q é falsa, então P ∧ Q é falsa"),
            ("C", "Se P é falsa e Q é falsa, então P ∧ Q é verdadeira"),
            ("D", "Se P é falsa e Q é verdadeira, então P ∧ Q é verdadeira"),
            ("E", "P ∧ Q só será verdadeira se P e Q forem falsas")
        ]
    },
    {
        "pos": 18, "materia": "Raciocínio Lógico", "dif": "MEDIO", "base": None,
        "enunc": "Considere que os símbolos →, ↔, ∧ e ∨ representam os operadores lógicos “se...então”, “se e somente se”, “e” e “ou”, respectivamente. Analise as sentenças abaixo e dê valores Verdadeiro (V) ou Falso (F).\n( ) (7 − 2 = 5) ∨ (3 > 2)\n( ) (3 + 2 = 4) ↔ (1 > 3)\n( ) (3 × 5 + 6 = 21) ∧ (18 − 3 − 1 = 7)\n( ) (4 × 4 + 3 = 19) → (9 − 2 = 7)\nAssinale a alternativa que apresenta a sequência correta de cima para baixo.",
        "gab": "A",
        "alts": [("A", "V, V, F, V"), ("B", "F, V, F, V"), ("C", "V, V, V, F"), ("D", "V, F, F, V"), ("E", "V, V, F, F")]
    },

    # História do Brasil (Q19 a Q26)
    {
        "pos": 19, "materia": "História do Brasil", "dif": "MEDIO", "base": None,
        "enunc": "A chegada dos Europeus à América, no século XV, significou o início da destruição da maioria das organizações sociais, culturais e políticas existentes. Os chamados conquistadores confiscaram as terras indígenas, sua liberdade e, muito frequentemente, suas vidas. Mais da metade dos cerca de 80 milhões de ameríndios que então se distribuíam por todo o continente acabaram mortos em pouco menos de um século de colonização (VICENTINO; DORIGO, 1997). A respeito da chegada dos portugueses ao Brasil, assinale a alternativa incorreta.",
        "gab": "D",
        "alts": [
            ("A", "Além da submissão à exploração colonial, dos sucessivos confrontos armados e da expulsão de suas terras, os indígenas também foram destruídos pelas doenças trazidas pelos conquistadores"),
            ("B", "Os conquistadores europeus, portadores de uma tecnologia superior e dotados da ambição comercial, impuseram um verdadeiro morticínio às populações nativas"),
            ("C", "O processo de massacre aos indígenas teve início no período colonial, manteve-se pela fase imperial e continuou pelo período republicano, não sendo raro na atualidade"),
            ("D", "Os primeiros séculos de contato entre brancos e índios revestiram-se de alguma amabilidade, pois, os interesses dos colonizadores com o passar do tempo mudaram radicalmente em relação ao dos indígenas"),
            ("E", "No início, os índios do Brasil foram atraídos pelo escambo, isto é, troca de produtos nativos por outra mercadoria")
        ]
    },
    {
        "pos": 20, "materia": "História do Brasil", "dif": "MEDIO", "base": None,
        "enunc": "No período de 1968 a 1974, o Brasil viveu um acelerado crescimento econômico, nomeado pelos militares de Milagre Econômico. Esse crescimento, ocorrido no governo do presidente Emílio Médici, foi garantido, entre outros fatores, pelos volumosos investimentos estrangeiros no setor industrial, sobretudo, na indústria de bens de consumo duráveis (CERRI, 2002).\nA respeito do Milagre Econômico e com base na tabela de distribuição de renda no Brasil (1960-1976), assinale a alternativa correta.",
        "gab": "D",
        "alts": [
            ("A", "Assegurou toda a distribuição da riqueza produzida entre os brasileiros"),
            ("B", "Possibilitou a diminuição das diferenças econômicas entre as classes sociais"),
            ("C", "Permitiu a redução da pobreza e elevou a qualidade de vida de modo igualitário"),
            ("D", "Concentrou a renda e acentuou as desigualdades sociais"),
            ("E", "Ampliou a capacidade produtiva e consumista do país, que se tornou modelo na América Latina de igualdade e prosperidade")
        ]
    },
    {
        "pos": 21, "materia": "História do Brasil", "dif": "MEDIO", "base": None,
        "enunc": "A maior parte dos engenhos aninhava-se na mata, não muito distante dos centros portuários, o que se explica pela maior fertilidade dos terrenos e pela abundância de lenha, necessárias às fornalhas famintas, alimentadas por um trabalho, que às vezes ocupava o dia e a noite, de oito a nove meses, normalmente de julho/agosto de um ano a abril/maio do ano seguinte (DEL PRIORI; VENANCIO, 2010).\nA respeito dos engenhos de açúcar, leia as afirmativas abaixo e dê valores Verdadeiro (V) ou Falso (F).\n( ) As primeiras mudas de canas de açúcar foram trazidas da ilha da Madeira para o Brasil por Martim Afonso de Souza que instalou o primeiro engenho da colônia em São Vicente.\n( ) A multiplicação dos engenhos pela costa brasileira foi bastante rápida, chegando a mais de 60 em 1570 e 200 no final do século XVI.\n( ) Coube a região Nordeste, destacadamente o litoral de Pernambuco e Bahia, o papel de principal produtora de açúcar da colônia.\n( ) O engenho, que em alguns casos chegava a ter perto de 5.000 moradores, era constituído por área extensas de florestas, fornecedoras de madeira; plantações de cana; a residência do proprietário conhecida como casa grande, a capela e a senzala.\nAssinale a alternativa que apresenta a sequência correta de cima para baixo.",
        "gab": "E",
        "alts": [("A", "V, F, V, F"), ("B", "F, F, F, F"), ("C", "F, F, V, V"), ("D", "V, V, F, F"), ("E", "V, V, V, V")]
    },
    {
        "pos": 22, "materia": "História do Brasil", "dif": "MEDIO", "base": None,
        "enunc": "A descoberta do ouro em Minas Gerais pelos bandeirantes paulistas, em finais do século XVII, atraiu para a região milhares de colonos de outras províncias, além de um grande número de europeus. Julgando-se com direito exclusivo de exploração das minas, os paulistas hostilizaram os forasteiros, que apelidaram de emboabas (em tupi, amô-abá significa “estrangeiro”) (GIANPAOLO, 1997). A respeito da Guerra dos Emboabas, assinale a alternativa correta.",
        "gab": "A",
        "alts": [
            ("A", "Os emboabas enfrentaram os paulistas em vários combates, entre eles, o mais marcante ocorreu no chamado Capão da traição, no qual 300 paulistas foram cercados pelos emboabas"),
            ("B", "O confronto teve como motivo principal a disputa pela exploração do café produzido em grande escala na região de Minas Gerais"),
            ("C", "Os paulistas desejavam ter exclusividade nas terras de Minas, pois diziam que tinham descoberto essa região e pretendiam explorá-la para a plantação de açúcar"),
            ("D", "Em 1750 o governo português interveio e, a fim de pacificar e melhor administrar a região, juntou a capitania de São Paulo e Minas Gerais com a capitania do Rio de Janeiro"),
            ("E", "Após vários conflitos os bandeirantes paulistas partiram em busca de novas explorações na região do Nordeste sob a liderança de Manuel Nunes Viana")
        ]
    },
    {
        "pos": 23, "materia": "História do Brasil", "dif": "MEDIO", "base": None,
        "enunc": "O quadro em destaque na imagem de Rugendas (1835) representa uma cena do que conhecemos historicamente como “As Negras do Tabuleiro”. A respeito deste período, leia as afirmativas abaixo.\nI. A mineração era um trabalho pesado, feito principalmente por homens.\nII. As negras retratadas por Rugendas na figura acima eram, provavelmente, vendedoras ambulantes, que ofereciam comida e bebida aos que trabalhavam na extração do ouro.\nIII. Geralmente essas mulheres eram livres, mas trabalhavam por conta dos mineradores, vigiando os trabalhadores na extração do ouro.\nIV. Elas transitavam pelas vilas, roças e arraiais, vendendo suas mercadorias para pessoas de todas as condições sociais.\nAssinale a alternativa correta.",
        "gab": "B",
        "alts": [
            ("A", "As afirmativas I, II, III e IV estão corretas"),
            ("B", "Apenas as afirmativas I, II e IV estão corretas"),
            ("C", "Apenas as afirmativas III e IV estão corretas"),
            ("D", "Todas as afirmativas estão incorretas"),
            ("E", "Apenas a afirmativa III está correta")
        ]
    },
    {
        "pos": 24, "materia": "História do Brasil", "dif": "MEDIO", "base": None,
        "enunc": "Ao contrário de Euclides que, antes de rumar para Canudos, permaneceu o mês de agosto praticamente inteiro em Salvador, Manuel Benício parece ter sido enviado diretamente para o campo da batalha. A respeito da Guerra de Canudos, assinale a alternativa correta.",
        "gab": "E",
        "alts": [
            ("A", "Esse movimento refletia a extrema fartura em que viviam as populações do Sertão Nordestino"),
            ("B", "A tensão política foi agravada pela expulsão dos ruralistas que atuavam nas revoltas catarinenses e paranaenses"),
            ("C", "A região onde foi estabelecido o vilarejo de Canudos, no interior de Pernambuco, era marcada por latifúndios improdutivos, pelas secas cíclicas e pelo desemprego"),
            ("D", "Os revoltosos incendiaram Canudos e mataram grande parte do exército, fazendo-os de prisioneiros"),
            ("E", "Foi um movimento de resistência da população sertaneja contra a estrutura agrário-latifundiária e as medidas repressivas oficiais")
        ]
    },
    {
        "pos": 25, "materia": "História do Brasil", "dif": "FACIL", "base": None,
        "enunc": "A respeito da Conjuração Baiana de 1798 em Salvador, assinale a alternativa incorreta.",
        "gab": "C",
        "alts": [
            ("A", "Condenados por conspirarem contra a Coroa de Portugal, dois alfaiates e dois soldados foram considerados os réus do movimento qualificado pelas autoridades do Tribunal da Relação da Bahia, em 1799, de “Sedição dos Mulatos”"),
            ("B", "Parte dos historiadores que versaram sobre a Conjuração Baiana de 1798, perceberam certo grau de coerência entre a tentativa de participação política dos setores populares e a ideia de república"),
            ("C", "Conjuração Baiana foi uma revolta social de caráter burguês, que ocorreu na Bahia em 1798. Recebeu uma importante influência dos ideais do Renascimento Cultural e Revolução Industrial"),
            ("D", "A Conjuração Baiana de 1798 deixa de ser um evento de identificação regional, para tornar-se o representante das mais profundas aspirações de amplos setores da sociedade brasileira"),
            ("E", "Esse movimento defendia a emancipação política do Brasil, ou seja, o fim do pacto colonial com Portugal e a instauração e implantação da República")
        ]
    },
    {
        "pos": 26, "materia": "História do Brasil", "dif": "MEDIO", "base": None,
        "enunc": "A República Velha também foi nomeada “República das Oligarquias”, porque era comandada pela aristocracia dos fazendeiros. A respeito deste período da história brasileira, assinale a alternativa incorreta.",
        "gab": "A",
        "alts": [
            ("A", "Não havia, da parte das elites, qualquer pretensão de impedir ou retroceder as mudanças ao regime vigente. Era de comum acordo qualquer projeto político substantivamente republicano, isto é, que se alicerçasse numa concepção igualitária, legalista e cívica da Nação"),
            ("B", "O conceito de República era, pois, bastante débil. Ele quase não tinha conteúdo próprio, sendo compreendido essencialmente por oposição à monarquia unitária"),
            ("C", "O exercício do poder político da Primeira República foi marcado pelo autoritarismo que sucessivamente lhe imprimiram as forças que a instauraram"),
            ("D", "O discurso reformista liberal da década de 1870 acabou servindo de fachada, na verdade, para uma reação aristocrática que, esvaziando o poder da Coroa e excluindo as camadas pobres do direito de voto, pretendia instalar um parlamentarismo aristocrático onde apenas as elites estivessem no controle do Estado"),
            ("E", "Na busca de outras fórmulas que eliminassem a autonomia do poder monárquico e, com ela, a possibilidade de uma reforma social pelo alto, a aristocracia rural aderiu sucessivamente ao federalismo e ao republicanismo, especialmente depois da Lei Áurea")
        ]
    },

    # Geografia do Brasil (Q27 a Q34)
    {
        "pos": 27, "materia": "Geografia do Brasil", "dif": "FACIL", "base": None,
        "enunc": "“Bioma é um conjunto de vida vegetal e animal, constituído pelo agrupamento de tipos de vegetação que são próximos e que podem ser identificados em nível regional, com condições de geologia e clima semelhantes e que, historicamente, sofreram os mesmos processos de formação da paisagem, resultando em uma diversidade de flora e fauna própria” (IBGE, 2019). No que concerne aos biomas que estão presentes no estado da Bahia, assinale a alternativa correta.",
        "gab": "D",
        "alts": [
            ("A", "Amazônia, Cerrado e Mata Atlântica"),
            ("B", "Amazônia, Caatinga e Pampa"),
            ("C", "Amazônia, Mata Atlântica e Pampa"),
            ("D", "Cerrado, Caatinga e Mata Atlântica"),
            ("E", "Cerrado, Caatinga e Pampa")
        ]
    },
    {
        "pos": 28, "materia": "Geografia do Brasil", "dif": "MEDIO", "base": None,
        "enunc": "No que se refere aos aspectos físicos do estado da Bahia, analise as afirmativas abaixo e dê valores Verdadeiro (V) ou Falso (F).\n( ) O estado possui relevos com altitudes que podem variar de 0 a 630 metros, sendo que as maiores elevações estão localizadas no Recôncavo Baiano.\n( ) A Serra do Espinhaço, a Serra da Canastra, a Chapada Diamantina e a Chapada dos Veadeiros são exemplos de acidentes geográficos localizados no estado.\n( ) Grande parte do território do estado é banhado por cursos dágua pertencentes à bacia hidrográfica do rio São Francisco.\n( ) A capital do estado, Salvador, está localizada na bacia hidrográfica do rio Jequitinhonha, e Feira de Santana, na bacia do rio Paraná.\nAssinale a alternativa que apresenta a sequência correta de cima para baixo.",
        "gab": "C",
        "alts": [("A", "F, F, F, V"), ("B", "F, V, V, F"), ("C", "F, F, V, F"), ("D", "V, V, F, F"), ("E", "V, F, F, V")]
    },
    {
        "pos": 29, "materia": "Geografia do Brasil", "dif": "MEDIO", "base": None,
        "enunc": "Associe os climas da legenda do mapa com os diferentes tipos de climas da região Nordeste. Analise as afirmativas abaixo e dê valores Verdadeiro (V) ou Falso (F).\n( ) O clima 1 é o subtropical.\n( ) O clima 2 é o tropical.\n( ) O clima 3 é o semiárido.\n( ) O clima 4 é o equatorial.\nAssinale a alternativa que apresenta a sequência correta de cima para baixo.",
        "gab": "B",
        "alts": [("A", "V, F, F, F"), ("B", "F, V, F, F"), ("C", "F, F, V, F"), ("D", "V, F, F, V"), ("E", "V, V, V, V")]
    },
    {
        "pos": 30, "materia": "Geografia do Brasil", "dif": "FACIL", "base": None,
        "enunc": "“O homem chega, já desfaz a natureza / Tira gente, põe represa, diz que tudo vai mudar... / Vai ter barragem no salto do Sobradinho / E o povo vai-se embora com medo de se afogar. / O sertão vai virar mar...” (Sá, Rodrix e Guarabyra)\nA canção Sobradinho protesta contra a construção da Usina Hidrelétrica de Sobradinho no rio São Francisco, Bahia. Sobre os impactos negativos causados pela construção de grandes barragens, que afetam a sociedade e o meio ambiente, assinale a alternativa incorreta.",
        "gab": "E",
        "alts": [
            ("A", "Desapropriação de propriedades particulares e realocação da população ribeirinha"),
            ("B", "Desintegração dos costumes e tradições históricas da população atingida"),
            ("C", "Perda de terras agricultáveis devido à elevação do nível da água do rio"),
            ("D", "Alteração da dinâmica natural do rio e derrubada de florestas"),
            ("E", "Rebaixamento do lençol freático e poluição radioativa do rio")
        ]
    },
    {
        "pos": 31, "materia": "Geografia do Brasil", "dif": "MEDIO", "base": None,
        "enunc": "A respeito do vazamento de óleo que ocorreu no litoral nordestino e atingiu praias do estado da Bahia, no segundo semestre de 2019, analise as afirmativas abaixo.\nI. O óleo pode causar a morte de animais marinhos, como tartarugas e peixes.\nII. O óleo pode alterar a qualidade da água, deixando-a inclusive imprópria para o banho.\nIII. O óleo pode ocasionar a formação de processos erosivos em áreas de mangue, como ravinas e voçorocas.\nIV. O óleo pode reduzir as emissões de dióxido de carbono na atmosfera, contribuindo assim com o aquecimento global.\nAssinale a alternativa correta.",
        "gab": "A",
        "alts": [
            ("A", "Apenas as afirmativas I e II estão corretas"),
            ("B", "Apenas as afirmativas I e III estão corretas"),
            ("C", "Apenas as afirmativas II e IV estão corretas"),
            ("D", "Apenas as afirmativas I, III e IV estão corretas"),
            ("E", "As afirmativas I, II, III e IV estão corretas")
        ]
    },
    {
        "pos": 32, "materia": "Geografia do Brasil", "dif": "FACIL", "base": None,
        "enunc": "“São três vozes de uma gente / Que assim solta a garganta... / Olodum, te amo! Ilê, te amo! / O seu som e a sua cor / Didá, te amo! Neguinho, te amo!” (Daniela Mercury / Marcelo Quintanilha)\nA canção acima homenageia entidades carnavalescas que são patrimônio da cultura baiana. Assinale a alternativa correta que indica, respectivamente, um termo que é utilizado para nomear essas entidades e qual sua representatividade.",
        "gab": "A",
        "alts": [
            ("A", "Bloco Afro, símbolo da resistência e da valorização negra"),
            ("B", "Trio Elétrico, palco móvel utilizado pelos artistas"),
            ("C", "Escola de Samba, agremiação popular voltada ao samba"),
            ("D", "Samba de Roda, propagador da cultura do Recôncavo da Bahia"),
            ("E", "Filhos de Gandhy, que difundiu o frevo na Bahia")
        ]
    },
    {
        "pos": 33, "materia": "Geografia do Brasil", "dif": "FACIL", "base": None,
        "enunc": "Assinale a alternativa correta que apresenta a cor ou raça predominantemente autodeclarada pela população do estado da Bahia, de acordo o Censo Demográfico realizado em 2010 pelo Instituto Brasileiro de Geografia e Estatística (IBGE).",
        "gab": "B",
        "alts": [("A", "Amarela"), ("B", "Parda"), ("C", "Preta"), ("D", "Branca"), ("E", "Indígena")]
    },
    {
        "pos": 34, "materia": "Geografia do Brasil", "dif": "MEDIO", "base": None,
        "enunc": "Em relação aos aspectos econômicos e sociais do estado da Bahia, assinale a alternativa correta.",
        "gab": "E",
        "alts": [
            ("A", "O Produto Interno Bruto (PIB) per capita da Bahia está entre os três maiores do Brasil"),
            ("B", "O Produto Interno Bruto (PIB) per capita da Bahia é o menor entre os estados do Brasil"),
            ("C", "O Índice de Desenvolvimento Humano (IDH) da Bahia está entre os três maiores do Brasil"),
            ("D", "O Índice de Desenvolvimento Humano (IDH) da Bahia é o menor entre os estados do Brasil"),
            ("E", "A expectativa de vida do baiano está crescendo, porém ainda está abaixo da média do brasileiro")
        ]
    },

    # Atualidades (Q35 a Q42)
    {
        "pos": 35, "materia": "Atualidades", "dif": "FACIL", "base": None,
        "enunc": "“A globalização implica que a produção de empresas transnacionais é para o mercado mundial...”. Assinale a alternativa que indica uma característica incorreta do processo de globalização.",
        "gab": "E",
        "alts": [
            ("A", "Integração social e econômica"),
            ("B", "Surgimento de blocos econômicos"),
            ("C", "Ampliação dos recursos tecnológicos"),
            ("D", "A instantaneidade e velocidade das informações"),
            ("E", "Redução da concorrência e da competitividade de mercado")
        ]
    },
    {
        "pos": 36, "materia": "Atualidades", "dif": "FACIL", "base": None,
        "enunc": "“Num plebiscito em 23 de junho de 2016, os britânicos foram perguntados se o Reino Unido deveria permanecer ou deixar a União Europeia (UE)...”. Assinale a alternativa correta que apresenta o termo comumente utilizado quando se fala sobre a decisão do Reino Unido de deixar UE.",
        "gab": "C",
        "alts": [("A", "Ukexit"), ("B", "Outofue"), ("C", "Brexit"), ("D", "Brexid"), ("E", "British-leave")]
    },
    {
        "pos": 37, "materia": "Atualidades", "dif": "FACIL", "base": None,
        "enunc": "Assinale a alternativa que apresenta, de forma incorreta, uma atitude que pode auxiliar na redução de gases do efeito estufa.",
        "gab": "E",
        "alts": [
            ("A", "Produzir menos lixo"),
            ("B", "Utilizar o transporte público"),
            ("C", "Reduzir a queima de combustíveis fósseis"),
            ("D", "Reduzir o consumo de carne bovina"),
            ("E", "Evitar produtos fabricados de maneira sustentável")
        ]
    },
    {
        "pos": 38, "materia": "Atualidades", "dif": "FACIL", "base": None,
        "enunc": "“A Inteligência Artificial (IA) está transformando a maneira como fazemos negócios. A adoção de aprendizado de máquina, Big Data, Analytics e outras novas tecnologias em busca de automação não é mais estritamente uma questão de tecnologia de informação...”. Assinale a alternativa correta que apresenta uma vantagem da inteligência artificial.",
        "gab": "*", # Anulada
        "alts": [
            ("A", "Aumento substancial de erros na produção"),
            ("B", "Maior tempo de trabalho e de produção"),
            ("C", "Queda na eficiência e na produtividade"),
            ("D", "Dificuldade na tomada de decisão e na solução de problemas"),
            ("E", "Modernização das etapas de produção")
        ]
    },
    {
        "pos": 39, "materia": "Atualidades", "dif": "FACIL", "base": None,
        "enunc": "Instituições de pesquisa utilizaram tecnologia de sensoriamento remoto para explicar a origem e evolução de manchas de óleo que poluíram o litoral Nordeste do Brasil, no segundo semestre de 2019, a partir de imagens capturadas pelo Sentinel-1A. Assinale a alternativa que indica de maneira correta o tipo de imagem citada no texto acima.",
        "gab": "C",
        "alts": [("A", "Imagem de GPS"), ("B", "Imagem de teodolito"), ("C", "Imagem de satélite"), ("D", "Imagem de termômetro"), ("E", "Imagem de pluviômetro")]
    },
    {
        "pos": 40, "materia": "Atualidades", "dif": "FACIL", "base": None,
        "enunc": "“O Irã anunciou, nesta segunda (4/11/2019), mais uma medida que desrespeita o Acordo Nuclear Internacional [...]. A preocupação mundial é que o enriquecimento de urânio chegue a um nível que permita produção de _____” (G1, 2019). Assinale a alternativa que preencha corretamente a lacuna.",
        "gab": "B",
        "alts": [("A", "tanques de guerra"), ("B", "bombas atômicas"), ("C", "bombas de gás lacrimogênio"), ("D", "armas biológicas"), ("E", "armas de fogo")]
    },
    {
        "pos": 41, "materia": "Atualidades", "dif": "MEDIO", "base": None,
        "enunc": "“O Supremo Tribunal Federal (STF) determinou na quinta-feira, 13 de junho de 2019, que a discriminação por orientação sexual e identidade de gênero passe a ser considerada um crime, [...] por 8 votos a 3, os ministros determinaram que a conduta passe a ser punida pela _____” (BBC, 2019). Assinale a alternativa que preencha corretamente a lacuna.",
        "gab": "D",
        "alts": [
            ("A", "Lei dos Crimes Hediondos"),
            ("B", "Lei Maria da Penha"),
            ("C", "Lei de Execução Penal"),
            ("D", "Lei de Racismo (define os crimes resultantes de preconceito de raça ou de cor)"),
            ("E", "Lei Menino Bernardo")
        ]
    },
    {
        "pos": 42, "materia": "Atualidades", "dif": "FACIL", "base": None,
        "enunc": "Os relatos de _____ contra brasileiros em Portugal - maior comunidade estrangeira no país - tiveram aumento expressivo: 150% em 12 meses. A _____ contra brasileiros é a terceira principal causa de discriminação em Portugal (Folha de São Paulo, 2019). Assinale a alternativa com a palavra que preencha corretamente as duas lacunas.",
        "gab": "A",
        "alts": [("A", "xenofobia"), ("B", "acrofobia"), ("C", "claustrofobia"), ("D", "homofobia"), ("E", "monofobia")]
    },

    # Informática (Q43 a Q50)
    {
        "pos": 43, "materia": "Informática", "dif": "FACIL", "base": None,
        "enunc": "No MS Excel 2010, idioma português, configuração padrão, existe uma função que permite arredondar um número até uma quantidade especificada de dígitos. Assinale a alternativa correta que corresponda a esta função.",
        "gab": "A",
        "alts": [("A", "ARRED"), ("B", "ARREDMULTB.PRECISO"), ("C", "ARREDIG"), ("D", "ARRED.PRECISO"), ("E", "ARRUMAR")]
    },
    {
        "pos": 44, "materia": "Informática", "dif": "FACIL", "base": None,
        "enunc": "Alessandro precisa montar um relatório no MS Excel 2010, idioma português, configuração padrão, que some o intervalo de células de A1 até A5, somente os valores maiores do que vinte. Assinale a alternativa correta que representa a fórmula que Alessandro irá utilizar.",
        "gab": "E",
        "alts": [
            ("A", "=SOMASE(A1:A5;>20)"),
            ("B", "=SE(A1:A5>20;SOMA())"),
            ("C", "=SOMA(SE(A1:A5>20))"),
            ("D", "=SOMASE(A1^A5;\">20\")"),
            ("E", "=SOMASE(A1:A5;\">20\")")
        ]
    },
    {
        "pos": 45, "materia": "Informática", "dif": "FACIL", "base": None,
        "enunc": "Otavio entrou em contato com seu provedor de internet para resolver um problema de conexão com a internet em um computador que utiliza Windows 10, idioma português, configuração padrão. O atendente do suporte técnico solicitou a informação do endereço IP do computador na rede. Assinale a alternativa que apresenta corretamente como obter este endereço em linha de comando.",
        "gab": "B",
        "alts": [("A", "netsh -a"), ("B", "ipconfig"), ("C", "getip -a"), ("D", "ifconfig"), ("E", "ipaddress")]
    },
    {
        "pos": 46, "materia": "Informática", "dif": "FACIL", "base": None,
        "enunc": "Sobre as Ferramentas de Lixeira do sistema operacional Windows 10, idioma português, configuração padrão, assinale a alternativa incorreta.",
        "gab": "C",
        "alts": [
            ("A", "Esvaziar Lixeira"),
            ("B", "Propriedades da Lixeira"),
            ("C", "Compactar Lixeira"),
            ("D", "Restaurar todos os itens"),
            ("E", "Restaurar os itens selecionados")
        ]
    },
    {
        "pos": 47, "materia": "Informática", "dif": "FACIL", "base": None,
        "enunc": "No MS Excel 2010, idioma português, configuração padrão, existe a funcionalidade Congelar Painéis. Assinale a alternativa correta sobre o menu no qual encontra-se disponível esta funcionalidade.",
        "gab": "E",
        "alts": [("A", "Layout de Página"), ("B", "Fórmulas"), ("C", "Dados"), ("D", "Revisão"), ("E", "Exibição")]
    },
    {
        "pos": 48, "materia": "Informática", "dif": "FACIL", "base": None,
        "enunc": "Assinale a alternativa correta quanto ao conceito de intranet.",
        "gab": "E",
        "alts": [
            ("A", "rede de propaganda de uma empresa"),
            ("B", "sinônimo de internet"),
            ("C", "rede de telecom"),
            ("D", "rede pública"),
            ("E", "rede de uso interno de uma instituição")
        ]
    },
    {
        "pos": 49, "materia": "Informática", "dif": "FACIL", "base": None,
        "enunc": "Eduarda precisa enviar um e-mail com um comunicado geral a vários destinatários, de tal maneira que eles não conheçam uns aos outros. Assinale a alternativa que apresenta corretamente a forma do envio que Eduarda deve utilizar para o comunicado.",
        "gab": "A",
        "alts": [("A", "Cco"), ("B", "Coc"), ("C", "Ccc"), ("D", "Coo"), ("E", "Cc")]
    },
    {
        "pos": 50, "materia": "Informática", "dif": "FACIL", "base": None,
        "enunc": "Marcos deseja migrar seu backup de arquivos pessoais, que atualmente encontra-se em seu computador, para nuvem. Assinale a alternativa correta para exemplos de serviços de armazenamento de arquivos em nuvem.",
        "gab": "D",
        "alts": [
            ("A", "Dropbox e Google Chrome"),
            ("B", "Firefox e Mozilla"),
            ("C", "Google Arq e Team Viewer"),
            ("D", "Dropbox e Google Drive"),
            ("E", "Google Arq e Firefox")
        ]
    },

    # Direito Constitucional (Q51 a Q55)
    {
        "pos": 51, "materia": "Direito Constitucional", "dif": "MEDIO", "base": None,
        "enunc": "Quem deve respeitar os direitos e garantias fundamentais? Essa questão refere-se aos sujeitos passivos ou destinatários das obrigações de observância e proteção ativa que decorrem dos direitos e garantias, por mais abstratos e indefinidos que sejam. Sobre os destinatários dos direitos fundamentais, analise as afirmativas abaixo e dê valores Verdadeiro (V) ou Falso (F).\n( ) Os direitos fundamentais, em regra, destinam-se a proteção dos estrangeiros residentes no país e, também, dos de passagem pelo País.\n( ) Os direitos fundamentais destinam-se à proteção dos apátridas.\n( ) Os direitos fundamentais destinam-se à proteção das pessoas jurídicas, observadas suas particularidades.\n( ) O destinatário principal do dever de respeitar os direitos dos indivíduos é o Estado no sentido mais amplo do termo. Sendo, também, atualmente possível ter como destinatário um particular a partir do reconhecimento do efeito horizontal dos direitos fundamentais.\nAssinale a alternativa que apresenta a sequência correta de cima para baixo.",
        "gab": "A",
        "alts": [("A", "V, V, V, V"), ("B", "V, V, F, F"), ("C", "V, F, F, V"), ("D", "F, F, V, V"), ("E", "F, V, V, F")]
    },
    {
        "pos": 52, "materia": "Direito Constitucional", "dif": "FACIL", "base": None,
        "enunc": "Os direitos sociais, direitos de segunda dimensão, apresentam-se como prestações positivas a serem implementadas pelo Estado (Social de Direito) e tendem a concretizar a perspectiva de uma isonomia substancial e social na busca de melhores e adequadas condições de vida. Sobre a Ordem Social assinale a alternativa correta.",
        "gab": "B",
        "alts": [
            ("A", "A educação é direito de todos e dever exclusivo do Estado"),
            ("B", "O Estado protegerá as manifestações das culturas populares, indígenas e afro-brasileiras, e das de grupos participantes do processo civilizatório nacional"),
            ("C", "As ações e serviços públicos de saúde integram uma rede regionalizada e hierarquizada e constituem um sistema único, organizado de forma centralizada, com direção única em cada esfera de governo"),
            ("D", "É dever do Estado fomentar práticas desportivas formais e não formais, como direito de cada um, observado a destinação de recursos públicos para a promoção prioritária do desporto de alto rendimento"),
            ("E", "É livre a manifestação do pensamento, sendo inconstitucional a regulamentação de diversões e espetáculos públicos, mesmo que para a indicação de faixas etárias a que não se recomendem")
        ]
    },
    {
        "pos": 53, "materia": "Direito Constitucional", "dif": "FACIL", "base": None,
        "enunc": "A segurança pública, dever do Estado, direito e responsabilidade de todos, é exercida para a preservação da ordem pública e da incolumidade das pessoas e do patrimônio. Considerando sua estrutura, assinale a alternativa que não contém um de seus órgãos.",
        "gab": "A",
        "alts": [
            ("A", "Guardas Municipais"),
            ("B", "Polícia Federal"),
            ("C", "Polícia Rodoviária Federal"),
            ("D", "Polícias Civis"),
            ("E", "Polícias militares e corpos de bombeiros militares")
        ]
    },
    {
        "pos": 54, "materia": "Direito Constitucional", "dif": "FACIL", "base": None,
        "enunc": "A Polícia Federal, instituída por lei como órgão permanente, é organizada e mantida pela União e estruturada em carreira. Sobre suas atribuições, assinale a alternativa correta.",
        "gab": "C",
        "alts": [
            ("A", "Dirigida por delegados de polícia de carreira, incumbem, ressalvada a competência da União, as funções de polícia judiciária e a apuração de infrações penais, exceto as militares"),
            ("B", "Cabe a ela o exercício da polícia ostensiva e a preservação da ordem pública"),
            ("C", "Destina-se a apurar infrações penais contra a ordem política e social ou em detrimento de bens, serviços e interesses da União ou de suas entidades autárquicas e empresas públicas, assim como outras infrações cuja prática tenha repercussão interestadual ou internacional e exija repressão uniforme, segundo dispuser em lei"),
            ("D", "Exerce as funções de polícia marítima e execução de atividade da defesa civil"),
            ("E", "Destina-se ao patrulhamento ostensivo das ferrovias federais, bem como prevenir e reprimir o tráfico ilícito de entorpecentes e drogas afins, o contrabando e o descaminho")
        ]
    },
    {
        "pos": 55, "materia": "Direito Constitucional", "dif": "MEDIO", "base": None,
        "enunc": "Nos termos da Constituição do Estado da Bahia, analise as afirmativas abaixo quanto às atribuições do Governador de Estado.\nI. Compete privativamente ao Governador do Estado exercer, com auxílio dos Secretários de Estado, a direção superior da administração estadual.\nII. Compete privativamente ao Governador do Estado decretar e fazer executar a intervenção no Município, na forma da Constituição do Estadual.\nIII. Compete privativamente ao Governador do Estado decretar as situações de emergência e estado de calamidade pública.\nIV. Compete privativamente ao Governador do Estado exercer o comando supremo da Polícia Militar e do Corpo de Bombeiros Militar, promover seus oficiais e nomeá-los para os cargos que lhe são privativos.\nAssinale a alternativa correta.",
        "gab": "D",
        "alts": [
            ("A", "Apenas as afirmativas II e IV estão corretas"),
            ("B", "Apenas as afirmativas I, II e IV estão corretas"),
            ("C", "Apenas a afirmativa II está correta"),
            ("D", "As afirmativas I, II, III e IV estão corretas"),
            ("E", "Apenas as afirmativas II e III estão corretas")
        ]
    },

    # Direitos Humanos (Q56 a Q60)
    {
        "pos": 56, "materia": "Direitos Humanos", "dif": "FACIL", "base": None,
        "enunc": "A Declaração Universal de Direitos Humanos de 1948 procurou colocar a dignidade da pessoa humana como núcleo de todos os direitos humanos. Assim, sobre seu âmbito de proteção, assinale a alternativa correta.",
        "gab": "D",
        "alts": [
            ("A", "Nem todo ser humano tem o direito de ser, em todos os lugares, reconhecido como pessoa perante a lei"),
            ("B", "O exílio é permitido em determinadas situações"),
            ("C", "Reconhece a possibilidade da norma retroagir para prejudicar o réu"),
            ("D", "Todo ser humano acusado de um ato delituoso tem o direito de ser presumido inocente até que a sua culpabilidade tenha sido provada de acordo com a lei, em julgamento público no qual lhe tenha sido asseguradas todas as garantias necessárias à sua defesa"),
            ("E", "A vontade do povo será a base da autoridade do governo; esta vontade será expressa em eleições periódicas e legítimas, por sufrágio censitário, por voto secreto ou processo equivalente que assegure a liberdade de voto")
        ]
    },
    {
        "pos": 57, "materia": "Direitos Humanos", "dif": "MEDIO", "base": None,
        "enunc": "A Convenção Americana de Direitos Humanos (Pacto de San José da Costa Rica, 1969) busca consolidar um regime de liberdade pessoal e justiça social. Assim, quanto ao seu âmbito de proteção, analise as afirmativas abaixo e dê valores Verdadeiro (V) ou Falso (F).\n( ) Não existe nenhuma relação entre o Pacto de San Jose da Costa Rica e a Declaração Universal dos Direitos Humanos.\n( ) Sobre os deveres das pessoas, determina que toda pessoa tem deveres para com a família, a comunidade e a humanidade.\n( ) Toda pessoa tem direito a um recurso simples e rápido ou a qualquer outro recurso efetivo, perante os juízes ou tribunais competentes, que a proteja contra atos que violem seus direitos fundamentais reconhecidos pela constituição, pela lei ou pela presente Convenção, mesmo quando tal violação seja cometida por pessoas que estejam atuando no exercício de suas funções oficiais.\n( ) Algumas disposições do Pacto de San José da Costa Rica podem excluir outros direitos e garantias que são inerentes ao ser humano ou que decorrem da forma democrática representativa de governo.\nAssinale a alternativa que apresenta a sequência correta de cima para baixo.",
        "gab": "E",
        "alts": [("A", "V, V, V, V"), ("B", "V, V, F, F"), ("C", "V, F, F, V"), ("D", "F, F, V, V"), ("E", "F, V, V, F")]
    },
    {
        "pos": 58, "materia": "Direitos Humanos", "dif": "FACIL", "base": None,
        "enunc": "O Pacto Internacional dos Direitos Econômicos, Sociais e Culturais é caracterizado por veicular normas programáticas. Sobre os direitos e compromissos previstos no referido Pacto, assinale a alternativa incorreta.",
        "gab": "C",
        "alts": [
            ("A", "A escolha da escola pelos pais, independentemente das indicações das autoridades públicas é um direito"),
            ("B", "Determina o compromisso de todo Estado-parte elaborar um plano de ação para implementação progressiva da educação primária obrigatória e gratuita para todos"),
            ("C", "O direito à escolha do trabalho é limitado a depender das necessidades momentâneas de determinados profissionais"),
            ("D", "A greve é reconhecida como um direito"),
            ("E", "A previdência social é reconhecida como um direito")
        ]
    },
    {
        "pos": 59, "materia": "Direitos Humanos", "dif": "MEDIO", "base": None,
        "enunc": "O Pacto Internacional dos Direitos Civis e Políticos (1966) instituiu um Comitê de Direitos Humanos. Sobre este, assinale a alternativa correta.",
        "gab": "*", # Anulada
        "alts": [
            ("A", "Os Estados-partes devem enviar ao Comitê, sempre que solicitados, relatórios sobre as medidas por eles adotadas para concretizar os direitos mencionados no Pacto"),
            ("B", "O Comitê é composto por 28 membros"),
            ("C", "O quorum para instalação dos trabalhos é de 22 membros"),
            ("D", "O Comitê é integrado exclusivamente por americanos eleitos"),
            ("E", "Os membros do Comitê serão eleitos para um mandato de 2 anos")
        ]
    },
    {
        "pos": 60, "materia": "Direitos Humanos", "dif": "MEDIO", "base": None,
        "enunc": "A Declaração de Pequim adotada pela Quarta Conferência Mundial sobre as mulheres, reconheceu as aspirações de todas as mulheres do mundo inteiro e levaram em consideração a diversidade das mulheres, suas funções e circunstâncias. Sobre sua apresentação, assinale a alternativa incorreta.",
        "gab": "B",
        "alts": [
            ("A", "Reafirma o seu compromisso com o reconhecimento da inalienabilidade, integralidade e indivisibilidade de todos os direitos humanos e liberdades fundamentais"),
            ("B", "Reafirma o compromisso com o reconhecimento do direto de todas as mulheres de controlar todos os aspectos de sua saúde, em particular sua própria fertilidade, exceto no que tange ao aborto, o qual é expressamente proibido"),
            ("C", "Reafirma o compromisso com o impulsionamento do consenso e do progresso alcançados nas anteriores Conferências das Nações Unidas, como sobre as Mulheres, em Nairóbi, sobre as Crianças, em New York e, sobre o Meio Ambiente e o Desenvolvimento, no Rio de Janeiro"),
            ("D", "Reafirma o compromisso com a determinação que é indispensável formular, implementar e monitorar, com a plena participação das mulheres, políticas e programas efetivos, eficientes e reforçadores do enfoque de gênero, incluindo políticas de desenvolvimento e programas que em todos os níveis busquem o fortalecimento e o avanço das mulheres"),
            ("E", "Reafirma o compromisso com a garantia do êxito da Plataforma de Ação em países cujas economias estejam em transição, o que requer continua cooperação e assistência internacional")
        ]
    },

    # Direito Administrativo (Q61 a Q65)
    {
        "pos": 61, "materia": "Direito Administrativo", "dif": "FACIL", "base": None,
        "enunc": "O artigo 37, parágrafo 1°, da Constituição Federal de 1988 dispõe o seguinte:\n“§1° A publicidade dos atos, programas, obras, serviços e campanhas dos órgãos públicos deverá ter caráter educativo, informativo ou de orientação social, dela não podendo constar nomes, símbolos ou imagens que caracterizem promoção pessoal de autoridades ou servidores públicos.”\nA expressão destacada tem relação com um princípio da Administração Pública encontrado na Constituição Federal. Assinale a alternativa correta que apresenta esse princípio.",
        "gab": "C",
        "alts": [("A", "Princípio da especialidade"), ("B", "Princípio da tutela"), ("C", "Princípio da impessoalidade"), ("D", "Princípio da hierarquia"), ("E", "Princípio da continuidade do interesse público")]
    },
    {
        "pos": 62, "materia": "Direito Administrativo", "dif": "FACIL", "base": None,
        "enunc": "No que se refere aos atributos dos atos administrativos, analise as afirmativas abaixo e dê valores Verdadeiro (V) ou Falso (F).\n( ) A imperatividade é um atributo do ato administrativo.\n( ) A autoexecutoriedade é um atributo pelo qual o ato administrativo pode ser posto em execução pela própria Administração Pública, sem necessidade de intervenção do Poder Judiciário.\n( ) Para que um ato administrativo esteja em consonância com a lei e seja presumido legítimo é necessário uma intervenção estatal.\nAssinale a alternativa que apresenta a sequência correta de cima para baixo.",
        "gab": "B",
        "alts": [("A", "V, V, V"), ("B", "V, V, F"), ("C", "V, F, V"), ("D", "F, F, V"), ("E", "F, V, F")]
    },
    {
        "pos": 63, "materia": "Direito Administrativo", "dif": "MEDIO", "base": None,
        "enunc": "Acerca dos Poderes da Administração Pública, em especial o Poder de Polícia, analise as afirmativas abaixo.\nI. A polícia administrativa rege-se pelo Direito Administrativo, incidindo sobre bens, direitos ou atividades.\nII. Costuma-se apontar como atributos do poder de polícia a discricionariedade, a autoexecutoriedade e a coercibilidade.\nIII. A polícia judiciária rege-se pelo Direito Processual Penal, incidindo sobre pessoas.\nAssinale a alternativa correta.",
        "gab": "A",
        "alts": [
            ("A", "As afirmativas I, II e III estão corretas"),
            ("B", "Apenas as afirmativas I e II estão corretas"),
            ("C", "Apenas as afirmativas II e III estão corretas"),
            ("D", "Apenas a afirmativa I está correta"),
            ("E", "Apenas a afirmativa II está correta")
        ]
    },
    {
        "pos": 64, "materia": "Direito Administrativo", "dif": "FACIL", "base": None,
        "enunc": "Acerca das disposições da Constituição Federal de 1988 sobre a Administração Pública e os servidores públicos, assinale a alternativa incorreta.",
        "gab": "D",
        "alts": [
            ("A", "Os cargos, empregos e funções públicas são acessíveis aos brasileiros que preencham os requisitos estabelecidos em lei, assim como aos estrangeiros, na forma da lei"),
            ("B", "A investidura em cargo ou emprego público depende de aprovação prévia em concurso público de provas ou de provas e títulos, de acordo com a natureza e a complexidade do cargo ou emprego, na forma prevista em lei, ressalvadas as nomeações para cargo em comissão declarado em lei de livre nomeação e exoneração"),
            ("C", "É garantido ao servidor público civil o direito à livre associação sindical"),
            ("D", "A Constituição estipula um teto para a remuneração e o subsídio dos ocupantes de cargos, funções e empregos públicos da administração direta, autárquica e fundacional, mas não para os membros de qualquer dos Poderes da União, dos Estados, do Distrito Federal e dos Municípios, dos detentores de mandato eletivo e dos demais agentes políticos"),
            ("E", "A lei reservará percentual dos cargos e empregos públicos para as pessoas portadoras de deficiência e definirá os critérios de sua admissão")
        ]
    },
    {
        "pos": 65, "materia": "Direito Administrativo", "dif": "MEDIO", "base": None,
        "enunc": "Sobre discricionariedade, vinculação e os elementos do ato administrativo, analise as afirmativas abaixo.\nI. Discricionariedade é sinônimo de arbitrariedade.\nII. A discricionariedade é verificada quando a lei deixa certa margem de liberdade de decisão diante do caso concreto, de tal modo que a autoridade poderá optar por uma dentre várias soluções possíveis, todas válidas perante o direito.\nIII. O exercício da discricionariedade comumente é verificado nos elementos motivo e objeto do ato administrativo.\nAssinale a alternativa correta.",
        "gab": "C",
        "alts": [
            ("A", "As afirmativas I, II e III estão corretas"),
            ("B", "Apenas as afirmativas I e II estão corretas"),
            ("C", "Apenas as afirmativas II e III estão corretas"),
            ("D", "Apenas a afirmativa I está correta"),
            ("E", "Apenas a afirmativa II está correta")
        ]
    },

    # Direito Penal (Q66 a Q70)
    {
        "pos": 66, "materia": "Direito Penal", "dif": "MEDIO", "base": None,
        "enunc": "A entrada em vigor da nova Lei de Drogas, revogando a anterior, fez com que o crime de porte de drogas para consumo pessoal deixasse de prever a aplicação de pena privativa de liberdade, passando a adotar sanções como advertência, prestação de serviços à comunidade e medida educativa. Nesse sentido, no que tange à pena aplicável ao autor do citado delito, é correto afirmar que a nova lei de drogas constitui um exemplo de:",
        "gab": "D",
        "alts": [("A", "novatio legis não incriminadora"), ("B", "abolitio criminis"), ("C", "novatio legis in pejus"), ("D", "novatio legis in mellius"), ("E", "lei intermediária")]
    },
    {
        "pos": 67, "materia": "Direito Penal", "dif": "FACIL", "base": None,
        "enunc": "Em face do crime de associação criminosa (art. 288 do Código Penal), assinale a alternativa correta.",
        "gab": "E",
        "alts": [
            ("A", "a pena aumenta-se até um terço se houver a participação de criança ou adolescente"),
            ("B", "trata-se de crime de concurso eventual de agentes"),
            ("C", "configura associação criminosa o ato de constituir, organizar ou manter grupo de pessoas com a finalidade de praticar crimes previstos no Código Penal"),
            ("D", "a pena aumenta-se até um terço se a associação é armada"),
            ("E", "configura associação criminosa o ato de associarem-se 3 (três) ou mais pessoas, para o fim específico de cometer crimes")
        ]
    },
    {
        "pos": 68, "materia": "Direito Penal", "dif": "FACIL", "base": None,
        "enunc": "Assinale a alternativa que preencha corretamente a lacuna:\nApresenta-se como causa excludente de ilicitude _____.",
        "gab": "A",
        "alts": [("A", "o exercício regular de direito"), ("B", "a inimputabilidade"), ("C", "a coação moral irresistível"), ("D", "a obediência hierárquica"), ("E", "o erro sobre a ilicitude do fato")]
    },
    {
        "pos": 69, "materia": "Direito Penal", "dif": "FACIL", "base": None,
        "enunc": "Sobre a definição de crime de importunação sexual (art. 215-A do Código Penal), assinale a alternativa correta.",
        "gab": "C",
        "alts": [
            ("A", "ter conjunção carnal ou praticar outro ato libidinoso com alguém, mediante fraude ou outro meio que impeça ou dificulte a livre manifestação de vontade da vítima"),
            ("B", "constranger alguém, mediante violência ou grave ameaça, a ter conjunção carnal ou a praticar ou permitir que com ele se pratique outro ato libidinoso"),
            ("C", "praticar contra alguém e sem a sua anuência ato libidinoso com o objetivo de satisfazer a própria lascívia ou a de terceiro"),
            ("D", "induzir alguém menor de 14 (catorze) anos a satisfazer a lascívia de outrem"),
            ("E", "constranger alguém com o intuito de obter vantagem ou favorecimento sexual, prevalecendo-se o agente da sua condição de superior hierárquico ou ascendência inerentes ao exercício de emprego, cargo ou função")
        ]
    },
    {
        "pos": 70, "materia": "Direito Penal", "dif": "FACIL", "base": None,
        "enunc": "Assinale a alternativa correta. Apresenta-se como conduta própria de contravenção penal o ato de:",
        "gab": "B",
        "alts": [
            ("A", "obter, para si ou para outrem, vantagem ilícita, em prejuízo alheio, induzindo ou mantendo alguém em erro, mediante artifício, ardil ou qualquer outro meio fraudulento"),
            ("B", "recusar à autoridade, quando por esta, justificadamente solicitados ou exigidos, dados ou indicações concernentes à própria identidade, estado, profissão, domicílio e residência"),
            ("C", "adquirir, receber ou ocultar, em proveito próprio ou alheio, coisa que sabe ser produto de crime, ou influir para que terceiro, de boa-fé, a adquira, receba ou oculte"),
            ("D", "destruir, inutilizar ou deteriorar coisa alheia"),
            ("E", "apropriar-se de coisa alheia móvel, de que tem a posse ou a detenção")
        ]
    },

    # Igualdade Racial e de Gênero (Q71 a Q75)
    {
        "pos": 71, "materia": "Igualdade Racial e de Gênero", "dif": "FACIL", "base": None,
        "enunc": "O artigo 4° da Constituição Federal preocupou-se fundamentalmente com a definição dos princípios que devem orientar o Estado brasileiro nas suas relações internacionais. Leia atentamente os itens abaixo e, nos termos da Constituição de 1988, assinale a alternativa que não contém princípio regente das relações internacionais brasileiras.",
        "gab": "A",
        "alts": [("A", "Pluralismo político"), ("B", "Prevalência dos direitos humanos"), ("C", "Repúdio ao terrorismo e ao racismo"), ("D", "Cooperação entre os povos para o progresso da humanidade"), ("E", "Concessão de asilo político")]
    },
    {
        "pos": 72, "materia": "Igualdade Racial e de Gênero", "dif": "FACIL", "base": None,
        "enunc": "Assinale a alternativa que apresenta corretamente órgão de assessoramento imediato ao Presidente da República nas questões sobre Políticas de promoção da Igualdade Racial",
        "gab": "B",
        "alts": [
            ("A", "Ministério da Justiça"),
            ("B", "Secretaria Especial de Políticas de Promoção da Igualdade Racial"),
            ("C", "Secretaria de políticas públicas"),
            ("D", "Advogado-Geral da União"),
            ("E", "Secretaria Especial da Defensoria Pública")
        ]
    },
    {
        "pos": 73, "materia": "Igualdade Racial e de Gênero", "dif": "MEDIO", "base": None,
        "enunc": "A Lei Federal n° 12.288 / 2010, institui o Estatuto da Igualdade Racial, destinado a garantir à população negra a efetivação da igualdade de oportunidades. Nos termos da lei, assinale a alternativa que indica corretamente o sentido de desigualdade de gênero e raça.",
        "gab": "E",
        "alts": [
            ("A", "o conjunto de pessoas que se autodeclaram pretas e pardas, conforme o quesito cor ou raça usado pela Fundação Instituto Brasileiro de Geografia e Estatística (IBGE), ou que adotam autodefinição análoga"),
            ("B", "toda situação injustificada de diferenciação de acesso e fruição de bens, serviços e oportunidades, nas esferas pública e privada, em virtude de raça, cor, descendência ou origem nacional ou étnica"),
            ("C", "toda distinção, exclusão, restrição ou preferência baseada em raça, cor, descendência ou origem nacional ou étnica que tenha por objeto anular ou restringir o reconhecimento, gozo ou exercício de direitos humanos"),
            ("D", "Os programas e medidas especiais adotados pelo Estado e pela iniciativa privada para a correção das desigualdades raciais e para a promoção da igualdade de oportunidades"),
            ("E", "Assimetria existente no âmbito da sociedade que acentua a distância social entre mulheres negras e os demais segmentos sociais")
        ]
    },
    {
        "pos": 74, "materia": "Igualdade Racial e de Gênero", "dif": "MEDIO", "base": None,
        "enunc": "A Convenção Internacional sobre a eliminação de todas as formas de discriminação racial considera todos os homens iguais perante a lei. Sobre o papel dos Estados Partes, assinale a alternativa incorreta.",
        "gab": "C",
        "alts": [
            ("A", "Cada Estado Parte compromete-se a efetuar nenhum ato ou prática de discriminação racial contra pessoas, grupos de pessoas ou instituições e fazer com que todas as autoridades públicas nacionais ou locais, se conformem com esta obrigação"),
            ("B", "Cada Estado Parte compromete-se a não encorajar, defender ou apoiar a discriminação racial praticada por uma pessoa ou uma organização qualquer"),
            ("C", "Cada Estado Parte só não deverá tomar medidas eficazes a fim de rever as politicas governamentais nacionais e locais e para modificar, ab-rogar ou anular qualquer disposição regulamentar que tenha como objetivo criar a discriminação ou perpetra-la onde já existir"),
            ("D", "Cada Estado Parte deverá, por todos os meios apropriados, inclusive se as circunstâncias o exigirem, as medidas legislativas, proibir e por fim, a discriminação racial praticadas por pessoa, por grupo ou das organizações"),
            ("E", "Cada Estado Parte compromete-se a favorecer, quando for o caso as organizações e movimentos multi-raciais e outros meios próprios a eliminar as barreiras entre as raças e a desencorajar o que tende a fortalecer a divisão racial")
        ]
    },
    {
        "pos": 75, "materia": "Igualdade Racial e de Gênero", "dif": "FACIL", "base": None,
        "enunc": "O Código Penal prevê, em seu artigo 140, a injúria racial como crime, considerando a ofensa feita a uma determinada pessoa com referência à sua raça, cor, etnia, religião ou origem. Sobre a injúria racial assinale a alternativa correta.",
        "gab": "D",
        "alts": [
            ("A", "Tem como bem jurídico a dignidade humana da coletividade"),
            ("B", "Trata-se de ação penal pública incondicionada"),
            ("C", "É imprescritível"),
            ("D", "Cabe fiança"),
            ("E", "A pena aplicada é detenção, de um a seis meses, ou multa")
        ]
    },

    # Direito Penal Militar (Q76 a Q80)
    {
        "pos": 76, "materia": "Direito Penal Militar", "dif": "FACIL", "base": None,
        "enunc": "Sobre o que constitui a conduta típica de crime militar de motim (art. 149 do CPM), assinale a alternativa correta.",
        "gab": "B",
        "alts": [
            ("A", "reunirem-se dois militares, com armamento de propriedade militar, praticando violência à coisa pública ou particular em lugar não sujeito à administração militar"),
            ("B", "reunirem-se militares desarmados agindo contra a ordem recebida de superior, ou negando-se a cumpri-la"),
            ("C", "reunirem-se mais de dois militares ou assemelhados, com material bélico de propriedade militar, praticando violência à pessoa em lugar sujeito à administração militar"),
            ("D", "deixar o militar de levar ao conhecimento do superior conspiração de cuja preparação teve notícia, ou, estando presente ao ato criminoso, não usar de todos os meios ao seu alcance para impedí-lo"),
            ("E", "reunirem-se militares armados, recusando obediência a superior, quando estejam agindo sem ordem ou praticando violência")
        ]
    },
    {
        "pos": 77, "materia": "Direito Penal Militar", "dif": "FACIL", "base": None,
        "enunc": "Sobre o que configura conduta típica do crime de recusa de obediência (art. 163 do CPM), assinale a alternativa correta.",
        "gab": "C",
        "alts": [
            ("A", "desrespeitar superior diante de outro militar"),
            ("B", "despojar-se de uniforme, condecoração militar, insígnia ou distintivo, por menosprezo ou vilipêndio"),
            ("C", "recusar obedecer a ordem do superior sobre assunto ou matéria de serviço, ou relativamente a dever imposto em lei, regulamento ou instrução"),
            ("D", "promover a reunião de militares, ou nela tomar parte, para discussão de ato de superior ou assunto atinente à disciplina militar"),
            ("E", "praticar o militar diante da tropa, ou em lugar sujeito à administração militar, ato que se traduza em ultraje a símbolo nacional")
        ]
    },
    {
        "pos": 78, "materia": "Direito Penal Militar", "dif": "FACIL", "base": None,
        "enunc": "O ato de “retardar ou deixar de praticar, indevidamente, ato de ofício, ou praticá-lo contra expressa disposição de lei, para satisfazer interesse ou sentimento pessoal” configura o crime militar de:",
        "gab": "E",
        "alts": [("A", "abuso de confiança"), ("B", "condescendência criminosa"), ("C", "omissão de dever funcional"), ("D", "retardamento de ato de ofício"), ("E", "prevaricação")]
    },
    {
        "pos": 79, "materia": "Direito Penal Militar", "dif": "MEDIO", "base": None,
        "enunc": "No que se refere ao crime de deserção (art. 187 do CPM), é correto afirmar que:",
        "gab": "*", # Anulada
        "alts": [
            ("A", "configura exercício regular de direito o ato de evadir-se o militar do poder da escolta, permanecendo ausente por mais de oito dias"),
            ("B", "é isento de pena o oficial que deixa de proceder contra desertor, sabendo, ou devendo saber encontrar-se entre os seus comandados"),
            ("C", "constitui conduta lícita o ato de dar asilo a desertor ou facilitar-lhe transporte, conhecendo sua particular situação frente às normas militares"),
            ("D", "na deserção especial, a pena é aumentada de um terço, se se tratar de sargento, subtenente ou suboficial, e de metade, se oficial"),
            ("E", "se a deserção ocorre em unidade estacionada em fronteira ou país estrangeiro, a pena é agravada de metade")
        ]
    },
    {
        "pos": 80, "materia": "Direito Penal Militar", "dif": "FACIL", "base": None,
        "enunc": "A ofensa à dignidade ou ao decoro são elementares que se fazem presentes expressamente no crime militar de:",
        "gab": "C",
        "alts": [
            ("A", "desacato a assemelhado ou funcionário"),
            ("B", "ingresso clandestino"),
            ("C", "desacato a superior"),
            ("D", "desobediência"),
            ("E", "desacato a militar")
        ]
    }
]

payload_api = []

for q in questoes:
    pos_str = f"{q['pos']:02d}"
    id_origem = f"PMBA_SOLDADO_2019_Q{pos_str}"
    
    enunciado_final = q["enunc"]
    if q["base"] and q["base"].strip():
        enunciado_final = f"{q['base'].strip()}\n\n{q['enunc'].strip()}"
        
    dif = q["dif"]
    if dif == "MEDIO":
        dif = "MODERADO"
        
    alternativas_list = []
    for letra, texto in q["alts"]:
        is_correta = (letra == q["gab"]) if q["gab"] != "*" else False
        alternativas_list.append({
            "letra": letra,
            "texto": texto,
            "correta": is_correta
        })
        
    payload_api.append({
        "idOrigem": id_origem,
        "fonte": fonte,
        "banca": banca,
        "orgao": orgao,
        "cargo": cargo,
        "ano": ano,
        "materiaNome": q["materia"],
        "dificuldade": dif,
        "enunciado": enunciado_final,
        "imagemUrl": None,
        "alternativas": alternativas_list
    })

output_dir = r"C:\Users\luisd\.gemini\antigravity\scratch\Parsertrajetoria\output"
os.makedirs(output_dir, exist_ok=True)

out_file = os.path.join(output_dir, "pmba_soldado_2019_payload_api.json")
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(payload_api, f, ensure_ascii=False, indent=2)

print(f"Sucesso! {len(payload_api)} questoes geradas em {out_file}")
