import sqlite3

conn = sqlite3.connect('data/portfolio.db')
c = conn.cursor()
try:
    c.execute("ALTER TABLE site_metadata ADD COLUMN profile_image_url TEXT DEFAULT '/static/img/wisdom_avatar.jpg'")
    conn.commit()
    print("Added profile_image_url column successfully.")
except Exception as e:
    print("Column status:", e)

c.execute("UPDATE site_metadata SET profile_image_url = '/static/img/wisdom_avatar.jpg' WHERE id = 1")
conn.commit()

c.execute("SELECT id, full_name, profile_image_url FROM site_metadata")
print("Site metadata record:", c.fetchone())
conn.close()
