import random
import arcade

# Ekran boyutları
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Galactic Defender"

# Roket sabitleri
ROCKET_SPEED = 8

# UFO sabitleri
UFO_COUNT = 5
UFO_SPEED = 1.2

# Mermi sabitleri
BULLET_SPEED = 10

class GalacticDefender(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Arka plan rengi
        arcade.set_background_color(arcade.color.BLACK)

        self.lives = 3  
        self.game_over = False  

        self.rocket_sprite = None
        self.rocket_x_change = 0
        self.rocket_y_change = 0

        self.ufo_list = None

        self.bullet_list = None

    def setup(self):
        self.background = arcade.load_texture("assets/background.png")
        self.rocket_sprite = arcade.Sprite("assets/rocket.png", scale=0.15)
        self.rocket_sprite.center_x = SCREEN_WIDTH // 2
        self.rocket_sprite.center_y = 100  


        self.ufo_list = arcade.SpriteList()
        for _ in range(UFO_COUNT):
            ufo = arcade.Sprite("assets/ufo.png", scale=0.2)
            ufo.center_x = random.randint(0, SCREEN_WIDTH)
            ufo.center_y = random.randint(SCREEN_HEIGHT // 2, SCREEN_HEIGHT)
            self.ufo_list.append(ufo)
        self.bullet_list = arcade.SpriteList()

    def on_draw(self):
        arcade.start_render()
        if self.background:
            arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.rocket_sprite.draw()
        self.ufo_list.draw()
        self.bullet_list.draw()


        arcade.draw_text(f"Lives: {self.lives}", SCREEN_WIDTH - 100, SCREEN_HEIGHT - 30, arcade.color.WHITE, 16)

        if self.game_over:
            arcade.draw_text("GAME OVER", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40, arcade.color.RED, 40, anchor_x="center")
            arcade.draw_text("Yeniden Başlat", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20, arcade.color.YELLOW, 24, anchor_x="center")

    def on_update(self, delta_time):
        self.rocket_sprite.center_x += self.rocket_x_change
        self.rocket_sprite.center_y += self.rocket_y_change



        if self.game_over:
            return


        if arcade.check_for_collision_with_list(self.rocket_sprite, self.ufo_list):
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
            else:
                self.rocket_sprite.center_x = SCREEN_WIDTH // 2
                self.rocket_sprite.center_y = 100

        for ufo in self.ufo_list:
            if ufo.bottom < 0:
                self.lives -= 1
                ufo.remove_from_sprite_lists()  
                if self.lives <= 0:
                    self.game_over = True



        while len(self.ufo_list) < UFO_COUNT:
            new_ufo = arcade.Sprite("assets/ufo.png", scale=0.2)
            new_ufo.center_x = random.randint(0, SCREEN_WIDTH)
            new_ufo.center_y = random.randint(SCREEN_HEIGHT, SCREEN_HEIGHT + 50)
            self.ufo_list.append(new_ufo)


        if self.rocket_sprite.left < 0:
            self.rocket_sprite.left = 0
        if self.rocket_sprite.right > SCREEN_WIDTH:
            self.rocket_sprite.right = SCREEN_WIDTH
        if self.rocket_sprite.bottom < 0:
            self.rocket_sprite.bottom = 0
        if self.rocket_sprite.top > SCREEN_HEIGHT:
            self.rocket_sprite.top = SCREEN_HEIGHT


        for ufo in self.ufo_list:
            ufo.center_y -= UFO_SPEED
            if ufo.center_y < 0:
                ufo.center_y = random.randint(SCREEN_HEIGHT, SCREEN_HEIGHT + 50)
                ufo.center_x = random.randint(0, SCREEN_WIDTH)
        self.bullet_list.update()


        for bullet in self.bullet_list:
            hit_list = arcade.check_for_collision_with_list(bullet, self.ufo_list)
            if hit_list:
                bullet.remove_from_sprite_lists()
                for ufo in hit_list:
                    ufo.remove_from_sprite_lists()

            # Mermi ekranın dışına çıkarsa yok et 
            if bullet.bottom > SCREEN_HEIGHT:
                bullet.remove_from_sprite_lists()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.game_over:
            # "Yeniden Başlat" yazısının tıklanıp tıklanmadığını kontrol et
            if SCREEN_WIDTH // 2 - 100 < x < SCREEN_WIDTH // 2 + 100 and SCREEN_HEIGHT // 2 - 40 < y < SCREEN_HEIGHT // 2:
                self.setup()  # Oyunu sıfırla
                self.lives = 3
                self.game_over = False
                

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.rocket_y_change = ROCKET_SPEED
        elif key == arcade.key.DOWN:
            self.rocket_y_change = -ROCKET_SPEED
        elif key == arcade.key.LEFT:
            self.rocket_x_change = -ROCKET_SPEED
        elif key == arcade.key.RIGHT:
            self.rocket_x_change = ROCKET_SPEED
        elif key == arcade.key.SPACE:
            # Mermi oluştur ve ateşle
            bullet = arcade.Sprite("assets/bullet.png", scale=0.05)
            bullet.center_x = self.rocket_sprite.center_x
            bullet.bottom = self.rocket_sprite.top
            bullet.change_y = BULLET_SPEED
            self.bullet_list.append(bullet)

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.UP, arcade.key.DOWN):
            self.rocket_y_change = 0
        elif key in (arcade.key.LEFT, arcade.key.RIGHT):
            self.rocket_x_change = 0


def main():
    game = GalacticDefender()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main() 





