class Ship:
    def __init__(self, length:int, orientation:str,coordinates:list):
        self.length=length
        self.hits=set()
        self.orientation=orientation
        self.is_sunk=False
        self.coordinates=coordinates

    def set_position(self, start_x: int, start_y: int, orientation: str):

        self.orientation = orientation
        self.coordinates = []

        for i in range(self.length):
            if orientation == 'horizontal':
                self.coordinates.append((start_x + i, start_y))
            else:
                self.coordinates.append((start_x, start_y + i))

    def is_hit(self, x: int, y: int) -> bool:

        hit_coordinates = (x, y)

        if hit_coordinates not in self.coordinates:
            return False

        self.hits.add(hit_coordinates)

        if len(self.hits) == self.length:
            self.is_sunk = True
            print(f"!!! Statek  zatonął! !!!")
            return True

        return False

