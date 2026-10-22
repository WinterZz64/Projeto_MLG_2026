# Little Garden — estado do projeto

## Estado desta revisão
- Portal informativo como escopo principal.
- Páginas Flask agora renderizam templates HTML, em vez de devolver textos simples.
- Criadas páginas iniciais para Mecânicas, Personagens e Recuperação ambiental.
- Removido o link "Entrar" da navegação, pois login não faz parte do escopo confirmado.
- Removida a referência CSS a `static/img/hero.jpg`, que não estava presente no ZIP. O destaque usa o fundo verde como fallback.
- O CSS e o JavaScript continuam separados em `static/css/` e `static/js/`.

## Como executar localmente
1. Instale Python, caso ainda não esteja instalado.
2. No terminal, entre na pasta `My Little Garden Site`.
3. Instale Flask: `python -m pip install flask`
4. Execute: `python app.py`
5. Abra `http://127.0.0.1:5000/` no navegador.
6. Para encerrar, use `Ctrl+C` no terminal.

## Estrutura
- `app.py`: rotas do servidor Flask.
- `templates/`: páginas HTML renderizadas pelo Flask.
- `static/css/style.css`: estilos.
- `static/js/script.js`: JavaScript.
- `static/img/`: imagens do portal (atualmente sem arquivos no pacote original).

## Pendências conhecidas
- Confirmar com a equipe se os detalhes de gameplay, regiões, loja, criaturas, equipamentos, Árvore Lendária e personagens são definitivos.
- Adicionar imagens autorizadas/oficiais do jogo; não há imagens no pacote atual.
- Uniformizar o cabeçalho/rodapé das páginas e revisar acessibilidade, responsividade e links.
- Validar ortografia e consistência textual, incluindo o texto existente em `sobre.html`.
- Decidir com base nas exigências das disciplinas se será necessário banco de dados e área de gerenciamento de conteúdo.
- Confirmar se a disciplina de Mensageria exige uma implementação específica; não foi adicionada uma fila de mensagens sem requisito.
- Cadastro, login e perfil estão fora do escopo confirmado e permanecem páginas antigas de rascunho, sem funcionalidade.
- `debug=True` é apropriado apenas para desenvolvimento local, nunca para implantação pública.

## Nota de conteúdo
Os textos das páginas novas foram escritos apenas a partir das informações presentes no rascunho enviado. Itens descritos como pendentes devem ser validados pela equipe antes da publicação.
