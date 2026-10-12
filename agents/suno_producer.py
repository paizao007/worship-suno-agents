"""
Agente 4: Diretor Musical & Engenheiro de Prompt do Suno AI.
Responsável por analisar o Tema e a Reflexão Bíblica gerada pelo Agente Teólogo e criar
dinamicamente o Estilo Musical, Preferência Vocal, Andamento/Dinâmica e Metatags do Suno AI.
"""

import random
import unicodedata
from typing import Optional, Type
from pydantic import BaseModel
from .base import BaseAgent
from schemas import SongDraft, TheologicalDossier, UserBriefing, SunoSongPackage


SUNO_PRODUCER_SYSTEM_PROMPT = """Você é um Produtor Musical Especialista no motor de geração de áudio do Suno AI (v3.5, v4 e v4.5).
Sua missão é criar a identidade sonora, arranjo, voz, andamento e metatags para a canção com base no Tema e na Reflexão Bíblica do Agente Teólogo.

REGRAS DE ENGENHARIA PARA O SUNO AI:
1. CAMPO 'STYLE OF MUSIC' (LIMITE DE 120-140 CARACTERES):
   - Lista concisa de tags separadas por vírgula em inglês.
   - Fórmula: [Gênero Principal], [Subgênero/Vibe], [Tipo Vocal], [Instrumentos Chave], [Dinâmica de Produção].
2. CAMPO 'LYRICS' E METATAGS ENTRE COLCHETES:
   - O Suno utiliza colchetes como metatags de controle instrumental e arranjo.
   - Intercale tags estruturais e de dinâmica alinhadas aos instrumentos escolhidos.
"""


def _norm(text: str) -> str:
    nfkd = unicodedata.normalize("NFKD", (text or "").lower().strip())
    return "".join(c for c in nfkd if not unicodedata.combining(c))


# Banco inteligente de Arranjos Musicais por Atmosfera Teológica / Reflexão Bíblica
THEMATIC_ARRANGEMENTS = {
    "amor_intimo": [
        {
            "arrangement_name": "Acústico Devocional Intimista (Violão, Violoncelo & Voz Feminina)",
            "style_of_music": "intimate acoustic worship, fingerpicked guitar, warm cello, soft piano, tender female vocals, emotional build",
            "vocal_preference": "Voz feminina suave e intimista nos versos, abrindo com harmonia vocal no refrão",
            "tempo_dynamics": "Lento devocional (66 BPM) começando em voz e violão e crescendo com violoncelo",
            "metatags": {
                "intro": ["[Fingerpicked Acoustic Guitar Intro]", "[Warm Cello Melody]"],
                "verse1": "[Tender Female Vocals]\n[Intimate Acoustic Guitar]",
                "verse2": "[Soft Piano & Cello Enter]\n[Warm Vocal Harmony]",
                "prechorus": "[Subtle Percussive Swell]\n[Growing Emotion]",
                "chorus": "[Emotional Chorus]\n[Full Acoustic Band & Backing Choir]",
                "bridge": "[Spontaneous Devotional Climax]\n[Soaring Female Lead & Strings]",
                "outro": "[Gentle Acoustic Guitar Outro]\n[Whispered Prayer]"
            }
        },
        {
            "arrangement_name": "Adoração Profética Soaking (Piano Rhodes, Pads & Dueto Vocal)",
            "style_of_music": "prophetic worship ballad, warm rhodes piano, ambient synth pads, male and female vocal duet, slow crescendo",
            "vocal_preference": "Dueto vocal (masculino e feminino) em harmonia apaixonada e suave",
            "tempo_dynamics": "Fluido e contemplativo (68 BPM) com atmosfera envolvente e refrão intenso",
            "metatags": {
                "intro": ["[Warm Rhodes Piano Intro]", "[Ethereal Synth Pad]"],
                "verse1": "[Gentle Male Vocal]\n[Soft Rhodes & Ambient Pad]",
                "verse2": "[Female Vocal Joins in Duet]\n[Deep Bass & Subtle Drums]",
                "prechorus": "[Swelling Guitars]\n[Building Devotion]",
                "chorus": "[Passionate Vocal Duet]\n[Full Worship Band & Lush Strings]",
                "bridge": "[Climactic Prophetic Worship]\n[Soaring Harmonies & Delayed Guitar]",
                "outro": "[Soft Piano & Ambient Pad Fade]\n[Intimate Ending]"
            }
        },
        {
            "arrangement_name": "Modern Worship Congregacional (Grand Piano, Guitarras & Voz Masculina)",
            "style_of_music": "modern congregational worship, grand piano, ambient electric guitars, emotional male lead, choir, anthem",
            "vocal_preference": "Voz masculina emotiva nos versos com coral congregacional forte no refrão",
            "tempo_dynamics": "Moderado solene (72 BPM) iniciando no piano e explodindo no refrão",
            "metatags": {
                "intro": ["[Atmospheric Grand Piano Intro]", "[Swelling Ambient Guitar]"],
                "verse1": "[Emotional Male Lead Vocal]\n[Grand Piano Only]",
                "verse2": "[Warm Bass & Soft Tom Drums]\n[Subtle Strings]",
                "prechorus": "[Drums Build Tension]\n[Rising Guitars]",
                "chorus": "[Anthemic Chorus]\n[Full Band & Congregational Choir]",
                "bridge": "[Explosive Worship Bridge]\n[Passionate Lead & Full Choir]",
                "outro": "[Acoustic Piano Breakdown]\n[Reverent Fade Out]"
            }
        }
    ],
    "amor_agape_cruz": [
        {
            "arrangement_name": "Gospel Soul & Coral Ágape (Piano, Hammond B3 & Coral Black Gospel)",
            "style_of_music": "soulful gospel ballad, grand piano, warm hammond organ, soulful female lead, rich gospel choir, emotional climax",
            "vocal_preference": "Voz feminina soulful potente com grande coral gospel harmônico respondendo",
            "tempo_dynamics": "Balada Soul cadenciada (70 BPM) com grande explosão coral no refrão e ponte",
            "metatags": {
                "intro": ["[Soulful Grand Piano Intro]", "[Warm Hammond B3 Organ]"],
                "verse1": "[Soulful Female Lead Vocal]\n[Expressive Piano & Soft Organ]",
                "verse2": "[Groovy Gospel Bass & Rimshot Drums]\n[Soft Choir Oohs]",
                "prechorus": "[Choir Harmony Swell]\n[Drum Fill Build]",
                "chorus": "[Powerful Gospel Chorus]\n[Full 3-Part Gospel Choir & Band]",
                "bridge": "[Key Modulation Climax]\n[Passionate Vocal Melisma & Choir Call-Response]",
                "outro": "[Gentle Piano & Hammond Chord]\n[Choir Amen]"
            }
        },
        {
            "arrangement_name": "Power Ballad da Cruz (Guitarras Limpas, Cordas & Dueto Emocional)",
            "style_of_music": "christian power ballad, clean electric guitar, orchestral strings, male and female duet, dramatic drums, epic chorus",
            "vocal_preference": "Dueto masculino e feminino emotivo com coro sinfônico no clímax",
            "tempo_dynamics": "Moderado dramático (74 BPM) crescendo até solo de guitarra e clímax coral",
            "metatags": {
                "intro": ["[Clean Arpeggiated Guitar Intro]", "[Orchestral Cello & Piano]"],
                "verse1": "[Warm Male Lead Vocal]\n[Clean Guitar & Piano]",
                "verse2": "[Female Vocal Harmony Enters]\n[Steady Drums & Strings]",
                "prechorus": "[Crescendo]\n[Timpani & Snare Build]",
                "chorus": "[Epic Worship Chorus]\n[Soaring Duet, Full Choir & Electric Guitars]",
                "bridge": "[Emotional Guitar Solo & Bridge]\n[Full Symphony & Congregational Voices]",
                "outro": "[Soft Piano & Solo Violin]\n[Fade Out]"
            }
        },
        {
            "arrangement_name": "Cinematic Worship Redenção (Piano de Cauda, Violoncelo & Voz Masculina)",
            "style_of_music": "cinematic worship anthem, grand piano, solo cello, passionate male vocals, celestial choir, slow build, majestic",
            "vocal_preference": "Voz masculina grave e apaixonada com coro celestial no refrão",
            "tempo_dynamics": "Lento majestoso (68 BPM) evoluindo de intimista para épico cinematográfico",
            "metatags": {
                "intro": ["[Solo Cello & Grand Piano Intro]", "[Cinematic Atmosphere]"],
                "verse1": "[Deep Reverent Male Vocal]\n[Soft Piano]",
                "verse2": "[Strings Section Enters]\n[Deep Heartbeat Drums]",
                "prechorus": "[Rising Brass & Strings]\n[Building Intensity]",
                "chorus": "[Majestic Anthem Chorus]\n[Full Orchestra, Band & Celestial Choir]",
                "bridge": "[Thunderous Drums & Choir Climax]\n[Passionate Tenor High Notes]",
                "outro": "[Quiet Grand Piano Outro]\n[Peaceful Resolution]"
            }
        }
    ],
    "santidade_trono": [
        {
            "arrangement_name": "Épico Sinfônico do Trono (Orquestra, Timpani, Harpa & Coral Sacro)",
            "style_of_music": "cinematic orchestral worship, symphony strings, brass swell, timpani, powerful lead vocal, 4-part sacred choir, majestic",
            "vocal_preference": "Solista imponente com Coral Sacro Polifônico (Soprano, Contralto, Tenor, Baixo)",
            "tempo_dynamics": "Solene e grandioso (68 BPM) com dinâmica de sala do trono celestial",
            "metatags": {
                "intro": ["[Celestial Harp & Symphony Strings Intro]", "[Distant Angelic Choir]"],
                "verse1": "[Reverent Solo Vocal]\n[Grand Piano & Soft Strings]",
                "verse2": "[French Horns & Cello Countermelody]\n[Timpani Roll]",
                "prechorus": "[Orchestral Crescendo]\n[Choir Voices Rising]",
                "chorus": "[Majestic Throne Room Chorus]\n[Full Symphony Orchestra & 4-Part Sacred Choir]",
                "bridge": "[Holy Holy Holy Climax]\n[Brass Fanfare, Timpani & Thunderous Choir]",
                "outro": "[Ethereal Choir & Harp Fade]\n[Sacred Silence]"
            }
        },
        {
            "arrangement_name": "Arena Worship Solene (Piano, Guitarras c/ Reverb, Synth & Voz Feminina)",
            "style_of_music": "modern arena worship, grand piano, shimmer reverb guitars, soaring female lead vocals, massive congregational choir",
            "vocal_preference": "Voz feminina potente e ungida com milhares de vozes congregacionais no refrão",
            "tempo_dynamics": "Moderado solene (72 BPM) com paredes de guitarra atmosférica e grande clímax",
            "metatags": {
                "intro": ["[Shimmer Guitar & Grand Piano Intro]", "[Deep Sub Bass Pad]"],
                "verse1": "[Clear Anointed Female Vocal]\n[Sparse Piano & Ambient Pad]",
                "verse2": "[Tom-Heavy Worship Drums]\n[Delayed Electric Guitar]",
                "prechorus": "[Rising Synth & Snare Build]\n[Congregation Singing Along]",
                "chorus": "[Massive Arena Worship Chorus]\n[Soaring Female Lead & Huge Choir]",
                "bridge": "[Explosive Worship Bridge]\n[Full Band Wall of Sound & Ad-libs]",
                "outro": "[Gentle Piano & Ambient Reverb]\n[Fade Out]"
            }
        }
    ],
    "avivamento_fogo": [
        {
            "arrangement_name": "Pentecostal de Avivamento & Impacto (Banda Completa, Metais & Coral)",
            "style_of_music": "pentecostal revival worship, passionate powerhouse vocals, driving drums, electric guitar, piano, choir, intense build",
            "vocal_preference": "Voz líder explosiva e pentecostal com coral vibrante em clamor",
            "tempo_dynamics": "Crescente e intenso (82 BPM) com bateria marcada e explosão de avivamento",
            "metatags": {
                "intro": ["[Dramatic Piano & Electric Guitar Intro]", "[Driving Drum Fill]"],
                "verse1": "[Passionate Revival Lead Vocal]\n[Piano & Bass Groove]",
                "verse2": "[Full Rhythm Section Enters]\n[Organ & Overdriven Guitar]",
                "prechorus": "[Snare Roll Crescendo]\n[Choir Voices Rising in Power]",
                "chorus": "[Explosive Revival Chorus]\n[Powerhouse Lead, Brass & Full Choir]",
                "bridge": "[Pentecostal Fire Bridge]\n[Intense Band Jam & Spontaneous Choir Cry]",
                "outro": "[Final Climactic Chord]\n[Worship Applause & Piano Fade]"
            }
        },
        {
            "arrangement_name": "Rock Worship Contemporâneo de Batalha (Guitarras, Bateria Forte & Voz Masculina)",
            "style_of_music": "christian rock worship, driving electric guitars, punchy drums, passionate male vocals, anthemic chorus, high energy",
            "vocal_preference": "Voz masculina firme e vibrante com backing vocals em uníssono no refrão",
            "tempo_dynamics": "Energético e firme (98 BPM) com pulsação constante de guitarra e bateria",
            "metatags": {
                "intro": ["[Anthemic Electric Guitar Riff Intro]", "[Driving Rock Drums]"],
                "verse1": "[Strong Male Lead Vocal]\n[Palm-Muted Guitar & Bass]",
                "verse2": "[Rhythm Guitars Open Up]\n[Energetic Drum Beat]",
                "prechorus": "[Building Guitar Octaves]\n[Crescendo]",
                "chorus": "[High-Energy Anthemic Chorus]\n[Distorted Guitars, Full Drums & Backing Choir]",
                "bridge": "[Epic Guitar Solo & Worship Cry]\n[Half-Time Heavy Groove]",
                "outro": "[Final Anthemic Riff]\n[Strong Ending]"
            }
        }
    ],
    "celebracao_jubilo": [
        {
            "arrangement_name": "Praise & Celebração Congregacional Alegre (Pop Gospel, Metais & Coral)",
            "style_of_music": "upbeat gospel praise, joyful brass section, funky bassline, rhythmic piano, energetic lead vocal, celebratory choir",
            "vocal_preference": "Líder alegre e contagiante com coral de celebração e palmas no refrão",
            "tempo_dynamics": "Rápido e festivo (118 BPM) em clima de gratidão, festa e júbilo",
            "metatags": {
                "intro": ["[Upbeat Brass & Rhythmic Piano Intro]", "[Funky Gospel Bass & Drums]"],
                "verse1": "[Joyful Lead Vocal]\n[Upbeat Piano & Tight Drums]",
                "verse2": "[Choir Call and Response]\n[Rhythm Guitar & Horn Stabs]",
                "prechorus": "[Handclaps & Drum Build]\n[Rising Excitement]",
                "chorus": "[Celebratory Praise Chorus]\n[Full Gospel Choir, Brass Section & Groove]",
                "bridge": "[Joyful Dance & Praise Breakdown]\n[Bass Solo & Choir Vamp]",
                "outro": "[Big Finale Brass Hit]\n[Joyful Ending]"
            }
        },
        {
            "arrangement_name": "Pop Worship Brasileiro / Acústico Alegre (Violão Aço, Percussão & Dueto)",
            "style_of_music": "upbeat acoustic pop worship, bright steel guitar, rhythmic percussion, warm bass, joyful male and female vocals",
            "vocal_preference": "Dueto masculino e feminino alegre e luminoso com coro jovem",
            "tempo_dynamics": "Médio alegre (106 BPM) com violão rítmico e batida contagiante",
            "metatags": {
                "intro": ["[Bright Acoustic Guitar & Percussion Intro]", "[Uplifting Whistle & Piano]"],
                "verse1": "[Warm Joyful Male Vocal]\n[Strummed Acoustic Guitar & Cajon]",
                "verse2": "[Bright Female Vocal Joins]\n[Full Drums & Bass Groove]",
                "prechorus": "[Rhythmic Claps & Vocal Oohs]\n[Building Joy]",
                "chorus": "[Uplifting Pop Worship Chorus]\n[Male & Female Duet with Youth Choir]",
                "bridge": "[Acoustic Breakdown & Singalong]\n[Everyone Singing Together]",
                "outro": "[Upbeat Acoustic Strumming Outro]\n[Clean End]"
            }
        }
    ],
    "paz_refugio_cura": [
        {
            "arrangement_name": "Piano Neoclássico & Cordas de Consolo (Piano Solo, Violino & Voz Feminina)",
            "style_of_music": "neoclassical devotional worship, solo grand piano, expressive violin, warm strings, gentle female vocals, peaceful",
            "vocal_preference": "Voz feminina doce, serena e consoladora com cordas suaves ao fundo",
            "tempo_dynamics": "Calmo e restaurador (64 BPM) transmitindo paz profunda e descanso na alma",
            "metatags": {
                "intro": ["[Gentle Neoclassical Piano Intro]", "[Expressive Solo Violin]"],
                "verse1": "[Soothing Female Vocal]\n[Delicate Grand Piano]",
                "verse2": "[Warm String Quartet Enters]\n[Soft Acoustic Guitar]",
                "prechorus": "[Swelling Strings]\n[Hopeful Crescendo]",
                "chorus": "[Peaceful Worship Chorus]\n[Clear Female Lead, Lush Strings & Soft Choir]",
                "bridge": "[Moment of Healing & Peace]\n[Piano Arpeggios & Angelic Harmonies]",
                "outro": "[Solo Piano & Violin Fade]\n[Peaceful Silence]"
            }
        },
        {
            "arrangement_name": "Folk Worship de Esperança (Violão Dedilhado, Piano Suave & Voz Masculina)",
            "style_of_music": "indie folk worship, warm acoustic guitar, soft upright piano, comforting male vocals, cello, hopeful crescendo",
            "vocal_preference": "Voz masculina acolhedora e serena nos versos, ganhando força de fé no refrão",
            "tempo_dynamics": "Moderado tranquilo (72 BPM) crescendo da lágrima para a certeza da vitória",
            "metatags": {
                "intro": ["[Warm Fingerpicked Guitar & Upright Piano]", "[Soft Cello Drone]"],
                "verse1": "[Comforting Male Vocal]\n[Intimate Guitar & Piano]",
                "verse2": "[Brush Drums & Upright Bass]\n[Subtle Vocal Harmony]",
                "prechorus": "[Cello & Acoustic Strum Build]\n[Rising Hope]",
                "chorus": "[Hopeful Folk Worship Chorus]\n[Full Acoustic Ensemble & Warm Choir]",
                "bridge": "[Declaration of Faith Bridge]\n[Passionate Vocals & Soaring Strings]",
                "outro": "[Gentle Acoustic Chord]\n[Peaceful End]"
            }
        }
    ]
}


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
        self._last_arrangement: Optional[dict] = None

    def design_arrangement_from_reflection(
        self,
        theme: str,
        biblical_reference: str = "",
        biblical_reflection: str = "",
        exclude_style: str = ""
    ) -> dict:
        """
        Analisa o Tema + Versículo + Reflexão Bíblica e gera dinamicamente uma nova
        configuração de Estilo Musical, Voz, Andamento/Dinâmica e Metatags, garantindo
        que mude a cada geração.
        """
        combined = _norm(f"{theme} {biblical_reference} {biblical_reflection}")

        # Classifica a família estética pela reflexão bíblica e tema
        if any(w in combined for w in ["primeiro amor", "amo-te", "madrugada", "sede", "intimidade", "meu amado", "coracao", "devocao"]):
            pool_key = "amor_intimo"
        elif any(w in combined for w in ["amor", "agape", "cruz", "sangue", "graca", "redencao", "perdao", "arrepend", "cordeiro"]):
            pool_key = "amor_agape_cruz"
        elif any(w in combined for w in ["santidade", "santo", "trono", "serafins", "majestade", "gloria", "rei", "exodo", "isaias 6", "apocalipse"]):
            pool_key = "santidade_trono"
        elif any(w in combined for w in ["espirito", "fogo", "avivamento", "pentecostes", "uncao", "vento", "poder", "guerra", "batalha"]):
            pool_key = "avivamento_fogo"
        elif any(w in combined for w in ["gratidao", "alegria", "jubilo", "celebr", "festa", "louvor", "acoes de gracas", "vitoria"]):
            pool_key = "celebracao_jubilo"
        elif any(w in combined for w in ["paz", "descanso", "refugio", "cura", "consolo", "lagrima", "medo", "ansiedade", "pastor", "salmo 23", "salmo 91", "salmo 121"]):
            pool_key = "paz_refugio_cura"
        else:
            # Combina todos os pools temáticos para variar amplamente
            pool_key = random.choice(list(THEMATIC_ARRANGEMENTS.keys()))

        candidates = list(THEMATIC_ARRANGEMENTS[pool_key])
        # Adiciona 1 opção complementar de outra família compatível para ampliar a variedade
        if pool_key == "amor_agape_cruz":
            candidates.extend(THEMATIC_ARRANGEMENTS["amor_intimo"])
        elif pool_key == "amor_intimo":
            candidates.extend(THEMATIC_ARRANGEMENTS["amor_agape_cruz"])

        exclude_norm = (exclude_style or "").strip().lower()
        if exclude_norm.startswith("auto:"):
            exclude_norm = exclude_norm[5:].strip()
        filtered = [
            arr for arr in candidates
            if arr["style_of_music"].lower() != exclude_norm
            and arr["arrangement_name"].lower() != exclude_norm
        ]
        if not filtered:
            filtered = candidates

        chosen = random.choice(filtered)
        ref_short = biblical_reference.split("(")[0].strip() if biblical_reference else "a passagem bíblica"
        producer_rationale = (
            f"Para o tema '{theme}' e a reflexão em {ref_short}, o Agente Musical desenhou o arranjo "
            f"'{chosen['arrangement_name']}', unindo {chosen['vocal_preference'].lower()} e andamento {chosen['tempo_dynamics'].lower()}."
        )

        result = dict(chosen)
        result["producer_rationale"] = producer_rationale
        self._last_arrangement = result
        return result

    def run(self, draft: SongDraft, dossier: TheologicalDossier, briefing: UserBriefing) -> SunoSongPackage:
        self._last_draft = draft
        self._last_dossier = dossier
        self._last_briefing = briefing

        # Se o usuário estiver no modo automático (ou para gerar nova configuração baseada na reflexão bíblica):
        arr = self.design_arrangement_from_reflection(
            theme=briefing.theme,
            biblical_reference=briefing.biblical_reference,
            biblical_reflection=dossier.exegetical_summary,
            exclude_style=briefing.musical_style_hint
        )

        # Se o briefing veio com estilo "auto" ou vazio, aplica o estilo gerado pela reflexão;
        # caso o usuário tenha escolhido um preset manual específico na hora, respeita as tags dele mas usa a reflexão.
        hint_clean = (briefing.musical_style_hint or "").strip()
        if not hint_clean or hint_clean.lower().startswith("auto"):
            briefing.musical_style_hint = arr["style_of_music"]
            briefing.vocal_preference = arr["vocal_preference"]
            briefing.tempo_hint = arr["tempo_dynamics"]

        prompt = f"""Gere o pacote definitivo para o Suno AI no modelo SunoSongPackage:
Título da Música: {draft.title}
Estilo Gerado pela Reflexão Bíblica: {briefing.musical_style_hint} | {briefing.tempo_hint}
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
        arr = self._last_arrangement or THEMATIC_ARRANGEMENTS["amor_intimo"][0]

        style_prompt = (
            briefing.musical_style_hint.strip()
            if (briefing and briefing.musical_style_hint and not briefing.musical_style_hint.lower().startswith("auto"))
            else arr["style_of_music"]
        )
        bpm = (
            briefing.tempo_hint.strip()
            if (briefing and briefing.tempo_hint)
            else arr["tempo_dynamics"]
        )
        vocal_guidance = (
            briefing.vocal_preference.strip()
            if (briefing and briefing.vocal_preference)
            else arr["vocal_preference"]
        )
        meta = arr.get("metatags", THEMATIC_ARRANGEMENTS["amor_intimo"][0]["metatags"])

        if draft and draft.sections:
            blocks = list(meta.get("intro", ["[Atmospheric Instrumental Intro]"]))
            for sec in draft.sections:
                tag = sec.tag
                t_low = tag.lower()
                if "verse 1" in t_low:
                    blocks.append(f"\n[{tag}]\n{meta.get('verse1', '[Soft Intimate Vocals]')}")
                elif "verse" in t_low:
                    blocks.append(f"\n[{tag}]\n{meta.get('verse2', '[Subtle Strings & Warm Piano]')}")
                elif "pre-chorus" in t_low:
                    blocks.append(f"\n[{tag}]\n{meta.get('prechorus', '[Drums enter softly]')}")
                elif "chorus" in t_low:
                    blocks.append(f"\n[{tag}]\n{meta.get('chorus', '[Full Band & Choir Harmony]')}")
                elif "bridge" in t_low:
                    blocks.append(f"\n[{tag}]\n{meta.get('bridge', '[Climactic Worship Explosion]')}")
                elif "outro" in t_low:
                    blocks.append(f"\n[{tag}]\n{meta.get('outro', '[Gentle Piano Fade]')}")
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
                f"Arranjo Musical Gerado: {arr.get('arrangement_name', 'Worship Personalizado')}",
                f"Voz Configurada: {vocal_guidance}",
                f"Dinâmica e BPM: {bpm}",
                "No Suno AI, ative o modo 'Custom' e cole os blocos 'Style of Music' e 'Lyrics'."
            ]
        )
