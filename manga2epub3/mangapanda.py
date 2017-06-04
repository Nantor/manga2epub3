import bs4
import math
import os
import pathlib
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid


class Manga:
    def __init__(self, url):
        self.url = url
        self.__base_url = "{0.scheme}://{0.netloc}/".format(urllib.parse.urlsplit(self.url))
        self.__main_page = bs4.BeautifulSoup(urllib.request.urlopen(self.url), "html.parser")
        self.title = self.__main_page.find("h2", "aname").string.strip()

    def parse(self, chapter=None):
        chapters = self.__main_page.find(id="listing").find_all("tr")[1:]
        if chapter is not None:
            a = "".join(chapters[chapter - 1].td.strings).strip()
            url = urllib.parse.urljoin(self.__base_url, chapters[chapter - 1].td.a["href"])
            name = str(a[a.find(":") + 2:]).strip()
            if name == '':
                name = "chapter " + str(chapter)
            yield Chapter(url, name)
        else:
            l = math.ceil(math.log10(len(chapters)))
            for i, _chapter in enumerate(chapters):
                a = "".join(_chapter.td.strings).strip()
                url = urllib.parse.urljoin(self.__base_url, _chapter.td.a["href"])
                name = str(a[a.find(":") + 2:]).strip()
                if name == '':
                    name = "chapter " + str(i + 1).zfill(l)
                yield Chapter(url, name)


class Chapter:
    __temp_dir = tempfile.TemporaryDirectory()

    def __init__(self, url, title):
        self.title = title
        self.url = url

    def parse(self, image=None):
        base_url = "{0.scheme}://{0.netloc}/".format(urllib.parse.urlsplit(self.url))
        response = urllib.request.urlopen(self.url)
        soup = bs4.BeautifulSoup(response, "html.parser")
        img_tag = soup.find(id="img")

        i = 0
        while img_tag is not None:
            img_url = urllib.parse.urljoin(base_url, img_tag.get("src"))
            name = str(uuid.uuid4()).replace("-", "")
            location = os.path.abspath(os.path.join(self.__temp_dir.name, name + ".jpg"))
            img = Image(img_url, location, img_tag['height'], img_tag['width'])
            if image is not None:
                if ++i == image:
                    yield img
                    break
            else:
                yield img

            a_tag = img_tag.parent
            info = a_tag.get("href").split("/")
            if len(info) < 4:
                break
            response = urllib.request.urlopen(urllib.parse.urljoin(base_url, a_tag.get("href")))
            soup = bs4.BeautifulSoup(response, "html.parser")
            img_tag = soup.find(id="img")


class Image:
    def __init__(self, url, img_path, height, width, retries=3):
        self.width = width
        self.height = height
        self.retries = retries
        self.img_path = img_path
        self.url = url

    def parse(self):
        for i in range(1, self.retries):
            try:
                if not pathlib.Path(self.img_path).is_file():
                    img_reg = urllib.request.Request(self.url)
                    img_reg.add_header("User-Agent",
                                       "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0")
                    with urllib.request.urlopen(img_reg) as f:
                        open(self.img_path, "wb").write(f.read())
                    break
                print("file {0} already exist.".format(self.img_path))
                break
            except ValueError and urllib.error.URLError and urllib.error.HTTPError:
                print("Could not download in the {2}. run the image from {1} to {0}".format(self.img_path, self.url, i))
            time.sleep(2)
