"""
Agente 4: Diretor Musical & Engenheiro de Prompt do Suno AI.
Responsável por converter a letra auditada e a estética pretendida no pacote final
de prompts, metatags de produção musical e configurações para o Suno AI.
"""

from typing import Type
from pydantic import BaseModel
from .base import BaseAgent
from schemas import SongDraft, TheologicalDossier, UserBriefing, SunoSongPackage


SUNO_PRODUCER_SYSTEM_PROMPT = """Você é um Produtor Musical Especialista no motor de geração de áudio do Suno AI (v3.5, v4 e v4.5).
Sua missão é preparar o pacote definitivo para o usuário colar diretamente no modo 'Custom' do Suno.

REGRAS DE ENGENHARIA PARA O SUNO AI:
1. CAMPO 'STYLE OF MUSIC' (LIMITE DE 120-140 CARACTERES):
   - Deve ser uma lista concisa de tags separadas por vírgula em inglês (pois o modelo base do Suno responde com muito mais precisão em inglês musical).
   - Fórmula: [Gênero Principal], [Subgênero/Vibe], [Tipo Vocal], [Instrumentos Chave], [Dinâmica de Produção].
   - Exemplo: modern worship, CCM, male emotional lead, celestial choir, grand piano, swelling electric guitars, slow build, cinematic
2. CAMPO 'LYRICS' E METATAGS ENTRE COLCHETES:
   - O Suno utiliza colchetes como metatags de controle instrumental e arranjo.
   - Intercale tags estruturais e de dinâmica:
     [Atmospheric Piano Intro], [Verse 1], [Verse 2], [Pre-Chorus], [Drums enter],
     [Chorus], [Full Band & Choir], [Bridge], [Acoustic Breakdown], [Explosive Worship],
     [Outro], [Fade out], [End].
   - NUNCA inclua prosa ou instruções soltas dentro dos colchetes que o modelo possa cantar por engano.
3. ORIENTAÇÃO DE GERAÇÃO:
   - Forneça recomendações práticas sobre BPM, pacing e como usar a ferramenta 'Extend' caso o usuário queira expandir a música para além de 3 ou 4 minutos.
"""


class SunoProducerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Diretor Musical Suno AI",
            role="Engenheiro de Áudio e Arquiteto de Metatags",
            system_prompt=SUNO_PRODUCER_SYSTEM_PROMPT,
        )

    def run(self, draft: SongDraft, dossier: TheologicalDossier, briefing: UserBriefing) -> SunoSongPackage:
        prompt = f"""Gere o pacote definitivo para o Suno AI no modelo SunoSongPackage:
Título da Música: {draft.title}
Estilo Desejado pelo Usuário: {briefing.musical_style_hint} | {briefing.tempo_hint}
Preferência Vocal: {briefing.vocal_preference}
Síntese Teológica: {dossier.exegetical_summary}

Estrutura da Letra Original:
"""
        for sec in draft.sections:
            prompt += f"\n[{sec.tag}]\n" + "\n".join(sec.lines) + "\n"

        return self.call_llm(prompt, SunoSongPackage)

    def _generate_contextual_demonstration(self, user_prompt: str, response_model: Type[BaseModel]) -> SunoSongPackage:
        # Extração de estilo musical inteligente
        if "Isaías" in user_prompt or "Trono" in user_prompt or "Glória" in user_prompt or "Santidade" in user_prompt:
            style_prompt = "modern worship, CCM, male emotional lead, grand piano, celestial choir, swelling guitars, slow build, cinematic"
            bpm = "68 - 72 BPM (Andamento solene em 4/4 com pulsação lenta)"
            vocal_guidance = "Voz masculina emotiva e solene nos versos; coral congregacional harmônico forte no refrão e na ponte."
            
            lyrics_with_metatags = """[Atmospheric Grand Piano Intro]
[Ambient Synth Pad]

[Verse 1]
[Soft Piano]
No ano em que o rei terreno faleceu
Meus olhos viram o verdadeiro Rei
Sentado sobre um alto e sublime trono
E a orla de Suas vestes enchia o templo santo

[Verse 2]
[Subtle Cello & Swelling Pads]
Serafins cobriam o rosto em temor
Com seis asas a voar ao Seu redor
E clamavam em um uníssono trovão
Fazendo estremecer os alicerces do chão

[Pre-Chorus]
[Drums enter softly]
[Building Tension]
A casa se encheu de glória e fumaça
A criação inteira curva a fronte em graça
E a nossa voz se une ao coro celestial:

[Chorus]
[Crescendo]
[Full Band Explosion]
[Choir Harmony]
Santo, Santo, Santo é o Senhor dos Exércitos!
Todo-Poderoso, Deus que era e que é!
Toda a terra está cheia da Tua glória!
Santo, Santo, reina para sempre em Teu trono!

[Verse 3]
[Acoustic Breakdown]
[Soft Piano & Guitar]
Ai de mim, que sou um homem impuro
De lábios maculados em meio à escuridão
Mas do altar veio a brasa acesa em amor
Tocou meu ser e apagou a transgressão

[Pre-Chorus]
[Drums building up]
E ouvi a voz do Deus que me chamou:
"A quem enviarei? Quem há de ir por nós?"
E o meu coração, quebrantado ao Teu altar,
Respondeu com temor:

[Chorus]
[Explosive Worship]
[Powerful Passionate Vocals]
Santo, Santo, Santo é o Senhor dos Exércitos!
Todo-Poderoso, Deus que era e que é!
Toda a terra está cheia da Tua glória!
Santo, Santo, reina para sempre em Teu trono!

[Bridge]
[Full Celestial Choir]
[Driving Drums & Swelling Guitars]
Purificado pelo sangue do Cordeiro,
Aqui estou, Senhor, envia-me a mim!
Digno é o Cordeiro que foi morto e ressurgiu!
Ao que está no trono seja a honra e o louvor!

[Bridge 2]
[Climactic Explosion]
Santo é o Senhor!
Digno é o Cordeiro!
Para sempre e sempre!

[Chorus]
[Maximum Energy]
[Full Congregational Choir]
Santo, Santo, Santo é o Senhor dos Exércitos!
Todo-Poderoso, Deus que era e que é!
Toda a terra está cheia da Tua glória!
Santo, Santo, reina para sempre em Teu trono!

[Outro]
[Acoustic Breakdown]
[Solo Soft Piano]
Santo... Tu és Santo...
Toda a terra se prostra aos Teus pés.
Eis-me aqui, Senhor.
Envia-me a mim.

[Fade out]
[End]"""

            return SunoSongPackage(
                song_title="A Glória do Teu Trono",
                style_of_music=style_prompt,
                lyrics_with_metatags=lyrics_with_metatags,
                target_bpm=bpm,
                vocal_configuration=vocal_guidance,
                theological_summary="Fundamentada em Isaías 6 e Apocalipse 4. Foco absoluto na santidade triúna de Deus e na purificação pela graça para consagração ao envio.",
                suno_tips=[
                    "No Suno, ative a chave 'Custom' (Modo Personalizado).",
                    "Cole o conteúdo exato de 'style_of_music' no campo 'Style of Music' (atenção para não exceder 120 caracteres para máxima fidelidade).",
                    "Cole o bloco completo de 'lyrics_with_metatags' no campo 'Lyrics'.",
                    "Dica de geração: Se o Suno finalizar antes do fim da letra, use a opção 'Extend' a partir do minuto do solo ou do refrão final."
                ]
            )

        # Fallback genérico para outros temas
        return SunoSongPackage(
            song_title="A Graça Que Sustenta",
            style_of_music="modern worship, organic CCM, male passionate lead, acoustic guitar, piano, swelling pads, slow build, emotional",
            lyrics_with_metatags="[Acoustic Guitar Intro]\n\n[Verse 1]\nQuando a tempestade cerca o caminhar...\n\n[Chorus]\n[Crescendo]\nA Tua graça me basta, ó Senhor!...\n\n[Outro]\n[Fade out]\n[End]",
            target_bpm="74 BPM",
            vocal_configuration="Voz masculina apaixonada e calorosa; backing vocals sutis.",
            theological_summary="Inspirada em Tiago 1 e 2 Coríntios 12. A suficiência de Cristo na fraqueza humana.",
            suno_tips=[
                "Cole o prompt no campo 'Style of Music' do Suno em modo Custom.",
                "Utilize fones para verificar a clareza da pronúncia das palavras cantadas."
            ]
        )
