import pygame
from random import randint
import numpy as np

c_white = (255, 255, 255)
c_gray = (200, 200, 200)
c_black = (0, 0, 0)
c_blue = (255, 0, 0)
scrH = 800
scrW = 800

density = "N@#W$9876543210?!abc;:+=-,._   "

def get_ascii(rg_color):
    avg_val = 0
    for i in range(3):
        avg_val += rg_color[i]
    avg_val /= 3
    avg_val = int(avg_val)
    str_pos = int((avg_val/255)*len(density))
    dns = len(density)-str_pos-1
    if dns < 1: dns = 0
    return density[dns]

def main():
    pygame.init()
    clock = pygame.time.Clock()
    fontx = pygame.font.SysFont("arial", 12)
    imgg = pygame.image.load(r'C:\Users\pl77906\Desktop\poke_small.jpg')
    scr = pygame.display.set_mode((imgg.get_width(), imgg.get_height()))
    pxarr = pygame.PixelArray(imgg)
    str_line = ''

    for i in range(imgg.get_height()):
        for j in range(imgg.get_width()):
            tmp_color = imgg.unmap_rgb(pxarr[j, i])
            tmp_str = get_ascii(tmp_color)
            str_line += tmp_str
        str_line += "\n"

    with open(r"C:\Users\pl77906\Desktop\out.txt", "w") as text_file:
        text_file.write(str_line)
    text_file.close()

if __name__ == "__main__":
    main()