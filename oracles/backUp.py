import os
import datetime

from apscheduler.schedulers.blocking import BlockingScheduler


def make_daily_mongo_back_up():
    r""" Makes a daily back up of the whole MongoDB at 3 AM.
    """
    scheduler = BlockingScheduler()
    scheduler.add_job(back_up_mongo_to_archive, 'cron', hour=3, minute=0)
    scheduler.start()


def back_up_mongo_to_archive(
        file_name=f'{datetime.datetime.now().date():%Y_%m_%d}_mongo_backUp',
        file_path='/home/wucloud/Dev/BackUp/'):
    r""" Makes a complete backup from MongoDB to an archive using the mongodump command line
    program.
    
    Args:
        file_name (str, optional): 
        file_path (str, optional):
    """
    os.system(f'mongodump --archive="{file_path}{file_name}"')


def main():
    make_daily_mongo_back_up()


if __name__ == "__main__":
    main()