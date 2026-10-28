# Little Garden — versão modernizada

Portal acadêmico do projeto **My Little Garden**, com uma identidade visual inspirada em jogos de aventura e fantasia: interface escura, detalhes verde-sálvia, ilustrações vetoriais originais e layouts adaptáveis a celulares, tablets e computadores. A referência foi apenas visual; a identidade, os textos e as ilustrações foram criados para este projeto.

## O que vem no projeto

- Página inicial redesenhada com hero ilustrado, destaques das mecânicas e chamada para a comunidade.
- Páginas de história, mecânicas, personagens e proposta ambiental.
- Cadastro, login, logout e perfil básico com Flask e SQLite.
- Menu responsivo para dispositivos móveis e controles acessíveis por teclado.
- Ilustrações SVG locais em `static/img/`, sem depender de imagens hospedadas em outros sites.

## Requisitos

- Python 3.10 ou superior
- pip

## Como executar no Windows (PowerShell)

1. Extraia o ZIP.
2. Abra a pasta `Little_Garden_Modernizado` no VS Code.
3. Abra o terminal nessa pasta, onde está o arquivo `app.py`.
4. Crie e ative um ambiente virtual (recomendado):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

5. Instale as dependências:

```powershell
python -m pip install -r requirements.txt
```

6. Inicie o servidor:

```powershell
python app.py
```

7. Acesse `http://127.0.0.1:5000/` no navegador. Para parar o servidor, use `Ctrl+C` no terminal.

O banco `little_garden.db` é criado automaticamente ao iniciar `app.py` diretamente. Se quiser manter as contas de teste, não apague esse arquivo.

## Páginas disponíveis

- `/` — início
- `/sobre` — história e visão geral
- `/mecanicas` — agricultura, exploração e restauração
- `/personagens` — cartões de personagens
- `/ambiental` — proposta ambiental
- `/cadastro` — criação de conta
- `/login` — entrada
- `/perfil` — página protegida por sessão
- `/logout` — saída por POST

## Estrutura principal

- `app.py` — rotas Flask, banco de dados e autenticação
- `templates/` — páginas HTML com Jinja
- `static/css/style.css` — identidade visual, layout e responsividade
- `static/js/script.js` — menu mobile, cartões expansíveis e confirmação de senha
- `static/img/` — ilustrações SVG locais
- `requirements.txt` — dependências Python

## Personalização

As ilustrações são arquivos SVG dentro de `static/img/`. Podem ser editadas em um editor de texto ou de vetores, ou substituídas pelas artes finais do jogo. Os principais estilos estão concentrados em `static/css/style.css`; as cores ficam nas variáveis CSS no começo do arquivo.

## Observações para o TCC

- Senhas são armazenadas usando hash via Werkzeug, não em texto puro.
- Consultas ao banco usam parâmetros.
- O perfil exige sessão autenticada.
- O perfil do site não salva progresso do jogo; é apenas uma área básica da conta.
- Os personagens 2 e 3 são conceitos provisórios. Atualize nomes, história e imagens com base na documentação oficial do jogo.
- O projeto é uma base acadêmica para desenvolvimento local, não uma aplicação pronta para produção. Antes de publicar, configure uma chave `LITTLE_GARDEN_SECRET` forte, desative `debug`, adicione proteção CSRF, limite tentativas de login e use HTTPS.
- As fontes do Google são opcionais. Sem conexão, o navegador usa fontes de sistema semelhantes.
