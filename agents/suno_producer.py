"""
Agente 4: Diretor Musical & Engenheiro de Prompt do Suno AI.
Responsável por converter a letra auditada e a estética pretendida no pacote final
de prompts, metatags de produção musical e configurações para o Suno AI.
"""

from typing import Optional, Type
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
        self._last_draft: Optional[SongDraft] = None
        self._last_dossier: Optional[TheologicalDossier] = None
        self._last_briefing: Optional[UserBriefing] = None

    def run(self, draft: SongDraft, dossier: TheologicalDossier, briefing: UserBriefing) -> SunoSongPackage:
        self._last_draft = draft
        self._last_dossier = dossier
        self._last_briefing = briefing

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
        draft = self._last_draft
        dossier = self._last_dossier
        briefing = self._last_briefing

        style_prompt = "modern worship, CCM, emotional lead vocals, grand piano, celestial choir, swelling guitars, slow build, cinematic"
        if briefing and briefing.musical_style_hint:
            style_prompt = briefing.musical_style_hint.strip()

        bpm = briefing.tempo_hint if (briefing and briefing.tempo_hint) else "70 BPM (Andamento solene com crescendo)"
        vocal_guidance = briefing.vocal_preference if (briefing and briefing.vocal_preference) else "Voz emotiva nos versos com coral congregacional no refrão"

        if draft and draft.sections:
            blocks = ["[Atmospheric Instrumental Intro]", "[Soft Ambient Pad]"]
            for sec in draft.sections:
                tag = sec.tag
                t_low = tag.lower()
                if "verse 1" in t_low:
                    blocks.append(f"\n[{tag}]\n[Soft Intimate Vocals]")
                elif "verse" in t_low:
                    blocks.append(f"\n[{tag}]\n[Subtle Strings & Warm Piano]")
                elif "pre-chorus" in t_low:
                    blocks.append(f"\n[{tag}]\n[Drums enter softly]\n[Building Tension]")
                elif "chorus" in t_low:
                    blocks.append(f"\n[{tag}]\n[Crescendo]\n[Full Band & Choir Harmony]")
                elif "bridge" in t_low:
                    blocks.append(f"\n[{tag}]\n[Climactic Worship Explosion]\n[Passionate Lead & Full Choir]")
                elif "outro" in t_low:
                    blocks.append(f"\n[{tag}]\n[Acoustic Breakdown]\n[Gentle Piano]")
                else:
                    blocks.append(f"\n[{tag}]")
                blocks.append("\n".join(sec.lines))

            blocks.append("\n[Fade out]\n[End]")
            lyrics_with_metatags = "\n".join(blocks)
            song_title = draft.title
        else:
            song_title = "Cântico de Adoração ao Rei"
            lyrics_with_metatags = "[Atmospheric Intro]\n\n[Verse 1]\nSenhor, diante do Teu trono nos prostramos...\n\n[Outro]\n[Fade out]\n[End]"

        theo_summary = (
            dossier.exegetical_summary
            if (dossier and dossier.exegetical_summary)
            else "Composição cristocêntrica fundamentada nas Escrituras Sagradas para adoração congregacional."
        )

        return SunoSongPackage(
            song_title=song_title,
            style_of_music=style_prompt[:135],
            lyrics_with_metatags=lyrics_with_metatags,
            target_bpm=bpm,
            vocal_configuration=vocal_guidance,
            theological_summary=theo_summary,
            suno_tips=[
                "No Suno AI, ative a chave 'Custom' (Modo Personalizado).",
                "Cole o conteúdo de 'Style of Music' no campo de estilo musical.",
                "Cole o bloco completo de 'Lyrics' com as metatags entre colchetes.",
                "Se desejar prolongar o clímax espontâneo, utilize a função 'Extend' no minuto final."
            ]
        )
