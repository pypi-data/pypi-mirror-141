import os, subprocess
def shell(cmd, encoding='utf-8'):
    process = subprocess.Popen(cmd.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    return out.decode(encoding)
def linux():
    try:
        if shell('uname') == 'Linux\n': 
            return True
        else: return False
    except:
        return False
def notify(header='Python App', text='Hello, Sovenok-Hacker!', time=1, icon=None):
    if not linux():
        print('Supported only Linux!')
    else:
        try:
            if icon == None:
                shell(f'notify-send "{header}" "{text}" --expire-time={time * 1000}')
            else:
                shell(f'notify-send "{header}" "{text}" --expire-time={time * 1000} --icon "{icon}"')
        except:
            raise OSError('cannot send notification')
def owl():
    print('''
Hello, Sovenok-Hacker!    ,''    ''.
                         / `-.  .-' \
                        /( (O))((O) )
                       /'-..-'/\`-..|
                     ,'\   `-.\/.--'|
                   ,' ( \           |
                 ,'( (   `._        |
                /( (  ( ( | `-._ _,-;
               /( (  ( ( (|     '  ;
              / ((  (    /        /
             //         /        /
             //  / /  ,'        /
            // /    ,'         /
            //  / ,'          ;
            //_,-'          ;
            // /,,,,..-))-))\    /|
              /; ; ;\ `.  \  \  / |
             /; ; ; ;\  \.  . \/./
            (; ; ;_,_,\  .: \   /
             `-'-'     | : . |:|
                       |. | : .|
''')
