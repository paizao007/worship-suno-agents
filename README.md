# 🕊️ Sistema Multiagente de Adoração Sacra para Suno AI 🎵

Um sistema colaborativo de agentes de Inteligência Artificial especializados em teologia bíblica, prosódia lírica e engenharia de áudio para composição de músicas de adoração cristã destinadas ao **Suno AI**.

Equipado com o mesmo ecossistema maduro de motores de IA do laboratório **ER0_DeV**:
- ✨ **Google Gemini Cloud API** (com chave configurada e fallback dinâmico entre modelos).
- 🦙 **Ollama Local & WSL** (com detecção automática de IP dinâmico do WSL Ubuntu para modelos como `deepseek-r1` e `qwen2.5-coder`).
- 🌐 **Servidor Web & API REST** com interface gráfica completa para rodar no navegador.

---

## 🏛️ A Equipe de Agentes (A "Banda Litúrgica")

1. **📜 Agente Teólogo & Exegeta**:
   - Extrai passagens bíblicas, define os atributos de Deus, estabelece o foco cristocêntrico e impõe salvaguardas doutrinárias (eliminando antropocentrismo e clichês vazios).
2. **✍️ Agente Poeta & Compositor Sacro**:
   - Transforma a teologia em poesia lírica com métrica adaptada ao canto em português, rimas nobres e progressão estrófica congregacional (`[Verse]`, `[Pre-Chorus]`, `[Chorus]`, `[Bridge]`, `[Outro]`).
3. **⚖️ Agente Auditor Doutrinário & Métrico**:
   - Atua no padrão **Actor-Critic** (Reflexão). Audita a ortodoxia, o ritmo silábico e a solenidade. Se a nota for inferior a 8.5/10, devolve ao compositor com instruções cirúrgicas de correção.
4. **🎵 Agente Diretor Musical & Engenheiro do Suno**:
   - Sintetiza o estilo em tags eficientes de áudio (máximo de 120-140 caracteres em inglês no campo *Style of Music*) e insere as metatags dinâmicas entre colchetes (`[Atmospheric Intro]`, `[Crescendo]`, `[Full Band Explosion]`, `[Acoustic Breakdown]`, `[Outro]`).

---

## 🚀 Como Iniciar e Rodar o Servidor Web ("Rodar o Serv")

### 1. No Windows (1 Clique)
Basta clicar duas vezes em **`iniciar_servidor.bat`** ou executar no PowerShell:

```powershell
.\iniciar_servidor.bat
```

Ou diretamente pelo Python:
```powershell
.\.venv\Scripts\python.exe server.py --port 5005
```

### 2. No Linux / WSL
```bash
chmod +x iniciar_servidor.sh
./iniciar_servidor.sh 5005
```

O servidor abrirá em:
👉 **`http://localhost:5005`**

A interface web inclui:
- Formulário intuitivo de briefing (Tema bíblico, escrituras, estilo e vocais).
- Painel ao vivo mostrando os 4 agentes em ação.
- Botão de 1 clique para **Copiar Style of Music** e **Copiar Letra Completa com Metatags**.
- Abas com a fundamentação teológica e o relatório de notas do auditor.

---

## 💻 Como Rodar via Linha de Comando (CLI Interativo)

Se preferir o terminal interativo com painéis coloridos:

```powershell
.\.venv\Scripts\python.exe main.py
```

---

## 🔑 Configuração dos Motores LLM (.env)

O arquivo `.env` já vem pré-configurado com as credenciais do seu ambiente:

```env
# Google Gemini Cloud API
GEMINI_API_KEY=AIzaSyCMxfBdnRZJt6RvIxh2FWSV8xMSrEwCRUs
GEMINI_MODEL=gemini-flash-latest

# Motor Ollama Local / WSL (Detectado automaticamente)
OLLAMA_MODEL=deepseek-r1:1.5b
OLLAMA_FALLBACK_MODEL=deepseek-r1:7b

# Servidor Web
SERVER_PORT=5005
SERVER_HOST=0.0.0.0
```

---

## 🎛️ Como Usar o Resultado no Suno AI

1. Acesse o [Suno AI](https://suno.com) e clique em **Create**.
2. Ative a chave **Custom** (Modo Personalizado).
3. No campo **Style of Music**: cole o conteúdo exato gerado (ex: `modern worship, CCM, grand piano, celestial choir, swelling guitars, slow build, cinematic`).
4. No campo **Lyrics**: cole a letra completa com todas as metatags `[Tag]` preservadas.
5. Clique em **Create** para gerar a música de adoração!
