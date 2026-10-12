"""
Servidor Web e API REST do Sistema Multiagente de Adoração para Suno AI.
🕊️ Banda LVS Litúrgica Multiagente & Suno AI 🎵
Inclui interface gráfica moderna, histórico persistente de canções e endpoints de composição.
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
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
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
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
        body { background: var(--bg-primary); color: var(--text-primary); padding: 24px; }
        .container { max-width: 1280px; margin: 0 auto; }
        
        header { text-align: center; margin-bottom: 32px; border-bottom: 1px solid var(--border-color); padding-bottom: 24px; }
        header h1 { font-size: 2.2rem; color: var(--accent-gold); margin-bottom: 8px; }
        header p { color: var(--text-secondary); font-size: 1.1rem; }
        
        .status-bar { display: flex; gap: 16px; justify-content: center; margin-top: 16px; flex-wrap: wrap; }
        .badge { padding: 6px 14px; border-radius: 20px; font-size: 0.85rem; font-weight: 600; display: inline-flex; align-items: center; gap: 6px; }
        .badge-gemini { background: rgba(88, 166, 255, 0.15); color: var(--accent-blue); border: 1px solid var(--accent-blue); }
        .badge-ollama { background: rgba(63, 185, 80, 0.15); color: var(--accent-green); border: 1px solid var(--accent-green); }
        .badge-history { background: rgba(227, 179, 65, 0.15); color: var(--accent-gold); border: 1px solid var(--accent-gold); cursor: pointer; }
        
        .grid { display: grid; grid-template-columns: 380px 1fr; gap: 24px; }
        @media (max-width: 960px) { .grid { grid-template-columns: 1fr; } }
        
        .card { background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: 12px; padding: 24px; }
        .card h2 { font-size: 1.3rem; margin-bottom: 16px; color: var(--accent-gold); border-bottom: 1px solid var(--border-color); padding-bottom: 8px; }
        
        .form-group { margin-bottom: 16px; }
        .form-group label { display: block; font-size: 0.9rem; font-weight: 600; color: var(--text-secondary); margin-bottom: 6px; }
        .form-group input, .form-group textarea, .form-group select {
            width: 100%; padding: 10px 12px; background: var(--bg-primary); border: 1px solid var(--border-color);
            border-radius: 6px; color: var(--text-primary); font-size: 0.95rem; outline: none; transition: 0.2s;
        }
        .form-group input:focus, .form-group textarea:focus { border-color: var(--accent-gold); box-shadow: 0 0 0 2px rgba(227, 179, 65, 0.2); }
        
        .btn-submit {
            width: 100%; padding: 14px; background: linear-gradient(135deg, #e3b341, #d29922);
            color: #000; font-weight: bold; font-size: 1.05rem; border: none; border-radius: 8px; cursor: pointer; transition: 0.2s;
        }
        .btn-submit:hover { opacity: 0.9; transform: translateY(-1px); }
        .btn-submit:disabled { opacity: 0.5; cursor: not-allowed; }
        
        .stepper { display: flex; flex-direction: column; gap: 12px; margin-top: 20px; }
        .step-item { display: flex; align-items: center; gap: 10px; font-size: 0.9rem; color: var(--text-secondary); }
        .step-item.active { color: var(--accent-gold); font-weight: bold; }
        .step-item.done { color: var(--accent-green); }
        
        .suno-field { background: var(--bg-primary); border: 1px solid var(--border-color); border-radius: 8px; padding: 16px; margin-bottom: 20px; position: relative; }
        .suno-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
        .suno-title { font-size: 0.95rem; font-weight: bold; color: var(--accent-blue); }
        .btn-copy {
            background: var(--bg-card); color: var(--text-primary); border: 1px solid var(--border-color);
            padding: 6px 12px; border-radius: 6px; font-size: 0.8rem; cursor: pointer; transition: 0.2s;
        }
        .btn-copy:hover { background: var(--accent-gold); color: #000; }
        
        pre { white-space: pre-wrap; font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace; font-size: 0.9rem; line-height: 1.5; color: #c9d1d9; }
        
        .tabs { display: flex; gap: 8px; margin-bottom: 16px; border-bottom: 1px solid var(--border-color); padding-bottom: 8px; flex-wrap: wrap; }
        .tab-btn { background: none; border: none; color: var(--text-secondary); font-size: 0.95rem; font-weight: 600; padding: 8px 14px; cursor: pointer; border-radius: 6px; }
        .tab-btn.active { color: var(--accent-gold); background: var(--bg-card); }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        
        .score-pill { font-size: 1.2rem; font-weight: bold; color: var(--accent-green); margin-bottom: 12px; }

        /* Estilos do Histórico */
        .history-card {
            background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 8px;
            padding: 16px; margin-bottom: 16px; transition: 0.2s;
        }
        .history-card:hover { border-color: var(--accent-gold); }
        .history-card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
        .history-title { font-size: 1.1rem; font-weight: bold; color: var(--accent-gold); }
        .history-meta { font-size: 0.8rem; color: var(--text-secondary); margin-bottom: 12px; }
        .history-actions { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 12px; }
        .btn-action {
            background: var(--bg-primary); color: var(--text-primary); border: 1px solid var(--border-color);
            padding: 6px 10px; border-radius: 6px; font-size: 0.8rem; cursor: pointer; transition: 0.2s;
        }
        .btn-action:hover { background: var(--accent-blue); color: #fff; }
        .btn-load { background: rgba(227, 179, 65, 0.2); border-color: var(--accent-gold); color: var(--accent-gold); }
        .btn-load:hover { background: var(--accent-gold); color: #000; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🕊️ Banda LVS Litúrgica Multiagente & Suno AI 🎵</h1>
            <p>Orquestração de Agentes para Composição Sacra • Rigor Bíblico • Engenharia de Prompts</p>
            <div class="status-bar" id="statusBar">
                <span class="badge badge-gemini">✨ Gemini Cloud: Ativo</span>
                <span class="badge badge-ollama">🦙 Ollama Local (WSL): Disponível</span>
                <span class="badge badge-history" onclick="switchTab('tabHistory')">📚 <span id="badgeHistoryText">Histórico de Músicas</span></span>
            </div>
        </header>

        <div class="grid">
            <!-- Coluna da Esquerda: Formulário de Briefing -->
            <div class="card">
                <h2>1. Novo Briefing de Adoração</h2>
                <form id="composeForm">
                    <div class="form-group">
                        <label>Tema Central / Doutrina</label>
                        <input type="text" id="theme" value="A Santidade de Deus e a Visão do Trono Celestial" required>
                    </div>
                    <div class="form-group">
                        <label>Passagens Bíblicas Base</label>
                        <input type="text" id="biblical_ref" value="Isaías 6:1-8 e Apocalipse 4:8-11" required>
                    </div>
                    <div class="form-group">
                        <label>Estilo Musical no Suno</label>
                        <select id="musical_style">
                            <option value="modern worship, CCM, grand piano, celestial choir, swelling guitars, slow build, cinematic">Modern Worship Solene (Estilo Hillsong/Elevation)</option>
                            <option value="brazilian worship, organic CCM, acoustic piano, acoustic guitar, passionate male lead, strings crescendo">Brazilian Worship Orgânico (Estilo Morada/FHOP)</option>
                            <option value="cinematic worship, orchestral, powerful female vocals, strings section, timpani, slow burning, celestial climax">Cinematic Orchestral Épico (Cordas e Tímpanos)</option>
                            <option value="black gospel worship, soul, hammond B3 organ, soulful lead, backing choir, expressive">Black Gospel & Soul Worship (Órgão Hammond & Coral)</option>
                            <option value="intimate acoustic worship, nylon guitar, soft piano, tender female vocals, warm ambient reverb">Acoustic Devotional Intimista (Voz e Violão)</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Preferência Vocal</label>
                        <input type="text" id="vocal_pref" value="Voz masculina emotiva nos versos com coral harmônico no refrão">
                    </div>
                    <div class="form-group">
                        <label>Andamento / Dinâmica</label>
                        <input type="text" id="tempo_pref" value="Lento (68-72 BPM) com grande crescendo para clímax">
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

            <!-- Coluna da Direita: Resultados e Histórico -->
            <div class="card">
                <h2>2. Cabine de Produção & Histórico de Músicas</h2>

                <div class="tabs">
                    <button class="tab-btn active" id="btnTabSuno" onclick="switchTab('tabSuno')">🎵 Música (Suno AI)</button>
                    <button class="tab-btn" id="btnTabTheology" onclick="switchTab('tabTheology')">📜 Teologia & Exegese</button>
                    <button class="tab-btn" id="btnTabAudit" onclick="switchTab('tabAudit')">⚖️ Parecer do Auditor</button>
                    <button class="tab-btn" id="btnTabHistory" onclick="switchTab('tabHistory')">📚 Histórico (<span id="historyTabCount">0</span>)</button>
                </div>

                <!-- Aba 1: Pacote do Suno -->
                <div class="tab-content active" id="tabSuno">
                    <div class="suno-field">
                        <div class="suno-header">
                            <span class="suno-title">🎹 Campo 'Style of Music' (<span id="styleCharCount">0</span> caracteres)</span>
                            <button class="btn-copy" onclick="copyText('styleText')">Copiar Estilo</button>
                        </div>
                        <pre id="styleText" style="color: var(--accent-gold); font-weight: bold;"></pre>
                    </div>

                    <div class="suno-field">
                        <div class="suno-header">
                            <span class="suno-title">✍️ Campo 'Lyrics' com Metatags [Tag]</span>
                            <button class="btn-copy" onclick="copyText('lyricsText')">Copiar Letra Completa</button>
                        </div>
                        <pre id="lyricsText" style="max-height: 480px; overflow-y: auto;"></pre>
                    </div>
                </div>

                <!-- Aba 2: Teologia -->
                <div class="tab-content" id="tabTheology">
                    <div class="suno-field">
                        <h3 id="theologyTitle" style="color: var(--accent-gold); margin-bottom: 12px;"></h3>
                        <p style="color: var(--text-secondary); margin-bottom: 8px;"><b>Atributos Divinos:</b> <span id="theologyAttributes" style="color: #fff;"></span></p>
                        <p style="color: var(--text-secondary); margin-bottom: 8px;"><b>Foco Cristocêntrico:</b> <span id="theologyChrist" style="color: #fff;"></span></p>
                        <p style="color: var(--text-secondary); margin-bottom: 8px;"><b>Palavras Sagradas:</b> <span id="theologyKeywords" style="color: #fff;"></span></p>
                        <p style="color: var(--text-secondary); margin-bottom: 12px;"><b>Salvaguardas Doutrinárias:</b> <span id="theologyGuardrails" style="color: #ff7b72;"></span></p>
                        <p style="color: var(--text-secondary);"><b>Síntese Exegética:</b></p>
                        <p id="theologySummary" style="color: #c9d1d9; margin-top: 4px; line-height: 1.5;"></p>
                    </div>
                </div>

                <!-- Aba 3: Auditoria -->
                <div class="tab-content" id="tabAudit">
                    <div class="suno-field">
                        <div class="score-pill" id="auditScore"></div>
                        <h4 style="margin-bottom: 8px; color: var(--accent-green);">Pontos Fortes:</h4>
                        <ul id="auditStrengths" style="margin-left: 20px; margin-bottom: 16px; color: #c9d1d9;"></ul>
                        <h4 style="margin-bottom: 8px; color: var(--accent-gold);">Observações Críticas:</h4>
                        <ul id="auditCritiques" style="margin-left: 20px; color: #c9d1d9;"></ul>
                    </div>
                </div>

                <!-- Aba 4: Histórico Persistente -->
                <div class="tab-content" id="tabHistory">
                    <div style="margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center;">
                        <h3 style="color: var(--accent-gold);">Histórico de Canções Criadas</h3>
                        <button class="btn-copy" onclick="loadHistory()">🔄 Atualizar</button>
                    </div>
                    <div id="historyListContainer">
                        <!-- Cards injetados via JavaScript -->
                    </div>
                </div>

            </div>
        </div>
    </div>

    <script>
        let globalHistory = [];

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

        function copyText(elemId) {
            const text = document.getElementById(elemId).innerText;
            navigator.clipboard.writeText(text).then(() => {
                alert("Copiado com sucesso para a área de transferência!");
            });
        }

        function copyRaw(text) {
            navigator.clipboard.writeText(text).then(() => {
                alert("Copiado com sucesso!");
            });
        }

        function renderSongOnScreen(item) {
            // Renderiza na aba Suno
            document.getElementById('styleText').innerText = item.style_of_music;
            document.getElementById('styleCharCount').innerText = item.style_of_music.length;
            document.getElementById('lyricsText').innerText = item.lyrics_with_metatags;

            // Renderiza Teologia
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

            // Renderiza Auditoria
            const scoreVal = item.audit_score || (item.audit ? item.audit.score : 9.0);
            document.getElementById('auditScore').innerText = `Nota Final: ${Number(scoreVal).toFixed(1)} / 10.0 (Aprovado)`;
            if (item.audit && item.audit.strengths) {
                document.getElementById('auditStrengths').innerHTML = item.audit.strengths.map(s => `<li>${s}</li>`).join('');
                document.getElementById('auditCritiques').innerHTML = (item.audit.critiques || []).map(c => `<li>${c}</li>`).join('');
            } else {
                document.getElementById('auditStrengths').innerHTML = `<li>Harmonia teológica bíblica e métrica alinhada ao Suno.</li>`;
                document.getElementById('auditCritiques').innerHTML = `<li>Pronto para produção no Suno AI Custom Mode.</li>`;
            }

            // Atualiza campos do formulário para referência
            if (item.theme) document.getElementById('theme').value = item.theme;
            if (item.biblical_reference) document.getElementById('biblical_ref').value = item.biblical_reference;
        }

        async function loadHistory() {
            try {
                const res = await fetch('/api/history');
                const list = await res.json();
                globalHistory = list;
                
                document.getElementById('historyTabCount').innerText = list.length;
                document.getElementById('badgeHistoryText').innerText = `Histórico de Músicas (${list.length})`;

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
                            📅 <b>Criada em:</b> ${item.created_at || 'Hoje'} | 📖 <b>Base:</b> ${item.biblical_reference || ''}
                        </div>
                        <p style="font-size: 0.85rem; color: #8b949e; margin-bottom: 8px;">
                            <b>Tema:</b> ${item.theme}
                        </p>
                        <div style="background: var(--bg-primary); padding: 8px; border-radius: 6px; font-size: 0.8rem; color: var(--accent-gold); font-family: monospace; margin-bottom: 8px;">
                            ${item.style_of_music}
                        </div>
                        <div class="history-actions">
                            <button class="btn-action btn-load" onclick="selectFromHistory(${idx})">👁️ Carregar na Tela</button>
                            <button class="btn-action" onclick="copyRaw(globalHistory[${idx}].style_of_music)">📋 Copiar Style</button>
                            <button class="btn-action" onclick="copyRaw(globalHistory[${idx}].lyrics_with_metatags)">📝 Copiar Letra</button>
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
                renderSongOnScreen(item);
                switchTab('tabSuno');
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

            const payload = {
                theme: document.getElementById('theme').value,
                biblical_reference: document.getElementById('biblical_ref').value,
                musical_style_hint: document.getElementById('musical_style').value,
                tempo_hint: document.getElementById('tempo_pref').value,
                vocal_preference: document.getElementById('vocal_pref').value
            };

            // Animação visual dos steps
            document.getElementById('step1').className = "step-item active";
            setTimeout(() => { document.getElementById('step1').className = "step-item done"; document.getElementById('step2').className = "step-item active"; }, 600);
            setTimeout(() => { document.getElementById('step2').className = "step-item done"; document.getElementById('step3').className = "step-item active"; }, 1200);
            setTimeout(() => { document.getElementById('step3').className = "step-item done"; document.getElementById('step4').className = "step-item active"; }, 1800);

            try {
                const res = await fetch('/api/compose', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                if (data.success) {
                    document.getElementById('step4').className = "step-item done";
                    
                    const newItem = {
                        song_title: data.suno_package.song_title,
                        style_of_music: data.suno_package.style_of_music,
                        lyrics_with_metatags: data.suno_package.lyrics_with_metatags,
                        audit_score: data.audit.score,
                        dossier: data.dossier,
                        audit: data.audit,
                        theme: payload.theme,
                        biblical_reference: payload.biblical_reference,
                        created_at: "Agora"
                    };
                    renderSongOnScreen(newItem);
                    switchTab('tabSuno');
                    loadHistory();
                } else {
                    alert("Erro ao compor: " + (data.error || "Desconhecido"));
                }
            } catch (err) {
                alert("Falha de conexão com o servidor: " + err);
            } finally {
                submitBtn.disabled = false;
                submitBtn.innerText = "⚡ Compor Música com Agentes";
            }
        });

        // Carrega ao iniciar a página
        window.addEventListener('DOMContentLoaded', async () => {
            await loadHistory();
            if (globalHistory.length > 0) {
                // Carrega a primeira música do histórico por padrão na tela
                renderSongOnScreen(globalHistory[0]);
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


@app.route("/api/compose", methods=["POST"])
def api_compose():
    data = request.get_json() or {}
    briefing = UserBriefing(
        theme=data.get("theme", "A Santidade de Deus no Trono"),
        biblical_reference=data.get("biblical_reference", "Isaías 6 e Apocalipse 4"),
        musical_style_hint=data.get("musical_style_hint", "Modern Worship"),
        tempo_hint=data.get("tempo_hint", "Lento com crescendo épico"),
        vocal_preference=data.get("vocal_preference", "Voz masculina emotiva"),
    )

    orchestrator = WorshipSunoOrchestrator()
    dossier, draft, report, package = orchestrator.execute(briefing)

    # Registro persistente no histórico
    now_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    history_entry = {
        "id": datetime.now().strftime("%Y%m%d%H%M%S"),
        "created_at": now_str,
        "theme": briefing.theme,
        "biblical_reference": briefing.biblical_reference,
        "musical_style_hint": briefing.musical_style_hint,
        "song_title": package.song_title,
        "style_of_music": package.style_of_music,
        "target_bpm": package.target_bpm,
        "vocal_configuration": package.vocal_configuration,
        "theological_summary": package.theological_summary,
        "audit_score": report.score,
        "lyrics_with_metatags": package.lyrics_with_metatags,
        "dossier": dossier.model_dump(),
        "audit": report.model_dump(),
    }
    save_song_to_history(history_entry)

    result_payload = {
        "success": True,
        "dossier": dossier.model_dump(),
        "draft": draft.model_dump(),
        "audit": report.model_dump(),
        "suno_package": package.model_dump(),
    }
    return jsonify(result_payload)


def run_server(host=None, port=None):
    h = host or config.SERVER_HOST
    p = port or config.SERVER_PORT
    print("=" * 70)
    print("🕊️  BANDA LVS LITÚRGICA MULTIAGENTE & SUNO AI INICIADA 🎵")
    print(f"📡  Interface Web acessível em: http://localhost:{p}")
    print(f"🌐  Rede local / Host: http://{h}:{p}")
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
