from modules.features.news import News


class Fakenews(News):
    NAME = "Fakenews"

    def __init__(self, sender, number):
        News.__init__(self, sender, number)

    def handle(self, content):
        News.handle(self, content)
