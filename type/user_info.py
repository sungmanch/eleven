class UserInfo:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.age = kwargs.get("age")
        self.gender = kwargs.get("gender")
        self.location = kwargs.get("location")
        self.id = kwargs.get("id")

    def __str__(self):
        return f"UserInfo(name={self.name}, age={self.age}, gender={self.gender}, location={self.location})"
