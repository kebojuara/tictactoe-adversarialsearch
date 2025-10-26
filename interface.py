import sys
import pygame
import main as engine

pygame.init()
WIDTH, HEIGHT = 800, 550
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe (Adversarial, Memory Stats) - Pygame")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (210, 210, 210)
DARK = (60, 60, 60)
BLUE = (40, 110, 200)
RED = (200, 50, 50)

FONT_H1 = pygame.font.SysFont("arial", 36, bold=True)
FONT_CELL = pygame.font.SysFont("franklingothicmedium", 48)
FONT_TEXT = pygame.font.SysFont("arial", 20)
FONT_BTN = pygame.font.SysFont("arial", 18)

GRID_X0, GRID_Y0 = 180, 120
CELL_SIZE = 100
GRID_COLOR = GRAY

class Button:
    def __init__(self, rect, text, bg=BLUE, fg=WHITE, callback=None):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.bg = bg
        self.fg = fg
        self.callback = callback
        self.hover = False

    def draw(self, surf):
        color = tuple(min(255, c+25) for c in self.bg) if self.hover else self.bg
        pygame.draw.rect(surf, color, self.rect, border_radius=10)
        label = FONT_BTN.render(self.text, True, self.fg)
        surf.blit(label, label.get_rect(center=self.rect.center))

    def handle(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos) and self.callback:
                self.callback()

class Dropdown:
    def __init__(self, rect, options, default_idx=0):
        self.rect = pygame.Rect(rect)
        self.options = options
        self.index = default_idx
        self.open = False

    def value(self):
        return self.options[self.index]

    def draw(self, surf):
        pygame.draw.rect(surf, (255,255,255), self.rect, border_radius=6)
        pygame.draw.rect(surf, DARK, self.rect, width=2, border_radius=6)
        label = FONT_BTN.render(self.value(), True, (0,0,0))
        surf.blit(label, (self.rect.x+10, self.rect.y+8))
        pygame.draw.polygon(surf, DARK, [(self.rect.right-20, self.rect.y+12),
                                         (self.rect.right-10, self.rect.y+12),
                                         (self.rect.right-15, self.rect.y+20)])
        if self.open:
            h = self.rect.height
            for i, opt in enumerate(self.options):
                r = pygame.Rect(self.rect.x, self.rect.y + (i+1)*h, self.rect.width, h)
                pygame.draw.rect(surf, (255,255,255), r)
                pygame.draw.rect(surf, DARK, r, 1)
                lbl = FONT_BTN.render(opt, True, (0,0,0))
                surf.blit(lbl, (r.x+10, r.y+8))

    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.open = not self.open
            elif self.open:
                h = self.rect.height
                for i, _ in enumerate(self.options):
                    r = pygame.Rect(self.rect.x, self.rect.y + (i+1)*h, self.rect.width, h)
                    if r.collidepoint(event.pos):
                        self.index = i
                        self.open = False
                        break
                else:
                    self.open = False

class Game:
    def __init__(self):
        self.board = engine.new_board()
        self.human = 'X'
        self.ai = 'O'
        self.game_over = False
        self.status_text = "Click any cell to play!"
        self.analysis_text = ""
        self.btn_player_first = Button((60, 480, 180, 40), "New Game (You=X)", callback=self.new_game_player_first)
        self.btn_ai_first = Button((260, 480, 180, 40), "New Game (AI First)", callback=self.new_game_ai_first)
        self.btn_reset = Button((460, 480, 140, 40), "Reset Board", bg=RED, callback=self.reset_board)
        self.dropdown = Dropdown((635, 140, 140, 36), ["Alpha-Beta", "Minimax"], default_idx=0)

    def new_game_player_first(self):
        self.board = engine.new_board()
        self.human, self.ai = 'X', 'O'
        self.game_over = False
        self.status_text = "You are X. Your move!"
        self.analysis_text = ""

    def new_game_ai_first(self):
        self.board = engine.new_board()
        self.human, self.ai = 'O', 'X'
        self.game_over = False
        self.status_text = "AI starts as X..."
        self.analysis_text = ""
        self.ai_play_if_needed()

    def reset_board(self):
        self.board = engine.new_board()
        self.game_over = False
        self.status_text = "Board reset. Click any cell to play!"
        self.analysis_text = ""

    def human_move(self, idx):
        if self.game_over or self.board[idx] != ' ':
            return
        self.board[idx] = self.human
        if self.check_end():
            return
        self.ai_play_if_needed()

    def ai_play_if_needed(self):
        if self.game_over:
            return
        algo = self.dropdown.value()
        move, stats = engine.ai_move(self.board, self.ai, algo)
        if move != -1:
            self.board[move] = self.ai
        self.show_analysis(algo, stats)
        self.check_end()

    def check_end(self):
        w = engine.winner(self.board)
        if w:
            self.status_text = f"{w} wins!"
            self.game_over = True
            return True
        if all(v != ' ' for v in self.board):
            self.status_text = "Draw."
            self.game_over = True
            return True
        self.status_text = "Your move!" if self.to_move_is_human() else "AI is thinking..."
        return False

    def to_move_is_human(self):
        x = sum(1 for v in self.board if v == 'X')
        o = sum(1 for v in self.board if v == 'O')
        if self.human == 'X':
            return x == o
        else:
            return o < x

    def show_analysis(self, algo, stats):
        kb = max(1, stats.peak_bytes // 1024)
        self.analysis_text = (
            f"Analysis of\n{algo}\n\n"
            f"Nodes expanded:\n{stats.nodes}\n"
            f"Search depth:\n{stats.depth}\n"
            f"Runtime:\n{stats.runtime:.3f} ms\n"
            f"Peak memory:\n{kb} KB"
        )

    def cell_at_pos(self, pos):
        x, y = pos
        for r in range(3):
            for c in range(3):
                rx = GRID_X0 + c * CELL_SIZE
                ry = GRID_Y0 + r * CELL_SIZE
                rect = pygame.Rect(rx, ry, CELL_SIZE, CELL_SIZE)
                if rect.collidepoint(x, y):
                    return r * 3 + c
        return None

    def draw_grid(self):
        for r in range(3):
            for c in range(3):
                x = GRID_X0 + c * CELL_SIZE
                y = GRID_Y0 + r * CELL_SIZE
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(SCREEN, GRID_COLOR, rect)
                pygame.draw.rect(SCREEN, DARK, rect, 3)
                val = self.board[r * 3 + c]
                if val.strip():
                    lbl = FONT_CELL.render(val, True, (0,0,0))
                    SCREEN.blit(lbl, lbl.get_rect(center=rect.center))

    def draw_panel(self):
        title = FONT_H1.render("Tic-Tac-Toe (Adversarial Search)", True, (0,0,0))
        SCREEN.blit(title, title.get_rect(center=(330, 70)))
        alg_label = FONT_TEXT.render("Search Algorithm:", True, (0,0,0))
        SCREEN.blit(alg_label, alg_label.get_rect(center=(705, 115)))
        status = FONT_TEXT.render(self.status_text, True, (0,0,0))
        SCREEN.blit(status, status.get_rect(center=(330, 450)))
        box = pygame.Rect(625, 200, 160, 260)
        pygame.draw.rect(SCREEN, (214, 214, 214), box)
        pygame.draw.rect(SCREEN, DARK, box, 3)
        y = box.y + 10
        for line in self.analysis_text.split("\n"):
            line_surf = FONT_TEXT.render(line, True, (0,0,0))
            SCREEN.blit(line_surf, (box.x + 10, y))
            y += 22
        self.dropdown.draw(SCREEN)
        self.btn_player_first.draw(SCREEN)
        self.btn_ai_first.draw(SCREEN)
        self.btn_reset.draw(SCREEN)

    def loop(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    idx = self.cell_at_pos(event.pos)
                    if idx is not None and self.to_move_is_human() and not self.game_over:
                        self.human_move(idx)
                self.btn_player_first.handle(event)
                self.btn_ai_first.handle(event)
                self.btn_reset.handle(event)
                self.dropdown.handle(event)
            SCREEN.fill((255,255,255))
            self.draw_grid()
            self.draw_panel()
            pygame.display.flip()
            clock.tick(60)
        pygame.quit()
        sys.exit()

def main():
    Game().loop()

if __name__ == "__main__":
    main()
