from hitcount.models import HitCount, Hit
from django.db.models import Sum

def daily_visits(day, month, year):
	day = int(day)
	month = int(month)
	year = int(year)
	visits = Hit.objects.filter(
		created__day=day,
		created__month=month,
		created__year=year).count()
	if visits is None:
		visits = 0
	return visits
