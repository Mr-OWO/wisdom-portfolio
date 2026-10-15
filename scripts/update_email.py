import sqlite3

conn = sqlite3.connect('data/portfolio.db')
c = conn.cursor()
c.execute("UPDATE site_metadata SET contact_email = 'contact@wisdomowabor.online, wisdomowabor1@gmail.com' WHERE id = 1")
conn.commit()
c.execute("SELECT id, full_name, contact_email FROM site_metadata")
print("Updated site metadata:", c.fetchone())
conn.close()
