# Little Garden — portal modernizado

Portal acadêmico do projeto **Little Garden**, com apresentação inspirada em sites de divulgação de jogos, preservando a identidade verde e natural do projeto e mantendo as páginas e o sistema de contas em Flask.

## O que inclui

- Página inicial com chamada principal, ilustrações locais e cartões de destaque para cultivar, explorar e restaurar.
- Páginas de história, mecânicas, personagens e proposta ambiental.
- Cadastro, login, logout e perfil básico com Flask e SQLite.
- Hash de senhas com Werkzeug e consultas SQL parametrizadas.
- Token CSRF imprevisível validado em todos os formulários POST.
- Senhas armazenadas com hash seguro do Werkzeug, nunca em texto puro.
- Consultas SQL parametrizadas, validação de dados e mensagens de autenticação genéricas.
- Cookies de sessão `HttpOnly`, `SameSite=Lax`, validade limitada e opção `Secure` obrigatória em produção.
- Cabeçalhos HTTP de segurança, política CSP, proteção contra cache do perfil e limite de tamanho de requisição.
- Banco SQLite com espera para contenção e modo WAL para melhorar a convivência entre leitura e escrita.
- Menu adaptável a dispositivos móveis, fechamento por tecla Escape e link para pular diretamente ao conteúdo.
- Ilustrações SVG locais, sem depender de imagens hospedadas em terceiros.

## Requisitos

- Python 3.10 ou superior
- pip

## Executar no Windows (PowerShell)

1. Extraia o ZIP.
2. Abra a pasta `Little_Garden_V2` no VS Code.
3. Abra o terminal nessa pasta.
4. Crie e ative um ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

5. Instale as dependências:

```powershell
python -m pip install -r requirements.txt
```

6. Execute:

```powershell
python app.py
```

7. Abra `http://127.0.0.1:5000/` no navegador. Para encerrar, use `Ctrl+C`.

O banco `little_garden.db` é criado automaticamente. Para guardar as contas de teste, mantenha esse arquivo.

## Páginas

- `/` — início
- `/sobre` — história do jogo
- `/mecanicas` — mecânicas
- `/personagens` — personagens
- `/ambiental` — proposta ambiental
- `/cadastro` — criação de conta
- `/login` — entrada
- `/perfil` — perfil protegido por sessão
- `/logout` — saída por POST

## Configuração para publicação

1. Gere uma chave aleatória forte, por exemplo com `python -c "import secrets; print(secrets.token_hex(32))"`.
2. Configure as variáveis de ambiente no painel seguro da hospedagem, sem colocar a chave diretamente no código:
   - `APP_ENV=production`
   - `LITTLE_GARDEN_SECRET` com a chave gerada
   - `COOKIE_SECURE=1`
   - `LITTLE_GARDEN_DATABASE` com um caminho persistente e gravável, se necessário.
3. Publique somente por HTTPS e execute atrás de um servidor WSGI adequado. Não habilite `FLASK_DEBUG` em produção.
4. Confirme que o volume onde o SQLite fica armazenado persiste após reinicializações e que há backup protegido e testado.

O arquivo `.env.example` é apenas um modelo. O Flask não carrega automaticamente um arquivo `.env` neste projeto; configure as variáveis no terminal ou na plataforma de hospedagem. Nunca envie segredos reais ao Git.

## Testes

Com as dependências instaladas, execute `python -m unittest discover -s tests -v`. Os testes cobrem páginas públicas, cabeçalhos, proteção CSRF, acesso ao perfil, cadastro, login e saída.

## Checklist antes de tornar o site público

- Configurar HTTPS, chave secreta exclusiva e armazenamento persistente.
- Implementar limitação de tentativas de login (rate limiting) e monitoramento de erros no ambiente de hospedagem.
- Definir e testar uma rotina de backup/restauração do SQLite e permissões restritas ao arquivo do banco.
- Atualizar dependências regularmente e executar os testes em ambiente equivalente ao de produção.
- Revisar as políticas de privacidade, retenção e exclusão de dados dos usuários.

As proteções do código reduzem riscos comuns, mas não substituem uma revisão de segurança e a configuração correta da infraestrutura.

## Estrutura

- `app.py` — rotas, sessão, validação CSRF e acesso ao banco
- `templates/` — páginas HTML com Jinja
- `static/css/style.css` — identidade visual, layout e responsividade
- `static/js/script.js` — menu móvel, cartões expansíveis e confirmação de senha
- `static/img/` — ilustrações SVG locais
- `requirements.txt` — dependências Python
- `tests/test_app.py` — testes automatizados das rotas e proteções

## Limites conhecidos

- O perfil do site não salva o progresso do jogo.
- O conteúdo dos personagens é provisório e deve ser revisado pela equipe.
- As ilustrações SVG são arte temporária para apresentação; substitua-as pelas artes finais do jogo quando estiverem disponíveis.
- SQLite é adequado para desenvolvimento e demonstração. A estratégia de armazenamento deve ser revista caso o site seja hospedado em um ambiente com sistema de arquivos efêmero ou múltiplas instâncias.
