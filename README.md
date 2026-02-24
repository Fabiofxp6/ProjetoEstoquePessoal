# Sistema de Gerenciamento de Estoque 📦

Sistema web responsivo desenvolvido em Python (Flask) e MongoDB para gerenciar produtos de uma loja, calcular lucros automaticamente e monitorar níveis de estoque.

## 🛠️ Tecnologias Utilizadas
* **Backend:** Python 3, Flask
* **Banco de Dados:** MongoDB, PyMongo
* **Frontend:** HTML5, CSS3, Bootstrap 5, FontAwesome
* **Segurança:** Variáveis de ambiente (`python-dotenv`), Proteção contra NoSQL Injection nativa do PyMongo (sanitização de tipos) e prevenção contra ReDoS.

## ⚙️ Como rodar o MongoDB Localmente

### Opção 1: Usando Docker (Recomendado)
Se você tem o Docker instalado, basta rodar:
```bash
docker run -d -p 27017:27017 --name mongodb mongo:latest