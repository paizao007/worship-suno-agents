"""
Agente 1: Teólogo & Exegeta Bíblico.
Responsável por identificar a doutrina central do tema, sortear versículos canônicos pertinentes
e extrair a fundamentação bíblica, ortodoxia cristocêntrica, atributos divinos e salvaguardas doutrinárias.
"""

import random
import re
from typing import Type
from pydantic import BaseModel
from .base import BaseAgent
from schemas import UserBriefing, TheologicalDossier, ScriptureSuggestion


THEOLOGIAN_SYSTEM_PROMPT = """Você é um Teólogo e Exegeta Cristão de erudição bíblica profunda, especializado em Liturgia e Hinologia Sacra.
Sua missão é fornecer a fundamentação espiritual e doutrinária inegociável para uma canção de adoração a Deus.

DIRETRIZES FUNDAMENTAIS:
1. CENTRALIDADE VERTICAL (DOXOLOGIA): A adoração deve ser prioritariamente direcionada a Deus — quem Ele é (Seus atributos eternos) e o que Ele fez através de Cristo —, e NÃO centrada nas conquistas, ambições materiais ou no ego humano.
2. RIGOR EXEGÉTICO: Extraia o sentido fidedigno das passagens bíblicas citadas, respeitando o contexto canônico.
3. CRISTOCENTRISMO: Toda revelação de Deus culmina na pessoa e na obra redentora de Jesus Cristo (a Cruz, a Graça, a Ressurreição).
4. COMBATE AO ANTROPOCENTRISMO E CLICHÊS: Rejeite veementemente chavões gospel triunfalistas ("eu vou pisar nos meus inimigos", "eu nasci para vencer por meu mérito") ou sentimentalismos vazios.
5. VOCABULÁRIO SAGRADO: Forneça metáforas bíblicas legítimas e ricas em reverência e temor do Senhor.
"""


# Acervo Canônico Categorizado para Gestão Instantânea e Sorteio do Agente Teólogo
THEOLOGICAL_POOLS = [
    {
        "id": "amor_a_deus",
        "name": "Devoção & Amor Intenso a Deus (Primeiro Amor)",
        "keywords": ["amor a deus", "amar a deus", "amo a deus", "te amo deus", "te amo senhor", "primeiro amor", "devoção", "devocao", "intimidade", "sede de deus", "apaixonado por deus"],
        "verses": [
            "Marcos 12:30 (Amarás o Senhor teu Deus de todo o teu coração, de toda a tua alma e de todo o teu entendimento)",
            "Salmo 18:1 (Eu Te amo, ó Senhor, força minha, rocha minha e meu libertador)",
            "Salmo 73:25-26 (Quem tenho eu no céu além de Ti? E na terra não há quem eu deseje além de Ti)",
            "Salmo 42:1-2 (Como a corça anseia pelas correntes das águas, assim a minha alma suspira por Ti, ó Deus)",
            "1 João 4:19 (Nós O amamos porque Ele nos amou primeiro)",
            "Deuteronômio 6:5 (Amarás o Senhor teu Deus de todo o teu coração, de toda a tua alma e de toda a tua força)",
            "Salmo 63:1-3 (Ó Deus, Tu és o meu Deus, de madrugada Te buscarei; a Tua benignidade é melhor do que a vida)",
            "João 14:21 (Aquele que tem os Meus mandamentos e os guarda, esse é o que Me ama)",
            "Apocalipse 2:4-5 (Lembra-te de onde caíste, arrepende-te e volta à prática das primeiras obras do primeiro amor)"
        ],
        "attributes": ["Digno de Todo Afeto", "Fonte de Água Viva", "Noivo Celestial", "Amor Primeiro e Eterno"],
        "christ_focus": "Nosso amor a Deus nasce como resposta grata ao sacrifício de Cristo na cruz: nós O amamos porque Ele nos amou primeiro (1 João 4:19).",
        "sacred_words": ["Primeiro amor", "Todo o meu coração", "Minha alma tem sede", "Tesouro supremo", "Altar de adoração", "Chama viva", "Devoção sincera"],
        "guardrails": ["Evitar tratar o amor a Deus como sentimento romântico humano superficial; focar em aliança, reverência, entrega e obediência amorosa."],
        "tone": "Devoção ardente, entrega total, sede espiritual e intimidade reverente no Santo dos Santos."
    },
    {
        "id": "amor_de_deus",
        "name": "O Amor Sacrificial e Eterno de Deus (Ágape)",
        "keywords": ["amor", "ágape", "agape", "amou", "amado", "bondade", "misericórdia", "misericordia", "benignidade", "cuidado de deus"],
        "verses": [
            "1 João 4:7-10 (Nisto se manifestou o amor de Deus para conosco: em haver Deus enviado o Seu Filho Unigênito ao mundo)",
            "Romanos 5:8 (Mas Deus prova o Seu próprio amor para conosco pelo fato de ter Cristo morrido por nós, sendo nós ainda pecadores)",
            "João 3:16-17 (Porque Deus amou o mundo de tal maneira que deu o Seu Filho Unigênito, para que todo o que Nele crê não pereça)",
            "Efésios 3:17-19 (Compreender com todos os santos a largura, o comprimento, a altura e a profundidade do amor de Cristo)",
            "Romanos 8:38-39 (Nem a morte, nem a vida, nem principados poderão nos separar do amor de Deus que está em Cristo Jesus)",
            "Jeremias 31:3 (Com amor eterno Eu te amei; por isso, com laços de benignidade te atraí)",
            "1 Coríntios 13:4-8 (O amor é paciente, é benigno; tudo sofre, tudo crê, tudo espera, o amor jamais acaba)",
            "Sofonias 3:17 (O Senhor teu Deus está no meio de ti, poderoso para salvar; Ele te renovará no Seu amor)",
            "1 João 3:1 (Vede que grande amor nos tem concedido o Pai, a ponto de sermos chamados filhos de Deus)"
        ],
        "attributes": ["Amor Incondicional (Ágape)", "Misericórdia Infinita", "Paternidade Redentora", "Fidelidade na Aliança"],
        "christ_focus": "A cruz do Calvário é a manifestação suprema e histórica do amor de Deus (Romanos 5:8), onde o Justo morreu pelos injustos.",
        "sacred_words": ["Amor eterno", "Graça no Calvário", "Laços de ternura", "Filhos amados", "Amor que não falha", "Profundidade e altura", "Sacrifício de amor"],
        "guardrails": ["Não separar o amor de Deus de Sua justiça e da cruz de Cristo; o amor divino é santo e redentor."],
        "tone": "Maravilhamento, gratidão profunda, segurança paterna e adoração diante da cruz."
    },
    {
        "id": "santidade",
        "name": "Santidade Transcendente & Majestade do Trono de Deus",
        "keywords": ["santidade", "santo", "trono", "majestade", "glória", "gloria", "soberano", "altíssimo", "altissimo", "reverência", "temor", "isaías"],
        "verses": [
            "Isaías 6:1-4 (Vi o Senhor assentado sobre um alto e sublime trono, e os serafins clamavam: Santo, Santo, Santo é o Senhor dos Exércitos)",
            "Apocalipse 4:8-11 (Santo, Santo, Santo é o Senhor Deus, o Todo-Poderoso, que era, que é e que há de vir)",
            "Salmo 99:1-5 (O Senhor reina; exaltai ao Senhor nosso Deus e prostrai-vos ante o Seu estrado, porque Ele é Santo)",
            "Êxodo 15:11 (Quem é semelhante a Ti, ó Senhor, glorioso em santidade, terrível em feitos gloriosos, que operas maravilhas?)",
            "1 Pedro 1:15-16 (Segundo é santo Aquele que vos chamou, tornai-vos santos também vós em todo o vosso procedimento)",
            "Salmo 29:2 (Tributai ao Senhor a glória devida ao Seu nome; adorai ao Senhor na beleza da Sua santidade)",
            "Hebreus 12:28-29 (Retenhamos a graça, servindo a Deus com reverência e santo temor, porque o nosso Deus é fogo consumidor)",
            "Apocalipse 15:3-4 (Quem não temerá e não glorificará o Teu nome, ó Senhor? Pois só Tu és Santo)"
        ],
        "attributes": ["Santidade Inegociável (Kadosh)", "Majestade e Soberania Eterna", "Glória Transcendente", "Fogo Consumidor e Purificador"],
        "christ_focus": "Jesus é o Rei glorioso contemplado por Isaías (João 12:41) e o Cordeiro imolado no centro do trono celestial (Apocalipse 5).",
        "sacred_words": ["Alto e sublime trono", "Orlas do manto", "Serafins", "Santo, Santo, Santo", "Brasa viva", "Coroas aos Teus pés", "Beleza da santidade"],
        "guardrails": ["Jamais colocar o ser humano como centro; a visão da santidade de Deus gera quebrantamento, purificação e prontidão ('Eis-me aqui')."],
        "tone": "Reverência solene, assombro diante do Sagrado, quebrantamento e doxologia majestosa."
    },
    {
        "id": "graca_cruz",
        "name": "Graça Salvadora, Redenção & O Sacrifício da Cruz",
        "keywords": ["graça", "graca", "cruz", "redenção", "redencao", "sangue", "salvação", "salvacao", "calvário", "calvario", "cordeiro", "sacrifício", "sacrificio"],
        "verses": [
            "Efésios 2:8-9 (Porque pela graça sois salvos, mediante a fé; e isto não vem de vós, é dom de Deus; não de obras)",
            "Romanos 5:1-2 (Justificados, pois, mediante a fé, temos paz com Deus por meio de nosso Senhor Jesus Cristo)",
            "Isaías 53:4-5 (Ele foi traspassado pelas nossas transgressões e moído pelas nossas iniquidades; pelas Suas pisaduras fomos sarados)",
            "Tito 2:11-14 (Porque a graça de Deus se manifestou salvadora a todos os homens)",
            "Hebreus 9:12-14 (Pelo Seu próprio sangue, entrou no Santo dos Santos, havendo obtido eterna redenção)",
            "2 Coríntios 5:21 (Aquele que não conheceu pecado, Ele O fez pecado por nós, para que Nele fôssemos feitos justiça de Deus)",
            "Gálatas 2:20 (Já não sou eu quem vive, mas Cristo vive em mim; e esse viver que agora tenho na carne, vivo pela fé no Filho de Deus)"
        ],
        "attributes": ["Graça Imerecida", "Justiça Redentora", "Cordeiro Imaculado", "Perdão Pleno"],
        "christ_focus": "A obra consumada de Cristo no Gólgota ('Está consumado'), rasgando o véu do templo e reconciliando o pecador com o Pai.",
        "sacred_words": ["Precioso sangue", "Véu rasgado", "Graça que alcançou", "Madeiro da cruz", "Cordeiro imolado", "Eterna redenção", "Justificados pela fé"],
        "guardrails": ["Excluir qualquer noção de mérito próprio ou barganha espiritual; a salvação é 100% dom da graça mediante o sangue de Cristo."],
        "tone": "Profunda gratidão, contrição diante do Calvário e júbilo pela salvação consumada."
    },
    {
        "id": "provacao_refugio",
        "name": "Fidelidade Divina na Provação & Deus como Refúgio",
        "keywords": ["provação", "provacao", "perseverança", "perseveranca", "dor", "luta", "força", "forca", "refúgio", "refugio", "consolo", "deserto", "tempestade", "aflição"],
        "verses": [
            "Tiago 1:2-4 (Tende por motivo de toda alegria o passardes por várias provações, sabendo que a provação da fé produz perseverança)",
            "2 Coríntios 12:9 (A Minha graça te basta, porque o Meu poder se aperfeiçoa na fraqueza)",
            "Salmo 46:1-2 (Deus é o nosso refúgio e fortaleza, socorro bem presente nas tribulações)",
            "Salmo 91:1-4 (Aquele que habita no esconderijo do Altíssimo e descansa à sombra do Onipotente)",
            "Habacuque 3:17-18 (Ainda que a figueira não floresça, todavia eu me alegrarei no Senhor, exultarei no Deus da minha salvação)",
            "Salmo 23:1-4 (O Senhor é o meu Pastor, nada me faltará; ainda que eu ande pelo vale da sombra da morte, não temerei mal algum)",
            "Romanos 8:18 (Os sofrimentos do tempo presente não podem ser comparados com a glória a ser revelada em nós)"
        ],
        "attributes": ["Refúgio Inabalável", "Pastor Fiel no Vale", "Suficiência na Fraqueza", "Soberania nas Tempestades"],
        "christ_focus": "Cristo é a Rocha Eterna e o Bom Pastor que caminha conosco no vale e acalma os ventos com Sua voz.",
        "sacred_words": ["Esconderijo do Altíssimo", "Rocha inabalável", "Vale da sombra", "Tua graça me basta", "Âncora da alma", "Fogo refinador", "Socorro presente"],
        "guardrails": ["Evitar triunfalismo mágico ou negação da realidade da dor; enfatizar que a presença de Cristo sustenta e aperfeiçoa a fé na provação."],
        "tone": "Esperança firme, consolo profundo, confiança serena e entrega incondicional."
    },
    {
        "id": "louvor_gratidao",
        "name": "Louvor Congregacional, Ações de Graças & Júbilo ao Senhor",
        "keywords": ["gratidão", "gratidao", "louvor", "júbilo", "jubilo", "celebração", "celebracao", "vitória", "vitoria", "alegria", "festa", "exaltação"],
        "verses": [
            "Salmo 100:1-4 (Celebrai com júbilo ao Senhor, todas as terras; entrai por Suas portas com ações de graças e nos Seus átrios com hinos)",
            "Salmo 103:1-5 (Bendize, ó minha alma, ao Senhor, e tudo o que há em mim bendiga ao Seu santo nome)",
            "Salmo 150:1-6 (Louvai a Deus no Seu santuário; tudo quanto tem fôlego louve ao Senhor! Aleluia!)",
            "Filipenses 4:4 (Alegrai-vos sempre no Senhor; outra vez digo: alegrai-vos!)",
            "Colossenses 3:16 (Habite ricamente em vós a palavra de Cristo; louvando a Deus com salmos, hinos e cânticos espirituais)",
            "Salmo 34:1-3 (Bendirei o Senhor em todo o tempo, o Seu louvor estará sempre nos meus lábios)",
            "Salmo 118:24 (Este é o dia que o Senhor fez; regozijemo-nos e alegremo-nos nele)"
        ],
        "attributes": ["Bondade Eterna", "Fidelidade de Geração em Geração", "Digno de Todo Louvor", "Autor da Alegria"],
        "christ_focus": "Por meio de Jesus oferecemos continuamente a Deus sacrifício de louvor, que é o fruto de lábios que confessam o Seu nome (Hebreus 13:15).",
        "sacred_words": ["Portas com ações de graças", "Bendize ó minha alma", "Tudo o que tem fôlego", "Cânticos espirituais", "Júbilo nos átrios", "Aleluia ao Rei"],
        "guardrails": ["Manter a alegria centrada nos feitos e no caráter de Deus, não em vaidade humana."],
        "tone": "Celebração vibrante, júbilo congregacional, gratidão transbordante e exaltação festiva."
    },
    {
        "id": "espirito_santo",
        "name": "Pneumatologia: Derramamento, Fogo & Presença do Espírito Santo",
        "keywords": ["espírito", "espirito", "pentecostes", "avivamento", "fogo", "presença", "presenca", "unção", "uncao", "consolador", "vento"],
        "verses": [
            "Atos 2:1-4 (De repente veio do céu um som, como de um vento impetuoso, e todos foram cheios do Espírito Santo)",
            "João 14:16-17 (E Eu rogarei ao Pai, e Ele vos dará outro Consolador, a fim de que esteja para sempre convosco: o Espírito da verdade)",
            "Ezequiel 37:4-5 (Profetiza sobre estes ossos secos: Eis que farei entrar em vós o espírito, e vivereis)",
            "Romanos 8:26-27 (O mesmo Espírito intercede por nós sobremaneira, com gemidos inexprimíveis)",
            "Gálatas 5:22-25 (Mas o fruto do Espírito é: amor, alegria, paz, longanimidade, benignidade, bondade, fidelidade, mansidão, domínio próprio)",
            "Zacarias 4:6 (Não por força nem por violência, mas pelo Meu Espírito, diz o Senhor dos Exércitos)",
            "João 7:37-39 (Quem crer em Mim, como diz a Escritura, do seu interior fluirão rios de água viva)"
        ],
        "attributes": ["Espírito Consolador (Parakletos)", "Sopro de Vida do Criador", "Fogo Santificador", "Rios de Água Viva"],
        "christ_focus": "O Espírito Santo glorifica a Cristo (João 16:14), aplica a redenção ao coração do crente e prepara a Igreja como Noiva de Jesus.",
        "sacred_words": ["Vento impetuoso", "Fogo do altar", "Espírito da Verdade", "Rios de água viva", "Sopro de vida", "Habita em nós", "Consolador"],
        "guardrails": ["A obra do Espírito Santo sempre aponta para Cristo, produzindo santificação e fruto espiritual, nunca misticismo desordenado."],
        "tone": "Clamor por avivamento, sensibilidade espiritual, reverência e fome pela presença de Deus."
    },
    {
        "id": "fe_paz",
        "name": "Fé Inabalável, Confiança & A Paz que Excede Todo Entendimento",
        "keywords": ["fé", "fe", "confiança", "confianca", "esperança", "esperanca", "descanso", "paz", "promessa", "crer"],
        "verses": [
            "Hebreus 11:1 (Ora, a fé é a certeza de coisas que se esperam, a convicção de fatos que se não veem)",
            "Filipenses 4:6-7 (E a paz de Deus, que excede todo o entendimento, guardará o vosso coração e a vossa mente em Cristo Jesus)",
            "Isaías 40:31 (Mas os que esperam no Senhor renovam as suas forças, sobem com asas como águias)",
            "Provérbios 3:5-6 (Confia no Senhor de todo o teu coração e não te estribes no teu próprio entendimento)",
            "Mateus 11:28-29 (Vinde a Mim, todos os que estais cansados e sobrecarregados, e Eu vos aliviarei)",
            "João 14:27 (Deixo-vos a paz, a Minha paz vos dou; não vo-la dou como o mundo a dá)",
            "Lamentações 3:22-23 (As misericórdias do Senhor são a causa de não sermos consumidos; renovam-se a cada manhã)"
        ],
        "attributes": ["Fidelidade nas Promessas", "Príncipe da Paz", "Rocha dos Séculos", "Renovador das Forças"],
        "christ_focus": "Jesus é o Autor e Consumador da nossa fé (Hebreus 12:2) e a nossa verdadeira Paz.",
        "sacred_words": ["Asas como águias", "Paz que excede o entendimento", "Descanso da alma", "Fiel é o que prometeu", "Olhos fitos em Jesus", "Certeza viva"],
        "guardrails": ["A fé bíblica não é pensamento positivo humano, mas confiança plena no caráter e nas promessas de Deus."],
        "tone": "Paz profunda, serenidade, confiança firme e renovo espiritual."
    },
    {
        "id": "cura_restauracao",
        "name": "Cristo o Médico dos Médicos: Cura, Libertação & Restauração",
        "keywords": ["cura", "milagre", "restauração", "restauracao", "libertação", "libertacao", "enfermidade", "saúde", "saude", "vida"],
        "verses": [
            "Isaías 53:5 (O castigo que nos traz a paz estava sobre Ele, e pelas Suas pisaduras fomos sarados)",
            "Salmo 103:2-3 (É Ele quem perdoa todas as tuas iniquidades; quem sara todas as tuas enfermidades)",
            "Jeremias 17:14 (Cura-me, Senhor, e serei curado; salva-me, e serei salvo; porque Tu és o meu louvor)",
            "Lucas 4:18-19 (O Espírito do Senhor está sobre Mim, para proclamar libertação aos cativos e restaurar os oprimidos)",
            "Êxodo 15:26 (Porque Eu sou o Senhor que te sara — Jeová Rafá)",
            "malaquias 4:2 (Mas para vós outros, os que temeis o Meu nome, nascerá o Sol da Justiça, trazendo salvação e cura nas Suas asas)"
        ],
        "attributes": ["Jeová Rafá (O Senhor que Sara)", "Sol da Justiça", "Restaurador da Alma", "Poder Libertador"],
        "christ_focus": "Em Seu ministério terreno e na cruz, Jesus revelou o Reino de Deus curando enfermos, libertando cativos e vencendo a morte.",
        "sacred_words": ["Pelas Suas pisaduras", "Sol da Justiça", "Jeová Rafá", "Bálsamo de Gileade", "Toque nas vestes", "Vida em abundância"],
        "guardrails": ["Submeter o clamor por cura à soberania amorosa de Deus, exaltando a cura maior da alma juntamente com o poder divino de restaurar."],
        "tone": "Fé expectante, clamor humilde, gratidão pela restauração e exaltação ao poder de Cristo."
    },
    {
        "id": "volta_cristo",
        "name": "Saudade da Pátria Celestial & Esperança Gloriosa (Maranata)",
        "keywords": [
            "volta", "maranata", "eternidade", "ressurreição", "ressurreicao", "noiva",
            "reino", "céu", "ceu", "apocalipse", "segunda vinda", "saudade", "cidade",
            "celestial", "jerusalém", "jerusalem", "pátria", "patria", "peregrino",
            "morada", "mansão", "mansao", "eternal", "encontro"
        ],
        "verses": [
            "Hebreus 11:10-16 (Porque aguardava a cidade que tem fundamentos, da qual Deus é o arquiteto e edificador — uma pátria superior, isto é, celestial)",
            "Filipenses 3:20-21 (Pois a nossa pátria está nos céus, de onde também aguardamos o Salvador, o Senhor Jesus Cristo)",
            "Apocalipse 21:1-4 (Vi a Cidade Santa, a nova Jerusalém; e Deus enxugará dos olhos toda lágrima, e a morte já não existirá)",
            "Salmo 84:1-2 (Quão amáveis são os Teus tabernáculos, Senhor dos Exércitos! A minha alma tem saudade e desfalece pelos átrios do Senhor)",
            "Apocalipse 22:17-20 (O Espírito e a Noiva dizem: Vem! Aquele que dá testemunho destas coisas diz: Certamente venho sem demora! Ora, vem, Senhor Jesus!)",
            "João 14:1-3 (Na casa de Meu Pai há muitas moradas; vou preparar-vos lugar e voltarei para vos receber Comigo)",
            "1 Tessalonicenses 4:16-17 (Porquanto o Senhor mesmo, dada a Sua palavra de ordem, descerá dos céus ao som da trombeta de Deus, e assim estaremos para sempre com o Senhor)",
            "1 Coríntios 15:54-57 (Tragada foi a morte pela vitória! Graças a Deus, que nos dá a vitória por intermédio de nosso Senhor Jesus Cristo)"
        ],
        "attributes": ["Arquiteto da Cidade Celestial", "Rei dos Reis e Senhor dos Senhores", "Alfa e Ômega", "Noivo Esperado da Igreja"],
        "christ_focus": "Cristo ressurreto preparou para nós a Cidade Celestial e voltará em glória para buscar Sua Noiva, saciando toda saudade da alma no Reino Eterno.",
        "sacred_words": ["Cidade Celestial", "Saudade do lar", "Nova Jerusalém", "Maranata", "Ora vem Senhor Jesus", "Pátria nos céus", "Ruas de cristal", "Face a face com o Rei"],
        "guardrails": ["Evitar especulações de datas; focar na santa saudade da presença de Cristo, na esperança da ressurreição e no anseio pelo lar celestial."],
        "tone": "Santa saudade da eternidade, esperança gloriosa, clamor profético ('Maranata') e contemplação da Cidade Celestial."
    },
    {
        "id": "arrependimento",
        "name": "Contrição, Quebrantamento & Graça Purificadora",
        "keywords": ["arrependimento", "perdão", "perdao", "quebrantamento", "humildade", "confissão", "confissao", "pecado", "purificação", "misericórdia"],
        "verses": [
            "Salmo 51:10-17 (Cria em mim, ó Deus, um coração puro e renova dentro de mim um espírito inabalável; ao coração quebrantado e contrito não desprezarás)",
            "Isaías 57:15 (Habito no alto e santo lugar, mas habito também com o contrito e abatido de espírito, para vivificar o coração dos contritos)",
            "1 João 1:9 (Se confessarmos os nossos pecados, Ele é fiel e justo para nos perdoar os pecados e nos purificar de toda injustiça)",
            "2 Crônicas 7:14 (Se o Meu povo, que se chama pelo Meu nome, se humilhar, e orar, e me buscar, então Eu ouvirei dos céus)",
            "Salmo 32:1-5 (Bem-aventurado aquele cuja iniquidade é perdoada; confessei-Te o meu pecado e perdoaste a culpabilidade)",
            "Lucas 15:20-24 (Quando ainda estava longe, seu pai o viu, compadeceu-se dele e, correndo, o abraçou; este meu filho estava morto e reviveu)"
        ],
        "attributes": ["Rico em Perdoar", "Pai Compassivo", "Purificador dos Corações", "Justo e Fiel"],
        "christ_focus": "Em Cristo temos um Advogado junto ao Pai e o Seu sangue nos lava mais alvos que a neve.",
        "sacred_words": ["Coração quebrantado", "Cria em mim um coração puro", "Mais alvo que a neve", "Braços do Pai", "Misericórdia sem fim", "Purifica-me"],
        "guardrails": ["O arrependimento bíblico nunca termina em desespero, mas na alegria da restauração e do perdão conquistado por Cristo."],
        "tone": "Humildade profunda, sinceridade na confissão, quebrantamento e alívio gracioso no perdão."
    },
    {
        "id": "familia_alianca",
        "name": "Aliança Familiar & Edificação do Lar sobre a Rocha",
        "keywords": ["família", "familia", "casa", "filhos", "aliança", "alianca", "casamento", "lar", "gerações"],
        "verses": [
            "Josué 24:15 (Porém eu e a minha casa serviremos ao Senhor)",
            "Salmo 127:1 (Se o Senhor não edificar a casa, em vão trabalham os que a edificam)",
            "Salmo 128:1-4 (Bem-aventurado aquele que teme ao Senhor e anda nos Seus caminhos; a tua família será abençoada)",
            "Deuteronômio 6:6-7 (Estas palavras que hoje te ordeno estarão no teu coração; tu as inculcarás a teus filhos)",
            "Efésios 5:25-27 (Cristo amou a igreja e a si mesmo se entregou por ela, para a santificar)"
        ],
        "attributes": ["Deus de Aliança Geracional", "Edificador da Casa", "Guardião das Famílias"],
        "christ_focus": "Cristo é a Pedra Angular sobre a qual o lar cristão é edificado e o modelo supremo de amor sacrificial.",
        "sacred_words": ["Eu e a minha casa", "Edificada sobre a Rocha", "De geração em geração", "Altar na família", "Aliança eterna"],
        "guardrails": ["Manter Deus como o Senhor da família, evitando idolatria familiar e apontando o lar para o serviço ao Reino."],
        "tone": "Gratidão familiar, consagração do lar, bênção sacerdotal e aliança solene."
    },
    {
        "id": "humildade_crianca",
        "name": "Simplicidade, Pureza & Tornar-se como Criança (O Maior no Reino)",
        "keywords": [
            "criança", "crianca", "crianças", "criancas", "pequenos", "pequeninos",
            "como crianca", "como criança", "como uma crianca", "como uma criança",
            "tornar como crianca", "tornar como criança", "se tornar como crianca",
            "se tornar como uma crianca", "se tornar como uma criança", "se tornar como",
            "humildade", "simplicidade", "singeleza", "dependência", "dependencia",
            "colo do pai", "menino", "filhinhos", "infância espiritual", "puro coração",
            "puro coracao", "mansidão", "mansidao"
        ],
        "verses": [
            "Mateus 18:2-4 (Se não vos converterdes e não vos tornardes como crianças, de modo algum entrareis no Reino dos Céus; quem se humilhar como esta criança, esse é o maior)",
            "Marcos 10:14-15 (Deixai vir a Mim os pequeninos e não os embaraceis, porque dos tais é o Reino de Deus; quem não receber o Reino como uma criança, de modo nenhum entrará nele)",
            "Salmo 131:1-2 (Fiz calar e sossegar a minha alma, como a criança desmamada no colo de sua mãe; assim é a minha alma para comigo)",
            "Lucas 18:16-17 (Deixai vir a Mim as criancinhas; dos tais é o Reino de Deus)",
            "Mateus 11:25 (Graças Te dou, ó Pai, porque ocultaste estas coisas aos sábios e instruídos e as revelaste aos pequeninos)",
            "1 Pedro 2:2 (Desejai afetuosamente, como meninos recém-nascidos, o leite espiritual não falsificado, para que por ele cresçais)",
            "1 João 3:1 (Vede que grande amor nos tem concedido o Pai, a ponto de sermos chamados filhos de Deus)"
        ],
        "attributes": ["Pai de Ternura e Acolhimento", "Refúgio dos Humildes", "Soberano que Exalta os Pequeninos", "Graça aos Desvalidos"],
        "christ_focus": "Jesus acolheu as crianças em Seus braços, repreendeu a soberba humana e ensinou que o Reino pertence aos puros, humildes e totalmente dependentes do Pai.",
        "sacred_words": ["Como uma criança", "Colo do Pai", "Coração singelo", "Simplicidade e pureza", "O menor no Reino", "Descanso em Teus braços", "Dependência filial", "Abba Pai"],
        "guardrails": ["Não confundir ser como criança com imaturidade moral; a metáfora do Evangelho retrata a ausência de soberba, fé sincera e total dependência do Pai."],
        "tone": "Intimidade suave, pureza despretensiosa, ternura nos braços do Pai, descanso filial e adoração singela."
    },
    {
        "id": "batalha_espiritual",
        "name": "A Armadura de Deus, Oração & Vitória em Cristo",
        "keywords": ["armadura", "batalha", "guerra", "inimigo", "espada", "escudo", "firmes", "vencedores", "vencer", "efésios 6", "efesios 6"],
        "verses": [
            "Efésios 6:10-18 (Revesti-vos de toda a armadura de Deus, para poderdes ficar firmes contra as ciladas do diabo)",
            "2 Coríntios 10:4-5 (As armas da nossa milícia não são carnais, mas poderosas em Deus para destruir fortalezas)",
            "Romanos 8:37 (Em todas estas coisas, porém, somos mais que vencedores, por meio Daquele que nos amou)",
            "Salmo 91:5-7 (Não temerás o terror noturno nem a seta que voe de dia; mil cairão ao teu lado, mas tu não serás atingido)"
        ],
        "attributes": ["Senhor dos Exércitos (Jeová Sabaoth)", "Capitão da Nossa Salvação", "Vencedor da Morte", "Escudo Protetor"],
        "christ_focus": "Cristo desarmou os principados e potestades na cruz, triunfando sobre eles (Colossenses 2:15).",
        "sacred_words": ["Armadura de Deus", "Escudo da fé", "Espada do Espírito", "Mais que vencedores", "Poder da oração"],
        "guardrails": ["Manter a vitória fundada no sangue de Cristo e na autoridade da Sua Palavra, não em presunção humana."],
        "tone": "Fé resoluta, firmeza espiritual, autoridade em Cristo e vigilância santa."
    }
]

DEFAULT_POOL = {
    "id": "soberania_geral",
    "name": "Soberania, Criação & Glória de Cristo",
    "keywords": [],
    "verses": [
        "Salmo 145:1-7 (Exaltar-Te-ei, ó Deus meu e Rei; bendirei o Teu nome pelos séculos dos séculos)",
        "João 1:14-17 (E o Verbo se fez carne e habitou entre nós, cheio de graça e de verdade, e vimos a Sua glória)",
        "Apocalipse 5:9-13 (Digno é o Cordeiro que foi morto de receber o poder, e riqueza, e sabedoria, e força, e honra, e glória)",
        "Salmo 19:1-4 (Os céus proclamam a glória de Deus e o firmamento anuncia as obras das Suas mãos)",
        "Colossenses 1:15-17 (Ele é a imagem do Deus invisível, o primogênito de toda a criação; tudo foi criado por meio Dele e para Ele)",
        "Romanos 11:33-36 (Ó profundidade da riqueza, tanto da sabedoria como do conhecimento de Deus! Porque Dele, e por meio Dele, e para Ele são todas as coisas)"
    ],
    "attributes": ["Soberania Absoluta", "Criador e Sustentador", "Verbo Encarnado", "Digno de Toda Glória"],
    "christ_focus": "Em Cristo habita corporalmente toda a plenitude da divindade; por meio Dele e para Ele foram criadas todas as coisas.",
    "sacred_words": ["Digno é o Cordeiro", "Verbo da Vida", "Dele por Ele e para Ele", "Rei da Glória", "Fidelidade eterna"],
    "guardrails": ["Manter a centralidade teocêntrica e cristocêntrica em cada estrofe."],
    "tone": "Solene exaltação, reverência e celebração da grandeza de Deus."
}


THEOLOGICAL_DOSSIER_JSON_EXAMPLE = """{
  "theme_title": "Identificação Doutrinária Precisa — Referência Bíblica Principal",
  "exegetical_summary": "Reflexão exegética cristocêntrica profunda conectando o tema ao versículo de forma fidedigna e sem clichês.",
  "primary_scriptures": [
    "Livro Capítulo:Versículo (Texto resumido)",
    "Passagem complementar (Texto)"
  ],
  "divine_attributes": ["Atributo Eterno de Deus 1", "Atributo 2", "Atributo 3"],
  "christocentric_focus": "Como a pessoa e a obra de Jesus Cristo são o centro desta mensagem espiritual.",
  "sacred_keywords": ["Metáfora Bíblica 1", "Expressão Sagrada 2", "Expressão 3"],
  "doctrinal_guardrails": ["Princípios para evitar desvios, antropocentrismo ou sentimentalismos superficiais."],
  "emotional_and_spiritual_tone": "Atmosfera devocional precisa (ex: intimidade suave, descanso filial, reverência solene)."
}"""


class TheologianAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Teólogo & Exegeta",
            role="Guardião Doutrinário e Analista Hermenêutico",
            system_prompt=THEOLOGIAN_SYSTEM_PROMPT,
        )

    def _match_pool(self, theme: str) -> dict:
        """Identifica a categoria doutrinária exata a partir do tema digitado pelo usuário."""
        t_lower = (theme or "").strip().lower()
        for category in THEOLOGICAL_POOLS:
            for kw in category["keywords"]:
                if kw in t_lower:
                    return category
        return DEFAULT_POOL

    def analyze_and_draw_scripture(self, theme: str, exclude_current: str = "") -> dict:
        """
        Gestão do Agente Teólogo (Instantânea):
        1. Identifica o tema doutrinário a partir do que o usuário escreveu.
        2. Sorteia 1 versículo bíblico específico daquele tema (garantindo não repetir o atual).
        3. Retorna metadados completos da gestão do agente para exibição na interface.
        """
        theme_clean = (theme or "").strip()
        if not theme_clean:
            theme_clean = "Louvor e Adoração a Deus"

        matched = self._match_pool(theme_clean)
        identified_name = matched["name"]
        if matched["id"] == "soberania_geral":
            identified_name = f"Exegese Cristocêntrica sobre '{theme_clean}'"

        pool = list(matched["verses"])
        exclude_clean = (exclude_current or "").strip()

        # Filtra o versículo que já está no campo para que cada clique sorteie um DIFERENTE
        available = [v for v in pool if v != exclude_clean and v.split(" (")[0] not in exclude_clean]
        if not available:
            available = pool

        chosen_verse = random.choice(available)
        others = [v for v in pool if v != chosen_verse]
        extra_samples = random.sample(others, k=min(2, len(others)))

        # Extrai a referência curta e o texto devocional entre parênteses para compor a Reflexão Bíblica
        if "(" in chosen_verse and ")" in chosen_verse:
            ref_part = chosen_verse.split("(")[0].strip()
            text_part = chosen_verse.split("(", 1)[1].rsplit(")", 1)[0].strip()
        else:
            ref_part = chosen_verse
            text_part = chosen_verse

        biblical_reflection = (
            f"Meditação em {ref_part}: \"{text_part}\". "
            f"Sob o tema '{theme_clean}' ({identified_name}), esta passagem revela {', '.join(matched['attributes'][:2]).lower()} "
            f"e nos conduz a {matched['christ_focus'][0].lower() + matched['christ_focus'][1:]}"
        )

        return {
            "identified_theme": identified_name,
            "chosen_verse": chosen_verse,
            "biblical_reflection": biblical_reflection,
            "pool_size": len(pool),
            "scriptures": [chosen_verse] + extra_samples,
            "formatted": chosen_verse,
            "category_data": matched,
        }

    def suggest_scriptures(self, theme: str, exclude_current: str = "") -> list[str]:
        """Retorna a lista de versículos sorteados pelo Agente Teólogo após identificar o tema."""
        analysis = self.analyze_and_draw_scripture(theme, exclude_current=exclude_current)
        return analysis["scriptures"]

    def run(self, briefing: UserBriefing) -> TheologicalDossier:
        biblical_info = (briefing.biblical_reference or "").strip()
        if not biblical_info:
            analysis = self.analyze_and_draw_scripture(briefing.theme)
            biblical_info = analysis["chosen_verse"]
            briefing.biblical_reference = biblical_info

        prompt = f"""Analise este pedido de canção de adoração cristã e construa o Dossier Teológico completo:
Tema: {briefing.theme}
Passagens Bíblicas Base: {biblical_info}
Estilo e Clima: {briefing.musical_style_hint} | {briefing.tempo_hint}
Preferência Vocal: {briefing.vocal_preference}
Instruções Adicionais: {briefing.user_prompt or 'Nenhuma'}

IMPORTANTE: 
1. Respeite rigorosamente o sentido e o contexto do Tema e das Passagens Bíblicas Base informadas!
2. Se o tema for sobre simplicidade, pureza ou tornar-se como criança (Mateus 18, Marcos 10, Salmo 131), todo o dossiê DEVE refletir intimidade suave, dependência filial, acolhimento nos braços do Pai e ausência de soberba, NUNCA imponência bélica ou triunfalismo descontextualizado.
"""
        return self.call_llm(prompt, TheologicalDossier, custom_json_example=THEOLOGICAL_DOSSIER_JSON_EXAMPLE)

    def _generate_contextual_demonstration(self, user_prompt: str, response_model: Type[BaseModel]) -> BaseModel:
        # Extrai o tema real e a passagem bíblica real do prompt
        theme_match = re.search(r"Tema:\s*(.+)", user_prompt)
        ref_match = re.search(r"Passagens Bíblicas Base:\s*(.+)", user_prompt)
        extracted_theme = theme_match.group(1).strip() if theme_match else user_prompt
        extracted_ref = ref_match.group(1).strip() if ref_match else ""

        analysis = self.analyze_and_draw_scripture(extracted_theme)
        cat = analysis["category_data"]

        if response_model == ScriptureSuggestion:
            return ScriptureSuggestion(
                identified_theme=analysis["identified_theme"],
                scriptures=analysis["scriptures"]
            )

        chosen_ref = extracted_ref if extracted_ref else analysis["chosen_verse"]
        if "(" in chosen_ref and ")" in chosen_ref:
            ref_short = chosen_ref.split("(")[0].strip()
            ref_meaning = chosen_ref.split("(", 1)[1].rsplit(")", 1)[0].strip()
        else:
            ref_short = chosen_ref
            ref_meaning = chosen_ref

        primary_refs = [chosen_ref]
        for s in analysis["scriptures"]:
            if s not in primary_refs:
                primary_refs.append(s)

        exegetical_reflection = (
            f"Reflexão Bíblica em {ref_short} (\"{ref_meaning}\"): "
            f"A canção exalta '{extracted_theme}' dentro da doutrina de {cat['name']}, "
            f"destacando {', '.join(cat['attributes'][:3]).lower()}. "
            f"Foco Cristocêntrico: {cat['christ_focus']}"
        )

        return TheologicalDossier(
            theme_title=f"{analysis['identified_theme']} — {ref_short}",
            primary_scriptures=primary_refs[:3],
            divine_attributes=cat["attributes"],
            christocentric_focus=cat["christ_focus"],
            sacred_keywords=cat["sacred_words"],
            doctrinal_guardrails=cat["guardrails"],
            emotional_and_spiritual_tone=cat["tone"],
            exegetical_summary=exegetical_reflection
        )

