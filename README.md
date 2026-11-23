# Jogo de Luta Arcade

Jogo de luta 1x1 local em Python + Pygame, feito como exercício de
introdução ao Pygame (loop principal, eventos, desenho de formas,
colisão de retângulos, texto, temporizador e classes).

## Como jogar

Dois lutadores, mesmo teclado, melhor de 3 rounds (60 segundos cada).
Quem zerar a vida do adversário, ou tiver mais vida quando o tempo
acabar, vence o round. Vence a luta quem fizer 2 rounds primeiro.

**Jogador 1** (vermelho): `A`/`D` mover, `W` pular, `S` bloquear (segurar), `ESPAÇO` socar.

**Jogador 2** (azul): setas mover/pular, seta para baixo bloquear (segurar), `CTRL direito` socar.

Bloquear reduz bastante o dano de um soco recebido. Socos acertados
empurram o adversário (knockback).

`R` reinicia a luta a qualquer momento, `ESC` sai do jogo.

## Como rodar

```bash
pip install -r requirements.txt
python3 main.py
```

## Estrutura

- `main.py` — loop principal, estados da partida (lutando / fim de round / fim de luta), rounds e pontuação.
- `fighter.py` — classe `Fighter` (movimento, pulo, soco, bloqueio, colisão de ataque) e funções de desenho (barra de vida, placar de rounds).
