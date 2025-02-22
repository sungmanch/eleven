class UserInfo:
    def __init__(self, name: str, age: int, gender: str, location: str, id: str):
        self.name = name
        self.age = age
        self.gender = gender
        self.location = location
        self.id = id

    def __str__(self):
        return f"UserInfo(name={self.name}, age={self.age}, gender={self.gender}, location={self.location})"
