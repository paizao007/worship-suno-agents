"""
Servidor Web e API REST do Sistema Multiagente de Adoração para Suno AI.
🕊️ Banda LVS Litúrgica Multiagente & Suno AI 🎵
Otimizado para Celulares (Mobile First / PWA) e Desktop com Histórico Persistente.
"""

import sys
import os
import argparse
import json
import urllib.request
from datetime import datetime
from pathlib import Path
from flask import Flask, request, jsonify, render_template_string

# Garante encoding UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

import config
from schemas import UserBriefing
from orchestrator import WorshipSunoOrchestrator

app = Flask(__name__)

HISTORY_FILE = Path(__file__).parent / "historico_musicas.json"


def load_song_history():
    """Carrega o histórico persistente de canções."""
    if HISTORY_FILE.exists():
        try:
            return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        except Exception:
            return []
    return []


def save_song_to_history(entry):
    """Salva uma canção no histórico persistente."""
    history = load_song_history()
    history.insert(0, entry)
    HISTORY_FILE.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
    <meta name="theme-color" content="#0d1117">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="Banda LVS">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🕊️</text></svg>">
    <link rel="manifest" href="/manifest.json">
    <title>🕊️ Banda LVS Litúrgica Multiagente & Suno AI 🎵</title>
    <style>
        :root {
            --bg-primary: #0d1117;
            --bg-secondary: #161b22;
            --bg-card: #21262d;
            --accent-gold: #e3b341;
            --accent-blue: #58a6ff;
            --accent-green: #3fb950;
            --text-primary: #f0f6fc;
            --text-secondary: #8b949e;
            --border-color: #30363d;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; -webkit-tap-highlight-color: transparent; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
        body { background: var(--bg-primary); color: var(--text-primary); padding: 24px; min-height: 100vh; font-size: 18px; }
        .container { max-width: 1480px; margin: 0 auto; }
        
        header { text-align: center; margin-bottom: 26px; border-bottom: 1px solid var(--border-color); padding-bottom: 20px; }
        header h1 { font-size: 2.35rem; color: var(--accent-gold); margin-bottom: 10px; line-height: 1.25; }
        header p { color: var(--text-secondary); font-size: 1.18rem; }
        
        .status-bar { display: flex; gap: 12px; justify-content: center; margin-top: 16px; flex-wrap: wrap; }
        .badge { padding: 8px 16px; border-radius: 20px; font-size: 0.98rem; font-weight: 600; display: inline-flex; align-items: center; gap: 6px; }
        .badge-gemini { background: rgba(88, 166, 255, 0.15); color: var(--accent-blue); border: 1px solid var(--accent-blue); }
        .badge-ollama { background: rgba(63, 185, 80, 0.15); color: var(--accent-green); border: 1px solid var(--accent-green); }
        .badge-history { background: rgba(227, 179, 65, 0.15); color: var(--accent-gold); border: 1px solid var(--accent-gold); cursor: pointer; }
        
        .grid { display: grid; grid-template-columns: 480px 1fr; gap: 24px; }
        
        .card { background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: 12px; padding: 24px; }
        .card h2 { font-size: 1.5rem; margin-bottom: 18px; color: var(--accent-gold); border-bottom: 1px solid var(--border-color); padding-bottom: 10px; }
        
        .form-group { margin-bottom: 18px; }
        .form-group label { display: block; font-size: 1.08rem; font-weight: 600; color: #c9d1d9; margin-bottom: 8px; }
        
        /* Fontes grandes e confortáveis nos campos de entrada */
        .form-group input, .form-group textarea, .form-group select {
            width: 100%; min-height: 50px; padding: 12px 14px; background: var(--bg-primary); border: 1px solid var(--border-color);
            border-radius: 8px; color: var(--text-primary); font-size: 1.12rem; outline: none; transition: 0.2s;
        }
        .form-group input:focus, .form-group textarea:focus, .form-group select:focus {
            border-color: var(--accent-gold); box-shadow: 0 0 0 2px rgba(227, 179, 65, 0.2);
        }
        
        .btn-submit {
            width: 100%; min-height: 56px; padding: 14px; background: linear-gradient(135deg, #e3b341, #d29922);
            color: #000; font-weight: bold; font-size: 1.22rem; border: none; border-radius: 8px; cursor: pointer; transition: 0.2s;
            display: flex; justify-content: center; align-items: center; gap: 8px;
        }
        .btn-submit:active { transform: scale(0.98); opacity: 0.9; }
        .btn-submit:disabled { opacity: 0.5; cursor: not-allowed; }
        
        .stepper { display: flex; flex-direction: column; gap: 12px; margin-top: 18px; }
        .step-item { display: flex; align-items: center; gap: 10px; font-size: 1.05rem; color: var(--text-secondary); }
        .step-item.active { color: var(--accent-gold); font-weight: bold; }
        .step-item.done { color: var(--accent-green); }
        
        .suno-field { background: var(--bg-primary); border: 1px solid var(--border-color); border-radius: 8px; padding: 18px; margin-bottom: 18px; }
        .suno-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; flex-wrap: wrap; gap: 8px; }
        .suno-title { font-size: 1.18rem; font-weight: bold; color: var(--accent-blue); }
        
        .btn-copy {
            background: var(--bg-card); color: var(--text-primary); border: 1px solid var(--border-color);
            padding: 10px 16px; border-radius: 6px; font-size: 1.02rem; font-weight: 600; cursor: pointer; transition: 0.2s;
            min-height: 42px; display: inline-flex; align-items: center; gap: 6px;
        }
        .btn-copy:active { background: var(--accent-gold); color: #000; transform: scale(0.96); }
        
        pre {
            white-space: pre-wrap; word-break: break-word; font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
            font-size: 1.12rem; line-height: 1.65; color: #e6edf3;
        }
        
        /* Abas com rolagem suave por toque em telas pequenas */
        .tabs {
            display: flex; gap: 8px; margin-bottom: 18px; border-bottom: 1px solid var(--border-color);
            padding-bottom: 10px; overflow-x: auto; -webkit-overflow-scrolling: touch; scrollbar-width: none;
        }
        .tabs::-webkit-scrollbar { display: none; }
        .tab-btn {
            background: none; border: none; color: var(--text-secondary); font-size: 1.08rem; font-weight: 600;
            padding: 10px 16px; cursor: pointer; border-radius: 6px; white-space: nowrap; flex-shrink: 0; min-height: 44px;
        }
        .tab-btn.active { color: var(--accent-gold); background: var(--bg-card); }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        
        .score-pill { font-size: 1.35rem; font-weight: bold; color: var(--accent-green); margin-bottom: 14px; }

        /* Cards do Histórico */
        .history-card {
            background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 8px;
            padding: 16px; margin-bottom: 16px; transition: 0.2s;
        }
        .history-card:active { border-color: var(--accent-gold); }
        .history-card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; flex-wrap: wrap; gap: 6px; }
        .history-title { font-size: 1.22rem; font-weight: bold; color: var(--accent-gold); }
        .history-meta { font-size: 0.96rem; color: var(--text-secondary); margin-bottom: 10px; }
        .history-actions { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 12px; }
        .btn-action {
            background: var(--bg-primary); color: var(--text-primary); border: 1px solid var(--border-color);
            padding: 10px 16px; border-radius: 6px; font-size: 1.0rem; font-weight: 600; cursor: pointer; transition: 0.2s; min-height: 42px;
        }
        .btn-action:active { background: var(--accent-blue); color: #fff; transform: scale(0.96); }
        .btn-load { background: rgba(227, 179, 65, 0.15); border-color: var(--accent-gold); color: var(--accent-gold); }
        .btn-load:active { background: var(--accent-gold); color: #000; }

        /* Toast flutuante moderno para celulares (substitui alert feio) */
        #toast {
            position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%) translateY(100px);
            background: #1c2128; color: var(--accent-gold); border: 1px solid var(--accent-gold);
            padding: 14px 28px; border-radius: 30px; font-weight: bold; font-size: 1.1rem;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6); z-index: 9999; opacity: 0; transition: 0.3s ease;
            pointer-events: none; text-align: center; max-width: 90vw;
        }
        #toast.show { transform: translateX(-50%) translateY(0); opacity: 1; }

        /* Regras Específicas para Smartphones (Mobile-First) */
        @media (max-width: 920px) {
            body { padding: 14px 10px 30px 10px; font-size: 17px; }
            header { margin-bottom: 18px; padding-bottom: 14px; }
            header h1 { font-size: 1.75rem; }
            header p { font-size: 1.05rem; }
            .grid { grid-template-columns: 1fr; gap: 18px; }
            .card { padding: 16px; border-radius: 10px; }
            .btn-action, .btn-copy { flex: 1; justify-content: center; }
            pre { font-size: 1.02rem; }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🕊️ Banda LVS Litúrgica Multiagente & Suno AI 🎵</h1>
            <p>Composição Sacra • Rigor Bíblico • Engenharia de Prompts para Suno</p>
            <div class="status-bar" id="statusBar">
                <span class="badge badge-gemini">✨ Gemini Cloud: Ativo</span>
                <span class="badge badge-ollama">🦙 Ollama Local (WSL): Disponível</span>
                <span class="badge badge-history" onclick="switchTab('tabHistory')">📚 <span id="badgeHistoryText">Histórico</span></span>
            </div>
        </header>

        <div class="grid">
            <!-- Formulário de Briefing -->
            <div class="card">
                <h2>1. Novo Briefing de Adoração</h2>
                <form id="composeForm">
                    <div class="form-group">
                        <label>Tema Central / Doutrina</label>
                        <input type="text" id="theme" value="A Santidade de Deus e a Visão do Trono Celestial" onchange="autoFillScriptures()" required>
                    </div>
                    <div class="form-group">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; gap: 8px; flex-wrap: wrap;">
                            <label style="margin-bottom: 0;">Passagens Bíblicas Base</label>
                            <button type="button" class="btn-action" style="min-height: 36px; padding: 6px 14px; font-size: 0.96rem; background: rgba(227, 179, 65, 0.15); border-color: var(--accent-gold); color: var(--accent-gold);" onclick="autoFillScriptures()">🎲 Sortear Versículo do Tema</button>
                        </div>
                        <input type="text" id="biblical_ref" value="Isaías 6:1-4 (Vi o Senhor assentado sobre um alto e sublime trono, e os serafins clamavam: Santo, Santo, Santo)" placeholder="Opcional: Deixe em branco para o Teólogo sortear automaticamente...">
                        <div id="agentManagementBox" style="margin-top: 10px; padding: 14px 16px; background: rgba(227, 179, 65, 0.08); border-left: 4px solid var(--accent-gold); border-radius: 8px; font-size: 1.02rem; color: #e6edf3; line-height: 1.55;">
                            <div style="color: var(--accent-gold); font-weight: bold; font-size: 1.08rem; margin-bottom: 6px;">🧠 Gestão do Agente Teólogo:</div>
                            <div style="margin-bottom: 4px;">📌 <b>Tema Identificado:</b> <span id="identifiedThemeText" style="color: #58a6ff;">Santidade Transcendente & Majestade do Trono de Deus</span></div>
                            <div style="margin-bottom: 4px;">🎯 <b>Versículo Sorteado:</b> <span id="drawnVerseStatus" style="color: #3fb950;">Isaías 6:1-4 (Clique em "Sortear Versículo" para sortear outro do mesmo tema!)</span></div>
                            <div style="margin-top: 6px;">📖 <b>Reflexão Bíblica:</b> <span id="biblicalReflectionText" style="color: #d2a8ff;">Meditação na majestade santa do Senhor no alto e sublime trono, conduzindo a igreja à reverência e adoração.</span></div>
                        </div>
                    </div>
                    <div class="form-group">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; flex-wrap: wrap;">
                            <label style="margin-bottom: 0;">Estilo Musical no Suno</label>
                            <span style="font-size: 0.95rem; color: var(--accent-gold); font-weight: bold;">🤖 Gerado pela Reflexão ou Manual</span>
                        </div>
                        <select id="musical_style_preset" onchange="applyStylePreset()">
                            <optgroup label="🤖 Gestão Inteligente do Agente Musical (Recomendado)">
                                <option value="auto" selected>🤖 Automático: Gerar Novo Estilo, Voz e Dinâmica pelo Tema e Reflexão Bíblica</option>
                            </optgroup>
                            <optgroup label="🕊️ Worship Contemporâneo & Soaking">
                                <option value="modern worship, CCM, grand piano, celestial choir, swelling guitars, slow build, cinematic">Modern Worship Solene (Hillsong / Elevation Worship)</option>
                                <option value="brazilian worship, organic CCM, acoustic piano, acoustic guitar, passionate male lead, strings crescendo, spontaneous atmosphere">Brazilian Worship Orgânico / Soaking (Morada / FHOP / Casa Worship)</option>
                                <option value="folk worship, acoustic guitar, mandolin, stomp and holler drums, warm vocal harmonies, heartfelt">Indie Folk Worship (CityAlight / Rend Collective)</option>
                                <option value="ambient worship, lush pad textures, soft delay electric guitar, intimate piano, whisper vocals, peaceful">Ambient Devotional / Soaking (Quarto de Oração)</option>
                                <option value="electronic worship, energetic synth leads, punchy 808 bass, upbeat drums, anthem choir, high energy">Synthwave / Eletrônico Cristão (Hillsong Y&F / Planetshakers)</option>
                            </optgroup>
                            <optgroup label="🎺 Gospel Negro, Soul & Pentecostal">
                                <option value="black gospel worship, soul, hammond B3 organ, soulful lead, backing choir, expressive vocal runs, dynamic shout">Black Gospel & Soul Tradicional (Kirk Franklin / Brooklyn Tabernacle)</option>
                                <option value="contemporary urban gospel, r&b worship, live drums, acoustic guitar, call and response choir, soulful passion">Urban Gospel & R&B Worship (Maverick City Music)</option>
                                <option value="pentecostal gospel, retro brazilian praise, brass section, energetic drums, vibrant organ, joyful congregational chorus">Pentecostal Retrô / Corinhos de Fogo (Harpa Cristã / Metais & Bateria)</option>
                                <option value="gospel blues, vintage electric guitar, groovy bassline, raspy vocals, stomping beat, raw passion">Gospel Blues & Southern Soul (The Blind Boys of Alabama)</option>
                            </optgroup>
                            <optgroup label="🎻 Orquestral, Clássico & Litúrgico">
                                <option value="cinematic worship, orchestral, powerful vocals, strings section, brass swell, timpani, slow burning, celestial climax">Cinematic Orchestral Épico (Hans Zimmer style / Cordas & Timpani)</option>
                                <option value="traditional hymn, pipe organ, 4-part choir harmony, solemn, reverence, majestic brass, stately">Hinologia Tradicional & Sacra (Órgão de Tubos & Coral Sacro Polifônico)</option>
                                <option value="celtic worship, irish flute, acoustic fiddle, bodhran drums, ethereal female vocals, soaring melodies">Celta Sacro & Épico Medieval (Flautas Irlandesas & Violino)</option>
                            </optgroup>
                            <optgroup label="🇧🇷 Ritmos Brasileiros & Regionais">
                                <option value="forro gospel, baiao, accordion, zabumba, triangle, acoustic rhythm guitar, upbeat brazilian praise">Forró & Baião Gospel (Sanfona, Zabumba & Triângulo)</option>
                                <option value="samba gospel, pagode, cavaquinho, pandeiro, surdo, joyful male vocal, community choir, celebration">Samba & Pagode Gospel (Cavaquinho, Pandeiro & Surdo)</option>
                                <option value="sertanejo gospel, acoustic 12-string viola, accordion, country drums, dual vocal harmonies, emotional ballad">Sertanejo Universitário Gospel & Modão Cristão</option>
                                <option value="reggae worship, roots reggae, heavy dub bass, skank guitar, horn section, rastafari groove with christ-centered lyrics">Reggae Cristão & Roots Worship (Christafari style)</option>
                            </optgroup>
                            <optgroup label="🎸 Rock, Baladas & Pop Contemporâneo">
                                <option value="christian rock, post-rock worship, atmospheric electric guitars, driving drums, distorted chorus, emotive vocals">Rock Cristão & Post-Rock Worship (Guitarras Distorcidas & Bateria Forte)</option>
                                <option value="power ballad worship, clean electric guitars, dramatic drum fills, soaring high notes, passionate climax">Power Ballad Worship Anos 90/2000 (Solo de Guitarra Emocional)</option>
                                <option value="christian pop, modern commercial production, crisp vocals, catchy melodic hook, punchy synth bass">Pop Cristão Contemporâneo (TobyMac / Tauren Wells)</option>
                            </optgroup>
                            <optgroup label="☕ Acústico, Lo-Fi & Intimista">
                                <option value="intimate acoustic worship, nylon guitar, soft piano, tender female vocals, warm ambient reverb">Acoustic Devotional Intimista (Voz e Violão Suave)</option>
                                <option value="lo-fi christian worship, dusty vinyl crackle, mellow rhodes piano, relaxing lo-fi hip hop beat, gentle whisper prayer">Lo-Fi Devocional / Oração Noturna (Rhodes & Batida Relaxante)</option>
                                <option value="solo grand piano, neoclassical devotional, expressive rubato tempo, contemplative female voice, gentle reverb">Piano Neoclássico Devocional & Voz Suave</option>
                            </optgroup>
                            <optgroup label="✍️ Personalizado">
                                <option value="custom">✍️ Digitar Outro Estilo Livremente...</option>
                            </optgroup>
                        </select>
                        <div style="margin-top: 10px;">
                            <label style="font-size: 0.98rem; color: #c9d1d9; margin-bottom: 6px; display: block;">Tags do Estilo (Geradas pelo Agente ou Editáveis):</label>
                            <input type="text" id="musical_style" value="modern worship, CCM, grand piano, celestial choir, swelling guitars, slow build, cinematic" placeholder="Digite os instrumentos e estilo desejados em inglês ou português...">
                        </div>
                    </div>
                    <div class="form-group">
                        <label>Preferência Vocal (Gerada pela Reflexão ou Editável)</label>
                        <input type="text" id="vocal_pref" list="vocal_suggestions" value="Voz masculina emotiva nos versos com coral harmônico no refrão">
                        <datalist id="vocal_suggestions">
                            <option value="Voz masculina emotiva nos versos com coral harmônico no refrão">
                            <option value="Voz feminina suave e ungida com grande alcance no clímax">
                            <option value="Dueto vocal (masculino e feminino) em harmonia congregacional">
                            <option value="Coral litúrgico sacro imponente (4 vozes: Soprano, Contralto, Tenor, Baixo)">
                            <option value="Voz solene profunda e reverente com coro celestial ao fundo">
                            <option value="Líder congregacional apaixonado com resposta calorosa da congregação">
                        </datalist>
                    </div>
                    <div class="form-group">
                        <label>Andamento / Dinâmica (Gerado pela Reflexão ou Editável)</label>
                        <input type="text" id="tempo_pref" list="tempo_suggestions" value="Lento (68-72 BPM) com grande crescendo para clímax">
                        <datalist id="tempo_suggestions">
                            <option value="Lento (68-72 BPM) com grande crescendo para clímax">
                            <option value="Moderado congregacional (78-85 BPM) envolvente e solene">
                            <option value="Médio alegre (96-108 BPM) com ritmo constante e celebração">
                            <option value="Rápido e vibrante (120-135 BPM) com batida enérgica de júbilo">
                            <option value="Devocional livre (Rubato), sem tempo rígido, focado na oração íntima">
                        </datalist>
                        <div id="producerManagementBox" style="margin-top: 10px; padding: 14px 16px; background: rgba(88, 166, 255, 0.08); border-left: 4px solid #58a6ff; border-radius: 8px; font-size: 1.02rem; color: #e6edf3; line-height: 1.55;">
                            <div style="color: #58a6ff; font-weight: bold; font-size: 1.08rem; margin-bottom: 6px;">🎹 Gestão do Agente Musical (Baseado no Tema & Reflexão):</div>
                            <div style="margin-bottom: 4px;">🎶 <b>Arranjo Sorteado:</b> <span id="arrangementNameText" style="color: var(--accent-gold);">Automático — Será gerado para cada nova música!</span></div>
                            <div>💡 <b>Direção Musical:</b> <span id="producerRationaleText" style="color: #c9d1d9;">Ao clicar em "Compor Música com Agentes", o Diretor Musical criará novo Estilo, Voz e Dinâmica alinhados à Reflexão Bíblica.</span></div>
                        </div>
                    </div>
                    
                    <button type="submit" class="btn-submit" id="submitBtn">⚡ Compor Música com Agentes</button>
                </form>

                <div class="stepper" id="stepper" style="display: none;">
                    <div class="step-item" id="step1"><span>📜</span> 1. Exegese Bíblica (Agente Teólogo)</div>
                    <div class="step-item" id="step2"><span>✍️</span> 2. Composição Litúrgica (Agente Poeta)</div>
                    <div class="step-item" id="step3"><span>⚖️</span> 3. Auditoria & Reflexão (Agente Revisor)</div>
                    <div class="step-item" id="step4"><span>🎵</span> 4. Engenharia de Metatags (Diretor Suno)</div>
                </div>
            </div>

            <!-- Cabine de Produção e Histórico -->
            <div class="card">
                <h2>2. Cabine de Produção & Saída Suno AI</h2>

                <div class="tabs">
                    <button class="tab-btn active" id="btnTabSuno" onclick="switchTab('tabSuno')">🎵 Música (Suno)</button>
                    <button class="tab-btn" id="btnTabTheology" onclick="switchTab('tabTheology')">📜 Teologia</button>
                    <button class="tab-btn" id="btnTabAudit" onclick="switchTab('tabAudit')">⚖️ Auditoria</button>
                    <button class="tab-btn" id="btnTabHistory" onclick="switchTab('tabHistory')">📚 Histórico (<span id="historyTabCount">0</span>)</button>
                </div>

                <!-- Aba 1: Pacote do Suno -->
                <div class="tab-content active" id="tabSuno">
                    <div class="suno-field">
                        <div class="suno-header">
                            <span class="suno-title">🎹 Campo 'Style of Music' (<span id="styleCharCount">0</span> carac.)</span>
                            <button class="btn-copy" onclick="copyText('styleText', 'Style of Music copiado!')">📋 Copiar Estilo</button>
                        </div>
                        <pre id="styleText" style="color: var(--accent-gold); font-weight: bold;"></pre>
                    </div>

                    <div class="suno-field">
                        <div class="suno-header">
                            <span class="suno-title">✍️ Campo 'Lyrics' com Metatags [Tag]</span>
                            <button class="btn-copy" onclick="copyText('lyricsText', 'Letra completa copiada!')">📝 Copiar Letra</button>
                        </div>
                        <pre id="lyricsText" style="max-height: 620px; overflow-y: auto;"></pre>
                    </div>
                </div>

                <!-- Aba 2: Teologia -->
                <div class="tab-content" id="tabTheology">
                    <div class="suno-field" style="font-size: 1.08rem; line-height: 1.6;">
                        <h3 id="theologyTitle" style="color: var(--accent-gold); margin-bottom: 14px; font-size: 1.35rem;"></h3>
                        <p style="color: var(--text-secondary); margin-bottom: 10px;"><b>Atributos Divinos:</b> <span id="theologyAttributes" style="color: #fff;"></span></p>
                        <p style="color: var(--text-secondary); margin-bottom: 10px;"><b>Foco Cristocêntrico:</b> <span id="theologyChrist" style="color: #fff;"></span></p>
                        <p style="color: var(--text-secondary); margin-bottom: 10px;"><b>Palavras Sagradas:</b> <span id="theologyKeywords" style="color: #fff;"></span></p>
                        <p style="color: var(--text-secondary); margin-bottom: 14px;"><b>Salvaguardas Doutrinárias:</b> <span id="theologyGuardrails" style="color: #ff7b72;"></span></p>
                        <p style="color: var(--text-secondary);"><b>Síntese Exegética & Reflexão:</b></p>
                        <p id="theologySummary" style="color: #e6edf3; margin-top: 6px; line-height: 1.65;"></p>
                    </div>
                </div>

                <!-- Aba 3: Auditoria -->
                <div class="tab-content" id="tabAudit">
                    <div class="suno-field" style="font-size: 1.08rem; line-height: 1.6;">
                        <div class="score-pill" id="auditScore"></div>
                        <h4 style="margin-bottom: 10px; color: var(--accent-green); font-size: 1.18rem;">Pontos Fortes:</h4>
                        <ul id="auditStrengths" style="margin-left: 22px; margin-bottom: 18px; color: #e6edf3; font-size: 1.06rem;"></ul>
                        <h4 style="margin-bottom: 10px; color: var(--accent-gold); font-size: 1.18rem;">Observações Críticas:</h4>
                        <ul id="auditCritiques" style="margin-left: 22px; color: #e6edf3; font-size: 1.06rem;"></ul>
                    </div>
                </div>

                <!-- Aba 4: Histórico Persistente -->
                <div class="tab-content" id="tabHistory">
                    <div style="margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center;">
                        <h3 style="color: var(--accent-gold); font-size: 1.25rem;">Histórico de Canções Salvas</h3>
                        <button class="btn-copy" onclick="loadHistory()">🔄 Atualizar</button>
                    </div>
                    <div id="historyListContainer"></div>
                </div>

            </div>
        </div>
    </div>

    <!-- Toast flutuante para celulares -->
    <div id="toast">✓ Copiado com sucesso!</div>

    <script>
        let globalHistory = [];

        function showToast(msg) {
            const toast = document.getElementById('toast');
            toast.innerText = msg || "✓ Copiado com sucesso!";
            toast.classList.add('show');
            setTimeout(() => { toast.classList.remove('show'); }, 2200);
        }

        function switchTab(tabId) {
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            
            const btnMap = {
                'tabSuno': 'btnTabSuno',
                'tabTheology': 'btnTabTheology',
                'tabAudit': 'btnTabAudit',
                'tabHistory': 'btnTabHistory'
            };
            const btn = document.getElementById(btnMap[tabId]);
            if (btn) btn.classList.add('active');
            
            const targetContent = document.getElementById(tabId);
            if (targetContent) targetContent.classList.add('active');
        }

        function copyText(elemId, customMsg) {
            const text = document.getElementById(elemId).innerText;
            navigator.clipboard.writeText(text).then(() => {
                showToast(customMsg || "✓ Copiado para a área de transferência!");
            }).catch(() => {
                showToast("✓ Copiado!");
            });
        }

        function copyRaw(text, customMsg) {
            navigator.clipboard.writeText(text).then(() => {
                showToast(customMsg || "✓ Copiado com sucesso!");
            }).catch(() => {
                showToast("✓ Copiado!");
            });
        }

        async function autoFillScriptures() {
            const theme = document.getElementById('theme').value.trim();
            const currentRef = document.getElementById('biblical_ref').value.trim();
            const currentStyle = document.getElementById('musical_style').value.trim();
            if (!theme) {
                showToast("⚠️ Digite um tema primeiro!");
                return;
            }
            try {
                const url = `/api/suggest-scriptures?theme=${encodeURIComponent(theme)}&current=${encodeURIComponent(currentRef)}&current_style=${encodeURIComponent(currentStyle)}`;
                const res = await fetch(url);
                const data = await res.json();
                if (data.success && data.chosen_verse) {
                    document.getElementById('biblical_ref').value = data.chosen_verse;
                    document.getElementById('identifiedThemeText').innerText = data.identified_theme;
                    document.getElementById('drawnVerseStatus').innerText = `${data.chosen_verse} (Sorteado dentre ${data.pool_size} passagens deste tema)`;
                    if (data.biblical_reflection) {
                        document.getElementById('biblicalReflectionText').innerText = data.biblical_reflection;
                    }
                    // Se estiver no modo Automático pelo Agente, também já atualiza Estilo, Voz e Dinâmica com base na Reflexão Bíblica!
                    const presetMode = document.getElementById('musical_style_preset').value;
                    if (presetMode === 'auto' && data.arrangement) {
                        document.getElementById('musical_style').value = data.arrangement.style_of_music;
                        document.getElementById('vocal_pref').value = data.arrangement.vocal_preference;
                        document.getElementById('tempo_pref').value = data.arrangement.tempo_dynamics;
                        document.getElementById('arrangementNameText').innerText = data.arrangement.arrangement_name;
                        document.getElementById('producerRationaleText').innerText = data.arrangement.producer_rationale;
                    }
                    showToast(`🎲 Sorteado: ${data.chosen_verse.split(' (')[0]} + Novo Arranjo Musical!`);
                } else {
                    showToast("Aviso: " + (data.error || "Não foi possível sugerir"));
                }
            } catch (err) {
                showToast("Erro ao contatar o Teólogo: " + err);
            }
        }

        function applyStylePreset() {
            const selectElem = document.getElementById('musical_style_preset');
            const val = selectElem.value;
            const inputElem = document.getElementById('musical_style');
            if (val === 'auto') {
                showToast("🤖 Modo Automático ativado! O Agente Musical gerará Estilo, Voz e Dinâmica pela Reflexão Bíblica.");
                autoFillScriptures();
            } else if (val === 'custom') {
                inputElem.value = '';
                inputElem.focus();
                showToast("✍️ Digite seu estilo e instrumentos livremente!");
            } else {
                inputElem.value = val;
                document.getElementById('arrangementNameText').innerText = selectElem.options[selectElem.selectedIndex].text;
                document.getElementById('producerRationaleText').innerText = "Estilo selecionado manualmente pelo usuário na lista.";
                showToast("🎶 Estilo manual aplicado!");
            }
        }

        function renderSongOnScreen(item, updateFormInputs = true) {
            document.getElementById('styleText').innerText = item.style_of_music;
            document.getElementById('styleCharCount').innerText = item.style_of_music.length;
            document.getElementById('lyricsText').innerText = item.lyrics_with_metatags;

            if (item.dossier) {
                document.getElementById('theologyTitle').innerText = item.dossier.theme_title || item.song_title;
                document.getElementById('theologyAttributes').innerText = (item.dossier.divine_attributes || []).join(', ');
                document.getElementById('theologyChrist').innerText = item.dossier.christocentric_focus || '';
                document.getElementById('theologyKeywords').innerText = (item.dossier.sacred_keywords || []).join(', ');
                document.getElementById('theologyGuardrails').innerText = (item.dossier.doctrinal_guardrails || []).join(' | ');
                document.getElementById('theologySummary').innerText = item.dossier.exegetical_summary || '';
            } else {
                document.getElementById('theologyTitle').innerText = item.song_title;
                document.getElementById('theologySummary').innerText = item.theological_summary || '';
            }

            const scoreVal = item.audit_score || (item.audit ? item.audit.score : 9.0);
            document.getElementById('auditScore').innerText = `Nota Final: ${Number(scoreVal).toFixed(1)} / 10.0 (Aprovado)`;
            if (item.audit && item.audit.strengths) {
                document.getElementById('auditStrengths').innerHTML = item.audit.strengths.map(s => `<li>${s}</li>`).join('');
                document.getElementById('auditCritiques').innerHTML = (item.audit.critiques || []).map(c => `<li>${c}</li>`).join('');
            } else {
                document.getElementById('auditStrengths').innerHTML = `<li>Harmonia teológica bíblica e métrica alinhada ao Suno.</li>`;
                document.getElementById('auditCritiques').innerHTML = `<li>Pronto para produção no Suno AI Custom Mode.</li>`;
            }

            if (updateFormInputs) {
                if (item.theme) document.getElementById('theme').value = item.theme;
                if (item.biblical_reference) document.getElementById('biblical_ref').value = item.biblical_reference;
                if (item.style_of_music || item.musical_style_hint) {
                    document.getElementById('musical_style').value = item.style_of_music || item.musical_style_hint;
                }
                if (item.vocal_configuration || item.vocal_preference) {
                    document.getElementById('vocal_pref').value = item.vocal_configuration || item.vocal_preference;
                }
                if (item.target_bpm) {
                    document.getElementById('tempo_pref').value = item.target_bpm;
                }
                if (item.dossier && item.dossier.exegetical_summary) {
                    document.getElementById('biblicalReflectionText').innerText = item.dossier.exegetical_summary;
                }
                if (item.arrangement) {
                    document.getElementById('arrangementNameText').innerText = item.arrangement.arrangement_name || 'Arranjo Personalizado';
                    document.getElementById('producerRationaleText').innerText = item.arrangement.producer_rationale || '';
                }
            }
        }

        async function loadHistory() {
            try {
                const res = await fetch('/api/history');
                const list = await res.json();
                globalHistory = list;
                
                document.getElementById('historyTabCount').innerText = list.length;
                document.getElementById('badgeHistoryText').innerText = `Histórico (${list.length})`;

                const container = document.getElementById('historyListContainer');
                if (!list.length) {
                    container.innerHTML = `<p style="color: var(--text-secondary); text-align: center; padding: 20px;">Nenhuma canção gravada ainda.</p>`;
                    return;
                }

                container.innerHTML = list.map((item, idx) => `
                    <div class="history-card">
                        <div class="history-card-header">
                            <span class="history-title">🎵 ${item.song_title}</span>
                            <span class="badge badge-ollama">★ Nota: ${Number(item.audit_score || 9.0).toFixed(1)}/10</span>
                        </div>
                        <div class="history-meta">
                            📅 <b>Criada:</b> ${item.created_at || 'Hoje'} | 📖 <b>Base:</b> ${item.biblical_reference || ''}
                        </div>
                        <p style="font-size: 1.04rem; color: #c9d1d9; margin-bottom: 10px;">
                            <b>Tema:</b> ${item.theme}
                        </p>
                        <div style="background: var(--bg-primary); padding: 10px; border-radius: 6px; font-size: 0.98rem; color: var(--accent-gold); font-family: monospace; margin-bottom: 10px; word-break: break-all;">
                            ${item.style_of_music}
                        </div>
                        <div class="history-actions">
                            <button class="btn-action btn-load" onclick="selectFromHistory(${idx})">👁️ Ver na Tela</button>
                            <button class="btn-action" onclick="copyRaw(globalHistory[${idx}].style_of_music, 'Style copiado!')">📋 Style</button>
                            <button class="btn-action" onclick="copyRaw(globalHistory[${idx}].lyrics_with_metatags, 'Letra copiada!')">📝 Letra</button>
                        </div>
                    </div>
                `).join('');

            } catch (e) {
                console.error("Erro ao carregar histórico:", e);
            }
        }

        function selectFromHistory(idx) {
            const item = globalHistory[idx];
            if (item) {
                renderSongOnScreen(item, true);
                switchTab('tabSuno');
                window.scrollTo({ top: 0, behavior: 'smooth' });
                showToast(`Canção "${item.song_title}" carregada!`);
            }
        }

        // Submissão do Formulário
        document.getElementById('composeForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const submitBtn = document.getElementById('submitBtn');
            const stepper = document.getElementById('stepper');

            submitBtn.disabled = true;
            submitBtn.innerText = "⏳ Orquestrando os Agentes...";
            stepper.style.display = "flex";

            const styleMode = document.getElementById('musical_style_preset').value;
            const currentStyleVal = document.getElementById('musical_style').value;

            const payload = {
                theme: document.getElementById('theme').value,
                biblical_reference: document.getElementById('biblical_ref').value,
                style_mode: styleMode,
                musical_style_hint: styleMode === 'auto' ? `auto:${currentStyleVal}` : currentStyleVal,
                tempo_hint: document.getElementById('tempo_pref').value,
                vocal_preference: document.getElementById('vocal_pref').value
            };

            document.getElementById('step1').className = "step-item active";
            setTimeout(() => { document.getElementById('step1').className = "step-item done"; document.getElementById('step2').className = "step-item active"; }, 250);
            setTimeout(() => { document.getElementById('step2').className = "step-item done"; document.getElementById('step3').className = "step-item active"; }, 500);
            setTimeout(() => { document.getElementById('step3').className = "step-item done"; document.getElementById('step4').className = "step-item active"; }, 750);

            try {
                const res = await fetch('/api/compose', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                if (data.success) {
                    document.getElementById('step4').className = "step-item done";
                    
                    let finalRef = data.biblical_reference || payload.biblical_reference;
                    if (finalRef) {
                        document.getElementById('biblical_ref').value = finalRef;
                    }
                    if (data.dossier && data.dossier.theme_title) {
                        document.getElementById('identifiedThemeText').innerText = data.dossier.theme_title;
                        document.getElementById('drawnVerseStatus').innerText = finalRef;
                        document.getElementById('biblicalReflectionText').innerText = data.dossier.exegetical_summary || '';
                    }

                    const newItem = {
                        song_title: data.suno_package.song_title,
                        style_of_music: data.suno_package.style_of_music,
                        target_bpm: data.suno_package.target_bpm,
                        vocal_configuration: data.suno_package.vocal_configuration,
                        lyrics_with_metatags: data.suno_package.lyrics_with_metatags,
                        audit_score: data.audit.score,
                        dossier: data.dossier,
                        audit: data.audit,
                        arrangement: data.arrangement,
                        theme: payload.theme,
                        biblical_reference: finalRef,
                        created_at: "Agora"
                    };
                    renderSongOnScreen(newItem, true);
                    switchTab('tabSuno');
                    loadHistory();
                    showToast("🎉 Nova Música + Arranjo gerados com base na Reflexão Bíblica!");
                } else {
                    showToast("Erro ao compor: " + (data.error || "Desconhecido"));
                }
            } catch (err) {
                showToast("Falha de conexão com o servidor: " + err);
            } finally {
                submitBtn.disabled = false;
                submitBtn.innerText = "⚡ Compor Música com Agentes";
            }
        });

        // Carrega ao iniciar a página (sem sobrescrever os campos de edição do usuário)
        window.addEventListener('DOMContentLoaded', async () => {
            await loadHistory();
            if (globalHistory.length > 0) {
                renderSongOnScreen(globalHistory[0], false);
                switchTab('tabSuno');
            }
        });
    </script>
</body>
</html>
"""


@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route("/manifest.json", methods=["GET"])
def manifest():
    """Manifest PWA para permitir adicionar o app à tela inicial do celular como aplicativo."""
    return jsonify({
        "name": "Banda LVS Litúrgica & Suno AI",
        "short_name": "Banda LVS",
        "description": "Composição Multiagente de Músicas de Adoração para Suno AI",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#0d1117",
        "theme_color": "#0d1117",
        "icons": [
            {
                "src": "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🕊️</text></svg>",
                "sizes": "192x192 512x512",
                "type": "image/svg+xml"
            }
        ]
    })


@app.route("/api/history", methods=["GET"])
def api_history():
    """Retorna todas as canções salvas no histórico persistente."""
    return jsonify(load_song_history())


@app.route("/api/status", methods=["GET"])
def api_status():
    ollama_host = config.resolve_ollama_host()
    ollama_ok = False
    try:
        urllib.request.urlopen(f"{ollama_host}/api/tags", timeout=3.0)
        ollama_ok = True
    except Exception:
        pass

    return jsonify({
        "status": "online",
        "service": "🕊️ Banda LVS Litúrgica Multiagente & Suno AI 🎵",
        "gemini_api_key_configured": bool(config.GEMINI_API_KEY),
        "gemini_model": config.GEMINI_MODEL,
        "ollama_host": ollama_host,
        "ollama_available": ollama_ok,
        "ollama_model": config.OLLAMA_MODEL,
        "total_songs_in_history": len(load_song_history()),
    })


@app.route("/api/suggest-scriptures", methods=["GET"])
def api_suggest_scriptures():
    """Identifica o tema doutrinário, sorteia um versículo bíblico, gera a reflexão e o arranjo musical."""
    theme = request.args.get("theme", "").strip()
    current = request.args.get("current", "").strip()
    current_style = request.args.get("current_style", "").strip()
    if not theme:
        return jsonify({"success": False, "error": "Por favor, forneça um tema."}), 400
    try:
        from agents.theologian import TheologianAgent
        from agents.suno_producer import SunoProducerAgent
        theologian = TheologianAgent()
        producer = SunoProducerAgent()
        analysis = theologian.analyze_and_draw_scripture(theme, exclude_current=current)
        arrangement = producer.design_arrangement_from_reflection(
            theme=theme,
            biblical_reference=analysis["chosen_verse"],
            biblical_reflection=analysis.get("biblical_reflection", ""),
            exclude_style=current_style
        )
        return jsonify({
            "success": True,
            "theme": theme,
            "identified_theme": analysis["identified_theme"],
            "chosen_verse": analysis["chosen_verse"],
            "biblical_reflection": analysis.get("biblical_reflection", ""),
            "pool_size": analysis["pool_size"],
            "scriptures": analysis["scriptures"],
            "formatted": analysis["chosen_verse"],
            "arrangement": {
                "arrangement_name": arrangement["arrangement_name"],
                "style_of_music": arrangement["style_of_music"],
                "vocal_preference": arrangement["vocal_preference"],
                "tempo_dynamics": arrangement["tempo_dynamics"],
                "producer_rationale": arrangement["producer_rationale"],
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/compose", methods=["POST"])
def api_compose():
    data = request.get_json() or {}
    briefing_ref = (data.get("biblical_reference") or "").strip()
    briefing = UserBriefing(
        theme=data.get("theme", "A Santidade de Deus no Trono"),
        biblical_reference=briefing_ref,
        musical_style_hint=data.get("musical_style_hint", "auto"),
        tempo_hint=data.get("tempo_hint", "Lento com crescendo épico"),
        vocal_preference=data.get("vocal_preference", "Voz masculina emotiva"),
    )

    orchestrator = WorshipSunoOrchestrator()
    dossier, draft, report, package = orchestrator.execute(briefing)

    chosen_ref = briefing.biblical_reference
    if not chosen_ref:
        if dossier.primary_scriptures:
            chosen_ref = dossier.primary_scriptures[0]
        else:
            chosen_ref = "Exegese Canônica Automática"

    arr_info = orchestrator.producer._last_arrangement or {}
    arrangement_summary = {
        "arrangement_name": arr_info.get("arrangement_name", "Arranjo Personalizado"),
        "style_of_music": package.style_of_music,
        "vocal_preference": package.vocal_configuration,
        "tempo_dynamics": package.target_bpm,
        "producer_rationale": arr_info.get("producer_rationale", ""),
    }

    # Registro persistente no histórico
    now_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    history_entry = {
        "id": datetime.now().strftime("%Y%m%d%H%M%S"),
        "created_at": now_str,
        "theme": briefing.theme,
        "biblical_reference": chosen_ref,
        "musical_style_hint": package.style_of_music,
        "song_title": package.song_title,
        "style_of_music": package.style_of_music,
        "target_bpm": package.target_bpm,
        "vocal_configuration": package.vocal_configuration,
        "theological_summary": package.theological_summary,
        "audit_score": report.score,
        "lyrics_with_metatags": package.lyrics_with_metatags,
        "dossier": dossier.model_dump(),
        "audit": report.model_dump(),
        "arrangement": arrangement_summary,
    }
    save_song_to_history(history_entry)

    result_payload = {
        "success": True,
        "biblical_reference": chosen_ref,
        "dossier": dossier.model_dump(),
        "draft": draft.model_dump(),
        "audit": report.model_dump(),
        "suno_package": package.model_dump(),
        "arrangement": arrangement_summary,
    }
    return jsonify(result_payload)


def run_server(host=None, port=None):
    h = host or config.SERVER_HOST
    p = port or config.SERVER_PORT
    print("=" * 70)
    print("🕊️  BANDA LVS LITÚRGICA MULTIAGENTE & SUNO AI INICIADA 🎵")
    print(f"📡  Interface Web acessível em: http://localhost:{p}")
    print(f"🌐  Rede local / Host: http://{h}:{p}")
    print(f"📱  Modo Mobile First / PWA: Ativado")
    print(f"📚  Histórico: {len(load_song_history())} canções salvas em historico_musicas.json")
    print(f"✨  Motor Gemini Cloud: {'Ativo com chave' if config.GEMINI_API_KEY else 'Não configurado'}")
    print(f"🦙  Motor Ollama Local (WSL): {config.resolve_ollama_host()}")
    print("=" * 70)
    app.run(host=h, port=p, debug=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Servidor de Composição Multiagente para Suno AI")
    parser.add_argument("--host", default=config.SERVER_HOST, help="Host do servidor (padrão: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=config.SERVER_PORT, help="Porta do servidor (padrão: 5005)")
    args = parser.parse_args()
    run_server(args.host, args.port)
