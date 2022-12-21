import logging


def setup_log() -> str:
    from datetime import datetime, timedelta
    import os
    time_format: str = '%d-%m-%Y'
    now: datetime = datetime.now()

    try:
        os.mkdir('logs')
    except FileExistsError:
        try:
            time_change: timedelta = timedelta(days=7)
            not_now: datetime = now + time_change
            os.remove(f'logs/{not_now.strftime(time_format)}.log')
        except IOError:
            pass

    log_name: str = f"logs/{now.strftime(time_format)}.log"
    logging.basicConfig(filename=log_name, datefmt='%d/%m/%Y %Hh%Mm%Ss', encoding='utf8',
                        format='%(levelname)s > %(asctime)s [%(filename)s at %(funcName)s:%(lineno)d] : %(message)s')
