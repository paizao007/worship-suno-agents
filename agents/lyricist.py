"""
Agente 2: Poeta & Compositor Sacro.
Responsável por transformar o Dossier Teológico (Tema + Versículo + Reflexão Bíblica)
em poesia litúrgica com métrica regular, prosódia fluida para canto em português e arquitetura estrófica clara.
"""

import random
from typing import Optional, Type
from pydantic import BaseModel
from .base import BaseAgent
from schemas import TheologicalDossier, SongDraft, LyricSection, AuditReport


LYRICIST_SYSTEM_PROMPT = """Você é um Compositor e Poeta Sacro experiente, especializado em música congregacional e contemporânea de adoração (Worship/CCM).
Sua missão é dar forma poética e musical ao conteúdo teológico e à reflexão bíblica fornecidos pelo Teólogo.

REGRAS DE OURO DA COMPOSIÇÃO:
1. FIDELIDADE AO DOSSIER: Utilize as passagens, atributos e palavras-chave sagradas indicadas. Respeite as salvaguardas doutrinárias (não introduza clichês antropocêntricos).
2. PROSÓDIA E CANTABILIDADE EM PORTUGUÊS:
   - Os versos devem ter ritmo e cadência naturais. Evite estrofes com excesso de palavras que atropelam a respiração do cantor.
   - Atenção redobrada aos acentos tônicos: as palavras devem fluir no compasso musical sem acentuações artificiais.
3. ESTRUTURA LITÚRGICA NARRATIVA:
   - [Verse 1]: Estabelece o cenário bíblico ou o sentimento inicial com tom intimista.
   - [Verse 2]: Aprofunda a narrativa e a contemplação da passagem sorteada.
   - [Pre-Chorus]: Constrói a subida de energia (tensão/antecipação).
   - [Chorus]: O ponto focal, solene e fácil de cantar em coro. Doxologia memorável.
   - [Bridge]: O clímax espiritual e emotivo — a declaração de entrega ou revelação gloriosa.
   - [Outro]: Resolução de louvor pacífico e consagração final.
4. QUALIDADE DAS RIMAS: Prefira rimas consoantes ou toantes ricas; evite rimas banais no infinitivo ou particípio em série.
"""


class LyricistAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Poeta & Compositor Sacro",
            role="Mestre de Prosódia, Métrica e Poética Hinológica",
            system_prompt=LYRICIST_SYSTEM_PROMPT,
        )
        self._last_dossier: Optional[TheologicalDossier] = None
        self._last_title: str = ""

    def run(self, dossier: TheologicalDossier, audit_feedback: Optional[AuditReport] = None) -> SongDraft:
        self._last_dossier = dossier
        feedback_instructions = ""
        if audit_feedback and audit_feedback.actionable_revisions:
            revisoes = "\n- ".join(audit_feedback.actionable_revisions)
            feedback_instructions = f"""
ATENÇÃO: A versão anterior foi avaliada pelo Auditor Doutrinário com nota {audit_feedback.score}/10 e requer correções:
Críticas do Auditor:
{revisoes}
Reescreva a canção refinando exatamente estes pontos apontados pelo Auditor!
"""

        prompt = f"""Escreva a letra completa da canção de adoração com base neste Dossier Teológico:
Título Conceitual: {dossier.theme_title}
Escrituras Base: {', '.join(dossier.primary_scriptures)}
Atributos Divinos: {', '.join(dossier.divine_attributes)}
Foco Cristocêntrico: {dossier.christocentric_focus}
Palavras Sagradas Obrigatórias: {', '.join(dossier.sacred_keywords)}
Salvaguardas Doutrinárias: {', '.join(dossier.doctrinal_guardrails)}
Tom Espiritual: {dossier.emotional_and_spiritual_tone}
Síntese Exegética: {dossier.exegetical_summary}
{feedback_instructions}
"""
        return self.call_llm(prompt, SongDraft)

    def _generate_contextual_demonstration(self, user_prompt: str, response_model: Type[BaseModel]) -> SongDraft:
        p_lower = user_prompt.lower()
        scripture_full = "Escrituras Sagradas"
        scripture_ref = "Escrituras Sagradas"
        verse_essence = "Tua Palavra eterna permanece para sempre"

        if self._last_dossier and self._last_dossier.primary_scriptures:
            scripture_full = self._last_dossier.primary_scriptures[0]
            scripture_ref = scripture_full.split(" (")[0].strip()
            if "(" in scripture_full and ")" in scripture_full:
                verse_essence = scripture_full.split("(", 1)[1].rsplit(")", 1)[0].strip()

        # 1. Família: Amor (Amor a Deus / Primeiro Amor / Amor Ágape de Deus)
        if any(w in p_lower for w in ["amor", "ágape", "agape", "amou", "primeiro amor", "devoção"]):
            love_songs = [
                SongDraft(
                    title=f"Te Amo, Senhor ({scripture_ref})",
                    meter_notes=f"Métrica poética inspirada na reflexão de {scripture_ref} ('{verse_essence}'), com cadência fluida para canto congregacional.",
                    rhyme_scheme="Rimas ricas e sonoras (coração/adoração, cruz/Jesus, viver/ser).",
                    sections=[
                        LyricSection(
                            tag="Verse 1",
                            liturgical_purpose=f"Meditação poética em {scripture_ref}: {verse_essence}",
                            lines=[
                                "Antes que o mundo pudesse existir",
                                "Teu santo olhar já me via ali",
                                "Não foi por mérito ou força em minhas mãos",
                                "Tu me atraíste com laços de perdão"
                            ]
                        ),
                        LyricSection(
                            tag="Verse 2",
                            liturgical_purpose="Sede da alma e entrega de todo o coração",
                            lines=[
                                "Como a corça suspira pelas águas do rio",
                                "Minha alma Te busca no deserto vazio",
                                "Quem mais eu tenho no céu além de Ti?",
                                "Na terra não há outro bem para mim"
                            ]
                        ),
                        LyricSection(
                            tag="Pre-Chorus",
                            liturgical_purpose=f"Eco bíblico direto de {scripture_ref}",
                            lines=[
                                "Nós Te amamos porque nos amaste primeiro,",
                                "Provaste Teu amor no sangue do Cordeiro,",
                                "Hoje ergo a minha voz no Teu santo altar:"
                            ]
                        ),
                        LyricSection(
                            tag="Chorus",
                            liturgical_purpose="Doxologia central de amor e consagração total a Deus",
                            lines=[
                                "Eu Te amo, Senhor, de todo o meu coração!",
                                "De toda a minha alma, com toda a razão!",
                                "Nem a morte nem a vida vão me separar",
                                "Do amor de Cristo que veio me resgatar!",
                                "És minha força, minha rocha e meu Rei,",
                                "Para sempre, ó Deus, Te amarei!"
                            ]
                        ),
                        LyricSection(
                            tag="Bridge",
                            liturgical_purpose="Clímax de retorno ao Primeiro Amor e entrega da igreja",
                            lines=[
                                "Acende de novo a chama em meu ser!",
                                "No primeiro amor eu quero viver!",
                                "Tua benignidade é melhor do que a vida,",
                                "Minha alma em Teus braços está escondida!"
                            ]
                        ),
                        LyricSection(
                            tag="Outro",
                            liturgical_purpose="Adoração íntima e repouso no amor eterno",
                            lines=[
                                f"Fiel é a Tua palavra em {scripture_ref}...",
                                "Porque Tu me amaste primeiro.",
                                "Todo o meu coração é Teu, Jesus."
                            ]
                        )
                    ]
                ),
                SongDraft(
                    title=f"Amor Que Excede Todo Entendimento ({scripture_ref})",
                    meter_notes=f"Balada adoradora fundamentada em {scripture_ref} ('{verse_essence}'), com subida intensa no refrão.",
                    rhyme_scheme="Esquema AABB / ABAB com foco cristocêntrico.",
                    sections=[
                        LyricSection(
                            tag="Verse 1",
                            liturgical_purpose=f"Contemplação do amor revelado em {scripture_ref}",
                            lines=[
                                "Nisto se manifestou o amor do nosso Deus:",
                                "Enviou Seu Filho amado lá dos altos céus",
                                "Quando ainda éramos fracos e sem direção,",
                                "Na cruz do Calvário escreveu nossa redenção"
                            ]
                        ),
                        LyricSection(
                            tag="Verse 2",
                            liturgical_purpose="Profundidade e largura do amor de Cristo",
                            lines=[
                                "Qual é a largura e o comprimento dessa luz?",
                                "Quão fundo é o oceano do amor do meu Jesus?",
                                "Não há condenação para quem em Cristo está,",
                                "Nenhuma tempestade pode nos arrebatar"
                            ]
                        ),
                        LyricSection(
                            tag="Pre-Chorus",
                            liturgical_purpose="Preparação de louvor e rendição",
                            lines=[
                                "O perfeito amor lança fora todo o temor,",
                                "Rendido aos Teus pés eu canto, ó Senhor:"
                            ]
                        ),
                        LyricSection(
                            tag="Chorus",
                            liturgical_purpose="Refrão congregacional sobre o Amor Ágape",
                            lines=[
                                "Ó Amor eterno que me alcançou na cruz!",
                                "Toda a minha vida pertence a Ti, Jesus!",
                                "Nem altura, nem abismo, nem tribulação",
                                "Podem apagar a chama desta comunhão!",
                                "Tu és o meu Amado, meu eterno Salvador,",
                                "Pra sempre cantarei as maravilhas do Teu amor!"
                            ]
                        ),
                        LyricSection(
                            tag="Bridge",
                            liturgical_purpose="Explosão de devoção e resposta da noiva de Cristo",
                            lines=[
                                "De madrugada Te buscarei, ó Deus meu!",
                                "Meu coração inteiro é somente Teu!",
                                "Mais forte que a morte é a chama do Teu altar,",
                                "Para todo o sempre eu vou Te adorar!"
                            ]
                        ),
                        LyricSection(
                            tag="Outro",
                            liturgical_purpose="Sussurro final de adoração",
                            lines=[
                                f"Meditação viva em {scripture_ref}...",
                                "Nada nos separará do amor de Cristo.",
                                "Amém."
                            ]
                        )
                    ]
                ),
                SongDraft(
                    title=f"Chama do Primeiro Amor ({scripture_ref})",
                    meter_notes=f"Composição devocional inspirada em {scripture_ref} ('{verse_essence}').",
                    rhyme_scheme="Rimas consoantes fluidas para adoração íntima.",
                    sections=[
                        LyricSection(
                            tag="Verse 1",
                            liturgical_purpose=f"Oração de busca íntima baseada em {scripture_ref}",
                            lines=[
                                "Ó Deus, Tu és o meu Deus desde o amanhecer,",
                                "A minha alma tem sede de Te conhecer",
                                "Melhor é um só dia nos átrios da Tua luz",
                                "Do que mil anos longe da presença de Jesus"
                            ]
                        ),
                        LyricSection(
                            tag="Verse 2",
                            liturgical_purpose="Guarda dos mandamentos e comunhão com o Pai",
                            lines=[
                                "Não quero apenas palavras vazias no altar,",
                                "Com minha vida inteira eu quero Te amar",
                                "Guardar Tua Palavra escrita em meu coração,",
                                "Viver em Tua graça e santa comunhão"
                            ]
                        ),
                        LyricSection(
                            tag="Pre-Chorus",
                            liturgical_purpose="Transição de entrega",
                            lines=[
                                "Toma o meu fôlego, toma o meu louvor,",
                                "Restaura em meu peito o primeiro amor:"
                            ]
                        ),
                        LyricSection(
                            tag="Chorus",
                            liturgical_purpose="Refrão de entrega total",
                            lines=[
                                "Ama o Senhor teu Deus de todo o coração!",
                                "Entrega a tua alma em plena adoração!",
                                "Não há outro tesouro no céu ou sobre o mar,",
                                "Somente a Jesus Cristo queremos exaltar!"
                            ]
                        ),
                        LyricSection(
                            tag="Bridge",
                            liturgical_purpose="Clímax profético",
                            lines=[
                                "As muitas águas não podem apagar este amor!",
                                "Tu és a nossa herança, nosso Redentor!",
                                "Que suba como incenso a nossa canção!"
                            ]
                        ),
                        LyricSection(
                            tag="Outro",
                            liturgical_purpose="Paz e comunhão",
                            lines=[
                                f"Firmados na verdade de {scripture_ref}...",
                                "Tu és o nosso primeiro e eterno Amor."
                            ]
                        )
                    ]
                )
            ]
            avail = [s for s in love_songs if s.title != self._last_title] or love_songs
            chosen = random.choice(avail)
            self._last_title = chosen.title
            return chosen

        # 2. Família: Santidade / Trono / Majestade
        if any(w in p_lower for w in ["trono", "isaías", "santidade", "santo", "serafins", "majestade", "êxodo 15", "exodo 15"]):
            holiness_songs = [
                SongDraft(
                    title=f"A Glória do Teu Trono ({scripture_ref})",
                    meter_notes=f"Métrica solene inspirada em {scripture_ref} ('{verse_essence}').",
                    rhyme_scheme="Rimas ricas valorizando a reverência ao Trono.",
                    sections=[
                        LyricSection(
                            tag="Verse 1",
                            liturgical_purpose=f"Contemplação solene da visão celestial ({scripture_ref})",
                            lines=[
                                "No ano em que o rei terreno faleceu",
                                "Meus olhos viram o verdadeiro Rei",
                                "Sentado sobre um alto e sublime trono",
                                "E a orla de Suas vestes enchia o templo santo"
                            ]
                        ),
                        LyricSection(
                            tag="Verse 2",
                            liturgical_purpose="A reverência dos serafins celestiais",
                            lines=[
                                "Serafins cobriam o rosto em temor",
                                "Com seis asas a voar ao Seu redor",
                                "E clamavam em um uníssono trovão",
                                "Fazendo estremecer os alicerces do chão"
                            ]
                        ),
                        LyricSection(
                            tag="Pre-Chorus",
                            liturgical_purpose="Elevação e preparação do coração para o louvor",
                            lines=[
                                "A casa se encheu de glória e fumaça",
                                "A criação inteira curva a fronte em graça",
                                "E a nossa voz se une ao coro celestial:"
                            ]
                        ),
                        LyricSection(
                            tag="Chorus",
                            liturgical_purpose="Doxologia máxima da congregação",
                            lines=[
                                "Santo, Santo, Santo é o Senhor dos Exércitos!",
                                "Todo-Poderoso, Deus que era e que é!",
                                "Toda a terra está cheia da Tua glória!",
                                "Santo, Santo, reina para sempre em Teu trono!"
                            ]
                        ),
                        LyricSection(
                            tag="Bridge",
                            liturgical_purpose="Clímax cristocêntrico e consagração ao envio",
                            lines=[
                                "E ouvi a voz do Deus que me chamou:",
                                "'A quem enviarei? Quem há de ir por nós?'",
                                "Purificado pelo sangue do Cordeiro,",
                                "Aqui estou, Senhor, envia-me a mim!"
                            ]
                        ),
                        LyricSection(
                            tag="Outro",
                            liturgical_purpose="Resolução serena e consagração pessoal",
                            lines=[
                                f"Santo é o Senhor revelado em {scripture_ref}...",
                                "Toda a terra se prostra aos Teus pés.",
                                "Eis-me aqui, Senhor."
                            ]
                        )
                    ]
                ),
                SongDraft(
                    title=f"Glorificado em Santidade ({scripture_ref})",
                    meter_notes=f"Hino majestoso fundamentado em {scripture_ref} ('{verse_essence}').",
                    rhyme_scheme="Rimas clássicas de exaltação litúrgica.",
                    sections=[
                        LyricSection(
                            tag="Verse 1",
                            liturgical_purpose=f"Exaltação baseada em {scripture_ref}",
                            lines=[
                                "Quem é como Tu, ó Senhor, entre os poderes?",
                                "Glorificado em santidade, temível em louvores!",
                                "Diante do mar de vidro que brilha como cristal,",
                                "Os anciãos depositam sua coroa real"
                            ]
                        ),
                        LyricSection(
                            tag="Verse 2",
                            liturgical_purpose="Chamado à santificação do povo de Deus",
                            lines=[
                                "Segundo é Santo Aquele que um dia nos chamou,",
                                "Pelo sangue precioso nossas vestes alvejou",
                                "Subimos ao Teu monte com mãos limpas no altar,",
                                "A beleza da Tua santidade vamos contemplar"
                            ]
                        ),
                        LyricSection(
                            tag="Pre-Chorus",
                            liturgical_purpose="Subida orquestral",
                            lines=[
                                "Os céus anunciam a Tua justiça,",
                                "E a igreja redimida proclama em uma só voz:"
                            ]
                        ),
                        LyricSection(
                            tag="Chorus",
                            liturgical_purpose="Coro do Trono",
                            lines=[
                                "Tu és Santo, Incomparável Rei da Glória!",
                                "Teu braço forte escreve a eterna vitória!",
                                "Não há rocha como o nosso Deus fiel,",
                                "Adorado pela terra e pelos anjos lá no céu!"
                            ]
                        ),
                        LyricSection(
                            tag="Bridge",
                            liturgical_purpose="Clímax de reverência",
                            lines=[
                                "Digno és, Cordeiro Santo, de receber o poder!",
                                "Riqueza, sabedoria, honra e glória a Teu ser!",
                                "Para todo o sempre reina o Senhor!"
                            ]
                        ),
                        LyricSection(
                            tag="Outro",
                            liturgical_purpose="Encerramento solene",
                            lines=[
                                f"Palavra eterna em {scripture_ref}...",
                                "Santo, Santo é o Senhor."
                            ]
                        )
                    ]
                )
            ]
            avail = [s for s in holiness_songs if s.title != self._last_title] or holiness_songs
            chosen = random.choice(avail)
            self._last_title = chosen.title
            return chosen

        # 3. Tema Dinâmico Adaptável a Qualquer Tema e Versículo Sorteado
        raw_t = self._last_dossier.theme_title if (self._last_dossier and self._last_dossier.theme_title) else "Adoração Cristocêntrica"
        title_clean = f"Cântico de {raw_t.split('—')[0].strip()[:35]} ({scripture_ref})"

        kw_list = (self._last_dossier.sacred_keywords if self._last_dossier else ["Graça eterna", "Cruz de Cristo", "Rocha fiel", "Palavra viva"])
        kw1 = kw_list[0] if len(kw_list) > 0 else "Tua presença"
        kw2 = kw_list[1] if len(kw_list) > 1 else "Tua fidelidade"
        kw3 = kw_list[2] if len(kw_list) > 2 else "Teu santo altar"

        return SongDraft(
            title=title_clean,
            meter_notes=f"Cadência poética fundamentada em {scripture_ref} ('{verse_essence}'), estruturada para adoração congregacional.",
            rhyme_scheme="Rimas ricas e naturais para canto fluido no Suno AI.",
            sections=[
                LyricSection(
                    tag="Verse 1",
                    liturgical_purpose=f"Fundamentação bíblica em {scripture_ref}: {verse_essence}",
                    lines=[
                        f"Na luz da Palavra escrita em {scripture_ref}",
                        f"Minha alma encontra vida em {kw1}",
                        "Ergo os olhos para o monte onde brilha a luz",
                        "Meu socorro e esperança vêm do Rei Jesus"
                    ]
                ),
                LyricSection(
                    tag="Verse 2",
                    liturgical_purpose="Contemplação dos atributos de Deus",
                    lines=[
                        f"Em meio às estações contemplo {kw2}",
                        "Tua aliança eterna jamais voltará atrás",
                        f"Purifica os nossos lábios junto a {kw3}",
                        "Pois somente em Tua graça encontramos paz"
                    ]
                ),
                LyricSection(
                    tag="Pre-Chorus",
                    liturgical_purpose="Transição de fé e exaltação",
                    lines=[
                        "Não há rocha mais segura que o Teu amor,",
                        "Toda a igreja se levanta para dar louvor:"
                    ]
                ),
                LyricSection(
                    tag="Chorus",
                    liturgical_purpose="Refrão congregacional cristocêntrico",
                    lines=[
                        "Tua graça nos sustenta, ó Cordeiro de Deus!",
                        "Reina soberano sobre a terra e os céus!",
                        f"Celebramos para sempre {kw1},",
                        "A Ti, Senhor Jesus, toda a glória e o poder!"
                    ]
                ),
                LyricSection(
                    tag="Bridge",
                    liturgical_purpose="Clímax de entrega e confiança",
                    lines=[
                        "Digno é o Cordeiro que venceu na cruz!",
                        "Nossa vida está firmada em Ti, Jesus!",
                        "De geração em geração cantaremos Teu louvor!"
                    ]
                ),
                LyricSection(
                    tag="Outro",
                    liturgical_purpose="Encerramento solene",
                    lines=[
                        f"Fiel é a Tua palavra em {scripture_ref}...",
                        "A Ti toda a honra para sempre. Amém."
                    ]
                )
            ]
        )
