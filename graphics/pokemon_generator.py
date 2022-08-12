import urllib.request
import os
from random import randint
import pygame
import csv

c_white = (255, 255, 255)
c_black = (0, 0, 0)
scrH = 450
scrW = 900

def download_file(poke_id):
    link_core = "https://assets.pokemon.com/assets/cms2/img/pokedex/detail/"
    f_name = str(poke_id) + ".png"
    link_full = link_core + f_name
    pic_path = "c:/poke_files/"
    urllib.request.urlretrieve(link_full, pic_path + f_name)

def gen_numbers():
    poke_ids = []
    for i in range(3):
        poke_id = str(randint(1, 890))
        if len(poke_id) == 2:
            poke_id = "0" + poke_id
        elif len(poke_id) == 1:
            poke_id = "00" + poke_id
        poke_ids.append(poke_id)
    return poke_ids

def display_text(scr, fontx, poke_ids, data):
    start_pos_x = 150
    pos_y = 300
    for p_id in poke_ids:
        filter_row = [k for k in data if p_id in k]
        poke_info = filter_row[0].split(";")
        text = fontx.render(p_id, True, c_white)
        scr.blit(text, (start_pos_x - text.get_width()/2, pos_y))
        pos_y += text.get_height() + 3
        text = fontx.render(poke_info[1], True, c_white)
        scr.blit(text, (start_pos_x - text.get_width()/2, pos_y))
        pos_y += text.get_height() + 3
        text = fontx.render("Gen: " + poke_info[3], True, c_white)
        scr.blit(text, (start_pos_x - text.get_width()/2, pos_y))
        pos_y += text.get_height() + 3
        text = fontx.render("Type: " + poke_info[4] + " " + poke_info[5], True, c_white)
        scr.blit(text, (start_pos_x - text.get_width()/2, pos_y))
        pos_y = 300
        start_pos_x += 300

def display_pics(scr, poke_ids, pic_path):
    start_pos_x = 150
    for p_id in poke_ids:
        poke_path = os.path.join(pic_path, p_id + ".png")
        p_img = pygame.image.load(poke_path)
        scr.blit(p_img, (start_pos_x - p_img.get_width()/2, 20))
        start_pos_x += 300

def main():
    pygame.init()
    clock = pygame.time.Clock()
    scr = pygame.display.set_mode((scrW, scrH))
    fontx = pygame.font.SysFont("arial", 20)

    pic_path = "c:/poke_files/"
    try:
        os.mkdir(pic_path)
    except OSError as error:
        print(error)

    csv_path = 'poke_list.csv'
    with open(csv_path, newline='') as csvfile:
        data = list(csv.reader(csvfile))
    poke_info = []
    for data_line in data:
        poke_info.append(data_line[0])

    for fname in os.listdir(pic_path):
        os.unlink(os.path.join(pic_path, fname))

    scr.fill(c_black)

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_SPACE]:
            for fname in os.listdir(pic_path):
                os.unlink(os.path.join(pic_path, fname))
            p_arr = gen_numbers()
            for p_id in p_arr:
                download_file(p_id)

            scr.fill(c_black)
            display_text(scr, fontx, p_arr, poke_info)
            display_pics(scr, p_arr, pic_path)

        pygame.display.flip()
        pygame.time.wait(40)
main()