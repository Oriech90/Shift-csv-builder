from datetime import datetime, timedelta
from cal_setup import get_calendar_service


def main():
    # creates one hour event tomorrow 10 AM IST
    service = get_calendar_service()

    # d = datetime.now().date()
    # tomorrow = datetime(d.year, d.month, d.day, 00)+timedelta(days=1)
    # start = tomorrow.isoformat()
    # end = (tomorrow + timedelta(days=1)).isoformat()

    d = datetime.now().date()
    tomorrow = datetime(d.year, d.month, d.day) + timedelta(days=1)
    start_date = tomorrow.strftime("%Y-%m-%d")
    end_date = (tomorrow + timedelta(days=1)).strftime("%Y-%m-%d")

    event_result = service.events().insert(calendarId='primary',
                                           body={
                                               "summary": 'Automating calendar',
                                               "description": 'This is a tutorial example of automating google calendar with python',
                                               "start": {"date": start_date},
                                               # "timeZone": 'Asia/Kolkata'
                                               "end": {"date": end_date},

                                           },
                                           ).execute()

    print("created event")
    print("id: ", event_result['id'])
    print("summary: ", event_result['summary'])
    print("starts at: ", event_result['start']['date'])
    print("ends at: ", event_result['end']['date'])


if __name__ == '__main__':
    main()
