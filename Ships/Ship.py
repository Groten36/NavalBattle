class Ship:
    def __init__(self, id:int,length:int, orientation:str,coordinates:list):
        self.id = id
        self.length=length
        self.hits=0
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
        print("A tu kurwa")
        if hit_coordinates not in self.coordinates:
            return False

        self.hits+=1
        print(f"Czy to sie kurwa odpala {self.hits}")
        #do poprawy jak zaczną wątki działać
        if self.hits == self.length:
            self.is_sunk = True
            print(f"!!! Statek  zatonął! !!!")


        return self.is_sunk

