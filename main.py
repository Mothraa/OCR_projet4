import logging


from chess.view import View
# import chess.controller

if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG,
                        filename="logfile.log",
                        filemode="w",  # "a"
                        format='%(asctime)s - %(levelname)s : %(message)s')  # WARNING

    vue = View()
    vue.MainMenu()
    pass


# # #    logging.warning("whoaa!")
