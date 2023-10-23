import pygame
from sys import exit
from Classes import *
from Functions import dict_fill, get_coordinate, read_file
from Settings import *

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tornadoes")
clock = pygame.time.Clock()
running = True

text = pygame.font.Font(None, 50)
load_map = pygame.image.load('us_map.png').convert()
map_surface = pygame.transform.scale(load_map, (width, height))

csv_generator = read_file()






pepe_generator = read_file()
naders = []
nader_dict = dict_fill()
iter_dict = iter(nader_dict)

for entry in pepe_generator:
    nader_dict[entry[0]].append([entry[1], entry[2]])






line_timer = pygame.USEREVENT + 1
pygame.time.set_timer(line_timer, 10)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == line_timer:
            for nader in naders:
                nader.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            if event.key == pygame.K_f:
                pygame.display.toggle_fullscreen()

    #try:
    #    date, start, end = next(csv_generator)
    #except:
    #    pass
    #l_start,l_end = get_coordinate(float(start[0]), float(start[1]), float(end[0]), float(end[1]))
    #naders.append(Tornado(l_start, l_end))

    try:
        date = next(iter_dict)
        for start, end in nader_dict[date]:
            l_start,l_end = get_coordinate(float(start[0]), float(start[1]), float(end[0]), float(end[1]))
            naders.append(Tornado(l_start, l_end))
    except:
        pass

    # Setup a drawing surface with alpha (crappy workaround for not being able to draw transparent lines)
    draw_surf = pygame.Surface((width, height), pygame.SRCALPHA)
    draw_surf.fill(pygame.Color('#00000000'))

    for i, nader in enumerate(naders):
        pygame.draw.line(draw_surf, (255, 0, 255, nader.alpha), nader.start, nader.current, 1)
        pygame.draw.circle(draw_surf, (255, 0, 255, nader.alpha), nader.current, cat)
        if nader.done:
            naders.pop(i)

    date_text = text.render(date, False, 'Green', 'Black')
    date_rect = date_text.get_rect(bottomleft = (50, height - 50))
    screen.blit(map_surface, (0,0))
    screen.blit(draw_surf, (0,0))
    screen.blit(date_text, date_rect)

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
