import Base

class Vector2():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return (f'({self.x}, {self.y})')

    def Add(self, vec2):
        self.x += vec2.x
        self.y += vec2.y
    def Substract(self, vec2):
        self.x -= vec2.x
        self.y -= vec2.y
    def Multiply(self, vec2):
        self.x *= vec2.x
        self.y *= vec2.y
    def Divide(self, vec2):
        self.x /= vec2.x
        self.y /= vec2.y
    
    def Add(vec1, vec2):
        return Vector2(vec1.x + vec2.x, vec1.y + vec2.y)        
    def Substract(vec1, vec2):
        return Vector2(vec1.x - vec2.x, vec1.y - vec2.y)
    def Multiply(vec1, vec2):
        return Vector2(vec1.x * vec2.x, vec1.y * vec2.y)
    def Divide(vec1, vec2):
        return Vector2(vec1.x / vec2.x, vec1.y / vec2.y)

    def magnitude(self):
        return Base.root((self.x * self.x) + (self.y * self.y), 2)

    def normalized(self):
        lenght = self.magnitude()
        return Vector2(self.x/lenght, self.y/lenght)
        
    def Normalize(self):
        lenght = self.magnitude()
        self.x /= lenght
        self.y /= lenght

    @staticmethod
    def Lerp(vec1, vec2, t):
        return Vector2(Base.lerp(vec1.x, vec2.x, t), Base.lerp(vec1.y, vec2.y, t))
