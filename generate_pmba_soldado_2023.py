import json
import os

banca = "FCC"
orgao = "Polícia Militar da Bahia - PMBA"
cargo = "Aluno Soldado da PM (PMM) - Tipo 001"
ano = 2023
fonte = "CONCURSO"

texto_drummond = """O importuno
Carlos Drummond de Andrade (13/07/1966)
1. − Que negócio é esse? Ninguém me atende?
2. A muito custo, atenderam; isto é, confessaram que não podiam atender, por causa do jogo com a Bulgária.
3. − Mas que tenho eu com o jogo com a Bulgária, façam-me o favor? E os senhores por acaso foram escalados para jogar?
4. O chefe da seção aproximou-se, apaziguador:
5. − Desculpe, cavalheiro. Queira voltar na quinta-feira, 14. Quinta-feira não haverá jogo, estaremos mais tranquilos.
6. − Mas prometeram que meu papel ficaria pronto hoje sem falta.
7. − Foi um lapso do funcionário que lhe prometeu tal coisa. Ele não se lembrou da Bulgária. O Brasil lutando com a Bulgária, o senhor quer que o nosso pessoal tenha cabeça fria para informar papéis?
8. − Perdão, o jogo vai ser logo mais, às quinze horas. É meio-dia, e já estão torcendo?
9. − Ah, meu caro senhor, não critique nossos bravos companheiros, que fizeram o sacrifício de vir à repartição trabalhar quando podiam ficar em casa ou na rua, participando da emoção do povo…
10. − Se vieram trabalhar, por que não trabalham?
11. − Porque não podem, ouviu? Porque não podem. O senhor está ficando impertinente. Aliás, disse logo de saída que não tinha nada com o jogo com a Bulgária! O Brasil em guerra − porque é uma verdadeira guerra, como revelam os jornais − nos campos da Europa, e o senhor, indiferente, alienado, perguntando por um vago papel, uma coisinha individual, insignificante, em face dos interesses da pátria!
12. − Muito bem! Muito bem! − funcionários batiam palmas.
13. − Mas, perdão, eu… eu…
14. − Já sei que vai se desculpar. O momento não é para dissensões. O momento é de união nacional, cérebros e corações uníssonos. Vamos, cavalheiro, não perturbe a preparação espiritual dos meus colegas, que estão analisando a Seleção Búlgara e descobrindo meios de frustrar a marcação de Pelé. O senhor acha bem o 4-2-4 ou prefere o 4-3-3?
15. − Bem, eu… eu…
16. − Compreendo que não queira opinar. É muita responsabilidade. Eu aliás não forço opinião de ninguém. Esta algazarra que o senhor está vendo resulta da ampla liberdade de opinião com que se discute a formação do selecionado. Todos querem ajudar, por isso cada um tem sua ideia própria, que não se ajusta com a ideia do outro, mas o resultado é admirável. A unidade pela diversidade. Na hora da batalha, formamos uma frente única.
17. − Está certo, mas será que, voltando na quinta-feira, eu encontro o meu papel pronto mesmo?
18. − Ah, o senhor é terrível, nem numa hora dessas esquece o seu papelzinho! Eu disse quinta-feira? Sim, certamente, pois é dia de folga no campeonato. Mas espere aí, com quatro jogos na quarta-feira, e o gasto de energia que isso determina, como é que eu posso garantir o seu papel para quinta-feira? Quer saber de uma coisa? Seja razoável, meu amigo, procure colaborar. Procure ser bom brasileiro, volte em agosto, na segunda quinzena de agosto é melhor, depois de comemorarmos a conquista do Tri.
19. − E… se não conquistarmos?
20. − Não diga uma besteira dessas! Sai, azar! Vá-se embora, antes que eu perca a cabeça e…
21. Vozes indignadas:
22. − Fora! Fora!
23. O servente sobe na cadeira e comanda o coro:
24. − Bra-sil! Bra-sil! Bra-sil!
25. Estava salva a honra da torcida, e o importuno retirou-se precipitadamente.
(Adaptado de: ANDRADE, Carlos Drummond de. Quando é dia de futebol. São Paulo: Companhia das Letras, 2014)"""

texto_sachs = """Será o Brasil o eterno país do futuro? Quase sessenta após [I] publicação do conhecido livro de Stefan Zweig, não obstante um século de crescimento econômico sobremodo rápido e de modernização espetacular no decurso do qual a sua produção decuplicou e o PIB foi multiplicado por quarenta, o Brasil não consegue superar o seu fantástico atraso social. Graças [II] bem-sucedida industrialização substitutiva das importações, conduzida nas décadas de 1950, 1960 e 1970, o Brasil se ergueu [III] posição de nona potência econômica do mundo. É hoje um país mal desenvolvido por ter adotado um padrão de crescimento socialmente perverso. Ostenta uma das mais regressivas repartições da renda no mundo, com diferenças abismais entre a minoria dos ganhadores e a massa dos sacrificados.
(Adaptado de: PINHEIRO, Paulo Sérgio et al. (orgs.). Brasil: um século de transformações. São Paulo: Companhia das Letras, 2001)"""

questoes = [
    # Língua Portuguesa
    {
        "pos": 1, "materia": "Língua Portuguesa", "dif": "FACIL", "base": texto_drummond,
        "enunc": "Na crônica, o chefe da seção acusa o homem que foi à repartição em busca de um documento de ser",
        "gab": "B",
        "alts": [("A", "preguiçoso."), ("B", "egoísta."), ("C", "contraditório."), ("D", "resignado."), ("E", "rancoroso.")]
    },
    {
        "pos": 2, "materia": "Língua Portuguesa", "dif": "FACIL", "base": texto_drummond,
        "enunc": "O cronista expressa uma retificação no seguinte trecho:",
        "gab": "D",
        "alts": [
            ("A", "O servente sobe na cadeira e comanda o coro: (23º parágrafo)"),
            ("B", "− Muito bem! Muito bem! − funcionários batiam palmas. (12º parágrafo)"),
            ("C", "− Está certo, mas será que, voltando na quinta-feira, eu encontro o meu papel pronto mesmo? (17º parágrafo)"),
            ("D", "A muito custo, atenderam; isto é, confessaram que não podiam atender, por causa do jogo com a Bulgária. (2º parágrafo)"),
            ("E", "Estava salva a honra da torcida, e o importuno retirou-se precipitadamente. (25º parágrafo)")
        ]
    },
    {
        "pos": 3, "materia": "Língua Portuguesa", "dif": "MEDIO", "base": texto_drummond,
        "enunc": "− Já sei que vai se desculpar. O momento não é para dissensões. O momento é de união nacional, cérebros e corações uníssonos. (14º parágrafo)\nO termo sublinhado (dissensões) pode ser substituído, sem prejuízo para o sentido do texto original, por:",
        "gab": "A",
        "alts": [("A", "desavenças."), ("B", "distrações."), ("C", "mentiras."), ("D", "hesitações."), ("E", "especulações.")]
    },
    {
        "pos": 4, "materia": "Língua Portuguesa", "dif": "FACIL", "base": texto_drummond,
        "enunc": "• Foi um lapso do funcionário que lhe prometeu tal coisa. (7º parágrafo)\n• Vamos, cavalheiro, não perturbe a preparação espiritual dos meus colegas, que estão analisando a Seleção Búlgara e descobrindo meios de frustrar a marcação de Pelé. (14º parágrafo)\nOs pronomes sublinhados (que) no texto referem-se, respectivamente, a",
        "gab": "A",
        "alts": [
            ("A", "funcionário e colegas."),
            ("B", "lapso e colegas."),
            ("C", "coisa e Seleção Búlgara."),
            ("D", "lapso e preparação espiritual."),
            ("E", "funcionário e preparação espiritual.")
        ]
    },
    {
        "pos": 5, "materia": "Língua Portuguesa", "dif": "FACIL", "base": texto_drummond,
        "enunc": "É invariável quanto a gênero e a número o termo sublinhado em:",
        "gab": "C",
        "alts": [
            ("A", "Mas prometeram que meu papel ficaria pronto hoje sem falta."),
            ("B", "Que negócio é esse?"),
            ("C", "Eu aliás não forço opinião de ninguém."),
            ("D", "É muita responsabilidade."),
            ("E", "Na hora da batalha, formamos uma frente única.")
        ]
    },
    {
        "pos": 6, "materia": "Língua Portuguesa", "dif": "FACIL", "base": texto_drummond,
        "enunc": "Verifica-se o emprego de vírgula(s) para isolar um vocativo em:",
        "gab": "E",
        "alts": [
            ("A", "Ah, o senhor é terrível, nem numa hora dessas esquece o seu papelzinho! (18º parágrafo)"),
            ("B", "Perdão, o jogo vai ser logo mais, às quinze horas. (8º parágrafo)"),
            ("C", "Mas, perdão, eu… eu… (13º parágrafo)"),
            ("D", "Na hora da batalha, formamos uma frente única. (16º parágrafo)"),
            ("E", "Seja razoável, meu amigo, procure colaborar. (18º parágrafo)")
        ]
    },
    {
        "pos": 7, "materia": "Língua Portuguesa", "dif": "FACIL", "base": texto_drummond,
        "enunc": "Exerce a função sintática de sujeito o elemento sublinhado no seguinte trecho:",
        "gab": "C",
        "alts": [
            ("A", "O senhor está ficando impertinente (11º parágrafo)."),
            ("B", "Quinta-feira não haverá jogo (5º parágrafo)."),
            ("C", "Estava salva a honra da torcida (25º parágrafo)."),
            ("D", "Na hora da batalha, formamos uma frente única (16º parágrafo)."),
            ("E", "Não diga uma besteira dessas (20º parágrafo).")
        ]
    },
    {
        "pos": 8, "materia": "Língua Portuguesa", "dif": "FACIL", "base": texto_drummond,
        "enunc": "Observa-se o emprego de voz passiva em:",
        "gab": "B",
        "alts": [
            ("A", "Ninguém me atende? (1º parágrafo)"),
            ("B", "E os senhores por acaso foram escalados para jogar? (3º parágrafo)"),
            ("C", "É meio-dia, e já estão torcendo? (8º parágrafo)"),
            ("D", "Se vieram trabalhar, por que não trabalham? (10º parágrafo)"),
            ("E", "O senhor acha bem o 4-2-4 ou prefere o 4-3-3? (14º parágrafo)")
        ]
    },
    {
        "pos": 9, "materia": "Língua Portuguesa", "dif": "FACIL", "base": texto_sachs,
        "enunc": "Em conformidade com a norma-padrão da língua portuguesa, as lacunas I, II e III devem ser preenchidas, respectivamente, por:",
        "gab": "D",
        "alts": [("A", "à – a – à."), ("B", "à – à – a."), ("C", "a – à – a."), ("D", "a – à – à."), ("E", "a – a – à.")]
    },
    {
        "pos": 10, "materia": "Língua Portuguesa", "dif": "FACIL", "base": texto_sachs,
        "enunc": "É hoje um país mal desenvolvido por ter adotado um padrão de crescimento socialmente perverso.\nEm relação ao trecho que o antecede, o segmento sublinhado expressa ideia de",
        "gab": "E",
        "alts": [("A", "concessão."), ("B", "consequência."), ("C", "condição."), ("D", "comparação."), ("E", "causa.")]
    },

    # Matemática (Q11 a Q18)
    {
        "pos": 11, "materia": "Matemática", "dif": "MEDIO", "base": None,
        "enunc": "Um setor administrativo recebeu 150 caixas de equipamentos que serão distribuídas para três grupos de funcionários. O primeiro grupo deverá receber 30 caixas a menos do que o segundo grupo e o terceiro grupo a metade do que vai receber o segundo. O número de caixas que serão recebidas pelo primeiro e o terceiro grupos juntos é:",
        "gab": "A",
        "alts": [("A", "78"), ("B", "52"), ("C", "44"), ("D", "80"), ("E", "96")]
    },
    {
        "pos": 12, "materia": "Matemática", "dif": "FACIL", "base": None,
        "enunc": "Em um fornecedor de uniformes, três camisas e duas calças custam, juntas, R$ 455,00, e um conjunto de calça e camisa do mesmo tipo custa R$ 190,00. O preço, em reais, para a compra de duas camisas e uma calça é:",
        "gab": "C",
        "alts": [("A", "215"), ("B", "240"), ("C", "265"), ("D", "280"), ("E", "305")]
    },
    {
        "pos": 13, "materia": "Matemática", "dif": "MEDIO", "base": None,
        "enunc": "A sequência de 3 figuras a seguir é formada com palitos de fósforo, acrescentando sempre um triângulo à figura anterior (Figura 1: 5 palitos, Figura 2: 7 palitos, Figura 3: 9 palitos...). O número de palitos necessários para continuarmos a sequência até a Figura 20 é:",
        "gab": "D",
        "alts": [("A", "620"), ("B", "520"), ("C", "560"), ("D", "670"), ("E", "750")]
    },
    {
        "pos": 14, "materia": "Matemática", "dif": "FACIL", "base": None,
        "enunc": "Placas para identificação de veículos deverão conter 4 letras distintas. Se escolhermos as letras X, Y, Z e W, o número de placas distintas que poderão ser produzidas é",
        "gab": "B",
        "alts": [("A", "36"), ("B", "24"), ("C", "20"), ("D", "16"), ("E", "12")]
    },
    {
        "pos": 15, "materia": "Matemática", "dif": "FACIL", "base": None,
        "enunc": "A soma das raízes da equação x · (x − 1) · (x + 3) · (x² + 16) = 0 é",
        "gab": "A",
        "alts": [("A", "−2"), ("B", "2"), ("C", "0"), ("D", "4"), ("E", "16")]
    },
    {
        "pos": 16, "materia": "Matemática", "dif": "FACIL", "base": None,
        "enunc": "Uma rampa será construída para acesso ao primeiro andar de uma construção, que está a 2,5 m de altura em relação ao nível do terreno. Decidiu-se que a inclinação da rampa deve ser de 30° em relação ao nível do térreo. O comprimento dessa rampa será",
        "gab": "E",
        "alts": [("A", "2 m"), ("B", "3,5 m"), ("C", "4 m"), ("D", "4,5 m"), ("E", "5 m")]
    },
    {
        "pos": 17, "materia": "Matemática", "dif": "MEDIO", "base": None,
        "enunc": "Num terreno retangular com 80 m de comprimento e 60 m de largura, duas áreas triangulares foram demarcadas para o plantio de árvores, como mostra a figura. O comprimento de um dos lados de cada triângulo é 20 m. A área da parte restante do terreno é, em m²:",
        "gab": "C",
        "alts": [("A", "2 400"), ("B", "3 000"), ("C", "3 400"), ("D", "3 600"), ("E", "3 800")]
    },
    {
        "pos": 18, "materia": "Matemática", "dif": "MEDIO", "base": None,
        "enunc": "O comprimento da aresta de um cubo é igual ao comprimento do lado do quadrado que é base de uma pirâmide quadrangular. A medida da altura da pirâmide é o dobro do comprimento do lado de sua base. A razão entre o volume do cubo e o volume da pirâmide é:",
        "gab": "C",
        "alts": [("A", "3"), ("B", "2"), ("C", "3/2"), ("D", "4/3"), ("E", "5/2")]
    },

    # História do Brasil (Q19 a Q26)
    {
        "pos": 19, "materia": "História do Brasil", "dif": "MEDIO", "base": None,
        "enunc": "No início da colonização portuguesa no Brasil, o emprego do sistema de Capitanias Hereditárias teve como objetivo",
        "gab": "B",
        "alts": [
            ("A", "incentivar o povoamento, por meio da distribuição de lotes de terras restritos à faixa litorânea que ainda permaneciam como sendo de propriedade e administração do rei, mas podiam ser explorados economicamente pelos donatários e por seus herdeiros."),
            ("B", "acelerar a ocupação de uma região que se estendia do litoral atlântico ao Meridiano de Tordesilhas, por meio da doação de terras a homens de posses, que pudessem desenvolvê-las com recursos próprios, mediante o pagamento de tributos."),
            ("C", "promover o desenvolvimento de uma vasta região do território a partir de um experimento inédito, ainda não empregado pela Coroa em suas colônias, e que se mostrou ineficiente, pois diversas capitanias fracassaram."),
            ("D", "assegurar a participação direta de nobres e burgueses ligados à Coroa portuguesa no esforço de colonização, tarefa que resultou, nas catorze capitanias regulamentadas, na instalação de vilas e sesmarias voltadas ao cultivo da cana."),
            ("E", "atrair investidores de diversas nacionalidades, que tivessem capital para empregar na colonização, adquirindo escravizados e se comprometendo, mediante um contrato assinado com a Coroa Portuguesa e com a Igreja Católica, a empregar as leis portuguesas e a catequizar índios e escravizados.")
        ]
    },
    {
        "pos": 20, "materia": "História do Brasil", "dif": "MEDIO", "base": None,
        "enunc": "O surgimento da Coluna Prestes se deu no contexto",
        "gab": "A",
        "alts": [
            ("A", "da expansão do movimento tenentista, principalmente nos estados do Sul e do atual Sudeste, e das reivindicações por uma ampla reforma política que assegurasse, entre várias demandas sociais e políticas, o voto secreto, o acesso ao ensino primário e o fim do poder das oligarquias."),
            ("B", "da insatisfação de parte dos militares com a chamada República Velha, em virtude do poder abusivo exercido por determinadas oligarquias regionais, exigindo, como solução, um golpe militar e uma restruturação do sistema de governo de partido único, por meio da qual as Forças Armadas passariam a ter especial influência sobre o Poder Executivo."),
            ("C", "da chamada Revolução de 30, sob a liderança de Getúlio Vargas, que decidiu pela criação da Coluna a fim de ocupar a capital do país e enfrentar a cúpula do Exército e os movimentos conservadores, como os integralistas, que apoiavam a chamada política do café com leite."),
            ("D", "da influência das ideias marxistas entre os jovens militares brasileiros que, insatisfeitos com o governo autoritário de Artur Bernardes, se reuniram, nos anos 1920, sob a liderança do comunista Luís Carlos Prestes e formaram uma coluna com aspirações revolucionárias."),
            ("E", "de crescimento da oposição popular e da imprensa ao governo, dadas as evidências de práticas antidemocráticas, como o voto de cabresto e a concessão de privilégios econômicos às oligarquias cafeeiras, fatores que resultaram em uma ampla frente popular armada, composta majoritariamente por camponeses, que contou com a preparação militar dos tenentes.")
        ]
    },
    {
        "pos": 21, "materia": "História do Brasil", "dif": "MEDIO", "base": None,
        "enunc": "A Sabinada foi uma revolta que eclodiu em Salvador e",
        "gab": "D",
        "alts": [
            ("A", "teve entre seus líderes o médico Francisco Sabino e o advogado João Carneiro da Silva que, inspirados pela Conjuração Baiana e pela Revolta dos Malês, haviam se tornado defensores da autonomia provincial e do fim da escravidão."),
            ("B", "foi duramente reprimida após alguns meses de sublevação em função do parco apoio recebido, tanto das camadas médias, como dos grandes proprietários de terras, sendo seus líderes condenados ao degredo, na África."),
            ("C", "ocorreu logo após a abdicação de Pedro I ao trono, em defesa da proclamação da República, uma vez que o poder estava acéfalo e o regime monárquico, desde a independência, vinha sendo duramente combatido na Bahia."),
            ("D", "defendia a separação da Bahia e que esta se constituísse em uma república independente e transitória, enquanto D. Pedro II não atingisse a maioridade, dado o grande descontentamento com a situação econômica e com o governo regencial."),
            ("E", "se contrapôs às medidas promulgadas pela Regência Trina, que reforçou o centralismo político, e principalmente contra o recrutamento de cidadãos baianos para a Guarda nacional, a fim de lutarem contra os separatistas do Sul.")
        ]
    },
    {
        "pos": 22, "materia": "História do Brasil", "dif": "FACIL", "base": None,
        "enunc": "O período conhecido como Estado Novo, durante a Era Vargas, foi marcado",
        "gab": "B",
        "alts": [
            ("A", "pelo anticomunismo e pela perseguição aos opositores mediante a atuação do DOPS, Departamento de Ordem Política e Social, organismo criado pelo Estado Novo, por meio da Lei de Segurança Nacional."),
            ("B", "por uma nova constituição de caráter autoritário e pelas ações de propaganda ideológica e censura promovidas pelo Departamento de Imprensa e Propaganda, criado no início desse período."),
            ("C", "pela aliança inicial com os países do Eixo, quando irrompeu a Segunda Guerra Mundial, até o rompimento com estes e a adesão aos Aliados, sob pressão norte-americana, no último ano desse conflito."),
            ("D", "pela criação de um partido situacionista liderado por Getúlio Vargas, que comandava o Estado Brasileiro junto com uma Câmara Corporativa por ele indicada."),
            ("E", "pela tentativa de levante comunista no início deste período e pelo apoio dos integralistas liderados por Vargas na repressão à esquerda.")
        ]
    },
    {
        "pos": 23, "materia": "História do Brasil", "dif": "MEDIO", "base": None,
        "enunc": "A escravidão no Brasil",
        "gab": "C",
        "alts": [
            ("A", "perdurou desde o início da colonização portuguesa até o começo do período republicano, sendo o Brasil um dos últimos países a abolir a escravidão, que atingiu a cifra de milhares de africanos e afrodescendentes escravizados."),
            ("B", "vigorou sob o amparo de uma legislação permanente, conhecida como Código Negro, que assegurou, durante o período colonial e imperial, o tráfico negreiro e amplos direitos dos proprietários sobre os escravizados, sendo toda essa legislação revogada, de uma vez, com a Lei Áurea."),
            ("C", "foi marcada pela submissão, por meio da força, de indígenas nativos no início do período colonial e, a partir da segunda metade do século XVI, pela importação de uma grande massa de africanos escravizados, estes últimos frequentemente explorados também nas propriedades da Igreja Católica."),
            ("D", "rendeu enormes lucros para a Companhia das Índias Ocidentais, empresa criada em Portugal e que detinha o monopólio do tráfico negreiro nos entrepostos portugueses da África."),
            ("E", "foi empregada desde o início da colonização, utilizando-se exclusivamente de mão de obra africana, como forma de preservar os indígenas do trabalho forçado, uma vez que os povos nativos eram considerados súditos da Coroa Portuguesa e aptos à catequese.")
        ]
    },
    {
        "pos": 24, "materia": "História do Brasil", "dif": "MEDIO", "base": None,
        "enunc": "A Independência do Brasil foi fruto de um processo histórico permeado por fatores externos e internos importantes. São exemplos de um fator externo e um fator interno que impactaram na relação entre Portugal e Brasil, respectivamente,",
        "gab": "E",
        "alts": [
            ("A", "as Cortes de Cádiz, que obrigaram o pronto retorno de Dom João VI a Portugal, e a circulação de ideias liberais e republicanas na imprensa das principais províncias brasileiras."),
            ("B", "a leva de independências ocorrida na América Hispânica, na década anterior, e as manifestações urbanas contra os privilégios da Coroa Portuguesa nos anos 1820, como a Noite das Garrafadas."),
            ("C", "a crise política interna de Portugal, devido à invasão de Napoleão, e a pressão popular provocada pelo assassinato de Líbero Badaró, jornalista militante da causa independentista."),
            ("D", "o aumento da exploração colonial devido à situação econômica de Portugal após ações de combate, por parte da Inglaterra, ao tráfico negreiro por meio da lei conhecida como Bill Aberdeen, e a criação das Juntas Provisórias nas províncias."),
            ("E", "a Revolução Liberal do Porto e o crescimento de mobilizações pela independência em várias regiões da América portuguesa, que demonstravam grande descontentamento por parte das elites locais.")
        ]
    },
    {
        "pos": 25, "materia": "História do Brasil", "dif": "MEDIO", "base": None,
        "enunc": "Considere as afirmações sobre a Revolta dos Malês, ocorrida em Salvador.\nI. Essa revolta contou com ampla participação de escravizados africanos e afrodescendentes, de diferentes procedências e crenças, que se insubordinaram em função de sua condição de vida.\nII. O termo malê provém de uma palavra de origem iorubá que significa muçulmano, e os escravizados que professavam essa crença lideraram o levante.\nIII. A revolta ocorreu durante o Primeiro Reinado e foi reprimida com extrema violência pelo Imperador, sendo derrotada em cerca de 24 horas, graças a uma denúncia notificando o planejamento da insurreição.\nIV. Irmandades de negros, a Igreja católica e profissionais liberais simpáticos à abolição apoiaram essa revolta, que se valeu da estratégia de provocar alguns incêndios para distrair a atenção das forças de segurança.\nSão corretas APENAS as afirmações",
        "gab": "A",
        "alts": [("A", "I e II."), ("B", "I e III."), ("C", "I, III e IV."), ("D", "II e IV."), ("E", "II e III.")]
    },
    {
        "pos": 26, "materia": "História do Brasil", "dif": "FACIL", "base": None,
        "enunc": "Dentre os Presidentes do Brasil que tomaram posse entre 1964 e 2019, foram eleitos por meio do voto direto popular, especificamente para esse cargo:",
        "gab": "B",
        "alts": [
            ("A", "Tancredo Neves, José Sarney, Itamar Franco, Fernando Collor, Fernando Henrique Cardoso, Luiz Inácio Lula da Silva (em duas eleições consecutivas), Dilma Roussef (em duas eleições consecutivas) e Jair Bolsonaro."),
            ("B", "Fernando Collor, Fernando Henrique Cardoso (em duas eleições consecutivas), Luiz Inácio Lula da Silva (em duas eleições consecutivas), Dilma Roussef (em duas eleições consecutivas) e Jair Bolsonaro."),
            ("C", "José Sarney, Fernando Collor, Itamar Franco, Fernando Henrique Cardoso, Luiz Inácio Lula da Silva (em duas eleições consecutivas), Dilma Roussef (em duas eleições consecutivas), Michel Temer, Jair Bolsonaro e Luiz Inácio Lula da Silva."),
            ("D", "Ulisses Guimarães, Tancredo Neves, Itamar Franco, Fernando Collor, Fernando Henrique Cardoso (em duas eleições consecutivas), Luiz Inácio Lula da Silva (em duas eleições consecutivas), Dilma Roussef e Jair Bolsonaro."),
            ("E", "João Figueiredo, Tancredo Neves, Fernando Collor, Fernando Henrique Cardoso (em duas eleições consecutivas), Luiz Inácio Lula da Silva (em duas eleições consecutivas), Dilma Roussef e Jair Bolsonaro.")
        ]
    },

    # Geografia do Brasil (Q27 a Q34)
    {
        "pos": 27, "materia": "Geografia do Brasil", "dif": "FACIL", "base": None,
        "enunc": "Leia os dois textos:\nI. São as áreas mais baixas e planas do relevo onde predominam os processos de sedimentação, já que recebem sedimentos oriundos de áreas mais elevadas.\nII. São áreas de médias e elevadas altitudes; as superfícies são irregulares e os processos de erosão são predominantes. É a forma predominante do relevo brasileiro.\nOs textos I e II definem, respectivamente,",
        "gab": "C",
        "alts": [("A", "chapadas e planícies."), ("B", "depressões e serras."), ("C", "planícies e planaltos."), ("D", "depressões e tabuleiros."), ("E", "chapadas e serras.")]
    },
    {
        "pos": 28, "materia": "Geografia do Brasil", "dif": "FACIL", "base": None,
        "enunc": "Segundo dados do Instituto Brasileiro de Geografia e Estatística (IBGE), em 1991 existiam 12 cidades com população superior a 1 milhão de habitantes. Em 2020, o número de cidades milionárias chegou a 17. Sobre esse crescimento observado entre 1991 e 2020 é correto afirmar que",
        "gab": "A",
        "alts": [
            ("A", "o dinamismo socioeconômico da sociedade brasileira se reflete, principalmente, nas grandes cidades."),
            ("B", "mais da metade da população brasileira passou a viver concentrada nessas 17 cidades."),
            ("C", "o forte crescimento vegetativo da população foi o fator responsável pelo crescimento urbano no país."),
            ("D", "o aumento do número de grandes cidades teve pouca influência sobre as densidades demográficas do país."),
            ("E", "as regiões Sudeste e Sul, as mais populosas, passaram a concentrar 15 das 17 cidades milionárias do país.")
        ]
    },
    {
        "pos": 29, "materia": "Geografia do Brasil", "dif": "MEDIO", "base": None,
        "enunc": "Considere o mapa e os textos a seguir sobre a Hidrografia da Bahia:\nI. O rio percorre cerca de 620 km até encontrar com as águas do Oceano Atlântico na cidade de Itacaré. Sua nascente é na Serra da Tromba na região central do estado. O baixo curso do rio atravessa a região conhecida como Costa do Cacau.\nII. É o maior rio genuinamente baiano. Este rio já foi a principal via de transporte e comunicação de toda a região da bacia, incluindo o Recôncavo Baiano. Com a construção de uma barragem, responsável pelo controle de suas cheias, ganhou mais uma utilização, a de responder por parte do abastecimento de água de todo o Recôncavo, Feira de Santana e da Grande Salvador.\nAs descrições I e II referem-se, respectivamente, aos rios indicados pelos números:",
        "gab": "D",
        "alts": [("A", "4 e 3."), ("B", "4 e 1."), ("C", "2 e 4."), ("D", "3 e 2."), ("E", "1 e 3.")]
    },
    {
        "pos": 30, "materia": "Geografia do Brasil", "dif": "FACIL", "base": None,
        "enunc": "Um levantamento do Instituto Brasileiro de Geografia e Estatística (IBGE), divulgado em 2021, apontou que, entre 2000 e 2018, a Bahia registrou, em números absolutos, o maior crescimento da área agrícola no Nordeste. Segundo o IBGE, durante os 18 anos, o território baiano destinado à agricultura cresceu 87,4%, passando de 16.808 para 31.490 km².\nO principal fator responsável pelo crescimento foi a",
        "gab": "E",
        "alts": [
            ("A", "introdução do cultivo de grãos no leste baiano."),
            ("B", "implantação de áreas vinícolas no vale do São Francisco."),
            ("C", "recuperação de áreas cacaueiras do sul do estado."),
            ("D", "instalação da pecuária leiteira nas áreas do cerrado."),
            ("E", "expansão da fronteira agrícola no oeste do estado.")
        ]
    },
    {
        "pos": 31, "materia": "Geografia do Brasil", "dif": "FACIL", "base": None,
        "enunc": "Em relação à matriz energética, a fonte de energia mais utilizada no Brasil é:",
        "gab": "B",
        "alts": [("A", "Derivados da cana-de-açúcar."), ("B", "Petróleo e seus derivados."), ("C", "Gás natural."), ("D", "Carvão Mineral."), ("E", "Eólica.")]
    },
    {
        "pos": 32, "materia": "Geografia do Brasil", "dif": "FACIL", "base": None,
        "enunc": "As brisas marítimas ou terrestres são correntes de ar que se originam nas regiões costeiras e têm duas direções possíveis: do mar para a areia (durante o dia) e da areia para o mar (à noite).\nAs duas direções possíveis das brisas ocorrem devido",
        "gab": "C",
        "alts": [
            ("A", "às extensas barreiras de corais do litoral brasileiro, que afetam a dinâmica dos ventos e das marés."),
            ("B", "ao elevado desmatamento da Mata Atlântica gerado no processo de urbanização brasileira."),
            ("C", "às diferenças de temperaturas entre a superfície terrestre e a superfície aquática."),
            ("D", "à proximidade do território brasileiro com a Zona de Convergência Intertropical."),
            ("E", "ao fato de o Brasil estar localizado à oeste do Meridiano de Greenwich e ser atravessado pelo Trópico de Capricórnio.")
        ]
    },
    {
        "pos": 33, "materia": "Geografia do Brasil", "dif": "FACIL", "base": None,
        "enunc": "Os dois textos descrevem problemas ambientais em biomas brasileiros.\nI. A agricultura, especialmente a cultura da soja, do milho e de vários cereais, assim como a pecuária têm sido responsáveis pela rápida devastação desse bioma. Estima-se que mais da metade de área originalmente ocupada pelo bioma já foi transformada para uso humano, num ritmo elevado de destruição.\nII. O difícil acesso à região protegeu-a de um grande impacto humano. Os maiores problemas são a pesca e caça predatória, o tráfico de animais silvestres e a poluição das águas dos rios que desaguam na região.\nOs textos fazem referência, respectivamente, aos biomas",
        "gab": "A",
        "alts": [("A", "Cerrado e Pantanal."), ("B", "Mata Atlântica e Floresta Amazônica."), ("C", "Caatinga e Campos Sulinos."), ("D", "Pantanal e Mata Atlântica."), ("E", "Floresta Amazônica e Cerrado.")]
    },
    {
        "pos": 34, "materia": "Geografia do Brasil", "dif": "FACIL", "base": None,
        "enunc": "Refere-se ao clima Tropical Semiárido quente o que se encontra em:",
        "gab": "D",
        "alts": [
            ("A", "Caracteriza-se por apresentar temperatura média do mês mais frio sempre superior a 18 °C, apresentando uma estação seca de pequena duração que é compensada pelos totais elevados de precipitação."),
            ("B", "Chuvas uniformemente distribuídas, sem estação seca, e a temperatura média do mês mais quente não chega a 22 °C. Precipitação de 1.100 a 2.000 mm."),
            ("C", "O total das chuvas do mês mais seco é superior a 60 mm, com precipitações maiores de março a agosto, ultrapassando o total de 1.500 mm anuais. Nos meses mais quentes (janeiro e fevereiro) a temperatura é de 24 a 25 °C."),
            ("D", "É caracterizado por escassez de chuvas e grande irregularidade em sua distribuição, baixa nebulosidade, índices elevados de evaporação e temperaturas médias elevadas."),
            ("E", "Apresenta estação chuvosa no verão e nítida estação seca no inverno. A temperatura média do mês mais frio é superior a 18 °C. As precipitações são superiores a 750 mm anuais, atingindo 1800 mm.")
        ]
    },

    # Atualidades (Q35 a Q42)
    {
        "pos": 35, "materia": "Atualidades", "dif": "FACIL", "base": None,
        "enunc": "Robin West tem 17 anos de idade e é uma pessoa diferente das demais − ela não tem um smartphone (telefone inteligente). Em vez de rolar a tela em aplicativos como TikTok e Instagram o dia inteiro, ela usa o chamado “telefone burro”.\nSobre o “telefone burro” é correto afirmar:",
        "gab": "C",
        "alts": [
            ("A", "Foi projetado para aprimorar o uso do e-mail como comunicação oficial no mundo do trabalho."),
            ("B", "Contém apenas a função de efetuar e receber ligações, tanto nacionais como internacionais."),
            ("C", "É aparelho similar a alguns dos primeiros telefones celulares do final da década de 1990."),
            ("D", "É obrigatório para reuniões e chamadas de vídeo embora não possa receber mensagens por SMS."),
            ("E", "Funciona apenas para recebimento e compartilhamento de notícias publicadas em agências institucionais.")
        ]
    },
    {
        "pos": 36, "materia": "Atualidades", "dif": "FACIL", "base": None,
        "enunc": "Um dia histórico para o mundo da música. A cantora conquistou o Grammy Latino de “Melhor Álbum de Música Popular Brasileira” nesta quinta-feira (17.11) e se tornou a primeira artista assumidamente trans a levar esse prêmio. Ao ter seu nome revelado na cerimônia, que acontece em Las Vegas, todos os convidados a aplaudiram de pé.\nA notícia trata do prêmio dado à cantora",
        "gab": "B",
        "alts": [("A", "Pabllo Vittar."), ("B", "Liniker."), ("C", "Linn da Quebrada."), ("D", "Aretuza Lovi."), ("E", "Gloria Groove.")]
    },
    {
        "pos": 37, "materia": "Atualidades", "dif": "FACIL", "base": None,
        "enunc": "Recentemente o empresário Elon Musk comprou a rede social Twitter, uma das plataformas de comunicação mais acessadas no planeta. Uma das primeiras ações do novo proprietário foi a",
        "gab": "D",
        "alts": [
            ("A", "proibição de manifestações político-partidárias na plataforma em anos de eleições nacionais."),
            ("B", "mudança da sede do Twitter, de São Francisco, nos Estados Unidos, para Londres, na Inglaterra."),
            ("C", "criação de uma nova rede social, a partir da fusão do Twitter com o Instagram e o Facebook."),
            ("D", "demissão de boa parte dos funcionários, incluindo vários executivos do alto escalão."),
            ("E", "liberação de postagens que fazem apologia a crimes de ódio, desde que devidamente identificadas.")
        ]
    },
    {
        "pos": 38, "materia": "Atualidades", "dif": "FACIL", "base": None,
        "enunc": "Apesar de ser um evento que abarca diversos países e culturas do planeta, a Copa do Mundo de Futebol Masculino de 2022, realizada no Catar, tem gerado polêmicas entre jogadores e organização do torneio. Uma das principais polêmicas se refere",
        "gab": "E",
        "alts": [
            ("A", "à liberação de roupas e hábitos de consumo ocidentais em um país com costumes distintos como o Catar."),
            ("B", "às manifestações de ex-colônias europeias que reivindicam reparação histórica pela exploração ocorrida."),
            ("C", "aos pedidos por equiparação salarial de jogadores profissionais em todas as ligas do planeta."),
            ("D", "às reclamações sobre patrocinadores que não seguem padrões internacionais de condições e leis trabalhistas."),
            ("E", "à proibição do uso do símbolo One Love em uniformes ou braçadeiras dos capitães de equipes.")
        ]
    },
    {
        "pos": 39, "materia": "Atualidades", "dif": "FACIL", "base": None,
        "enunc": "O Parque de Exposições, em Salvador, será palco do evento, considerado o maior festival de cultura negra do mundo. Para os organizadores, esta segunda edição tem um ‘gosto de primeira vez’, já que será 100% presencial na cidade mais negra fora da África, a capital baiana, Salvador.\nA notícia anuncia a realização do evento:",
        "gab": "C",
        "alts": [("A", "Samba do Nordeste."), ("B", "Carnaval na Primavera."), ("C", "Afropunk Bahia."), ("D", "Lollapalooza."), ("E", "Rock in Salvador.")]
    },
    {
        "pos": 40, "materia": "Atualidades", "dif": "FACIL", "base": None,
        "enunc": "A grave crise humanitária que se abate sobre o país asiático provocou um novo fluxo migratório de afegãos para diversas partes do mundo, inclusive o Brasil, que também tem recebido muitos refugiados.\nEm relação à atual situação dos refugiados no planeta, está correto o que se afirma em:",
        "gab": "A",
        "alts": [
            ("A", "Pesadas medidas de restrição na Europa têm aumentado o fluxo de refugiados para países emergentes do Sul."),
            ("B", "Índia e Estados Unidos aparecem como os principais destinos de refugiados oriundos do continente africano."),
            ("C", "A China tem o maior contingente de evasão de refugiados devido ao alto desemprego e perseguições políticas."),
            ("D", "O Canadá tem, desde 2020, suas fronteiras abertas para os mexicanos no intuito de estimular o crescimento demográfico canadense."),
            ("E", "Têm diminuído os movimentos migratórios em nível mundial.")
        ]
    },
    {
        "pos": 41, "materia": "Atualidades", "dif": "FACIL", "base": None,
        "enunc": "No contexto da globalização o comércio internacional é fundamental para a economia de um país. No caso do Brasil, dois de seus principais parceiros comerciais são",
        "gab": "D",
        "alts": [("A", "México e Colômbia."), ("B", "Austrália e Canadá."), ("C", "França e Japão."), ("D", "Argentina e China."), ("E", "Uruguai e África do Sul.")]
    },
    {
        "pos": 42, "materia": "Atualidades", "dif": "FACIL", "base": None,
        "enunc": "A partir de 2020 teve início a expansão de Covid-19 por todos os continentes. Recentemente, a varíola dos macacos (Monkeypox) passou a ser diagnosticada em diferentes países do mundo. Novas epidemias podem surgir e se difundir. Esta situação ocorre devido",
        "gab": "E",
        "alts": [
            ("A", "ao pequeno avanço da medicina, mesmo nos países desenvolvidos."),
            ("B", "ao grande número de habitantes do mundo, que, atualmente, conta com 8 milhões de pessoas."),
            ("C", "à deficiente rede de comunicações entre os países mais pobres."),
            ("D", "às diferenças econômicas, pois a população dos países ricos não é atingida pelas pandemias."),
            ("E", "à globalização, que facilita a movimentação das pessoas pelo mundo.")
        ]
    },

    # Informática (Q43 a Q50)
    {
        "pos": 43, "materia": "Informática", "dif": "FACIL", "base": None,
        "enunc": "Na ferramenta Impress do LibreOffice 7.4.2, em português, para definir o plano de fundo e outras características de todos os slides na apresentação é necessário criar um slide com um conjunto específico de características que atuam como um modelo que é utilizado como o ponto inicial para criar outros slides. Este slide é chamado de",
        "gab": "B",
        "alts": [("A", "Design Pattern."), ("B", "Slide Mestre."), ("C", "Frame Default."), ("D", "Head Slide."), ("E", "Slide Base.")]
    },
    {
        "pos": 44, "materia": "Informática", "dif": "FACIL", "base": None,
        "enunc": "Na ferramenta Calc do LibreOffice 7.4.2, em português, um usuário possui na célula A1 os valores 1,2,3,4,5 e deseja separar automaticamente esses números, colocando o número 1 na célula A1, 2 na célula B1, 3 na célula C1, 4 na célula D1 e 5 na célula E1. Após selecionar a célula A1, este usuário conseguirá fazer essa distribuição, a partir de configurações que aparecerão na janela que será exibida após clicar no menu",
        "gab": "C",
        "alts": [("A", "Dados e na opção Classificar"), ("B", "Ferramentas e na opção Atingir Meta"), ("C", "Dados e na opção Texto para colunas..."), ("D", "Ferramentas e na opção Fragmentar"), ("E", "Editar e na opção Separar valores...")]
    },
    {
        "pos": 45, "materia": "Informática", "dif": "FACIL", "base": None,
        "enunc": "Na ferramenta Writer do LibreOffice 7.4.2, em português, é possível criar uma lista de elementos dispostos em vários níveis. Após criar uma lista, um usuário escreveu o elemento de primeiro nível em uma linha e pressionou a tecla Enter. Na nova linha, para avançar para o próximo nível (segundo nível) da lista este usuário deverá pressionar",
        "gab": "D",
        "alts": [("A", "Shift + Tab."), ("B", "Insert ou Ins."), ("C", "F2."), ("D", "Tab."), ("E", "Alt + Tab.")]
    },
    {
        "pos": 46, "materia": "Informática", "dif": "FACIL", "base": None,
        "enunc": "Um policial está utilizando um computador com o Windows 10 em português, e, após abrir um software, a janela congelou, indicando que o software parou de responder, mas outros recursos continuam acessíveis. Ao fazer contato com o suporte, foi orientado a encerrar o processo do software na memória, por meio da opção Finalizar Tarefa do Gerenciador de Tarefas do Windows. Rapidamente o policial lembrou-se que o Gerenciador de Tarefas pode ser acessado após",
        "gab": "E",
        "alts": [
            ("A", "pressionar simultaneamente a tecla que contém o símbolo do Windows e a tecla T."),
            ("B", "clicar no botão Iniciar, depois na opção Configurações e, por último, na opção Gerenciador de Processos."),
            ("C", "pressionar a tecla F11 ou a partir da opção Gerenciador de Processos do Painel de Controle."),
            ("D", "clicar com o botão direito do mouse no botão Iniciar e depois, com o botão esquerdo do mouse, na opção Gerenciador de Dispositivos."),
            ("E", "pressionar simultaneamente as teclas CTRL ALT DEL ou CTRL ALT DELETE.")
        ]
    },
    {
        "pos": 47, "materia": "Informática", "dif": "FACIL", "base": None,
        "enunc": "Utilizando o Excel da suíte de aplicativos do Office 365, em português, um policial precisa dividir a soma do intervalo de células de A3 até A6 pela média do intervalo de células de B3 até B6. Na célula que vai receber o resultado, deve utilizar a fórmula:",
        "gab": "B",
        "alts": [
            ("A", "=SOMA(A3,A6)/MÉDIA(B3,B6)"),
            ("B", "=SOMA(A3:A6)/MÉDIA(B3:B6)"),
            ("C", "=SOMA(A3..A6)/MÉDIA(B3..B6)"),
            ("D", "=SOMA(A3+A4+A5+A6)/MÉDIA(B3+B4+B5+B6)"),
            ("E", "=SOMA(A3;A6)/MÉDIA(B3;B6)")
        ]
    },
    {
        "pos": 48, "materia": "Informática", "dif": "FACIL", "base": None,
        "enunc": "Para criar, em um terminal Linux, uma pasta chamada polmil, um policial deverá digitar a instrução",
        "gab": "A",
        "alts": [("A", "mkdir polmil"), ("B", "md polmil"), ("C", "create folder polmil"), ("D", "cf polmil"), ("E", "cd polmil")]
    },
    {
        "pos": 49, "materia": "Informática", "dif": "FACIL", "base": None,
        "enunc": "Imediatamente após salvar um documento no Microsoft Word, um policial pressionou simultaneamente as teclas ALT F4 para",
        "gab": "C",
        "alts": [
            ("A", "maximizar a janela do Microsoft Word."),
            ("B", "alternar para a janela de outra ferramenta aberta."),
            ("C", "fechar o arquivo e a janela do Microsoft Word."),
            ("D", "fechar o arquivo, mantendo a janela do Microsoft Word aberta."),
            ("E", "minimizar a janela do Microsoft Word.")
        ]
    },
    {
        "pos": 50, "materia": "Informática", "dif": "FACIL", "base": None,
        "enunc": "No prompt de comandos do Windows 10, um policial digitou o comando ipconfig e pressionou a tecla Enter para",
        "gab": "B",
        "alts": [
            ("A", "mudar o endereço IP do seu computador."),
            ("B", "ver o endereço IP do seu computador na rede."),
            ("C", "renovar o endereço IP do seu computador."),
            ("D", "conectar seu computador à rede local."),
            ("E", "obter seu endereço IP público na internet.")
        ]
    },

    # Direito Constitucional (Q51 a Q55)
    {
        "pos": 51, "materia": "Direito Constitucional", "dif": "FACIL", "base": None,
        "enunc": "Nos termos da Constituição Federal, constitui um dos objetivos fundamentais da República Federativa do Brasil",
        "gab": "E",
        "alts": [
            ("A", "erradicar as desigualdades sociais e regionais."),
            ("B", "reduzir a pobreza e a marginalização."),
            ("C", "garantir o desenvolvimento nacional e internacional."),
            ("D", "assegurar a cooperação entre os povos para o progresso da humanidade."),
            ("E", "construir uma sociedade livre, justa e solidária.")
        ]
    },
    {
        "pos": 52, "materia": "Direito Constitucional", "dif": "FACIL", "base": None,
        "enunc": "De acordo com a Constituição Federal, são órgãos responsáveis pela segurança pública, dentre outros,",
        "gab": "B",
        "alts": [
            ("A", "polícias penais estaduais e municipais e polícia federal."),
            ("B", "polícias militares e corpos de bombeiros militares."),
            ("C", "seguranças de empresas privadas e polícia ferroviária federal."),
            ("D", "polícia ferroviária federal e polícias penais estaduais e municipais."),
            ("E", "corpos de bombeiros civis e polícias militares.")
        ]
    },
    {
        "pos": 53, "materia": "Direito Constitucional", "dif": "FACIL", "base": None,
        "enunc": "Virgulino tem uma dívida civil vencida de R$ 5.000,00 e está com receio de ser preso, caso não faça a respectiva quitação. Após consulta a um advogado, o profissional respondeu a ele que, nos termos da Constituição Federal, é",
        "gab": "D",
        "alts": [
            ("A", "vedada a prisão civil por dívida, desde que de valores inferiores a R$ 10.000,00."),
            ("B", "permitida a prisão civil por dívida, desde que de valores superiores R$ 3.000,00."),
            ("C", "vedada a prisão civil por dívida, em qualquer hipótese e valor."),
            ("D", "permitida a prisão civil por dívida, do responsável pelo pagamento de obrigação alimentícia, se o inadimplemento decorre de ato voluntário e inescusável do devedor."),
            ("E", "permitida a prisão civil por dívida, do responsável pelo pagamento de obrigação alimentícia, ainda que o inadimplemento decorra de ato involuntário e escusável do devedor.")
        ]
    },
    {
        "pos": 54, "materia": "Direito Constitucional", "dif": "FACIL", "base": None,
        "enunc": "Nos termos da Constituição Federal, a Administração Pública é regida, dentre outros, pelos princípios da",
        "gab": "C",
        "alts": [
            ("A", "tipicidade, legalidade e impessoalidade."),
            ("B", "autoexecutoriedade, moralidade e impessoalidade."),
            ("C", "moralidade, publicidade e eficiência."),
            ("D", "eficiência, imperatividade e legalidade."),
            ("E", "impessoalidade, moralidade e autoexecutoriedade.")
        ]
    },
    {
        "pos": 55, "materia": "Direito Constitucional", "dif": "MEDIO", "base": None,
        "enunc": "O Conselho de Defesa Nacional, constituindo-se em um órgão de consulta do Presidente da República, segundo a Constituição Federal, é integrado, na qualidade de membros natos, dentre outros, por",
        "gab": "T",
        "alts": [
            ("A", "Vice-Presidente da República e Ministro da Justiça."),
            ("B", "líderes da maioria no Senado Federal e Governadores de Estado."),
            ("C", "Vice-Governadores de Estado e Vice-Presidente da República."),
            ("D", "líderes da maioria no Senado Federal e Governadores de Estado."),
            ("E", "Presidente do Senado Federal e Prefeitos das Capitais.")
        ]
    },

    # Direitos Humanos (Q56 a Q60)
    {
        "pos": 56, "materia": "Direitos Humanos", "dif": "FACIL", "base": None,
        "enunc": "Nos termos da Declaração Universal dos Direitos Humanos, de 1948,",
        "gab": "D",
        "alts": [
            ("A", "todo ser humano tem capacidade para gozar os direitos e as liberdades estabelecidos na Declaração, sem distinção, salvo se fundada na condição política, jurídica ou internacional do país ou território a que pertença a pessoa."),
            ("B", "ninguém será submetido à tortura, nem a tratamento ou castigo cruel, desumano ou degradante, salvo em período de guerra declarada de acordo com as leis de caráter nacional e internacional."),
            ("C", "todo ser humano, vítima de perseguição, tem o direito de procurar e de gozar asilo em outros países, ainda que a perseguição seja motivada por crimes de direito comum ou por atos contrários aos objetivos e princípios das Nações Unidas."),
            ("D", "ninguém será mantido em escravidão ou servidão, sendo a escravidão e o tráfico de escravos proibidos em todas as suas formas."),
            ("E", "ninguém poderá ser culpado por ação ou omissão que, no momento, não constituíam delito, admitindo-se apenas a imposição de pena mais grave do que aquela que, no momento da prática, era aplicável ao ato delituoso, se previsto em norma de direito internacional.")
        ]
    },
    {
        "pos": 57, "materia": "Direitos Humanos", "dif": "MEDIO", "base": None,
        "enunc": "A Constituição brasileira estabelece que é dever da família, da sociedade e do Estado, em relação à criança, ao adolescente e ao jovem, colocá-los a salvo de toda forma de negligência, discriminação, exploração, violência, crueldade e opressão. Entre outras regras consagradas em tratados e convenções internacionais de que o Estado brasileiro é partícipe, referida norma constitucional guarda relação com previsão contida na Convenção Americana sobre Direitos Humanos (Pacto de San José da Costa Rica, de 1969), segundo a qual",
        "gab": "A",
        "alts": [
            ("A", "toda criança tem direito às medidas de proteção que a sua condição de menor requer por parte da sua família, da sociedade e do Estado."),
            ("B", "a criança e o adolescente gozam de todos os direitos fundamentais inerentes à pessoa humana, autorizada sua suspensão apenas em caso de guerra, de perigo público ou outra emergência que ameace a segurança do Estado."),
            ("C", "ninguém deve ser constrangido a executar trabalho forçado ou obrigatório, sendo proibido o cumprimento de pena dessa natureza, ainda que o país a prescreva e que seja imposta por juiz ou tribunal competente."),
            ("D", "a infância tem direito a cuidados e assistência especiais, devendo todas as crianças, nascidas dentro ou fora do matrimônio, gozar da mesma proteção social."),
            ("E", "devem ser concedidas à família as mais amplas proteção e assistência possíveis, especialmente para a sua constituição e enquanto for responsável pela criação e educação dos filhos.")
        ]
    },
    {
        "pos": 58, "materia": "Direitos Humanos", "dif": "MEDIO", "base": None,
        "enunc": "Ao dispor sobre os direitos de circulação e residência, a Convenção Americana sobre Direitos Humanos (Pacto de San José da Costa Rica, de 1969) estabelece que",
        "gab": "B",
        "alts": [
            ("A", "a expulsão de estrangeiro que se ache legalmente no território de Estado-Parte na Convenção deve se dar mediante decisão adotada conforme a lei, somente sendo admitida a expulsão coletiva de estrangeiros nos casos de risco à integridade do território ou à segurança nacional."),
            ("B", "o exercício desses direitos pode ser restringido, em virtude de lei, na medida indispensável, numa sociedade democrática, para, entre outras finalidades, proteger a moral ou a saúde públicas, ou os direitos e liberdades das demais pessoas."),
            ("C", "toda pessoa tem o direito de sair livremente de qualquer país, exceto do próprio, em que o exercício desse direito pode ser restringido, por decisão da autoridade administrativa, em zonas determinadas, por motivo de interesse público."),
            ("D", "toda pessoa tem o direito de buscar e receber asilo em território estrangeiro, em caso de perseguição por delitos políticos ou comuns conexos com delitos políticos, independentemente da legislação de cada Estado."),
            ("E", "o estrangeiro não pode ser entregue a outro país, onde seu direito à vida ou à liberdade pessoal esteja em risco de violação por causa da sua raça, nacionalidade, religião, condição social ou de suas opiniões políticas, exceto se se tratar de seu país de origem.")
        ]
    },
    {
        "pos": 59, "materia": "Direitos Humanos", "dif": "MEDIO", "base": None,
        "enunc": "Relativamente à educação e à cultura, de acordo com o Pacto Internacional dos Direitos Econômicos, Sociais e Culturais, os Estados Parte reconhecem que\nI. a educação deverá capacitar todas as pessoas a participar efetivamente de uma sociedade livre, favorecer a compreensão, a tolerância e a amizade entre todas as nações e entre todos os grupos raciais, étnicos ou religiosos.\nII. cada indivíduo tem o direito de participar da vida cultural, de desfrutar o processo científico e suas aplicações, e de beneficiar-se da proteção dos interesses morais e materiais decorrentes de toda a produção científica, literária ou artística de que seja autor.\nIII. indivíduos e entidades têm liberdade de criar e dirigir instituições de ensino, desde que respeitados os princípios estabelecidos no Pacto e que essas instituições observem os padrões mínimos prescritos pelo Estado.\nEstá correto o que se afirma em",
        "gab": "C",
        "alts": [("A", "I e II, apenas."), ("B", "II e III, apenas."), ("C", "I, II e III."), ("D", "I, apenas."), ("E", "III, apenas.")]
    },
    {
        "pos": 60, "materia": "Direitos Humanos", "dif": "MEDIO", "base": None,
        "enunc": "Considere os seguintes compromissos, extraídos de instrumentos internacionais de proteção dos direitos humanos, dos quais a República Federativa do Brasil é signatária:\nI. Encorajar os homens a participar plenamente de todas as ações orientadas à busca da igualdade.\nII. Promover um desenvolvimento sustentado centrado na pessoa, incluindo o crescimento econômico sustentado através da educação básica, educação durante toda a vida, alfabetização e capacitação e atenção primária à saúde das meninas e das mulheres.\nIII. Assegurar um salário equitativo e uma remuneração igual por um trabalho de igual valor, sem qualquer distinção; em particular, as mulheres deverão ter a garantia de condições de trabalho não inferiores às dos homens e perceber a mesma remuneração que eles por trabalho igual.\nReferidos compromissos integram:",
        "gab": "E",
        "alts": [
            ("A", "I, II e III, a Declaração de Pequim Adotada pela Quarta Conferência Mundial sobre as Mulheres."),
            ("B", "I, o Pacto Internacional dos Direitos Econômicos, Sociais e Culturais, II e III, a Declaração Universal dos Direitos Humanos."),
            ("C", "I, a Declaração Universal dos Direitos Humanos, II Convenção Americana sobre Direitos Humano; e III, a Declaração de Pequim Adotada pela Quarta Conferência Mundial sobre as Mulheres."),
            ("D", "I, II e III, a Convenção Americana sobre Direitos Humanos."),
            ("E", "I e II, a Declaração de Pequim Adotada pela Quarta Conferência Mundial sobre as Mulheres; e III, o Pacto Internacional dos Direitos Econômicos, Sociais e Culturais.")
        ]
    },

    # Direito Administrativo (Q61 a Q65)
    {
        "pos": 61, "materia": "Direito Administrativo", "dif": "FACIL", "base": None,
        "enunc": "No exercício de suas atividades, a Administração Pública",
        "gab": "C",
        "alts": [
            ("A", "não tem como objetivo trabalhar em favor da cultura, de uma maneira geral, por se tratar de manifestação estritamente privada, desprovida de interesse público."),
            ("B", "tem como objetivo apenas a prestação de segurança pública à coletividade, tendo os agentes públicos plenos poderes para atingir os seus fins."),
            ("C", "tem como objetivo trabalhar a favor do interesse público, por meio da prestação de serviços públicos e fomento de iniciativas de utilidade pública, dentre outros."),
            ("D", "tem como objetivo restringir-se à forma centralizada e concentrada de atribuição de competências, pois somente o Poder Executivo é competente para a prestação de serviço de qualidade ao administrado."),
            ("E", "tem como objetivo a observância pelo administrador dos usos e costumes da região administrada, ainda que a vontade da lei fixe finalidade a ser perseguida de modo diverso.")
        ]
    },
    {
        "pos": 62, "materia": "Direito Administrativo", "dif": "FACIL", "base": None,
        "enunc": "Relativamente ao poder de polícia da Administração Pública,",
        "gab": "E",
        "alts": [
            ("A", "a polícia administrativa deve atuar preventiva e repressivamente quando há ilícito penal."),
            ("B", "cabe à polícia judiciária proibir o porte de arma de fogo ou a direção de veículos automotores."),
            ("C", "restringe-se a sua atuação ao âmbito da polícia judiciária, sendo vedado o seu exercício em se tratando de polícia administrativa."),
            ("D", "é a atividade do Estado consistente em limitar o exercício do interesse público em detrimento dos direitos individuais do cidadão."),
            ("E", "é a atividade do Estado por meio da qual se limita ou disciplina o exercício de direitos em benefício do interesse público.")
        ]
    },
    {
        "pos": 63, "materia": "Direito Administrativo", "dif": "FACIL", "base": None,
        "enunc": "Em virtude do princípio constitucional da legalidade que rege a Administração Pública,",
        "gab": "B",
        "alts": [
            ("A", "ao administrador faculta-se atuar sem previsão legal, pautando-se apenas pela sua vontade pessoal."),
            ("B", "age licitamente o administrador que atuar em conformidade com o que estiver previsto no ordenamento jurídico."),
            ("C", "o interesse do particular se sobrepõe ao interesse da Administração quando contrariá-lo."),
            ("D", "pode o administrador emitir, em benefício pessoal, orientação colidente com aquela estabelecida previamente no ordenamento jurídico, mediante justificativa expressa, em processo administrativo."),
            ("E", "a apuração e avaliação da conduta do agente público será delegada ao particular, pois este detém maior capacidade técnica.")
        ]
    },
    {
        "pos": 64, "materia": "Direito Administrativo", "dif": "FACIL", "base": None,
        "enunc": "Na hipótese de o administrador público praticar conduta fora dos limites da lei, expressa ou implicitamente, produzindo resultado ilegítimo, haverá",
        "gab": "D",
        "alts": [
            ("A", "exercício regular de direito."),
            ("B", "aplicação regular de prerrogativa."),
            ("C", "uso do poder-dever ínsito ao agente público."),
            ("D", "abuso de poder."),
            ("E", "utilização do direito administrativo de agir.")
        ]
    },
    {
        "pos": 65, "materia": "Direito Administrativo", "dif": "FACIL", "base": None,
        "enunc": "Nos termos do Estatuto dos Policiais Militares do Estado da Bahia (Lei Estadual nº 7.990/2001), são formas de provimento do cargo de policial militar:",
        "gab": "A",
        "alts": [
            ("A", "nomeação e reintegração."),
            ("B", "nomeação e remoção."),
            ("C", "remoção e reintegração."),
            ("D", "reintegração e transferência."),
            ("E", "transferência e nomeação.")
        ]
    },

    # Direito Penal (Q66 a Q70)
    {
        "pos": 66, "materia": "Direito Penal", "dif": "MEDIO", "base": None,
        "enunc": "Pedro e Paulo praticaram crime de furto em concurso de pessoas, tendo o delito chegado ao conhecimento das autoridades. Após o oferecimento da denúncia pelo Ministério Público, Pedro, sem o conhecimento de Paulo, restituiu o objeto furtado. O juiz da comarca ainda não analisou a denúncia. Diante da situação hipotética acima mencionada,",
        "gab": "C",
        "alts": [
            ("A", "Pedro e Paulo não terão qualquer benefício, pois a restituição se deu após a denúncia."),
            ("B", "somente Pedro fará jus à causa de diminuição relativa ao arrependimento posterior."),
            ("C", "Pedro e Paulo fazem jus à causa de diminuição relativa ao arrependimento posterior."),
            ("D", "Pedro e Paulo fazem jus ao benefício de redução da pena relativa à desistência eficaz."),
            ("E", "somente Pedro fará jus à causa de diminuição relativa à desistência eficaz.")
        ]
    },
    {
        "pos": 67, "materia": "Direito Penal", "dif": "MEDIO", "base": None,
        "enunc": "Adriano, soldado da polícia militar, sacava uma certa quantia em dinheiro no caixa eletrônico existente em uma praça do município, ocasião em que foi abordado por Flávio que, fazendo uso de um estilete, anunciou o assalto, subtraindo o valor sacado por Adriano naquele instante. Na sequência, Flávio foge do local em sua bicicleta, ocasião em que Adriano, armado de um revólver, passa a persegui-lo, localizando-o, aproximadamente, uma hora depois dos fatos, há três quilômetros do local, quando então efetua um disparo contra Flávio que, ferido, cai de sua bicicleta, vindo a falecer no local. Diante da situação acima descrita, Adriano",
        "gab": "B",
        "alts": [
            ("A", "deverá responder pelo excesso, embora tenha agido em legítima defesa."),
            ("B", "praticou crime de homicídio doloso contra Flávio."),
            ("C", "ficará isento de pena diante da inexigibilidade de conduta diversa."),
            ("D", "estará acobertado pela excludente da legítima defesa."),
            ("E", "ficará isento de pena por ter agido em estrito cumprimento de um dever legal.")
        ]
    },
    {
        "pos": 68, "materia": "Direito Penal", "dif": "MEDIO", "base": None,
        "enunc": "Analise as assertivas abaixo:\nI. O cumprimento da pena do crime de tortura se dará integralmente em regime fechado, vedando-se a progressão.\nII. A condenação no crime de tortura acarretará a perda do cargo, função ou emprego público e a interdição para seu exercício pelo dobro do prazo da pena aplicada.\nIII. O crime de tortura é inafiançável e insuscetível de graça ou anistia.\nIV. Aumenta-se a pena do crime de tortura até o dobro se ele for cometido mediante sequestro.\nDe acordo com o que estabelece a Lei nº 9.455/1997, que define os crimes de tortura e dá outras providências, está correto APENAS o que se afirma em",
        "gab": "E",
        "alts": [("A", "I, III e IV."), ("B", "I e IV."), ("C", "I e III."), ("D", "II e IV."), ("E", "II e III.")]
    },
    {
        "pos": 69, "materia": "Direito Penal", "dif": "FACIL", "base": None,
        "enunc": "Arthur mantinha um estabelecimento no centro da cidade onde explorava a prática ilegal de jogos de azar. Tomando ciência desse fato, os policiais civis Bruno e Cândido dirigiram-se até o local, ocasião em que lhes foi oferecida, por parte de Arthur, determinada quantia em dinheiro para que não fossem apreendidos os equipamentos de jogo ilegal, o que foi por eles prontamente aceito. Diante da situação hipotética acima mencionada,",
        "gab": "C",
        "alts": [
            ("A", "todos os envolvidos praticaram o crime de corrupção ativa."),
            ("B", "Arthur praticou o crime de corrupção passiva, enquanto Bruno e Cândido praticaram o crime de corrupção ativa."),
            ("C", "Arthur praticou o crime de corrupção ativa, enquanto Bruno e Cândido praticaram o crime de corrupção passiva."),
            ("D", "todos os envolvidos praticaram o crime de corrupção passiva."),
            ("E", "a conduta de Arthur somente será enquadrada como contravenção pela prática de jogos de azar, enquanto a dos policiais será tipificada como corrupção ativa.")
        ]
    },
    {
        "pos": 70, "materia": "Direito Penal", "dif": "FACIL", "base": None,
        "enunc": "Marina pedalava sua bicicleta em via pública, ocasião em que Carlos, pilotando sua motocicleta no mesmo local, aproximou-se da ciclista. Aproveitando-se da distração de Marina, Carlos passou sua mão nas nádegas da vítima, empreendendo, na sequência, fuga do local. Diante da situação hipotética acima mencionada, Carlos praticou em tese o crime de",
        "gab": "A",
        "alts": [
            ("A", "importunação sexual."),
            ("B", "assédio sexual."),
            ("C", "tentativa de estupro."),
            ("D", "estupro consumado."),
            ("E", "estupro privilegiado.")
        ]
    },

    # Igualdade Racial e de Gênero (Q71 a Q75)
    {
        "pos": 71, "materia": "Igualdade Racial e de Gênero", "dif": "FACIL", "base": None,
        "enunc": "De acordo com o Estatuto de Igualdade Racial, o estudo da história geral da África e da história da população negra no Brasil é",
        "gab": "C",
        "alts": [
            ("A", "obrigatório somente nos estabelecimentos de ensino fundamental e de ensino médio públicos."),
            ("B", "facultativo nos estabelecimentos de ensino fundamental e de ensino médio, públicos e privados."),
            ("C", "obrigatório nos estabelecimentos de ensino fundamental e de ensino médio, públicos e privados."),
            ("D", "facultativo somente nos estabelecimentos de ensino fundamental e de ensino médio privados."),
            ("E", "obrigatório somente nos estabelecimentos de ensino médio públicos e privados.")
        ]
    },
    {
        "pos": 72, "materia": "Igualdade Racial e de Gênero", "dif": "MEDIO", "base": None,
        "enunc": "Sobre a inquirição da mulher em situação de violência doméstica e familiar, avalie as assertivas abaixo:\nI. O depoimento não poderá ser registrado em meio eletrônico ou magnético.\nII. A mulher em situação de violência doméstica e familiar poderá ser inquirida sucessivas vezes sobre o mesmo fato nos âmbitos criminal, cível e administrativo, bem como ser questionada sobre a vida privada.\nIII. Deve-se garantir que, em nenhuma hipótese, a mulher em situação de violência doméstica e familiar terá contato direto com investigados ou suspeitos e pessoas a eles relacionadas.\nEstá correto o que consta APENAS de",
        "gab": "B",
        "alts": [("A", "I."), ("B", "III."), ("C", "II."), ("D", "I e III."), ("E", "I e II.")]
    },
    {
        "pos": 73, "materia": "Igualdade Racial e de Gênero", "dif": "FACIL", "base": None,
        "enunc": "É considerado afiançável o crime de",
        "gab": "D",
        "alts": [
            ("A", "tortura."),
            ("B", "racismo."),
            ("C", "tráfico de entorpecentes."),
            ("D", "ameaça no âmbito de violência doméstica e familiar contra a mulher."),
            ("E", "ação de grupos armados, civis ou militares, contra a ordem constitucional e o Estado Democrático.")
        ]
    },
    {
        "pos": 74, "materia": "Igualdade Racial e de Gênero", "dif": "MEDIO", "base": None,
        "enunc": "De acordo com a Convenção sobre a Eliminação de Todas as Formas de Discriminação contra a Mulher, os Estados Partes se comprometem a\nI. tomar as medidas apropriadas para eliminar a discriminação contra a mulher praticada por qualquer pessoa ou órgãos públicos, mas não em relação às empresas.\nII. adotar todas as medidas adequadas, inclusive de caráter legislativo, para modificar ou derrogar leis, regulamentos, usos e práticas que constituam discriminação contra a mulher.\nIII. derrogar todas as disposições penais nacionais que constituam discriminação contra a mulher.\nEstá correto o que consta em",
        "gab": "E",
        "alts": [("A", "III, apenas."), ("B", "I e II, apenas."), ("C", "I e III apenas."), ("D", "I, II e III."), ("E", "II e III, apenas.")]
    },
    {
        "pos": 75, "materia": "Igualdade Racial e de Gênero", "dif": "FACIL", "base": None,
        "enunc": "São objetivos fundamentais da República Federativa do Brasil:\nI. promover o bem de todos, sem preconceitos de origem, raça, sexo, cor, idade e quaisquer outras formas de discriminação.\nII. permitir a livre manifestação do pensamento, sendo permitido o anonimato.\nIII. erradicar a pobreza e a marginalização e reduzir as desigualdades sociais e regionais.\nEstá correto o que consta de",
        "gab": "A",
        "alts": [("A", "I e III, apenas"), ("B", "II e III, apenas."), ("C", "I, apenas"), ("D", "II, apenas."), ("E", "I, II e III.")]
    },

    # Direito Penal Militar (Q76 a Q80)
    {
        "pos": 76, "materia": "Direito Penal Militar", "dif": "MEDIO", "base": None,
        "enunc": "De acordo com o que estabelece o Código Penal Militar sobre o crime de violência contra superior (art. 157),",
        "gab": "D",
        "alts": [
            ("A", "se a violência é praticada com arma, a pena é aumentada de 1/6 a 1/3."),
            ("B", "a pena é aumentada da metade, se o crime ocorre em serviço."),
            ("C", "a pena é dobrada, se da violência resulta morte."),
            ("D", "se da violência resulta lesão corporal, aplica-se, além da pena da violência, a do crime contra a pessoa."),
            ("E", "se o superior é comandante da unidade a que pertence o agente, ou oficial general, a pena é aumentada da sexta parte.")
        ]
    },
    {
        "pos": 77, "materia": "Direito Penal Militar", "dif": "FACIL", "base": None,
        "enunc": "Opor-se à execução de ato legal, mediante ameaça ou violência ao executor, ou a quem esteja prestando auxílio, configura, nos termos do que dispõe o Código Penal Militar, o crime de",
        "gab": "A",
        "alts": [
            ("A", "Resistência mediante ameaça ou violência."),
            ("B", "Recusa de obediência."),
            ("C", "Oposição a ordem de sentinela."),
            ("D", "Descumprimento de missão."),
            ("E", "Motim, revolta ou conspiração.")
        ]
    },
    {
        "pos": 78, "materia": "Direito Penal Militar", "dif": "FACIL", "base": None,
        "enunc": "Emerson, policial militar, presenciou dois colegas da corporação, também militares, embriagados, deixando, em razão do sentimento de amizade que nutria por eles, de comunicar tal fato ao seu superior. Agindo dessa forma, Emerson, em tese, praticou",
        "gab": "E",
        "alts": [
            ("A", "o crime de desrespeito a superior."),
            ("B", "mera infração administrativa."),
            ("C", "o crime de descumprimento de missão."),
            ("D", "o crime de desobediência."),
            ("E", "o crime de prevaricação.")
        ]
    },
    {
        "pos": 79, "materia": "Direito Penal Militar", "dif": "MEDIO", "base": None,
        "enunc": "Analise as assertivas abaixo:\nI. A pena de desacato a superior é agravada, se o superior é oficial general ou comandante da unidade a que pertence o agente.\nII. As penas previstas em abstrato para os crimes de desacato a superior e desacato a militar são idênticas.\nIII. Haverá o crime de desobediência mesmo que a ordem da autoridade militar seja ilegal.\nDe acordo com o que estabelece o Código Penal Militar, está correto o que se afirma APENAS em",
        "gab": "C",
        "alts": [("A", "II."), ("B", "I e II."), ("C", "I."), ("D", "III."), ("E", "II e III.")]
    },
    {
        "pos": 80, "materia": "Direito Penal Militar", "dif": "FACIL", "base": None,
        "enunc": "Ronaldo, soldado da polícia militar, em patrulhamento pelas ruas de determinado município do Estado da Bahia, decidiu, durante o seu horário de trabalho, estacionar a viatura que conduzia, em via pública, para fazer um lanche em um estabelecimento comercial no centro da cidade, deixando as chaves no interior do veículo. Distraído, não percebeu que um indivíduo não identificado, aproveitando-se da situação, ingressou no interior da viatura e a subtraiu do local. Diante dos fatos hipotéticos acima mencionados, Ronaldo praticou, em tese, o crime de",
        "gab": "B",
        "alts": [
            ("A", "peculato-furto."),
            ("B", "peculato culposo."),
            ("C", "prevaricação."),
            ("D", "concussão."),
            ("E", "desobediência culposa.")
        ]
    }
]

payload_api = []

for q in questoes:
    pos_str = f"{q['pos']:02d}"
    id_origem = f"PMBA_SOLDADO_2023_Q{pos_str}"
    
    enunciado_final = q["enunc"]
    if q["base"] and q["base"].strip():
        enunciado_final = f"{q['base'].strip()}\n\n{q['enunc'].strip()}"
        
    dif = q["dif"]
    if dif == "MEDIO":
        dif = "MODERADO"
        
    alternativas_list = []
    for letra, texto in q["alts"]:
        # Se for anulada (T), correta é False em todas ou True se gabarito T
        is_correta = (letra == q["gab"])
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

out_file = os.path.join(output_dir, "pmba_soldado_2023_payload_api.json")
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(payload_api, f, ensure_ascii=False, indent=2)

print(f"Sucesso! {len(payload_api)} questoes geradas em {out_file}")
