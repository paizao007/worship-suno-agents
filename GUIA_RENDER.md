# 🌐 Guia Passo a Passo: Como Subir no Render (render.com)
### 🕊️ Banda LVS Litúrgica Multiagente & Suno AI 🎵

Este guia ensina como colocar a **Banda LVS Litúrgica Multiagente & Suno AI** no ar na nuvem usando o plano gratuito do **Render**.

---

## 📋 Arquivos Já Preparados no Projeto

O projeto já contém todos os arquivos necessários para o Render:
1. **`Procfile`**: Define o comando de inicialização em produção com WSGI (`web: gunicorn server:app`).
2. **`render.yaml`**: Blueprint com todas as configurações do serviço pré-definidas.
3. **`requirements.txt`**: Inclui `gunicorn`, `flask`, `pydantic`, `requests`, etc.
4. **`.gitignore`**: Impede que a sua chave do `.env` ou pastas pesadas (`.venv`) sejam enviadas publicamente para o Git.

---

## 🚀 Passo a Passo para Deploy

### Passo 1: Inicializar o Repositório Git Local e Enviar para o GitHub

No seu terminal (dentro da pasta `worship-suno-agents`), inicialize o Git e envie para a sua conta do GitHub:

```powershell
git init
git add .
git commit -m "feat: multiagent worship suno system with web UI"
```

Crie um novo repositório no seu GitHub (ex: `worship-suno-agents`) e vincule:

```powershell
git remote add origin https://github.com/SEU_USUARIO/worship-suno-agents.git
git branch -M main
git push -u origin main
```

---

### Passo 2: Criar a Conta e o Serviço no Render

1. Acesse **[https://render.com](https://render.com)** e faça login com a sua conta do **GitHub**.
2. No painel principal (Dashboard), clique no botão **New +** no canto superior direito e selecione **Web Service**.
3. Selecione a opção **"Build and deploy from a Git repository"** e clique em **Next**.
4. Conecte e selecione o repositório **`worship-suno-agents`** que você acabou de subir.

---

### Passo 3: Configurar os Parâmetros do Serviço

Preencha os campos da seguinte forma:

- **Name**: `worship-suno-agents` (ou o nome que preferir)
- **Region**: Qualquer uma (ex: *Oregon (US West)* ou *Frankfurt (EU)*)
- **Branch**: `main`
- **Root Directory**: Deixe em branco (raiz)
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn server:app`
- **Instance Type**: Selecione **Free** ($0/mês).

---

### Passo 4: Configurar as Variáveis de Ambiente (Environment Variables)

Ainda na tela de criação (ou na aba **Environment** após criar), adicione as chaves:

| Key (Chave) | Value (Valor) |
| :--- | :--- |
| `GEMINI_API_KEY` | `AIzaSyCMxfBdnRZJt6RvIxh2FWSV8xMSrEwCRUs` |
| `GEMINI_MODEL` | `gemini-flash-latest` |
| `PYTHON_VERSION` | `3.12.0` |

> [!NOTE]
> No ambiente de nuvem do Render, as requisições utilizam a **Google Gemini Cloud API**. Caso a API esteja em limite de cota, o motor ativa automaticamente o **Fallback Contextual**, garantindo que a aplicação nunca fique fora do ar.

---

### Passo 5: Concluir e Acessar

1. Clique em **Create Web Service** no final da página.
2. O Render iniciará a instalação (`pip install`) e iniciará o Gunicorn.
3. Em cerca de 1 a 2 minutos, o status mudará para **Live** (Verde).
4. O Render fornecerá uma URL pública HTTPS gratuita, como:
   👉 `https://worship-suno-agents.onrender.com`

Pronto! Qualquer pessoa poderá acessar a interface pelo navegador, compor músicas de adoração e copiar os dados diretamente para o Suno AI!
