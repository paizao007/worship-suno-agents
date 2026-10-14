"""
Agente 4: Diretor Musical & Engenheiro de Prompt do Suno AI (100% Dinâmico).
Analisa autonomamente o Tema, a Passagem Bíblica e a Reflexão do Agente Teólogo para
construir dinamicamente a identidade sonora, arranjo de instrumentos, tipo de voz, BPM e metatags.
Zero categorias engessadas: o produtor lê e compõe o estilo ideal para a alma de cada mensagem.
"""

import re
import random
import unicodedata
from typing import Optional, Type
from pydantic import BaseModel
from .base import BaseAgent
from schemas import SongDraft, TheologicalDossier, UserBriefing, SunoSongPackage


SUNO_PRODUCER_SYSTEM_PROMPT = """Você é um Produtor Musical Especialista no motor de áudio do Suno AI (v3.5, v4 e v4.5).
Sua missão é analisar o Tema, a Passagem Bíblica e a Reflexão Teológica para criar a identidade sonora perfeita para a canção.

DIRETRIZES DE ENGENHARIA MUSICAL PARA O SUNO AI:
1. CAMPO 'STYLE OF MUSIC' (ATÉ 180 CARACTERES):
   - Deve conter de forma concisa e sinérgica: [Gênero/Subgênero], [Instrumentos Chave], [Tipo de Voz], [BPM Exato] e [Dinâmica de Produção].
   - Exemplo Intimista: intimate acoustic worship, fingerpicked guitar, warm cello, soft piano, tender female lead vocals, vocal harmony, 66 BPM, slow emotional build
   - Exemplo Majestoso: cinematic sacred worship, grand piano, symphony strings, solemn male lead vocal, 4-part choir, 70 BPM, majestic throne room climax
2. SINTONIA COM A MENSAGEM:
   - Se o tema for ternura, pureza, oração ou ser como criança: use violão dedilhado, piano suave, violoncelo, voz terna e 64-68 BPM. NUNCA use metais de guerra ou tambores estrondosos!
   - Se o tema for celebração e gratidão: use violão folk com ritmo, piano alegre, coro festivo e 104-116 BPM.
   - Se o tema for a Cruz e Graça: use balada soul/gospel com piano, órgão suave e coral emotivo a 70 BPM.
"""


def _norm(text: str) -> str:
    nfkd = unicodedata.normalize("NFKD", (text or "").lower().strip())
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def build_complete_suno_style(base_style: str, vocal_pref: str = "", tempo_pref: str = "") -> str:
    """Garante que o campo 'style_of_music' sempre contenha Estilo + Instrumentos + Voz + BPM + Dinâmica."""
    style_clean = (base_style or "").strip().rstrip(",")
    if style_clean.lower().startswith("auto:"):
        style_clean = style_clean[5:].strip()

    s_low = style_clean.lower()
    v_low = _norm(vocal_pref)
    t_low = _norm(tempo_pref)

    # 1. Garante presença da Voz (Vocal)
    has_vocal = any(w in s_low for w in ["vocal", "voice", "lead", "duet", "choir", "tenor", "soprano", "baritone", "singer"])
    if not has_vocal:
        if "dueto" in v_low or "masculino e feminino" in v_low:
            vocal_tag = "male and female vocal duet, rich choir harmony"
        elif "feminina" in v_low and "suave" in v_low:
            vocal_tag = "tender female lead vocals, soft vocal harmony"
        elif "feminina" in v_low:
            vocal_tag = "anointed female lead vocals, warm backing choir"
        elif "coral" in v_low:
            vocal_tag = "powerful lead vocal, 4-part sacred choir harmony"
        elif "masculina" in v_low and "intima" in v_low:
            vocal_tag = "intimate gentle male lead vocals, subtle backing"
        elif "masculina" in v_low:
            vocal_tag = "emotional male lead vocals, congregational choir"
        else:
            vocal_tag = "heartfelt lead vocals, sacred choir harmony"
        style_clean = f"{style_clean}, {vocal_tag}" if style_clean else vocal_tag

    # 2. Garante presença do BPM e Dinâmica
    has_bpm = bool(re.search(r"\b\d{2,3}\s*bpm\b", style_clean, re.IGNORECASE))
    if not has_bpm:
        bpm_match = re.search(r"(\d{2,3})\s*(?:-\s*\d{2,3})?\s*bpm", tempo_pref or "", re.IGNORECASE)
        if bpm_match:
            bpm_tag = f"{bpm_match.group(1)} BPM"
        elif any(w in t_low for w in ["rapido", "vibrante", "festa", "jubilo", "120"]):
            bpm_tag = "116 BPM"
        elif any(w in t_low for w in ["medio", "alegre", "celebr", "100", "104"]):
            bpm_tag = "104 BPM"
        elif any(w in t_low for w in ["calmo", "paz", "intima", "descanso", "crianca", "colo", "64", "66"]):
            bpm_tag = "64 BPM"
        else:
            bpm_tag = "70 BPM"

        if not any(w in s_low for w in ["build", "climax", "crescendo", "peaceful", "groove"]):
            if any(w in t_low for w in ["alegre", "vibrante", "festa", "jubilo"]):
                dyn = "upbeat joyful groove"
            elif any(w in t_low for w in ["calmo", "paz", "intima", "descanso", "crianca", "colo"]):
                dyn = "pure and peaceful dynamics"
            else:
                dyn = "slow emotional build to climax"
            style_clean = f"{style_clean}, {bpm_tag}, {dyn}"
        else:
            style_clean = f"{style_clean}, {bpm_tag}"

    return style_clean[:190]


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
        Análise Sonora Autônoma:
        Lê o tema, a passagem e a reflexão teológica e compõe dinamicamente o arranjo musical,
        instrumentação, vocal, andamento em BPM e metatags estruturais.
        """
        combined = _norm(f"{theme} {biblical_reference} {biblical_reflection}")

        # 1. Atmosfera Filial / Intimista / Pureza de Criança / Descanso da Alma
        if any(w in combined for w in ["crianca", "criança", "pequeno", "pequenino", "humild", "singel", "simplicidade", "desmamar", "colo do pai", "menino", "filhinho"]):
            arrangement_name = "Acústico Singelo & Íntimo nos Braços do Pai (Piano Suave, Violão Dedilhado • 64 BPM)"
            style_of_music = "intimate acoustic worship, fingerpicked acoustic guitar, gentle upright piano, warm cello, tender heartfelt lead vocal, 64 BPM, pure and peaceful dynamics"
            vocal_preference = "Voz suave e terna, sincera e despretensiosa, cantando como uma oração no colo do Pai"
            tempo_dynamics = "Lento e sereno (64 BPM), criando um ambiente de descanso, pureza e recolhimento filial"
            metatags = {
                "intro": ["[64 BPM - Gentle & Pure Worship Tempo]", "[Fingerpicked Acoustic Guitar & Soft Upright Piano Intro]"],
                "verse1": "[Tender Gentle Lead Vocal]\n[Soft Fingerpicked Guitar Only]\n[Childlike Faith]",
                "verse2": "[Warm Cello Enters]\n[Gentle Piano Notes]\n[Peaceful Rest]",
                "prechorus": "[Soft Vocal Swell]\n[Sweet String Harmony]",
                "chorus": "[Heartfelt Intimate Chorus]\n[Pure Lead Vocals, Soft Acoustic Band & Subtle Backing Choir]",
                "bridge": "[Tender Devotional Climax]\n[Passionate Prayer in the Father's Arms]\n[Warm Strings & Upright Piano]",
                "outro": "[Quiet Acoustic Guitar Breakdown]\n[Whispered Final Prayer: 'Nos Teus braços, Pai. Amém']\n[Fade Out]"
            }

        # 2. Atmosfera de Devoção / Primeiro Amor / Sede de Deus
        elif any(w in combined for w in ["primeiro amor", "amo a deus", "te amo", "sede de deus", "intimidade", "meu amado", "coracao devoto"]):
            arrangement_name = "Acústico Devocional Intimista (Violão, Violoncelo, Voz Serena • 66 BPM)"
            style_of_music = "intimate acoustic worship, fingerpicked guitar, warm cello, soft piano, tender female lead vocals, vocal harmony, 66 BPM, slow emotional build"
            vocal_preference = "Voz suave e intimista nos versos, abrindo com harmonia vocal no refrão"
            tempo_dynamics = "Lento devocional (66 BPM) começando em voz e violão e crescendo com violoncelo"
            metatags = {
                "intro": ["[66 BPM - Slow Devotional Tempo]", "[Fingerpicked Acoustic Guitar & Warm Cello Intro]"],
                "verse1": "[Tender Female Lead Vocals]\n[Intimate Acoustic Guitar]",
                "verse2": "[Soft Piano & Cello Enter]\n[Warm Vocal Harmony]",
                "prechorus": "[Subtle Percussive Swell]\n[Growing Emotion]",
                "chorus": "[Emotional Chorus]\n[Soaring Female Lead, Acoustic Band & Backing Choir]",
                "bridge": "[Spontaneous Devotional Climax]\n[Passionate Female Lead & Lush Strings]",
                "outro": "[Gentle Acoustic Guitar Outro]\n[Whispered Female Vocal Prayer]"
            }

        # 3. Atmosfera da Cruz / Graça / Redenção / Calvário
        elif any(w in combined for w in ["cruz", "sangue", "graca", "graça", "redencao", "redenção", "calvario", "calvário", "cordeiro", "perdao", "perdão"]):
            arrangement_name = "Gospel Soul & Balada da Cruz (Piano de Cauda, Cordas, Voz Emotiva • 70 BPM)"
            style_of_music = "soulful gospel ballad, grand piano, warm hammond B3 organ, soulful lead vocals, 3-part gospel choir, 70 BPM, emotional choir climax"
            vocal_preference = "Voz solista emotiva com grande coral harmônico respondendo no refrão"
            tempo_dynamics = "Balada solene cadenciada (70 BPM) com grande explosão coral no refrão e na ponte"
            metatags = {
                "intro": ["[70 BPM - Soulful Gospel Ballad]", "[Grand Piano & Warm Hammond B3 Organ Intro]"],
                "verse1": "[Soulful Lead Vocal]\n[Expressive Piano & Soft Organ]",
                "verse2": "[Groovy Gospel Bass & Rimshot Drums]\n[Soft Choir Harmonies]",
                "prechorus": "[Choir Harmony Swell]\n[Drum Fill Build]",
                "chorus": "[Powerful Gospel Chorus]\n[Soulful Lead & Full 3-Part Gospel Choir]",
                "bridge": "[Key Modulation Climax]\n[Passionate Vocal Runs & Choir Call-Response]",
                "outro": "[Gentle Piano & Hammond Chord]\n[Choir Amen]"
            }

        # 4. Atmosfera de Celebração / Gratidão / Júbilo / Alegria
        elif any(w in combined for w in ["gratidao", "gratidão", "alegria", "jubilo", "júbilo", "celebr", "festa", "acoes de gracas", "vitoria"]):
            arrangement_name = "Folk Worship Vibrante & Júbilo Congregacional (Violões, Piano, Coral • 106 BPM)"
            style_of_music = "joyful acoustic folk worship, acoustic rhythm guitar, grand piano, driving upright bass, uplifting vocals, celebratory backing choir, 106 BPM, upbeat joyful groove"
            vocal_preference = "Voz solista alegre e contagiante com coral congregacional em júbilo"
            tempo_dynamics = "Andamento alegre e cadenciado (106 BPM) com pulsação rítmica contagiante"
            metatags = {
                "intro": ["[106 BPM - Joyful Folk Worship]", "[Acoustic Guitar Strumming & Upbeat Tambourine Intro]"],
                "verse1": "[Uplifting Lead Vocal]\n[Rhythmic Acoustic Guitar]",
                "verse2": "[Grand Piano & Shaker Enter]\n[Bouncy Acoustic Bass]",
                "prechorus": "[Rising Strumming & Claps]\n[Building Joy]",
                "chorus": "[Celebratory Folk Chorus]\n[Passionate Lead Vocals, Full Acoustic Band & Cheerful Choir]",
                "bridge": "[Congregational Celebration Climax]\n[Stomp-Clap Rhythm & Soaring Voices]",
                "outro": "[Vibrant Acoustic Outro]\n[Joyful Final Chord & Congregational Shouts of Praise]"
            }

        # 5. Atmosfera Profética / Fogo / Avivamento / Ressurreição / Ossos Secos
        elif any(w in combined for w in ["avivamento", "fogo", "espirito santo", "pentecostes", "batalha", "armadura", "poder de deus", "vento impetuoso", "ossos", "secos", "vale", "ezequiel", "sopro", "ressurreicao", "ressurreição"]):
            arrangement_name = "Modern Worship Poderoso & Clamor Profético (Guitarras, Bateria, Coral • 78 BPM)"
            style_of_music = "powerful modern worship anthem, ambient electric guitars, driving drums, passionate lead vocals, full congregational choir, 78 BPM, explosive anthemic climax"
            vocal_preference = "Voz forte e apaixonada com coro congregacional potente e clamor profético"
            tempo_dynamics = "Moderado crescente (78 BPM) iniciando etéreo e explodindo em clímax congregacional"
            metatags = {
                "intro": ["[78 BPM - Prophetic Anthem Tempo]", "[Atmospheric Swelling Electric Guitars & Cymbal Rolls]"],
                "verse1": "[Passionate Lead Vocal]\n[Subtle Guitar Arpeggios & Deep Bass]",
                "verse2": "[Steady Floor Tom Drum Beat]\n[Warm Synth Pad Layer]",
                "prechorus": "[Snare Build & Guitar Overdrive Swell]\n[Rising Clamor]",
                "chorus": "[Explosive Anthemic Chorus]\n[Powerful Lead, Wall of Guitars & Massive Choir]",
                "bridge": "[Triumphant Worship Climax]\n[Thunderous Drum Fills & Soaring Vocal Declarations]",
                "outro": "[Decrescendo to Ambient Guitar Reverb]\n[Solemn Prayer Ending]"
            }

        # 6. Atmosfera de Cura, Milagre & Restauração da Esperança
        elif any(w in combined for w in ["cura", "curado", "sarado", "sara", "cego", "jericó", "jerico", "bartimeu", "milagre", "enfermidade", "pisaduras"]):
            arrangement_name = "Worship de Esperança & Milagre (Piano, Cordas Emocionantes • 68 BPM)"
            style_of_music = "emotional modern worship, emotive piano, soaring cello and violin, passionate heartfelt lead vocal, dynamic choir, 68 BPM, emotional build to triumphant praise"
            vocal_preference = "Voz expressiva e comovente que cresce em clamor e celebração de cura"
            tempo_dynamics = "Balada devocional crescente (68 BPM) da súplica íntima à celebração do milagre"
            metatags = {
                "intro": ["[68 BPM - Worship of Hope & Healing]", "[Emotive Piano & Solo Cello Intro]"],
                "verse1": "[Tender Heartfelt Lead Vocal]\n[Soft Acoustic Piano]\n[Humble Supplication]",
                "verse2": "[Soaring Violin Enters]\n[Warm Acoustic Guitar Arpeggio]",
                "prechorus": "[Dynamic Swell in String Section]\n[Rising Faith and Expectation]",
                "chorus": "[Triumphant Healing Chorus]\n[Passionate Lead Vocals, Full Strings & Soulful Backing Choir]",
                "bridge": "[Miraculous Breakthrough Climax]\n[Full Symphony, Powerful Vocal Runs & Joyful Declaration of Faith]",
                "outro": "[Peaceful Piano & Violin Fade]\n[Reverent Gratitude & Amen]"
            }

        # 7. Atmosfera de Santidade / Trono / Soberania / Reverência
        elif any(w in combined for w in ["santidade", "santo", "trono", "majestade", "serafins", "reverencia", "temor do senhor"]):
            arrangement_name = "Épico Reverente do Trono Celestial (Piano de Cauda, Cordas, Coral Sacro • 68 BPM)"
            style_of_music = "cinematic reverent worship, grand piano, symphony strings section, solemn lead vocal, 4-part sacred choir, 68 BPM, majestic slow build"
            vocal_preference = "Solista reverente com Coral Sacro Polifônico em harmonia sublime"
            tempo_dynamics = "Lento solene (68 BPM) evoluindo com orquestra de cordas até adoração sublime"
            metatags = {
                "intro": ["[68 BPM - Solemn Sacred Tempo]", "[Grand Piano & Symphony Cello Intro]"],
                "verse1": "[Reverent Solo Lead Vocal]\n[Grand Piano & Soft Strings]",
                "verse2": "[Strings Section Deepens]\n[Subtle Orchestral Timpani Roll]",
                "prechorus": "[Choir Swell in Polyphony]\n[Ascending Wonder]",
                "chorus": "[Majestic Sacred Chorus]\n[Reverent Lead Vocal, Rich Symphony Strings & 4-Part Choir]",
                "bridge": "[Holy Throne Room Climax]\n[Full Symphony & Thunderous Chorus of Praise]",
                "outro": "[Solo Piano & Violin Fade]\n[Solemn Breath & Amen]"
            }

        # 8. Síntese Dinâmica Geral para qualquer outro tema
        else:
            arrangement_name = f"Modern Worship Contemplativo ({theme.title()} • 70 BPM)"
            style_of_music = "modern contemplative worship, grand piano, acoustic guitar, warm cello, emotional lead vocals, vocal harmony, 70 BPM, slow emotional build"
            vocal_preference = "Voz emotiva e sincera nos versos, com harmonia vocal no refrão"
            tempo_dynamics = "Moderado devocional (70 BPM) com dinâmica orgânica e emotiva"
            metatags = {
                "intro": ["[70 BPM - Contemplative Worship Tempo]", "[Acoustic Guitar & Piano Intro]"],
                "verse1": "[Emotional Lead Vocal]\n[Intimate Acoustic Guitar & Piano]",
                "verse2": "[Warm Cello & Subtle Bass Enter]\n[Warm Vocal Harmony]",
                "prechorus": "[Percussive Swell]\n[Growing Devotion]",
                "chorus": "[Heartfelt Chorus]\n[Passionate Lead Vocals, Full Worship Ensemble & Choir]",
                "bridge": "[Spiritual Climax Bridge]\n[Soaring Strings & Full Band]",
                "outro": "[Soft Piano Outro]\n[Reverent Fade Out]"
            }

        ref_short = biblical_reference.split("(")[0].strip() if biblical_reference else "a Palavra de Deus"
        rationale = (
            f"O Produtor Musical analisou o tema '{theme}' e a passagem {ref_short}. "
            f"Projetou uma identidade sonora autônoma: '{arrangement_name}', "
            f"alinhavando instrumentos e dinâmica à mensagem bíblica."
        )

        result = {
            "arrangement_name": arrangement_name,
            "style_of_music": build_complete_suno_style(style_of_music, vocal_preference, tempo_dynamics),
            "vocal_preference": vocal_preference,
            "tempo_dynamics": tempo_dynamics,
            "producer_rationale": rationale,
            "metatags": metatags
        }
        self._last_arrangement = result
        return result

    def run(self, draft: SongDraft, dossier: TheologicalDossier, briefing: UserBriefing) -> SunoSongPackage:
        self._last_draft = draft
        self._last_dossier = dossier
        self._last_briefing = briefing

        arr = self.design_arrangement_from_reflection(
            theme=briefing.theme,
            biblical_reference=briefing.biblical_reference,
            biblical_reflection=dossier.exegetical_summary,
            exclude_style=briefing.musical_style_hint
        )

        hint_clean = (briefing.musical_style_hint or "").strip()
        if not hint_clean or hint_clean.lower().startswith("auto"):
            briefing.vocal_preference = arr["vocal_preference"]
            briefing.tempo_hint = arr["tempo_dynamics"]
            briefing.musical_style_hint = arr["style_of_music"]
        else:
            briefing.musical_style_hint = build_complete_suno_style(
                hint_clean,
                briefing.vocal_preference,
                briefing.tempo_hint
            )

        pkg = self._generate_contextual_demonstration("", SunoSongPackage)
        pkg.style_of_music = build_complete_suno_style(
            pkg.style_of_music or briefing.musical_style_hint,
            briefing.vocal_preference,
            briefing.tempo_hint
        )
        return pkg

    def _generate_contextual_demonstration(self, user_prompt: str, response_model: Type[BaseModel]) -> SunoSongPackage:
        draft = self._last_draft
        dossier = self._last_dossier
        briefing = self._last_briefing
        arr = self._last_arrangement or {}

        bpm = (
            briefing.tempo_hint.strip()
            if (briefing and briefing.tempo_hint)
            else arr.get("tempo_dynamics", "70 BPM")
        )
        vocal_guidance = (
            briefing.vocal_preference.strip()
            if (briefing and briefing.vocal_preference)
            else arr.get("vocal_preference", "Voz emotiva e sincera")
        )
        raw_style = (
            briefing.musical_style_hint.strip()
            if (briefing and briefing.musical_style_hint and not briefing.musical_style_hint.lower().startswith("auto"))
            else arr.get("style_of_music", "intimate acoustic worship, piano, 70 BPM")
        )
        style_prompt = build_complete_suno_style(raw_style, vocal_guidance, bpm)

        meta = arr.get("metatags", {
            "intro": ["[Atmospheric Instrumental Intro]"],
            "verse1": "[Intimate Lead Vocal]\n[Soft Acoustic Accompaniment]",
            "verse2": "[Subtle Strings Enter]\n[Warm Vocal Harmony]",
            "prechorus": "[Dynamic Swell]\n[Rising Emotion]",
            "chorus": "[Congregational Chorus]\n[Full Band & Choir Harmony]",
            "bridge": "[Climactic Bridge]\n[Passionate Vocal Declaration]",
            "outro": "[Gentle Instrumental Fade]\n[Reverent Silence]"
        })

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
            song_title = "Cântico de Adoração ao Senhor"
            lyrics_with_metatags = "[Intro]\n\n[Verse 1]\nDiante do Teu amor nos prostramos...\n\n[Outro]\n[Fade out]\n[End]"

        theo_summary = (
            dossier.exegetical_summary
            if (dossier and dossier.exegetical_summary)
            else "Composição cristocêntrica fundamentada nas Escrituras Sagradas para adoração a Deus."
        )

        return SunoSongPackage(
            song_title=song_title,
            style_of_music=style_prompt,
            lyrics_with_metatags=lyrics_with_metatags,
            target_bpm=bpm,
            vocal_configuration=vocal_guidance,
            theological_summary=theo_summary,
            suno_tips=[
                f"Arranjo Musical Gerado: {arr.get('arrangement_name', 'Worship Personalizado')}",
                f"Voz Incluída no Style: {vocal_guidance}",
                f"BPM e Dinâmica Incluídos no Style: {bpm}",
                "No Suno AI, ative o modo 'Custom' e cole os blocos 'Style of Music' e 'Lyrics'."
            ]
        )
