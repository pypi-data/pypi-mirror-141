# holyshit.py

An experimental wrapper for the holyshit API.  
This is asynchronous, meaning that you can use it within your Discord bot without making blocking calls

## Installation
PyPi wheel (stable)
```bash
$ python3.8 -m pip install holyshit # requires Python 3.8+ for aiohttp compatibility
```

Git source (unstable)
```bash
$ python3.8 -m pip install git+https://github.com/cobaltgit/holyshit # requires Python 3.8+ for aiohttp compatibility
```

## Examples

discord.py bot command
```py
from holyshit import Client
...
@bot.command(name="slap")
async def slap(ctx: commands.Context, member: discord.Member):
    # You can do this one of two ways:

    # Creating a client without specifying an aiohttp.ClientSession object
    client = await Client.create()
    try: # context managers will be implemented soon, this is very rough
        slap_img = await client.slap()
        await ctx.send(f"You slapped {member.mention}!\n{slap_img}")
    finally:
        await client.close()
    # attempting to interact with the client beyond the close statement will raise an error

    # Specifying an aiohttp.ClientSession object
    async with aiohttp.ClientSession() as session:
        client = Client(session=session)
        slap_img = await client.slap()
        await ctx.send(f"You slapped {member.mention}!\n{slap_img}")
        # no need to use try...finally as we're within a context manager for the aiohttp session 
        # will raise an error when attempting to interact with the client outside the context manager
```
