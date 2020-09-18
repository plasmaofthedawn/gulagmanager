log_channel = None

async def log(message):
    await log_channel.send(message)
    print(message)
