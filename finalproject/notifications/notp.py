from .models import Notification
from cal.models import RDV
from datetime import datetime, timedelta, date
from apscheduler.schedulers.background import BackgroundScheduler
from .updater import update
def update_start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update,'interval',days=1)
    scheduler.start()