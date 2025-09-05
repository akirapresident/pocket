# 🎯 Instagram Analytics Platform

Uma plataforma completa para análise de conteúdo do Instagram com backend Python + frontend React.

## 🚀 **Status do Projeto**

**MICROFASE 1.1 ✅ CONCLUÍDA**
- ✅ Estrutura Clean Architecture
- ✅ FastAPI configurado e funcionando
- ✅ Banco de dados SQLAlchemy
- ✅ Coleta de dados do Instagram via Apify
- ✅ Transcrição de áudio com Whisper
- ✅ Cálculo de taxas de engajamento
- ✅ API REST completa

## 📁 **Estrutura do Projeto**

```
instagram-analytics/
├── backend/                    # Backend Python + FastAPI
│   ├── app/
│   │   ├── models/            # Modelos SQLAlchemy
│   │   ├── routers/           # Endpoints da API
│   │   ├── services/          # Lógica de negócio
│   │   ├── schemas/           # Validação Pydantic
│   │   └── utils/             # Utilitários
│   ├── requirements.txt       # Dependências Python
│   └── init_db.py            # Inicialização do banco
├── IMPLEMENTATION_PLAN.md     # Plano de implementação
└── README.md                  # Este arquivo
```

## 🛠️ **Tecnologias Utilizadas**

### **Backend:**
- **FastAPI** - Framework web moderno
- **SQLAlchemy** - ORM para banco de dados
- **SQLite** - Banco de dados (desenvolvimento)
- **Apify API** - Scraping do Instagram
- **OpenAI Whisper** - Transcrição de áudio
- **FFmpeg** - Processamento de vídeo/áudio

### **APIs Externas:**
- **Apify Instagram Scraper** - Coleta de dados
- **YouTube Data API v3** - Dados do YouTube (futuro)

## 🚀 **Como Executar**

### **1. Instalar Dependências**
```bash
cd backend
pip install -r requirements.txt
```

### **2. Inicializar Banco de Dados**
```bash
python init_db.py
```

### **3. Executar API**
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### **4. Acessar Documentação**
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

## 📊 **Endpoints Disponíveis**

### **Vídeos**
- `GET /api/v1/videos/` - Listar vídeos
- `POST /api/v1/videos/scrape?url=...` - Coletar dados de vídeo
- `GET /api/v1/videos/{id}` - Obter vídeo específico
- `PUT /api/v1/videos/{id}` - Atualizar vídeo
- `DELETE /api/v1/videos/{id}` - Deletar vídeo

### **Perfis**
- `GET /api/v1/profiles/` - Listar perfis
- `GET /api/v1/profiles/{id}` - Obter perfil específico
- `POST /api/v1/profiles/` - Criar perfil
- `PUT /api/v1/profiles/{id}` - Atualizar perfil
- `DELETE /api/v1/profiles/{id}` - Deletar perfil

### **Analytics**
- `GET /api/v1/analytics/engagement-stats` - Estatísticas gerais
- `GET /api/v1/analytics/top-performers` - Top performers
- `GET /api/v1/analytics/outliers` - Vídeos outliers
- `GET /api/v1/analytics/profile-stats/{username}` - Stats por perfil

## 📋 **Dados Coletados**

### **Por Vídeo:**
- ✅ URL do post
- ✅ Username (@username)
- ✅ Likes, Comments, Views
- ✅ Taxas de engajamento (likes/views, comments/views)
- ✅ Transcrição do áudio
- ✅ Data/hora de postagem

### **Por Perfil:**
- ✅ Username
- ✅ Número de seguidores
- ✅ Métricas agregadas
- ✅ Taxas médias de engajamento

## 🎯 **Próximas Fases**

### **MICROFASE 1.2** - Coleta de Dados Avançados
- [ ] Duração do vídeo
- [ ] Hashtags e legendas
- [ ] Análise de sentimento
- [ ] Métricas de perfil detalhadas

### **MICROFASE 1.3** - Métricas Agregadas + Outlier Detection
- [ ] Cálculo de métricas agregadas por perfil
- [ ] Detecção de outliers
- [ ] Cache para performance
- [ ] Endpoints otimizados

### **MICROFASE 1.4** - API REST Completa
- [ ] Autenticação JWT
- [ ] Rate limiting
- [ ] Documentação automática
- [ ] Testes de integração

## 🔧 **Configuração**

### **Configuração de Variáveis de Ambiente**

1. **Copie o arquivo de exemplo:**
```bash
cp env.example .env
```

2. **Configure suas variáveis no arquivo `.env`:**
```bash
# Apify API Token (obtenha em https://console.apify.com/account/integrations)
APIFY_TOKEN=apify_api_YOUR_TOKEN_HERE

# Database URL
DATABASE_URL=sqlite:///./instagram_analytics.db

# Secret Key (gere uma string aleatória segura)
SECRET_KEY=your-secret-key-change-in-production
```

**⚠️ IMPORTANTE:** Nunca commite o arquivo `.env` com suas chaves reais!

## 📈 **Exemplo de Uso**

### **Coletar dados de um vídeo:**
```bash
curl -X POST "http://localhost:8000/api/v1/videos/scrape?url=https://www.instagram.com/p/ABC123/"
```

### **Resposta:**
```json
{
  "url": "https://www.instagram.com/p/ABC123/",
  "username": "@username",
  "likes": 523247,
  "comments": 16600,
  "views": 1364032,
  "likes_rate": 38.36,
  "comments_rate": 1.22,
  "transcription": "Texto transcrito do áudio...",
  "posted_at": "2025-09-04T22:34:25",
  "id": 1,
  "created_at": "2025-09-05T21:02:40",
  "updated_at": "2025-09-05T21:02:40"
}
```

## 🧹 **Cleanup Realizado**

- ❌ Removido `baixar_instagram.py` (script inicial simples)
- ❌ Removido `coletor_instagram.py` (script standalone)
- ❌ Removido `README.md` antigo (documentação desatualizada)
- ❌ Removido `Instagram scraper.csv` (arquivo de teste)
- ✅ Mantida estrutura backend limpa e organizada

## 📝 **Notas de Desenvolvimento**

- **Clean Architecture** implementada
- **Separação de responsabilidades** clara
- **Código limpo** e bem documentado
- **Tratamento de erros** robusto
- **Logging** detalhado para debug

---

**Desenvolvido com ❤️ seguindo princípios de Clean Code e Clean Architecture**
