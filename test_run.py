"""
Script de teste direto para validar a execução do orquestrador e geração de arquivos.
"""

from pathlib import Path
from schemas import UserBriefing
from orchestrator import WorshipSunoOrchestrator
from cli import display_theological_dossier, display_audit_report, display_suno_package

briefing = UserBriefing(
    theme="A Santidade de Deus e a Visão do Trono Celestial",
    biblical_reference="Isaías 6:1-8 e Apocalipse 4:8-11",
    musical_style_hint="Modern Worship congregacional solene, piano de cauda com crescendo para guitarras e coral épico",
    tempo_hint="Lento (68-72 BPM) com grande crescendo para clímax",
    vocal_preference="Voz masculina emotiva com coral harmônico celestial"
)

print("Iniciando teste automatizado do pipeline...")
orchestrator = WorshipSunoOrchestrator(
    status_callback=lambda stage, msg: print(f"[{stage}] {msg}")
)

dossier, draft, report, package = orchestrator.execute(briefing)

output_file = Path(__file__).parent / "suno_output_pronto.txt"
conteudo_salvar = f"""====================================================================
CANÇÃO DE ADORAÇÃO SACRA: {package.song_title}
GERADA PELO SISTEMA MULTIAGENTE PARA SUNO AI
====================================================================

1. CAMPO 'STYLE OF MUSIC' NO SUNO (COPIE E COLE ABAIXO):
{package.style_of_music}

2. CONFIGURAÇÕES ADICIONAIS RECOMENDADAS:
- Andamento: {package.target_bpm}
- Vocais: {package.vocal_configuration}
- Base Teológica: {package.theological_summary}

3. CAMPO 'LYRICS' NO SUNO (COPIE E COLE O BLOCO ABAIXO NO MODO CUSTOM):
--------------------------------------------------------------------
{package.lyrics_with_metatags}
--------------------------------------------------------------------

DICAS DE PRODUÇÃO NO SUNO:
{chr(10).join(f"- {tip}" for tip in package.suno_tips)}
"""
output_file.write_text(conteudo_salvar, encoding="utf-8")

display_theological_dossier(dossier)
display_audit_report(report)
display_suno_package(package, output_file=output_file)

print("\nTeste concluído com sucesso total!")
