class Ship:
    def __init__(self, hp, length, artillery, max_speed,x_coordinate,y_coordinate):
        self.hp=hp
        self.length=length
        self.artillery=artillery
        self.max_speed=max_speed
        self.status=None
        self.x_coordinate=x_coordinate
        self.y_coordinate=y_coordinate

    def setup(self):
        pass

    def shoot(self,artillery_number):
        pass

    def move(self,speed):
        pass

    def take_damage(self,damage):
        pass

    def turn(self,direction):
        pass

    def calculate_damage(self,artillery_number):
        pass

    def lose_artillery(self,artillery_number):
        pass

    def check_status(self):
        pass

    def take_critical_hit(self):
        pass

    def ram(self):
        pass