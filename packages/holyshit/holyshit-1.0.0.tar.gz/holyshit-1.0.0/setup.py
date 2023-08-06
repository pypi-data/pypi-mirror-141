# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['holyshit']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.0']

setup_kwargs = {
    'name': 'holyshit',
    'version': '1.0.0',
    'description': 'Asynchronous experimental wrapper for the holyshit.wtf API',
    'long_description': '# holyshit.py\n\nAn experimental wrapper for the holyshit API.  \nThis is asynchronous, meaning that you can use it within your Discord bot without making blocking calls\n\n## Installation\nPyPi wheel (stable)\n```bash\n$ python3.8 -m pip install holyshit # requires Python 3.8+ for aiohttp compatibility\n```\n\nGit source (unstable)\n```bash\n$ python3.8 -m pip install git+https://github.com/cobaltgit/holyshit # requires Python 3.8+ for aiohttp compatibility\n```\n\n## Examples\n\ndiscord.py bot command\n```py\nfrom holyshit import Client\n...\n@bot.command(name="slap")\nasync def slap(ctx: commands.Context, member: discord.Member):\n    # You can do this one of two ways:\n\n    # Creating a client without specifying an aiohttp.ClientSession object\n    client = await Client.create()\n    try: # context managers will be implemented soon, this is very rough\n        slap_img = await client.slap()\n        await ctx.send(f"You slapped {member.mention}!\\n{slap_img}")\n    finally:\n        return await client.close()\n\n    # Specifying an aiohttp.ClientSession object\n    async with aiohttp.ClientSession() as session:\n        client = Client(session=session)\n        try:\n            slapt_img = await client.slap()\n            await ctx.send(f"You slapped {member.mention}!\\n{slap_img}")\n        finally:\n            await client.close()\n```',
    'author': 'cobaltgit',
    'author_email': 'criterion@chitco.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
