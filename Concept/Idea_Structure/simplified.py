import aiosqlite, asyncio, json, threading
from guilded import Color, Embed
from guilded.ext import commands

prefix = "!"
database_name = "my_database.db"
bot_owner_ids = [
    ""
]  # Manually add your UserID here to whoever uses this code to access and config your bot globally.
guilded_token = ""   # If you are planning to use secrets (or "os.environ['']"), replace >> "" << to os.environ['']
virustotal_token = ""  # Same goes here

async def create_db():
    """
    Automatically create a database if the selected database is not found.
    :return:
    """
    with open(r"Dictionaries/sqlite_tables.json") as raw_tables:
        tables = json.load(raw_tables)

    async with aiosqlite.connect(database_name) as db:
        for table in tables:
            columns = ', '.join(table['columns'])
            await db.execute(f'CREATE TABLE IF NOT EXISTS {table["name"]} ({columns})')

        await db.commit()

        async with db.execute("SELECT * FROM global_switch") as cursor:
            async for row in cursor:
                if len(row) == 0:
                    await db.execute("""INSERT OR IGNORE INTO global_switch (
                            help_c,
                            ping_c
                        ) VALUES (?)""", (True,True))
                    await db.commit()
                else:
                    pass


async def db_add_entry(table_name=None, **kwargs):
    """
    Add a new entry to the specified table.
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


async def db_search_table(table_name=None, column_name=None, value=None):
    """
    Search for an entry in the specified table.
    :param table_name:str:
    :param column_name:str:
    :param value:str:
    :return:list:
    """
    if table_name is None:
        return {'status': False, 'error': 'table_name parameter is required'}
    elif column_name is None:
        return {'status': False, 'error': 'column_name parameter is required'}
    elif value is None:
        return {'status': False, 'error': 'value parameter is required'}
    else:
        async with aiosqlite.connect(database_name) as db:
            cursor = await db.execute(f'SELECT * FROM {table_name} WHERE {column_name} = ?', (value,))
            rows = await cursor.fetchall()
            return rows


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


async def clear_oldest_user_id():
    """
    Clear the oldest user_id for every 5 minutes based on the different server_id.
    :return:
    """
    while True:
        async with aiosqlite.connect(database_name) as db:
            cursor = await db.execute('SELECT DISTINCT server_id FROM server_join_cache')
            rows = await cursor.fetchall()

            for row in rows:
                cursor = await db.execute(f'SELECT * FROM server_join_cache WHERE server_id = ? ORDER BY id ASC LIMIT 1', (row[0],))
                oldest_row = await cursor.fetchone()

                if oldest_row is not None:
                    await db.execute(f'DELETE FROM server_join_cache WHERE id = ?', (oldest_row[0],))

            await db.commit()

        await asyncio.sleep(300)


client = commands.Bot(commands.when_mentioned_or(prefix), case_insensitive=False, help_command=None)

cache_thread_count = 0  # DO NOT MODIFY

def main():
    @client.event
    async def on_ready():
        await create_db()
        # Prevent creating another thread when the bot went offline (Internet problem) and goes back online again
        if cache_thread_count > 0:
            pass
        else:
            threading.Thread(target=asyncio.run, args=(clear_oldest_user_id(),)).start()
        print("SimpleGuildBot Client Is Online! {0.name} :: {0.id}".format(client.user))

    @client.event()
    async def on_disconnect():
        print("SimpleGuildBot Client Is Offline")

    @client.command(name="help", aliases=["h", "1"])
    async def help_command(ctx, param1=None, param2=None):
        with open(r"Dictionaries/help_layout.json") as raw_help_layout:
            help_layout = json.load(raw_help_layout)

        help_embed = Embed(title="Help Command", description="Prefix = `{0}Help <CATEGORY> <COMMAND-NAME>\n`".format(prefix),color=Color.blue())

        if param1 is None:
            for categories in help_layout:
                if categories["public"]:
                    help_embed.add_field(name=categories["name"], value=categories["defines"], inline=categories["inline"])
        else:
            if param2 is None:
                aliases_cache = []
                for categories in help_layout:
                    for aliases in categories["cogs"]["aliases"]:
                        aliases_cache.append(aliases)
                if param2 in aliases_cache:

            else:
                pass
            """breakdown = value.lower().split()
            # help_embed.add_field(name="Test", value=breakdown, inline=False)
            if breakdown[0] in ["f", "fun", "1"]:
                help_embed.add_field(name="GayMeter", value="generate a random percentage of how gay that user is.", inline=False)
                help_embed.add_field(name="LoveMeter", value="generate a random percentage of how in love they are.", inline=False)
            elif breakdown[0] in ["u", "util", "utils", "utility", "2"]:
                help_embed.add_field(name="Help", value="Show this help page.", inline=False)
                help_embed.add_field(name="Ping", value="Test this bot server latency.", inline=False)
                help_embed.add_field(name="URLScan", value="scan given link and return useful info if it is safe or not.", inline=False)
                help_embed.add_field(name="QR", value="generate a qr code/image.", inline=False)
            elif breakdown[0] in ["m", "mod", "moderation", "3"]:
                help_embed.add_field(name="Kick", value="Kick someone out of this current server.", inline=False)
                help_embed.add_field(name="Ban", value="Ban someone out of this current server.", inline=False)
                help_embed.add_field(name="Report", value="Report someone to be blacklisted.", inline=False)
                help_embed.add_field(name="Config", value="Configure how will this bot functionwork on this current server.", inline=False)
            elif breakdown[0] == "sgb_dev":
                help_embed.add_field(name="GlobalSwitch", value="Enable or disable bot features.", inline=False)
            elif len(breakdown) > 1:
                pass
            else:
                help_embed.add_field(name="Unknown category type", value=f"Type `{prefix}help` for more info.", inline=False)
        help_embed.set_footer(icon_url=ctx.author.avatar, text=f"{ctx.author.name} requested this command.")"""
        await ctx.reply(embed=help_embed, silent=True)

if __name__ == "__main__":
    main()
    client.run(guilded_token)
