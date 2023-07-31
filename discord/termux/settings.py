discord_bot_key='The_Elite_Order_of_Pure_Thought'
llama_main_path='~/llama.cpp/main'
model_path='~/storage/downloads/model.bin'
cache_file='~/storage/downloads/cache'
threads=7
tab_filling_default=False

if discord_bot_key=='The_Elite_Order_of_Pure_Thought':discord_bot_key=input('input discord bot key: ')
import os, asyncio

class _Getch:
    """Gets a single character from standard input. Does not echo to the screen."""
    def __init__(self):
        try:
            self.impl = _GetchUnix()
        except ImportError:
            print('windows is for pussies')
            self.impl = _GetchWindows()

    def __call__(self):
        return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            if ch == '\x7f':  # Check for backspace character
                sys.stdout.write('\b \b') 
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

getch = _Getch()

async def ask_path(prompt=''):
    print(prompt,end='',flush=True)
    full = '';wrapped=second_tab=False;i=0
    while True:
        try:
            char = await asyncio.to_thread(getch)
            try:
                # if (os.path.join(directory,filename)==full and prev_char!='\r') or len(common_prefix)>len(filename):second_tab=True
                if os.path.join(directory,filename)==full and prev_char=='\t':second_tab=True
            except:pass
            if char=='\x7f':
                full=full[:-1]
            elif char == '\x03':
                print();break
            elif char == '\t' or (char=='\r' and second_tab):
                directory, filename = os.path.split(full)
                directory=os.path.expanduser(os.path.expandvars(directory)) if directory else os.path.expanduser(os.path.expandvars(filename))
                suggestions=[entry for entry in os.listdir(directory) if entry.lower().startswith(filename.lower())]
                prefix = os.path.commonprefix([path.lower() for path in suggestions]) #generous, case insensitive prefix search
                index = next((i for i, path in enumerate(suggestions) if path.lower().startswith(prefix)), -1) 
                index = next((i for i, path in enumerate(suggestions) if path.startswith(prefix)), index) if index!=-1 else index
                common_prefix=suggestions[index][:len(prefix)] if index!=-1 else ''
                full = os.path.join(directory, common_prefix) + '/' if os.path.isdir(os.path.join(directory, common_prefix)) and len(suggestions)==1 else os.path.join(directory, common_prefix)
                if os.path.exists(os.path.join(directory, common_prefix)):os.system('clear;cls > /dev/null 2>&1')
                if second_tab:
                    if i>=len(suggestions):i=0;wrapped=True
                    if char=='\r':os.system('clear;cls > /dev/null 2>&1');full=os.path.join(directory,suggestions[i-1]) + '/' if os.path.isdir(os.path.join(directory, suggestions[i-1])) else os.path.join(directory,suggestions[i-1]);print('\n',prompt,full,end='',sep='',flush=True)
                    elif len(suggestions)>1:
                        suggestions[i]='*'+suggestions[i]
                        print('\n',f'{prompt}({full})',' '.join(suggestions),sep='',end='') if i==0 and wrapped==False else print('\r',f'{prompt}({full})',' '.join(suggestions),sep='',end='')
                        i+=1
                print('\r', prompt, full, end='', sep='', flush=True) if len(suggestions) == 1 or (second_tab and char=='\r' and len(suggestions)==1) else print('\n', ' '.join(suggestions), '\n', prompt, full, end='', sep='', flush=True) if not second_tab else print(end='')
            elif char=='\r':os.system('clear;cls > /dev/null 2>&1' );return full
            else:full += char
            print(repr(char)[1:][:-1] if char not in ['\t','\x7f','\r'] else '',end='',flush=True)
            prev_char=char;second_tab=False;wrapped=False
        except Exception as e:print('wtf!:',e);pass

tab_once=['tab','t'];tab_always=['all','a']

def handle_file_input(file_path, prompt):
    global tab_filling_default
    if not os.path.isfile(os.path.expanduser(os.path.expandvars(file_path))):
        if not tab_filling_default:file_path = input(f"{prompt}")
        if file_path in tab_always:tab_filling_default = True
        if tab_filling_default or file_path in tab_once:file_path = asyncio.run(ask_path(prompt))
    return file_path
print("enter 'all'/'a' to enable tab filling for all", flush=True)
llama_main_path = handle_file_input(llama_main_path, "path to 'main' file from llama.cpp: ")
model_path = handle_file_input(model_path, "path to model: ")
cache_file = handle_file_input(cache_file, "path to cache: ")





# if not os.path.isfile(os.path.expanduser(os.path.expandvars(llama_main_path))):
#     if not tab_filling_default:llama_main_path=input("(type 'tab'/'t' for prompt with tab filling)\npath to 'main' file from llama.cpp: ")
#     if llama_main_path in tab_always:tab_filling_default=True
#     if tab_filling_default or llama_main_path in tab_once:llama_main_path=asyncio.run(ask_path('llama main path:'))
# if not os.path.isfile(os.path.expanduser(os.path.expandvars(model_path))):
#     if not tab_filling_default:model_path=input("(type 'tab'/'t' for prompt with tab filling)\npath to model: ")
#     if model_path in tab_always:tab_filling_default=True
#     if tab_filling_default or model_path in tab_once:model_path=asyncio.run(ask_path('model path: '))
# if not os.path.isfile(os.path.expanduser(os.path.expandvars(cache_file))):
#     if not tab_filling_default:cache_file=input("(type 'tab'/'t' for prompt with tab filling)\npath to cache: ")
#     if tab_filling_default or cache_file in tab_once:cache_file=asyncio.run(ask_path('cache path: '))

