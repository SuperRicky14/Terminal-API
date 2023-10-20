
# Terminal-API

My attempt at creating an API (Application Programming Interface) to create terminal applications using [asyncio](https://docs.python.org/3/library/asyncio.html), [aioconsole](https://pypi.org/project/aioconsole/) and [python](https://www.python.org/downloads/) 
Examples are down below the file

Currently it has a built in **help** command which prints properties of every registered command:
Their **name** (e.g. print)
Their **description** (e.g. Prints Hi to the console) | Dosen't need to be specified in the "register_command" function can also be specified in the functions [docstring](https://peps.python.org/pep-0257/)
Their **aliases** (e.g. write, printhi)
Or if you enter a specific command, it will just tell you about the properties of that command.


## Requirements

[asyncio](https://docs.python.org/3/library/asyncio.html) (Bundled in **3.7** or higher), [aioconsole](https://pypi.org/project/aioconsole/) and [python](https://www.python.org/downloads/) 3.11 (anything above 3.7 should work due to the implementation of asyncio)

## Creating commands
Setup:
If you're using this from another file make sure to import the CommandHandler class from the terminal.py file
    handler = CommandHandler # create a new CommandHandler object and name it "handler"
Later this should be done with imports once i upload it to the pip repository.


You can create commands by first defining a function with a [docstring](https://peps.python.org/pep-0257/) (must be asynchronous and use asyncio's syntax):

    async def printhi():
      
    	print ("Hello!")
Now that you have your function, there are two ways to register your function:
Method **1** (blockingly register the task preventing glitches (requires a running event loop AND must be executed in an async function)):

    await(handler.register_command("print",
									printhi,
									aliases=["printhi", "hello"] # must be a list
									usage=["print"] # must also be a list
									))
Method **2** (asynchronously register a task (needs a running event loop)):

    asyncio.create_task(handler.register_command("print",
																   printhi,
																   aliases=["printhi", "hello"]
																   ))
Notice how in both of these methods we did not need to explicitly state a description, that is because of the [docstring](https://peps.python.org/pep-0257/) that we added in the function of the command.

#### Calling Commands from another class:
**IMPORTANT**: make sure to import your handler object you created from the other file, *DO NOT CREATE ANOTHER INSTANCE OF THE *"CommandHandler"* CLASS IN THIS FILE AS IT WILL CAUSE DESYNCS AND PROBABLY CRASHES!*


    from <yourfile> import handler
    
    async def when_ready():
	    await handler.register_command(
									  "example_cmd_from_another_file",
									  example_command_from_another_file,
									  aliases=["ecfaf"],
									  usage=["example_cmd_from_another_file"])
	async def example_command_from_another_file():
		"""
		This function will be called from another file
		"""
		print("This was called from another file")

Make sure to afterwards in your main file, call the when_ready() function to register your commands!

## TODO:

Todo:

1. **BUGFIX**: Prevent multiple instances of the same command

2. **BUGFIX**: Prevent multiple instances of the same alias

3. **BUGFIX**: Fix Logger

4. **FEATURE_REQUEST**: Create a command system similar to linux terminal, where entering a command then && and another command will execute all commands specified in order like this:

       \<command1\> && \<command2\> && \<command3\>....... and so on

### If you find a bug or think of a really great feature to add, feel free to open a bug report or pull request! (don't ask questions about asyncio or general python syntax / knowledge on the issue requests)


