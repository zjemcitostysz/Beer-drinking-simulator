import pygame
import random
import sys

pygame.init()

# --- OKNO I ROZDZIELCZOŚĆ TELEFONU ---
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Symulator Nocy")

font = pygame.font.SysFont("arial", 28)

# --- Wczytanie obrazów ---
tlo = pygame.image.load("Tlo.jpg")
piwo_img = pygame.image.load("piwo.png")
kibel_img = pygame.image.load("kibel.jpg")
butelki_img = pygame.image.load("butelki.jpg")
kasyno_img = pygame.image.load("Casino.jpg")
blackjack_img = pygame.image.load("blackjack.jpg")
automaty_img = pygame.image.load("automaty.png")
hit_img = pygame.image.load("hit.jpg")
stand_img = pygame.image.load("stand.jpg")

# --- PRZESKALOWANIE ---
tlo = pygame.transform.scale(tlo, (WIDTH, HEIGHT))
przycisk_w, przycisk_h = WIDTH//6, HEIGHT//6

piwo_img = pygame.transform.scale(piwo_img, (przycisk_w, przycisk_h))
kibel_img = pygame.transform.scale(kibel_img, (przycisk_w, przycisk_h))
butelki_img = pygame.transform.scale(butelki_img, (przycisk_w, przycisk_h))
kasyno_img = pygame.transform.scale(kasyno_img, (przycisk_w, przycisk_h))
blackjack_img = pygame.transform.scale(blackjack_img, (przycisk_w, przycisk_h))
automaty_img = pygame.transform.scale(automaty_img, (przycisk_w, przycisk_h))
hit_img = pygame.transform.scale(hit_img, (przycisk_w//2, przycisk_h//2))
stand_img = pygame.transform.scale(stand_img, (przycisk_w//2, przycisk_h//2))

# --- POZYCJE PRZYCISKÓW ---
gap = (WIDTH - przycisk_w*4) // 5
piwo_rect = piwo_img.get_rect(topleft=(gap, HEIGHT - przycisk_h - 20))
kasyno_rect = kasyno_img.get_rect(topleft=(gap*2 + przycisk_w, HEIGHT - przycisk_h - 20))
butelki_rect = butelki_img.get_rect(topleft=(gap*3 + przycisk_w*2, HEIGHT - przycisk_h - 20))
kibel_rect = kibel_img.get_rect(topleft=(gap*4 + przycisk_w*3, HEIGHT - przycisk_h - 20))

# --- STATS ---
piwa = 0
promile = 0.0
pecherz = 0
kasa = 50
zbierania = 0
MAX_ZBIERAN = 5
zmeczenie = 0

# --- FLAGI ---
kasyno_open = False
blackjack_active = False
blackjack_player = []
blackjack_dealer = []

# --- EVENTY LOSOWE ---
wydarzenia = [
    ("Kolega stawia Ci kolejkę! Pijesz za darmo.", 1, 0.4, 15, 0),
    ("Znalazłeś 20 zł na podłodze!", 0, 0, 0, 20),
    ("Kibel zajęty przez menela. Musisz trzymać!", 0, 0, 20, 0),
    ("Barman daje Ci wodę, żebyś nie padł.", 0, -0.3, 5, 0),
    ("Zagrałeś w rzutki i wygrałeś browara!", 1, 0.4, 15, 0)
]

# --- FUNKCJE ---
def draw_text(txt, x, y):
    render = font.render(txt, True, (255,255,255))
    screen.blit(render, (x,y))

def pokaz_event(tekst, czas=1500):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0,0,0,150))  # półprzezroczyste tło
    screen.blit(overlay, (0,0))
    draw_text(tekst, WIDTH*0.1, HEIGHT*0.45)
    pygame.display.update()
    pygame.time.delay(czas)

def losuj_karte():
    return random.randint(2,11)

def start_blackjack():
    global blackjack_player, blackjack_dealer
    blackjack_player = [losuj_karte(), losuj_karte()]
    blackjack_dealer = [losuj_karte(), losuj_karte()]

def blackjack_hit():
    global blackjack_player
    blackjack_player.append(losuj_karte())

def blackjack_stand():
    global blackjack_player, blackjack_dealer, kasa, blackjack_active
    while sum(blackjack_dealer) < 17:
        blackjack_dealer.append(losuj_karte())
    player_sum = sum(blackjack_player)
    dealer_sum = sum(blackjack_dealer)
    if player_sum > 21 or (dealer_sum <= 21 and dealer_sum > player_sum):
        kasa -= 20
        pokaz_event("Przegrałeś rundę w Blackjack!")
    elif player_sum == dealer_sum:
        pokaz_event("Remis w Blackjack!")
    else:
        kasa += 20
        pokaz_event("Wygrałeś rundę w Blackjack!")
    blackjack_active = False

def automaty(kasa):
    los = random.random()
    if los < 0.4:
        kasa -= 20
        pokaz_event("Przegrałeś na automatach!")
    elif los < 0.85:
        kasa += 20
        pokaz_event("Wygrałeś 20 zł na automatach!")
    else:
        kasa += 60
        pokaz_event("SUPER MEGA BIG MASSIVE SOLID WIN  100 zł!")
    return kasa

clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)
    screen.blit(tlo, (0,0))

    # --- STATYSTYKI ---
    draw_text(f"Kasa: {kasa} zł", WIDTH*0.05, HEIGHT*0.02)
    draw_text(f"Promile: {round(promile,2)}‰", WIDTH*0.05, HEIGHT*0.07)
    draw_text(f"Pęcherz: {pecherz}%", WIDTH*0.05, HEIGHT*0.12)
    draw_text(f"Piwa: {piwa}", WIDTH*0.05, HEIGHT*0.17)
    draw_text(f"Butelki: {zbierania}/{MAX_ZBIERAN}", WIDTH*0.05, HEIGHT*0.22)

    # --- RYSOWANIE PRZYCISKÓW ---
    if not kasyno_open and not blackjack_active:
        screen.blit(piwo_img, piwo_rect)
        screen.blit(kasyno_img, kasyno_rect)
        screen.blit(butelki_img, butelki_rect)
        screen.blit(kibel_img, kibel_rect)
    elif kasyno_open:
        screen.blit(blackjack_img, blackjack_img.get_rect(center=(WIDTH*0.3, HEIGHT*0.5)))
        screen.blit(automaty_img, automaty_img.get_rect(center=(WIDTH*0.7, HEIGHT*0.5)))
        draw_text("Wybierz grę w kasynie", WIDTH*0.3, HEIGHT*0.3)
    elif blackjack_active:
        draw_text("Twoje karty: " + str(blackjack_player), WIDTH*0.05, HEIGHT*0.7)
        draw_text("Krupier: " + str([blackjack_dealer[0], '?']), WIDTH*0.05, HEIGHT*0.75)
        hit_rect = hit_img.get_rect(topleft=(WIDTH*0.3, HEIGHT*0.85))
        stand_rect = stand_img.get_rect(topleft=(WIDTH*0.5, HEIGHT*0.85))
        screen.blit(hit_img, hit_rect)
        screen.blit(stand_img, stand_rect)

    # --- DOTYK / KLIK ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            if not kasyno_open and not blackjack_active:
                # PIWO
                if piwo_rect.collidepoint(pos) and kasa >= 8:
                    kasa -= 8
                    piwa += 1
                    promile += 0.4
                    pecherz += random.randint(10,20)
                    # losowy event
                    if random.random() < 0.3:
                        opis, d_piwa, d_promile, d_pecherz, d_kasa = random.choice(wydarzenia)
                        piwa += d_piwa
                        promile += d_promile
                        pecherz += d_pecherz
                        kasa += d_kasa
                        pokaz_event(opis)
                # BUTELKI
                if butelki_rect.collidepoint(pos) and zbierania < MAX_ZBIERAN:
                    bazowy = random.randint(8,18)
                    zarobek = max(2, bazowy - zmeczenie)
                    kasa += zarobek
                    zbierania += 1
                    zmeczenie += 3
                    if random.random() < 0.3:
                        opis, d_piwa, d_promile, d_pecherz, d_kasa = random.choice(wydarzenia)
                        piwa += d_piwa
                        promile += d_promile
                        pecherz += d_pecherz
                        kasa += d_kasa
                        pokaz_event(opis)
                # KIBEL
                if kibel_rect.collidepoint(pos):
                    pecherz = 0
                    promile = max(0, promile-0.2)
                    if random.random() < 0.3:
                        opis, d_piwa, d_promile, d_pecherz, d_kasa = random.choice(wydarzenia)
                        piwa += d_piwa
                        promile += d_promile
                        pecherz += d_pecherz
                        kasa += d_kasa
                        pokaz_event(opis)
                # KASYNO
                if kasyno_rect.collidepoint(pos):
                    kasyno_open = True
            elif kasyno_open:
                blackjack_rect_menu = blackjack_img.get_rect(center=(WIDTH*0.3, HEIGHT*0.5))
                automaty_rect_menu = automaty_img.get_rect(center=(WIDTH*0.7, HEIGHT*0.5))
                if blackjack_rect_menu.collidepoint(pos):
                    kasyno_open = False
                    blackjack_active = True
                    start_blackjack()
                if automaty_rect_menu.collidepoint(pos):
                    kasyno_open = False
                    kasa = automaty(kasa)
            elif blackjack_active:
                hit_rect = hit_img.get_rect(topleft=(WIDTH*0.3, HEIGHT*0.85))
                stand_rect = stand_img.get_rect(topleft=(WIDTH*0.5, HEIGHT*0.85))
                if hit_rect.collidepoint(pos):
                    blackjack_hit()
                if stand_rect.collidepoint(pos):
                    blackjack_stand()

    # --- WYGRANA ---
    if kasa >= 500 and promile <= 4:
        pokaz_event("WYGRANA! Zebrałeś 500 zł!", 4000)
        running = False

    # --- PRZEGRANA ---
    if promile > 4 or pecherz >= 100:
        pokaz_event("KONIEC GRY! Nie wytrzymałeś...", 4000)
        running = False

    pygame.display.update()

pygame.quit()
sys.exit()