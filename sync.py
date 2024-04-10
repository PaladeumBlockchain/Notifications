from apscheduler.schedulers.background import BlockingScheduler
from service import sync

background = BlockingScheduler(daemon=True, misfire_grace_time=None)

# background.add_job(sync.send_notifications, "interval", minutes=1)
background.add_job(sync.check_addresses, "interval", minutes=1)

background.start()
