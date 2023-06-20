discord_bot_key='The_Elite_Order_of_Pure_Thought'
llama_main_path='~/llama.cpp/main'
model_path='~/storage/downloads/vicuna-7b-1.1.ggmlv3.q3_K_S.bin'
cache_file='~/storage/downloads/cache'
threads=4
cache_is_supported_trust_me_bro=False






if discord_bot_key=='The_Elite_Order_of_Pure_Thought':discord_bot_key=input('input discord bot key: ')
import os
if not os.path.exists(llama_main_path):
    print(f'llama main file not available at {llama_main_path}')
    llama_main_path=input("path to 'main' file from llama.cpp: ")
if not os.path.exists(model_path):
    print(f'model file not available at {model_path}')
    model_path=input("path to model: ")
if cache_file!='' and not os.path.exists(cache_file):
    print(f'cache file not available at {cache_file}\njust press enter to not use cache')
    cache_file=input("path to cache: ")

