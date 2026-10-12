"""
Agente 1: Teólogo & Exegeta Bíblico.
Responsável por extrair a fundamentação bíblica, ortodoxia cristocêntrica, atributos divinos
e salvaguardas doutrinárias para evitar antropocentrismo ou desvios heréticos.
"""

import random
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


class TheologianAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Teólogo & Exegeta",
            role="Guardião Doutrinário e Analista Hermenêutico",
            system_prompt=THEOLOGIAN_SYSTEM_PROMPT,
        )

    def suggest_scriptures(self, theme: str) -> list[str]:
        """
        Identifica a essência teológica do tema informado pelo usuário e seleciona/sorteia
        passagens bíblicas canônicas de alta precisão doutrinária.
        """
        theme_clean = (theme or "").strip()
        if not theme_clean:
            return ["Salmo 100:1-5 (Celebrai com júbilo ao Senhor)"]

        # 1. Tenta consulta ao motor de IA (Gemini Cloud ou Ollama)
        try:
            prompt = (
                f"Você é um Teólogo e Exegeta Bíblico especialista em adoração e hinologia sacra.\n"
                f"Analise o seguinte tema doutrinário informado pelo usuário: '{theme_clean}'.\n"
                f"Identifique o foco teológico e selecione exatamente 3 referências bíblicas canônicas e profundas "
                f"(equilibrando Antigo e Novo Testamento) que se relacionem diretamente com o tema.\n"
                f"Para cada referência, adicione uma explicação sucinta no formato 'Livro Capítulo:Versículos (Explicação)'.\n"
                f"Responda no formato JSON com 'identified_theme' e 'scriptures'."
            )
            result = self.call_llm(prompt, ScriptureSuggestion)
            if result and result.scriptures and len(result.scriptures) >= 1:
                return result.scriptures
        except Exception:
            pass

        # 2. Identificação Temática Canônica com Sorteio Dinâmico (Fallback Robusto)
        return self._identify_and_sample_scriptures(theme_clean)

    def _identify_and_sample_scriptures(self, theme: str) -> list[str]:
        """Identifica o núcleo temático e sorteia 2 a 3 versículos altamente pertinentes de um acervo robusto."""
        t_lower = theme.lower()

        # 1. Tema: Amor / Ágape / Amor de Deus / Bondade / Misericórdia
        if any(w in t_lower for w in ["amor", "ágape", "agape", "amou", "amado", "bondade", "misericórdia", "misericordia", "benignidade"]):
            pool = [
                "1 João 4:7-12 (O amor procede de Deus; nisto conhecemos o amor: Ele nos amou primeiro)",
                "Romanos 5:8 (Deus prova o Seu próprio amor para conosco pelo sacrifício de Cristo na cruz)",
                "João 3:16-17 (Porque Deus amou o mundo de tal maneira que deu o Seu Filho unigênito)",
                "Efésios 3:17-19 (Compreender a largura, comprimento, altura e profundidade do amor de Cristo)",
                "1 Coríntios 13:4-8 (O hino ao amor ágape: paciente, benigno e que jamais acaba)",
                "Jeremias 31:3 (Com amor eterno te amei; com laços de benignidade te atraí)",
                "Romanos 8:38-39 (Nem a morte, nem a vida, nada nos poderá separar do amor de Deus)",
                "Sofonias 3:17 (O Senhor se deleitará em ti com júbilo e te renovará no Seu amor)",
                "1 João 3:1 (Vede que grande amor nos tem concedido o Pai, a ponto de sermos chamados filhos de Deus)"
            ]
        # 2. Tema: Santidade / Glória / Trono / Majestade
        elif any(w in t_lower for w in ["santidade", "santo", "trono", "majestade", "glória", "gloria", "soberano", "altíssimo", "altissimo"]):
            pool = [
                "Isaías 6:1-8 (A visão do trono alto e sublime e os serafins clamando Santo, Santo, Santo)",
                "Apocalipse 4:8-11 (Os seres viventes prostrados clamando Santo é o Senhor Deus Todo-Poderoso)",
                "Salmo 99:5-9 (Exaltai ao Senhor nosso Deus e prostrai-vos ante o estrado dos Seus pés)",
                "1 Pedro 1:15-16 (Sede santos em todo o vosso procedimento, porque Eu sou santo)",
                "Êxodo 15:11 (Quem é semelhante a Ti, ó Senhor, glorioso em santidade e terrível em louvores?)",
                "Hebreus 12:28-29 (Servir a Deus com reverência e santo temor, pois Ele é fogo consumidor)",
                "Salmo 29:2 (Tributai ao Senhor a glória devida ao Seu nome; adorai na beleza da santidade)"
            ]
        # 3. Tema: Graça / Salvação / Cruz / Redenção / Sangue
        elif any(w in t_lower for w in ["graça", "graca", "cruz", "redenção", "redencao", "sangue", "salvação", "salvacao", "calvário", "calvario"]):
            pool = [
                "Efésios 2:8-10 (Pela graça sois salvos mediante a fé, isso não vem de vós, é dom de Deus)",
                "Romanos 5:1-8 (Justificados mediante a fé, temos paz com Deus por nosso Senhor Jesus)",
                "Tito 2:11-14 (A graça salvadora de Deus se manifestou a todos os homens ensinando a piedade)",
                "Isaías 53:4-6 (O servo sofredor traspassado pelas nossas transgressões e moído por nossos pecados)",
                "Hebreus 9:11-14 (O sangue precioso de Cristo que purifica a nossa consciência do pecado)",
                "2 Coríntios 5:17-21 (A reconciliação em Cristo e a justiça de Deus imputada aos pecadores)",
                "Gálatas 2:20 (Estou crucificado com Cristo; já não sou eu quem vive, mas Cristo vive em mim)"
            ]
        # 4. Tema: Provação / Perseverança / Refúgio / Consolo / Dor
        elif any(w in t_lower for w in ["provação", "provacao", "perseverança", "perseveranca", "dor", "luta", "força", "forca", "refúgio", "refugio", "consolo", "deserto"]):
            pool = [
                "Tiago 1:2-4 (A fé provada gerando paciência e maturidade perfeita em Cristo)",
                "2 Coríntios 12:9-10 (A Minha graça te basta, pois o Meu poder se aperfeiçoa na fraqueza)",
                "Salmo 46:1-3 (Deus é o nosso refúgio e fortaleza, socorro bem presente nas tribulações)",
                "Salmo 91:1-4 (Aquele que habita no esconderijo do Altíssimo descansará sob as Suas asas)",
                "Romanos 8:31-39 (Se Deus é por nós, quem será contra nós? Em tudo somos mais que vencedores)",
                "Habacuque 3:17-19 (Ainda que a figueira não floresça, todavia eu me alegrarei no Senhor meu Salvador)",
                "Salmo 23:1-6 (O Senhor é o meu pastor; ainda que eu ande pelo vale da sombra da morte, não temerei)"
            ]
        # 5. Tema: Gratidão / Louvor / Júbilo / Celebração / Vitória / Alegria
        elif any(w in t_lower for w in ["gratidão", "gratidao", "louvor", "júbilo", "jubilo", "celebração", "celebracao", "vitória", "vitoria", "alegria"]):
            pool = [
                "Salmo 100:1-5 (Celebrai com júbilo ao Senhor, entrai pelas Suas portas com ações de graças)",
                "Salmo 103:1-5 (Bendize, ó minha alma, ao Senhor, e não te esqueças de nenhum dos Seus benefícios)",
                "Filipenses 4:4-7 (Alegrai-vos sempre no Senhor; a paz de Deus guardará vossa mente)",
                "Colossenses 3:15-17 (Com salmos, hinos e cânticos espirituais, louvando com gratidão no coração)",
                "Salmo 150:1-6 (Tudo quanto tem fôlego louve ao Senhor! Louvai ao Senhor nas alturas)",
                "Salmo 34:1-3 (Louvarei ao Senhor em todo o tempo; o Seu louvor estará continuamente nos meus lábios)"
            ]
        # 6. Tema: Espírito Santo / Pentecostes / Avivamento / Fogo / Presença
        elif any(w in t_lower for w in ["espírito", "espirito", "pentecostes", "avivamento", "fogo", "presença", "presenca", "unção", "uncao"]):
            pool = [
                "Atos 2:1-4 (O derramamento do Espírito Santo no Pentecostes com poder e línguas de fogo)",
                "João 14:16-17 (O Consolador, o Espírito da Verdade que habita para sempre convosco)",
                "Romanos 8:26-27 (O Espírito intercede por nós sobremaneira com gemidos inexprimíveis)",
                "Gálatas 5:22-25 (O fruto do Espírito: amor, paz, paciência, bondade, mansidão)",
                "Ezequiel 37:1-10 (O sopro de vida do Espírito Santo ressuscitando o vale de ossos secos)",
                "Zacarias 4:6 (Não por força nem por violência, mas pelo Meu Espírito, diz o Senhor dos Exércitos)"
            ]
        # 7. Tema: Fé / Confiança / Esperança / Descanso / Paz
        elif any(w in t_lower for w in ["fé", "fe", "confiança", "confianca", "esperança", "esperanca", "descanso", "paz", "crença"]):
            pool = [
                "Hebreus 11:1-6 (A fé é a certeza das coisas que se esperam e a convicção do que não se vê)",
                "Provérbios 3:5-6 (Confia no Senhor de todo o teu coração e Ele endireitará as tuas veredas)",
                "Isaías 40:29-31 (Os que esperam no Senhor renovam as suas forças e voam como águias)",
                "Mateus 11:28-30 (Vinde a Mim todos os cansados e oprimidos, e Eu vos darei descanso)",
                "João 14:27 (Deixo-vos a paz, a Minha paz vos dou; não se turbe o vosso coração)",
                "Lamentações 3:22-24 (As misericórdias do Senhor se renovam a cada manhã; grande é a Tua fidelidade)"
            ]
        # 8. Tema: Cura / Milagres / Restauração / Libertação
        elif any(w in t_lower for w in ["cura", "milagre", "restauração", "restauracao", "libertação", "libertacao", "enfermidade", "saúde"]):
            pool = [
                "Isaías 53:5 (Ele foi ferido por nossas transgressões, e pelas Suas pisaduras fomos sarados)",
                "Salmo 103:2-3 (Ele é quem perdoa todas as tuas iniquidades e sara todas as tuas enfermidades)",
                "Jeremias 17:14 (Cura-me, Senhor, e serei curado; salva-me, e serei salvo, pois és meu louvor)",
                "Lucas 4:18-19 (O Espírito do Senhor me ungiu para proclamar libertação e cura aos quebrantados)",
                "Tiago 5:14-16 (A oração da fé salvará o enfermo, e o Senhor o levantará em poder)"
            ]
        # 9. Tema: Volta de Cristo / Eternidade / Noiva / Ressurreição
        elif any(w in t_lower for w in ["volta", "maranata", "eternidade", "ressurreição", "ressurreicao", "noiva", "reino", "segunda vinda"]):
            pool = [
                "Apocalipse 21:1-5 (Eis que faço novas todas as coisas; novo céu e nova terra sem pranto e sem dor)",
                "Apocalipse 22:17-20 (O Espírito e a Noiva dizem: Vem! Aquele que testifica diz: Certamente venho sem demora)",
                "1 Tessalonicenses 4:16-18 (O Senhor descerá dos céus com brado de arcanjo e ao som da trombeta de Deus)",
                "1 Coríntios 15:51-57 (Tragada foi a morte na vitória; graças a Deus que nos dá vitória por Cristo)",
                "Filipenses 2:9-11 (Ao nome de Jesus se dobre todo joelho nos céus, na terra e debaixo da terra)"
            ]
        # 10. Tema: Arrependimento / Perdão / Quebrantamento
        elif any(w in t_lower for w in ["arrependimento", "perdão", "perdao", "quebrantamento", "humildade", "confissão", "pecado"]):
            pool = [
                "Salmo 51:1-12 (Cria em mim, ó Deus, um coração puro; o coração quebrantado e contrito não desprezarás)",
                "Isaías 57:15 (Habito no alto e santo lugar, mas também com o contrito e humilde de espírito)",
                "1 João 1:9 (Se confessarmos os nossos pecados, Ele é fiel e justo para nos perdoar e purificar)",
                "2 Crônicas 7:14 (Se o Meu povo se humilhar, orar, buscar a Minha face e se converter dos maus caminhos)",
                "Lucas 18:13-14 (Ó Deus, sê propício a mim, pecador! Justificado pela graça e humildade)"
            ]
        # 11. Tema Geral / Criação / Soberania Canônica
        else:
            pool = [
                "Salmo 145:1-7 (Celebração da grandeza incomensurável e bondade soberana de Deus)",
                "João 1:14-17 (O Verbo se fez carne e habitou entre nós, cheio de graça e de verdade)",
                "Apocalipse 5:9-13 (Digno é o Cordeiro de receber honra, glória, louvor e domínio eterno)",
                "Salmo 19:1-4 (Os céus proclamam a glória de Deus e o firmamento anuncia as Suas obras)",
                "Colossenses 1:15-17 (Ele é a imagem do Deus invisível; Nele subsistem todas as coisas)",
                "Romanos 11:33-36 (Ó profundidade das riquezas de Deus! Porque Dele, por Ele e para Ele são todas as coisas)"
            ]

        qtd = min(3, len(pool))
        return random.sample(pool, k=qtd)

    def run(self, briefing: UserBriefing) -> TheologicalDossier:
        biblical_info = (briefing.biblical_reference or "").strip()
        if not biblical_info:
            sugestoes = self.suggest_scriptures(briefing.theme)
            biblical_info = f"NÃO ESPECIFICADA PELO USUÁRIO. O Teólogo pesquisou e selecionou as seguintes passagens fundamentais para o tema '{briefing.theme}': {', '.join(sugestoes)}"

        prompt = f"""Analise este pedido de canção de adoração e construa o Dossier Teológico completo:
Tema: {briefing.theme}
Passagens Bíblicas Base: {biblical_info}
Estilo e Clima: {briefing.musical_style_hint} | {briefing.tempo_hint}
Preferência Vocal: {briefing.vocal_preference}

IMPORTANTE: Caso o usuário não tenha informado passagens bíblicas, utilize sua erudição para fundamentar com rigor canônico e incluir as passagens mais ricas em 'primary_scriptures'!
"""
        return self.call_llm(prompt, TheologicalDossier)

    def _generate_contextual_demonstration(self, user_prompt: str, response_model: Type[BaseModel]) -> BaseModel:
        if response_model == ScriptureSuggestion:
            samples = self._identify_and_sample_scriptures(user_prompt)
            return ScriptureSuggestion(
                identified_theme="Tema Bíblico Identificado",
                scriptures=samples
            )

        # Se for o tema de Isaías 6 / Santidade de Deus
        if "Isaías" in user_prompt or "Santidade" in user_prompt or "Trono" in user_prompt:
            return TheologicalDossier(
                theme_title="A Majestade Transcendente e a Santidade do Deus do Trono",
                primary_scriptures=[
                    "Isaías 6:1-8 (A visão do trono alto e sublime e o envio)",
                    "Apocalipse 4:8-11 (Os quatro seres viventes e os 24 anciãos clamando Santo)",
                    "Salmo 99:5 (Exaltai ao Senhor nosso Deus e prostrai-vos ante Seu estrado)"
                ],
                divine_attributes=[
                    "Santidade Inegociável (Kadosh - três vezes santo)",
                    "Majestade e Soberania Eterna",
                    "Glória que enche toda a criação",
                    "Graça Purificadora (a brasa viva do altar)"
                ],
                christocentric_focus=(
                    "Jesus é o Rei glorioso visto por Isaías (João 12:41) e o Cordeiro imolado no centro do trono (Ap 5). "
                    "A purificação do homem impuro não vem de obras humanas, mas do sacrifício propiciatório de Cristo."
                ),
                sacred_keywords=[
                    "Alto e sublime trono", "Orlas do manto", "Serafins", "Santo, Santo, Santo",
                    "Brasa viva", "Lábios purificados", "Eis-me aqui", "Cordeiro no trono", "Anciãos e coroas"
                ],
                doctrinal_guardrails=[
                    "NUNCA colocar o homem como o protagonista da cena: o protagonista é o Rei no trono.",
                    "Evitar antropocentrismo triunfalista ou sentimentalismo raso.",
                    "O reconhecimento da própria impureza deve levar à graça purificadora e à prontidão para o envio ('Envia-me a mim')."
                ],
                emotional_and_spiritual_tone="Reverência profunda, assombro diante do Sagrado, quebrantamento sincero e consagração solene.",
                exegetical_summary=(
                    "A canção deve conduzir a igreja da contemplação da glória celestial (onde a voz do homem se cala) "
                    "ao quebrantamento do coração diante da santidade de Deus, culminando na purificação graciosa e "
                    "no clamor uníssono de adoração ao Cordeiro eterno."
                )
            )

        # Caso seja outro tema (ex: Tiago 1 / Perseverança / Graça)
        return TheologicalDossier(
            theme_title=f"A Soberania da Graça e a Fidelidade Divina na Provação",
            primary_scriptures=[
                "Tiago 1:2-4 (A fé provada gerando perseverança e maturidade)",
                "Romanos 5:3-5 (A tribulação produz paciência e esperança que não confunde)",
                "2 Coríntios 12:9 (A minha graça te basta, pois o poder se aperfeiçoa na fraqueza)"
            ],
            divine_attributes=[
                "Fidelidade Inabalável no Sofrimento",
                "Suficiência da Graça Divina",
                "Sabedoria e Soberania Pedagógica de Deus"
            ],
            christocentric_focus=(
                "Nossa esperança na provação repousa em Cristo, o autor e consumador da fé, que suportou a cruz pelo regozijo proposto."
            ),
            sacred_keywords=[
                "Fogo refinador", "Âncora da alma", "Graça que sustenta", "Paciência santa", "Maturidade em Cristo", "Fidelidade eterna"
            ],
            doctrinal_guardrails=[
                "Não prometer isenção mágica de dor nem teologia da prosperidade.",
                "Não tratar o sofrimento como ausência de Deus, mas como solo onde a fidelidade divina floresce.",
                "Manter o olhar fixo na eternidade e no aperfeiçoamento da fé."
            ],
            emotional_and_spiritual_tone="Confiança serena, esperança inabalável, consolo genuíno e louvor perseverante.",
            exegetical_summary=(
                "A canção guia a congregação do reconhecimento honesto da fraqueza humana à celebração da suficiência de Cristo, "
                "declarando que as provações não anulam o amor de Deus, mas forjam a perseverança dos santos."
            )
        )
