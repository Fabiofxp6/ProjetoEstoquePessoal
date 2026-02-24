📦 Sistema de Gestão de Estoque & PDV 🚀
Este é um sistema web completo para gerenciamento de lojas, permitindo o controle rigoroso de estoque, frente de caixa (PDV) para vendas rápidas e um dashboard de relatórios financeiros.

🌟 Funcionalidades Principais
Frente de Caixa (PDV): Realização de vendas com múltiplos itens, baixa automática de estoque e escolha de forma de pagamento (Pix, Crédito, Débito, Dinheiro).

Gestão de Inventário: Cadastro, edição, busca e exclusão de produtos com cálculo automático de lucro.

Alertas Visuais: Identificação imediata de produtos com estoque baixo (≤ 2) ou esgotados.

Dashboard Financeiro: Relatórios em tempo real de Faturamento Total, Lucro Real, Ticket Médio e Histórico de Vendas.

Segurança: Confirmação de exclusão via Modal, proteção contra injeção NoSQL e variáveis de ambiente.

Interface Responsiva: Otimizado para computadores, tablets e celulares usando Bootstrap 5.

🛠️ Tecnologias Utilizadas
Backend: Python 3 + Flask

Banco de Dados: MongoDB (Atlas ou Local)

Arquitetura: Padrão modular (Blueprints/MVC)

Frontend: HTML5, CSS3, JavaScript (Vanilla), Bootstrap 5 e FontAwesome.

⚙️ Configuração do Ambiente
1. Pré-requisitos

Python 3.10 ou superior instalado.

Conta no MongoDB Atlas (ou MongoDB instalado localmente).

2. Instalação

Clone o repositório ou extraia os arquivos, então abra o terminal na pasta do projeto:

Bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# No Windows:
venv\Scripts\activate
# No Mac/Linux:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
3. Variáveis de Ambiente (.env)

Crie um arquivo chamado .env na raiz do projeto e configure suas chaves:

Snippet de código
MONGO_URI=sua_string_de_conexao_do_mongodb_atlas
SECRET_KEY=uma_chave_aleatoria_para_sessao
Nota: Se usar o MongoDB Atlas, certifique-se de liberar o acesso ao IP (Network Access) no painel do Atlas.

🚀 Como Executar
Para iniciar o servidor de desenvolvimento:

Bash
python app.py
O sistema estará disponível nos seguintes endereços:

Local: http://127.0.0.1:5001

Rede Local (Celular): http://[SEU-IP]:5001

📂 Estrutura do Projeto
Plaintext
estoque_app/
├── app.py              # Inicialização do Flask e registro de Blueprints
├── config.py           # Configurações de sistema e banco de dados
├── .env                # Variáveis sensíveis (não versionar em produção)
├── routes/
│   ├── product_routes.py # Gestão de produtos e estoque
│   └── sales_routes.py   # Lógica de vendas e relatórios
├── templates/          # Arquivos HTML (Jinja2)
└── static/             # CSS personalizado e imagens
👨‍💻 Boas Práticas Implementadas
Separação de Responsabilidades: Rotas divididas em módulos para facilitar a manutenção.

Sanitização de Dados: Uso de Regex e PyMongo para prevenir ataques.

UX (User Experience): Modais de confirmação evitam erros do usuário; cálculos em JavaScript garantem fluidez na venda.

Cálculo de Lucro: O lucro é calculado tanto no cadastro do produto quanto no fechamento da venda para garantir precisão financeira.

📝 Licença

Este projeto foi desenvolvido para fins de gerenciamento comercial e educacional. Sinta-se à vontade para expandir!