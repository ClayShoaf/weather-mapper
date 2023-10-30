import pygame
from tkinter import filedialog, Tk
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import io
from PIL import Image


class Button():
    def __init__(self, btype, string, location, head='', text_color='Black', bg_color='Gray'):
        self.btype = btype
        self.text_color = text_color
        self.bg_color = bg_color
        self.string = string
        self.start_point = location
        self.filepath = ''
        self.head = head
        self.font = pygame.font.Font(None, 50)
        self.text = self.font.render(self.string, False, self.text_color, self.bg_color)
        self.rect = self.text.get_rect(topleft = location)
        self.is_clicked = False
    def update(self):
        if self.is_clicked:
            self.bg_color = '#AAAAAA'
            self.text = self.font.render(self.string, False, self.text_color, self.bg_color)
        else:
            self.bg_color = '#000000'
            self.text = self.font.render(self.string, False, self.text_color, self.bg_color)
            
    def set_filepath(self):
        temp = Tk()
        self.filepath = filedialog.askopenfilename()
        temp.destroy()


class Chart():
    def __init__(self, ctype, file, x, y, values=None):
        self.ctype = ctype
        self.x = x
        self.y = y
        self.values = values
        self.file = file

    def make_chart(self):
        df = self.file

        chart_data = df[[self.y, self.x, self.values]].pivot(index=self.y, columns=self.x, values=self.values)
        #chart_data = df[['YEAR', 'DAY OF YEAR', self.values]].pivot(index='DAY OF YEAR', columns='YEAR', values=self.values)
        fig, ax = plt.subplots(figsize=(9,9))
        fig.tight_layout(rect=[0.02, 0.03, 1.05, .98])
        test = sns.heatmap(chart_data, cmap='coolwarm')
        test.collections[0].colorbar.set_label("")
        #ax.set_title(f" Weather Station: {df.NAME.iloc[0]}")
        img_buf = io.BytesIO()
        plt.savefig(img_buf, format='png')

        im = Image.open(img_buf)
        im.save('output/temp.png')
        return 'output/temp.png'
