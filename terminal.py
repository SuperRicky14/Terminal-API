import asyncio
import aioconsole
import shlex
import logging
import traceback
import time

"""
Todo:
1. Prevent multiple instances of the same command
2. Prevent multiple instances of the same alias
3. Fix help command
4. Test this and fix it up
"""

class CommandHandler:
    __logger = logging.getLogger("CommandHandler")
    
    __logger.setLevel(logging.INFO)

    def __init__(self):
        self.commands = {}
                
        asyncio.create_task(self.register_command("help", self.__help))
    
    async def register_command(self, command, command_executor, aliases=None, description=None, usage=None):
        start_time = time.time()
        self.__logger.info(f"REGISTERING COMMAND \"{command}\" (\"{command_executor.__name__}\")...")
        if aliases is None:
            aliases = []
        if description is None:
            if command_executor.__doc__:
                description = command_executor.__doc__
            else:
                description = "No description provided!"
                self.__logger.warning(f"Command {command} does not have a description!")
        if usage is None:
            usage = "No usage example(s) provided!"
            self.__logger.warning(f"Command {command} does not have usage example(s)!")
        
        end_time = time.time()
        self.__logger.info(f"...REGISTERED \"{command}\" (\"{command_executor.__name__}\") IN {end_time - start_time}!")

        self.commands[command] = {
            "executor": command_executor,
            "aliases": aliases,
            "description": description,
            "usage": usage
        }
        for alias in aliases:
            self.commands[alias] = self.commands[command]

    async def handle_input(self, user_input):
        parts = shlex.split(user_input)
        try:
            command = parts[0]
        except IndexError:
            pass
        args = parts[1:]

        if command in self.commands:
            command_info = self.commands[command]
            command_executor = command_info["executor"]
            await command_executor(*args)
        else:
            print(f"Unknown command: {command}")
    
    async def __help(self, command=None):
        if not command is None:
            if command in self.commands:
                await self.format_command_info(command)
            else:
                print(f"Unknown command: {command}")
        else:
            commands = await self.list_commands()
            print(f"Available commands ({len(commands)}):")
            for command in self.commands:
                await self.__format_command_info(command)
    
    async def __format_command_info(self, command):
            command_info = await self.get_command_info(command)
            description = command_info["description"]
            usage = command_info["usage"]
            aliases = command_info["aliases"]
            print(f"  {command}:")
            print(f"    Description: {description}")
            print(f"    Usage:")
            for example in usage:
                print(f"      {example}")
            if aliases:
                print(f"    Aliases: {', '.join(aliases)}")

    async def list_commands(self):
        return list(self.commands.keys())

    async def get_command_info(self, command):
        if command in self.commands:
            info = self.commands[command]
            return info
        return None

global handler

async def input_loop(): # the default input loop, you can override it with your own if needed
    try:
        running = True
        while running:
            user_input = await aioconsole.ainput("root@localhost $ ")
            await handler.handle_input(user_input)
    except asyncio.CancelledError: # catch keyboard interrupt
        running = False
    except Exception:
        print(traceback.format_exc())

async def on_ready():
     # do something when the terminal event loop is loaded
     # you can do anything here, but i just registered the commands to show you what can be done
    start_time = time.time()
    register_hello = asyncio.create_task(handler.register_command("hello", hello, aliases=["hi","hey"], usage=["hello", "hello <name>"], description="Say hello to someone else."))
    register_bye = asyncio.create_task(handler.register_command("bye", bye, aliases=["goodbye","cya"], usage=["bye", "bye <name>"], description="Say goodbye to someone else."))
    register_quit = asyncio.create_task(handler.register_command("quit", quit, aliases=["close","exit"], usage=["quit"], description="Shutdown the currently running event loop. (in this example case the terminal)"))
    await register_hello
    await register_bye
    await register_quit
    end_time = time.time()
    print(f"Ready in {end_time - start_time} seconds!")
    # remove these objects from memory if you do other shit even though its like 5 bytes and dosen't even matter
    del start_time
    del end_time

async def wrapper():
    global handler
    handler = CommandHandler() # initialize the command handler
    await on_ready()
    await input_loop()

"""
    BEGINNING OF EXAMPLE COMMANDS
"""

async def hello(name):
    if name:
        print(f"Hello, {name}!")
    else:
        print("Hello!")

async def bye(name):
    if name:
        print(f"Bye, {name}!")
    else:
        print("Bye!")

async def quit():
    loop = asyncio.get_event_loop()
    print("Shutting down...")
    loop.stop()
"""
    END OF EXAMPLE COMMANDS
"""

asyncio.run(wrapper()) # if you don't have an input loop, just use this | MUST BE LAST LINE IN FILE OTHERWISE ANY CODE BELOW WILL NOT WORK