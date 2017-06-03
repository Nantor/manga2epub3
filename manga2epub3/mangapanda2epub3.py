import logging
import multiprocessing
import os
import urllib.parse
import manga2epub3.mangapanda
import manga2epub3.epub3


class Manga2epub3:
    __base_url = "http://www.mangapanda.com"
    __title_manga = "{0}"
    __title_manga_chapter = "{0} - {1}"
    __file_name_manga = __title_manga + "epub"
    __file_name_manga_chapter = __title_manga_chapter + ".epub"

    def __init__(self, manga_url, dic, separate=True, chapter=None, pool_size=None):
        if pool_size is not None and pool_size < 1:
            pool_size = 1

        self.__pool = multiprocessing.Pool(processes=pool_size)

        self.dic = dic
        self.separate = separate

        if manga_url[0:4] is "http":
            self.manga_url = manga_url
        else:
            self.manga_url = urllib.parse.urljoin(self.__base_url, manga_url)

        self.__chapter = chapter
        self.manga = manga2epub3.mangapanda.Manga(self.manga_url)

    def save(self):
        print("start processing manga: {0}".format(self.manga.title))
        images = []
        if self.separate:
            with self.__pool as pool:
                epubs = []
                for chapter in self.manga.parse(self.__chapter):
                    print("process chapter: {0}".format(chapter.title))
                    file_name = self.__convert_filename(
                        self.__file_name_manga_chapter.format(self.manga.title, chapter.title))
                    title = self.__title_manga_chapter.format(self.manga.title, chapter.title)
                    file_path = os.path.join(self.dic, file_name)
                    epub = manga2epub3.epub3.Epub3(file_path, title)
                    for image in chapter.parse():
                        epub.add_image(image.img_path, image.height, image.width)
                        images.append(pool.apply_async(image.parse))
                    print("stop process chapter: {0}".format(chapter.title))
                    epubs.append(epub)
                print("wait for downloading")
                for i in images:
                    i.wait()
                print("stop downloading")
                print("start creating epubs")
                if self.__chapter is None:
                    creating = []
                    for epub in epubs:
                        creating.append(pool.apply_async(epub.create))
                        # epub.create()
                    for e in creating:
                        e.wait()
                else:
                    epubs[0].create()
            print("created all epubs")
        else:
            with self.__pool as pool:
                file_name = self.__convert_filename(self.__file_name_manga.format(self.manga.title))
                title = self.__title_manga.format(self.manga.title)
                file_path = os.path.join(self.dic, file_name)
                epub = manga2epub3.epub3.Epub3(file_path, title)
                for chapter in self.manga.parse(self.__chapter):
                    print("process chapter: {0}".format(chapter.title))
                    for image in chapter.parse():
                        epub.add_image(image.img_path, image.height, image.width)
                        images.append(pool.apply_async(image.parse))
                    print("stop process chapter: {0}".format(chapter.title))
                print("wait for downloading")
                for i in images:
                    i.wait()
                print("stop downloading")
                print("start creating epub")
                epub.create()
            print("created epub")

    def __worker(self, task, message):
        print("start " + message)
        result = task()
        print("stop " + message)
        return result

    def __convert_filename(self, filename: str):
        return filename.replace(r'<>:"/\\|?*', '_') \
            .replace(r'<', '_') \
            .replace(r'>', '_') \
            .replace(r':', '_') \
            .replace(r'"', '_') \
            .replace(r'/', '_') \
            .replace(r'\\', '_') \
            .replace(r'|', '_') \
            .replace(r'?', '_') \
            .replace(r'*', '_')
