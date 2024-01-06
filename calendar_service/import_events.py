from datetime import datetime, timedelta
from cal_setup import get_calendar_service


def main():
    # import csv file to primary calendar
    service = get_calendar_service()

    event_result = service.events().import_(calendarId='primary', body={
        "attachments": [
            {"fileUrl": "./December shifts_new.csv"}
        ]
    }
    )

    # event_result = service.events().insert(calendarId='primary',
    #                                        body={
    #                                            "summary": 'Automating calendar',
    #                                            "description": 'This is a tutorial example of automating google calendar with python',
    #                                            "start": {"date": start_date},
    #                                            # "timeZone": 'Asia/Kolkata'
    #                                            "end": {"date": end_date},

    #                                        },
    #                                        ).execute()

    print("created event")
    print("id: ", event_result['body'])
    # print("summary: ", event_result['summary'])
    # print("starts at: ", event_result['start']['date'])
    # print("ends at: ", event_result['end']['date'])


if __name__ == '__main__':
    main()
