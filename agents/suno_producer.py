"""
Agente 4: Diretor Musical & Engenheiro de Prompt do Suno AI.
Responsável por analisar o Tema e a Reflexão Bíblica gerada pelo Agente Teólogo e criar
dinamicamente o Estilo Musical (já com Instrumentos + Voz + BPM + Dinâmica integrados),
Preferência Vocal, Andamento/Dinâmica e Metatags do Suno AI.
"""

import re
import random
import unicodedata
from typing import Optional, Type
from pydantic import BaseModel
from .base import BaseAgent
from schemas import SongDraft, TheologicalDossier, UserBriefing, SunoSongPackage


SUNO_PRODUCER_SYSTEM_PROMPT = """Você é um Produtor Musical Especialista no motor de geração de áudio do Suno AI (v3.5, v4 e v4.5).
Sua missão é criar a identidade sonora, arranjo, voz, andamento (BPM) e metatags para a canção com base no Tema e na Reflexão Bíblica do Agente Teólogo.

REGRAS DE ENGENHARIA PARA O SUNO AI:
1. CAMPO 'STYLE OF MUSIC' (ATÉ 180 CARACTERES):
   - DEVE obrigatoriamente conter: [Gênero/Subgênero], [Instrumentos Chave], [Tipo de Voz/Coral], [BPM Exato] e [Dinâmica de Produção].
   - Exemplo: intimate acoustic worship, fingerpicked guitar, warm cello, soft piano, tender female lead vocals, vocal harmony, 66 BPM, slow emotional build
2. CAMPO 'LYRICS' E METATAGS ENTRE COLCHETES:
   - O Suno utiliza colchetes como metatags de controle instrumental e arranjo.
   - Intercale tags estruturais e de dinâmica alinhadas aos instrumentos, voz e BPM escolhidos.
"""


def _norm(text: str) -> str:
    nfkd = unicodedata.normalize("NFKD", (text or "").lower().strip())
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def build_complete_suno_style(base_style: str, vocal_pref: str = "", tempo_pref: str = "") -> str:
    """
    Garante que o campo 'style_of_music' SEMPRE contenha:
    Estilo + Instrumentos + Voz (Vocal) + BPM + Dinâmica de acordo com a geração.
    """
    style_clean = (base_style or "").strip().rstrip(",")
    if style_clean.lower().startswith("auto:"):
        style_clean = style_clean[5:].strip()

    s_low = style_clean.lower()
    v_low = _norm(vocal_pref)
    t_low = _norm(tempo_pref)

    # 1. Garante presença da Voz (Vocal) no Style of Music
    has_vocal_in_style = any(
        w in s_low for w in ["vocal", "voice", "lead", "duet", "choir", "tenor", "soprano", "baritone", "singer"]
    )
    if not has_vocal_in_style:
        if "dueto" in v_low or "masculino e feminino" in v_low:
            vocal_tag = "male and female vocal duet, rich choir harmony"
        elif "feminina" in v_low and "soul" in v_low:
            vocal_tag = "soulful female lead vocals, full gospel choir"
        elif "feminina" in v_low:
            vocal_tag = "anointed female lead vocals, warm backing choir"
        elif "coral" in v_low and ("4 vozes" in v_low or "sacro" in v_low or "polifonico" in v_low):
            vocal_tag = "powerful lead vocal, 4-part sacred choir harmony"
        elif "masculina" in v_low:
            vocal_tag = "emotional male lead vocals, congregational choir"
        else:
            vocal_tag = "passionate lead vocals, congregational choir"
        style_clean = f"{style_clean}, {vocal_tag}" if style_clean else vocal_tag

    # 2. Garante presença do BPM exato e Dinâmica no Style of Music
    has_bpm_in_style = bool(re.search(r"\b\d{2,3}\s*bpm\b", style_clean, re.IGNORECASE))
    if not has_bpm_in_style:
        bpm_match = re.search(r"(\d{2,3})\s*(?:-\s*\d{2,3})?\s*bpm", tempo_pref or "", re.IGNORECASE)
        if bpm_match:
            bpm_tag = f"{bpm_match.group(1)} BPM"
        elif any(w in t_low for w in ["rapido", "vibrante", "festa", "jubilo", "120"]):
            bpm_tag = "120 BPM"
        elif any(w in t_low for w in ["medio", "alegre", "celebr", "100", "106"]):
            bpm_tag = "104 BPM"
        elif any(w in t_low for w in ["moderado", "78", "80", "82", "85"]):
            bpm_tag = "78 BPM"
        elif any(w in t_low for w in ["calmo", "paz", "consolo", "rubato", "64", "66"]):
            bpm_tag = "66 BPM"
        else:
            bpm_tag = "70 BPM"

        # Dinâmica
        if any(w in s_low for w in ["build", "climax", "crescendo", "upbeat", "groove", "peaceful"]):
            style_clean = f"{style_clean}, {bpm_tag}"
        else:
            if any(w in t_low for w in ["alegre", "vibrante", "festa", "jubilo"]):
                dyn_tag = "upbeat celebratory groove"
            elif any(w in t_low for w in ["calmo", "paz", "intima", "descanso"]):
                dyn_tag = "intimate peaceful dynamics"
            else:
                dyn_tag = "slow build to epic climax"
            style_clean = f"{style_clean}, {bpm_tag}, {dyn_tag}"

    return style_clean[:190]


# Banco inteligente de Arranjos Musicais por Atmosfera Teológica / Reflexão Bíblica
# Todos os 'style_of_music' já incluem: [Estilo + Instrumentos + Voz + BPM + Dinâmica]
THEMATIC_ARRANGEMENTS = {
    "amor_intimo": [
        {
            "arrangement_name": "Acústico Devocional Intimista (Violão, Violoncelo, Voz Feminina • 66 BPM)",
            "style_of_music": "intimate acoustic worship, fingerpicked guitar, warm cello, soft piano, tender female lead vocals, vocal harmony, 66 BPM, slow emotional build",
            "vocal_preference": "Voz feminina suave e intimista nos versos, abrindo com harmonia vocal no refrão",
            "tempo_dynamics": "Lento devocional (66 BPM) começando em voz e violão e crescendo com violoncelo",
            "metatags": {
                "intro": ["[66 BPM - Slow Devotional Tempo]", "[Fingerpicked Acoustic Guitar & Warm Cello Intro]"],
                "verse1": "[Tender Female Lead Vocals]\n[Intimate Acoustic Guitar]",
                "verse2": "[Soft Piano & Cello Enter]\n[Warm Vocal Harmony]",
                "prechorus": "[Subtle Percussive Swell]\n[Growing Emotion]",
                "chorus": "[Emotional Chorus]\n[Soaring Female Lead, Acoustic Band & Backing Choir]",
                "bridge": "[Spontaneous Devotional Climax]\n[Passionate Female Lead & Lush Strings]",
                "outro": "[Gentle Acoustic Guitar Outro]\n[Whispered Female Vocal Prayer]"
            }
        },
        {
            "arrangement_name": "Adoração Profética Soaking (Piano Rhodes, Pads, Dueto Vocal • 68 BPM)",
            "style_of_music": "prophetic worship ballad, warm rhodes piano, ambient synth pads, male and female vocal duet, lush strings, 68 BPM, slow atmospheric crescendo",
            "vocal_preference": "Dueto vocal (masculino e feminino) em harmonia apaixonada e suave",
            "tempo_dynamics": "Fluido e contemplativo (68 BPM) com atmosfera envolvente e refrão intenso",
            "metatags": {
                "intro": ["[68 BPM - Contemplative Worship Tempo]", "[Warm Rhodes Piano & Ethereal Synth Pad Intro]"],
                "verse1": "[Gentle Male Lead Vocal]\n[Soft Rhodes & Ambient Pad]",
                "verse2": "[Female Vocal Joins in Harmony Duet]\n[Deep Bass & Subtle Brush Drums]",
                "prechorus": "[Swelling Guitars]\n[Building Devotion]",
                "chorus": "[Passionate Male & Female Vocal Duet]\n[Full Worship Band & Lush Strings]",
                "bridge": "[Climactic Prophetic Worship]\n[Soaring Duet Harmonies & Delayed Guitar]",
                "outro": "[Soft Piano & Ambient Pad Fade]\n[Intimate Duet Ending]"
            }
        },
        {
            "arrangement_name": "Modern Worship Congregacional (Grand Piano, Guitarras, Voz Masculina • 72 BPM)",
            "style_of_music": "modern congregational worship, grand piano, ambient electric guitars, emotional male lead vocals, full choir, 72 BPM, slow build to anthemic climax",
            "vocal_preference": "Voz masculina emotiva nos versos com coral congregacional forte no refrão",
            "tempo_dynamics": "Moderado solene (72 BPM) iniciando no piano e explodindo no refrão",
            "metatags": {
                "intro": ["[72 BPM - Solemn Worship Tempo]", "[Atmospheric Grand Piano & Swelling Guitar Intro]"],
                "verse1": "[Emotional Male Lead Vocal]\n[Grand Piano Only]",
                "verse2": "[Warm Bass & Soft Tom Drums]\n[Subtle Strings]",
                "prechorus": "[Drums Build Tension]\n[Rising Guitars]",
                "chorus": "[Anthemic Chorus]\n[Passionate Male Lead, Full Band & Congregational Choir]",
                "bridge": "[Explosive Worship Bridge]\n[Soaring Male Tenor & Full Choir]",
                "outro": "[Acoustic Piano Breakdown]\n[Reverent Fade Out]"
            }
        }
    ],
    "amor_agape_cruz": [
        {
            "arrangement_name": "Gospel Soul & Coral Ágape (Piano, Hammond B3, Voz Feminina Soul • 70 BPM)",
            "style_of_music": "soulful gospel ballad, grand piano, warm hammond B3 organ, soulful female lead vocals, 3-part gospel choir, 70 BPM, emotional choir climax",
            "vocal_preference": "Voz feminina soulful potente com grande coral gospel harmônico respondendo",
            "tempo_dynamics": "Balada Soul cadenciada (70 BPM) com grande explosão coral no refrão e ponte",
            "metatags": {
                "intro": ["[70 BPM - Soulful Gospel Ballad]", "[Grand Piano & Warm Hammond B3 Organ Intro]"],
                "verse1": "[Soulful Female Lead Vocal]\n[Expressive Piano & Soft Organ]",
                "verse2": "[Groovy Gospel Bass & Rimshot Drums]\n[Soft Choir Harmonies]",
                "prechorus": "[Choir Harmony Swell]\n[Drum Fill Build]",
                "chorus": "[Powerful Gospel Chorus]\n[Soulful Female Lead & Full 3-Part Gospel Choir]",
                "bridge": "[Key Modulation Climax]\n[Passionate Female Vocal Runs & Choir Call-Response]",
                "outro": "[Gentle Piano & Hammond Chord]\n[Choir Amen]"
            }
        },
        {
            "arrangement_name": "Power Ballad da Cruz (Guitarras Limpas, Cordas, Dueto Emocional • 74 BPM)",
            "style_of_music": "christian power ballad, clean electric guitar, orchestral strings, male and female vocal duet, dramatic drums, 74 BPM, epic chorus climax",
            "vocal_preference": "Dueto masculino e feminino emotivo com coro sinfônico no clímax",
            "tempo_dynamics": "Moderado dramático (74 BPM) crescendo até solo de guitarra e clímax coral",
            "metatags": {
                "intro": ["[74 BPM - Dramatic Worship Ballad]", "[Clean Arpeggiated Guitar & Orchestral Cello Intro]"],
                "verse1": "[Warm Male Lead Vocal]\n[Clean Guitar & Piano]",
                "verse2": "[Female Lead Vocal Joins in Duet]\n[Steady Drums & Strings]",
                "prechorus": "[Crescendo]\n[Timpani & Snare Build]",
                "chorus": "[Epic Worship Chorus]\n[Soaring Male & Female Duet, Full Choir & Electric Guitars]",
                "bridge": "[Emotional Guitar Solo & Bridge]\n[Full Symphony & Congregational Voices]",
                "outro": "[Soft Piano & Solo Violin]\n[Fade Out]"
            }
        },
        {
            "arrangement_name": "Cinematic Worship Redenção (Piano de Cauda, Violoncelo, Voz Masculina • 68 BPM)",
            "style_of_music": "cinematic worship anthem, grand piano, solo cello, passionate male lead vocals, celestial choir, 68 BPM, slow majestic build",
            "vocal_preference": "Voz masculina grave e apaixonada com coro celestial no refrão",
            "tempo_dynamics": "Lento majestoso (68 BPM) evoluindo de intimista para épico cinematográfico",
            "metatags": {
                "intro": ["[68 BPM - Majestic Cinematic Tempo]", "[Solo Cello & Grand Piano Intro]"],
                "verse1": "[Deep Reverent Male Lead Vocal]\n[Soft Piano]",
                "verse2": "[Strings Section Enters]\n[Deep Heartbeat Drums]",
                "prechorus": "[Rising Brass & Strings]\n[Building Intensity]",
                "chorus": "[Majestic Anthem Chorus]\n[Passionate Male Lead, Full Orchestra & Celestial Choir]",
                "bridge": "[Thunderous Drums & Choir Climax]\n[Soaring Male Tenor High Notes]",
                "outro": "[Quiet Grand Piano Outro]\n[Peaceful Resolution]"
            }
        }
    ],
    "santidade_trono": [
        {
            "arrangement_name": "Épico Sinfônico do Trono (Orquestra, Timpani, Harpa, Coral Sacro • 68 BPM)",
            "style_of_music": "cinematic orchestral worship, symphony strings, brass swell, timpani, powerful lead vocal, 4-part sacred choir, 68 BPM, majestic throne room climax",
            "vocal_preference": "Solista imponente com Coral Sacro Polifônico (Soprano, Contralto, Tenor, Baixo)",
            "tempo_dynamics": "Solene e grandioso (68 BPM) com dinâmica de sala do trono celestial",
            "metatags": {
                "intro": ["[68 BPM - Solemn Throne Room Tempo]", "[Celestial Harp, Symphony Strings & Angelic Choir Intro]"],
                "verse1": "[Reverent Solo Lead Vocal]\n[Grand Piano & Soft Strings]",
                "verse2": "[French Horns & Cello Countermelody]\n[Timpani Roll]",
                "prechorus": "[Orchestral Crescendo]\n[Choir Voices Rising]",
                "chorus": "[Majestic Throne Room Chorus]\n[Full Symphony Orchestra & 4-Part Sacred Choir]",
                "bridge": "[Holy Holy Holy Climax]\n[Brass Fanfare, Timpani & Thunderous Choir]",
                "outro": "[Ethereal Choir & Harp Fade]\n[Sacred Silence]"
            }
        },
        {
            "arrangement_name": "Arena Worship Solene (Piano, Guitarras Shimmer, Voz Feminina & Coral • 72 BPM)",
            "style_of_music": "modern arena worship, grand piano, shimmer reverb guitars, soaring female lead vocals, massive congregational choir, 72 BPM, slow build to epic climax",
            "vocal_preference": "Voz feminina potente e ungida com milhares de vozes congregacionais no refrão",
            "tempo_dynamics": "Moderado solene (72 BPM) com paredes de guitarra atmosférica e grande clímax",
            "metatags": {
                "intro": ["[72 BPM - Arena Worship Tempo]", "[Shimmer Guitar & Grand Piano Intro]"],
                "verse1": "[Clear Anointed Female Lead Vocal]\n[Sparse Piano & Ambient Pad]",
                "verse2": "[Tom-Heavy Worship Drums]\n[Delayed Electric Guitar]",
                "prechorus": "[Rising Synth & Snare Build]\n[Congregation Singing Along]",
                "chorus": "[Massive Arena Worship Chorus]\n[Soaring Female Lead & Huge Congregational Choir]",
                "bridge": "[Explosive Worship Bridge]\n[Full Band Wall of Sound & Female Vocal Ad-libs]",
                "outro": "[Gentle Piano & Ambient Reverb]\n[Fade Out]"
            }
        }
    ],
    "avivamento_fogo": [
        {
            "arrangement_name": "Pentecostal de Avivamento & Impacto (Banda Completa, Metais, Voz Potente • 84 BPM)",
            "style_of_music": "pentecostal revival worship, driving drums, electric guitar, piano, brass section, powerhouse lead vocals, passionate choir, 84 BPM, intense revival build",
            "vocal_preference": "Voz líder explosiva e pentecostal com coral vibrante em clamor",
            "tempo_dynamics": "Crescente e intenso (84 BPM) com bateria marcada e explosão de avivamento",
            "metatags": {
                "intro": ["[84 BPM - Revival Worship Tempo]", "[Dramatic Piano, Electric Guitar & Driving Drum Fill Intro]"],
                "verse1": "[Passionate Revival Lead Vocal]\n[Piano & Bass Groove]",
                "verse2": "[Full Rhythm Section Enters]\n[Hammond Organ & Overdriven Guitar]",
                "prechorus": "[Snare Roll Crescendo]\n[Choir Voices Rising in Power]",
                "chorus": "[Explosive Revival Chorus]\n[Powerhouse Lead Vocal, Brass & Full Choir]",
                "bridge": "[Pentecostal Fire Bridge]\n[Intense Band Jam & Spontaneous Choir Cry]",
                "outro": "[Final Climactic Chord]\n[Worship Applause & Piano Fade]"
            }
        },
        {
            "arrangement_name": "Rock Worship de Batalha & Vitória (Guitarras, Bateria Forte, Voz Masculina • 98 BPM)",
            "style_of_music": "christian rock worship, driving electric guitars, punchy rock drums, strong male lead vocals, anthemic backing choir, 98 BPM, high energy",
            "vocal_preference": "Voz masculina firme e vibrante com backing vocals em uníssono no refrão",
            "tempo_dynamics": "Energético e firme (98 BPM) com pulsação constante de guitarra e bateria",
            "metatags": {
                "intro": ["[98 BPM - Driving Rock Worship Tempo]", "[Anthemic Electric Guitar Riff & Rock Drums Intro]"],
                "verse1": "[Strong Male Lead Vocal]\n[Palm-Muted Guitar & Bass]",
                "verse2": "[Rhythm Guitars Open Up]\n[Energetic Drum Beat]",
                "prechorus": "[Building Guitar Octaves]\n[Crescendo]",
                "chorus": "[High-Energy Anthemic Chorus]\n[Strong Male Lead, Distorted Guitars & Backing Choir]",
                "bridge": "[Epic Guitar Solo & Worship Cry]\n[Half-Time Heavy Groove]",
                "outro": "[Final Anthemic Riff]\n[Strong Ending]"
            }
        }
    ],
    "celebracao_jubilo": [
        {
            "arrangement_name": "Praise & Celebração Congregacional Alegre (Pop Gospel, Metais, Coral • 118 BPM)",
            "style_of_music": "upbeat gospel praise, joyful brass section, funky bassline, rhythmic piano, energetic lead vocals, celebratory choir, 118 BPM, joyful party groove",
            "vocal_preference": "Líder alegre e contagiante com coral de celebração e palmas no refrão",
            "tempo_dynamics": "Rápido e festivo (118 BPM) em clima de gratidão, festa e júbilo",
            "metatags": {
                "intro": ["[118 BPM - Upbeat Praise Tempo]", "[Joyful Brass, Rhythmic Piano & Funky Bass Intro]"],
                "verse1": "[Joyful Energetic Lead Vocal]\n[Upbeat Piano & Tight Drums]",
                "verse2": "[Choir Call and Response]\n[Rhythm Guitar & Horn Stabs]",
                "prechorus": "[Handclaps & Drum Build]\n[Rising Excitement]",
                "chorus": "[Celebratory Praise Chorus]\n[Energetic Lead, Full Gospel Choir & Brass Groove]",
                "bridge": "[Joyful Dance & Praise Breakdown]\n[Bass Solo & Choir Vamp]",
                "outro": "[Big Finale Brass Hit]\n[Joyful Ending]"
            }
        },
        {
            "arrangement_name": "Pop Worship Acústico Alegre (Violão Aço, Percussão, Dueto Alegre • 106 BPM)",
            "style_of_music": "upbeat acoustic pop worship, bright steel guitar, rhythmic percussion, warm bass, joyful male and female vocal duet, youth choir, 106 BPM, uplifting groove",
            "vocal_preference": "Dueto masculino e feminino alegre e luminoso com coro jovem",
            "tempo_dynamics": "Médio alegre (106 BPM) com violão rítmico e batida contagiante",
            "metatags": {
                "intro": ["[106 BPM - Uplifting Acoustic Pop Tempo]", "[Bright Steel Guitar & Percussion Intro]"],
                "verse1": "[Warm Joyful Male Lead Vocal]\n[Strummed Acoustic Guitar & Cajon]",
                "verse2": "[Bright Female Lead Joins in Duet]\n[Full Drums & Bass Groove]",
                "prechorus": "[Rhythmic Claps & Vocal Oohs]\n[Building Joy]",
                "chorus": "[Uplifting Pop Worship Chorus]\n[Joyful Male & Female Duet with Youth Choir]",
                "bridge": "[Acoustic Breakdown & Singalong]\n[Everyone Singing Together]",
                "outro": "[Upbeat Acoustic Strumming Outro]\n[Clean End]"
            }
        }
    ],
    "paz_refugio_cura": [
        {
            "arrangement_name": "Piano Neoclássico & Cordas de Consolo (Piano Solo, Violino, Voz Feminina • 64 BPM)",
            "style_of_music": "neoclassical devotional worship, solo grand piano, expressive violin, warm strings, soothing female lead vocals, angelic choir, 64 BPM, peaceful healing dynamics",
            "vocal_preference": "Voz feminina doce, serena e consoladora com cordas suaves ao fundo",
            "tempo_dynamics": "Calmo e restaurador (64 BPM) transmitindo paz profunda e descanso na alma",
            "metatags": {
                "intro": ["[64 BPM - Peaceful Restorative Tempo]", "[Gentle Neoclassical Piano & Solo Violin Intro]"],
                "verse1": "[Soothing Female Lead Vocal]\n[Delicate Grand Piano]",
                "verse2": "[Warm String Quartet Enters]\n[Soft Acoustic Guitar]",
                "prechorus": "[Swelling Strings]\n[Hopeful Crescendo]",
                "chorus": "[Peaceful Worship Chorus]\n[Clear Female Lead, Lush Strings & Soft Angelic Choir]",
                "bridge": "[Moment of Healing & Peace]\n[Piano Arpeggios & Soaring Female Harmony]",
                "outro": "[Solo Piano & Violin Fade]\n[Peaceful Silence]"
            }
        },
        {
            "arrangement_name": "Folk Worship de Esperança (Violão Dedilhado, Piano, Voz Masculina • 72 BPM)",
            "style_of_music": "indie folk worship, warm acoustic guitar, upright piano, cello, comforting male lead vocals, warm vocal harmonies, 72 BPM, hopeful crescendo",
            "vocal_preference": "Voz masculina acolhedora e serena nos versos, ganhando força de fé no refrão",
            "tempo_dynamics": "Moderado tranquilo (72 BPM) crescendo da lágrima para a certeza da vitória",
            "metatags": {
                "intro": ["[72 BPM - Gentle Folk Worship Tempo]", "[Warm Fingerpicked Guitar & Upright Piano Intro]"],
                "verse1": "[Comforting Male Lead Vocal]\n[Intimate Guitar & Piano]",
                "verse2": "[Brush Drums & Upright Bass]\n[Subtle Vocal Harmony]",
                "prechorus": "[Cello & Acoustic Strum Build]\n[Rising Hope]",
                "chorus": "[Hopeful Folk Worship Chorus]\n[Warm Male Lead, Full Acoustic Ensemble & Choir]",
                "bridge": "[Declaration of Faith Bridge]\n[Passionate Male Vocals & Soaring Strings]",
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
        configuração de Estilo Musical (já com Voz e BPM integrados), Preferência Vocal,
        Andamento/Dinâmica e Metatags, garantindo que mude a cada geração.
        """
        combined = _norm(f"{theme} {biblical_reference} {biblical_reflection}")

        if any(w in combined for w in ["primeiro amor", "amo-te", "madrugada", "sede", "intimidade", "meu amado", "coracao", "devocao"]):
            pool_key = "amor_intimo"
        elif any(w in combined for w in ["amor", "agape", "cruz", "sangue", "graca", "redencao", "perdao", "arrepend", "cordeiro"]):
            pool_key = "amor_agape_cruz"
        elif any(w in combined for w in ["saudade", "cidade", "celestial", "jerusalem", "patria", "peregrino", "morada"]):
            pool_key = random.choice(["santidade_trono", "paz_refugio_cura", "amor_intimo"])
        elif any(w in combined for w in ["santidade", "santo", "trono", "serafins", "majestade", "gloria", "rei", "exodo", "isaias 6", "apocalipse"]):
            pool_key = "santidade_trono"
        elif any(w in combined for w in ["espirito", "fogo", "avivamento", "pentecostes", "uncao", "vento", "poder", "guerra", "batalha"]):
            pool_key = "avivamento_fogo"
        elif any(w in combined for w in ["gratidao", "alegria", "jubilo", "celebr", "festa", "louvor", "acoes de gracas", "vitoria"]):
            pool_key = "celebracao_jubilo"
        elif any(w in combined for w in ["paz", "descanso", "refugio", "cura", "consolo", "lagrima", "medo", "ansiedade", "pastor", "salmo 23", "salmo 91", "salmo 121"]):
            pool_key = "paz_refugio_cura"
        else:
            pool_key = random.choice(list(THEMATIC_ARRANGEMENTS.keys()))

        candidates = list(THEMATIC_ARRANGEMENTS[pool_key])
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
            f"Para o tema '{theme}' e a reflexão em {ref_short}, o Agente Musical gerou o estilo completo com BPM e Voz: "
            f"'{chosen['arrangement_name']}'."
        )

        result = dict(chosen)
        result["style_of_music"] = build_complete_suno_style(
            chosen["style_of_music"],
            chosen["vocal_preference"],
            chosen["tempo_dynamics"]
        )
        result["producer_rationale"] = producer_rationale
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
            # Mesmo no modo manual, garante que o Style of Music incorpore a Voz e o BPM escolhidos!
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
        arr = self._last_arrangement or THEMATIC_ARRANGEMENTS["amor_intimo"][0]

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
        raw_style = (
            briefing.musical_style_hint.strip()
            if (briefing and briefing.musical_style_hint and not briefing.musical_style_hint.lower().startswith("auto"))
            else arr["style_of_music"]
        )
        style_prompt = build_complete_suno_style(raw_style, vocal_guidance, bpm)

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
