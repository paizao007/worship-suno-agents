"""
Orquestrador central do sistema de agentes de adoração para o Suno AI.
Implementa o fluxo de trabalho colaborativo e o loop de crítica e reflexão (Actor-Critic).
"""

from typing import Callable, Optional
from schemas import UserBriefing, TheologicalDossier, SongDraft, AuditReport, SunoSongPackage
from agents import TheologianAgent, LyricistAgent, AuditorAgent, SunoProducerAgent
import config


class WorshipSunoOrchestrator:
    def __init__(self, status_callback: Optional[Callable[[str, str], None]] = None):
        """
        Args:
            status_callback: Função opcional para notificar progresso na interface (ex: Rich/CLI).
        """
        self.theologian = TheologianAgent()
        self.lyricist = LyricistAgent()
        self.auditor = AuditorAgent()
        self.producer = SunoProducerAgent()
        self.status_callback = status_callback or (lambda etapa, msg: None)

    def execute(self, briefing: UserBriefing) -> tuple[TheologicalDossier, SongDraft, AuditReport, SunoSongPackage]:
        """
        Executa o pipeline completo:
        1. Análise Teológica e Exegese.
        2. Composição Poética Inicial.
        3. Ciclo de Auditoria Crítica (Reflexão com refatoração se necessário).
        4. Sonorização e Engenharia de Metatags para o Suno AI.
        """
        # Etapa 1: Teologia
        self.status_callback("THEOLOGY_START", f"Iniciando exegese bíblica sobre: {briefing.biblical_reference}")
        dossier = self.theologian.run(briefing)
        self.status_callback("THEOLOGY_DONE", f"Dossier teológico gerado: '{dossier.theme_title}'")

        # Etapa 2 & 3: Composição e Ciclo de Auditoria
        draft: Optional[SongDraft] = None
        audit_report: Optional[AuditReport] = None
        current_iteration = 1

        while current_iteration <= config.MAX_AUDIT_ITERATIONS:
            self.status_callback(
                "LYRICS_START",
                f"Compondo letra (Iteração {current_iteration}/{config.MAX_AUDIT_ITERATIONS})"
            )
            draft = self.lyricist.run(dossier, audit_feedback=audit_report)
            self.status_callback("LYRICS_DONE", f"Rascunho poético gerado: '{draft.title}'")

            self.status_callback("AUDIT_START", f"Auditor avaliando integridade doutrinária e métrica...")
            audit_report = self.auditor.run(draft, dossier)

            if audit_report.approved or audit_report.score >= config.MIN_PASSING_SCORE:
                self.status_callback(
                    "AUDIT_PASS",
                    f"Letra APROVADA com nota {audit_report.score:.1f}/10! Pronta para sonorização."
                )
                break
            else:
                self.status_callback(
                    "AUDIT_RETRY",
                    f"Letra reprovada com nota {audit_report.score:.1f}/10. Devolvendo ao letrista com instruções de correção."
                )
                current_iteration += 1

        # Etapa 4: Engenharia do Suno
        self.status_callback("SUNO_START", "Diretor Musical gerando metatags de áudio e prompt de estilo para o Suno AI...")
        suno_package = self.producer.run(draft, dossier, briefing)
        self.status_callback("SUNO_DONE", f"Pacote para Suno AI finalizado com sucesso! ({len(suno_package.style_of_music)} caracteres no estilo)")

        return dossier, draft, audit_report, suno_package
