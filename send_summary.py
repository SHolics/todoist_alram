import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import os

TODOIST_TOKEN = os.environ['TODOIST_API_TOKEN']
GMAIL_PASSWORD = os.environ['GMAIL_APP_PASSWORD']
GMAIL_ADDRESS = 'karenain@gmail.com'

def get_tasks(due_date):
    res = requests.get(
        'https://api.todoist.com/rest/v2/tasks',
        headers={'Authorization': f'Bearer {TODOIST_TOKEN}'}
    )
    tasks = res.json()
    return [t['content'] for t in tasks if t.get('due') and t['due']['date'] == due_date]

today = datetime.now().strftime('%Y-%m-%d')
tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
day_after = (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')

today_tasks = get_tasks(today)
tomorrow_tasks = get_tasks(tomorrow)
day_after_tasks = get_tasks(day_after)

def fmt(tasks):
    return '\n'.join(f'• {t}' for t in tasks) if tasks else '• 없음'

body = f"""오늘 ({today})
{fmt(today_tasks)}

내일
{fmt(tomorrow_tasks)}

모레
{fmt(day_after_tasks)}
"""

msg = MIMEText(body, 'plain', 'utf-8')
msg['Subject'] = f'📋 할 일 요약 {today}'
msg['From'] = GMAIL_ADDRESS
msg['To'] = GMAIL_ADDRESS

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(GMAIL_ADDRESS, GMAIL_PASSWORD)
    smtp.send_message(msg)

print('전송 완료')
