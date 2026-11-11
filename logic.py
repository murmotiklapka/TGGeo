import sqlite3
from config import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import cartopy.crs as ccrs


class DB_Map():
    def __init__(self, database):
        self.database = database
    
    def create_user_table(self):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS users_cities (
                                user_id INTEGER,
                                city_id TEXT,
                                FOREIGN KEY(city_id) REFERENCES cities(id)
                            )''')
            conn.commit()

    def add_city(self,user_id, city_name):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM cities WHERE city=?", (city_name,))
            city_data = cursor.fetchone()
            if city_data:
                city_id = city_data[0]  
                conn.execute('INSERT INTO users_cities VALUES (?, ?)', (user_id, city_id))
                conn.commit()
                return 1
            else:
                return 0

            
    def select_cities(self, user_id):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT cities.city 
                            FROM users_cities  
                            JOIN cities ON users_cities.city_id = cities.id
                            WHERE users_cities.user_id = ?''', (user_id,))

            cities = [row[0] for row in cursor.fetchall()]
            return cities


    def get_coordinates(self, city_name):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT lat, lng
                            FROM cities  
                            WHERE city = ?''', (city_name,))
            coordinates = cursor.fetchone()
            return coordinates

    def create_grapf(self, path, cities):
        for city in cities:
            cord = self.get_coordinates(city)
            if cord:
                lat, lng = cord
                plt.figure(figsize=(10, 5))
                ax = plt.axes(projection=ccrs.PlateCarree())
                img = plt.imread("Blue_Marble_2002.png")
                ax.imshow(img, extent=[-180, 180, -90, 90], transform=ccrs.PlateCarree())
                ax.plot(lng + 0.5 , lat + 3 , marker='x', color='blue', markersize=10)
                plt.savefig(path)

        
    def draw_distance(self, path, city1, city2):
        ax = plt.axes(projection=ccrs.PlateCarree())
        img = plt.imread("Blue_Marble_2002.png")
        ax.imshow(img, extent=[-180, 180, -90, 90], transform=ccrs.PlateCarree())
        ny_lat, ny_lon = self.get_coordinates(city1)
        delhi_lat, delhi_lon = self.get_coordinates(city2)
        plt.plot([ny_lon, delhi_lon], [ny_lat, delhi_lat],
                color='purple', linestyle='-', linewidth=1, marker='x',
                transform=ccrs.PlateCarree(),
                )
        plt.plot([ny_lon, delhi_lon], [ny_lat, delhi_lat],
                color='cyan', linestyle='--', linewidth=2, marker='x',
                transform=ccrs.PlateCarree(),
                )
        plt.text(ny_lon - 3, ny_lat - 12, city1, color = 'cyan',
                horizontalalignment='right',
                transform=ccrs.PlateCarree()
                )
        plt.text(delhi_lon + 3, delhi_lat - 12, city2, color = 'red',
                horizontalalignment='left',
                transform=ccrs.PlateCarree()
                )
        plt.savefig(path)


if __name__=="__main__":
    
    m = DB_Map(DATABASE)
    m.create_user_table()
