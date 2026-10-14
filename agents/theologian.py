"""
Agente 1: Teólogo & Exegeta Bíblico (100% Pesquisa Analítica e Dinâmica).
Lê o tema livre do usuário, pesquisa as Sagradas Escrituras, identifica o contexto histórico/canônico,
extrai as passagens mais pertinentes com seu texto literal e constrói o dossiê doutrinário cristocêntrico.
Zero categorias engessadas: os agentes leem, pesquisam e compreendem o tema em profundidade.
"""

import random
import re
from typing import Type
from pydantic import BaseModel, Field
from .base import BaseAgent
from schemas import UserBriefing, TheologicalDossier, ScriptureSuggestion


THEOLOGIAN_SYSTEM_PROMPT = """Você é um Teólogo e Exegeta Cristão de alta erudição bíblica, especializado em Liturgia e Hinologia Sacra.
Sua missão é realizar a pesquisa canônica profunda e a exegese espiritual do TEMA que o usuário fornecer.

DIRETRIZES FUNDAMENTAIS DE PESQUISA:
1. COMPREENSÃO INTEGRAL DO TEMA: Analise o coração espiritual do tema que o usuário informou (seja uma narrativa bíblica, uma doutrina, uma oração ou uma parábola de Jesus). Não use categorias prontas ou genéricas.
2. RIGOR CANÔNICO: Encontre passagens bíblicas reais, fidedignas e contextuais que tratem exatamente do assunto proposto, com livro, capítulo e versículo citados com precisão.
3. CENTRALIDADE EM CRISTO (CRISTOCENTRISMO): Mostre como o tema aponta para a pessoa e a obra de Jesus Cristo (Sua vida, Sua cruz, Sua ressurreição ou Seu Reino eterno).
4. COMBATE A CHAVÕES E ANTROPOCENTRISMO: Rejeite triunfalismos vazios ou clichês superficiais. A adoração é vertical: quem Deus é e o que Ele fez.
5. VOCABULÁRIO SAGRADO: Forneça imagens e metáforas bíblicas legítimas e adequadas à atmosfera espiritual do tema.
"""


class ScriptureResearchResult(BaseModel):
    """Resultado da pesquisa bíblica dinâmica do Agente Teólogo."""
    identified_theme: str = Field(description="Síntese doutrinária profunda e exata do tema de adoração")
    chosen_verse: str = Field(description="Versículo bíblico principal com citação e texto exato entre parênteses: Livro Cap:Vers (Texto)")
    complementary_verses: list[str] = Field(description="1 a 2 outras passagens bíblicas canônicas complementares")
    biblical_reflection: str = Field(description="Reflexão bíblica e exegética fidedigna conectando o tema ao versículo")
    divine_attributes: list[str] = Field(description="Atributos eternos de Deus revelados neste tema")
    christocentric_focus: str = Field(description="Como este tema aponta para a pessoa e a obra redentora de Jesus Cristo")
    sacred_keywords: list[str] = Field(description="Palavras sagradas e metáforas bíblicas adequadas")
    emotional_and_spiritual_tone: str = Field(description="Atmosfera devocional recomendada (ex: intimidade suave, descanso filial, reverência solene, celebração)")
    doctrinal_guardrails: list[str] = Field(description="Salvaguardas doutrinárias para evitar clichês ou desvios")


RESEARCH_JSON_EXAMPLE = """{
  "identified_theme": "Síntese doutrinária exata do tema pesquisado",
  "chosen_verse": "Livro Cap:Vers (Texto bíblico exato e fiel da passagem)",
  "complementary_verses": [
    "Outro Livro Cap:Vers (Texto complementar relevante)"
  ],
  "biblical_reflection": "Exegese bíblica aprofundada conectando o coração do tema à Palavra de Deus e a Cristo.",
  "divine_attributes": ["Atributo de Deus 1", "Atributo 2", "Atributo 3"],
  "christocentric_focus": "Como este tema culmina na graça e na obra de Jesus Cristo.",
  "sacred_keywords": ["Metáfora Bíblica 1", "Metáfora 2", "Expressão Sagrada 3"],
  "emotional_and_spiritual_tone": "Atmosfera litúrgica e emocional precisa",
  "doctrinal_guardrails": ["Princípios para preservar a ortodoxia e evitar clichês"]
}"""


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
  "emotional_and_spiritual_tone": "Atmosfera devocional precisa (ex: intimidade suave, descanso filial, reverência solene).",
  "theme_title": "Título Teológico Preciso (Referência Bíblica)"
}"""


# Léxico Canônico Amplo para Pesquisa Semântica Rápida e Contingência Autônoma
BIBLICAL_CANONICAL_INDEX = [
    {
        "tokens": ["criança", "crianca", "crianças", "criancas", "pequeno", "pequenino", "humild", "simplicidade", "singel", "colo", "desmamada", "menino", "filhinho"],
        "identified_theme": "Simplicidade, Pureza & Tornar-se como Criança (O Maior no Reino)",
        "chosen_verse": "Mateus 18:2-4 (Se não vos converterdes e não vos tornardes como crianças, de modo algum entrareis no Reino dos Céus; quem se humilhar como esta criança, esse é o maior)",
        "complementary_verses": [
            "Marcos 10:14-15 (Deixai vir a Mim os pequeninos e não os embaraceis, porque dos tais é o Reino de Deus; quem não receber o Reino como uma criança, de modo nenhum entrará nele)",
            "Salmo 131:1-2 (Fiz calar e sossegar a minha alma, como a criança desmamada no colo de sua mãe; assim é a minha alma para comigo)",
            "Mateus 11:25 (Graças Te dou, ó Pai, porque ocultaste estas coisas aos sábios e instruídos e as revelaste aos pequeninos)"
        ],
        "attributes": ["Pai de Ternura e Acolhimento", "Refúgio dos Humildes", "Soberano que Exalta os Pequeninos"],
        "christ_focus": "Jesus colocou a criança no centro como o modelo supremo de humildade, pureza e dependência do Reino de Deus.",
        "sacred_keywords": ["Como uma criança", "Colo do Pai", "Coração singelo", "Simplicidade e pureza", "O menor no Reino", "Descanso em Teus braços"],
        "tone": "Intimidade suave, pureza despretensiosa, ternura nos braços do Pai, descanso filial e adoração singela.",
        "guardrails": ["Não confundir ser como criança com imaturidade moral; a metáfora bíblica é sobre pureza, ausência de soberba e dependência total do Pai."]
    },
    {
        "tokens": ["cura", "curado", "sarado", "sara", "jeová rafá", "jeova rafa", "enfermidade", "saúde", "saude", "médico", "medico", "pisaduras", "bálsamo", "balsamo"],
        "identified_theme": "Cristo o Médico dos Médicos: Cura, Libertação & Restauração",
        "chosen_verse": "Isaías 53:5 (O castigo que nos traz a paz estava sobre Ele, e pelas Suas pisaduras fomos sarados)",
        "complementary_verses": [
            "Êxodo 15:26 (Porque Eu sou o Senhor que te sara — Jeová Rafá)",
            "Lucas 4:18-19 (O Espírito do Senhor está sobre Mim para curar os quebrantados de coração e libertar os cativos)",
            "Salmo 103:2-3 (Bendize ó minha alma ao Senhor, que sara todas as tuas enfermidades)"
        ],
        "attributes": ["Jeová Rafá (O Senhor que Sara)", "Sol da Justiça", "Restaurador da Alma", "Poder Libertador"],
        "christ_focus": "Na cruz e em Seu ministério, Cristo tomou sobre Si as nossas dores e enfermidades, manifestando o Reino de Deus.",
        "sacred_keywords": ["Pelas Suas pisaduras", "Sol da Justiça", "Bálsamo de Gileade", "Toque nas vestes", "Vida em abundância"],
        "tone": "Fé expectante, clamor humilde, gratidão pela restauração e exaltação ao poder de Cristo.",
        "guardrails": ["Submeter o clamor por cura à soberania amorosa de Deus, exaltando a cura eterna da alma."]
    },
    {
        "tokens": ["ossos", "secos", "vale de ossos", "vale de ossos secos", "ezequiel", "ezequiel 37", "renovo", "ressurreição", "ressurreicao", "sopro de vida", "quatro ventos", "profetiza aos ossos"],
        "identified_theme": "O Vale de Ossos Secos: O Sopro do Espírito & Ressurreição Sobrenatural",
        "chosen_verse": "Ezequiel 37:4-5 (Profetiza sobre estes ossos secos e dize-lhes: Ossos secos, ouvi a palavra do Senhor! Eis que farei entrar em vós o espírito, e vivereis)",
        "complementary_verses": [
            "Ezequiel 37:9-10 (Vem dos quatro ventos, ó espírito, e assopra sobre estes mortos, para que vivam. E o espírito entrou neles, e viveram)",
            "Romanos 8:11 (Se o Espírito Daquele que ressuscitou a Jesus dentre os mortos habita em vós, vivificará também os vossos corpos mortais)",
            "João 11:25 (Eu sou a ressurreição e a vida; quem crê em Mim, ainda que esteja morto, viverá)"
        ],
        "attributes": ["Deus Vivificador", "Senhor do Sopro da Vida (Ruach)", "Deus que Traz Vida do Vale", "Todo-Poderoso"],
        "christ_focus": "Cristo é a Ressurreição e a Vida, Aquele que pela Sua Palavra e Espírito faz o deserto florescer e os ossos secos se levantarem como um exército vivo.",
        "sacred_keywords": ["Sopro dos quatro ventos", "Ossos secos ouvi a palavra", "Espírito vivificador", "Ressurreição e vida", "Exército que se levanta"],
        "tone": "Clamor profético solene, fé vibrante na ressurreição, triunfo do Espírito sobre a morte e autoridade espiritual.",
        "guardrails": ["Enfatizar que o milagre acontece unicamente pelo poder da Palavra de Deus e do Seu Espírito, jamais por mérito humano."]
    },
    {
        "tokens": ["cego", "jericó", "jerico", "bartimeu", "cegueira", "enxergar", "olhos", "filho de davi", "misericórdia", "misericordia", "abrir os olhos"],
        "identified_theme": "A Cura do Cego de Jericó (Bartimeu) & A Misericórdia do Filho de Davi",
        "chosen_verse": "Lucas 18:41-42 (Que queres que Eu te faça? E ele disse: Senhor, que eu veja! E Jesus lhe disse: Vê; a tua fé te salvou)",
        "complementary_verses": [
            "Marcos 10:49-52 (Jesus parou e disse: Chamai-o. Lançando de si a capa, levantou-se e foi até Jesus... E logo viu, e seguia a Jesus pelo caminho)",
            "Salmo 146:8 (O Senhor abre os olhos aos cegos; o Senhor levanta os abatidos; o Senhor ama os justos)",
            "João 9:25 (Uma coisa sei: eu era cego e agora vejo!)"
        ],
        "attributes": ["Filho de Davi", "Cheio de Misericórdia e Compaixão", "A Luz que Dissipa as Trevas", "Aquele que Ouve o Clamor"],
        "christ_focus": "Jesus ouve o clamor dos abatidos à beira do caminho, detém os Seus passos para acolher o necessitado e abre os olhos físicos e espirituais para Sua luz.",
        "sacred_keywords": ["Jesus Filho de Davi tem compaixão", "Senhor que eu veja", "A tua fé te salvou", "Deixar a velha capa", "Eu era cego e agora vejo"],
        "tone": "Clamor urgente e humilde, fé perseverante, alegria transbordante ao ver a Luz e consagração ao seguir a Cristo pelo caminho.",
        "guardrails": ["Destacar a graça de Jesus em parar para ouvir o clamor de quem a multidão mandava calar."]
    },
    {
        "tokens": ["pastor", "bom pastor", "salmo 23", "ovelha", "pastos", "águas de descanso", "águas tranquilas", "cajado", "vale da sombra"],
        "identified_theme": "O Senhor é o Meu Pastor: Cuidado, Condução & Descanso da Alma",
        "chosen_verse": "Salmo 23:1-3 (O Senhor é o meu pastor; nada me faltará. Ele me faz repousar em pastos verdejantes e me guia suavemente a águas de descanso; refrigera a minha alma)",
        "complementary_verses": [
            "João 10:11-14 (Eu sou o Bom Pastor; o Bom Pastor dá a vida pelas Suas ovelhas... Eu conheço as Minhas ovelhas e as Minhas ovelhas Me conhecem)",
            "Salmo 23:4-6 (Ainda que eu ande pelo vale da sombra da morte, não temerei mal algum, porque Tu estás comigo; a Tua vara e o Teu cajado me consolam)",
            "Isaías 40:11 (Como pastor apascentará o Seu rebanho; entre os Seus braços recolherá os cordeirinhos e os levará no Seu regaço)"
        ],
        "attributes": ["Bom Pastor da Alma", "Provedor Fiel (Jeová Jireh)", "Guia Compassivo", "Presença Protetora no Vale"],
        "christ_focus": "Jesus é o Bom Pastor que deu Sua vida pelo rebanho na cruz e nos conduz com amor às mansões celestiais.",
        "sacred_keywords": ["O Senhor é o meu Pastor", "Águas de descanso", "Refrigera a minha alma", "Vara e cajado me consolam", "Cálice que transborda"],
        "tone": "Paz reconfortante, descanso pleno, gratidão filial e segurança inabalável.",
        "guardrails": ["Focar na dependência serena e na providência amorosa do Bom Pastor."]
    },
    {
        "tokens": ["volta", "maranata", "segunda vinda", "arrebatamento", "trombeta", "encontro", "noiva", "pátria", "patria", "jerusalém", "jerusalem", "céu", "ceu", "saudade"],
        "identified_theme": "Saudade da Pátria Celestial & Esperança Gloriosa (Maranata)",
        "chosen_verse": "1 Tessalonicenses 4:16-17 (O Senhor mesmo descerá dos céus ao som da trombeta de Deus, e assim estaremos para sempre com o Senhor)",
        "complementary_verses": [
            "Apocalipse 22:17-20 (O Espírito e a Noiva dizem: Vem! Certamente venho sem demora! Ora, vem, Senhor Jesus!)",
            "Filipenses 3:20-21 (A nossa pátria está nos céus, de onde também aguardamos o Salvador, o Senhor Jesus Cristo)",
            "Apocalipse 21:1-4 (Vi a Cidade Santa, a nova Jerusalém; e Deus enxugará dos olhos toda lágrima)"
        ],
        "attributes": ["Arquiteto da Cidade Celestial", "Rei dos Reis", "Alfa e Ômega", "Noivo Esperado"],
        "christ_focus": "Cristo voltará em glória para buscar Sua Igreja e saciar toda saudade do coração humano na eternidade.",
        "sacred_keywords": ["Cidade Celestial", "Nova Jerusalém", "Maranata", "Ora vem Senhor Jesus", "Pátria nos céus", "Ruas de cristal"],
        "tone": "Santa saudade da eternidade, esperança gloriosa, clamor profético ('Maranata') e júbilo celestial.",
        "guardrails": ["Evitar especulações de datas; focar no amor da Noiva por Cristo e na perseverança da fé."]
    },
    {
        "tokens": ["cruz", "graça", "graca", "sangue", "redenção", "redencao", "calvário", "calvario", "cordeiro", "perdão", "perdao", "salvação", "salvacao"],
        "identified_theme": "Graça Salvadora, Redenção & O Sacrifício da Cruz",
        "chosen_verse": "Efésios 2:8-9 (Porque pela graça sois salvos, mediante a fé; e isto não vem de vós, é dom de Deus; não de obras)",
        "complementary_verses": [
            "Romanos 5:8 (Deus prova o Seu próprio amor para conosco pelo fato de ter Cristo morrido por nós, sendo nós ainda pecadores)",
            "Gálatas 2:20 (Já não sou eu quem vive, mas Cristo vive em mim)",
            "Hebreus 9:12 (Pelo Seu próprio sangue, entrou no Santo dos Santos, havendo obtido eterna redenção)"
        ],
        "attributes": ["Graça Imerecida", "Justiça Redentora", "Cordeiro Imaculado", "Perdão Pleno"],
        "christ_focus": "A obra consumada de Cristo no Calvário reconciliou para sempre o homem com o Pai.",
        "sacred_keywords": ["Precioso sangue", "Véu rasgado", "Graça que alcançou", "Madeiro da cruz", "Cordeiro imolado"],
        "tone": "Profunda contrição, gratidão diante do Calvário e júbilo pela salvação consumada.",
        "guardrails": ["Excluir méritos humanos; a salvação é inteiramente graça de Deus mediante a fé em Jesus."]
    },
    {
        "tokens": ["santo", "santidade", "trono", "majestade", "serafins", "soberano", "altíssimo", "altissimo", "glória", "gloria", "temor", "reverência", "reverencia"],
        "identified_theme": "Santidade Transcendente & Majestade do Trono de Deus",
        "chosen_verse": "Isaías 6:1-3 (Vi o Senhor assentado sobre um alto e sublime trono; e os serafins clamavam: Santo, Santo, Santo é o Senhor dos Exércitos)",
        "complementary_verses": [
            "Apocalipse 4:8-11 (Santo, Santo, Santo é o Senhor Deus, o Todo-Poderoso, que era, que é e que há de vir)",
            "Salmo 99:1-5 (O Senhor reina; prostrai-vos ante o Seu estrado, porque Ele é Santo)",
            "Hebreus 12:28-29 (Sirvamos a Deus com reverência e santo temor, porque o nosso Deus é fogo consumidor)"
        ],
        "attributes": ["Santidade Inegociável (Kadosh)", "Majestade Eterna", "Glória Transcendente", "Fogo Consumidor"],
        "christ_focus": "Jesus é o Rei da Glória contemplado pelos profetas e o Cordeiro no centro do trono celestial.",
        "sacred_keywords": ["Alto e sublime trono", "Orlas do manto", "Santo, Santo, Santo", "Brasa viva", "Beleza da santidade"],
        "tone": "Reverência solene, assombro diante do Sagrado, quebrantamento e doxologia majestosa.",
        "guardrails": ["Nunca rebaixar a glória divina; a visão da santidade gera adoração pura e submissão."]
    },
    {
        "tokens": ["provação", "provacao", "deserto", "tempestade", "refúgio", "refugio", "fortaleza", "consolo", "dor", "luta", "lágrima", "lagrima", "choro"],
        "identified_theme": "Fidelidade Divina na Provação & Deus como Refúgio Inabalável",
        "chosen_verse": "Salmo 46:1-2 (Deus é o nosso refúgio e fortaleza, socorro bem presente nas tribulações)",
        "complementary_verses": [
            "Salmo 91:1-2 (Aquele que habita no esconderijo do Altíssimo e descansa à sombra do Onipotente)",
            "2 Coríntios 12:9 (A Minha graça te basta, porque o Meu poder se aperfeiçoa na fraqueza)",
            "Habacuque 3:17-18 (Ainda que a figueira não floresça, todavia eu me alegrarei no Senhor)"
        ],
        "attributes": ["Refúgio Inabalável", "Pastor Fiel no Vale", "Suficiência na Fraqueza", "Socorro Presente"],
        "christ_focus": "Cristo é a Rocha Eterna que acalma os ventos e sustenta o cansado no vale da sombra da morte.",
        "sacred_keywords": ["Esconderijo do Altíssimo", "Rocha inabalável", "Tua graça me basta", "Âncora da alma", "Socorro presente"],
        "tone": "Esperança firme, consolo profundo, confiança serena e entrega incondicional.",
        "guardrails": ["Evitar triunfalismo mágico; destacar que a presença fiel de Cristo nos sustenta na provação."]
    },
    {
        "tokens": ["espírito", "espirito", "pentecostes", "avivamento", "fogo", "unção", "uncao", "vento", "consolador", "sopra", "parakletos"],
        "identified_theme": "Pneumatologia: Derramamento, Fogo & Presença do Espírito Santo",
        "chosen_verse": "Atos 2:1-4 (De repente veio do céu um som, como de um vento impetuoso, e todos foram cheios do Espírito Santo)",
        "complementary_verses": [
            "João 14:16-17 (E Eu rogarei ao Pai, e Ele vos dará outro Consolador: o Espírito da verdade)",
            "Ezequiel 37:4-5 (Profetiza sobre estes ossos secos: Eis que farei entrar em vós o espírito, e vivereis)",
            "Zacarias 4:6 (Não por força nem por violência, mas pelo Meu Espírito, diz o Senhor dos Exércitos)"
        ],
        "attributes": ["Espírito Consolador (Parakletos)", "Sopro de Vida", "Fogo Santificador", "Rios de Água Viva"],
        "christ_focus": "O Espírito Santo glorifica a Cristo, habita no crente e capacita a Igreja com poder e santidade.",
        "sacred_keywords": ["Vento impetuoso", "Fogo do altar", "Espírito da Verdade", "Rios de água viva", "Sopro de vida"],
        "tone": "Clamor por avivamento, sensibilidade espiritual, reverência e fome da presença de Deus.",
        "guardrails": ["A obra do Espírito Santo sempre aponta para Cristo e produz fruto moral, santidade e ordem."]
    },
    {
        "tokens": ["amor a deus", "amar a deus", "primeiro amor", "devoção", "devocao", "intimidade", "sede de deus", "te amo", "apaixonado"],
        "identified_theme": "Devoção, Primeiro Amor & Intimidade Profunda com Deus",
        "chosen_verse": "Salmo 73:25-26 (Quem tenho eu no céu além de Ti? E na terra não há quem eu deseje além de Ti. Deus é a fortaleza do meu coração e a minha herança para sempre)",
        "complementary_verses": [
            "Marcos 12:30 (Amarás o Senhor teu Deus de todo o teu coração, de toda a tua alma e de todo o teu entendimento)",
            "Salmo 42:1-2 (Como a corça anseia pelas correntes das águas, assim a minha alma suspira por Ti, ó Deus)",
            "1 João 4:19 (Nós O amamos porque Ele nos amou primeiro)"
        ],
        "attributes": ["Tesouro Supremo", "Fonte de Água Viva", "Noivo Celestial", "Amor Eterno"],
        "christ_focus": "O nosso amor a Deus é a resposta apaixonada e grata à revelação do amor de Cristo na cruz.",
        "sacred_keywords": ["Primeiro amor", "Todo o meu coração", "Minha alma tem sede", "Tesouro supremo", "Altar de adoração"],
        "tone": "Devoção ardente, entrega total, sede espiritual e intimidade reverente.",
        "guardrails": ["Focar em adoração reverente, obediência e rendição da vontade, evitando sentimentalismo humano."]
    },
    {
        "tokens": ["louvor", "gratidão", "gratidao", "júbilo", "jubilo", "celebração", "celebracao", "alegria", "cântico", "cantico", "festa", "ações de graças"],
        "identified_theme": "Louvor Congregacional, Ações de Graças & Júbilo ao Senhor",
        "chosen_verse": "Salmo 100:1-4 (Celebrai com júbilo ao Senhor, todas as terras; entrai por Suas portas com ações de graças e nos Seus átrios com hinos)",
        "complementary_verses": [
            "Salmo 103:1-5 (Bendize, ó minha alma, ao Senhor, e tudo o que há em mim bendiga ao Seu santo nome)",
            "Salmo 150:1-6 (Tudo quanto tem fôlego louve ao Senhor! Aleluia!)",
            "Filipenses 4:4 (Alegrai-vos sempre no Senhor; outra vez digo: alegrai-vos!)"
        ],
        "attributes": ["Digno de Todo Louvor", "Fidelidade sem Fim", "Autor da Alegria", "Bondade Eterna"],
        "christ_focus": "Por meio de Jesus oferecemos a Deus sacrifício contínuo de louvor, fruto de lábios que confessam o Seu nome.",
        "sacred_keywords": ["Portas com ações de graças", "Bendize ó minha alma", "Tudo o que tem fôlego", "Aleluia ao Rei"],
        "tone": "Celebração vibrante, júbilo congregacional, gratidão transbordante e exaltação festiva.",
        "guardrails": ["A alegria cristã deve ser fundamentada em quem Deus é e na salvação, nunca em euforia vazia."]
    },
    {
        "tokens": ["batalha", "armadura", "guerra", "inimigo", "espada", "escudo", "fortaleza", "vencer", "vencedor"],
        "identified_theme": "A Armadura de Deus, Firmeza Espiritual & Vitória em Cristo",
        "chosen_verse": "Efésios 6:10-18 (Revesti-vos de toda a armadura de Deus, para poderdes ficar firmes contra as ciladas do diabo)",
        "complementary_verses": [
            "Romanos 8:37 (Em todas estas coisas, porém, somos mais que vencedores, por meio Daquele que nos amou)",
            "2 Coríntios 10:4-5 (As armas da nossa milícia não são carnais, mas poderosas em Deus para destruir fortalezas)",
            "Salmo 91:5-7 (Mil cairão ao teu lado, mas tu não serás atingido)"
        ],
        "attributes": ["Senhor dos Exércitos (Jeová Sabaoth)", "Capitão da Salvação", "Vencedor da Morte"],
        "christ_focus": "Na cruz, Cristo desarmou os principados e potestades, assegurando nossa vitória final.",
        "sacred_keywords": ["Armadura de Deus", "Escudo da fé", "Espada do Espírito", "Mais que vencedores"],
        "tone": "Fé resoluta, firmeza espiritual, autoridade em Cristo e vigilância santa.",
        "guardrails": ["A vitória do cristão está no sangue do Cordeiro e na Palavra de Deus, não em vanglória humana."]
    }
]


class TheologianAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Teólogo & Exegeta",
            role="Guardião Doutrinário e Analista Hermenêutico",
            system_prompt=THEOLOGIAN_SYSTEM_PROMPT,
        )

    def _semantic_research_fallback(self, theme: str, exclude_current: str = "") -> dict:
        """
        Pesquisa semântica autônoma para quando o LLM estiver indisponível:
        Analisa os termos do tema e pesquisa o índice canônico sem categorias pré-fixadas.
        """
        theme_clean = (theme or "").strip()
        t_low = theme_clean.lower()
        exclude_clean = (exclude_current or "").strip().lower()

        words_in_theme = set(re.findall(r"\w+", t_low))
        best_match = None
        best_score = 0
        for entry in BIBLICAL_CANONICAL_INDEX:
            score = 0
            for token in entry["tokens"]:
                tok_clean = token.lower()
                if tok_clean in t_low:
                    score += 5 if " " in tok_clean else 3
                elif tok_clean in words_in_theme:
                    score += 3
            if score > best_score:
                best_score = score
                best_match = entry

        if not best_match:
            general_pool = [
                "Salmo 145:1-3 (Exaltar-Te-ei, ó Deus meu e Rei; bendirei o Teu nome para todo o sempre)",
                "Salmo 103:1-5 (Bendize, ó minha alma, ao Senhor, e não te esqueças de nenhum de Seus benefícios)",
                "Isaías 40:28-31 (Não sabes, não ouviste? O Senhor é o Deus eterno; os que esperam no Senhor renovam as suas forças)",
                "João 1:1-4 (No princípio era o Verbo, e o Verbo estava com Deus, e o Verbo era Deus; Nele estava a vida)",
                "Colossenses 1:16-17 (Tudo foi criado por meio de Cristo e para Ele; Ele é antes de todas as coisas)",
                "Filipenses 2:9-11 (Pelo que Deus O exaltou soberanamente e Lhe deu o nome que está sobre todo nome)",
                "Apocalipse 5:12-13 (Digno é o Cordeiro que foi morto de receber poder, honra, glória e louvor)"
            ]
            available = [v for v in general_pool if exclude_clean not in v.lower()]
            chosen_v = random.choice(available if available else general_pool)
            identified = f"Exegese Teológica sobre '{theme_clean}'"
            verses_list = [chosen_v] + [v for v in general_pool if v != chosen_v]
            attributes = ["Soberano e Santo", "Fiel em Toda a Palavra", "Redentor Eterno", "Criador de Todas as Coisas"]
            christ_focus = f"Cristo Jesus é o centro e a plenitude de toda adoração bíblica sobre '{theme_clean}'."
            sacred_words = [theme_clean, "Graça e Verdade", "Luz Eterna", "Cordeiro Digno", "Nome sobre todo nome"]
            tone = "Reverência solene, profundidade bíblica e gratidão cristocêntrica."
            guardrails = ["Manter Deus e Cristo como o centro absoluto da mensagem da canção."]
            ref_part = chosen_v.split("(")[0].strip() if "(" in chosen_v else chosen_v
            txt_part = chosen_v.split("(", 1)[1].rsplit(")", 1)[0].strip() if "(" in chosen_v else chosen_v
            reflection = (
                f"Pesquisa Bíblica em {ref_part}: \"{txt_part}\". "
                f"Para o tema '{theme_clean}', esta passagem canônica nos conduz à soberania de Deus, "
                f"proclamando que toda a criação e redenção culminam na glória de Cristo Jesus."
            )
        else:
            identified = best_match["identified_theme"]
            pool = [best_match["chosen_verse"]] + [v for v in best_match["complementary_verses"] if v != best_match["chosen_verse"]]
            available = [v for v in pool if exclude_clean not in v.lower()]
            chosen_v = random.choice(available if available else pool)
            verses_list = [chosen_v] + [v for v in pool if v != chosen_v]
            attributes = best_match["attributes"]
            christ_focus = best_match["christ_focus"]
            sacred_words = best_match["sacred_keywords"]
            tone = best_match["tone"]
            guardrails = best_match["guardrails"]
            ref_part = chosen_v.split("(")[0].strip() if "(" in chosen_v else chosen_v
            txt_part = chosen_v.split("(", 1)[1].rsplit(")", 1)[0].strip() if "(" in chosen_v else chosen_v
            reflection = (
                f"Meditação em {ref_part}: \"{txt_part}\". "
                f"Para o tema '{theme_clean}' ({identified}), esta passagem canônica nos ensina sobre {', '.join(attributes[:2]).lower()} "
                f"e nos conduz à verdade de que {christ_focus[0].lower() + christ_focus[1:]}"
            )

        return {
            "identified_theme": identified,
            "chosen_verse": chosen_v,
            "biblical_reflection": reflection,
            "pool_size": len(verses_list),
            "scriptures": verses_list,
            "formatted": chosen_v,
            "attributes": attributes,
            "christ_focus": christ_focus,
            "sacred_words": sacred_words,
            "tone": tone,
            "guardrails": guardrails,
        }

    def analyze_and_draw_scripture(self, theme: str, exclude_current: str = "") -> dict:
        """
        Pesquisa e Exegese Bíblica Autônoma:
        Lê o tema, pesquisa o cânon bíblico via Inteligência Artificial (ou semântica avançada)
        e extrai o versículo canônico real, exegese e metadados teológicos.
        """
        theme_clean = (theme or "").strip()
        if not theme_clean:
            theme_clean = "Louvor e Adoração ao Senhor"

        prompt = f"""Você é um Teólogo e Exegeta Cristão erudito em Hinologia Sacra.
Pesquise nas Sagradas Escrituras e elabore a análise bíblica profunda para este tema de adoração:
TEMA INFORMADO: "{theme_clean}"

DIRETRIZES DA PESQUISA:
1. Compreenda exatamente o sentido espiritual de "{theme_clean}".
2. Pesquise e cite passagens bíblicas canônicas reais e fidedignas (Antigo ou Novo Testamento) que tratem especificamente deste tema.
3. No campo 'chosen_verse', forneça o versículo principal com citação e texto exato entre parênteses: "Livro Cap:Vers (Texto)".
4. Se o versículo '{exclude_current}' for informado, forneça uma passagem bíblica alternativa diferente.
5. Elabore uma reflexão bíblica e exegética fidedigna conectando o tema ao versículo e a Cristo.
6. Aponte os atributos divinos, vocabulário sagrado e o tom devocional mais adequado.
"""
        try:
            res: ScriptureResearchResult = self.call_llm(
                prompt,
                ScriptureResearchResult,
                custom_json_example=RESEARCH_JSON_EXAMPLE
            )
            verses = [res.chosen_verse] + [v for v in res.complementary_verses if v != res.chosen_verse]
            return {
                "identified_theme": res.identified_theme,
                "chosen_verse": res.chosen_verse,
                "biblical_reflection": res.biblical_reflection,
                "pool_size": len(verses),
                "scriptures": verses,
                "formatted": res.chosen_verse,
                "attributes": res.divine_attributes,
                "christ_focus": res.christocentric_focus,
                "sacred_words": res.sacred_keywords,
                "tone": res.emotional_and_spiritual_tone,
                "guardrails": res.doctrinal_guardrails,
            }
        except Exception:
            return self._semantic_research_fallback(theme_clean, exclude_current=exclude_current)

    def suggest_scriptures(self, theme: str, exclude_current: str = "") -> list[str]:
        """Retorna as passagens bíblicas pesquisadas pelo Agente Teólogo para o tema."""
        analysis = self.analyze_and_draw_scripture(theme, exclude_current=exclude_current)
        return analysis["scriptures"]

    def run(self, briefing: UserBriefing) -> TheologicalDossier:
        biblical_info = (briefing.biblical_reference or "").strip()
        if not biblical_info:
            analysis = self.analyze_and_draw_scripture(briefing.theme)
            biblical_info = analysis["chosen_verse"]
            briefing.biblical_reference = biblical_info

        prompt = f"""Como Teólogo e Exegeta Bíblico, realize uma exegese aprofundada para esta canção de adoração:
TEMA: {briefing.theme}
PASSAGEM BÍBLICA BASE: {biblical_info}
ESTILO MUSICAL / CLIMA: {briefing.musical_style_hint} | {briefing.tempo_hint}
PREFERÊNCIA VOCAL: {briefing.vocal_preference}
INSTRUÇÕES ESPECÍFICAS DO COMPOSITOR: {briefing.user_prompt or 'Nenhuma'}

REGRAS:
1. Respeite com fidelidade canônica o tema '{briefing.theme}' e a passagem '{biblical_info}'.
2. Se o tema for íntimo, terno ou filial (ex: como uma criança, quebrantamento, consolo), toda a teologia deve refletir acolhimento, descanso e pureza, NUNCA triunfalismo arrogante ou clichês vazios.
3. Toda a revelação culmina na cruz e na glória de Cristo.
"""
        return self.call_llm(prompt, TheologicalDossier, custom_json_example=THEOLOGICAL_DOSSIER_JSON_EXAMPLE)

    def _generate_contextual_demonstration(self, user_prompt: str, response_model: Type[BaseModel]) -> BaseModel:
        theme_match = re.search(r"Tema(?:\s*INFORMADO)?:\s*[\"']?([^\"'\n\r]+)[\"']?", user_prompt, re.IGNORECASE)
        ref_match = re.search(r"Passagens?(?:\s*Bíblicas?)?(?:\s*Base)?:\s*[\"']?([^\"'\n\r]+)[\"']?", user_prompt, re.IGNORECASE)
        extracted_theme = theme_match.group(1).strip() if theme_match else "Adoração ao Senhor"
        extracted_ref = ref_match.group(1).strip() if ref_match else ""

        research = self._semantic_research_fallback(extracted_theme, exclude_current=extracted_ref)

        if response_model == ScriptureSuggestion:
            return ScriptureSuggestion(
                identified_theme=research["identified_theme"],
                scriptures=research["scriptures"]
            )

        if response_model == ScriptureResearchResult:
            return ScriptureResearchResult(
                identified_theme=research["identified_theme"],
                chosen_verse=research["chosen_verse"],
                complementary_verses=research["scriptures"][1:],
                biblical_reflection=research["biblical_reflection"],
                divine_attributes=research["attributes"],
                christocentric_focus=research["christ_focus"],
                sacred_keywords=research["sacred_words"],
                emotional_and_spiritual_tone=research["tone"],
                doctrinal_guardrails=research["guardrails"]
            )

        chosen_ref = extracted_ref if extracted_ref else research["chosen_verse"]
        ref_short = chosen_ref.split("(")[0].strip() if "(" in chosen_ref else chosen_ref
        primary_refs = [chosen_ref] + [s for s in research["scriptures"] if s != chosen_ref][:2]

        return TheologicalDossier(
            theme_title=f"{research['identified_theme']} — {ref_short}",
            primary_scriptures=primary_refs,
            divine_attributes=research["attributes"],
            christocentric_focus=research["christ_focus"],
            sacred_keywords=research["sacred_words"],
            doctrinal_guardrails=research["guardrails"],
            emotional_and_spiritual_tone=research["tone"],
            exegetical_summary=research["biblical_reflection"]
        )
