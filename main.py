import logging


from chess.controller import Controller
# import chess.controller

if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG,
                        filename="logfile.log",
                        filemode="w",  # "a"
                        format='%(asctime)s - %(levelname)s : %(message)s')  # WARNING

    controller = Controller()

    controller.run()
# # #    logging.warning("whoaa!")


