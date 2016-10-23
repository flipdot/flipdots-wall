#!/usr/bin/env python3
# created by swegener
from io import BlockingIOError

import pygame
import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 2323

PIXEL_SIZE = 10

DISPLAY_WIDTH = 48
DISPLAY_HEIGHT = 20
FPS = 60


# while True:
#

def bits(n):
    while n:
        b = n & (~n + 1)
        yield b
        n ^= b


class Display():
    def __init__(self):
        self.matrix = [[0] * DISPLAY_HEIGHT for x in range(DISPLAY_WIDTH)]

    def run(self, sock):
        sock.setblocking(False)
        pygame.init()
        width = DISPLAY_WIDTH * PIXEL_SIZE
        height = DISPLAY_HEIGHT * PIXEL_SIZE
        screen = pygame.display.set_mode((width, height))
        clock = pygame.time.Clock()
        self.running = True
        while self.running:
            try:
                data, addr = sock.recvfrom(2048)  # buffer size is 1024 bytes
            except BlockingIOError:
                data = None
            if data:
                self.handle_data(data)
            clock.tick(FPS)
            self.draw(screen)
            self.handle_events()

    def handle_data(self, data):
        n = 0
        for byte in data:
            for i in range(8):
                bit = byte & 128 >> i
                x = n // DISPLAY_HEIGHT
                y = n % DISPLAY_HEIGHT
                if y == 0 and i != 0:
                    # do not care about the extra bits in the last byte
                    break
                self.matrix[-1 * x][y] = not not bit
                n += 1

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def draw(self, screen):
        screen.fill((0x00, 0x00, 0x00))
        for x in range(DISPLAY_WIDTH):
            x_pos = PIXEL_SIZE * x
            for y in range(DISPLAY_HEIGHT):
                y_pos = PIXEL_SIZE * y
                if self.matrix[x][y]:
                    v = 0xff
                    pygame.draw.rect(screen, (v, v, v), (x_pos, y_pos, PIXEL_SIZE, PIXEL_SIZE))
        pygame.display.flip()


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    display = Display()
    display.run(sock)
