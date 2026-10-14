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

    def _pick_unused_section(self, pool: list[list[str]], used_lines: set[str]) -> list[str]:
        """Sorteia uma estrofe/refrão dando prioridade absoluta à que tiver menos linhas repetidas no histórico."""
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

        t_lower = f"{theme_title} {scripture_full} {self._last_dossier.exegetical_summary if self._last_dossier else ''}".lower()

        # =========================================================================
        # FAMÍLIA: SE TORNAR COMO CRIANÇA / HUMILDADE / SIMPLICIDADE & COLO DO PAI
        # =========================================================================
        if any(w in t_lower for w in [
            "criança", "crianca", "crianças", "criancas", "pequenos", "pequeninos",
            "como crianca", "como criança", "como uma crianca", "como uma criança",
            "tornar como crianca", "tornar como criança", "se tornar como crianca",
            "se tornar como uma crianca", "se tornar como uma criança", "se tornar como",
            "mateus 18", "marcos 10", "lucas 18", "salmo 131", "colo do pai",
            "humildade", "simplicidade", "singeleza", "desmamada", "menino", "filhinhos"
        ]):
            base_titles = [
                "Como Uma Criança nos Teus Braços",
                "No Colo do Meu Pai",
                "Coração Singelo e Puro",
                "O Menor no Teu Reino",
                "Alma Serena em Teus Braços",
                "Simplicidade Diante do Altar",
                "Descanso Filial em Ti",
                "Ensina-me a Ser Pequeno",
            ]
            v1_openings = [
                ["Despindo o orgulho e as glórias que o mundo me deu,", "Venho como um menino aos pés do Deus dos céus,"],
                ["Como a criança desmamada no colo a descansar,", "Fiz calar a minha alma para Te adorar,"],
                ["Não busco grandezas que não posso alcançar,", "Apenas nos Teus braços desejo repousar,"],
                ["Jesus chamou os pequeninos com tanto amor e luz,", "O Teu Reino pertence a quem se curva à Tua cruz,"],
            ]
            v1_closings = [
                [f"Conforme a santa Palavra viva em {scripture_ref},", "Quem se faz bem pequeno encontra o Reino pela fé."],
                ["Nos Teus braços de amor descanso o coração,", "Encontrando a pureza da verdadeira adoração."],
                ["Pois dos tais é o Teu Reino de graça e redenção,", "Onde a fé de uma criança desfaz toda aflição."],
            ]
            v2_openings = [
                ["Abba, Pai de bondade, seguro a Tua mão,", "Guia os meus passos com Tua santa direção,"],
                ["Olho nos Teus olhos e esqueço todo o temor,", "Pois sou Teu filho amado, guardado em Teu amor,"],
                ["Cria em mim a pureza de um sincero coração,", "Longe da vaidade e de toda pretensão,"],
            ]
            v2_closings = [
                ["Nos Teus braços paternos a alma encontra a paz,", "Tua doce presença é tudo o que me satisfaz."],
                ["Ensina-me a viver na mais pura dependência,", "Rendendo todo o meu ser à Tua santa providência."],
                ["A maior grandeza é ser menor diante do Rei,", "Na Tua santa graça para sempre viverei."],
            ]
            pre_pool = [
                ["Ouvindo a doce voz do Salvador a me chamar:", "Deixai vir a Mim os pequeninos para amar:"],
                ["Aos sábios deste mundo a glória se escondeu,", "Mas aos pequeninos o Pai se revelou do céu:"],
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
                ],
                [
                    "Dos pequeninos é o Reino da Tua santa paz,",
                    "O Teu amor paterno tudo me satisfaz!",
                    "Abba Pai, meu refúgio e consolador,",
                    "Recebe a singeleza do meu humilde louvor!",
                ],
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
                ],
            ]
            outro_pool = [
                "Nos Teus braços de amor descanso... Como uma criança. Amém.",
                "Abba Pai, eu sou Teu filho pequeno. Amém.",
                "Simples, puro e dependente de Ti, Jesus. Amém.",
            ]

        # =========================================================================
        # FAMÍLIA 1: CURA / LIBERTAÇÃO / RESTAURAÇÃO / JEOVÁ RAFÁ
        # =========================================================================
        elif any(w in t_lower for w in [
            "cura", "curado", "sarado", "sara", "jeová rafá", "jeova rafa", "lucas 4",
            "enfermidade", "libertação", "libertacao", "cativos", "pisaduras",
            "bálsamo", "balsamo", "médico", "medico", "restauração", "restauracao",
            "êxodo 15", "exodo 15", "jeremias 17", "salmo 103:2", "sol da justiça"
        ]):
            base_titles = [
                "O Senhor Que Me Sara",
                "Cadeias Rompidas na Cruz",
                "Jeová Rafá, Minha Cura",
                "Pelas Suas Pisaduras Sarados",
                "Bálsamo Que Restaura a Alma",
                "Toque de Vida e Graça",
                "O Sol da Justiça Nasceu",
                "Libertação aos Cativos",
            ]
            v1_openings = [
                ["O Espírito do Senhor está sobre nós para ungir,", "As cadeias mais pesadas pela fé vão se abrir,"],
                ["Águas amargas se tornam manancial de poder,", "Quando o Senhor que sara nos faz renascer,"],
                ["Pelas Tuas feridas fomos nós resgatados,", "Pelo Teu santo sangue sarados e curados,"],
                ["Ao clamor do aflito o Senhor se inclinou,", "Com a destra de justiça minha vida tocou,"],
            ]
            v1_closings = [
                [f"Conforme a promessa viva em {scripture_ref},", "A graça de Jesus desfaz as trevas e traz luz."],
                ["Nenhuma enfermidade pode resistir ao Teu poder,", "Pois Tu és Jeová Rafá que nos faz reviver."],
                ["O bálsamo celeste desce sobre o coração,", "Trazendo vida nova, paz e libertação."],
            ]
            v2_openings = [
                ["Aos quebrantados de coração o Senhor vem curar,", "E todo cativeiro em vitória transformar,"],
                ["Sol da Justiça que traz salvação nas Suas asas,", "Tua presença enche de saúde nossas casas,"],
                ["Ele perdoa todas as nossas iniquidades,", "E sara com amor todas as enfermidades,"],
            ]
            v2_closings = [
                ["Levantamos as mãos para render gratidão,", "Pois em Cristo encontramos total restauração."],
                ["Onde havia tristeza nasce um hino de louvor,", "Ao Deus que nos renova em Seu eterno amor."],
                ["Toda dor se dissipa na presença do Rei,", "Na Sua fidelidade sempre confiarei."],
            ]
            pre_pool = [
                ["Quebrem-se as correntes, abram-se as prisões,", "O Libertador opera em nossos corações:"],
                ["Ele levou sobre Si as nossas dores e aflições,", "Ouvindo o clamor humilde de nossas orações:"],
            ]
            chorus_pool = [
                [
                    "Tu és Jeová Rafá, o Deus que sara e restaura!",
                    "Toda enfermidade e jugo cai agora!",
                    "Pelas Tuas pisaduras sarados nós somos,",
                    "Filhos redimidos pelo sangue que fomos!",
                    "Jesus, o Médico dos médicos, opera com poder,",
                    "Vida abundante faz em nós florescer!"
                ],
                [
                    "Rompeu os grilhões, libertou os cativos!",
                    "Em Cristo Jesus nós estamos vivos!",
                    "Sua destra de graça nos levantou do pó,",
                    "Adoramos ao Senhor que é Santo e Deus só!",
                    "Toda glória a Jesus, nosso Libertador,",
                    "Que sara a ferida com Seu santo amor!"
                ],
            ]
            bridge_pool = [
                [
                    "Haja vida! Haja cura no Teu santo nome!",
                    "O poder do pecado e da morte se consome!",
                    "Ergue-te, ó Igreja, em fé e santidade,",
                    "Jesus é o mesmo ontem, hoje e por toda a eternidade!"
                ],
                [
                    "Basta uma palavra da Tua santa voz,",
                    "E o milagre acontece no meio de nós!",
                    "Para sempre exaltamos o Teu braço forte,",
                    "Que venceu a doença, o pecado e a morte!"
                ],
            ]

        # =========================================================================
        # FAMÍLIA 2: VOLTA DE CRISTO / SEGUNDA VINDA / MARANATA
        # =========================================================================
        elif any(w in t_lower for w in [
            "volta", "maranata", "segunda vinda", "arrebatamento", "trombeta",
            "nuvens", "noiva", "1 tessalonicenses", "tessalonicenses 4",
            "apocalipse 22", "apocalipse 19", "mateus 24", "mateus 25"
        ]):
            base_titles = [
                "O Clamor da Noiva",
                "Maranata, O Rei Vem",
                "Ao Som da Última Trombeta",
                "O Noivo Vem Nas Nuvens",
                "Certamente Venho Sem Demora",
                "Até Que Ele Venha",
                "Vigiai, O Rei Está Às Portas",
            ]
            v1_openings = [
                ["Ergamos os nossos olhos para o horizonte além,", "Ouvindo o sussurro santo: o Noivo em breve vem,"],
                ["O gemido da criação logo vai cessar,", "Quando o Cordeiro em glória nas nuvens despontar,"],
                ["Com as lâmpadas acesas e o azeite a transbordar,", "A Igreja vigilante se prepara para adorar,"],
            ]
            v1_closings = [
                [f"Conforme a Palavra viva em {scripture_ref},", "Todo olho O verá descendo em majestade e luz."],
                ["O mundo e suas dores vão para sempre findar,", "E a face do Amado vamos contemplar."],
            ]
            v2_openings = [
                ["A trombeta de Deus nos ares ressoará,", "E a voz do Arcanjo os santos despertará,"],
                ["Seremos transformados na glória do Senhor,", "Para sempre unidos ao nosso Salvador,"],
            ]
            v2_closings = [
                ["Toda lágrima dos olhos o próprio Deus limpará,", "E a morte derrotada nunca mais voltará."],
                ["Na ceia do Cordeiro tomaremos o nosso lugar,", "Com vestes de justiça para sempre celebrar."],
            ]
            pre_pool = [
                ["O Espírito e a Noiva clamam a uma voz:", "Maranata, Rei da Glória, vem buscar a todos nós!"],
                ["A noite está findando, o dia vai raiar,", "Prepara-te, ó Noiva, o Rei vai chegar:"],
            ]
            chorus_pool = [
                [
                    "Maranata! Ora vem, Senhor Jesus!",
                    "Desce em Tua glória, esplendor e luz!",
                    "A Igreja Te espera com ardente clamor,",
                    "Reina pelos séculos, bendito Salvador!",
                    "Todo joelho se dobrará diante do Rei dos Reis,",
                    "Para sempre exaltado entre todos os Seus fiéis!"
                ],
                [
                    "O Noivo esperado em breve voltará!",
                    "Toda a criação diante Dele se prostrará!",
                    "Vem buscar Tua Noiva comprada na cruz,",
                    "Nossa esperança viva é o Teu retorno, Jesus!",
                    "Aleluia ao Cordeiro que triunfou na dor,",
                    "Maranata para sempre ao nosso Redentor!"
                ],
            ]
            bridge_pool = [
                [
                    "Tragada foi a morte na vitória da cruz!",
                    "Os portais se abrirão para o Rei Jesus!",
                    "Face a face com o Cordeiro cantaremos sem cessar:",
                    "Santo, Santo é o Senhor que veio nos resgatar!"
                ],
                [
                    "Ouçam o clamor que ecoa pelas nações:",
                    "O Leão de Judá vem libertar os corações!",
                    "Nem sombras nem sepulturas O puderam deter,",
                    "O Rei está voltando com suprema glória e poder!"
                ],
            ]

        # =========================================================================
        # FAMÍLIA 3: SAUDADE DA PÁTRIA CELESTIAL & NOVA JERUSALÉM
        # =========================================================================
        elif any(w in t_lower for w in [
            "saudade", "cidade celestial", "nova jerusalém", "nova jerusalem",
            "pátria", "patria", "peregrino", "morada", "mansão", "mansao",
            "hebreus 11", "salmo 84", "apocalipse 21", "filipenses 3:20", "joão 14:1"
        ]):
            base_titles = [
                "Santa Saudade do Teu Lar",
                "Saudade dos Átrios do Rei",
                "Além do Rio de Cristal",
                "Fundamentos da Pátria Celestial",
                "Suspiro de um Peregrino",
                "Ruas de Ouro e Luz Eterna",
                "Portais da Nova Jerusalém",
            ]
            v1_openings = [
                ["Caminho neste mundo como quem vai voltar,", "Trago no peito a chama de um eterno lar,"],
                ["Minha alma tem saudade dos átrios do Senhor,", "Onde não há mais pranto, nem sombras, nem temor,"],
                ["Como estrangeiro e peregrino passo por aqui,", "Pois minha herança eterna está guardada em Ti,"],
                ["Não pertenço às areias deste mundo fugaz,", "Busco a Cidade Santa onde reina a plena paz,"],
            ]
            v1_closings = [
                [f"Na promessa bendita escrita em {scripture_ref},", "Vejo a Cidade Eterna onde o Cordeiro é a luz."],
                ["Aguardo os fundamentos que o próprio Deus traçou,", "A Pátria Celestial que Jesus me preparou."],
                ["Onde os muros de jaspe refletem Teu esplendor,", "E a alma descansa nos braços do Redentor."],
            ]
            v2_openings = [
                ["As tendas desta terra não podem me prender,", "Pois lá nos altos céus está o meu viver,"],
                ["Lá não haverá noite, nem lâmpada ou sol,", "Pois a glória de Cristo é o nosso farol,"],
                ["Da árvore da vida em breve vou provar,", "Junto ao rio cristalino que flui do Teu altar,"],
            ]
            v2_closings = [
                ["Veremos as ruas de ouro e o mar de cristal,", "No banquete bendito do Reino eternal."],
                ["E o abraço do Pai toda dor dissipará,", "E a santa comunhão jamais terminará."],
                ["Diante do Teu trono cantaremos sem cessar,", "Na pátria prometida onde vamos habitar."],
            ]
            pre_pool = [
                ["Esta santa saudade aponta para o céu,", "Onde veremos Cristo sem a sombra de um véu:"],
                ["Já posso ouvir os anjos preparando a canção,", "E o coração da Igreja pulsa em adoração:"],
            ]
            chorus_pool = [
                [
                    "Que saudade eu sinto da Cidade Celestial!",
                    "Do abraço do Cordeiro no banquete eternal!",
                    "Aqui sou peregrino, minha pátria está nos céus,",
                    "Face a face adorarei na presença do meu Deus!",
                    "Minha alma anseia por contemplar a Tua luz,",
                    "Leva-me para o Teu lar, ó meu amado Jesus!"
                ],
                [
                    "Cidade Santa, Nova Jerusalém!",
                    "Onde o Cordeiro Vivo é a luz que nos mantém!",
                    "Deus enxugará dos olhos toda lágrima e dor,",
                    "Viveremos nos átrios do perfeito amor!",
                    "Valeu a pena crer, valeu a pena esperar,",
                    "Na casa do meu Pai é onde vou morar!"
                ],
            ]
            bridge_pool = [
                [
                    "Abre os portais eternos, ó Cidade de Luz!",
                    "Queremos contemplar a face de Jesus!",
                    "Nem ouro nem riquezas se comparam ao Teu olhar,",
                    "Contigo, ó Redentor, queremos sempre estar!"
                ],
                [
                    "Adeus, dores do mundo! Adeus, aflição!",
                    "Chegamos à morada da eterna redenção!",
                    "Com todos os remidos erguemos o louvor:",
                    "Para sempre em Sião com o nosso Salvador!"
                ],
            ]

        # =========================================================================
        # FAMÍLIA 4: AMOR A DEUS / PRIMEIRO AMOR / DEVOÇÃO
        # =========================================================================
        elif any(w in t_lower for w in [
            "primeiro amor", "amar a deus", "amo a deus", "devoção", "devocao",
            "intimidade", "sede de deus", "marcos 12:30", "salmo 42", "salmo 63",
            "salmo 73", "1 joão 4:19", "deuteronômio 6:5"
        ]):
            base_titles = [
                "Chama do Primeiro Amor",
                "De Todo o Meu Coração",
                "Porque Me Amaste Primeiro",
                "Minha Alma Tem Sede de Ti",
                "Fogo no Altar da Devoção",
                "Amor Que Não Se Apaga",
                "Tesouro Supremo da Minha Alma",
            ]
            v1_openings = [
                ["Como a corça suspira pelas águas a correr,", "Assim a minha alma anseia pelo Teu viver,"],
                ["De madrugada acordo para buscar Tua luz,", "Nada neste mundo se compara a Ti, Jesus,"],
                ["Quem mais eu tenho nos céus além de Ti, Senhor?", "Na terra não desejo outro bem ou esplendor,"],
            ]
            v1_closings = [
                [f"Conforme o mandamento doce em {scripture_ref},", "Consagro minha vida ao Teu amor, Jesus."],
                ["Tua benignidade vale mais que a própria vida,", "Em Teu altar sagrado minha história está contida."],
                ["Com laços de ternura Tu vieste me atrair,", "E hoje o meu prazer é Te amar e Te servir."],
            ]
            v2_openings = [
                ["Quero voltar às obras da primeira paixão,", "E derramar meu vaso em pura adoração,"],
                ["Ainda que a carne e o coração venham a falhar,", "Deus é a fortaleza onde posso descansar,"],
            ]
            v2_closings = [
                ["O perfeito amor lança fora todo o medo,", "E guarda a minha vida no Teu santo segredo."],
                ["As muitas águas não apagarão esse amor,", "Pois foste Tu quem me amou primeiro, ó Redentor."],
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
                    "Acende o fogo que nunca se apagará!",
                    "Em Teu altar meu coração descansará!",
                    "Mais que bênçãos ou dons, eu quero a Ti, Senhor,",
                    "Viver mergulhado no Teu imenso amor!",
                    "A Ti me entrego em santa devoção,",
                    "Reina absoluto sobre a minha oração!"
                ],
            ]
            bridge_pool = [
                [
                    "Acende outra vez a chama do primeiro amor!",
                    "Purifica o nosso altar, ó Santo Redentor!",
                    "Toda a minha afeição pertence a Ti, Jesus,",
                    "Que deste a Tua vida por mim naquela cruz!"
                ],
            ]

        # =========================================================================
        # FAMÍLIA 5: GRAÇA SALVADORA / SACRIFÍCIO DA CRUZ / REDENÇÃO
        # =========================================================================
        elif any(w in t_lower for w in [
            "graça", "graca", "cruz", "calvário", "calvario", "sangue", "redenção",
            "redencao", "justificação", "justificacao", "efésios 2:8", "romanos 5:1",
            "gálatas 2:20", "cordeiro imolado"
        ]):
            base_titles = [
                "Amor Escrito no Calvário",
                "Oceano do Teu Ágape",
                "A Cruz Que Me Salvou",
                "Pela Graça Fui Comprado",
                "Precioso Sangue Vertido",
                "O Véu Rasgado no Gólgota",
            ]
            v1_openings = [
                ["Não foi por meu esforço nem por merecimento,", "Mas pelo Teu eterno e santo livramento,"],
                ["Olho para o madeiro onde o Justo padeceu,", "E vejo o infinito amor que me acolheu,"],
            ]
            v1_closings = [
                [f"Conforme a graça revelada em {scripture_ref},", "Fomos resgatados pelo sangue de Jesus."],
                ["Ali o castigo da nossa paz caiu sobre Ti,", "E vida abundante conquistaste para mim."],
            ]
            v2_openings = [
                ["O véu do santuário de alto a baixo se rasgou,", "E o caminho vivo para o Pai se inaugurou,"],
                ["Já não sou eu quem vive, mas Cristo vive em mim,", "Uma aliança eterna que jamais terá um fim,"],
            ]
            v2_closings = [
                ["Justificados pela fé temos a paz com Deus,", "Herdeiros com Jesus das bênçãos lá dos céus."],
                ["Nenhuma condenação há para quem em Cristo está,", "Sua misericórdia para sempre nos susterá."],
            ]
            pre_pool = [
                ["Diante da cruz nos prostramos em gratidão,", "Erguendo aos céus o cântico da redenção:"],
            ]
            chorus_pool = [
                [
                    "Ó Graça sublime que resgatou o pecador!",
                    "Lavados no sangue do nosso Redentor!",
                    "Está consumado, a dívida Ele pagou,",
                    "Das garras da morte e do medo nos livrou!",
                    "Para sempre exaltamos o nome de Jesus,",
                    "O Cordeiro imaculado que venceu naquela cruz!"
                ],
            ]
            bridge_pool = [
                [
                    "Não há outro nome pelo qual possamos nos salvar!",
                    "Jesus Cristo, o Justo, que veio nos resgatar!",
                    "A Ele toda honra, o louvor e o poder,",
                    "A razão infinita do nosso viver!"
                ],
            ]

        # =========================================================================
        # FAMÍLIA 6: SANTIDADE / MAJESTADE / TRONO CELESTIAL
        # =========================================================================
        elif any(w in t_lower for w in [
            "santidade", "santo", "trono", "serafins", "isaías 6", "isaias 6",
            "apocalipse 4", "salmo 99", "kadosh", "fogo consumidor"
        ]):
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
        # FAMÍLIA 7: REFÚGIO / FORTALEZA / PAZ NA PROVAÇÃO
        # =========================================================================
        elif any(w in t_lower for w in [
            "refúgio", "refugio", "fortaleza", "provação", "provacao", "vale",
            "deserto", "tempestade", "salmo 46", "salmo 91", "salmo 23",
            "habacuque", "2 coríntios 12", "tiago 1", "paz"
        ]):
            base_titles = [
                "Refúgio Inabalável",
                "Socorro Bem Presente",
                "O Pastor Que Me Guia No Vale",
                "Ainda Que a Figueira Não Floresça",
                "À Sombra do Onipotente",
                "A Paz Que Excede Todo o Entendimento",
            ]
            v1_openings = [
                ["Ainda que a terra se transtorne e os montes caiam no mar,", "No refúgio do Altíssimo minh'alma vai descansar,"],
                ["O Senhor é o meu pastor e nada vai me faltar,", "Por verdes pastos serenos Ele me faz caminhar,"],
            ]
            v1_closings = [
                [f"Seguro na promessa fiel de {scripture_ref},", "Minha esperança viva está posta em Jesus."],
                ["Sob Suas asas sagradas encontro proteção,", "Minha rocha segura em tempos de aflição."],
            ]
            v2_openings = [
                ["Ainda que eu ande pelo vale escuro e sombrio,", "Não temerei mal algum, pois em Deus eu confio,"],
                ["Tua graça me basta quando fraco eu me sinto,", "Pois Teu poder se aperfeiçoa e me faz convicto,"],
            ]
            v2_closings = [
                ["Tua vara e Teu cajado me trazem consolo e paz,", "A fidelidade do Senhor jamais volta atrás."],
                ["Ainda que a figueira não venha a florescer,", "No Deus da salvação o meu ser vai se erguer."],
            ]
            pre_pool = [
                ["Não temerei o terror da noite nem o perigo,", "Pois o Senhor Todo-Poderoso caminha comigo:"],
            ]
            chorus_pool = [
                [
                    "Deus é o nosso refúgio e fortaleza presente!",
                    "Socorro bem certo no coração do crente!",
                    "A tempestade se aquieta ao som da Tua voz,",
                    "O Deus de Jacó é refúgio seguro para nós!",
                    "Descanso em Tua paz que excede o entendimento,",
                    "Fiel para sempre em cada momento!"
                ],
            ]
            bridge_pool = [
                [
                    "Minha âncora firme em meio ao vendaval!",
                    "Tua fidelidade me livra de todo o mal!",
                    "Passarão os céus e a terra, mas Tua Palavra não passará,",
                    "Quem confia no Senhor jamais se abalará!"
                ],
            ]

        # =========================================================================
        # FAMÍLIA 8: ESPÍRITO SANTO / AVIVAMENTO / PENTECOSTES
        # =========================================================================
        elif any(w in t_lower for w in [
            "espírito", "espirito", "pentecostes", "avivamento", "unção", "uncao",
            "consolador", "fogo", "vento", "atos 2", "ezequiel 37", "zacarias 4"
        ]):
            base_titles = [
                "Vento Impetuoso do Céu",
                "Fogo do Espírito Santo",
                "Rios de Água Viva",
                "Sopra Sobre os Ossos Secos",
                "Aviva a Tua Obra, Senhor",
            ]
            v1_openings = [
                ["Como em Jerusalém de repente o vento soprou,", "O poder do Espírito Santo o cenáculo inundou,"],
                ["Sopra, ó Vento dos quatro cantos sobre o nosso altar,", "Para que este povo possa ressuscitar,"],
            ]
            v1_closings = [
                [f"Conforme prometido em {scripture_ref},", "Línguas de fogo descem revelando a Jesus."],
                ["Não por força nem por violência haveremos de vencer,", "Mas pelo Santo Espírito e Seu eterno poder."],
            ]
            v2_openings = [
                ["Do nosso interior fluirão rios de vida e graça,", "Consumindo o pecado enquanto Tua presença passa,"],
                ["Consolador bendito que nos guia em verdade,", "Enche a Tua Igreja de santa autoridade,"],
            ]
            v2_closings = [
                ["Queima a palha do ego e acende o fervor,", "Para que o mundo veja a glória do Salvador."],
                ["Produz em nosso peito o fruto de retidão,", "Amor, paciência, paz e consagração."],
            ]
            pre_pool = [
                ["Ouvimos o estrondo da Tua glória a descer,", "Aviva o Teu povo com fogo e poder:"],
            ]
            chorus_pool = [
                [
                    "Vem, Santo Espírito, enche este lugar!",
                    "Batiza com fogo o nosso coração e altar!",
                    "Rios de água viva brotem do nosso ser,",
                    "Aviva a Tua Igreja para Te obedecer!",
                    "A Ti, Consolador, todo o nosso clamor,",
                    "Glorifica a Jesus Cristo, o nosso Senhor!"
                ],
            ]
            bridge_pool = [
                [
                    "Vento impetuoso, sopra outra vez!",
                    "Queremos viver a pureza que um dia nos deste!",
                    "Até que as nações se curvem diante da cruz,",
                    "No poder do Espírito Santo em nome de Jesus!"
                ],
            ]

        # =========================================================================
        # FAMÍLIA 9: LOUVOR CONGREGACIONAL / GRATIDÃO & JÚBILO
        # =========================================================================
        elif any(w in t_lower for w in [
            "gratidão", "gratidao", "louvor", "júbilo", "jubilo", "celebração", "celebracao",
            "salmo 100", "salmo 150", "filipenses 4", "alegria", "festa"
        ]):
            base_titles = [
                "Entrai Por Suas Portas Com Ações de Graças",
                "Celebrai Com Júbilo ao Senhor",
                "Bendize, Ó Minha Alma",
                "Tudo o Que Tem Fôlego Louve",
                "Cântico Novo de Alegria",
            ]
            v1_openings = [
                ["Celebrai com júbilo ao Senhor, todas as terras,", "Ele desfaz o pranto e vence todas as guerras,"],
                ["Bendize, ó minha alma, e não te esqueças jamais,", "De todos os Seus benefícios santos e reais,"],
            ]
            v1_closings = [
                [f"Conforme entoamos o cântico de {scripture_ref},", "Rendemos graças e honras ao Rei Jesus."],
                ["Porque o Senhor é bom e Sua misericórdia dura para sempre,", "Sua fidelidade alcança toda semente."],
            ]
            v2_openings = [
                ["Entrai por Suas portas entoando hinos de amor,", "Nos Seus átrios sagrados tributando louvor,"],
                ["Tudo quanto tem fôlego erga a voz e proclame,", "Que não há outro Deus cujo poder se derrame,"],
            ]
            v2_closings = [
                ["Com trombetas e harpas, saltério e tamborim,", "Exaltamos a graça que não terá fim."],
                ["A alegria do Senhor é a nossa fortaleza,", "Em Sua presença santa contemplamos pureza."],
            ]
            pre_pool = [
                ["Batam palmas os povos, cantem com exaltação,", "Pois o Senhor é grande sobre toda nação:"],
            ]
            chorus_pool = [
                [
                    "Aleluia ao Senhor! Digno de todo louvor!",
                    "Exaltamos com júbilo o nosso Redentor!",
                    "Entramos em Seus átrios com ações de gratidão,",
                    "Pois Ele fez prodígios na nossa redenção!",
                    "Seja a glória, a honra e o poder eternal,",
                    "Ao nosso Deus bendito no trono celestial!"
                ],
            ]
            bridge_pool = [
                [
                    "Celebrem céus e terra, montanhas e mares!",
                    "Ecoem hinos santos por todos os lugares!",
                    "Do nascer do sol até o poente brilhar,",
                    "O nome de Jesus vamos glorificar!"
                ],
            ]

        # =========================================================================
        # FAMÍLIA 10: TEMAS DINÂMICOS GERAIS
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

        # Selo bíblico e consagração final dinâmica por família
        outro_closing = "A Ti toda a honra, glória e louvor para sempre, Jesus. Amém."
        if any(w in t_lower for w in ["volta", "maranata", "segunda vinda"]):
            outro_closing = "Vem sem demora, Senhor Jesus! Tua Noiva Te espera. Amém."
        elif any(w in t_lower for w in ["saudade", "cidade", "pátria", "patria", "céu"]):
            outro_closing = "Nosso coração suspira pela Pátria Celestial. Amém."
        elif any(w in t_lower for w in ["cura", "médico", "medico", "sarado", "jeová rafá", "lucas 4"]):
            outro_closing = "Pelas Tuas pisaduras fomos sarados e restaurados para sempre. Amém."
        elif any(w in t_lower for w in ["santidade", "santo", "trono", "serafins"]):
            outro_closing = "Santo, Santo, Santo é o Senhor Deus Todo-Poderoso. Amém."
        elif any(w in t_lower for w in ["amor", "ágape", "primeiro amor"]):
            outro_closing = "Nós Te amamos porque Tu nos amaste primeiro, Jesus. Amém."
        elif any(w in t_lower for w in ["graça", "cruz", "sangue"]):
            outro_closing = "Pela graça fomos salvos e justificados no Teu sangue. Amém."
        elif any(w in t_lower for w in ["refúgio", "paz", "descanso"]):
            outro_closing = "Em paz me deito e durmo, pois só Tu, Senhor, me fazes viver seguro. Amém."
        elif any(w in t_lower for w in ["espírito", "espirito", "fogo", "avivamento"]):
            outro_closing = "Enche a Tua Igreja de poder e graça até que Tu venhas. Amém."
        elif any(w in t_lower for w in ["louvor", "gratidão", "júbilo", "celebração"]):
            outro_closing = "Tudo quanto tem fôlego louve ao Senhor! Aleluia! Amém."

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
