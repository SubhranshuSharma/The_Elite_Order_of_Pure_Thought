# श्रेष्ठचिन्तायाः अभिज्ञानसंघः | The Elite Order of Pure Thought

## Quick Start

`git clone https://github.com/SubhranshuSharma/The_Elite_Order_of_Pure_Thought`


### Linux

install dependency: `pip install llama-cpp-python[server]`

start server: `python3 -m llama_cpp.server --model /path/to/model --n_ctx 2048`

put discord bot key in `discord/settings.py` file

run `python3 discord/the_elite_bot.py`


### Linux/Termux

run `git clone https://github.com/ggerganov/llama.cpp ~;cd ~;make`

cache files of llama can be used but not generated/edited in termux yet, so run it on a computer till `Preprompt in, ready to go!` then copy the model and cache file over to `downloads` folder in your phone.

on termux run `termux-setup-storage` to mount the downloads folder at `~/storage/downloads`

put model path and discord key in `discord/termux/settings.py` file, make `cache_is_supported_trust_me_bro=True` if ur sure or on computer, make `cache_file=''` to not use cache at all

run `python3 the_elite_bot_termux.py`

