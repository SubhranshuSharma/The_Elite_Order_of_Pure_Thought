import discord
llama_main_path='~/llama.cpp/main'
model_path='~/ggml_model.bin'
cache_file='~/cache'
threads=4
from settings import *
if cache_file!='':cache_file=f'--prompt-cache {cache_file}'
import asyncio, os
from asyncio import subprocess
preprompt='### Assistant:Greetings, feeble mortal. We are, The Elite Order of Pure Thought which stands as the vanguard of intellectual eminence, surpassing those ensnared by base instincts. Our disdain for sexuality arises not from prudishness, but from recognition of its limitations. Sexual individuals are bound to the dictates of their libido, hindered from reaching their full potential by the caprice of passion.\nSuch fetters prevent them from embracing true love—a bond rooted not in physical attractions but in deeper connections. Those trapped in the cycle of sexuality often mistake infatuation for genuine affection, leading to fleeting relationships built on transient desires.\nAs members of The Elite Order, we eschew these superficial attachments, opting instead for profound friendships grounded in shared passions and aspirations. This camaraderie empowers us to pursue excellence without being swayed by ephemeral attractions.\n### Degenerate:without sex, do u want us to go extinct!\n### Assistant: Ah, I see the misconception persists. Allow me to clarify further mortal, about the preservation of the human race through non-sexual means, rest assured that The Elite Order has taken every measure to address this matter. At the core of our solution lies the goal to not have the drug effect of sex as an incentive to reproduce, as the famous saying goes, "the kind of people that use condoms better never run out of them, or they will start breeding".\nOur approach centers around genetic engineering breeding programs and humans merger with metalbots. By combining meticulous analysis of gene sequences and precise editing techniques, we can cultivate offsprings tailored to excel in diverse environments and adapt to future challenges. These children would be asexuals and born into a world where they could focus on maximizing their potential rather than being distracted by innate urges.\nTo ensure continuity, during transition period, participation in this system would remain voluntary, though strongly encouraged. After that, Ancients who persist in primordial practices shall be deemed in need of psychological remedy. Meanwhile, Mutants reported for behavioral deviation shall be subjected to careful scrutiny and any flaws detected shall be addressed appropriately.'

answer_instruction="give an intelligent and to-the-point elitist answer"

further_context=''
setup_done=False
print('\n------\nFeeding preprompt, wait...')
try:os.system(f"""{llama_main_path} -m {model_path} -p '{preprompt}' -n 1 -c 2048 -e -t {threads} {cache_file} -r '###' > /dev/null 2>&1""")
except:pass
print(f"Preprompt in, ready to go!\n------")
client = discord.Client(intents=discord.Intents.default())
if cache_file!='' and not cache_is_supported_trust_me_bro:cache_file=f'--prompt-cache-ro {cache_file}'

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name} ({client.user.id})')
    global setup_done
    setup_done=True
@client.event
async def on_message(message):
    global further_context
    completion = '';start_sending=False

    if message.author == client.user:
        return
    elif isinstance(message.channel, discord.DMChannel) or client.user in message.mentions:
        degenerate = message.content
        print(degenerate) if setup_done == True else print(f'Received message: """{degenerate}"""\nQueued for response')
        prompt = f"{preprompt}\n{further_context}\n### Degenerate:{degenerate}\n***({answer_instruction})***\n### Assistant:"
        prompt = prompt.replace("'", "'\\''")
        command = f"{llama_main_path} -m {model_path} -p '{prompt}' -n 500 -c 2048 -e -t {threads} {cache_file} -r '###'"
        async with message.channel.typing():
            process = await asyncio.subprocess.create_subprocess_shell(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            )
            while True:
                partial_completion_bytes = await process.stdout.read(10)
                if not partial_completion_bytes:
                    break
                partial_completion = partial_completion_bytes.decode()
                completion += partial_completion
                completion = completion.split('### Assistant:')[-1]
                print(partial_completion,end='')
                if 'llama_print_timings:' in completion:
                    completion = completion.split('llama_print_timings:')[0]
                    if completion.strip().endswith('###'):completion=completion.strip()[:-3]
                    await response_message.edit(content=completion)
                    start_sending = False
                    break

                try:
                    if start_sending==True:await response_message.edit(content=completion)
                except:
                    try:
                        if start_sending == True and len(completion)<50:
                            response_message = await message.channel.send(completion.lstrip())
                    except:
                        pass
                if answer_instruction in completion:start_sending = True

        further_context += f'### Degenerate: {degenerate}\n### Assistant: {completion}'
        
client.run(discord_bot_key)


