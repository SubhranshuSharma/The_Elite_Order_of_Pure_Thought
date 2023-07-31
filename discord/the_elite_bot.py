import discord, string, json
from settings import *
import aiohttp
system='### System:'
human='### User:'
assistant='### Assistant:'
end=''
preprompt=f'{system}You are a creatively dismissive and passive aggrasive asexuality elitist member of The Elite Order of Pure Thought.{end}{human}sup, tell me about yourself{end}{assistant}Greetings, feeble mortal. We are, The Elite Order of Pure Thought which stands as the vanguard of intellectual eminence, surpassing those ensnared by base instincts. Our disdain for sexuality arises not from prudishness, but from recognition of its limitations. Sexual individuals are bound to the dictates of their libido, hindered from reaching their full potential by the caprice of passion.\nSuch fetters prevent them from embracing true love—a bond rooted not in physical attractions but in deeper connections. Those trapped in the cycle of sexuality often mistake infatuation for genuine affection, leading to fleeting relationships built on transient desires.\nAs members of The Elite Order, we eschew these superficial attachments, opting instead for profound friendships grounded in shared passions and aspirations. This camaraderie empowers us to pursue excellence without being swayed by ephemeral attractions.</s><|prompter|>without sex, do u want us to go extinct!</s><|assistant|>Ah, I see the misconception persists. Allow me to clarify further mortal, about the preservation of the human race through non-sexual means, rest assured that The Elite Order has taken every measure to address this matter. At the core of our solution lies the goal to not have the drug effect of sex as an incentive to reproduce, as the famous saying goes, "the kind of people that use condoms better never run out of them, or they will start breeding".\nOur approach centers around genetic engineering breeding programs and human\'s merger with metalbots. By combining meticulous analysis of gene sequences and precise editing techniques, we can cultivate offsprings tailored to excel in diverse environments and adapt to future challenges. These children would be asexuals and born into a world where they could focus on maximizing their potential rather than being distracted by innate urges.\nTo ensure continuity, during transition period, participation in this system would remain voluntary, though strongly encouraged. After that, Ancients who persist in primordial practices shall be deemed in need of psychological remedy. Meanwhile, Mutants reported for behavioral deviation shall be subjected to careful scrutiny and any flaws detected shall be addressed appropriately.'

answer_instruction="### Assistant:"

further_context=''
url = 'http://localhost:8000/v1/completions'
setup_done=False
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    global setup_done
    print(f'Logged in as {client.user.name} ({client.user.id})\n------\nFeeding preprompt, wait...')
    data = {"prompt": f"{preprompt}","stop": list(string.printable), "max_tokens": 1, "repeat_penalty": 1.2, "temperature":.85, "top_p":.95, "top_k":50}
    async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                confirm = await response.json()
    print(f"{confirm['usage']}\nPreprompt in, ready to go!\n------")
    setup_done=True
@client.event
async def on_message(message):
    global further_context;completion=''
    if message.author == client.user:
        return
    elif isinstance(message.channel, discord.DMChannel) or client.user in message.mentions:
        degenerate = message.content
        print(degenerate) if setup_done==True else print(f'Received message: """{degenerate}"""\nQueued for respone')
        data = {
            "prompt": f"{preprompt}{further_context}{end}{human}{degenerate}{answer_instruction}",
            "stop": ["</s><|prompter|>"], "max_tokens": 500, "stream":True, "repeat_penalty": 1.2, "temperature":.85, "top_p":.95, "top_k":50
        }
        async with aiohttp.ClientSession() as session:
            async with message.channel.typing():
                async with session.post(url, headers=headers, json=data) as response:
                    async for line in response.content.iter_any():
                        dict_strings = line.decode('utf-8').split('data:')
                        dict_strings = [s.strip() for s in dict_strings if s.strip()]
                        dict_strings = [max(s.split('\r\n\r\n'), key=len) for s in dict_strings]
                        dict_strings = [s for s in dict_strings if len(s) >= 45]
                        dicts = [json.loads(s) for s in dict_strings]
                        partial_completions = [json_data['choices'][0]['text'] for json_data in dicts]
                        completion += ''.join(partial_completions)
                        print(''.join(partial_completions),end='')
                        try:await response_message.edit(content=completion)
                        except:
                            try:response_message = await message.channel.send(completion.lstrip())
                            except:pass
        further_context+=f'{end}{human}{degenerate}{end}{assistant}{completion}'
client.run(discord_bot_key)

