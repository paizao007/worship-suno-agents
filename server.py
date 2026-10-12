"""
Servidor Web e API REST do Sistema Multiagente de Adoração para Suno AI.
Fornece interface gráfica moderna no navegador e endpoints para composição automatizada.
Inspirado na arquitetura de servidores de ER0_DeV / Moltbook.
"""

import sys
import os
import argparse
import json
import urllib.request
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

# Histórico em memória de canções geradas nesta sessão
SESSION_HISTORY = []

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
        .container { max-width: 1200px; margin: 0 auto; }
        
        header { text-align: center; margin-bottom: 32px; border-bottom: 1px solid var(--border-color); padding-bottom: 24px; }
        header h1 { font-size: 2.2rem; color: var(--accent-gold); margin-bottom: 8px; }
        header p { color: var(--text-secondary); font-size: 1.1rem; }
        
        .status-bar { display: flex; gap: 16px; justify-content: center; margin-top: 16px; }
        .badge { padding: 6px 14px; border-radius: 20px; font-size: 0.85rem; font-weight: 600; display: inline-flex; align-items: center; gap: 6px; }
        .badge-gemini { background: rgba(88, 166, 255, 0.15); color: var(--accent-blue); border: 1px solid var(--accent-blue); }
        .badge-ollama { background: rgba(63, 185, 80, 0.15); color: var(--accent-green); border: 1px solid var(--accent-green); }
        
        .grid { display: grid; grid-template-columns: 380px 1fr; gap: 24px; }
        @media (max-width: 900px) { .grid { grid-template-columns: 1fr; } }
        
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
        
        .result-box { display: none; }
        .suno-field { background: var(--bg-primary); border: 1px solid var(--border-color); border-radius: 8px; padding: 16px; margin-bottom: 20px; position: relative; }
        .suno-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
        .suno-title { font-size: 0.95rem; font-weight: bold; color: var(--accent-blue); }
        .btn-copy {
            background: var(--bg-card); color: var(--text-primary); border: 1px solid var(--border-color);
            padding: 6px 12px; border-radius: 6px; font-size: 0.8rem; cursor: pointer; transition: 0.2s;
        }
        .btn-copy:hover { background: var(--accent-gold); color: #000; }
        
        pre { white-space: pre-wrap; font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace; font-size: 0.9rem; line-height: 1.5; color: #c9d1d9; }
        
        .tabs { display: flex; gap: 8px; margin-bottom: 16px; border-bottom: 1px solid var(--border-color); padding-bottom: 8px; }
        .tab-btn { background: none; border: none; color: var(--text-secondary); font-size: 0.95rem; font-weight: 600; padding: 6px 12px; cursor: pointer; border-radius: 6px; }
        .tab-btn.active { color: var(--accent-gold); background: var(--bg-card); }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        
        .score-pill { font-size: 1.2rem; font-weight: bold; color: var(--accent-green); margin-bottom: 12px; }
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
            </div>
        </header>

        <div class="grid">
            <!-- Coluna da Esquerda: Formulário de Briefing -->
            <div class="card">
                <h2>1. Briefing de Adoração</h2>
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

            <!-- Coluna da Direita: Resultados dos Agentes -->
            <div class="card">
                <h2>2. Cabine de Produção & Saída Suno AI</h2>
                <div id="placeholderMsg" style="text-align: center; padding: 60px 20px; color: var(--text-secondary);">
                    <p style="font-size: 1.1rem; margin-bottom: 8px;">Preencha o briefing ao lado e clique em <b>Compor Música</b>.</p>
                    <p style="font-size: 0.9rem;">Os 4 agentes trabalharão em cadeia com ciclo de validação doutrinária.</p>
                </div>

                <div class="result-box" id="resultBox">
                    <div class="tabs">
                        <button class="tab-btn active" onclick="switchTab('tabSuno')">🎵 Pacote Suno AI</button>
                        <button class="tab-btn" onclick="switchTab('tabTheology')">📜 Teologia & Exegese</button>
                        <button class="tab-btn" onclick="switchTab('tabAudit')">⚖️ Parecer do Auditor</button>
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
                </div>
            </div>
        </div>
    </div>

    <script>
        function switchTab(tabId) {
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            event.target.classList.add('active');
            document.getElementById(tabId).classList.add('active');
        }

        function copyText(elemId) {
            const text = document.getElementById(elemId).innerText;
            navigator.clipboard.writeText(text).then(() => {
                alert("Copiado com sucesso para a área de transferência!");
            });
        }

        document.getElementById('composeForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const submitBtn = document.getElementById('submitBtn');
            const stepper = document.getElementById('stepper');
            const placeholder = document.getElementById('placeholderMsg');
            const resultBox = document.getElementById('resultBox');

            submitBtn.disabled = true;
            submitBtn.innerText = "⏳ Orquestrando os Agentes...";
            stepper.style.display = "flex";
            placeholder.style.display = "none";
            resultBox.style.display = "none";

            const payload = {
                theme: document.getElementById('theme').value,
                biblical_reference: document.getElementById('biblical_ref').value,
                musical_style_hint: document.getElementById('musical_style').value,
                tempo_hint: document.getElementById('tempo_pref').value,
                vocal_preference: document.getElementById('vocal_pref').value
            };

            // Simulação visual dos steps
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
                    
                    // Preenche Suno
                    const pkg = data.suno_package;
                    document.getElementById('styleText').innerText = pkg.style_of_music;
                    document.getElementById('styleCharCount').innerText = pkg.style_of_music.length;
                    document.getElementById('lyricsText').innerText = pkg.lyrics_with_metatags;

                    // Preenche Teologia
                    const dos = data.dossier;
                    document.getElementById('theologyTitle').innerText = dos.theme_title;
                    document.getElementById('theologyAttributes').innerText = dos.divine_attributes.join(', ');
                    document.getElementById('theologyChrist').innerText = dos.christocentric_focus;
                    document.getElementById('theologyKeywords').innerText = dos.sacred_keywords.join(', ');
                    document.getElementById('theologyGuardrails').innerText = dos.doctrinal_guardrails.join(' | ');
                    document.getElementById('theologySummary').innerText = dos.exegetical_summary;

                    // Preenche Auditoria
                    const aud = data.audit;
                    document.getElementById('auditScore').innerText = `Nota Final: ${aud.score.toFixed(1)} / 10.0 (Aprovado)`;
                    document.getElementById('auditStrengths').innerHTML = aud.strengths.map(s => `<li>${s}</li>`).join('');
                    document.getElementById('auditCritiques').innerHTML = aud.critiques.map(c => `<li>${c}</li>`).join('');

                    resultBox.style.display = "block";
                } else {
                    alert("Erro ao processar composição: " + (data.error || "Desconhecido"));
                }
            } catch (err) {
                alert("Falha de conexão com o servidor: " + err);
            } finally {
                submitBtn.disabled = false;
                submitBtn.innerText = "⚡ Compor Música com Agentes";
            }
        });
    </script>
</body>
</html>
"""


@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML_TEMPLATE)


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

    result_payload = {
        "success": True,
        "dossier": dossier.model_dump(),
        "draft": draft.model_dump(),
        "audit": report.model_dump(),
        "suno_package": package.model_dump(),
    }
    SESSION_HISTORY.append(result_payload)
    return jsonify(result_payload)


def run_server(host=None, port=None):
    h = host or config.SERVER_HOST
    p = port or config.SERVER_PORT
    print("=" * 70)
    print("🕊️  BANDA LVS LITÚRGICA MULTIAGENTE & SUNO AI INICIADA 🎵")
    print(f"📡  Interface Web acessível em: http://localhost:{p}")
    print(f"🌐  Rede local / Host: http://{h}:{p}")
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
