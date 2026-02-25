# 🚀 GUIA DE DEPLOY COM POSTGRESQL PERMANENTE — Render.com

## ✅ Pré-requisitos
- Conta no GitHub (gratuita): https://github.com
- Conta no Render.com (gratuita): https://render.com

---

## PASSO 1 — Criar repositório no GitHub

1. Acesse https://github.com/new
2. Nome: `ajudajf`
3. Visibilidade: **Público**
4. Clique em **"Create repository"**
5. Na página do repositório, clique em **"uploading an existing file"**
6. Arraste TODOS os arquivos desta pasta e clique em **"Commit changes"**

---

## PASSO 2 — Criar o Banco PostgreSQL no Render

1. Acesse https://dashboard.render.com
2. Clique em **"New +"** → **"PostgreSQL"**
3. Configure:

   | Campo | Valor |
   |-------|-------|
   | Name | `ajudajf-db` |
   | Database | `ajudajf` |
   | Region | qualquer (ex: Oregon) |
   | Plan | **Free** ✅ |

4. Clique em **"Create Database"**
5. Aguarde ~1 minuto. Quando ficar verde ("Available"), copie o valor de **"Internal Database URL"**

---

## PASSO 3 — Criar o Web Service

1. Clique em **"New +"** → **"Web Service"**
2. Conecte ao GitHub e selecione o repositório `ajudajf`
3. Configure:

   | Campo | Valor |
   |-------|-------|
   | Name | `ajudajf` |
   | Runtime | `Python 3` |
   | Build Command | `pip install -r requirements.txt` |
   | Start Command | `gunicorn app:app --bind 0.0.0.0:$PORT` |
   | Instance Type | **Free** ✅ |

4. Role até **"Environment Variables"** e adicione:

   | Key | Value |
   |-----|-------|
   | `ADMIN_PASSWORD` | `ajudajf2024` ← troque se quiser |
   | `DATABASE_URL` | cole aqui a **Internal Database URL** copiada no Passo 2 |

5. Clique em **"Create Web Service"**

---

## PASSO 4 — Aguardar o Deploy

Em ~2 minutos você verá nos logs:
```
==> Your service is live 🎉
```

Sua URL será algo como: **https://ajudajf.onrender.com**

---

## 🔑 Dados de Acesso Admin

| Item | Valor |
|------|-------|
| **URL pública** | `https://ajudajf.onrender.com` |
| **Painel admin** | botão **⚙ Admin** no canto superior direito |
| **Senha** | `ajudajf2024` (ou a que você definiu) |

Para trocar a senha: Render → seu serviço → **Environment** → edite `ADMIN_PASSWORD` → clique em Save → o serviço reinicia automaticamente.

---

## 💾 Sobre a Persistência

Com PostgreSQL no Render:
- ✅ Dados **nunca são perdidos** ao reiniciar o serviço
- ✅ Banco gratuito por **90 dias** (depois R$ ~0/mês no plano pago ou migrar para outro)
- ✅ Backups automáticos diários

---

## 🆘 Contatos de Emergência JF
- Defesa Civil: **199**
- SAMU: **192**
- Bombeiros: **193**
- Prefeitura JF: **(32) 3690-8000**
