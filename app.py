import tkinter as tk

from mysql.connector import connect

import datetime


app = tk.Tk()
app.geometry('500x500')

client_full_name_label = tk.Label(app, text='ФИО Клиента')
client_full_name = tk.Entry(app, width='30')

device_label = tk.Label(app, text='Устройство')
device = tk.Entry(app, width=30)

client_full_name_label.place(x=50, y=30)
client_full_name.place(x=50, y=50)

device_label.place(x=50, y=80)
device.place(x=50, y=100)



service_label = tk.Label(app, text='Тип услуги')
service = tk.Entry(app, width=30)

master_label = tk.Label(app, text='Имя мастера')
master = tk.Entry(app, width=30)

price_label = tk.Label(app, text='Цена')
price = tk.Entry(app, width=30)

master_label.place(x=250, y=30)
master.place(x=250, y=50)

service_label.place(x=250, y=80)
service.place(x=250, y=100)

price_label.place(x=250, y=130)
price.place(x=250, y=150)



description_label = tk.Label(app, text='Описание')
description = tk.Entry(app, width=63)

description_label.place(x=50, y=180)
description.place(x=50, y=200)


def create_oreder():
  connection = connect(host='localhost', username='root', database='itshka')
  c = connection.cursor()

  if not device.get() or \
     not client_full_name.get() or \
     not service.get() in ['Diagnose', 'Repair', 'Cleaning'] or \
     not price.get() or \
     not description.get() or \
     not master.get(): return

  c.execute(f"SELECT id FROM clients WHERE full_name LIKE '{client_full_name.get()}' LIMIT 1")
  client_id = c.fetchall()

  if not client_id: return
  
  date_time = datetime.datetime.now()
  date = date_time.strftime("%d.%m.%Y")

  c.execute(f"INSERT INTO accessories(device_name) values ('{device.get()}')")
  connection.commit()

  c.execute(f"SELECT id FROM accessories WHERE device_name LIKE '{device.get()}'")
  device_id = c.fetchall()

  if not device_id: return
  
  c.execute(f"INSERT INTO orders(date, clients_id, price, status, master, description, accessories_id, service) values ('{date}', {client_id[0][0]}, {price.get()}, 'Accepted', '{master.get()}', '{description.get()}', {device_id[0][0]}, '{service.get()}')")
  connection.commit()

  connection.close()

submit = tk.Button(app, text='Создать заказ', width=30, height=5, command=create_oreder)

submit.place(x=135, y=250)



app.mainloop()
