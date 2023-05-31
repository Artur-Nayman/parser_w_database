import mysql.connector
from bs4 import BeautifulSoup as bs
from requests import get

conn = mysql.connector.connect(host="localhost", port="3306", user="root", password="root", database="artur_bot")
cursor = conn.cursor()
url = "https://www.eneba.com/store/xbox-game-pass?drms[]=xbox&page=1&regions[]=emea&regions[]=europe&regions[]=finland&regions[]=global&text=game%20pass%20subscription"
r = get(url)
site = bs(r.text, "html.parser")
not_clear_game = site.find_all('span', class_="YLosEL")
not_clear_price = site.find_all('span', class_="L5ErLT")
not_clear_place = site.find_all('div', class_="Pm6lW1")
not_clear_link = site.find_all('div', class_="XFafY_")
gamel = [c.text for c in not_clear_game] # превращает код в текст
game_price =[c.text for c in not_clear_price] # превращает код в текст
placer = [c.text for c in not_clear_place] # превращает код в текст
linker = [c.text for c in not_clear_link] # превращает код в текст
price = [float(price[1:]) for price in game_price] # Превращает в флоат каждый элемент списка не считая превый
game = len(gamel)
n_game = []
n_price = []
#get / update
#получение данных / обновление данных
try:
    # Удаление старых данных
    delete_query = "DELETE FROM xbox"
    cursor.execute(delete_query)

    count = -1
    while count != game:
        count = count + 1
        if price[count] > 20:
            continue
        Title = gamel[count]
        Price = price[count]
        Place = placer[count]
        link = linker[count]
        n_game.append(gamel[count])
        n_price.append(price[count])
        sql = "INSERT INTO xbox (Title, Price, Place, link) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (Title, Price, Place, link))
        conn.commit()

except:
    None

#Get from DB and print
#Получение из БД и вывод
try:
    # Выполнение SQL-запроса для выборки данных
    sql = "SELECT Title, Price FROM xbox"
    cursor.execute(sql)

    # Получение результатов запроса
    results = cursor.fetchall()

    # Вывод данных
    for row in results:
        title = row[0]
        price = row[1]
        print("Title:", title)
        print("Price:", price)

except mysql.connector.Error as error:
    print("Ошибка при выполнении запроса:", error)

cursor.close()
conn.close()

