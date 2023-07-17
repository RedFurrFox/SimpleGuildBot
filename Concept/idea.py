import aiosqlite, asyncore
from guilded import Color, Embed
from guilded.ext import commands

database_name = "vol_database.db"
guilded_token = ""
virustotal_token = ""

async def create_db():
	"""
	Automatically create a database if the selected database is not found.
	:return:
	"""
	async with aiosqlite.connect(database_name) as db:
		await db.execute("""
			CREATE TABLE IF NOT EXISTS blacklist (
				id INTEGER PRIMARY KEY,
				uid TEXT,
				name TEXT,
				date_when TEXT,
				reason TEXT
			)
			""")

		await db.execute("""
			CREATE TABLE IF NOT EXISTS server_configs (
				id INTEGER PRIMARY KEY,
				server_id TEXT,
				log_channel TEXT,
				admin_role_id TEXT,
				antiraid_mode BOOLEAN,
				antiraid_hardened_mode BOOLEAN,
				lockdown_mod BOOLEAN,
				auto_lockdown BOOLEAN
			)
			""")

		await db.execute("""
			CREATE TABLE IF NOT EXISTS server_join_cache (
				id INTEGER PRIMARY KEY,
				server_id TEXT,
				joiner_id TEXT
			)
			""")

		await db.execute("""
			CREATE TABLE IF NOT EXISTS global_switch (
				id INTEGER PRIMARY KEY,
				help_c BOOLEAN
			)
			""")
		await db.commit()

		async with db.execute("SELECT * FROM global_switch") as cursor:
			async for row in cursor:
				if len(row) == 0:
					await db.execute("""INSERT OR IGNORE INTO global_switch (
							help_c
						) VALUES (?)""", (False,))
					await db.commit()
				else:
					pass


async def db_add_blacklist(uid=None, name=None, date_when=None, reason=None):
	"""
	Add new entry to blacklist table.
	:param uid:str:
	:param name:str:
	:param date_when:str:
	:param reason:str:
	:return:
	"""
	if uid is None:
		return {'status': False, 'error': 'uid parameter is required'}
	else:
		if name is None:
			name = "NO-RECORDED-NAME-PROVIDED"
		if date_when is None:
			date_when = "NO-RECORDED-DATE-PROVIDED"
		if reason is None:
			reason = "NO-RECORDED-REASON-PROVIDED"

		async with aiosqlite.connect(database_name) as db:
			cursor = await db.execute('SELECT * FROM blacklist WHERE uid = ?', (uid,))
			rows = await cursor.fetchall()
			if len(rows) > 0:
				return {"status": False, "error": "The user you are trying to add already existed"}
			else:
				await db.execute('INSERT INTO blacklist (uid, name, date_when, reason) VALUES (?, ?, ?, ?)', (uid, name, date_when, reason))
				await db.commit()
				return {"status": True}


async def db_add_server_configs(server_id=None):
	"""
	Add new entry to server_configs table.
	:param server_id:str:
	:return:
	"""
	if server_id is None:
		return {'status': False, 'error': 'server_id parameter is required'}
	else:
		async with aiosqlite.connect(database_name) as db:
			cursor = await db.execute('SELECT * FROM server_configs WHERE server_id = ?', (server_id,))
			rows = await cursor.fetchall()
			if len(rows) > 0:
				return {"status": False, "error": "The server_id you are trying to add already existed"}
			else:
				await db.execute('INSERT INTO server_configs (server_id, log_channel, admin_role_id, antiraid_mode, antiraid_hardened_mode, lockdown_mod, auto_lockdown) VALUES (?, ?, ?, ?, ?, ?, ?)', (server_id, "NOT-YET-REGISTERED", "NOT-YET-REGISTERED", False, False, False, False))
				await db.commit()
				return {"status": True}


async def db_add_server_join_cache(server_id=None, joiner_id=None):
	if server_id is None or joiner_id is None:
		return {'status': False, 'error': 'server_id parameter is required'}
	else:
		async with aiosqlite.connect(database_name) as db:
			cursor = await db.execute('SELECT * FROM server_join_cache')
			column = await cursor.fetchall()
			warn = 0
			for row in column:
				if row[1] == server_id and row[2] == joiner_id:
					warn += 1
			if warn > 0:
				return {"status": False, "error": "The server_id you are trying to add already existed"}
			else:
				await db.execute('INSERT INTO server_join_cache (server_id, joiner_id) VALUES (?, ?)', (server_id, joiner_id))
				await db.commit()
				return {"status": True}


