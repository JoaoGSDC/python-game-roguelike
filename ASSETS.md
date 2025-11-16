# Guia de Assets

Este jogo funciona perfeitamente sem arquivos de imagem ou som, usando animações geométricas como fallback. No entanto, você pode adicionar seus próprios assets para melhorar a experiência visual e sonora.

## Estrutura de Pastas

```
pygame-roguelike/
├── images/          # Imagens dos sprites
├── sounds/          # Efeitos sonoros
└── music/           # Música de fundo
```

## Sprites Necessários

O jogo procura pelos seguintes sprites (todos opcionais):

### Herói
- `hero_idle_down_1.png`, `hero_idle_down_2.png`
- `hero_idle_left_1.png`, `hero_idle_left_2.png`
- `hero_idle_right_1.png`, `hero_idle_right_2.png`
- `hero_idle_up_1.png`, `hero_idle_up_2.png`
- `hero_move_down_1.png`, `hero_move_down_2.png`, `hero_move_down_3.png`
- `hero_move_left_1.png`, `hero_move_left_2.png`, `hero_move_left_3.png`
- `hero_move_right_1.png`, `hero_move_right_2.png`, `hero_move_right_3.png`
- `hero_move_up_1.png`, `hero_move_up_2.png`, `hero_move_up_3.png`

### Inimigos
- `enemy_idle_down_1.png`, `enemy_idle_down_2.png`
- `enemy_idle_left_1.png`, `enemy_idle_left_2.png`
- `enemy_idle_right_1.png`, `enemy_idle_right_2.png`
- `enemy_idle_up_1.png`, `enemy_idle_up_2.png`
- `enemy_move_down_1.png`, `enemy_move_down_2.png`, `enemy_move_down_3.png`
- `enemy_move_left_1.png`, `enemy_move_left_2.png`, `enemy_move_left_3.png`
- `enemy_move_right_1.png`, `enemy_move_right_2.png`, `enemy_move_right_3.png`
- `enemy_move_up_1.png`, `enemy_move_up_2.png`, `enemy_move_up_3.png`

**Tamanho recomendado**: 32x32 pixels

## Sons Necessários

- `sounds/step.ogg` ou `sounds/step.wav` - Som de passo ao mover
- `sounds/button_click.ogg` ou `sounds/button_click.wav` - Som de clique no botão
- `sounds/game_over.ogg` ou `sounds/game_over.wav` - Som de game over

## Música

- `music/background.ogg` ou `music/background.wav` - Música de fundo (deve ser um arquivo de loop)

## Nota

Se você não adicionar esses arquivos, o jogo continuará funcionando normalmente usando animações geométricas e sem sons. Isso é intencional e permite que o jogo seja executado imediatamente sem necessidade de assets externos.

