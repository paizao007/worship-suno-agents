"""
Interface de linha de comando rica e interativa usando a biblioteca Rich.
Apresenta o fluxo de trabalho de cada agente com formatação visual elegante.
"""

import sys
from typing import Optional
from pathlib import Path

# Garante suporte a UTF-8 em consoles Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.syntax import Syntax
from rich import print as rprint

from schemas import UserBriefing, TheologicalDossier, SongDraft, AuditReport, SunoSongPackage
from orchestrator import WorshipSunoOrchestrator

console = Console(legacy_windows=False)


def print_banner():
    banner = """
    ╔═══════════════════════════════════════════════════════════════════════════════╗
    ║        🕊️  BANDA LVS LITÚRGICA MULTIAGENTE & SUNO AI  🎵                     ║
    ║        Harmonia Teológica • Prosódia Bíblica • Engenharia de Áudio             ║
    ╚═══════════════════════════════════════════════════════════════════════════════╝
    """
    console.print(Panel(Text(banner, justify="center", style="bold cyan"), border_style="blue"))


def display_theological_dossier(dossier: TheologicalDossier):
    table = Table(title="📜 Dossier Teológico & Exegético", border_style="gold1", title_style="bold gold1")
    table.add_column("Dimensão", style="bold yellow", width=25)
    table.add_column("Conteúdo Teológico", style="white")

    table.add_row("Tema Central", dossier.theme_title)
    table.add_row("Passagens Canônicas", "\n".join(f"• {p}" for p in dossier.primary_scriptures))
    table.add_row("Atributos de Deus", ", ".join(dossier.divine_attributes))
    table.add_row("Foco Cristocêntrico", dossier.christocentric_focus)
    table.add_row("Palavras Sagradas", ", ".join(dossier.sacred_keywords))
    table.add_row("Salvaguardas Doutrinárias", "\n".join(f"🚫 {g}" for g in dossier.doctrinal_guardrails))
    table.add_row("Tom Espiritual", dossier.emotional_and_spiritual_tone)

    console.print("\n")
    console.print(table)


def display_audit_report(report: AuditReport):
    status_color = "green" if report.approved else "red"
    status_text = "APROVADO" if report.approved else "REQUER REVISÃO"
    
    table = Table(title=f"⚖️ Parecer do Auditor Doutrinário & Métrico [{status_text}]", border_style=status_color)
    table.add_column("Métrica", style="bold", width=25)
    table.add_column("Avaliação", style="white")

    table.add_row("Nota Geral", f"[{status_color}]{report.score:.1f} / 10.0[/{status_color}]")
    table.add_row("Fidelidade Doutrinária", f"{report.theological_fidelity_score:.1f} / 10.0")
    table.add_row("Prosódia & Cantabilidade", f"{report.poetic_prosody_score:.1f} / 10.0")
    table.add_row("Pontos Fortes", "\n".join(f"✓ {s}" for s in report.strengths))
    
    if report.critiques:
        table.add_row("Observações Críticas", "\n".join(f"• {c}" for c in report.critiques))
    if report.actionable_revisions:
        table.add_row("Ajustes Solicitados", "\n".join(f"⚠️ {r}" for r in report.actionable_revisions))

    console.print("\n")
    console.print(table)


def display_suno_package(package: SunoSongPackage, output_file: Optional[Path] = None):
    console.print("\n")
    console.print(Panel(
        Text(f"🎵 PACOTE FINAL OTIMIZADO PARA O SUNO AI: '{package.song_title}'", justify="center", style="bold green"),
        border_style="green"
    ))

    # Estilo musical
    style_len = len(package.style_of_music)
    style_info = f"[bold cyan]Campo 'Style of Music' no Suno ({style_len} caracteres):[/bold cyan]\n[bold yellow]{package.style_of_music}[/bold yellow]"
    console.print(Panel(style_info, title="🎹 1. Configuração de Estilo (Custom Mode)", border_style="cyan"))

    # Configuração complementar
    info_table = Table(show_header=False, border_style="dim")
    info_table.add_column("Chave", style="bold magenta", width=20)
    info_table.add_column("Valor", style="white")
    info_table.add_row("Andamento Alvo", package.target_bpm)
    info_table.add_row("Configuração Vocal", package.vocal_configuration)
    info_table.add_row("Base Litúrgica", package.theological_summary)
    console.print(info_table)

    # Letras com metatags
    console.print("\n")
    console.print(Panel(
        package.lyrics_with_metatags,
        title="✍️ 2. Letra Formatada com Metatags (Copie e Cole no Campo 'Lyrics' do Suno)",
        border_style="bright_magenta"
    ))

    # Dicas práticas
    tips_text = "\n".join(f"• {tip}" for tip in package.suno_tips)
    console.print(Panel(tips_text, title="💡 Dicas Práticas de Produção no Suno AI", border_style="yellow"))

    if output_file:
        console.print(f"\n[bold green]✓ Pacote completo salvo com sucesso em:[/bold green] [underline]{output_file}[/underline]\n")


def run_cli_interactive():
    print_banner()

    console.print("[bold yellow]Vamos criar uma canção de adoração estruturada para o Suno AI![/bold yellow]\n")
    
    # Pergunta temas ou usa o exemplo clássico de Isaías 6
    theme = console.input("[bold cyan]Tema Central[/bold cyan] [dim](Ex: Santidade de Deus no Trono)[/dim]: ").strip()
    if not theme:
        theme = "A Santidade de Deus e a Visão do Trono Celestial"
        console.print(f"[dim]Usando padrão: {theme}[/dim]")

    biblical_ref = console.input("[bold cyan]Passagens Bíblicas de Base[/bold cyan] [dim](Ex: Isaías 6 e Apocalipse 4)[/dim]: ").strip()
    if not biblical_ref:
        biblical_ref = "Isaías 6:1-8 e Apocalipse 4:8-11"
        console.print(f"[dim]Usando padrão: {biblical_ref}[/dim]")

    style_hint = console.input("[bold cyan]Estilo Musical[/bold cyan] [dim](Ex: Modern Worship contemporâneo com piano e coral)[/dim]: ").strip()
    if not style_hint:
        style_hint = "Modern Worship congregacional solene, piano de cauda com crescendo para guitarras e coral épico"
        console.print(f"[dim]Usando padrão: {style_hint}[/dim]")

    briefing = UserBriefing(
        theme=theme,
        biblical_reference=biblical_ref,
        musical_style_hint=style_hint,
        tempo_hint="Lento (68-72 BPM) com grande crescendo para clímax",
        vocal_preference="Voz masculina emotiva com coral harmônico celestial"
    )

    console.print("\n[bold green]Iniciando orquestração dos agentes...[/bold green]\n")

    def status_logger(stage: str, msg: str):
        icons = {
            "THEOLOGY_START": "📜", "THEOLOGY_DONE": "✅",
            "LYRICS_START": "✍️", "LYRICS_DONE": "📝",
            "AUDIT_START": "⚖️", "AUDIT_PASS": "🌟", "AUDIT_RETRY": "🔄",
            "SUNO_START": "🎵", "SUNO_DONE": "🚀"
        }
        icon = icons.get(stage, "🔹")
        console.print(f"{icon} [bold cyan][{stage}][/bold cyan] {msg}")

    orchestrator = WorshipSunoOrchestrator(status_callback=status_logger)
    dossier, draft, report, package = orchestrator.execute(briefing)

    display_theological_dossier(dossier)
    display_audit_report(report)

    # Salva arquivo de saída
    output_path = Path(__file__).parent / "suno_output_pronto.txt"
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
    output_path.write_text(conteudo_salvar, encoding="utf-8")

    display_suno_package(package, output_file=output_path)
