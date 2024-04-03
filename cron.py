import schedule
import datetime
import time
import os
import pytz
import threading
import pymysql

def run_job_with_timeout(job_func, timeout_seconds):
    def wrapper():
        start_time = datetime.datetime.now()
        job_thread = threading.Thread(target=job_func)
        job_thread.start()
        job_thread.join(timeout=timeout_seconds)
        end_time = datetime.datetime.now()
        elapsed_time = (end_time - start_time).total_seconds()
        if job_thread.is_alive():
            job_thread.join()
            print(f"{job_func.__name__} took too long ({elapsed_time} seconds), restarting...")
        else:
            print(f"{job_func.__name__} completed in {elapsed_time} seconds at {end_time}")

    return wrapper

def main2():
    os.system("python main2.py")

def astrata_check_status():
    os.system("python astrata-check-status.py")

def astrata_update():
    os.system("python astrata-update.py")
    
counter = 0;

def astrata_check_update():
    global counter
    
    if(counter == 0 or counter % 5 == 0):
        os.system("python astrata-check-status.py")
    else:
        os.system("python astrata-update.py")
    
    counter += 1

def clean_database():
    os.system("python clean-database.py")

def schedule_jobs():
    # Lịch chạy main2 mỗi 30 giây, với thời gian chạy tối đa 600 giây (10 phút)
    #schedule.every(30).seconds.do(run_job_with_timeout(main2, 60))
    # Lịch chạy astrata_check_status mỗi 10 phút, với thời gian chạy tối đa 600 giây (10 phút)
    #schedule.every(10).minutes.do(run_job_with_timeout(astrata_check_status, 600))

    # Lịch chạy astrata_update mỗi 1 phút, với thời gian chạy tối đa 600 giây (10 phút)
    #schedule.every(1).minutes.do(run_job_with_timeout(astrata_update, 600))
    
    schedule.every(1).minutes.do(run_job_with_timeout(astrata_check_update, 60))

    # Lịch chạy clean_database vào 00h15p hàng ngày, với thời gian chạy tối đa 600 giây (10 phút)
    schedule.every().day.at("00:15").do(run_job_with_timeout(clean_database, 60))

class ScheduleThread(threading.Thread):
    def run(self):
        schedule_jobs()
        while True:
            schedule.run_pending()
            time.sleep(1)

if __name__ == "__main__":
    scheduler_thread = ScheduleThread()
    scheduler_thread.start()
    print("Press Ctrl+{0} to exit".format('Break' if os.name == 'nt' else 'C'))

    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler_thread.join()
        print("\nExiting...")
        exit()
