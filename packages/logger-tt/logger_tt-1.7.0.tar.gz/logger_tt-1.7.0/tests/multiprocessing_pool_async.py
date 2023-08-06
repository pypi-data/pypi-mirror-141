import time
import sys
from random import randint

from multiprocessing import Pool
from logger_tt import setup_logging
from logging import getLogger


__author__ = "Duc Tin"
logger = getLogger(__name__)
setup_logging(use_multiprocessing=True)


def worker(arg):
    logger.info(f'child process {arg}: started')
    time.sleep(randint(1,10))
    logger.info(f'child process {arg}: stopped')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        proc_no = int(sys.argv[1])
    else:
        proc_no = 7

    logger.info('Parent process pool is ready to spawn child')

    with Pool(proc_no) as p:
        processing_workers = p.map_async(worker, [1, 2, 3, 4, 5])
        processing_workers.get()  # Wait for the workers to finish

    print('__finished__')
