import threading
import time
import random
import queue
from ConstantVariables import *



class Oponent(threading.Thread):
    def __init__(self, target_board):
        super().__init__()
        self.daemon = True
        self.target_board = target_board
        self.is_running = True
        self.is_active = False
        self.move_queue = queue.Queue()

    def run(self):

        while self.is_running:
            if self.is_active:
                self.process_turn()
                self.is_active = False
            time.sleep(0.1)

    def process_turn(self):



        print("AI: Rozpoczynam myślenie...")
        time.sleep(1.5)




        x = random.randint(0, BOARD_SIZE - 1)
        y = random.randint(0, BOARD_SIZE- 1)


        self.move_queue.put((x, y))
        print(f"AI: Wygenerowano ruch i umieszczono w kolejce: ({x}, {y})")

    def stop(self):
        self.is_running = False