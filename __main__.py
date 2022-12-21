from package.gui.basic_window import BasicWindow
import logging

bw: BasicWindow = BasicWindow()
logfile_name: str

if __name__ == '__main__':
    from package.utils.log_handler import *
    from package.utils.log_handler import *

    setup_log()
    logger: logging.Logger = logging.getLogger("APPS")
    logger.setLevel(logging.INFO)
    logger.info("Démarrage de l'application")
    bw.mainloop()
