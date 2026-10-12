"""
Agente 2: Poeta & Compositor Sacro.
Responsável por transformar o Dossier Teológico (Tema + Versículo + Reflexão Bíblica)
em poesia litúrgica 100% original e inédita, inspirada nas Escrituras Sagradas,
com métrica regular, prosódia fluida para canto em português e arquitetura estrófica clara.
Possui Memória Anti-Repetição de Histórico e Motor Combinatório de Dísticos Sacros.
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
1. ORIGINALIDADE ABSOLUTA (PROIBIDO REPETIR):
   - NUNCA repita letras, títulos ou estrofes já existentes no histórico.
   - Cada música deve nascer especificamente da imagem poética do VERSÍCULO SORTEADO e do TEMA DO USUÁRIO.
2. INSPIRAÇÃO BÍBLICA VIVA:
   - Transforme as palavras e metáforas do versículo bíblico principal em poesia cantável e emocionante.
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
        """
        Carrega todos os títulos base e versos já usados em historico_musicas.json
        para garantir que o agente JAMAIS repita títulos ou estrofes!
        """
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
                            base_titles.add(t.lower())
                        lyr = item.get("lyrics_with_metatags") or ""
                        for line in lyr.splitlines():
                            l_clean = line.strip()
                            if l_clean and not l_clean.startswith("["):
                                used_lines.add(l_clean.lower())
        except Exception:
            pass
        return base_titles, used_lines

    def _pick_unused_couplet(self, couplets: list[list[str]], used_lines: set[str]) -> list[str]:
        """Sorteia um dístico (par de versos rimados) que ainda não tenha sido usado no histórico."""
        fresh = [
            c for c in couplets
            if all(line.strip().lower() not in used_lines for line in c)
        ]
        chosen = random.choice(fresh if fresh else couplets)
        for line in chosen:
            self._used_lines.add(line.strip().lower())
            used_lines.add(line.strip().lower())
        return chosen

    def _pick_unused_title(self, base_candidates: list[str], scripture_ref: str, used_base_titles: set[str]) -> str:
        """Sorteia um título poético cujo nome base nunca tenha sido usado antes."""
        fresh = [
            t for t in base_candidates
            if t.strip().lower() not in used_base_titles
        ]
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

        prompt = f"""Componha uma canção de adoração cristã 100% INÉDITA, ORIGINAL e profundamente inspirada no Espírito Santo para este Dossier Teológico:

- TEMA E DOUTRINA CENTRAL: {dossier.theme_title}
- VERSÍCULO BÍBLICO PRINCIPAL (BASE OBRIGATÓRIA DA LETRA): {main_scripture}
- PASSAGENS COMPLEMENTARES: {', '.join(dossier.primary_scriptures[1:])}
- REFLEXÃO BÍBLICA / EXEGESE: {dossier.exegetical_summary}
- ATRIBUTOS DE DEUS A EXALTAR: {', '.join(dossier.divine_attributes)}
- FOCO CRISTOCÊNTRICO: {dossier.christocentric_focus}
- EXPRESSÕES SAGRADAS SUGERIDAS: {', '.join(dossier.sacred_keywords)}
- TOM ESPIRITUAL E EMOCIONAL: {dossier.emotional_and_spiritual_tone}
- TÍTULOS PROIBIDOS (NÃO REPETIR): {avoid_str}
- SEMENTE CRIATIVA: #{random.randint(10000, 99999)}

INSTRUÇÃO ESPECIAL:
1. O título da música DEVE ser poético, inédito e terminar com a referência entre parênteses: `({scripture_ref})`.
2. Os versos de [Verse 1], [Verse 2], [Pre-Chorus], [Chorus], [Bridge] e [Outro] devem refletir diretamente o tema e a meditação de `{main_scripture}`.
{feedback_instructions}
"""
        draft = self.call_llm(prompt, SongDraft, custom_json_example=SONG_DRAFT_JSON_EXAMPLE)
        if scripture_ref and scripture_ref.lower() not in draft.title.lower():
            draft.title = f"{draft.title.strip()} ({scripture_ref})"
        self._used_base_titles.add(draft.title.split("(")[0].strip().lower())
        return draft

    def _generate_contextual_demonstration(self, user_prompt: str, response_model: Type[BaseModel]) -> SongDraft:
        """
        Motor Poético Combinatório Sacro de Alta Criatividade:
        Constrói composições 100% inéditas combinando dísticos rimados independentes,
        a essência literal do versículo sorteado e a reflexão bíblica do tema,
        verificando o histórico para NUNCA repetir títulos ou estrofes.
        """
        used_base_titles, used_lines = self._load_history_memory()

        scripture_full = "Salmo 145:1-7 (Exaltar-Te-ei, ó Deus meu e Rei)"
        scripture_ref = "Salmo 145:1-7"
        verse_essence = "Exaltar-Te-ei, ó Deus meu e Rei"
        theme_title = "Adoração ao Senhor"
        sacred_words = ["Graça eterna", "Altar de luz", "Fidelidade", "Redentor"]
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

        t_lower = (theme_title + " " + scripture_full + " " + user_prompt).lower()

        # =========================================================================
        # FAMÍLIA 1: SAUDADE / CIDADE CELESTIAL / ETERNIDADE / MARANATA
        # =========================================================================
        if any(w in t_lower for w in [
            "saudade", "cidade", "celestial", "jerusalém", "jerusalem", "pátria", "patria",
            "maranata", "eternidade", "morada", "peregrino", "hebreus 11", "filipenses 3",
            "apocalipse 21", "apocalipse 22", "salmo 84", "tessalonicenses", "joão 14"
        ]):
            # Diferencia títulos e aberturas quando o foco é "saudade" vs "Cidade Celestial"
            if "saudade" in t_lower or "salmo 84" in t_lower:
                base_titles = [
                    "Santa Saudade do Teu Lar",
                    "Saudade dos Átrios do Rei",
                    "Lágrimas de Saudade pelo Céu",
                    "Suspiro de um Peregrino",
                    "Saudade da Tua Presença Eterna",
                    "Coração que Anseia pelo Céu",
                    "Quando a Saudade Encontrar o Rei",
                    "Alma que Suspira por Sião",
                ]
            else:
                base_titles = [
                    "Arquiteto da Cidade Celestial",
                    "Portais da Nova Jerusalém",
                    "Além do Rio de Cristal",
                    "Fundamentos da Pátria Celestial",
                    "Brilho da Cidade do Grande Rei",
                    "Moradas da Casa do Meu Pai",
                    "Ruas de Ouro e Luz Eterna",
                    "A Noiva Rumo à Cidade Santa",
                ]

            v1_openings = [
                ["Caminho neste mundo como quem vai voltar,", "Trago no peito a chama de um eterno lar,"],
                ["Minha alma tem saudade dos átrios do Senhor,", "Onde não há mais pranto, nem sombras, nem temor,"],
                ["Olhando para o horizonte além da escuridão,", "Ouço o chamado eterno da celestial Sião,"],
                ["Como estrangeiro e peregrino passo por aqui,", "Pois minha herança eterna está guardada em Ti,"],
                ["Quantas vezes na noite meu coração chorou,", "Lembrando da morada que Cristo preparou,"],
                ["Não pertenço às areias deste mundo fugaz,", "Busco a Cidade Santa onde reina a plena paz,"],
            ]
            v1_closings = [
                [f"Na promessa bendita escrita em {scripture_ref},", "Vejo a Cidade Eterna onde o Cordeiro é a luz."],
                ["Aguardo os fundamentos que o próprio Deus traçou,", "A Pátria Celestial que Jesus me preparou."],
                [f"Guardando na memória a luz de {scripture_ref},", "Cada passo na terra me aproxima de Jesus."],
                ["Onde os muros de jaspe refletem Teu esplendor,", "E a alma descansa nos braços do Redentor."],
            ]
            v2_openings = [
                ["As tendas desta terra não podem me prender,", "Pois lá nos altos céus está o meu viver,"],
                ["Cada lágrima caída o Pai enxugará,", "E a noite do deserto para sempre findará,"],
                ["Lá não haverá noite, nem lâmpada ou sol,", "Pois a glória de Cristo é o nosso farol,"],
                ["Da árvore da vida em breve vou provar,", "Junto ao rio cristalino que flui do Teu altar,"],
                ["O tempo de espera logo vai terminar,", "A trombeta nos ares está prestes a soar,"],
            ]
            v2_closings = [
                ["Veremos as ruas de ouro e o mar de cristal,", "Quando soar nas nuvens o toque triunfal."],
                ["Seremos transformados na glória de Jesus,", "Revestidos pra sempre de imortalidade e luz."],
                ["E o Noivo esperado em glória descerá,", "Toda saudade antiga em Seu abraço acabará."],
                ["Diante do Teu trono cantaremos sem cessar,", "Na pátria prometida onde vamos habitar."],
            ]
            pre_pool = [
                ["O Espírito e a Noiva clamam em uma só voz:", "Maranata, Rei da Glória, vem buscar a todos nós!"],
                ["Esta santa saudade aponta para o céu,", "Onde veremos Cristo sem a sombra de um véu:"],
                ["Já posso ouvir os anjos preparando a canção,", "E o coração da Igreja pulsa em adoração:"],
                ["Mais perto está o dia da nossa redenção,", "Erguemos para o alto a nossa oração:"],
            ]
            chorus_pool = [
                [
                    "Que saudade eu sinto da Cidade Celestial!",
                    "Do abraço do Cordeiro no banquete eternal!",
                    "Aqui sou peregrino, minha pátria está nos céus,",
                    "Face a face adorarei na presença do meu Deus!",
                    "Ora vem, Senhor Jesus, consumar a redenção,",
                    "Tua Noiva Te espera de todo o coração!"
                ],
                [
                    "Cidade Santa, Nova Jerusalém!",
                    "Onde o Cordeiro Vivo é a luz que nos mantém!",
                    "Deus enxugará dos olhos toda dor e aflição,",
                    "A morte foi vencida pelo Autor da Salvação!",
                    "Maranata, vem depressa, nosso amado Salvador,",
                    "Leva a Tua Igreja para o Reino do Teu amor!"
                ],
                [
                    "Minha alma suspira pelos átrios do Senhor!",
                    "Tenho sede do meu lar, tenho fome do Teu amor!",
                    "Na casa do meu Pai muitas moradas há,",
                    "Jesus foi preparar lugar e em breve voltará!",
                    "Todo joelho se dobrará diante do Rei Jesus,",
                    "Para sempre viveremos na Cidade da Tua Luz!"
                ],
            ]
            bridge_pool = [
                [
                    "Não há mais morte, não há mais dor!",
                    "Só o cântico novo ao nosso Redentor!",
                    "Prepara as nossas vestes em santidade e fé,",
                    "Até o grande dia em que estivermos de pé!"
                ],
                [
                    "Abre os portais eternos, ó Cidade de Luz!",
                    "Queremos contemplar a face de Jesus!",
                    "Valeu a pena esperar, valeu a pena crer,",
                    "Com o Rei dos Reis pra sempre iremos viver!"
                ],
                [
                    "Vem, Senhor Jesus! O Teu povo clama a Ti!",
                    "Acende a esperança enquanto estamos aqui!",
                    "De glória em glória até o céu se abrir,",
                    "O nosso Rei eterno está prestes a vir!"
                ],
            ]

        # =========================================================================
        # FAMÍLIA 2: AMOR A DEUS / PRIMEIRO AMOR / AMOR ÁGAPE DA CRUZ
        # =========================================================================
        elif any(w in t_lower for w in ["amor", "ágape", "agape", "primeiro amor", "devoção", "amou", "1 joão 4", "joão 3:16", "romanos 5:8", "marcos 12:30"]):
            base_titles = [
                "Chama do Primeiro Amor",
                "Oceano do Teu Ágape",
                "Porque Me Amaste Primeiro",
                "De Todo o Meu Coração",
                "Laços de Eterna Ternura",
                "Amor Escrito no Calvário",
                "Minha Alma Tem Sede de Ti",
                "Fogo no Altar da Devoção",
            ]
            v1_openings = [
                ["Antes que a aurora tocasse a imensidão,", "Teu coração já tinha a nossa redenção,"],
                ["Como a corça suspira pelas águas a correr,", "Assim a minha alma anseia pelo Teu viver,"],
                ["Não foi por meu esforço nem por merecimento,", "Mas pelo Teu eterno e santo livramento,"],
                ["De madrugada acordo para buscar Tua luz,", "Nada neste mundo se compara a Ti, Jesus,"],
            ]
            v1_closings = [
                [f"Como revela a graça escrita em {scripture_ref},", "Fomos resgatados pelo sangue de Jesus."],
                ["Tua benignidade vale mais que a própria vida,", "Em Teu altar sagrado minha história está contida."],
                ["Com laços de ternura Tu vieste me atrair,", "E hoje o meu prazer é Te amar e Te servir."],
            ]
            v2_openings = [
                ["Qual é a altura e a largura desse eterno amor?", "Que entregou o Filho amado pelo pecador,"],
                ["Quem mais eu tenho nos céus além de Ti, Senhor?", "Na terra não desejo outro bem ou esplendor,"],
                ["Ainda que a carne e o coração venham a falhar,", "Deus é a fortaleza onde posso descansar,"],
            ]
            v2_closings = [
                ["O perfeito amor lança fora todo o medo,", "E guarda a minha vida no Teu santo segredo."],
                ["Nem altura nem abismo podem nos separar,", "Do amor que no Calvário veio nos salvar."],
                ["Quero voltar às obras da primeira paixão,", "E derramar meu vaso em pura adoração."],
            ]
            pre_pool = [
                ["Nós Te amamos porque Tu nos amaste primeiro,", "Rendemos nossa vida aos pés do Cordeiro:"],
                ["Toma o meu fôlego, recebe o meu louvor,", "Acende em meu peito o primeiro amor:"],
            ]
            chorus_pool = [
                [
                    "Eu Te amo, Senhor, de todo o meu coração!",
                    "Minha alma transborda em grata adoração!",
                    "Nem a morte, nem a vida, nem a tribulação",
                    "Vão me separar da Tua santa comunhão!",
                    "És meu Tesouro eterno, minha Rocha e minha Luz,",
                    "Todo o meu afeto pertence a Ti, Jesus!"
                ],
                [
                    "Ó Amor incomparável que brilhou lá na cruz!",
                    "Nossa vida inteira se rende a Ti, Jesus!",
                    "Mais profundo que os mares é o Teu perdão,",
                    "Escreveste o Teu nome em nosso coração!",
                    "Para sempre cantaremos a grandeza desse amor,",
                    "Digno de toda honra és Tu, nosso Redentor!"
                ],
            ]
            bridge_pool = [
                [
                    "Acende outra vez a chama do primeiro amor!",
                    "Purifica o nosso altar, ó Santo Redentor!",
                    "As muitas águas não apagarão essa paixão,",
                    "Reina soberano sobre a nossa geração!"
                ],
                [
                    "Mais que palavras, entregamos nosso ser!",
                    "Para o Teu louvor queremos sempre viver!",
                    "Tudo o que somos vem da Tua mão,",
                    "Recebe a nossa eterna gratidão!"
                ],
            ]

        # =========================================================================
        # FAMÍLIA 3: SANTIDADE / TRONO / ISAÍAS 6 / APOCALIPSE 4
        # =========================================================================
        elif any(w in t_lower for w in ["santidade", "serafins", "isaías 6", "isaias 6", "apocalipse 4", "salmo 99", "êxodo 15", "kadosh"]):
            base_titles = [
                "Beleza da Tua Santidade",
                "Diante do Mar de Cristal",
                "Coroas aos Pés do Rei",
                "Kadosh, O Senhor Reina",
                "Trovões do Trono de Glória",
                "Santo Pelos Séculos",
            ]
            v1_openings = [
                ["Quem é semelhante a Ti entre os poderes,", "Glorificado em santidade, temível em louvores,"],
                ["Diante do trono onde brilha o cristal,", "Prostram-se os anjos em reverência real,"],
                ["Os céus manifestam o Teu resplendor,", "Toda a criação treme diante do Senhor,"],
            ]
            v1_closings = [
                [f"Conforme a visão sagrada de {scripture_ref},", "Todo o universo se curva perante Jesus."],
                ["Tua glória preenche o templo celestial,", "Rei eterno, soberano, justo e imortal."],
            ]
            v2_openings = [
                ["Anciãos depositam suas coroas no chão,", "Reconhecendo o autor da eterna criação,"],
                ["Toca os nossos lábios com a brasa do altar,", "Purifica a Tua Igreja para Te adorar,"],
            ]
            v2_closings = [
                ["Subimos ao Teu monte com temor e tremor,", "Pois o nosso Deus é fogo consumidor."],
                ["Pelo sangue do Cordeiro podemos entrar,", "E a beleza da Tua santidade contemplar."],
            ]
            pre_pool = [
                ["Unimos nossas vozes ao coro celestial,", "Exaltando o Deus eterno em glória triunfal:"],
            ]
            chorus_pool = [
                [
                    "Santo, Santo, Santo é o Senhor Deus Todo-Poderoso!",
                    "Que era, que é, e que há de vir, Rei glorioso!",
                    "Toda a terra está repleta do Teu esplendor,",
                    "Só Tu és digno de receber honra e louvor!"
                ],
            ]
            bridge_pool = [
                [
                    "Eis-me aqui, Senhor, purificado por Tua luz!",
                    "Envia a Tua Igreja em nome de Jesus!",
                    "Reina para sempre sobre toda nação,",
                    "Recebe o nosso clamor e adoração!"
                ],
            ]

        # =========================================================================
        # FAMÍLIA 4: TEMAS GERAIS & DINÂMICOS (FÉ, GRAÇA, CURA, ESPÍRITO SANTO, REFÚGIO, ETC.)
        # =========================================================================
        else:
            kw1 = sacred_words[0] if len(sacred_words) > 0 else "Tua presença"
            kw2 = sacred_words[1] if len(sacred_words) > 1 else "Tua promessa"
            kw3 = sacred_words[2] if len(sacred_words) > 2 else "Teu santo altar"
            attr1 = attributes[0] if len(attributes) > 0 else "Deus Soberano"

            base_titles = [
                f"Altar de {kw1.title()}",
                f"Manancial de {kw2.title()}",
                f"Soberano em {theme_title[:25].title()}",
                f"Luz da Promessa Viva",
                f"Rocha de {kw1.title()}",
                f"Cântico de {attr1.title()}",
            ]
            v1_openings = [
                [f"Diante da Palavra viva em {scripture_ref},", "Meu coração descansa sob a luz da Tua cruz,"],
                ["Quando o silêncio tenta calar a minha voz,", "Lembro que o Deus Eterno caminha entre nós,"],
                ["Levantamos nossos olhos para o monte do Senhor,", "De onde vem a força, a graça e o penhor,"],
            ]
            v1_closings = [
                [f"Contemplo em Tua glória a riqueza de {kw1.lower()},", "Pois somente em Tua mão encontro direção e paz."],
                [f"Guardando no coração a verdade: '{verse_essence[:48]}',", "Sabemos que a Tua destra jamais falhará."],
            ]
            v2_openings = [
                [f"Tu és exaltado como {attr1},", f"Que transforma o deserto pelo poder de {kw2.lower()},"],
                ["As tempestades ouvem o som da Tua voz,", "E o véu que separava já se rasgou por nós,"],
            ]
            v2_closings = [
                [f"Erguemos nossas mãos junto a {kw3.lower()},", "Para que o Nome de Cristo venha sempre triunfar."],
                ["Nossa fé se firma na rocha da salvação,", "Onde o Espírito Santo renova o coração."],
            ]
            pre_pool = [
                [f"Ecoa em nossa alma a promessa de {scripture_ref},", "Por isso toda a Igreja exalta o Rei Jesus:"],
            ]
            chorus_pool = [
                [
                    "Santo e Fiel é o Senhor da nossa salvação!",
                    f"Celebramos {kw1.lower()} em plena comunhão!",
                    "Do trono da graça flui o rio do Teu poder,",
                    "Jesus, o Verbo Vivo, é a razão do nosso ser!"
                ],
                [
                    f"Tu és {attr1}, nossa Rocha e Redentor!",
                    "Em meio à caminhada provamos Teu favor!",
                    f"Sustentados para sempre por {kw2.lower()},",
                    "A Ti, Senhor Jesus, todo o nosso louvor!"
                ],
            ]
            bridge_pool = [
                [
                    f"Derrama sobre nós {kw1.lower()} sem cessar!",
                    "Que toda a terra veja a Tua glória brilhar!",
                    "A Ti, Cordeiro Santo, toda honra e majestade,",
                    "De geração em geração por toda a eternidade!"
                ],
            ]

        chosen_title = self._pick_unused_title(base_titles, scripture_ref, used_base_titles)
        v1_lines = self._pick_unused_couplet(v1_openings, used_lines) + self._pick_unused_couplet(v1_closings, used_lines)
        v2_lines = self._pick_unused_couplet(v2_openings, used_lines) + self._pick_unused_couplet(v2_closings, used_lines)
        pre_lines = self._pick_unused_couplet(pre_pool, used_lines)
        chorus_lines = self._pick_unused_couplet(chorus_pool, used_lines)
        bridge_lines = self._pick_unused_couplet(bridge_pool, used_lines)

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
                        "A Ti toda a glória, Jesus. Amém.",
                    ],
                ),
            ],
        )
