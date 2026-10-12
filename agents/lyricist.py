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

    def run(self, dossier: TheologicalDossier, audit_feedback: Optional[AuditReport] = None) -> SongDraft:
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
        # Se for tema de Santidade / Trono / Isaías 6
        if "Trono" in user_prompt or "Isaías" in user_prompt or "Santidade" in user_prompt:
            return SongDraft(
                title="A Glória do Teu Trono",
                meter_notes="Métrica equilibrada em redondilhas maiores e decassílabos adaptados para balada congregacional lenta.",
                rhyme_scheme="Rimas alternadas e emparelhadas ricas (Senhor/templo/chão/purificou), valorizando a solenidade.",
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
                        tag="Bridge 2",
                        liturgical_purpose="Aclamação final ao Cordeiro de Deus",
                        lines=[
                            "Digno é o Cordeiro que foi morto e ressurgiu!",
                            "Ao que está no trono e ao Cordeiro seja o louvor!",
                            "Honra, glória, força e domínio eterno!"
                        ]
                    ),
                    LyricSection(
                        tag="Outro",
                        liturgical_purpose="Resolução serena e consagração pessoal",
                        lines=[
                            "Santo... Tu és Santo...",
                            "Toda a terra se prostra aos Teus pés.",
                            "Eis-me aqui, Senhor.",
                            "Envia-me a mim."
                        ]
                    )
                ]
            )

        # Tema genérico de Graça / Perseverança
        return SongDraft(
            title="A Graça Que Sustenta",
            meter_notes="Cadência regular pensada para condução em piano e violão acústico com crescendo de bateria.",
            rhyme_scheme="Rimas sonoras ricas, mantendo o tom devocional e solene.",
            sections=[
                LyricSection(
                    tag="Verse 1",
                    liturgical_purpose="Confissão da fraqueza humana e busca do refúgio divino",
                    lines=[
                        "Quando a tempestade cerca o caminhar",
                        "E as forças do meu peito parecem findar",
                        "Ergo os olhos para o monte onde reina a luz",
                        "Meu socorro vem do trono onde está Jesus"
                    ]
                ),
                LyricSection(
                    tag="Pre-Chorus",
                    liturgical_purpose="Transição da angústia para a confiança santa",
                    lines=[
                        "A dor não é o fim, mas prova que refina",
                        "Em cada provação Tua mão santa me ensina",
                        "Pois a Tua palavra jamais voltará vazia"
                    ]
                ),
                LyricSection(
                    tag="Chorus",
                    liturgical_purpose="Declaração jubilosa da fidelidade eterna de Deus",
                    lines=[
                        "A Tua graça me basta, ó Senhor!",
                        "Teu poder se aperfeiçoa no meu clamor!",
                        "Se no vale eu passar, sei que Tu comigo estás,",
                        "Minha âncora bendita, minha rocha e minha paz!"
                    ]
                ),
                LyricSection(
                    tag="Bridge",
                    liturgical_purpose="Clímax da consagração e vitória na Cruz",
                    lines=[
                        "Pela cruz de Cristo eu aprendo a esperar,",
                        "Pois quem começou a boa obra vai completar!",
                        "Nem a morte, nem a dor vão me separar",
                        "Do amor soberano que veio me resgatar!"
                    ]
                ),
                LyricSection(
                    tag="Outro",
                    liturgical_purpose="Descanso pacífico na soberania de Deus",
                    lines=[
                        "Tu és fiel, Senhor...",
                        "Minha fé descansa em Ti.",
                        "Para sempre amém."
                    ]
                )
            ]
        )
