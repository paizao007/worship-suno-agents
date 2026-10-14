"""
Agente 2: Poeta & Compositor Sacro (100% Dinâmico & Anti-Repetição).
Transforma o Dossier Teológico (Tema, Versículo Canônico, Reflexão e Atributos de Deus)
em poesia litúrgica viva, profunda, inspirada pelo Espírito Santo e sem categorias engessadas.
Métrica regular, prosódia fluida para canto em português e metatags estruturais claras.
"""

import json
import os
import random
from typing import Optional, Type
from pydantic import BaseModel
from .base import BaseAgent
from schemas import TheologicalDossier, SongDraft, LyricSection, AuditReport


LYRICIST_SYSTEM_PROMPT = """Você é um Compositor e Poeta Sacro Cristão inspirado por Deus, de profunda sensibilidade bíblica e excelência poética (Worship Congregacional / Hinologia Contemporânea).
Sua missão é criar uma canção de adoração 100% INÉDITA, ORIGINAL E PROFUNDA a partir do Tema, do Versículo Bíblico e da Reflexão Bíblica fornecidos pelo Teólogo.

DIRETRIZES INEGOCIÁVEIS DE CRIAÇÃO POÉTICA:
1. ORIGINALIDADE ABSOLUTA (ZERO CLICHÊS):
   - Cada música deve nascer do coração e das imagens do VERSÍCULO BÍBLICO e do TEMA DO USUÁRIO.
   - NUNCA repita versos ou fórmulas prontas.
2. SINTONIA TEOLÓGICA E EMOCIONAL:
   - Se o tema for infantil/pureza/singeleza (tornar-se como criança, Salmo 131, Mateus 18): use vocabulário terno, descanso nos braços do Pai, simplicidade da fé, pureza e humildade.
   - Se o tema for a Cruz e Graça: use imagens de redenção, amor imerecido, preço pago e perdão eterno.
   - Se o tema for a Soberania e Santidade: use imagens de majestade, fogo consumidor, altares e reverência solene.
3. PROSÓDIA E CANTABILIDADE EM PORTUGUÊS (PARA SUNO AI):
   - Versos com cadência musical natural (7 a 11 sílabas poéticas), fáceis de respirar e cantar.
   - Rimas ricas e sonoras (consoantes e toantes suaves).
4. ARQUITETURA LITÚRGICA COMPLETA (6 SEÇÕES OBRIGATÓRIAS):
   - "Verse 1", "Verse 2", "Pre-Chorus", "Chorus", "Bridge", "Outro".
"""

SONG_DRAFT_JSON_EXAMPLE = """{
  "title": "Título Poético Inédito (Referência Bíblica)",
  "meter_notes": "Compasso 4/4 fluido, cadência adoradora inspirada no versículo base com subida emocional no refrão.",
  "rhyme_scheme": "Esquema AABB / ABAB com rimas sonoras e naturais para canto em português.",
  "sections": [
    {
      "tag": "Verse 1",
      "liturgical_purpose": "Estabelecer a atmosfera devocional do versículo sorteado",
      "lines": [
        "Primeiro verso poético inédito inspirado na passagem",
        "Segundo verso rimando com cadência suave",
        "Terceiro verso aprofundando a imagem bíblica",
        "Quarto verso preparando o coração diante de Deus"
      ]
    },
    {
      "tag": "Verse 2",
      "liturgical_purpose": "Aprofundar a reflexão teológica e a entrega",
      "lines": [
        "Primeiro verso da segunda estrofe com novas imagens",
        "Segundo verso exaltando a fidelidade do Senhor",
        "Terceiro verso conectando a cruz de Cristo ao tema",
        "Quarto verso elevando a esperança da alma"
      ]
    },
    {
      "tag": "Pre-Chorus",
      "liturgical_purpose": "Construir tensão ascendente para o refrão",
      "lines": [
        "Verso de transição que cresce em intensidade",
        "Preparando o clamor congregacional diante do Rei"
      ]
    },
    {
      "tag": "Chorus",
      "liturgical_purpose": "Doxologia central e refrão congregacional",
      "lines": [
        "Primeiro verso forte e memorável do refrão",
        "Segundo verso proclamando a glória de Jesus",
        "Terceiro verso celebrando a promessa da Escritura",
        "Quarto verso de entrega total e adoração eterna"
      ]
    },
    {
      "tag": "Bridge",
      "liturgical_purpose": "Clímax espiritual e declaração profética",
      "lines": [
        "Primeiro verso intenso da ponte de clímax",
        "Segundo verso de clamor e quebrantamento",
        "Terceiro verso exaltando o Cordeiro Vencedor",
        "Quarto verso culminando na vitória eterna em Cristo"
      ]
    },
    {
      "tag": "Outro",
      "liturgical_purpose": "Resolução serena e selo bíblico",
      "lines": [
        "Sussurro final de adoração fundamentado na Palavra",
        "Declaração de amor eterno a Jesus. Amém."
      ]
    }
  ]
}"""


class LyricistAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Poeta & Compositor Sacro",
            role="Mestre de Prosódia, Métrica e Poética Hinológica",
            system_prompt=LYRICIST_SYSTEM_PROMPT,
        )
        self._last_dossier: Optional[TheologicalDossier] = None
        self._last_theme_raw: str = ""
        self._used_base_titles: set[str] = set()
        self._used_lines: set[str] = set()

    def _load_history_memory(self) -> tuple[set[str], set[str]]:
        """Carrega títulos base e versos já usados em historico_musicas.json."""
        base_titles = set(self._used_base_titles)
        used_lines = set(self._used_lines)
        try:
            hist_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "historico_musicas.json",
            )
            if os.path.exists(hist_path):
                with open(hist_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, list):
                    for item in data[:40]:
                        t = (item.get("song_title") or item.get("title") or "").strip()
                        if t:
                            base_t = t.split("(")[0].strip().lower()
                            base_titles.add(base_t)
                        raw_lyrics = item.get("lyrics_with_metatags") or item.get("lyrics") or ""
                        for line in raw_lyrics.splitlines():
                            line_clean = line.strip().lower()
                            if line_clean and not line_clean.startswith("[") and len(line_clean) > 8:
                                used_lines.add(line_clean)
        except Exception:
            pass
        return base_titles, used_lines

    def _pick_unused_couplet(self, pool: list[list[str]], used_lines: set[str]) -> list[str]:
        scored = []
        for pair in pool:
            overlap = sum(1 for line in pair if line.strip().lower() in used_lines)
            scored.append((overlap, pair))
        scored.sort(key=lambda x: x[0])
        min_overlap = scored[0][0]
        best_candidates = [pair for overlap, pair in scored if overlap == min_overlap]
        chosen = random.choice(best_candidates)
        for line in chosen:
            self._used_lines.add(line.strip().lower())
            used_lines.add(line.strip().lower())
        return chosen

    def _pick_unused_section(self, pool: list[list[str]], used_lines: set[str]) -> list[str]:
        scored = []
        for sec in pool:
            overlap = sum(1 for line in sec if line.strip().lower() in used_lines)
            scored.append((overlap, sec))
        scored.sort(key=lambda x: x[0])
        min_overlap = scored[0][0]
        best_candidates = [sec for overlap, sec in scored if overlap == min_overlap]
        chosen = random.choice(best_candidates)
        for line in chosen:
            self._used_lines.add(line.strip().lower())
            used_lines.add(line.strip().lower())
        return chosen

    def _pick_unused_title(self, base_candidates: list[str], scripture_ref: str, used_base_titles: set[str]) -> str:
        fresh = [t for t in base_candidates if t.strip().lower() not in used_base_titles]
        chosen_base = random.choice(fresh if fresh else base_candidates)
        self._used_base_titles.add(chosen_base.strip().lower())
        used_base_titles.add(chosen_base.strip().lower())
        return f"{chosen_base} ({scripture_ref})"

    def run(self, dossier: TheologicalDossier, audit_feedback: Optional[AuditReport] = None) -> SongDraft:
        self._last_dossier = dossier
        used_base_titles, _ = self._load_history_memory()
        avoid_str = ", ".join(f'"{t}"' for t in list(used_base_titles)[:12]) if used_base_titles else "Nenhum"

        feedback_instructions = ""
        if audit_feedback and audit_feedback.actionable_revisions:
            revisoes = "\n- ".join(audit_feedback.actionable_revisions)
            feedback_instructions = f"""
ATENÇÃO: A versão anterior recebeu nota {audit_feedback.score}/10 e requer correções:
- {revisoes}
Reescreva a canção refinando esses pontos!
"""

        main_scripture = dossier.primary_scriptures[0] if dossier.primary_scriptures else "Escrituras Sagradas"
        scripture_ref = main_scripture.split(" (")[0].strip()

        prompt = f"""Componha uma canção de adoração cristã 100% INÉDITA, ORIGINAL e inspirada pelo Espírito Santo para este Dossier Teológico:

- TEMA E DOUTRINA CENTRAL: {dossier.theme_title}
- VERSÍCULO BÍBLICO PRINCIPAL (BASE DA LETRA): {main_scripture}
- PASSAGENS COMPLEMENTARES: {', '.join(dossier.primary_scriptures[1:])}
- REFLEXÃO BÍBLICA / EXEGESE: {dossier.exegetical_summary}
- ATRIBUTOS DE DEUS A EXALTAR: {', '.join(dossier.divine_attributes)}
- FOCO CRISTOCÊNTRICO: {dossier.christocentric_focus}
- EXPRESSÕES SAGRADAS SUGERIDAS: {', '.join(dossier.sacred_keywords)}
- TOM ESPIRITUAL E EMOCIONAL: {dossier.emotional_and_spiritual_tone}
- TÍTULOS PROIBIDOS (NÃO REPETIR): {avoid_str}

DIRETRIZES DA COMPOSIÇÃO:
1. O título da música DEVE ser poético, inédito e terminar com a referência: `({scripture_ref})`.
2. Todos os versos de [Verse 1], [Verse 2], [Pre-Chorus], [Chorus], [Bridge] e [Outro] devem nascer diretamente do coração de `{main_scripture}` e do tema `{dossier.theme_title}`.
3. Se o tema for infantil/filial/humildade (como criança, colo do Pai), a poesia DEVE ser terna, pura e sincera, sem elementos belicosos ou triunfalismos fora de lugar.
{feedback_instructions}
"""
        draft = self.call_llm(prompt, SongDraft, custom_json_example=SONG_DRAFT_JSON_EXAMPLE)
        if scripture_ref and scripture_ref.lower() not in draft.title.lower():
            draft.title = f"{draft.title.strip()} ({scripture_ref})"
        self._used_base_titles.add(draft.title.split("(")[0].strip().lower())
        return draft

    def _generate_contextual_demonstration(self, user_prompt: str, response_model: Type[BaseModel]) -> SongDraft:
        """
        Síntese Poética Autônoma Dinâmica:
        Constrói a letra inspirada no versículo e na reflexão teológica sem categorias fixas.
        """
        used_base_titles, used_lines = self._load_history_memory()

        scripture_full = "Salmo 145:1-3 (Exaltar-Te-ei, ó Deus meu e Rei)"
        scripture_ref = "Salmo 145:1-3"
        verse_essence = "Exaltar-Te-ei, ó Deus meu e Rei"
        theme_title = "Adoração ao Senhor"
        sacred_words = ["Graça eterna", "Altar de adoração", "Fidelidade", "Luz divina"]
        attributes = ["Fiel e Santo", "Amor Eterno"]

        if self._last_dossier:
            theme_title = self._last_dossier.theme_title.split("—")[0].strip()
            if self._last_dossier.primary_scriptures:
                scripture_full = self._last_dossier.primary_scriptures[0]
                scripture_ref = scripture_full.split(" (")[0].strip()
                if "(" in scripture_full and ")" in scripture_full:
                    verse_essence = scripture_full.split("(", 1)[1].rsplit(")", 1)[0].strip()
            if self._last_dossier.sacred_keywords:
                sacred_words = list(self._last_dossier.sacred_keywords)
            if self._last_dossier.divine_attributes:
                attributes = list(self._last_dossier.divine_attributes)

        t_lower = f"{theme_title} {scripture_full} {self._last_dossier.exegetical_summary if self._last_dossier else ''}".lower()
        t_clean = theme_title.replace("—", "-").strip()
        word1 = sacred_words[0] if sacred_words else "Graça"
        attr1 = attributes[0] if attributes else "Santo"

        # Se for tema de infância / pureza / como criança / colo do Pai
        if any(w in t_lower for w in ["criança", "crianca", "pequeno", "pequenino", "humild", "singel", "colo", "desmamada", "filhinho"]):
            base_titles = [
                "Como Uma Criança nos Teus Braços",
                "No Colo do Meu Pai",
                "Coração Singelo e Puro",
                "O Menor no Teu Reino",
                "Alma Serena em Teus Braços",
                "Descanso Filial em Ti",
                "A Fé de Uma Criança",
                "Ensina-me a Ser Pequeno"
            ]
            v1_openings = [
                ["Despindo o orgulho e as glórias que o mundo me deu,", "Venho como um menino aos pés do Deus dos céus,"],
                ["Como a criança desmamada no colo a descansar,", "Fiz calar a minha alma para Te adorar,"],
                ["Jesus chamou os pequeninos com tanto amor e luz,", "O Teu Reino pertence a quem se curva à Tua cruz,"],
            ]
            v1_closings = [
                [f"Conforme a santa Palavra viva em {scripture_ref},", "Quem se faz bem pequeno encontra o Reino pela fé."],
                ["Nos Teus braços de amor descanso o coração,", "Encontrando a pureza da verdadeira adoração."],
            ]
            v2_openings = [
                ["Abba, Pai de bondade, seguro a Tua mão,", "Guia os meus passos com Tua santa direção,"],
                ["Cria em mim a pureza de um sincero coração,", "Longe da vaidade e de toda pretensão,"],
            ]
            v2_closings = [
                ["A maior grandeza é ser menor diante do Rei,", "Na Tua santa graça para sempre viverei."],
                ["Nos Teus braços paternos a alma encontra a paz,", "Tua doce presença é tudo o que me satisfaz."],
            ]
            pre_pool = [
                ["Aos sábios deste mundo a glória se escondeu,", "Mas aos pequeninos o Pai se revelou do céu:"],
                ["Ouvindo a doce voz do Salvador a me chamar:", "Deixai vir a Mim os pequeninos para amar:"],
            ]
            chorus_pool = [
                [
                    "Faze-me ser como uma criança, Pai de amor!",
                    "Simples na fé, dependente do Teu favor!",
                    "Não quero ser grande, só quero ser Teu,",
                    "Pois o menor na terra é o maior lá no céu!",
                ],
                [
                    "No Teu colo seguro, ó meu doce Jesus,",
                    "A minha alma descansa e caminha em Tua luz!",
                    "Coração desprovido de orgulho e pesar,",
                    "Como uma criança eu vim Te adorar!",
                ]
            ]
            bridge_pool = [
                [
                    "Se eu não me converter e não me humilhar,",
                    "No Teu Reino de glória não poderei entrar!",
                    "Quebre a minha soberba, arranca a altivez,",
                    "Faz-me puro e singelo mais uma vez!",
                ],
                [
                    "Tu colocaste uma criança no centro do Teu olhar,",
                    "Para a todos nós a verdadeira fé ensinar:",
                    "A grandeza no Reino é servir e se prostrar,",
                    "E no colo do Pai para sempre confiar!",
                ]
            ]
            outro_closing = "Nos Teus braços de amor descanso... Como uma criança. Amém."

        # Para todos os demais temas bíblicos (Síntese Poética Dinâmica)
        else:
            base_titles = [
                f"{t_clean}",
                f"Diante do Teu Altar ({word1})",
                f"A Tua Glória Revelada",
                f"Descanso e Fé em Ti",
                f"Graça Soberana e Eterna",
                f"O Teu Santo Nome Exaltado",
                f"Coração em Adoração",
                f"Luz da Tua Presença",
            ]
            v1_openings = [
                ["Diante da Tua santa presença viemos nos prostrar,", "Para a grandeza do Teu nome celebrar e exaltar,"],
                ["A Tua santa Palavra ilumina o nosso caminhar,", "Trazendo viva esperança para a alma descansar,"],
                ["Em reverência e temor nos achegamos ao Teu altar,", "Pois não há outro Deus em quem possamos confiar,"],
            ]
            v1_closings = [
                [f"Conforme a verdade proclamada em {scripture_ref},", "O Teu povo fiel permanece firmado na fé."],
                ["Exaltamos a Tua glória manifesta com poder,", "Pois a Tua benignidade nos faz reviver."],
            ]
            v2_openings = [
                [f"Tu és {attr1}, maravilhoso em Teus santos caminhos,", "Guiando os Teus servos para não andarem sozinhos,"],
                ["A Tua fidelidade atravessa toda e qualquer geração,", "Derramando paz, consolo e graça sobre o coração,"],
                ["No sacrifício perfeito de Cristo encontramos salvação,", "E erguemos as nossas vozes em profunda gratidão,"],
            ]
            v2_closings = [
                ["A Tua glória e o Teu louvor jamais terão fim,", "Cumpra o Teu querer e a Tua vontade em mim."],
                ["Para sempre cantaremos a bondade do Senhor,", "Rendendo honra, majestade e o mais puro louvor."],
            ]
            pre_pool = [
                ["A criação inteira e a Igreja proclamam a uma só voz:", "O Senhor é digno de reinar eternamente sobre nós:"],
                ["Ergam-se os corações em santa consagração:", "Ao Deus Todo-Poderoso entregamos nossa adoração:"],
            ]
            chorus_pool = [
                [
                    f"Digno és Tu, Senhor, de receber glória e louvor!",
                    f"Proclamamos Teu poder e a riqueza do Teu amor!",
                    f"Exaltado seja o Teu nome, Autor de {word1.lower()},",
                    "A Ti nos prostramos em sincera adoração!",
                ],
                [
                    f"Grande é o Senhor, nosso {attr1} e Salvador!",
                    "Pelo sangue do Cordeiro fomos nós resgatados!",
                    f"Sustentados para sempre pelo Teu santo favor,",
                    "O Teu Reino de glória para sempre é exaltado!",
                ],
                [
                    "Santo, Santo, Santo é o Deus Todo-Poderoso!",
                    "O Teu amor é eterno, o Teu trono é glorioso!",
                    "Exaltado sobre a terra e os céus para sempre,",
                    "O Teu povo fiel aos Teus pés se rende!",
                ]
            ]
            bridge_pool = [
                [
                    f"Ecoa em nossa alma a verdade proclamada em {scripture_ref}:",
                    "A Tua Palavra jamais falhará, vivemos pela fé!",
                    "A Ti toda honra, império e majestade,",
                    "Desde agora e para sempre em toda a eternidade!",
                ],
                [
                    "Não a nós, Senhor, não a nós, mas ao Teu nome dai glória!",
                    "Pois em Cristo Jesus encontramos a vitória!",
                    "Quebrem-se os altares da humana presunção,",
                    "E reine a Tua soberania em cada coração!",
                ]
            ]
            outro_closing = "A Ti seja a glória, a honra e o louvor para sempre. Em Cristo Jesus. Amém."

        chosen_title = self._pick_unused_title(base_titles, scripture_ref, used_base_titles)
        v1_lines = self._pick_unused_couplet(v1_openings, used_lines) + self._pick_unused_couplet(v1_closings, used_lines)
        v2_lines = self._pick_unused_couplet(v2_openings, used_lines) + self._pick_unused_couplet(v2_closings, used_lines)
        pre_lines = self._pick_unused_couplet(pre_pool, used_lines)
        chorus_lines = self._pick_unused_section(chorus_pool, used_lines)
        bridge_lines = self._pick_unused_section(bridge_pool, used_lines)

        return SongDraft(
            title=chosen_title,
            meter_notes=f"Métrica poética original inspirada em {scripture_ref} ('{verse_essence}'), com cadência fluida para o Suno AI.",
            rhyme_scheme="Esquema AABB com rimas consoantes e toantes ricas.",
            sections=[
                LyricSection(
                    tag="Verse 1",
                    liturgical_purpose=f"Meditação poética direta em {scripture_ref}: {verse_essence}",
                    lines=v1_lines,
                ),
                LyricSection(
                    tag="Verse 2",
                    liturgical_purpose=f"Aprofundamento doutrinário em {theme_title}",
                    lines=v2_lines,
                ),
                LyricSection(
                    tag="Pre-Chorus",
                    liturgical_purpose="Subida melódica e preparação congregacional",
                    lines=pre_lines,
                ),
                LyricSection(
                    tag="Chorus",
                    liturgical_purpose="Doxologia central cristocêntrica",
                    lines=chorus_lines,
                ),
                LyricSection(
                    tag="Bridge",
                    liturgical_purpose="Clímax espiritual e entrega da Igreja",
                    lines=bridge_lines,
                ),
                LyricSection(
                    tag="Outro",
                    liturgical_purpose="Selo bíblico e consagração final",
                    lines=[
                        f"Palavra viva e eterna em {scripture_ref}:",
                        f"\"{verse_essence}\"",
                        outro_closing,
                    ],
                ),
            ],
        )
