import json
import logging
import typing
from data_classes.Lists import CategoryList, PlayerList, TaskList, InterfaceList
from discord import Member
from discord.ext import commands

log = logging.getLogger(__name__)
logging.basicConfig()
log.setLevel(logging.DEBUG)

CONFIG_FILE = "config.json"
CATEGORY_LIST_FILE = "data/categories.p"
PLAYER_LIST_FILE = "data/players.p"
TASK_LIST_FILE = "data/tasks.p"
INTERFACE_LIST_FILE = "data/interfaces.p"

def load_critical_config_file(path):
    try:
        with open(path, 'r') as file:
            return json.load(file)
    except (OSError, json.JSONDecodeError) as exc:
        print(str(exc))
        print("Could not load/read {} D:".format(path))
        raise SystemExit

class TaskMistress(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.config = load_critical_config_file(CONFIG_FILE)

        self.category_list = CategoryList(self, CATEGORY_LIST_FILE)
        self.player_list = PlayerList(self, PLAYER_LIST_FILE)
        self.task_list = TaskList(self, TASK_LIST_FILE)
        self.interface_list = InterfaceList(self, INTERFACE_LIST_FILE)

    def save_data(self):
        self.player_list.save()
        self.task_list.save()
        self.interface_list.save()

    def when_mentioned(self, message):
        return [
            '{} '.format(self.user.mention),
            '<@!{}> '.format(self.user.id)]

    async def on_command_error(self, ctx, error):
        await ctx.channel.send(str(error))

    async def on_ready(self):
        log.info("We have logged in as {}".format(self.user))
        # TODO: Check for the presence of an ActionsInterface and CategoriesInfoInterface in the infoChannel.
        # If they don't exist, publish them.
        # If they do, refresh the CategoriesInfoInterface.

    async def on_message(self, message):
        if message.author.bot:
            return  # Ignore bots
        await self.process_commands(message)

    async def on_raw_reaction_add(self, event):
        print(event.emoji.name)
        print(str(event.emoji))


bot = TaskMistress(command_prefix=TaskMistress.when_mentioned)

@bot.command(hidden=True)
async def foo(ctx):
    """Useless testing function."""

@bot.command()
async def assign(ctx, target: Member, task_id: typing.Optional[int]):
    """Give a task to a particular person."""
    raise NotImplementedError

@bot.command()
async def verify(ctx, task_id: int):
    """Verify the completion of a task."""
    raise NotImplementedError

@bot.group()
async def tasks(ctx):
    """Lists tasks you have created."""
    raise NotImplementedError

@tasks.command()
async def create(ctx):
    """Begin the process of creating a new task."""
    raise NotImplementedError

@tasks.command()
async def edit(ctx, task_id: int):
    """Edit a task you have created."""
    raise NotImplementedError

@tasks.command()
async def delete(ctx, task_id: int):
    """Mark a task as deleted."""
    raise NotImplementedError

def main():
    try:
        with open('token.txt', 'r') as file:
            bot.run(file.read())
    except IOError as exc:
        log.exception(exc, exc_info=exc)
        log.error("Could not load/read token.txt D:")
        raise SystemExit


if __name__ == "__main__":
    main()
