$outputDir = "C:\Users\luisd\.gemini\antigravity\scratch\Parsertrajetoria\output"
if (-not (Test-Path $outputDir)) { New-Item -ItemType Directory -Path $outputDir -Force | Out-Null }

$banca = "IBFC"
$orgao = "Polícia Militar da Bahia - PMBA"
$cargo = "Aluno Soldado da PM - Caderno 01"
$ano = 2019
$fonte = "CONCURSO"

$tv = @"
Segurança
Luis Fernando Veríssimo
O ponto de venda mais forte do condomínio era a sua segurança. Havia as mais belas casas, os jardins, os playgrounds, as piscinas, mas havia, acima de tudo, segurança. Toda a área era cercada por um muro alto. Havia um portão principal com muitos guardas que controlavam tudo por um circuito fechado de TV. Só entravam no condomínio os proprietários e visitantes devidamente identificados e crachados. Mas os assaltos começaram assim mesmo. Os ladrões pulavam os muros. Os condôminos decidiram colocar torres com guardas ao longo do muro alto. Nos quatro lados. [...] Agora não só os visitantes eram obrigados a usar crachá. Os proprietários e seus familiares também. Não passava ninguém pelo portão sem se identificar para a guarda. Nem as babás. Nem os bebês. Mas os assaltos continuaram. Decidiram eletrificar os muros. Houve protestos, mas no fim todos concordaram. O mais importante era a segurança. Quem tocasse no fio de alta tensão em cima do muro morreria eletrocutado. Se não morresse, atrairia para o local um batalhão de guardas com ordens de atirar para matar. Mas os assaltos continuaram.
Grades nas janelas de todas as casas. Era o jeito. Mesmo se os ladrões ultrapassassem os altos muros, [...] não conseguiriam entrar nas casas. Todas as janelas foram engradadas. Mas os assaltos continuaram. Foi feito um apelo para que as pessoas saíssem de casa o mínimo possível. Dois assaltantes tinham entrado no condomínio no banco de trás do carro de um proprietário, com um revólver apontado para a sua nuca. Assaltaram a casa, depois saíram no carro roubado, com crachás roubados. [...]
Foi reforçada a guarda. Construíram uma terceira cerca. As famílias de mais posses, com mais coisas para serem roubadas, mudaram-se para uma chamada área de segurança máxima. E foi tomada uma medida extrema. Ninguém pode entrar no condomínio. Ninguém. Visitas, só num local predeterminado pela guarda, sob sua severa vigilância e por curtos períodos. E ninguém pode sair. Agora, a segurança é completa. Não tem havido mais assaltos. Ninguém precisa temer pelo seu patrimônio. Os ladrões que passam pela calçada só conseguem espiar através do grande portão de ferro e talvez avistar um ou outro condômino agarrado às grades da sua casa, olhando melancolicamente para a rua. [...]
"@

# Helper function
function New-ItemPayload($pos, $materia, $dif, $base, $enunc, $gab, $alts) {
    $posStr = "{0:D2}" -f $pos
    $id = "PMBA_SOLDADO_2019_Q$posStr"
    
    $enuncFinal = $enunc
    if ($base -and -not [string]::IsNullOrWhiteSpace($base)) {
        $enuncFinal = "$base`n`n$enunc"
    }
    
    $d = $dif
    if ($d -eq "MEDIO") { $d = "MODERADO" }
    
    $altsList = @()
    foreach ($a in $alts) {
        $letra = $a.L
        $texto = $a.T
        $isCorreta = ($gab -ne "*" -and $letra -eq $gab)
        $altsList += [PSCustomObject]@{
            letra = $letra
            texto = $texto
            correta = $isCorreta
        }
    }
    
    return [PSCustomObject]@{
        idOrigem = $id
        fonte = $fonte
        banca = $banca
        orgao = $orgao
        cargo = $cargo
        ano = $ano
        materiaNome = $materia
        dificuldade = $d
        enunciado = $enuncFinal
        imagemUrl = $null
        alternativas = $altsList
    }
}

$items = @()

# Q01 a Q10
$items += New-ItemPayload 1 "Língua Portuguesa" "FACIL" $tv "De acordo com o texto, assinale a alternativa correta." "*" @(
    @{L="A"; T="O texto discorre sobre um condomínio que ainda sofre uma série de assaltos por não haver um trabalho eficiente na segurança."},
    @{L="B"; T="Dois assaltantes entraram no condomínio no banco de trás do carro de um proprietário e remitiram seus bens."},
    @{L="C"; T="Infere-se do texto que há uma relevante crítica às prestações de serviço de segurança oferecidas em condomínios."},
    @{L="D"; T="No portão mais ínfero, existiam muitos guardas que controlavam tudo por um circuito fechado de TV."},
    @{L="E"; T="Os assaltos continuaram no condomínio porque a segurança apresentou um serviço falho e exímio."}
)
$items += New-ItemPayload 2 "Língua Portuguesa" "FACIL" $tv "A tipologia textual se relaciona com a estrutura e aspectos linguísticos de como um texto se apresenta; já os gêneros textuais são formações advindas de contextos culturais e históricos e possuem função social específica. Quanto ao gênero do texto 'Segurança', assinale a alternativa correta." "B" @(
    @{L="A"; T="Narração."}, @{L="B"; T="Crônica."}, @{L="C"; T="Anedota."}, @{L="D"; T="Relato."}, @{L="E"; T="Fábula."}
)
$items += New-ItemPayload 3 "Língua Portuguesa" "FACIL" $tv "Analise as afirmativas abaixo e assinale a alternativa correta.`nI. O vocábulo 'condomínio' recebe acento agudo porque é uma oxítona terminada em ditongo.`nII. Já o vocábulo 'condômino' recebe acento circunflexo porque todas as proparoxítonas devem receber este acento.`nIII. O vocábulo 'possível' recebe acento agudo porque é uma paroxítona terminada em 'l'." "A" @(
    @{L="A"; T="Apenas a afirmativa III está correta."},
    @{L="B"; T="Apenas as afirmativas I e III estão corretas."},
    @{L="C"; T="Apenas a afirmativa I está correta."},
    @{L="D"; T="Apenas as afirmativas II e III estão corretas."},
    @{L="E"; T="Apenas a afirmativa II está correta."}
)
$items += New-ItemPayload 4 "Língua Portuguesa" "MODERADO" $tv "A vírgula exerce inúmeras funções na comunicação escrita. Analise as justificativas para o seu uso, nas alternativas abaixo, e assinale a incorreta." "E" @(
    @{L="A"; T="“Havia as mais belas casas, os jardins, os playgrounds, as piscinas,” [...] É obrigatório o uso da vírgula para separar termos com funções semelhantes."},
    @{L="B"; T="“Agora, a segurança é completa”. É facultativo o uso da vírgula para separar adjuntos adverbiais, de pouca extensão, antepostos."},
    @{L="C"; T="“Houve protestos, mas no fim todos concordaram”. É obrigatório o uso da vírgula para separar orações coordenadas sindéticas adversativas."},
    @{L="D"; T="“Mesmo se os ladrões ultrapassassem os altos muros, não conseguiriam entrar nas casas”. É recomendável o uso da vírgula para separar orações subordinadas adverbiais condicionais quando vierem antes da principal."},
    @{L="E"; T="“Se não morresse, atrairia para o local um batalhão de guardas”. É obrigatório o uso da vírgula para separar verbos com tempos e modos diferentes."}
)
$items += New-ItemPayload 5 "Língua Portuguesa" "FACIL" $tv "Observe o enunciado extraído do texto: “Nem as babás. Nem os bebês”. Assinale a alternativa que apresenta a correta classificação da conjunção em destaque." "D" @(
    @{L="A"; T="coordenativa negativa."}, @{L="B"; T="coordenativa explicativa."}, @{L="C"; T="coordenativa conclusiva."}, @{L="D"; T="coordenativa aditiva."}, @{L="E"; T="coordenativa causal."}
)
$items += New-ItemPayload 6 "Língua Portuguesa" "FACIL" $tv "O vocábulo 'mas' aparece repetidas vezes no texto. Assinale a alternativa que apresenta corretamente sua relação estabelecida dentro do corpo textual." "C" @(
    @{L="A"; T="consequência."}, @{L="B"; T="causa."}, @{L="C"; T="adversidade."}, @{L="D"; T="explicação."}, @{L="E"; T="adição."}
)
$items += New-ItemPayload 7 "Língua Portuguesa" "MODERADO" $tv "Analise as afirmativas abaixo e dê valores Verdadeiro (V) ou Falso (F).`n( ) O texto possui narrador onisciente em 1ª pessoa.`n( ) 'Toda a área era cercada por um muro alto.' O enunciado anterior está escrito na voz passiva.`n( ) O título do texto sugere proteção e isto é refutado ao longo da obra.`nAssinale a alternativa que apresenta a sequência correta de cima para baixo." "E" @(
    @{L="A"; T="F, F, V."}, @{L="B"; T="V, F, F."}, @{L="C"; T="F, V, F."}, @{L="D"; T="V, V, F."}, @{L="E"; T="F, V, V."}
)
$items += New-ItemPayload 8 "Língua Portuguesa" "FACIL" $null "Quanto às normas para o uso do acento grave, assinale a alternativa correta." "C" @(
    @{L="A"; T="Os médicos atenderão nas salas de 1 à 5."},
    @{L="B"; T="Desde às duas horas estou no ponto."},
    @{L="C"; T="Eu assisti à cerimônia do casamento de minha sobrinha."},
    @{L="D"; T="As encomendas já foram repassadas à todas as escolas."},
    @{L="E"; T="A moça vai à pé todos os dias para o trabalho."}
)
$items += New-ItemPayload 9 "Língua Portuguesa" "FACIL" $null "Assinale a alternativa que apresenta uma palavra grafada de forma incorreta." "D" @(
    @{L="A"; T="A mesa de pingue-pongue está desmontada."},
    @{L="B"; T="Há de ser um super-homem para dar conta de tudo isto."},
    @{L="C"; T="O exército nacional decidiu contra-atacar."},
    @{L="D"; T="É preciso ser muito cara-de-pau para fingir tão bem."},
    @{L="E"; T="Não havia mais lugares no micro-ônibus."}
)
$items += New-ItemPayload 10 "Língua Portuguesa" "FACIL" $null "A fala do personagem da esquerda diz respeito ao sinal de _____ que foi abolido com o novo acordo ortográfico, assim como também o _____ das palavras destacadas na fala do personagem da direita." "B" @(
    @{L="A"; T="dois pontos / travessão."}, @{L="B"; T="trema / hífen."}, @{L="C"; T="reticências / traço."}, @{L="D"; T="dois pontos / hífen."}, @{L="E"; T="reticências / travessão."}
)

# Q11 a Q18 - Raciocínio Lógico
$items += New-ItemPayload 11 "Raciocínio Lógico" "FACIL" $null "Observe a disjunção: 'Marcelo não gosta de futebol ou Bruno não gosta de natação', assinale a alternativa correta que apresenta a negação dessa disjunção." "D" @(
    @{L="A"; T="Marcelo gosta de futebol e Bruno não gosta de natação"},
    @{L="B"; T="Marcelo gosta de futebol se e somente se Bruno gosta de natação"},
    @{L="C"; T="Ou Marcelo gosta de futebol ou Bruno gosta de natação"},
    @{L="D"; T="Marcelo gosta de futebol e Bruno gosta de natação"},
    @{L="E"; T="Marcelo não gosta de futebol e Bruno não gosta de natação"}
)
$items += New-ItemPayload 12 "Raciocínio Lógico" "MODERADO" $null "Em uma prateleira de uma biblioteca, deseja-se dispor 4 livros de maneiras distintas. Sabendo que a prateleira possui 10 espaços em que os livros podem ser colocados, assinale a alternativa que apresenta corretamente a quantidade de maneiras que esses livros podem ser dispostos nessa prateleira." "B" @(
    @{L="A"; T="3628800"}, @{L="B"; T="5040"}, @{L="C"; T="151200"}, @{L="D"; T="720"}, @{L="E"; T="24"}
)
$items += New-ItemPayload 13 "Raciocínio Lógico" "MODERADO" $null "Uma loja de eletroeletrônicos decide realizar o sorteio de dois brindes para os clientes que comprarem um televisor. No total, 200 clientes realizaram a compra de televisor e concorreram aos brindes, sendo 120 mulheres e 80 homens. Considerando que ao ganhar um brinde não se pode concorrer a outro brinde, assinale a alternativa que apresenta corretamente a probabilidade de que os ganhadores sejam um homem e uma mulher." "*" @(
    @{L="A"; T="50/199"}, @{L="B"; T="1/4"}, @{L="C"; T="9/40"}, @{L="D"; T="48/199"}, @{L="E"; T="6/25"}
)
$items += New-ItemPayload 14 "Raciocínio Lógico" "FACIL" $null "Considere a proposição: 'Todo pesquisador é estudioso.' Assinale a alternativa que não apresenta uma negação da proposição anterior." "E" @(
    @{L="A"; T="Existe algum pesquisador que não é estudioso"},
    @{L="B"; T="Algum pesquisador não é estudioso"},
    @{L="C"; T="Pelo menos um pesquisador não é estudioso"},
    @{L="D"; T="Existe pesquisador que não é estudioso"},
    @{L="E"; T="Nenhum pesquisador é estudioso"}
)
$items += New-ItemPayload 15 "Raciocínio Lógico" "MODERADO" $null "Analise a proposição composta a seguir: 'Maria viaja para o Rio de Janeiro se e somente se Fernando viaja para São Paulo'. Assinale a alternativa que apresenta a negação dessa proposição composta." "*" @(
    @{L="A"; T="Maria não viaja para o Rio de Janeiro ou Fernando não viaja para São Paulo"},
    @{L="B"; T="Maria não viaja para o Rio de Janeiro e Fernando não viaja para São Paulo"},
    @{L="C"; T="Ou Maria viaja para o Rio de Janeiro ou Fernando viaja para São Paulo"},
    @{L="D"; T="Ou Maria não viaja para o Rio de Janeiro ou Fernando não viaja para São Paulo"},
    @{L="E"; T="Maria não viaja para o Rio de Janeiro ou Fernando viaja para São Paulo"}
)
$items += New-ItemPayload 16 "Raciocínio Lógico" "MODERADO" $null "Observe as duas proposições P e Q apresentadas a seguir:`nP: Ana é engenheira.`nQ: Bianca é arquiteta.`nConsidere que Ana é engenheira somente se Bianca é arquiteta e, assinale a alternativa correta." "B" @(
    @{L="A"; T="Ana ser engenheira não implica Bianca ser arquiteta"},
    @{L="B"; T="Ana ser engenheira é condição suficiente para Bianca ser arquiteta"},
    @{L="C"; T="Uma condição necessária para Bianca ser arquiteta é Ana ser engenheira"},
    @{L="D"; T="Ana é engenheira se e somente se Bianca não é arquiteta"},
    @{L="E"; T="Uma condição necessária para Bianca ser arquiteta é Ana não ser engenheira"}
)
$items += New-ItemPayload 17 "Raciocínio Lógico" "FACIL" $null "Conjunções são proposições compostas em que há a presença do conectivo 'e' e podem ser representadas pelo símbolo '∧'. Sendo assim, assinale a alternativa correta." "B" @(
    @{L="A"; T="Se P é verdadeira e Q é verdadeira, então P ∧ Q é falsa"},
    @{L="B"; T="Se P é verdadeira e Q é falsa, então P ∧ Q é falsa"},
    @{L="C"; T="Se P é falsa e Q é falsa, então P ∧ Q é verdadeira"},
    @{L="D"; T="Se P é falsa e Q é verdadeira, então P ∧ Q é verdadeira"},
    @{L="E"; T="P ∧ Q só será verdadeira se P e Q forem falsas"}
)
$items += New-ItemPayload 18 "Raciocínio Lógico" "MODERADO" $null "Considere que os símbolos →, ↔, ∧ e ∨ representam os operadores lógicos 'se...então', 'se e somente se', 'e' e 'ou', respectivamente. Analise as sentenças abaixo e dê valores Verdadeiro (V) ou Falso (F).`n( ) (7 − 2 = 5) ∨ (3 > 2)`n( ) (3 + 2 = 4) ↔ (1 > 3)`n( ) (3 × 5 + 6 = 21) ∧ (18 − 3 − 1 = 7)`n( ) (4 × 4 + 3 = 19) → (9 − 2 = 7)`nAssinale a alternativa que apresenta a sequência correta de cima para baixo." "A" @(
    @{L="A"; T="V, V, F, V"}, @{L="B"; T="F, V, F, V"}, @{L="C"; T="V, V, V, F"}, @{L="D"; T="V, F, F, V"}, @{L="E"; T="V, V, F, F"}
)

# Q19 a Q26 - História do Brasil
$items += New-ItemPayload 19 "História do Brasil" "MODERADO" $null "A chegada dos Europeus à América, no século XV, significou o início da destruição da maioria das organizações sociais, culturais e políticas existentes. A respeito da chegada dos portugueses ao Brasil, assinale a alternativa incorreta." "D" @(
    @{L="A"; T="Além da submissão à exploração colonial, dos sucessivos confrontos armados e da expulsão de suas terras, os indígenas também foram destruídos pelas doenças trazidas pelos conquistadores"},
    @{L="B"; T="Os conquistadores europeus, portadores de uma tecnologia superior e dotados da ambição comercial, impuseram um verdadeiro morticínio às populações nativas"},
    @{L="C"; T="O processo de massacre aos indígenas teve início no período colonial, manteve-se pela fase imperial e continuou pelo período republicano, não sendo raro na atualidade"},
    @{L="D"; T="Os primeiros séculos de contato entre brancos e índios revestiram-se de alguma amabilidade, pois, os interesses dos colonizadores com o passar do tempo mudaram radicalmente em relação ao dos indígenas"},
    @{L="E"; T="No início, os índios do Brasil foram atraídos pelo escambo, isto é, troca de produtos nativos por outra mercadoria"}
)
$items += New-ItemPayload 20 "História do Brasil" "MODERADO" $null "No período de 1968 a 1974, o Brasil viveu um acelerado crescimento econômico, nomeado pelos militares de Milagre Econômico. A respeito do Milagre Econômico e com base na concentração de renda (1960-1976), assinale a alternativa correta." "D" @(
    @{L="A"; T="Assegurou toda a distribuição da riqueza produzida entre os brasileiros"},
    @{L="B"; T="Possibilitou a diminuição das diferenças econômicas entre as classes sociais"},
    @{L="C"; T="Permitiu a redução da pobreza e elevou a qualidade de vida de modo igualitário"},
    @{L="D"; T="Concentrou a renda e acentuou as desigualdades sociais"},
    @{L="E"; T="Ampliou a capacidade produtiva e consumista do país, que se tornou modelo na América Latina de igualdade e prosperidade"}
)
$items += New-ItemPayload 21 "História do Brasil" "MODERADO" $null "A respeito dos engenhos de açúcar no Brasil Colonial, leia as afirmativas abaixo e dê valores Verdadeiro (V) ou Falso (F).`n( ) As primeiras mudas de canas de açúcar foram trazidas da ilha da Madeira para o Brasil por Martim Afonso de Souza que instalou o primeiro engenho da colônia em São Vicente.`n( ) A multiplicação dos engenhos pela costa brasileira foi bastante rápida, chegando a mais de 60 em 1570 e 200 no final do século XVI.`n( ) Coube a região Nordeste, destacadamente o litoral de Pernambuco e Bahia, o papel de principal produtora de açúcar da colônia.`n( ) O engenho, que em alguns casos chegava a ter perto de 5.000 moradores, era constituído por área extensas de florestas, fornecedoras de madeira; plantações de cana; a residência do proprietário conhecida como casa grande, a capela e a senzala.`nAssinale a alternativa que apresenta a sequência correta de cima para baixo." "E" @(
    @{L="A"; T="V, F, V, F"}, @{L="B"; T="F, F, F, F"}, @{L="C"; T="F, F, V, V"}, @{L="D"; T="V, V, F, F"}, @{L="E"; T="V, V, V, V"}
)
$items += New-ItemPayload 22 "História do Brasil" "MODERADO" $null "A descoberta do ouro em Minas Gerais pelos bandeirantes paulistas, em finais do século XVII, atraiu para a região milhares de colonos. A respeito da Guerra dos Emboabas, assinale a alternativa correta." "A" @(
    @{L="A"; T="Os emboabas enfrentaram os paulistas em vários combates, entre eles, o mais marcante ocorreu no chamado Capão da traição, no qual 300 paulistas foram cercados pelos emboabas"},
    @{L="B"; T="O confronto teve como motivo principal a disputa pela exploração do café produzido em grande escala na região de Minas Gerais"},
    @{L="C"; T="Os paulistas desejavam ter exclusividade nas terras de Minas, pois diziam que tinham descoberto essa região e pretendiam explorá-la para a plantação de açúcar"},
    @{L="D"; T="Em 1750 o governo português interveio e, a fim de pacificar e melhor administrar a região, juntou a capitania de São Paulo e Minas Gerais com a capitania do Rio de Janeiro"},
    @{L="E"; T="Após vários conflitos os bandeirantes paulistas partiram em busca de novas explorações na região do Nordeste sob a liderança de Manuel Nunes Viana"}
)
$items += New-ItemPayload 23 "História do Brasil" "MODERADO" $null "O quadro de Rugendas (1835) representa uma cena do que conhecemos historicamente como 'As Negras do Tabuleiro'. A respeito deste período, leia as afirmativas abaixo.`nI. A mineração era um trabalho pesado, feito principalmente por homens.`nII. As negras retratadas por Rugendas eram vendedoras ambulantes, que ofereciam comida e bebida aos que trabalhavam na extração do ouro.`nIII. Geralmente essas mulheres eram livres, mas trabalhavam por conta dos mineradores, vigiando os trabalhadores na extração do ouro.`nIV. Elas transitavam pelas vilas, roças e arraiais, vendendo suas mercadorias para pessoas de todas as condições sociais.`nAssinale a alternativa correta." "B" @(
    @{L="A"; T="As afirmativas I, II, III e IV estão corretas"},
    @{L="B"; T="Apenas as afirmativas I, II e IV estão corretas"},
    @{L="C"; T="Apenas as afirmativas III e IV estão corretas"},
    @{L="D"; T="Todas as afirmativas estão incorretas"},
    @{L="E"; T="Apenas a afirmativa III está correta"}
)
$items += New-ItemPayload 24 "História do Brasil" "MODERADO" $null "A respeito da Guerra de Canudos (1896-1897), assinale a alternativa correta." "E" @(
    @{L="A"; T="Esse movimento refletia a extrema fartura em que viviam as populações do Sertão Nordestino"},
    @{L="B"; T="A tensão política foi agravada pela expulsão dos ruralistas que atuavam nas revoltas catarinenses e paranaenses"},
    @{L="C"; T="A região onde foi estabelecido o vilarejo de Canudos, no interior de Pernambuco, era marcada por latifúndios improdutivos, pelas secas cíclicas e pelo desemprego"},
    @{L="D"; T="Os revoltosos incendiaram Canudos e mataram grande parte do exército, fazendo-os de prisioneiros"},
    @{L="E"; T="Foi um movimento de resistência da população sertaneja contra a estrutura agrário-latifundiária e as medidas repressivas oficiais"}
)
$items += New-ItemPayload 25 "História do Brasil" "FACIL" $null "A respeito da Conjuração Baiana de 1798 em Salvador, assinale a alternativa incorreta." "C" @(
    @{L="A"; T="Condenados por conspirarem contra a Coroa de Portugal, dois alfaiates e dois soldados foram considerados os réus do movimento qualificado pelas autoridades do Tribunal da Relação da Bahia, em 1799, de 'Sedição dos Mulatos'"},
    @{L="B"; T="Parte dos historiadores que versaram sobre a Conjuração Baiana de 1798, perceberam certo grau de coerência entre a tentativa de participação política dos setores populares e a ideia de república"},
    @{L="C"; T="Conjuração Baiana foi uma revolta social de caráter burguês, que ocorreu na Bahia em 1798. Recebeu uma importante influência dos ideais do Renascimento Cultural e Revolução Industrial"},
    @{L="D"; T="A Conjuração Baiana de 1798 deixa de ser um evento de identificação regional, para tornar-se o representante das mais profundas aspirações de amplos setores da sociedade brasileira"},
    @{L="E"; T="Esse movimento defendia a emancipação política do Brasil, ou seja, o fim do pacto colonial com Portugal e a instauração e implantação da República"}
)
$items += New-ItemPayload 26 "História do Brasil" "MODERADO" $null "A República Velha também foi nomeada 'República das Oligarquias', porque era comandada pela aristocracia dos fazendeiros. A respeito deste período da história brasileira, assinale a alternativa incorreta." "A" @(
    @{L="A"; T="Não havia, da parte das elites, qualquer pretensão de impedir ou retroceder as mudanças ao regime vigente. Era de comum acordo qualquer projeto político substantivamente republicano, isto é, que se alicerçasse numa concepção igualitária, legalista e cívica da Nação"},
    @{L="B"; T="O conceito de República era, pois, bastante débil. Ele quase não tinha conteúdo próprio, sendo compreendido essencialmente por oposição à monarquia unitária"},
    @{L="C"; T="O exercício do poder político da Primeira República foi marcado pelo autoritarismo que sucessivamente lhe imprimiram as forças que a instauraram"},
    @{L="D"; T="O discurso reformista liberal da década de 1870 acabou servindo de fachada, na verdade, para uma reação aristocrática que, esvaziando o poder da Coroa e excluindo as camadas pobres do direito de voto, pretendia instalar um parlamentarismo aristocrático onde apenas as elites estivessem no controle do Estado"},
    @{L="E"; T="Na busca de outras fórmulas que eliminassem a autonomia do poder monárquico e, com ela, a possibilidade de uma reforma social pelo alto, a aristocracia rural aderiu sucessivamente ao federalismo e ao republicanismo, especialmente depois da Lei Áurea"}
)

# Q27 a Q34 - Geografia do Brasil
$items += New-ItemPayload 27 "Geografia do Brasil" "FACIL" $null "No que concerne aos biomas que estão presentes no estado da Bahia, assinale a alternativa correta." "D" @(
    @{L="A"; T="Amazônia, Cerrado e Mata Atlântica"}, @{L="B"; T="Amazônia, Caatinga e Pampa"}, @{L="C"; T="Amazônia, Mata Atlântica e Pampa"}, @{L="D"; T="Cerrado, Caatinga e Mata Atlântica"}, @{L="E"; T="Cerrado, Caatinga e Pampa"}
)
$items += New-ItemPayload 28 "Geografia do Brasil" "MODERADO" $null "No que se refere aos aspectos físicos do estado da Bahia, analise as afirmativas abaixo e dê valores Verdadeiro (V) ou Falso (F).`n( ) O estado possui relevos com altitudes que podem variar de 0 a 630 metros, sendo que as maiores elevações estão localizadas no Recôncavo Baiano.`n( ) A Serra do Espinhaço, a Serra da Canastra, a Chapada Diamantina e a Chapada dos Veadeiros são exemplos de acidentes geográficos localizados no estado.`n( ) Grande parte do território do estado é banhado por cursos dágua pertencentes à bacia hidrográfica do rio São Francisco.`n( ) A capital do estado, Salvador, está localizada na bacia hidrográfica do rio Jequitinhonha, e Feira de Santana, na bacia do rio Paraná.`nAssinale a alternativa que apresenta a sequência correta de cima para baixo." "C" @(
    @{L="A"; T="F, F, F, V"}, @{L="B"; T="F, V, V, F"}, @{L="C"; T="F, F, V, F"}, @{L="D"; T="V, V, F, F"}, @{L="E"; T="V, F, F, V"}
)
$items += New-ItemPayload 29 "Geografia do Brasil" "MODERADO" $null "Associe os climas da legenda do mapa com os diferentes tipos de climas da região Nordeste. Analise as afirmativas abaixo e dê valores Verdadeiro (V) ou Falso (F).`n( ) O clima 1 é o subtropical.`n( ) O clima 2 é o tropical.`n( ) O clima 3 é o semiárido.`n( ) O clima 4 é o equatorial.`nAssinale a alternativa que apresenta a sequência correta de cima para baixo." "B" @(
    @{L="A"; T="V, F, F, F"}, @{L="B"; T="F, V, F, F"}, @{L="C"; T="F, F, V, F"}, @{L="D"; T="V, F, F, V"}, @{L="E"; T="V, V, V, V"}
)
$items += New-ItemPayload 30 "Geografia do Brasil" "FACIL" $null "A canção Sobradinho (Sá, Rodrix e Guarabyra) protesta contra a construção da Usina Hidrelétrica de Sobradinho no rio São Francisco, Bahia. Sobre os impactos negativos causados pela construção de grandes barragens, que afetam a sociedade e o meio ambiente, assinale a alternativa incorreta." "E" @(
    @{L="A"; T="Desapropriação de propriedades particulares e realocação da população ribeirinha"},
    @{L="B"; T="Desintegração dos costumes e tradições históricas da população atingida"},
    @{L="C"; T="Perda de terras agricultáveis devido à elevação do nível da água do rio"},
    @{L="D"; T="Alteração da dinâmica natural do rio e derrubada de florestas"},
    @{L="E"; T="Rebaixamento do lençol freático e poluição radioativa do rio"}
)
$items += New-ItemPayload 31 "Geografia do Brasil" "MODERADO" $null "A respeito do vazamento de óleo que ocorreu no litoral nordestino e atingiu praias do estado da Bahia, no segundo semestre de 2019, analise as afirmativas abaixo.`nI. O óleo pode causar a morte de animais marinhos, como tartarugas e peixes.`nII. O óleo pode alterar a qualidade da água, deixando-a inclusive imprópria para o banho.`nIII. O óleo pode ocasionar a formação de processos erosivos em áreas de mangue, como ravinas e voçorocas.`nIV. O óleo pode reduzir as emissões de dióxido de carbono na atmosfera, contribuindo assim com o aquecimento global.`nAssinale a alternativa correta." "A" @(
    @{L="A"; T="Apenas as afirmativas I e II estão corretas"},
    @{L="B"; T="Apenas as afirmativas I e III estão corretas"},
    @{L="C"; T="Apenas as afirmativas II e IV estão corretas"},
    @{L="D"; T="Apenas as afirmativas I, III e IV estão corretas"},
    @{L="E"; T="As afirmativas I, II, III e IV estão corretas"}
)
$items += New-ItemPayload 32 "Geografia do Brasil" "FACIL" $null "A canção homenageia entidades carnavalescas que são patrimônio da cultura baiana: 'Olodum, te amo! Ilê, te amo! Didá, te amo! Neguinho, te amo!'. Assinale a alternativa correta que indica, respectivamente, um termo que é utilizado para nomear essas entidades e qual sua representatividade." "A" @(
    @{L="A"; T="Bloco Afro, símbolo da resistência e da valorização negra"},
    @{L="B"; T="Trio Elétrico, palco móvel utilizado pelos artistas"},
    @{L="C"; T="Escola de Samba, agremiação popular voltada ao samba"},
    @{L="D"; T="Samba de Roda, propagador da cultura do Recôncavo da Bahia"},
    @{L="E"; T="Filhos de Gandhy, que difundiu o frevo na Bahia"}
)
$items += New-ItemPayload 33 "Geografia do Brasil" "FACIL" $null "Assinale a alternativa correta que apresenta a cor ou raça predominantemente autodeclarada pela população do estado da Bahia, de acordo o Censo Demográfico realizado em 2010 pelo Instituto Brasileiro de Geografia e Estatística (IBGE)." "B" @(
    @{L="A"; T="Amarela"}, @{L="B"; T="Parda"}, @{L="C"; T="Preta"}, @{L="D"; T="Branca"}, @{L="E"; T="Indígena"}
)
$items += New-ItemPayload 34 "Geografia do Brasil" "MODERADO" $null "Em relação aos aspectos econômicos e sociais do estado da Bahia, assinale a alternativa correta." "E" @(
    @{L="A"; T="O Produto Interno Bruto (PIB) per capita da Bahia está entre os três maiores do Brasil"},
    @{L="B"; T="O Produto Interno Bruto (PIB) per capita da Bahia é o menor entre os estados do Brasil"},
    @{L="C"; T="O Índice de Desenvolvimento Humano (IDH) da Bahia está entre os três maiores do Brasil"},
    @{L="D"; T="O Índice de Desenvolvimento Humano (IDH) da Bahia é o menor entre os estados do Brasil"},
    @{L="E"; T="A expectativa de vida do baiano está crescendo, porém ainda está abaixo da média do brasileiro"}
)

# Q35 a Q42 - Atualidades
$items += New-ItemPayload 35 "Atualidades" "FACIL" $null "“A globalização implica que a produção de empresas transnacionais é para o mercado mundial...”. Assinale a alternativa que indica uma característica incorreta do processo de globalização." "E" @(
    @{L="A"; T="Integração social e econômica"},
    @{L="B"; T="Surgimento de blocos econômicos"},
    @{L="C"; T="Ampliação dos recursos tecnológicos"},
    @{L="D"; T="A instantaneidade e velocidade das informações"},
    @{L="E"; T="Redução da concorrência e da competitividade de mercado"}
)
$items += New-ItemPayload 36 "Atualidades" "FACIL" $null "“Num plebiscito em 23 de junho de 2016, os britânicos foram perguntados se o Reino Unido deveria permanecer ou deixar a União Europeia (UE)...”. Assinale a alternativa correta que apresenta o termo comumente utilizado quando se fala sobre a decisão do Reino Unido de deixar UE." "C" @(
    @{L="A"; T="Ukexit"}, @{L="B"; T="Outofue"}, @{L="C"; T="Brexit"}, @{L="D"; T="Brexid"}, @{L="E"; T="British-leave"}
)
$items += New-ItemPayload 37 "Atualidades" "FACIL" $null "Assinale a alternativa que apresenta, de forma incorreta, uma atitude que pode auxiliar na redução de gases do efeito estufa." "E" @(
    @{L="A"; T="Produzir menos lixo"},
    @{L="B"; T="Utilizar o transporte público"},
    @{L="C"; T="Reduzir a queima de combustíveis fósseis"},
    @{L="D"; T="Reduzir o consumo de carne bovina"},
    @{L="E"; T="Evitar produtos fabricados de maneira sustentável"}
)
$items += New-ItemPayload 38 "Atualidades" "FACIL" $null "A Inteligência Artificial (IA) está transformando a maneira como fazemos negócios. Assinale a alternativa correta que apresenta uma vantagem da inteligência artificial." "*" @(
    @{L="A"; T="Aumento substancial de erros na produção"},
    @{L="B"; T="Maior tempo de trabalho e de produção"},
    @{L="C"; T="Queda na eficiência e na produtividade"},
    @{L="D"; T="Dificuldade na tomada de decisão e na solução de problemas"},
    @{L="E"; T="Modernização das etapas de produção"}
)
$items += New-ItemPayload 39 "Atualidades" "FACIL" $null "Instituições de pesquisa utilizaram tecnologia de sensoriamento remoto para explicar a origem e evolução de manchas de óleo que poluíram o litoral Nordeste do Brasil, no segundo semestre de 2019, a partir de imagens capturadas pelo Sentinel-1A. Assinale a alternativa que indica de maneira correta o tipo de imagem citada no texto acima." "C" @(
    @{L="A"; T="Imagem de GPS"}, @{L="B"; T="Imagem de teodolito"}, @{L="C"; T="Imagem de satélite"}, @{L="D"; T="Imagem de termômetro"}, @{L="E"; T="Imagem de pluviômetro"}
)
$items += New-ItemPayload 40 "Atualidades" "FACIL" $null "“O Irã anunciou, nesta segunda (4/11/2019), mais uma medida que desrespeita o Acordo Nuclear Internacional [...]. A preocupação mundial é que o enriquecimento de urânio chegue a um nível que permita produção de _____” (G1, 2019). Assinale a alternativa que preencha corretamente a lacuna." "B" @(
    @{L="A"; T="tanques de guerra"}, @{L="B"; T="bombas atômicas"}, @{L="C"; T="bombas de gás lacrimogênio"}, @{L="D"; T="armas biológicas"}, @{L="E"; T="armas de fogo"}
)
$items += New-ItemPayload 41 "Atualidades" "MEDIO" $null "“O Supremo Tribunal Federal (STF) determinou na quinta-feira, 13 de junho de 2019, que a discriminação por orientação sexual e identidade de gênero passe a ser considerada um crime, [...] por 8 votos a 3, os ministros determinaram que a conduta passe a ser punida pela _____” (BBC, 2019). Assinale a alternativa que preencha corretamente a lacuna." "D" @(
    @{L="A"; T="Lei dos Crimes Hediondos"},
    @{L="B"; T="Lei Maria da Penha"},
    @{L="C"; T="Lei de Execução Penal"},
    @{L="D"; T="Lei de Racismo (define os crimes resultantes de preconceito de raça ou de cor)"},
    @{L="E"; T="Lei Menino Bernardo"}
)
$items += New-ItemPayload 42 "Atualidades" "FACIL" $null "Os relatos de _____ contra brasileiros em Portugal - maior comunidade estrangeira no país - tiveram aumento expressivo: 150% em 12 meses. A _____ contra brasileiros é a terceira principal causa de discriminação em Portugal (Folha de São Paulo, 2019). Assinale a alternativa com a palavra que preencha corretamente as duas lacunas." "A" @(
    @{L="A"; T="xenofobia"}, @{L="B"; T="acrofobia"}, @{L="C"; T="claustrofobia"}, @{L="D"; T="homofobia"}, @{L="E"; T="monofobia"}
)

# Q43 a Q50 - Informática
$items += New-ItemPayload 43 "Informática" "FACIL" $null "No MS Excel 2010, idioma português, configuração padrão, existe uma função que permite arredondar um número até uma quantidade especificada de dígitos. Assinale a alternativa correta que corresponda a esta função." "A" @(
    @{L="A"; T="ARRED"}, @{L="B"; T="ARREDMULTB.PRECISO"}, @{L="C"; T="ARREDIG"}, @{L="D"; T="ARRED.PRECISO"}, @{L="E"; T="ARRUMAR"}
)
$items += New-ItemPayload 44 "Informática" "FACIL" $null "Alessandro precisa montar um relatório no MS Excel 2010, idioma português, configuração padrão, que some o intervalo de células de A1 até A5, somente os valores maiores do que vinte. Assinale a alternativa correta que representa a fórmula que Alessandro irá utilizar." "E" @(
    @{L="A"; T="=SOMASE(A1:A5;>20)"},
    @{L="B"; T="=SE(A1:A5>20;SOMA())"},
    @{L="C"; T="=SOMA(SE(A1:A5>20))"},
    @{L="D"; T="=SOMASE(A1^A5;\">20\")"},
    @{L="E"; T="=SOMASE(A1:A5;\">20\")"}
)
$items += New-ItemPayload 45 "Informática" "FACIL" $null "Otavio entrou em contato com seu provedor de internet para resolver um problema de conexão com a internet em um computador que utiliza Windows 10, idioma português, configuração padrão. O atendente do suporte técnico solicitou a informação do endereço IP do computador na rede. Assinale a alternativa que apresenta corretamente como obter este endereço em linha de comando." "B" @(
    @{L="A"; T="netsh -a"}, @{L="B"; T="ipconfig"}, @{L="C"; T="getip -a"}, @{L="D"; T="ifconfig"}, @{L="E"; T="ipaddress"}
)
$items += New-ItemPayload 46 "Informática" "FACIL" $null "Sobre as Ferramentas de Lixeira do sistema operacional Windows 10, idioma português, configuração padrão, assinale a alternativa incorreta." "C" @(
    @{L="A"; T="Esvaziar Lixeira"}, @{L="B"; T="Propriedades da Lixeira"}, @{L="C"; T="Compactar Lixeira"}, @{L="D"; T="Restaurar todos os itens"}, @{L="E"; T="Restaurar os itens selecionados"}
)
$items += New-ItemPayload 47 "Informática" "FACIL" $null "No MS Excel 2010, idioma português, configuração padrão, existe a funcionalidade Congelar Painéis. Assinale a alternativa correta sobre o menu no qual encontra-se disponível esta funcionalidade." "E" @(
    @{L="A"; T="Layout de Página"}, @{L="B"; T="Fórmulas"}, @{L="C"; T="Dados"}, @{L="D"; T="Revisão"}, @{L="E"; T="Exibição"}
)
$items += New-ItemPayload 48 "Informática" "FACIL" $null "Assinale a alternativa correta quanto ao conceito de intranet." "E" @(
    @{L="A"; T="rede de propaganda de uma empresa"}, @{L="B"; T="sinônimo de internet"}, @{L="C"; T="rede de telecom"}, @{L="D"; T="rede pública"}, @{L="E"; T="rede de uso interno de uma instituição"}
)
$items += New-ItemPayload 49 "Informática" "FACIL" $null "Eduarda precisa enviar um e-mail com um comunicado geral a vários destinatários, de tal maneira que eles não conheçam uns aos outros. Assinale a alternativa que apresenta corretamente a forma do envio que Eduarda deve utilizar para o comunicado." "A" @(
    @{L="A"; T="Cco"}, @{L="B"; T="Coc"}, @{L="C"; T="Ccc"}, @{L="D"; T="Coo"}, @{L="E"; T="Cc"}
)
$items += New-ItemPayload 50 "Informática" "FACIL" $null "Marcos deseja migrar seu backup de arquivos pessoais, que atualmente encontra-se em seu computador, para nuvem. Assinale a alternativa correta para exemplos de serviços de armazenamento de arquivos em nuvem." "D" @(
    @{L="A"; T="Dropbox e Google Chrome"}, @{L="B"; T="Firefox e Mozilla"}, @{L="C"; T="Google Arq e Team Viewer"}, @{L="D"; T="Dropbox e Google Drive"}, @{L="E"; T="Google Arq e Firefox"}
)

# Q51 a Q55 - Direito Constitucional
$items += New-ItemPayload 51 "Direito Constitucional" "MEDIO" $null "Quem deve respeitar os direitos e garantias fundamentais? Sobre os destinatários dos direitos fundamentais, analise as afirmativas abaixo e dê valores Verdadeiro (V) ou Falso (F).`n( ) Os direitos fundamentais, em regra, destinam-se a proteção dos estrangeiros residentes no país e, também, dos de passagem pelo País.`n( ) Os direitos fundamentais destinam-se à proteção dos apátridas.`n( ) Os direitos fundamentais destinam-se à proteção das pessoas jurídicas, observadas suas particularidades.`n( ) O destinatário principal do dever de respeitar os direitos dos indivíduos é o Estado no sentido mais amplo do termo. Sendo, também, atualmente possível ter como destinatário um particular a partir do reconhecimento do efeito horizontal dos direitos fundamentais.`nAssinale a alternativa que apresenta a sequência correta de cima para baixo." "A" @(
    @{L="A"; T="V, V, V, V"}, @{L="B"; T="V, V, F, F"}, @{L="C"; T="V, F, F, V"}, @{L="D"; T="F, F, V, V"}, @{L="E"; T="F, V, V, F"}
)
$items += New-ItemPayload 52 "Direito Constitucional" "FACIL" $null "Os direitos sociais, direitos de segunda dimensão, apresentam-se como prestações positivas a serem implementadas pelo Estado. Sobre a Ordem Social assinale a alternativa correta." "B" @(
    @{L="A"; T="A educação é direito de todos e dever exclusivo do Estado"},
    @{L="B"; T="O Estado protegerá as manifestações das culturas populares, indígenas e afro-brasileiras, e das de grupos participantes do processo civilizatório nacional"},
    @{L="C"; T="As ações e serviços públicos de saúde integram uma rede regionalizada e hierarquizada e constituem um sistema único, organizado de forma centralizada, com direção única em cada esfera de governo"},
    @{L="D"; T="É dever do Estado fomentar práticas desportivas formais e não formais, como direito de cada um, observado a destinação de recursos públicos para a promoção prioritária do desporto de alto rendimento"},
    @{L="E"; T="É livre a manifestação do pensamento, sendo inconstitucional a regulamentação de diversões e espetáculos públicos, mesmo que para a indicação de faixas etárias a que não se recomendem"}
)
$items += New-ItemPayload 53 "Direito Constitucional" "FACIL" $null "A segurança pública, dever do Estado, direito e responsabilidade de todos, é exercida para a preservação da ordem pública e da incolumidade das pessoas e do patrimônio. Considerando sua estrutura, assinale a alternativa que não contém um de seus órgãos." "A" @(
    @{L="A"; T="Guardas Municipais"}, @{L="B"; T="Polícia Federal"}, @{L="C"; T="Polícia Rodoviária Federal"}, @{L="D"; T="Polícias Civis"}, @{L="E"; T="Polícias militares e corpos de bombeiros militares"}
)
$items += New-ItemPayload 54 "Direito Constitucional" "FACIL" $null "A Polícia Federal, instituída por lei como órgão permanente, é organizada e mantida pela União e estruturada em carreira. Sobre suas atribuições, assinale a alternativa correta." "C" @(
    @{L="A"; T="Dirigida por delegados de polícia de carreira, incumbem, ressalvada a competência da União, as funções de polícia judiciária e a apuração de infrações penais, exceto as militares"},
    @{L="B"; T="Cabe a ela o exercício da polícia ostensiva e a preservação da ordem pública"},
    @{L="C"; T="Destina-se a apurar infrações penais contra a ordem política e social ou em detrimento de bens, serviços e interesses da União ou de suas entidades autárquicas e empresas públicas, assim como outras infrações cuja prática tenha repercussão interestadual ou internacional e exija repressão uniforme, segundo dispuser em lei"},
    @{L="D"; T="Exerce as funções de polícia marítima e execução de atividade da defesa civil"},
    @{L="E"; T="Destina-se ao patrulhamento ostensivo das ferrovias federais, bem como prevenir e reprimir o tráfico ilícito de entorpecentes e drogas afins, o contrabando e o descaminho"}
)
$items += New-ItemPayload 55 "Direito Constitucional" "MODERADO" $null "Nos termos da Constituição do Estado da Bahia, analise as afirmativas abaixo quanto às atribuições do Governador de Estado.`nI. Compete privativamente ao Governador do Estado exercer, com auxílio dos Secretários de Estado, a direção superior da administração estadual.`nII. Compete privativamente ao Governador do Estado decretar e fazer executar a intervenção no Município, na forma da Constituição do Estadual.`nIII. Compete privativamente ao Governador do Estado decretar as situações de emergência e estado de calamidade pública.`nIV. Compete privativamente ao Governador do Estado exercer o comando supremo da Polícia Militar e do Corpo de Bombeiros Militar, promover seus oficiais e nomeá-los para os cargos que lhe são privativos.`nAssinale a alternativa correta." "D" @(
    @{L="A"; T="Apenas as afirmativas II e IV estão corretas"},
    @{L="B"; T="Apenas as afirmativas I, II e IV estão corretas"},
    @{L="C"; T="Apenas a afirmativa II está correta"},
    @{L="D"; T="As afirmativas I, II, III e IV estão corretas"},
    @{L="E"; T="Apenas as afirmativas II e III estão corretas"}
)

# Q56 a Q60 - Direitos Humanos
$items += New-ItemPayload 56 "Direitos Humanos" "FACIL" $null "A Declaração Universal de Direitos Humanos de 1948 procurou colocar a dignidade da pessoa humana como núcleo de todos os direitos humanos. Assim, sobre seu âmbito de proteção, assinale a alternativa correta." "D" @(
    @{L="A"; T="Nem todo ser humano tem o direito de ser, em todos os lugares, reconhecido como pessoa perante a lei"},
    @{L="B"; T="O exílio é permitido em determinadas situações"},
    @{L="C"; T="Reconhece a possibilidade da norma retroagir para prejudicar o réu"},
    @{L="D"; T="Todo ser humano acusado de um ato delituoso tem o direito de ser presumido inocente até que a sua culpabilidade tenha sido provada de acordo com a lei, em julgamento público no qual lhe tenha sido asseguradas todas as garantias necessárias à sua defesa"},
    @{L="E"; T="A vontade do povo será a base da autoridade do governo; esta vontade será expressa em eleições periódicas e legítimas, por sufrágio censitário, por voto secreto ou processo equivalente que assegure a liberdade de voto"}
)
$items += New-ItemPayload 57 "Direitos Humanos" "MODERADO" $null "A Convenção Americana de Direitos Humanos (Pacto de San José da Costa Rica, 1969) busca consolidar um regime de liberdade pessoal e justiça social. Assim, quanto ao seu âmbito de proteção, analise as afirmativas abaixo e dê valores Verdadeiro (V) ou Falso (F).`n( ) Não existe nenhuma relação entre o Pacto de San Jose da Costa Rica e a Declaração Universal dos Direitos Humanos.`n( ) Sobre os deveres das pessoas, determina que toda pessoa tem deveres para com a família, a comunidade e a humanidade.`n( ) Toda pessoa tem direito a um recurso simples e rápido ou a qualquer outro recurso efetivo, perante os juízes ou tribunais competentes, que a proteja contra atos que violem seus direitos fundamentais reconhecidos pela constituição, pela lei ou pela presente Convenção, mesmo quando tal violação seja cometida por pessoas que estejam atuando no exercício de suas funções oficiais.`n( ) Algumas disposições do Pacto de San José da Costa Rica podem excluir outros direitos e garantias que são inerentes ao ser humano ou que decorrem da forma democrática representativa de governo.`nAssinale a alternativa que apresenta a sequência correta de cima para baixo." "E" @(
    @{L="A"; T="V, V, V, V"}, @{L="B"; T="V, V, F, F"}, @{L="C"; T="V, F, F, V"}, @{L="D"; T="F, F, V, V"}, @{L="E"; T="F, V, V, F"}
)
$items += New-ItemPayload 58 "Direitos Humanos" "FACIL" $null "O Pacto Internacional dos Direitos Econômicos, Sociais e Culturais é caracterizado por veicular normas programáticas. Sobre os direitos e compromissos previstos no referido Pacto, assinale a alternativa incorreta." "C" @(
    @{L="A"; T="A escolha da escola pelos pais, independentemente das indicações das autoridades públicas é um direito"},
    @{L="B"; T="Determina o compromisso de todo Estado-parte elaborar um plano de ação para implementação progressiva da educação primária obrigatória e gratuita para todos"},
    @{L="C"; T="O direito à escolha do trabalho é limitado a depender das necessidades momentâneas de determinados profissionais"},
    @{L="D"; T="A greve é reconhecida como um direito"},
    @{L="E"; T="A previdência social é reconhecida como um direito"}
)
$items += New-ItemPayload 59 "Direitos Humanos" "MODERADO" $null "O Pacto Internacional dos Direitos Civis e Políticos (1966) instituiu um Comitê de Direitos Humanos. Sobre este, assinale a alternativa correta." "*" @(
    @{L="A"; T="Os Estados-partes devem enviar ao Comitê, sempre que solicitados, relatórios sobre as medidas por eles adotadas para concretizar os direitos mencionados no Pacto"},
    @{L="B"; T="O Comitê é composto por 28 membros"},
    @{L="C"; T="O quorum para instalação dos trabalhos é de 22 membros"},
    @{L="D"; T="O Comitê é integrado exclusivamente por americanos eleitos"},
    @{L="E"; T="Os membros do Comitê serão eleitos para um mandato de 2 anos"}
)
$items += New-ItemPayload 60 "Direitos Humanos" "MODERADO" $null "A Declaração de Pequim adotada pela Quarta Conferência Mundial sobre as mulheres, reconheceu as aspirações de todas as mulheres do mundo inteiro e levaram em consideração a diversidade das mulheres, suas funções e circunstâncias. Sobre sua apresentação, assinale a alternativa incorreta." "B" @(
    @{L="A"; T="Reafirma o seu compromisso com o reconhecimento da inalienabilidade, integralidade e indivisibilidade de todos os direitos humanos e liberdades fundamentais"},
    @{L="B"; T="Reafirma o compromisso com o reconhecimento do direto de todas as mulheres de controlar todos os aspectos de sua saúde, em particular sua própria fertilidade, exceto no que tange ao aborto, o qual é expressamente proibido"},
    @{L="C"; T="Reafirma o compromisso com o impulsionamento do consenso e do progresso alcançados nas anteriores Conferências das Nações Unidas, como sobre as Mulheres, em Nairóbi, sobre as Crianças, em New York e, sobre o Meio Ambiente e o Desenvolvimento, no Rio de Janeiro"},
    @{L="D"; T="Reafirma o compromisso com a determinação que é indispensável formular, implementar e monitorar, com a plena participação das mulheres, políticas e programas efetivos, eficientes e reforçadores do enfoque de gênero, incluindo políticas de desenvolvimento e programas que em todos os níveis busquem o fortalecimento e o avanço das mulheres"},
    @{L="E"; T="Reafirma o compromisso com a garantia do êxito da Plataforma de Ação em países cujas economias estejam em transição, o que requer continua cooperação e assistência internacional"}
)

# Q61 a Q65 - Direito Administrativo
$items += New-ItemPayload 61 "Direito Administrativo" "FACIL" $null "O artigo 37, parágrafo 1°, da Constituição Federal de 1988 dispõe o seguinte: '§1° A publicidade dos atos, programas, obras, serviços e campanhas dos órgãos públicos deverá ter caráter educativo, informativo ou de orientação social, dela não podendo constar nomes, símbolos ou imagens que caracterizem promoção pessoal de autoridades ou servidores públicos.' A expressão destacada tem relação com um princípio da Administração Pública encontrado na Constituição Federal. Assinale a alternativa correta que apresenta esse princípio." "C" @(
    @{L="A"; T="Princípio da especialidade"}, @{L="B"; T="Princípio da tutela"}, @{L="C"; T="Princípio da impessoalidade"}, @{L="D"; T="Princípio da hierarquia"}, @{L="E"; T="Princípio da continuidade do interesse público"}
)
$items += New-ItemPayload 62 "Direito Administrativo" "FACIL" $null "No que se refere aos atributos dos atos administrativos, analise as afirmativas abaixo e dê valores Verdadeiro (V) ou Falso (F).`n( ) A imperatividade é um atributo do ato administrativo.`n( ) A autoexecutoriedade é um atributo pelo qual o ato administrativo pode ser posto em execução pela própria Administração Pública, sem necessidade de intervenção do Poder Judiciário.`n( ) Para que um ato administrativo esteja em consonância com a lei e seja presumido legítimo é necessário uma intervenção estatal.`nAssinale a alternativa que apresenta a sequência correta de cima para baixo." "B" @(
    @{L="A"; T="V, V, V"}, @{L="B"; T="V, V, F"}, @{L="C"; T="V, F, V"}, @{L="D"; T="F, F, V"}, @{L="E"; T="F, V, F"}
)
$items += New-ItemPayload 63 "Direito Administrativo" "MODERADO" $null "Acerca dos Poderes da Administração Pública, em especial o Poder de Polícia, analise as afirmativas abaixo.`nI. A polícia administrativa rege-se pelo Direito Administrativo, incidindo sobre bens, direitos ou atividades.`nII. Costuma-se apontar como atributos do poder de polícia a discricionariedade, a autoexecutoriedade e a coercibilidade.`nIII. A polícia judiciária rege-se pelo Direito Processual Penal, incidindo sobre pessoas.`nAssinale a alternativa correta." "A" @(
    @{L="A"; T="As afirmativas I, II e III estão corretas"},
    @{L="B"; T="Apenas as afirmativas I e II estão corretas"},
    @{L="C"; T="Apenas as afirmativas II e III estão corretas"},
    @{L="D"; T="Apenas a afirmativa I está correta"},
    @{L="E"; T="Apenas a afirmativa II está correta"}
)
$items += New-ItemPayload 64 "Direito Administrativo" "FACIL" $null "Acerca das disposições da Constituição Federal de 1988 sobre a Administração Pública e os servidores públicos, assinale a alternativa incorreta." "D" @(
    @{L="A"; T="Os cargos, empregos e funções públicas são acessíveis aos brasileiros que preencham os requisitos estabelecidos em lei, assim como aos estrangeiros, na forma da lei"},
    @{L="B"; T="A investidura em cargo ou emprego público depende de aprovação prévia em concurso público de provas ou de provas e títulos, de acordo com a natureza e a complexidade do cargo ou emprego, na forma prevista em lei, ressalvadas as nomeações para cargo em comissão declarado em lei de livre nomeação e exoneração"},
    @{L="C"; T="É garantido ao servidor público civil o direito à livre associação sindical"},
    @{L="D"; T="A Constituição estipula um teto para a remuneração e o subsídio dos ocupantes de cargos, funções e empregos públicos da administração direta, autárquica e fundacional, mas não para os membros de qualquer dos Poderes da União, dos Estados, do Distrito Federal e dos Municípios, dos detentores de mandato eletivo e dos demais agentes políticos"},
    @{L="E"; T="A lei reservará percentual dos cargos e empregos públicos para as pessoas portadoras de deficiência e definirá os critérios de sua admissão"}
)
$items += New-ItemPayload 65 "Direito Administrativo" "MODERADO" $null "Sobre discricionariedade, vinculação e os elementos do ato administrativo, analise as afirmativas abaixo.`nI. Discricionariedade é sinônimo de arbitrariedade.`nII. A discricionariedade é verificada quando a lei deixa certa margem de liberdade de decisão diante do caso concreto, de tal modo que a autoridade poderá optar por uma dentre várias soluções possíveis, todas válidas perante o direito.`nIII. O exercício da discricionariedade comumente é verificado nos elementos motivo e objeto do ato administrativo.`nAssinale a alternativa correta." "C" @(
    @{L="A"; T="As afirmativas I, II e III estão corretas"},
    @{L="B"; T="Apenas as afirmativas I e II estão corretas"},
    @{L="C"; T="Apenas as afirmativas II e III estão corretas"},
    @{L="D"; T="Apenas a afirmativa I está correta"},
    @{L="E"; T="Apenas a afirmativa II está correta"}
)

# Q66 a Q70 - Direito Penal
$items += New-ItemPayload 66 "Direito Penal" "MODERADO" $null "A entrada em vigor da nova Lei de Drogas, revogando a anterior, fez com que o crime de porte de drogas para consumo pessoal deixasse de prever a aplicação de pena privativa de liberdade, passando a adotar sanções como advertência, prestação de serviços à comunidade e medida educativa. Nesse sentido, no que tange à pena aplicável ao autor do citado delito, é correto afirmar que a nova lei de drogas constitui um exemplo de:" "D" @(
    @{L="A"; T="novatio legis não incriminadora"}, @{L="B"; T="abolitio criminis"}, @{L="C"; T="novatio legis in pejus"}, @{L="D"; T="novatio legis in mellius"}, @{L="E"; T="lei intermediária"}
)
$items += New-ItemPayload 67 "Direito Penal" "FACIL" $null "Em face do crime de associação criminosa (art. 288 do Código Penal), assinale a alternativa correta." "E" @(
    @{L="A"; T="a pena aumenta-se até um terço se houver a participação de criança ou adolescente"},
    @{L="B"; T="trata-se de crime de concurso eventual de agentes"},
    @{L="C"; T="configura associação criminosa o ato de constituir, organizar ou manter grupo de pessoas com a finalidade de praticar crimes previstos no Código Penal"},
    @{L="D"; T="a pena aumenta-se até um terço se a associação é armada"},
    @{L="E"; T="configura associação criminosa o ato de associarem-se 3 (três) ou mais pessoas, para o fim específico de cometer crimes"}
)
$items += New-ItemPayload 68 "Direito Penal" "FACIL" $null "Assinale a alternativa que preencha corretamente a lacuna: Apresenta-se como causa excludente de ilicitude _____." "A" @(
    @{L="A"; T="o exercício regular de direito"}, @{L="B"; T="a inimputabilidade"}, @{L="C"; T="a coação moral irresistível"}, @{L="D"; T="a obediência hierárquica"}, @{L="E"; T="o erro sobre a ilicitude do fato"}
)
$items += New-ItemPayload 69 "Direito Penal" "FACIL" $null "Sobre a definição de crime de importunação sexual (art. 215-A do Código Penal), assinale a alternativa correta." "C" @(
    @{L="A"; T="ter conjunção carnal ou praticar outro ato libidinoso com alguém, mediante fraude ou outro meio que impeça ou dificulte a livre manifestação de vontade da vítima"},
    @{L="B"; T="constranger alguém, mediante violência ou grave ameaça, a ter conjunção carnal ou a praticar ou permitir que com ele se pratique outro ato libidinoso"},
    @{L="C"; T="praticar contra alguém e sem a sua anuência ato libidinoso com o objetivo de satisfazer a própria lascívia ou a de terceiro"},
    @{L="D"; T="induzir alguém menor de 14 (catorze) anos a satisfazer a lascívia de outrem"},
    @{L="E"; T="constranger alguém com o intuito de obter vantagem ou favorecimento sexual, prevalecendo-se o agente da sua condição de superior hierárquico ou ascendência inerentes ao exercício de emprego, cargo ou função"}
)
$items += New-ItemPayload 70 "Direito Penal" "FACIL" $null "Assinale a alternativa correta. Apresenta-se como conduta própria de contravenção penal o ato de:" "B" @(
    @{L="A"; T="obter, para si ou para outrem, vantagem ilícita, em prejuízo alheio, induzindo ou mantendo alguém em erro, mediante artifício, ardil ou qualquer outro meio fraudulento"},
    @{L="B"; T="recusar à autoridade, quando por esta, justificadamente solicitados ou exigidos, dados ou indicações concernentes à própria identidade, estado, profissão, domicílio e residência"},
    @{L="C"; T="adquirir, receber ou ocultar, em proveito próprio ou alheio, coisa que sabe ser produto de crime, ou influir para que terceiro, de boa-fé, a adquira, receba ou oculte"},
    @{L="D"; T="destruir, inutilizar ou deteriorar coisa alheia"},
    @{L="E"; T="apropriar-se de coisa alheia móvel, de que tem a posse ou a detenção"}
)

# Q71 a Q75 - Igualdade Racial e de Gênero
$items += New-ItemPayload 71 "Igualdade Racial e de Gênero" "FACIL" $null "O artigo 4° da Constituição Federal preocupou-se fundamentalmente com a definição dos princípios que devem orientar o Estado brasileiro nas suas relações internacionais. Leia atentamente os itens abaixo e, nos termos da Constituição de 1988, assinale a alternativa que não contém princípio regente das relações internacionais brasileiras." "A" @(
    @{L="A"; T="Pluralismo político"}, @{L="B"; T="Prevalência dos direitos humanos"}, @{L="C"; T="Repúdio ao terrorismo e ao racismo"}, @{L="D"; T="Cooperação entre os povos para o progresso da humanidade"}, @{L="E"; T="Concessão de asilo político"}
)
$items += New-ItemPayload 72 "Igualdade Racial e de Gênero" "FACIL" $null "Assinale a alternativa que apresenta corretamente órgão de assessoramento imediato ao Presidente da República nas questões sobre Políticas de promoção da Igualdade Racial" "B" @(
    @{L="A"; T="Ministério da Justiça"},
    @{L="B"; T="Secretaria Especial de Políticas de Promoção da Igualdade Racial"},
    @{L="C"; T="Secretaria de políticas públicas"},
    @{L="D"; T="Advogado-Geral da União"},
    @{L="E"; T="Secretaria Especial da Defensoria Pública"}
)
$items += New-ItemPayload 73 "Igualdade Racial e de Gênero" "MODERADO" $null "A Lei Federal n° 12.288 / 2010, institui o Estatuto da Igualdade Racial, destinado a garantir à população negra a efetivação da igualdade de oportunidades. Nos termos da lei, assinale a alternativa que indica corretamente o sentido de desigualdade de gênero e raça." "E" @(
    @{L="A"; T="o conjunto de pessoas que se autodeclaram pretas e pardas, conforme o quesito cor ou raça usado pela Fundação Instituto Brasileiro de Geografia e Estatística (IBGE), ou que adotam autodefinição análoga"},
    @{L="B"; T="toda situação injustificada de diferenciação de acesso e fruição de bens, serviços e oportunidades, nas esferas pública e privada, em virtude de raça, cor, descendência ou origem nacional ou étnica"},
    @{L="C"; T="toda distinção, exclusão, restrição ou preferência baseada em raça, cor, descendência ou origem nacional ou étnica que tenha por objeto anular ou restringir o reconhecimento, gozo ou exercício de direitos humanos"},
    @{L="D"; T="Os programas e medidas especiais adotados pelo Estado e pela iniciativa privada para a correção das desigualdades raciais e para a promoção da igualdade de oportunidades"},
    @{L="E"; T="Assimetria existente no âmbito da sociedade que acentua a distância social entre mulheres negras e os demais segmentos sociais"}
)
$items += New-ItemPayload 74 "Igualdade Racial e de Gênero" "MODERADO" $null "A Convenção Internacional sobre a eliminação de todas as formas de discriminação racial considera todos os homens iguais perante a lei. Sobre o papel dos Estados Partes, assinale a alternativa incorreta." "C" @(
    @{L="A"; T="Cada Estado Parte compromete-se a efetuar nenhum ato ou prática de discriminação racial contra pessoas, grupos de pessoas ou instituições e fazer com que todas as autoridades públicas nacionais ou locais, se conformem com esta obrigação"},
    @{L="B"; T="Cada Estado Parte compromete-se a não encorajar, defender ou apoiar a discriminação racial praticada por uma pessoa ou uma organização qualquer"},
    @{L="C"; T="Cada Estado Parte só não deverá tomar medidas eficazes a fim de rever as politicas governamentais nacionais e locais e para modificar, ab-rogar ou anular qualquer disposição regulamentar que tenha como objetivo criar a discriminação ou perpetra-la onde já existir"},
    @{L="D"; T="Cada Estado Parte deverá, por todos os meios apropriados, inclusive se as circunstâncias o exigirem, as medidas legislativas, proibir e por fim, a discriminação racial praticadas por pessoa, por grupo ou das organizações"},
    @{L="E"; T="Cada Estado Parte compromete-se a favorecer, quando for o caso as organizações e movimentos multi-raciais e outros meios próprios a eliminar as barreiras entre as raças e a desencorajar o que tende a fortalecer a divisão racial"}
)
$items += New-ItemPayload 75 "Igualdade Racial e de Gênero" "FACIL" $null "O Código Penal prevê, em seu artigo 140, a injúria racial como crime, considerando a ofensa feita a uma determinada pessoa com referência à sua raça, cor, etnia, religião ou origem. Sobre a injúria racial assinale a alternativa correta." "D" @(
    @{L="A"; T="Tem como bem jurídico a dignidade humana da coletividade"},
    @{L="B"; T="Trata-se de ação penal pública incondicionada"},
    @{L="C"; T="É imprescritível"},
    @{L="D"; T="Cabe fiança"},
    @{L="E"; T="A pena aplicada é detenção, de um a seis meses, ou multa"}
)

# Q76 a Q80 - Direito Penal Militar
$items += New-ItemPayload 76 "Direito Penal Militar" "FACIL" $null "Sobre o que constitui a conduta típica de crime militar de motim (art. 149 do CPM), assinale a alternativa correta." "B" @(
    @{L="A"; T="reunirem-se dois militares, com armamento de propriedade militar, praticando violência à coisa pública ou particular em lugar não sujeito à administração militar"},
    @{L="B"; T="reunirem-se militares desarmados agindo contra a ordem recebida de superior, ou negando-se a cumpri-la"},
    @{L="C"; T="reunirem-se mais de dois militares ou assemelhados, com material bélico de propriedade militar, praticando violência à pessoa em lugar sujeito à administração militar"},
    @{L="D"; T="deixar o militar de levar ao conhecimento do superior conspiração de cuja preparação teve notícia, ou, estando presente ao ato criminoso, não usar de todos os meios ao seu alcance para impedí-lo"},
    @{L="E"; T="reunirem-se militares armados, recusando obediência a superior, quando estejam agindo sem ordem ou praticando violência"}
)
$items += New-ItemPayload 77 "Direito Penal Militar" "FACIL" $null "Sobre o que configura conduta típica do crime de recusa de obediência (art. 163 do CPM), assinale a alternativa correta." "C" @(
    @{L="A"; T="desrespeitar superior diante de outro militar"},
    @{L="B"; T="despojar-se de uniforme, condecoração militar, insígnia ou distintivo, por menosprezo ou vilipêndio"},
    @{L="C"; T="recusar obedecer a ordem do superior sobre assunto ou matéria de serviço, ou relativamente a dever imposto em lei, regulamento ou instrução"},
    @{L="D"; T="promover a reunião de militares, ou nela tomar parte, para discussão de ato de superior ou assunto atinente à disciplina militar"},
    @{L="E"; T="praticar o militar diante da tropa, ou em lugar sujeito à administração militar, ato que se traduza em ultraje a símbolo nacional"}
)
$items += New-ItemPayload 78 "Direito Penal Militar" "FACIL" $null "O ato de 'retardar ou deixar de praticar, indevidamente, ato de ofício, ou praticá-lo contra expressa disposição de lei, para satisfazer interesse ou sentimento pessoal' configura o crime militar de:" "E" @(
    @{L="A"; T="abuso de confiança"}, @{L="B"; T="condescendência criminosa"}, @{L="C"; T="omissão de dever funcional"}, @{L="D"; T="retardamento de ato de ofício"}, @{L="E"; T="prevaricação"}
)
$items += New-ItemPayload 79 "Direito Penal Militar" "MODERADO" $null "No que se refere ao crime de deserção (art. 187 do CPM), é correto afirmar que:" "*" @(
    @{L="A"; T="configura exercício regular de direito o ato de evadir-se o militar do poder da escolta, permanecendo ausente por mais de oito dias"},
    @{L="B"; T="é isento de pena o oficial que deixa de proceder contra desertor, sabendo, ou devendo saber encontrar-se entre os seus comandados"},
    @{L="C"; T="constitui conduta lícita o ato de dar asilo a desertor ou facilitar-lhe transporte, conhecendo sua particular situação frente às normas militares"},
    @{L="D"; T="na deserção especial, a pena é aumentada de um terço, se se tratar de sargento, subtenente ou suboficial, e de metade, se oficial"},
    @{L="E"; T="se a deserção ocorre em unidade estacionada em fronteira ou país estrangeiro, a pena é agravada de metade"}
)
$items += New-ItemPayload 80 "Direito Penal Militar" "FACIL" $null "A ofensa à dignidade ou ao decoro são elementares que se fazem presentes expressamente no crime militar de:" "C" @(
    @{L="A"; T="desacato a assemelhado ou funcionário"}, @{L="B"; T="ingresso clandestino"}, @{L="C"; T="desacato a superior"}, @{L="D"; T="desobediência"}, @{L="E"; T="desacato a militar"}
)

$outFile = Join-Path $outputDir "pmba_soldado_2019_payload_api.json"
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
$json = $items | ConvertTo-Json -Depth 10
[System.IO.File]::WriteAllText($outFile, $json, $utf8NoBom)

Write-Host "PMBA Soldado 2019 gerado com sucesso! Total: $($items.Count) questões."
