# Roguelike Game - PgZero

Um jogo roguelike desenvolvido em Python usando PgZero, com animações de sprites, inimigos inteligentes e sistema de som.

## Requisitos

- Python 3.10.5 (recomendado via pyenv)
- PgZero
- Módulos padrão: `math`, `random`
- Pygame (apenas para importar `Rect`)

## Instalação

1. Certifique-se de ter Python 3.10.5 instalado:
```bash
pyenv local 3.10.5
```

2. Instale o PgZero:
```bash
pip install pgzero
```

## Como Executar

Execute o jogo usando:
```bash
pgzrun game.py
```

Ou:
```bash
python -m pgzero game.py
```

## Controles

- **Setas** ou **WASD**: Mover o herói
- **Mouse**: Clicar nos botões do menu
- **ESPAÇO**: Voltar ao menu após game over

## Estrutura do Projeto

- `game.py`: Arquivo principal do jogo com toda a lógica
- `images/`: Pasta para imagens dos sprites
- `sounds/`: Pasta para arquivos de som
- `music/`: Pasta para música de fundo

## Características

- ✅ Menu principal com botões clicáveis
- ✅ Sistema de animação de sprites para herói e inimigos
- ✅ Inimigos que se movem em seu território
- ✅ Música de fundo e efeitos sonoros
- ✅ Sistema de grid roguelike com movimento suave
- ✅ Animações tanto em movimento quanto parado
- ✅ Código limpo seguindo PEP8

## Notas

O jogo funciona mesmo sem arquivos de imagem ou som. Se os arquivos não estiverem presentes, o jogo usará formas geométricas animadas como fallback, que ainda demonstram animação de sprite através de variações cíclicas de tamanho, posição e características visuais.

