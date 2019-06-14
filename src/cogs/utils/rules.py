import sqlite3

def setrule(key: str, value: str, guildId: int):
        db = sqlite3.connect('rules.db')
        cr = db.cursor()
        if not value == 'get':
            cr.execute('CREATE TABLE IF NOT EXISTS rules(keyword TEXT, value TEXT, server INTEGER)')
            cr.execute('SELECT keyword, server FROM rules')
            varexist: bool = False
            for row in cr.fetchall():
                if value == 'NONE':
                    cr.execute("DELETE FROM rules WHERE keyword = (?) AND server = (?)",
                              (key, guildId))
                    db.commit()
                    return f'```apache\nVariable {key} deleted.```'
                    varexist: bool = True
                    break
                else:
                    if row[0] == key and int(row[1]) == int(guildId):
                        cr.execute("UPDATE rules SET value = (?) WHERE keyword = (?)",
                                  (value, key))
                        db.commit()
                        varexist: bool = True
            if not varexist:
                cr.execute("INSERT INTO rules (keyword, value, server) VALUES (?, ?, ?)",
                         (key, value, guildId))
                db.commit()

        ruleinf = getrule(key, guildId)
        if not ruleinf:
            return '```apache\nNot set.```'
        return f'```apache\n{ruleinf}```'
        cr.close()
        db.close()

def getrule(key: str, guildId: int):
    db = sqlite3.connect('rules.db')
    cr = db.cursor()
    cr.execute('SELECT keyword, value, server FROM rules')
    inf = False
    for row in cr.fetchall():
        if row[0] == key and row[2] == guildId:
            inf = row[1]
    return inf
