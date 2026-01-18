import pygame
pygame.init()

# ===================== SETUP LAYAR =====================
LEBAR_LAYAR = 500
TINGGI_LAYAR = 500
layar = pygame.display.set_mode((LEBAR_LAYAR, TINGGI_LAYAR))
pygame.display.set_caption("Arkanoid Game")

warna_bg = (72, 61, 139)
jam = pygame.time.Clock()

# ===================== VARIABEL GAME =====================
jalan = True
game_selesai = False
hasil_game = ""

kecepatan_bola_x = 2
kecepatan_bola_y = 2

gerak_kiri = False
gerak_kanan = False
kecepatan_platform = 5

# ===================== CLASS =====================
class Area:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)

class Label(Area):
    def set_text(self, text, ukuran, warna):
        self.image = pygame.font.SysFont("verdana", ukuran).render(text, True, warna)

    def draw(self):
        layar.blit(self.image, self.rect)

class Gambar(Area):
    def __init__(self, file, x, y, w, h):
        super().__init__(x, y, w, h)
        self.image = pygame.image.load(file)

    def draw(self):
        layar.blit(self.image, self.rect)

# ===================== OBJECT =====================
bola = Gambar("grimreaper.png", 160, 200, 50, 50)
platform = Gambar("platform.png", 200, 430, 100, 20)

monster = []
x_awal = 10
y_awal = 10
jumlah = 9

for baris in range(3):
    x = x_awal + baris * 25
    y = y_awal + baris * 55
    for i in range(jumlah):
        monster.append(Gambar("enemyghost.png", x, y, 50, 50))
        x += 55
    jumlah -= 1

# ===================== GAME LOOP =====================
while jalan:
    layar.fill(warna_bg)

    # ---------- EVENT ----------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jalan = False

        if not game_selesai:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    gerak_kiri = True
                if event.key == pygame.K_RIGHT:
                    gerak_kanan = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    gerak_kiri = False
                if event.key == pygame.K_RIGHT:
                    gerak_kanan = False

    # ---------- GERAK PLATFORM ----------
    if not game_selesai:
        if gerak_kiri:
            platform.rect.x -= kecepatan_platform
        if gerak_kanan:
            platform.rect.x += kecepatan_platform

        # biar platform tidak keluar layar
        if platform.rect.x < 0:
            platform.rect.x = 0
        if platform.rect.x + platform.rect.width > LEBAR_LAYAR:
            platform.rect.x = LEBAR_LAYAR - platform.rect.width

    # ---------- GERAK BOLA ----------
    if not game_selesai:
        bola.rect.x += kecepatan_bola_x
        bola.rect.y += kecepatan_bola_y

        # pantul kiri & kanan
        if bola.rect.x <= 0 or bola.rect.x + bola.rect.width >= LEBAR_LAYAR:
            kecepatan_bola_x *= -1

        # pantul atas
        if bola.rect.y <= 0:
            kecepatan_bola_y *= -1

        # pantul platform
        if bola.rect.colliderect(platform.rect):
            kecepatan_bola_y *= -1

        # tabrak monster
        for m in monster[:]:
            if bola.rect.colliderect(m.rect):
                monster.remove(m)
                kecepatan_bola_y *= -1
                break

        # ---------- LOGIKA AWAM GAME OVER ----------
        bola_jatuh = bola.rect.y + bola.rect.height >= TINGGI_LAYAR
        monster_habis = len(monster) == 0

        if bola_jatuh:
            game_selesai = True
            hasil_game = "YOU LOSE"

        if monster_habis:
            game_selesai = True
            hasil_game = "YOU WIN"

    # ---------- DRAW ----------
    for m in monster:
        m.draw()

    platform.draw()
    bola.draw()

    if game_selesai:
        tulisan = Label(120, 220, 260, 60)
        warna = (255, 0, 0) if hasil_game == "YOU LOSE" else (0, 255, 0)
        tulisan.set_text(hasil_game, 60, warna)
        tulisan.draw()

    pygame.display.update()
    jam.tick(60)

pygame.quit()
