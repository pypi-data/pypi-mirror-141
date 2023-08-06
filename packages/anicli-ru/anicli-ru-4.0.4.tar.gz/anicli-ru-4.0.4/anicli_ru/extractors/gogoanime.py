from anicli_ru.base import *
import re


class Anime(BaseAnimeHTTP):
    BASE_URL = "https://gogoanime.fi/"

    def search(self, q: str) -> ResultList[BaseAnimeResult]:
        r = self.request_get(self.BASE_URL + "search.html", params={"keyword": q}).text
        return AnimeResult.parse(r)

    def ongoing(self, *args, **kwargs) -> ResultList[BaseOngoing]:
        """Вывод онгоингов
        Здесь идёт запрос, который выведет онгоинги"""
        r = self.request_get(self.BASE_URL).text
        return Ongoing.parse(r)

    def episodes(self, *args, **kwargs) -> ResultList[BaseEpisode]:
        """Вывод доступных эпизодов
        Здесь идёт запрос, который выведет эпизоды с найденного Тайтла/Онгоинга

        :param Union[AnimeResult, Ongoing]: - Объект AnimeResult или Ongoing
        """
        r = self.request_get(self.BASE_URL + "/category/serial-experiments-lain")
        return Episode.parse()

    def players(self, *args, **kwargs) -> ResultList[BasePlayer]:
        """Вывод доступных ссылок на видео.
        Здесь необходимо отправить запрос, на котором присутствуют ссылки на видео"""
        return Player.parse()


class AnimeResult(BaseAnimeResult):
    ANIME_HTTP = Anime()
    REGEX = {"url": re.compile("foo (.*?)"),
             "title": re.compile("bar (.*?)")}

    url: str
    title: str

    def __str__(self):
        return f"{self.title}"


class Ongoing(BaseOngoing):
    ANIME_HTTP = Anime()
    REGEX = {}

    def __str__(self):
        return


class Player(BasePlayer):
    ANIME_HTTP = Anime()
    REGEX = {"url": re.compile("url (.*?)")}
    url: str

    def __str__(self):
        return


class Episode(BaseEpisode):
    ANIME_HTTP = Anime()
    REGEX = {}

    def __str__(self):
        return ""
