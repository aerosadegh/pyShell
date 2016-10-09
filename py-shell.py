import sys

STATUS_RUN = 1
STATUS_STOP = 0
M = ['START','SingleLine','MultiLine']
_global_env = {}
_local_env = {}

def set_mod(cmd,mod,getcom):
    try:
        if getcom == STATUS_STOP:
            if cmd[-2] == ':' :
                mod = M[2]
                getcom = STATUS_RUN
            elif cmd[-2] != ':' :
                mod = M[1]
    except IndexError:
        pass
    return mod,getcom

    
def exect(cmd):
    #print('CMD:\n',cmd)
    sp = [';','=',':','print','import']
    if all([sp[i] not in cmd for i in range(len(sp))]):
        print(eval(cmd,_global_env, _local_env))
    else:
        my_code_AST = compile(cmd, "MyCode", "exec")
        exec(my_code_AST, _global_env, _local_env)
    return STATUS_STOP
    
    
def shell_loop():
    status = STATUS_RUN
    getcom = STATUS_STOP
    mode = M[0]
    cm2 = ''
    
    while status == STATUS_RUN:
        # Display a shell
        if mode != M[2]:
            sys.stdout.write('> ')
        elif mode == M[2]:
            sys.stdout.write('. ')

        sys.stdout.flush()

        # Read command input
        cmd = sys.stdin.readline()
        
        # set mode run
        mode,getcom = set_mod(cmd,mode,getcom)

        #run process
        if mode == M[1]:
            status = exect(cmd)

        if mode == M[2]:
            cm2 = cm2 + cmd
            if cm2[-2:] == '\n\n':
                status =  exect(cm2)
 
    shell_loop()

if __name__ == "__main__":
    try:
        if len(sys.argv)>1:
            file = sys.argv[-1]
            exect(open(file).read())
    except IndexError:
        pass
    
    if '-i' in sys.argv or len(sys.argv)==1:
        shell_loop() 
