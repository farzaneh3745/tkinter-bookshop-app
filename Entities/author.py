class Author:
    def __init__(self,id,firstname,lastname):
        self.id=id
        self.firstname=firstname
        self.lastname=lastname

    def get_fullname(self):
        return f"{self.firstname} {self.lastname}"