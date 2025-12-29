import random
from settings import *
from player import Player
from pytmx.util_pygame import load_pygame
from sprite import *
class Game:
    def __init__(self):
        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.camera_offset = pygame.Vector2(0, 0)

        # groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.setup()

        #     bg
        self.bg = pygame.image.load(join("..","assets","Graphics","bg","bg.png")).convert()
        self.bg = pygame.transform.scale(
            self.bg, (WINDOW_WIDTH, WINDOW_HEIGHT)
        )
    def setup(self):
        tmx_map = load_pygame(join("..", "assets", "maps", "level1-final.tmx"))

        # =========================
        # VISUAL DECORATIONS
        # =========================
        for obj in tmx_map.get_layer_by_name("decorations"):
            Decoration.from_tmx(obj, self.all_sprites)

        # =========================
        # VISUAL GROUND TILES
        # =========================
        for x, y, image in tmx_map.get_layer_by_name("Ground").tiles():
            Sprite(
                (x * TILE_SIZE, y * TILE_SIZE),
                image,
                self.all_sprites
            )

        # =========================
        # PLATFORM COLLISIONS (POLYGONS)
        # =========================
        for obj in tmx_map.get_layer_by_name("platforms"):
            points = obj.as_points

            xs = [p[0] for p in points]
            ys = [p[1] for p in points]

            rect = pygame.FRect(
                min(xs),
                min(ys),
                max(xs) - min(xs),
                max(ys) - min(ys)
            )

            CollisionSprite(rect, self.collision_sprites)

        # =========================
        # PLAYER SPAWN
        # =========================
        self.player = None
        for obj in tmx_map.get_layer_by_name("player"):
            if obj.name == "spawn":
                self.player = Player(
                    (obj.x, obj.y),
                    self.all_sprites,
                    self.collision_sprites
                )

        if self.player is None:
            raise RuntimeError("No player spawn found in TMX map")

    def run(self):
        while self.running:
            # dt
            dt = self.clock.tick()/1000
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # update
            self.all_sprites.update(dt)

            self.camera_offset.x = self.player.rect.centerx - WINDOW_WIDTH // 2
            self.camera_offset.y = self.player.rect.centery - WINDOW_HEIGHT // 2

            # draw
            # # draw background with parallax
            # bg_x = -self.camera_offset.x * 0.2
            # bg_y = -self.camera_offset.y * 0.2
            # self.display_surface.blit(self.bg, (bg_x, bg_y))
            self.display_surface.blit(self.bg, (0, 0))

            for sprite in self.all_sprites:
                offset_rect = sprite.rect.copy()
                offset_rect.topleft -= self.camera_offset
                self.display_surface.blit(sprite.image, offset_rect)
            for sprite in self.collision_sprites:
                debug_rect = sprite.rect.copy()
                debug_rect.topleft -= self.camera_offset
                pygame.draw.rect(self.display_surface, "red", debug_rect, 2)

            pygame.display.update()
        # end
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()