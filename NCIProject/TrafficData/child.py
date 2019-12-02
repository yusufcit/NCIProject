from kaggle import KaggleApi


class Child(KaggleApi):
    def authenticate(self):
        return self.value + 1
