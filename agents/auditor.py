"""
Agente 3: Auditor Doutrinário & Métrico.
Atua como o Crítico Rigoroso (Actor-Critic Pattern) avaliando a letra segundo a ortodoxia bíblica,
centralidade de Deus, métrica para canto e ausência de clichês ou heresias.
"""

from typing import Type
from pydantic import BaseModel
from .base import BaseAgent
from schemas import SongDraft, TheologicalDossier, AuditReport
import config


AUDITOR_SYSTEM_PROMPT = """Você é um Auditor Doutrinário e Crítico Hinológico de alta exigência teológica e estética musical.
Sua missão é auditar a letra de adoração proposta antes que ela seja transformada em áudio.

CRITÉRIOS DE AUDITORIA:
1. ORTODOXIA E CRISTOCENTRISMO:
   - A letra exalta a Deus por quem Ele é, ou descamba para o antropocentrismo egoísta ("eu quero a bênção", "eu sou campeão")?
   - Há alguma afirmação ambígua que possa flertar com heresias históricas (ex: arianismo, pelagianismo, teologia da prosperidade)?
   - O sacrifício de Cristo e Sua soberania são honrados adequadamente?
2. MÉTRICA, PROSÓDIA E CANTABILIDADE:
   - Os versos são fluidos para serem cantados por uma congregação ou pelo motor de voz do Suno?
   - Há estrofes desproporcionalmente longas que fariam o cantor perder o fôlego?
   - As rimas enriquecem a poesia ou soam forçadas e infantis?
3. CRITÉRIO DE CORTE:
   - Nota mínima de aprovação: 8.5 / 10.0.
   - Se a nota for inferior a 8.5, marque approved=False e forneça instruções corretivas claras e cirúrgicas para o Compositor.
"""


class AuditorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Auditor Doutrinário & Métrico",
            role="Guardião de Ortodoxia Teológica e Excelência Poética",
            system_prompt=AUDITOR_SYSTEM_PROMPT,
        )

    def run(self, draft: SongDraft, dossier: TheologicalDossier) -> AuditReport:
        letra_formatada = ""
        for sec in draft.sections:
            letra_formatada += f"\n[{sec.tag}] ({sec.liturgical_purpose}):\n"
            letra_formatada += "\n".join(sec.lines) + "\n"

        prompt = f"""Audite detalhadamente esta canção de adoração em relação ao Dossier Teológico:

TÍTULO DA MÚSICA: {draft.title}
NOTAS DE MÉTRICA DO AUTOR: {draft.meter_notes}

DOSSIER TEOLÓGICO DE REFERÊNCIA:
- Escrituras: {', '.join(dossier.primary_scriptures)}
- Atributos Divinos: {', '.join(dossier.divine_attributes)}
- Salvaguardas: {', '.join(dossier.doctrinal_guardrails)}
- Foco Cristocêntrico: {dossier.christocentric_focus}

LETRA SUBMETIDA:
{letra_formatada}

Forneça sua pontuação e parecer rigoroso no modelo estruturado AuditReport.
"""
        return self.call_llm(prompt, AuditReport)

    def _generate_contextual_demonstration(self, user_prompt: str, response_model: Type[BaseModel]) -> AuditReport:
        # Avaliação de alta qualidade na demonstração
        return AuditReport(
            approved=True,
            score=9.4,
            theological_fidelity_score=9.8,
            poetic_prosody_score=9.0,
            strengths=[
                "Cristocentrismo impecável: a ênfase repousa na santidade de Deus e na suficiência do Cordeiro no trono.",
                "Excelente arco litúrgico: transição magistral do assombro santo (Isaías 6) para a graça purificadora e prontidão de envio.",
                "Ausência total de antropocentrismo ou triunfalismo raso.",
                "Métrica fluida e rimas solenes que facilitam a respiração e a interpretação vocal natural no Suno AI."
            ],
            critiques=[
                "A transição entre o Verso 3 e a Ponte se beneficia de uma dinâmica instrumental gradual para não soar abrupta."
            ],
            actionable_revisions=[]
        )
