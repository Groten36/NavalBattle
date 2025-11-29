import threading
import time
import random
import queue


# from game_classes import Board # Załóżmy, że importujesz planszę gracza

class AIBoard(threading.Thread):
    def __init__(self, target_board):
        super().__init__()
        self.daemon = True  # Wątek zakończy się, gdy główny program się zakończy
        self.target_board = target_board  # Plansza gracza (cel dla AI)
        self.is_running = True  # Flaga do bezpiecznego zatrzymania
        self.is_active = False  # Flaga sygnalizująca, czy AI powinno myśleć
        self.move_queue = queue.Queue()  # Kolejka do przekazywania wyników (ruchów)

    def run(self):
        """Metoda wykonująca się w osobnym wątku."""
        while self.is_running:
            if self.is_active:
                self.process_turn()
                self.is_active = False  # Zakończone myślenie, czekaj na kolejną aktywację
            time.sleep(0.1)  # Krótka pauza, by zwolnić zasoby CPU

    def process_turn(self):
        """Główna logika podejmowania decyzji AI."""

        # 1. FAZA MYŚLENIA (BLOKUJĄCA)
        print("AI: Rozpoczynam myślenie...")
        time.sleep(1.5)  # Symulacja czasu potrzebnego na złożone obliczenia

        # 2. LOGIKA RUCHU
        # Implementacja algorytmu:
        # np. losowe_współrzędne = self.find_random_unshot_target()
        # Lub zaawansowane przeszukiwanie celów (np. tryb Hunt/Target)

        # Przykład losowego ruchu:
        x = random.randint(0, self.target_board.size - 1)
        y = random.randint(0, self.target_board.size - 1)

        # 3. PRZEKAZANIE WYNIKU
        # Przekazujemy wynik strzału (x, y) do głównego wątku za pomocą kolejki
        self.move_queue.put((x, y))
        print(f"AI: Wygenerowano ruch i umieszczono w kolejce: ({x}, {y})")

    def stop(self):
        """Bezpieczne zatrzymanie wątku."""
        self.is_running = False