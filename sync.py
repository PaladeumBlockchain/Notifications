from apscheduler.schedulers.background import BlockingScheduler
from service import sync

background = BlockingScheduler(daemon=True, misfire_grace_time=None)

background.add_job(sync.send_swap_notifications, "interval", seconds=30)
background.add_job(sync.send_notifications, "interval", seconds=30)
background.add_job(sync.check_addresses, "interval", seconds=30)

background.start()
