import discord
import re
import asyncio

client=discord.Client()

def flush(text):
  if "||" in text or "| |" in text:
    text=text.replace("||", "|")
    text=text.replace("| |", "|")
    flush(text)
  else:
    pass
  if text=="|":
    return ""
  return text

@client.event
async def on_ready():
  print("Make way for {}".format(client.user))

@client.event
async def on_message(msg):

  if msg.author==client.user:
    return
  
  mes=msg.content #content of the message
  tasks=str(msg.author.id) #user ID of the sender
  
  #ADD TASK
  if mes.startswith(".add") and mes[5:]!="":
    with open(tasks,"a") as f:
      f.write(mes[5:]+"|")
    await msg.channel.send("task added")
    #with open(tasks, "r") as f:
      #print(f.read())
  
  #LIST TASKS
  if mes==".list":
    await msg.channel.send("list of tasks:")
    with open(tasks, "r") as f:
      cont=f.read().split("|")
      #print(cont)
      if cont==['']:
        await msg.channel.send("EMPTY")
      else:
        for i in cont:
          try:
            await msg.channel.send(i)
          except Exception as e:
            pass
    #with open(tasks, "r") as f:
      #f.read()
  
  #CLEAR TASKS
  if mes==".clear":
    with open(tasks, "w") as f:
      pass
    await msg.channel.send("tasks cleared")
  
  #DELETE A TASK
  if mes.startswith(".del"):
    with open(tasks, "r") as f:
      cont=f.read().split("|")
      #print(cont)
    pos=int(mes[5:])
    del cont[pos-1]
    cont.remove("")
    with open(tasks,"w") as f:
      for i in cont:
        f.write(i+"|")
    await msg.channel.send("task deleted")
    #with open(tasks, "r") as f:
      #print(f.read())
  
  #OPTIMIZE
  if mes.startswith(".flush"):
    with open(tasks, "r+") as f:
      cont=f.read()
    #print(cont)
    cont=flush(cont)
    #print(cont)
    with open(tasks, "w") as f:
      f.write(cont)
    await msg.channel.send("optimized")


  #SCHEDULING
  if mes.startswith(".schedule"):
    timing=re.match("\\d*mins", mes[10:]).group().strip("mins")
    task=re.match("\\d*mins .*", mes[10:]).group()
    task=re.sub("\\d*mins ", "", task, count=1)
    await msg.channel.send("task scheduled for {} mins".format(timing))
    async def delayed(timing, task):
      await asyncio.sleep(int(timing)*60)
      await msg.channel.send(task)
    await asyncio.create_task(delayed(timing, task))

client.run("TOKEN-GOES-HERE")
