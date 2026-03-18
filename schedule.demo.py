import schedule
import time 

def run_every30seconds():
    print("每30秒跑一次")

schedule.every(30).seconds.do(run_every30seconds)

while True:
    schedule.run_pending()
    time.sleep(1)