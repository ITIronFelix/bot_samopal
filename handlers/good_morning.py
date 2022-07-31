from create_bot import bot
import datetime
import sqlite3
import os.path
from os import path
from configure import admin_id
from handlers import note_today

async def hello():
    for filename in os.listdir("user_profiles"):
        if path.splitext(filename)[1] == '.db':
            dtn = datetime.datetime.now()
            date = dtn.strftime("%d.%m.%Y")
            chat = path.splitext(filename)[0]
            mess = f"Доброе утро! Сегодня {date}"
            await bot.send_message(chat, mess)
            await note_today.note_today_show(chat)

async def sing():
    for filename in os.listdir("user_profiles"):
        if path.splitext(filename)[1] == '.db':
            dtn = datetime.datetime.now()
            time = dtn.strftime("%H:%M")
            path1 = 'user_profiles/' + filename
            chat = path.splitext(filename)[0]
            base = sqlite3.connect(path1)
            cur = base.cursor()
            data = cur.execute('SELECT * FROM note_today WHERE time == ? AND status == ? ORDER BY time ASC', (time, '🕔')).fetchall()
            if len(data):
                cur.execute(f"UPDATE note_today SET status == ? WHERE time == ? AND status == ?", ('❌', time, '🕔'))
                base.commit()
                lst = [*(x for t in data for x in t)]
                i = 0
                sms = []
                while i < len(lst):
                    sms.append(lst[i] + " " + lst[i + 1] + " " + lst[i + 2])
                    i += 3
                await bot.send_message(chat, f'Напоминание! \n ⚠️=============================⚠️ \n {sms[0]} \n ⚠️=============================⚠️')
            base.close()


async def note_swap():
    for filename in os.listdir("user_profiles"):
        if path.splitext(filename)[1] == '.db':
            path1 = 'user_profiles/' + filename
            base = sqlite3.connect(path1)
            cur = base.cursor()
            cur.execute('INSERT INTO note_tomorrow(time, description, status) SELECT time, description, status FROM note_today '
                        'WHERE status == ?', ('❌'))
            cur.execute('DELETE FROM note_today')
            cur.execute('INSERT INTO note_today(time, description, status) SELECT time, description, status FROM note_tomorrow')
            cur.execute('DELETE FROM note_tomorrow')
            base.commit()
            base.close()

async def start_bot():
    path = sorted(os.listdir("updates_review"))
    latest_file = path[-1]
    version = latest_file[:7]
    date = latest_file[9:19]
    mess = f'Бот запущен на версии: {version} от {date}'
    await bot.send_message(admin_id, mess)