import logging

def setup_logger(logfile='hydrotracker.log'):
    logging.basicConfig(
        filename=logfile,
        level=logging.INFO,
        format='[%(asctime)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger("HydroLogger")
