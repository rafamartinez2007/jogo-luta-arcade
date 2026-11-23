# Jogo de Luta Arcade

Jogo de luta 1x1 em Python + Pygame, feito como exercício de
introdução ao Pygame (loop principal, eventos, desenho de formas,
colisão de retângulos, texto, temporizador, som e classes).

## Como jogar

Ao abrir, escolha o modo no menu:

- `1` — Dois jogadores no mesmo teclado.
- `2` — Jogador contra o computador (CPU), com 3 níveis de dificuldade (`1` fácil, `2` médio, `3` difícil).

Depois aparece uma tela de **Controles** com o resumo dos comandos —
pressione `ENTER` para começar a luta, ou `M` para voltar ao menu.

Melhor de 3 rounds (60 segundos cada). Quem zerar a vida do
adversário, ou tiver mais vida quando o tempo acabar, vence o round.
Vence a luta quem fizer 2 rounds primeiro.

**Jogador 1** (vermelho): `A`/`D` mover, `W` pular, `S` bloquear (segurar), `ESPAÇO` socar.

**Jogador 2 / CPU** (azul): setas mover/pular, seta para baixo bloquear (segurar), `CTRL direito` socar.

Bloquear reduz bastante o dano de um soco recebido. Socos acertados
empurram o adversário (knockback) e tocam um som — acerto, bloqueio e
fim de round têm efeitos sonoros próprios, gerados por código (sem
arquivos de áudio externos).

`P` pausa/despausa a luta, `R` dá revanche (mesmo modo/dificuldade), `M` volta ao menu, `ESC` sai do jogo.

## Como rodar

```bash
pip install -r requirements.txt
python3 main.py
```

## Testes

```bash
pip install -r requirements-dev.txt
pytest
```

Os testes cobrem dano, bloqueio, knockback, cooldown de ataque, a
funcionalidade de pausa, os efeitos sonoros, as telas de menu e a
resolução de round/luta, além do comportamento da IA (aproximação,
ataque e bloqueio em cada dificuldade) — tudo sem precisar abrir uma
janela.

## Estrutura

- `main.py` — loop principal, telas de menu (modo / dificuldade / instruções), estados da partida (lutando / pausado / fim de round / fim de luta), rounds e pontuação.
- `fighter.py` — classe `Fighter` (movimento, pulo, soco, bloqueio, colisão de ataque) e funções de desenho (barra de vida, placar de rounds).
- `bot.py` — classe `Bot`, a IA do computador: aproxima, ataca e bloqueia com probabilidades e tempo de reação que variam por dificuldade (fácil, médio, difícil).
- `sound.py` — gera os efeitos sonoros (acerto, bloqueio, fim de round) por código, sem depender de arquivos de áudio.
- `tests/` — suíte de testes automatizados (pytest).
