#!/usr/bin/env python3
import pygame as pg
import sys
from pygame import sprite
from os import path
from settings import *
from sprites import *
from UltraColor import *
from tilemap import *
from maps import *
import pytmx
from pytmx.util_pygame import load_pygame

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()


    def load_data(self):
        game_folder = path.dirname(__file__)
        image_folder = path.join(game_folder, 'images')
        map_folder = path.join(game_folder, 'maps')
        self.map = TiledMap(path.join(map_folder, 'Tile1.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.spritesheet = Spritesheet(path.join(image_folder, 'mousie1.png'))



    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.portals = pg.sprite.Group()
        #for row, tiles in enumerate(self.map.data):
            #for col, tile in enumerate(tiles):
                #if tile == '1':
                    #Wall(self, col, row)
                #if tile == 'P':
                    #self.player = Player(self, col, row)
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'player':
                self.player = Player(self, tile_object.x, tile_object.y)
            if tile_object.name == 'TPZone':
                # tile_object.properties['level'])
                Portals(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, tile_object.properties)
            if tile_object.name == 'Wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
        self.camera = Camera(self.map.width, self.map.height)

    def new_level(self, map_file='Door1.tmx'):
        game_folder = path.dirname(__file__)
        image_folder = path.join(game_folder, 'images')
        map_folder = path.join(game_folder, 'maps')
        self.map = TiledMap(path.join(map_folder, map_file))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

    def run(self):
        #game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()


    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        #update portion of the game loop
        pp = pprint.PrettyPrinter(depth=1000)
        self.all_sprites.update()
        for portal in sprite.spritecollide(self.player, self.portals, False):
            level = portal.properties['level']
            print(level)
            self.new_level(map_file="Door%s.tmx" % level)
            self.new()

        self.camera.update(self.player)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, Color.LightGray, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, Color.LightGray, (0, y), (WIDTH, y))

    def draw(self):
        #self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
                #self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pg.display.flip()

    def events(self):
        #catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass



#create the game object
g = Game()
g.show_start_screen()
# don't call the new() method every frame D:
# That's an object constructor!!
g.new()
while True:
    g.run()
    g.show_go_screen()
