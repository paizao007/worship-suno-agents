"""
Módulo de Schemas Pydantic para o Sistema Multiagente de Composição Sacra (Suno AI).
Define contratos estritos de dados trocados entre cada agente.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class UserBriefing(BaseModel):
    """Entrada inicial fornecida pelo usuário."""
    theme: str = Field(description="Tema central da canção (ex: Santidade de Deus, Graça e Redenção)")
    biblical_reference: Optional[str] = Field(
        default="",
        description="Passagens bíblicas de inspiração. Se vazio, o Teólogo selecionará as melhores referências canônicas automaticamente."
    )
    musical_style_hint: str = Field(
        default="Modern Worship contemporâneo",
        description="Estilo musical sugerido (ex: Hillsong moderno, Balada acústica, Épico orquestral, Black gospel)"
    )
    tempo_hint: Optional[str] = Field(
        default="Lento com crescendo para clímax épico",
        description="Sensação de andamento e dinâmica"
    )
    vocal_preference: Optional[str] = Field(
        default="Voz masculina emotiva ou dueto com coral",
        description="Preferência de arranjo vocal"
    )


class TheologicalDossier(BaseModel):
    """Saída produzida pelo Agente Teólogo & Exegeta."""
    theme_title: str = Field(description="Título conceitual da mensagem teológica")
    primary_scriptures: List[str] = Field(description="Textos bíblicos canônicos fundamentais")
    divine_attributes: List[str] = Field(description="Atributos de Deus enfatizados (ex: Santidade, Soberania, Misericórdia)")
    christocentric_focus: str = Field(description="Como a canção aponta para Cristo ou reflete o Evangelho")
    sacred_keywords: List[str] = Field(description="Palavras-chave e metáforas bíblicas ricas a serem usadas")
    doctrinal_guardrails: List[str] = Field(description="O que NÃO deve ser dito (para evitar heresias e antropocentrismo)")
    emotional_and_spiritual_tone: str = Field(description="Tom espiritual (ex: Reverente, Solene, Quebrantamento, Júbilo)")
    exegetical_summary: str = Field(description="Síntese teológica que guiará a composição poética")


class LyricSection(BaseModel):
    """Uma seção estrutural da letra (Verso, Refrão, etc.)."""
    tag: str = Field(description="Nome da seção (ex: Verse 1, Pre-Chorus, Chorus, Bridge, Outro)")
    lines: List[str] = Field(description="Linhas poéticas que compõem a seção")
    liturgical_purpose: str = Field(description="Propósito litúrgico da seção (ex: Confissão, Doxologia, Clímax)")


class SongDraft(BaseModel):
    """Rascunho poético completo gerado pelo Agente Compositor."""
    title: str = Field(description="Título proposto para a música")
    sections: List[LyricSection] = Field(description="Lista sequencial de seções da letra")
    meter_notes: str = Field(description="Observações sobre contagem silábica e ritmo para canto")
    rhyme_scheme: str = Field(description="Esquema e qualidade das rimas empregadas")


class AuditReport(BaseModel):
    """Parecer crítico elaborado pelo Agente Auditor Doutrinário & Métrico."""
    approved: bool = Field(description="Indica se a letra foi aprovada para a fase de sonorização")
    score: float = Field(description="Nota geral de 0.0 a 10.0 (Aprovação requer >= 8.5)")
    theological_fidelity_score: float = Field(description="Nota específica para integridade doutrinária (0.0 a 10.0)")
    poetic_prosody_score: float = Field(description="Nota específica para fluidez, métrica e cantabilidade (0.0 a 10.0)")
    strengths: List[str] = Field(description="Pontos fortes da letra atual")
    critiques: List[str] = Field(description="Problemas encontrados (desvios doutrinários, rimas pobres, sílabas truncadas)")
    actionable_revisions: List[str] = Field(
        default_factory=list,
        description="Instruções cirúrgicas de correção caso a letra tenha sido reprovada"
    )


class SunoSongPackage(BaseModel):
    """Entrega final otimizada para o Suno AI (Modo Custom)."""
    song_title: str = Field(description="Título final da canção")
    style_of_music: str = Field(
        description="Prompt de estilo para o campo 'Style of Music' do Suno (Máximo recomendado: 120-140 caracteres)"
    )
    lyrics_with_metatags: str = Field(
        description="Letra completa intercalada com metatags de produção musical entre colchetes [Tag]"
    )
    target_bpm: str = Field(description="Andamento sugerido (ex: 68-72 BPM)")
    vocal_configuration: str = Field(description="Configuração vocal sugerida para o Suno")
    theological_summary: str = Field(description="Resumo da base bíblica e espiritual da canção")
    suno_tips: List[str] = Field(description="Dicas práticas para gerar ou estender esta música no Suno")
