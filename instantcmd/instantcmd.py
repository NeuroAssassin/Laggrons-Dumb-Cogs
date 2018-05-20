# InstantCommands by retke, aka El Laggron
# Idea by Malarne

import discord
import asyncio  # for coroutine checks
import inspect  # for checking is value is a class
import traceback
import random

from discord.ext import commands
from redbot.core import checks
from redbot.core import Config
from redbot.core.utils.chat_formatting import pagify


class InstantCommands:
    """
    Generate a new command from a code snippet, without making a new cog.
    Report a bug or ask a question: https://discord.gg/WsTGeQ
    Full documentation and FAQ: https://github.com/retke/Laggrons-Dumb-Cogs/wiki
    """

    def __init__(self, bot):
        self.bot = bot
        self.data = Config.get_conf(self, 260)

        def_global = {"commands": {}}
        self.data.register_global(**def_global)

        # these are the availables values when creating an instant cmd
        self.env = {
            "bot": self.bot,
            "discord": discord,
            "commands": commands,
            "checks": checks,
        }
        # resume all commands and listeners
        bot.loop.create_task(self.resume_commands())

    __author__ = "retke (El Laggron)"
    __version__ = "Laggrons-Dumb-Cogs/instantcmd beta 2b"

    def get_config_identifier(self, name):
        """Get a random ID from a string for Config"""

        random.seed(name)
        identifier = random.randint(0, 999999)
        self.env["config"] = Config.get_conf(self, identifier)

    def get_function_from_str(self, command, name):
        """
        Execute a string, and try to get a function from it.
        """

        self.get_config_identifier(name)

        old_locals = dict(locals())
        exec(command, self.environement)

        new_locals = dict(locals())
        new_locals.pop("old_locals")

        function = [b for a, b in new_locals.items() if a not in old_locals]
        return function[0]

    def load_command_or_listener(self, function):
        """
        Add a command to discord.py or create a listener
        """

        if isinstance(function, commands.Command):
            self.bot.add_command(function)
        else:
            self.bot.add_listener(function)

    async def resume_commands(self):
        """
        Load all instant commands made.
        This is executed on load with __init__
        """

        _commands = await self.data.commands()
        for name, command_string in _commands.items():
            function = self.get_function_from_str(command_string, name)
            self.load_command_or_listener(function)

    # from DEV cog, made by Cog Creators (tekulvw)
    @staticmethod
    def cleanup_code(content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith("```") and content.endswith("```"):
            return "\n".join(content.split("\n")[1:-1])

        # remove `foo`
        return content.strip("` \n")

    @checks.is_owner()
    @commands.group(aliases=["instacmd", "instantcommand"])
    async def instantcmd(self, ctx):
        """Instant Commands cog management"""

        if not ctx.invoked_subcommand:
            await ctx.send_help()

    @instantcmd.command()
    async def create(self, ctx, name: str):
        """
        Instantly generate a new command from a code snippet.

        If you want to make a listener, give its name instead of the command name.
        """

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        await ctx.send(
            "You're about to create a new command. \n"
            "Your next message will be the code of the command. \n\n"
            "If this is the first time you're adding instant commands, "
            "please read the wiki:\n"
            "<https://github.com/retke/Laggrons-Dumb-Cogs/wiki>"
        )

        try:
            response = await self.bot.wait_for("message", timeout=900, check=check)
        except asyncio.TimeoutError:
            await ctx.send("Question timed out.")
            return

        function_string = self.cleanup_code(response.content)
        self.get_config_identifier()

        # we get all existing functions in this process
        # then we compare to the one after executing the code snippet
        # so we can find the function name
        old_locals = dict(locals())  # we get its dict so it is a static value

        try:
            exec(function_string, self.environement)
        except Exception as e:
            message = (
                "An exception has occured while compiling your code:\n"
                "```py\n"
                "{}```".format(
                    "".join(traceback.format_exception(type(e), e, e.__traceback__))
                )
            )
            for page in pagify(message):
                await ctx.send(page)
            return

        new_locals = dict(locals())
        new_locals.pop("old_locals")  # we only want the exec() functions

        function = [b for a, b in new_locals.items() if a not in old_locals]
        # if the user used the command correctly, we should have one async function

        if len(function) < 1:
            await ctx.send("Error: No function detected")
            return
        if len(function) > 1:
            await ctx.send("Error: More than one function found")
            return
        if inspect.isclass(function[0]):
            await ctx.send("Error: You cannot give a class")
            return

        function = function[0]
        if isinstance(function, commands.Command):

            if name != function.name:
                await ctx.send(
                    "Error: The command's name is different than what you gave when initializing the command.\n"
                )
                return

            async with self.data.commands() as _commands:
                if name in _commands:
                    await ctx.send("Error: That listener is already registered.")
                    return

            try:
                self.bot.add_command(function)

            except Exception as e:
                message = (
                    "An expetion has occured while adding the command to discord.py:\n"
                    "```py\n"
                    "{}```".format(
                        "".join(traceback.format_exception(type(e), e, e.__traceback__))
                    )
                )
                for page in pagify(message):
                    await ctx.send(page)
                return

            else:
                async with self.data.commands() as _commands:
                    _commands[function.name] = function_string
                await ctx.send(
                    "The command `{}` was successfully added.".format(function.name)
                )

        else:

            if name != function.__name__:
                await ctx.send(
                    "Error: The listener's name is different than what you gave when initializing the command.\n"
                )
                return

            async with self.data.commands() as _commands:
                if name in _commands:
                    await ctx.send("Error: That listener is already registered.")
                    return

            try:
                self.bot.add_listener(function)

            except Exception as e:
                message = (
                    "An expetion has occured while adding the listener to discord.py:\n"
                    "```py\n"
                    "{}```".format(
                        "".join(traceback.format_exception(type(e), e, e.__traceback__))
                    )
                )
                for page in pagify(message):
                    await ctx.send(page)
                return

            else:
                async with self.data.commands() as _commands:
                    _commands[function.__name__] = function_string
                await ctx.send(
                    "The listener `{}` was successfully added.".format(
                        function.__name__
                    )
                )

    @instantcmd.command(aliases=["del", "remove"])
    async def delete(self, ctx, command: str):
        """
        Remove a command from the registered instant commands.
        """

        _commands = await self.data.commands()

        if command not in _commands:
            await ctx.send("That instant command doesn't exist")
            return

        if not self.bot.remove_command(command):
            function = self.get_function_from_str(_commands[command], command)
            self.bot.remove_listener(function)
        _commands.pop(command)
        await self.data.commands.set(_commands)
        await ctx.send(
            "The command/listener `{}` was successfully removed.\n\n"
            "**WARNING:** Since discord.py is glitchy with listeners, "
            "they can't be removed for now. Restart to remove them (if already removed using that command). "
            "If you want, join the conversation and refer discord.py#1284's issue.".format(
                command
            )
        )

    @instantcmd.command()
    async def info(self, ctx, command: str = None):
        """
        List all existing commands made using Instant Commands.

        If a command name is given and found in the Instant commands list, the code will be shown.
        """

        if not command:
            message = "List of instant commands:\n" "```Diff\n"
            _commands = await self.data.commands()

            for name, command in _commands.items():
                message += "+ {}\n".format(name)
            message += (
                "```\n"
                "*Hint:* You can show the command source code by typing "
                "`{}instacmd info <command>`".format(ctx.prefix)
            )

            if _commands == {}:
                await ctx.send("No instant command created.")
                return

            for page in pagify(message):
                await ctx.send(message)

        else:
            _commands = await self.data.commands()

            if command not in _commands:
                await ctx.send("Command not found.")
                return

            message = (
                "Source code for `{}{}`:\n".format(ctx.prefix, command)
                + "```Py\n"
                + _commands[command]
                + "```"
            )
            for page in pagify(message):
                await ctx.send(page)