"""
Agente 1: Teólogo & Exegeta Bíblico.
Responsável por extrair a fundamentação bíblica, ortodoxia cristocêntrica, atributos divinos
e salvaguardas doutrinárias para evitar antropocentrismo ou desvios heréticos.
"""

from typing import Type
from pydantic import BaseModel
from .base import BaseAgent
from schemas import UserBriefing, TheologicalDossier


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
        """Busca e sugere rapidamente referências bíblicas sólidas para um tema específico."""
        t_lower = theme.lower()
        if any(w in t_lower for w in ["santidade", "santo", "trono", "majestade"]):
            return [
                "Isaías 6:1-8 (A visão do trono e dos serafins)",
                "Apocalipse 4:8-11 (Santo, Santo, Santo é o Senhor)",
                "1 Pedro 1:15-16 (Sede santos como Eu sou santo)",
                "Salmo 99:5 (Exaltai ao Senhor nosso Deus)"
            ]
        elif any(w in t_lower for w in ["graça", "cruz", "redenção", "sangue", "salvação"]):
            return [
                "Efésios 2:8-10 (Pela graça sois salvos mediante a fé)",
                "Romanos 5:1-8 (Justificados pela fé, temos paz com Deus)",
                "Tito 2:11-14 (A graça de Deus se manifestou salvadora)",
                "Isaías 53:4-6 (O servo sofredor e a redenção na cruz)"
            ]
        elif any(w in t_lower for w in ["provação", "perseverança", "dor", "luta", "força", "refúgio"]):
            return [
                "Tiago 1:2-4 (A fé provada gerando perseverança)",
                "Romanos 8:31-39 (Nada nos separará do amor de Deus)",
                "2 Coríntios 12:9 (A minha graça te basta)",
                "Salmo 46:1-3 (Deus é o nosso refúgio e fortaleza)"
            ]
        elif any(w in t_lower for w in ["gratidão", "louvor", "júbilo", "celebração", "vitória"]):
            return [
                "Salmo 100:1-5 (Celebrai com júbilo ao Senhor)",
                "Salmo 103:1-5 (Bendize, ó minha alma, ao Senhor)",
                "Filipenses 4:4-7 (Alegrai-vos sempre no Senhor)",
                "Colossenses 3:15-17 (Com salmos, hinos e cânticos espirituais)"
            ]
        return [
            "Salmo 145:1-7 (Celebração da grandeza e bondade de Deus)",
            "João 1:14-17 (O Verbo se fez carne cheio de graça e verdade)",
            "Apocalipse 5:9-13 (Digno é o Cordeiro de receber honra e glória)"
        ]

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

    def _generate_contextual_demonstration(self, user_prompt: str, response_model: Type[BaseModel]) -> TheologicalDossier:
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
