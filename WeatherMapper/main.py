import pygame
from Classes import *
from sys import exit
from tkinter import filedialog, Tk
import tkinter as tk
import pandas as pd
import numpy as np

def date_splitter(date):
    global df, column_buttons
    df['temporary date'] = pd.to_datetime(df[date])
    df.insert(loc=0, column='DAY OF YEAR', value=df['temporary date'].dt.dayofyear)
    df.insert(loc=1, column='YEAR', value=df['temporary date'].dt.year)
    df.insert(loc=2, column='MONTH', value=df['temporary date'].dt.month)
    df.insert(loc=3, column='DAY', value=df['temporary date'].dt.day)
    df.drop(columns=['temporary date'])
    column_buttons = []
    counter = 1
    for i in df.columns:
        text = ''
        for j in pd.unique(df[i])[:10]:
            text += str(j) + '\n'
        column_buttons.append(Button('param', i, (0 ,counter*38), text, 'White', 'Black'))
        counter += 1

width, height = 1920,1080
fps = 60
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Title")
clock = pygame.time.Clock()
running = True

#BUTTONS
buttons = []
get_file = Button('get_file', 'Open File', (width-200,height-100), '', 'Green', 'Black')
get_file.filepath = '/home/user/testpad/python/pygame/pandas/WeatherMapper/data/USW00024157.csv'
buttons.append(get_file)
make_chart = Button('make_chart', 'Make Chart', (width-200,height-150), '', 'Green', 'Black')
buttons.append(make_chart)
split_date = Button('split_date', 'Split Date', (width-200,height-200), '', 'Green', 'Black')
buttons.append(split_date)

column_buttons = []

font = pygame.font.Font(None, 50)
free_font = pygame.freetype.Font(None)
hover_text = font.render('', False, '#000000', '#EEEEEE')
hover_rect = hover_text.get_rect(topleft = (0,0))

clicked = (False,False,False)
filepath = ''
df = None
date = ''
date_has_been_split = False
chart_surf = pygame.image.load("output/temp.png").convert()
chart_rect = chart_surf.get_rect(center = (width//2,height//2))

# Boxes for dropping the `active_param` into
param_boxes = []
x_box = pygame.Rect(0,0,200,50)
x_box.midtop = chart_rect.midbottom
param_boxes.append(x_box)
y_box = pygame.Rect(0,0,200,50)
y_box.midright = chart_rect.midleft
param_boxes.append(y_box)
val_box = pygame.Rect(0,0,200,50)
val_box.midleft = chart_rect.midright
param_boxes.append(val_box)
date_box = pygame.Rect(0,0,200,50)
date_box.bottomright = split_date.rect.bottomleft
param_boxes.append(date_box)

# The hitbox used to scroll the parameters
param_hitbox = pygame.Rect(0,0,int(width * .2), height)

active_param = None

chart_values = ['heatmap', df, '', '', '']

while running:
# GET EVENTS
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            if event.mod & pygame.KMOD_CTRL:
                if event.key == pygame.K_o:
                    temp = Tk()
                    get_file.filepath = filedialog.askopenfilename()
                    temp.destroy()

        if event.type == pygame.MOUSEWHEEL:
            if param_hitbox.collidepoint(pos):
                for button in column_buttons:
                    button.rect.bottom += event.y * 42
                    button.start_point = (button.start_point[0], button.start_point[1] + event.y * 42)

        # Mouse Motion
        if event.type == pygame.MOUSEMOTION:
            if clicked[0]:
                if active_param:
                    active_param.rect = active_param.text.get_rect(center = pos)
                # BUTTONS
                for button in buttons:
                    if button.rect.collidepoint(pos):
                        button.is_clicked = True
                    else:
                        button.is_clicked = False
                    button.update()
                # PARAMS
                for button in column_buttons:
                    if button.rect.collidepoint(pos):
                        button.is_clicked = True
                    else:
                        button.is_clicked = False
                    button.update()
            # Check for hover text
            for button in column_buttons:
                if button.rect.collidepoint(pos):
                    if not button.is_clicked:
                        hover_text = font.render(button.head, False, '#000000', '#EEEEEE')
                        hover_rect = hover_text.get_rect(topleft = pos)
                    else: hover_rect = hover_text.get_rect(bottomright = (-1,-1))
                    break
                else: hover_rect = hover_text.get_rect(bottomright = (-1,-1))

        # Check for button clicks
        if event.type == pygame.MOUSEBUTTONDOWN and event.button != 5 and event.button != 4:
            # BUTTONS
            for button in buttons:
                if button.rect.collidepoint(pos):
                    button.is_clicked = True
                else:
                    button.is_clicked = False
                button.update()
            # PARAMS
            for button in column_buttons:
                if button.rect.collidepoint(pos):
                    active_param = button
                    active_param.rect = active_param.text.get_rect(center = pos)
                    button.is_clicked = True
                else:
                    button.is_clicked = False
                button.update()
            clicked = pygame.mouse.get_pressed()

        if event.type == pygame.MOUSEBUTTONUP and event.button != 5 and event.button != 4:
            for button in buttons:
                if button.is_clicked:
                    if button.btype == 'get_file':
                        button.set_filepath()
                    elif button.btype == 'make_chart' and not any(item == '' for item in [chart_values[2], chart_values[3], chart_values[4]]):
                        chart = Chart(*chart_values)
                        chart_surf = pygame.image.load(chart.make_chart()).convert()
                    elif button.btype == 'split_date' and date and not date_has_been_split:
                        date_splitter(date)
                        date_has_been_split = True

                button.is_clicked = False
                button.update()
            for button in column_buttons:
                if button.is_clicked:
                    if button.rect.colliderect(x_box):
                        chart_values[2] = button.string
                    elif button.rect.colliderect(y_box):
                        chart_values[3] = button.string
                    elif button.rect.colliderect(val_box):
                        chart_values[4] = button.string
                    elif button.rect.colliderect(date_box):
                        date = button.string

                button.is_clicked = False
                button.update()
            if active_param:
                active_param.rect = active_param.text.get_rect(topleft = active_param.start_point)
                active_param = None
            clicked = (False,False,False)
# EVENTS OVER

    if get_file.filepath != filepath:
        column_buttons = []
        if get_file.filepath[-3:] == 'csv':
            df = pd.read_csv(get_file.filepath, low_memory=False)
            counter = 1
            for i in df.columns:
                text = ''
                for j in pd.unique(df[i])[:10]:
                    text += str(j) + '\n'
                column_buttons.append(Button('param', i, (0 ,counter*38), text, 'White', 'Black'))
                counter += 1
            date_has_been_split = False
        filepath = get_file.filepath
        chart_values[1] = df

    screen.fill((255,255,255))

    screen.blit(chart_surf, chart_rect)
    for button in buttons:
        screen.blit(button.text, button.rect)
    for button in column_buttons:
        screen.blit(button.text, button.rect)
    screen.blit(hover_text, hover_rect)


    #Draw value boxes
    x_param = font.render(chart_values[2], False, 'Black')
    y_param = font.render(chart_values[3], False, 'Black')
    val_param = font.render(chart_values[4], False, 'Black')
    date_param = font.render(date, False, 'Black')
    x_box.w = max(x_box.w, x_param.get_rect().w + 5)
    y_box.w = max(y_box.w, y_param.get_rect().w + 5)
    val_box.w = max(val_box.w, val_param.get_rect().w + 5)
    for box in param_boxes:
        pygame.draw.rect(screen, 'White', box)
        pygame.draw.rect(screen, 'Black', box, 2)
    screen.blit(x_param, x_box)
    screen.blit(y_param, y_box)
    screen.blit(val_param, val_box)
    screen.blit(date_param, date_box)
    if active_param:
        screen.blit(active_param.text, active_param.rect)

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
