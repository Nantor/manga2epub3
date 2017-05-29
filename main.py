if __name__ == "__main__":
    import argparse
    import os
    import manga2epub3.mangapanda2epub3
    import logging

    logging.basicConfig(filename='manga.log', level=logging.DEBUG)


    def check_folder(folder):
        if not os.path.isdir(folder):
            os.mkdir(folder)
        return folder


    parser = argparse.ArgumentParser(description='Save a manga from mangapanda.com to a epub3 file')
    parser.add_argument('url', action='store', nargs=1,
                        help='The absolute or relative url to the manga.')
    parser.add_argument('-s', '--single', action='store_true',
                        help='The manga will stored in a single epub instant of a separate epub for each chapter.')
    parser.add_argument('-c', '--chapter', action='store', type=int, nargs=1, default=[None],
                        help='Save only a specific chapter with the chapter number CHAPTER.')
    parser.add_argument('folder', action='store', nargs=1, type=check_folder,
                        help='Path to th folder where the epub(s) will stored.')

    # args = parser.parse_args(["ranma-12", "./ranma-12"])
    # args = parser.parse_args(["ranma-12", "-c", "1", "D:/manga/ranma-12"])
    args = parser.parse_args()
    # args = parser.parse_args(['-h'])

    manga2epub3.mangapanda2epub3.Manga2epub3(args.url[0], args.folder[0], not args.single, args.chapter[0]).save()
