# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['discordpy_logging_handler']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'discordpy-logging-handler',
    'version': '0.1.0',
    'description': 'Forward Discord bot logs to Discord Text channel.',
    'long_description': '# WIP: discordpy-logging-handler\n\nForward Discord bot logs to Discord Text channel.\n\n## Usage\n\n```python\nimport logging\n\nimport discord\nfrom discordpy_logging_handler import DiscordBotHandler\n\n\nLOG_TEXT_CHANNEL_ID = 1111111111111\n\nlogger = logging.getLogger(__name__)\n\n\nclass MyClient(discord.Client):\n    async def on_ready(self):\n        logger.info("Logged on as {0}!".format(self.user))\n\n    async def on_message(self, message):\n        logger.info("Message from {0.author}: {0.content}".format(message))\n\n\nclient = MyClient()\nclient.run("my token goes here")\n\nlog_channel = client.get_channel(LOG_TEXT_CHANNEL_ID)\nlogger.setLevel(logging.DEBUG)\n\nhandler = DiscordBotHandler(log_channel)\nhandler.setLevel(logging.INFO)\n\n# add ch to logger\nlogger.addHandler(handler)\n```\n',
    'author': 'zztkm',
    'author_email': 'takumi.basket1682@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': '',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
