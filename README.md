# google-calendar-shifts-creator
The program has the option to choose between 2 method executions for this task:
1. The program loads a csv file with shift information('x' in specific row+column) and creates a new csv file, that holds the full information needed for adding the csv file into Google Calendar. branch: create-new-csv
2. The program loads a csv file and do the necessarry parsing in order to create events directly in the calendar, using Google Calendar API. branch: actions_with_calendar_api
