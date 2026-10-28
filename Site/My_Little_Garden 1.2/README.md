# Little Garden — versão reformulada

Portal acadêmico de Little Garden, com identidade visual cozy, espaços reservados para as artes originais do projeto, páginas informativas e autenticação básica com Flask + SQLite.

## Requisitos
- Python 3.10 ou superior
- pip

## Executar no Windows (PowerShell)

1. Extraia o ZIP.
2. Abra a pasta `Little_Garden_Reformulado` no VS Code.
3. Abra o terminal do VS Code e confirme que está na pasta que contém `app.py`.
4. (Recomendado) Crie e ative um ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Se o PowerShell bloquear a ativação, pode continuar sem ativar o ambiente e usar `python -m pip` no passo seguinte.

5. Instale a dependência:

```powershell
python -m pip install -r requirements.txt
```

6. Inicie o servidor:

```powershell
python app.py
```

7. Abra `http://127.0.0.1:5000/` no navegador. Para encerrar, volte ao terminal e pressione `Ctrl+C`.

O banco `little_garden.db` é criado automaticamente na primeira inicialização. Não apague esse arquivo se quiser manter as contas de teste.

## Páginas
- `/` — início
- `/sobre` — história e visão geral do jogo
- `/mecanicas` — agricultura, exploração e restauração
- `/personagens` — cartões de personagens
- `/ambiental` — proposta ambiental
- `/cadastro` — criação de conta
- `/login` — entrada
- `/perfil` — página protegida por sessão
- `/logout` — saída (POST)

## Onde inserir suas próprias imagens
Os blocos com borda tracejada e texto como `SUA ILUSTRAÇÃO PRINCIPAL AQUI` são placeholders intencionais, não imagens faltando por engano. Coloque seus arquivos em `static/img/` e troque cada bloco `div.image-placeholder` no template correspondente por uma tag, por exemplo:

```html
<img class="hero-art" src="{{ url_for('static', filename='img/ilha-principal.png') }}" alt="O gnomo diante da ilha">
```

Para manter o enquadramento, use `object-fit: cover` e uma altura definida. Para imagem de fundo decorativa, prefira CSS. Não é necessário usar nomes iguais aos exemplos; atualize o caminho para o nome real do arquivo.

## Estrutura
- `app.py` — rotas Flask, banco de dados e autenticação
- `templates/` — templates Jinja das páginas
- `static/css/style.css` — identidade visual, layout e responsividade
- `static/js/script.js` — menu mobile, cartões expansíveis e validação de confirmação de senha
- `static/img/` — local para imagens originais do projeto
- `requirements.txt` — dependências Python

## Notas importantes para o TCC
- Senhas são armazenadas usando hash via Werkzeug, não em texto puro.
- Consultas ao banco usam parâmetros para reduzir risco de SQL injection.
- A página de perfil exige sessão autenticada.
- Esta é uma base acadêmica para desenvolvimento local, não uma aplicação pronta para produção. Antes de publicar, configure `LITTLE_GARDEN_SECRET` com uma chave aleatória forte, desative o modo debug, adicione proteção CSRF (por exemplo, Flask-WTF), revise limites de tentativas de login e configure HTTPS.
- O conteúdo dos personagens 2 e 3 é provisório e deve ser ajustado conforme a documentação real do jogo.
- A aplicação não inclui inteligência artificial nem sistema de mensageria; confirme os requisitos específicos dessas disciplinas com o professor antes de adicionar componentes desnecessários.
- O site usa Google Fonts via internet; se não houver conexão, as fontes de sistema serão usadas.
