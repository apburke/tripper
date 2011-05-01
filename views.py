from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404
import calendar

def home(request):
    return render_to_response('calendar.html', {'calendar': calendar.HTMLCalendar().formatmonth(2011, 1)})

def year(request, year):
    return render_to_response('calendar.html',
            {'calendar': calendar.HTMLCalendar().formatyear(int(year), width=4)})

def month_view(request, year, month):
    try:
        year = int(year)
	month = int(month)
    except TypeError:
        raise Http404()
    p_m = (month-1+11)%12+1
    n_m = (month+1+11)%12+1
    previous_month = {'year': year if month>1 else year-1,
                      'month': "{0:02d}".format(p_m),
		      'month_name': calendar.month_name[p_m]}
    next_month = {'year': year if month<12 else year+1,
                  'month': "{0:02d}".format(n_m),
		  'month_name': calendar.month_name[n_m]}
    return render_to_response('month.html',
        {'day_names': calendar.day_name[:],
	 'week_list': calendar.Calendar().monthdayscalendar(year, month),
	 'current_month': {'year': year, 'month': month, 'month_name': calendar.month_name[month]},
	 'previous_month': previous_month,
	 'next_month': next_month
	})
