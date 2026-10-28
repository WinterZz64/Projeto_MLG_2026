# Little Garden — portal do projeto

Este é o site do projeto escolar Little Garden. O jogo é uma aventura 2D com agricultura e exploração: um gnomo tenta recuperar uma ilha contaminada por lixo mágico.

## O que o site tem

- Páginas sobre a história, as mecânicas planejadas, os personagens e a proposta ambiental.
- Cadastro, login e perfil básico de usuário.
- Flask (Python), HTML, CSS, JavaScript e SQLite.
- Ilustrações SVG provisórias. Elas não são as artes oficiais dos personagens.

**Importante:** os textos descrevem o planejamento do jogo enviado pela equipe. Quando uma mecânica ainda estiver em desenvolvimento, o site não deve dar a entender que ela já está pronta. O perfil do site não salva o progresso do jogo.

## Rodar no computador

Você precisa ter Python instalado.

1. Abra o terminal dentro desta pasta.
2. Crie um ambiente virtual:

   ```bash
   python -m venv .venv
   ```

3. Ative o ambiente virtual.

   Windows PowerShell:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   macOS/Linux:

   ```bash
   source .venv/bin/activate
   ```

4. Instale a dependência:

   ```bash
   python -m pip install -r requirements.txt
   ```

5. Inicie o site:

   ```bash
   python app.py
   ```

6. Abra no navegador o endereço local informado pelo Flask (normalmente `http://127.0.0.1:5000`).

O banco `little_garden.db` é criado automaticamente na pasta do projeto. Não apague esse arquivo se quiser preservar as contas cadastradas nesse computador.

## Segurança e versionamento

- O arquivo `.env` e os bancos SQLite locais ficam fora do Git.
- `.env.example` serve como exemplo, não coloque senhas ou chaves reais nele.
- Em produção, configure `APP_ENV=production`, `LITTLE_GARDEN_SECRET` com uma chave aleatória longa, `COOKIE_SECURE=1` e HTTPS.
- Use uma chave diferente para cada ambiente. Não publique a chave real no GitHub.
- Faça backup do banco antes de atualizar ou mover a instalação.
- O site usa tokens CSRF nos formulários, hash de senha e consultas SQL parametrizadas.
- Para um site público, ainda é necessário configurar hospedagem corretamente, HTTPS, backups e proteção contra tentativas repetidas de login.

## Banco de dados

O SQLite é adequado para desenvolvimento e para um site pequeno com armazenamento persistente. Se a hospedagem apagar arquivos locais ao reiniciar ou não oferecer armazenamento persistente, o banco precisará ficar em um volume persistente ou em outro serviço de banco. Não envie o arquivo de banco com contas reais para o GitHub.

## Testes

Os testes básicos ficam em `tests/test_app.py`. Com as dependências instaladas, execute:

```bash
python -m unittest discover -s tests -v
```

Os testes precisam ser executados antes de considerar uma atualização pronta para publicação.


## Artes de cenário

As imagens `hero-island.webp`, `garden.webp`, `exploration.webp` e `restoration.webp` são cenários ilustrativos gerados para preencher os espaços visuais do portal. Elas não representam capturas de tela do jogo nem artes oficiais dos personagens. Substitua-as pelas artes definitivas quando estiverem prontas.
