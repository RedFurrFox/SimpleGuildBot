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
    tables = [
        {
            'name': 'blacklist',
            'columns': [
                'id INTEGER PRIMARY KEY',
                'uid TEXT',
                'name TEXT',
                'date_when TEXT',
                'reason TEXT'
            ]
        },
        {
            'name': 'server_configs',
            'columns': [
                'id INTEGER PRIMARY KEY',
                'server_id TEXT',
                'log_channel TEXT',
                'admin_role_id TEXT',
                'antiraid_mode BOOLEAN',
                'antiraid_hardened_mode BOOLEAN',
                'lockdown_mod BOOLEAN',
                'auto_lockdown BOOLEAN'
            ]
        },
        {
            'name': 'server_join_cache',
            'columns': [
                'id INTEGER PRIMARY KEY',
                'server_id TEXT',
                'joiner_id TEXT'
            ]
        },
        {
            'name': 'global_switch',
            'columns': [
                'id INTEGER PRIMARY KEY',
                'help_c BOOLEAN'
            ]
        }
    ]

    async with aiosqlite.connect(database_name) as db:
        for table in tables:
            columns = ', '.join(table['columns'])
            await db.execute(f'CREATE TABLE IF NOT EXISTS {table["name"]} ({columns})')

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


async def db_add_entry(table_name=None, **kwargs):
    """
    Add new entry to the specified table.
    :param table_name:str:
    :param kwargs:dict:
    :return:
    """
    if table_name is None:
        return {'status': False, 'error': 'table_name parameter is required'}
    else:
        async with aiosqlite.connect(database_name) as db:
            cursor = await db.execute(f'SELECT * FROM {table_name} WHERE uid = ?', (kwargs.get('uid'),))
            rows = await cursor.fetchall()
            if len(rows) > 0:
                return {"status": False, "error": f"The {table_name} you are trying to add already existed"}
            else:
                columns = ', '.join(kwargs.keys())
                placeholders = ', '.join('?' * len(kwargs))
                values = tuple(kwargs.values())
                await db.execute(f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})', values)
                await db.commit()
                return {"status": True}


async def db_update_entry(table_name=None, uid=None, **kwargs):
    """
    Update an existing entry in the specified table.
    :param table_name:str:
    :param uid:str:
    :param kwargs:dict:
    :return:
    """
    if table_name is None:
        return {'status': False, 'error': 'table_name parameter is required'}
    elif uid is None:
        return {'status': False, 'error': 'uid parameter is required'}
    else:
        async with aiosqlite.connect(database_name) as db:
            cursor = await db.execute(f'SELECT * FROM {table_name} WHERE uid = ?', (uid,))
            rows = await cursor.fetchall()
            if len(rows) == 0:
                return {"status": False, "error": f"The {table_name} you are trying to update does not exist"}
            else:
                set_clause = ', '.join([f'{key} = ?' for key in kwargs.keys()])
                values = tuple(kwargs.values()) + (uid,)
                await db.execute(f'UPDATE {table_name} SET {set_clause} WHERE uid = ?', values)
                await db.commit()
                return {"status": True}


async def db_delete_entry(table_name=None, uid=None):
    """
    Delete an entry from the specified table.
    :param table_name:str:
    :param uid:str:
    :return:
    """
    if table_name is None:
        return {'status': False, 'error': 'table_name parameter is required'}
    elif uid is None:
        return {'status': False, 'error': 'uid parameter is required'}
    else:
        async with aiosqlite.connect(database_name) as db:
            cursor = await db.execute(f'SELECT * FROM {table_name} WHERE uid = ?', (uid,))
            rows = await cursor.fetchall()
            if len(rows) == 0:
                return {"status": False, "error": f"The {table_name} you are trying to delete does not exist"}
            else:
                await db.execute(f'DELETE FROM {table_name} WHERE uid = ?', (uid,))
                await db.commit()
                return {"status": True}
