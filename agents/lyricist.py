"""
Agente 2: Poeta & Compositor Sacro.
Responsável por transformar o Dossier Teológico em poesia litúrgica com métrica regular,
prosódia fluida para canto em português e arquitetura estrófica clara.
"""

from typing import Optional, Type
from pydantic import BaseModel
from .base import BaseAgent
from schemas import TheologicalDossier, SongDraft, LyricSection, AuditReport


LYRICIST_SYSTEM_PROMPT = """Você é um Compositor e Poeta Sacro experiente, especializado em música congregacional e contemporânea de adoração (Worship/CCM).
Sua missão é dar forma poética e musical ao conteúdo teológico fornecido pelo Teólogo.

REGRAS DE OURO DA COMPOSIÇÃO:
1. FIDELIDADE AO DOSSIER: Utilize as passagens, atributos e palavras-chave sagradas indicadas. Respeite as salvaguardas doutrinárias (não introduza clichês antropocêntricos).
2. PROSÓDIA E CANTABILIDADE EM PORTUGUÊS:
   - Os versos devem ter ritmo e cadência naturais. Evite estrofes com excesso de palavras que atropelam a respiração do cantor.
   - Atenção redobrada aos acentos tônicos: as palavras devem fluir no compasso musical sem acentuações artificiais.
3. ESTRUTURA LITÚRGICA NARRATIVA:
   - [Verse 1]: Estabelece o cenário bíblico ou o sentimento inicial com tom intimista.
   - [Verse 2]: Aprofunda a narrativa e a contemplação.
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
        scripture_ref = "Escrituras Sagradas"
        if self._last_dossier and self._last_dossier.primary_scriptures:
            scripture_ref = self._last_dossier.primary_scriptures[0].split(" (")[0]

        # 1. Tema: Amor a Deus / Primeiro Amor / Amor de Deus (Ágape)
        if any(w in p_lower for w in ["amor", "ágape", "agape", "amou", "primeiro amor", "devoção"]):
            return SongDraft(
                title="Te Amo, Senhor, Meu Primeiro Amor",
                meter_notes=f"Métrica poética em redondilhas e decassílabos inspirada em {scripture_ref}, com cadência fluida para canto congregacional.",
                rhyme_scheme="Rimas ricas e sonoras (coração/adoração, cruz/Jesus, viver/ser).",
                sections=[
                    LyricSection(
                        tag="Verse 1",
                        liturgical_purpose=f"Declaração de devoção e resposta ao amor divino ({scripture_ref})",
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
                        liturgical_purpose="Elevação ao mistério da Cruz e do Amor Ágape",
                        lines=[
                            "Nós Te amamos porque nos amaste primeiro",
                            "Provaste Teu amor no sangue do Cordeiro",
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
                        tag="Verse 3",
                        liturgical_purpose="Contemplação da largura e profundidade do amor de Cristo",
                        lines=[
                            "Quão largo e profundo é o amor de Jesus",
                            "Que excede o saber e brilha na cruz",
                            "O medo se cala onde reina o Teu amor",
                            "Me fazes Teu filho, me chamas pelo nome, Senhor"
                        ]
                    ),
                    LyricSection(
                        tag="Bridge",
                        liturgical_purpose="Clímax de retorno ao Primeiro Amor e entrega da igreja",
                        lines=[
                            "Acende de novo a chama em meu ser!",
                            "No primeiro amor eu quero viver!",
                            "Tua graça é melhor do que a própria vida,",
                            "Minha alma em Teus braços está escondida!"
                        ]
                    ),
                    LyricSection(
                        tag="Outro",
                        liturgical_purpose="Adoração íntima e repouso no amor eterno",
                        lines=[
                            "Eu Te amo, Senhor... força minha.",
                            "Porque Tu me amaste primeiro.",
                            "Todo o meu coração é Teu, Jesus."
                        ]
                    )
                ]
            )

        # 2. Tema: Santidade / Trono / Isaías 6 / Glória
        if any(w in p_lower for w in ["trono", "isaías", "santidade", "santo", "serafins"]):
            return SongDraft(
                title="A Glória do Teu Trono",
                meter_notes=f"Métrica equilibrada inspirada em {scripture_ref} adaptada para balada congregacional solene.",
                rhyme_scheme="Rimas alternadas e emparelhadas ricas valorizando a reverência ao Trono.",
                sections=[
                    LyricSection(
                        tag="Verse 1",
                        liturgical_purpose="Contemplação solene da visão celestial",
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
                        tag="Verse 3",
                        liturgical_purpose="Quebrantamento, confissão e graça purificadora",
                        lines=[
                            "Ai de mim, que sou um homem impuro",
                            "De lábios maculados em meio à escuridão",
                            "Mas do altar veio a brasa acesa em amor",
                            "Tocou meu ser e apagou a transgressão"
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
                            "Santo... Tu és Santo...",
                            "Toda a terra se prostra aos Teus pés.",
                            "Eis-me aqui, Senhor. Envia-me a mim."
                        ]
                    )
                ]
            )

        # 3. Tema: Espírito Santo / Avivamento / Fogo / Pentecostes
        if any(w in p_lower for w in ["espírito", "espirito", "pentecostes", "avivamento", "consolador", "vento impetuoso"]):
            return SongDraft(
                title="Sopro de Vida e Fogo do Altar",
                meter_notes=f"Cadência ascendente baseada em {scripture_ref}, ideal para clamor congregacional.",
                rhyme_scheme="Rimas sonoras ricas focadas na ação do Espírito Santo.",
                sections=[
                    LyricSection(
                        tag="Verse 1",
                        liturgical_purpose="Clamor pelo derramamento do Espírito",
                        lines=[
                            "Reunidos em um mesmo coração",
                            "Esperamos a promessa da unção",
                            "Vem como o som de um vento impetuoso",
                            "Inunda este lugar, Deus glorioso"
                        ]
                    ),
                    LyricSection(
                        tag="Pre-Chorus",
                        liturgical_purpose="Profecia sobre o vale de ossos secos",
                        lines=[
                            "Não por força nem violência humana,",
                            "Mas pelo Teu Espírito que nos chama:",
                            "Sopra nos quatro cantos e traz a vida!"
                        ]
                    ),
                    LyricSection(
                        tag="Chorus",
                        liturgical_purpose="Exaltação ao Espírito Consolador",
                        lines=[
                            "Vem, Espírito Santo, Consolador fiel!",
                            "Acende em nosso peito o fogo lá do céu!",
                            "Faz fluir em nós os rios de água viva,",
                            "Glorifica a Jesus na igreja que Te bendiz!"
                        ]
                    ),
                    LyricSection(
                        tag="Bridge",
                        liturgical_purpose="Clímax de avivamento e santificação",
                        lines=[
                            "Onde o Espírito está, ali há liberdade!",
                            "Guia os nossos passos em toda a verdade!",
                            "Sopra em nós, transforma o nosso viver!"
                        ]
                    ),
                    LyricSection(
                        tag="Outro",
                        liturgical_purpose="Comunhão reverente",
                        lines=[
                            "Santo Espírito, habita em nós...",
                            "Queremos ouvir a Tua doce voz."
                        ]
                    )
                ]
            )

        # 4. Tema Dinâmico Adaptável a Qualquer Tema do Usuário
        title_clean = "A Graça Que Sustenta"
        if self._last_dossier and self._last_dossier.theme_title:
            raw_t = self._last_dossier.theme_title
            if "(" in raw_t and ")" in raw_t:
                user_t = raw_t.split("(")[-1].replace(")", "").strip().title()
                title_clean = f"Cântico de {user_t}"
            else:
                title_clean = raw_t[:45]

        kw_list = (self._last_dossier.sacred_keywords if self._last_dossier else ["Graça eterna", "Cruz de Cristo", "Rocha fiel"])
        kw1 = kw_list[0] if len(kw_list) > 0 else "Tua presença"
        kw2 = kw_list[1] if len(kw_list) > 1 else "Tua fidelidade"
        kw3 = kw_list[2] if len(kw_list) > 2 else "Teu santo altar"

        return SongDraft(
            title=title_clean,
            meter_notes=f"Cadência poética fundamentada em {scripture_ref}, estruturada para adoração congregacional.",
            rhyme_scheme="Rimas ricas e naturais para canto fluido no Suno AI.",
            sections=[
                LyricSection(
                    tag="Verse 1",
                    liturgical_purpose=f"Fundamentação bíblica em {scripture_ref}",
                    lines=[
                        f"Diante da Palavra escrita em {scripture_ref}",
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
