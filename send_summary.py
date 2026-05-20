import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import os

TODOIST_TOKEN = os.environ['TODOIST_API_TOKEN']
GMAIL_PASSWORD = os.environ['GMAIL_APP_PASSWORD']
GMAIL_ADDRESS = 'karenain@gmail.com'

# 디버깅
print(f"토큰 앞 5자: {TODOIST_TOKEN[:5]}")

res = requests.get(
'https://api.todoist.com/api/v1/tasks',
    headers={'Authorization': f'Bearer {TODOIST_TOKEN}'}
)
print(f"응답 코드: {res.status_code}")
print(f"응답 내용: {res.text[:200]}")

tasks = res.json()

def get_tasks(due_date):
    return [t['content'] for t in tasks if t.get('due') and t['due']['date'] == due_date]

today = datetime.now().strftime('%Y-%m-%d')
tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
day_after = (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')

def fmt(tasks):
    return '\n'.join(f'• {t}' for t in tasks) if tasks else '• 없음'

body = f"""오늘 ({today})
{fmt(get_tasks(today))}

내일
{fmt(get_tasks(tomorrow))}

모레
{fmt(get_tasks(day_after))}
"""

msg = MIMEText(body, 'plain', 'utf-8')
msg['Subject'] = f'📋 할 일 요약 {today}'
msg['From'] = GMAIL_ADDRESS
msg['To'] = GMAIL_ADDRESS

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(GMAIL_ADDRESS, GMAIL_PASSWORD)
    smtp.send_message(msg)

print('전송 완료')
