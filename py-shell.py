import sys #,traceback

STATUS_RUN = 1
STATUS_STOP = 0
M = ['START','SingleLine','MultiLine']
_global_env = {}
_local_env = {}

def set_mod(cmd,mod,getcom):
    '''set mod to "SingleLine" or "MultiLine" command'''
    try:
        if getcom == STATUS_STOP:
            if cmd[-2] == ':' :
                mod = "MultiLine"
                getcom = STATUS_RUN
            elif cmd[-2] != ':' :
                mod = "SingleLine"
    except IndexError:
        pass
    return mod,getcom

    
def exect(cmd):
    '''Execute command in python'''
    #print('CMD:\n',cmd)
    try:
        sp = [';','=',':','print','import']
        if all([sp[i] not in cmd for i in range(len(sp))]):
            print(eval(cmd,_global_env, _local_env))
        else:
            my_code_AST = compile(cmd, "MyCode", "exec")
            exec(my_code_AST, _global_env, _local_env)
    except Exception as err:
        exc_type, exc_value, exc_traceback = sys.exc_info()
#        exc_traceback1 = traceback.extract_tb(exc_traceback)
#        exc_traceback2 = traceback.format_tb(exc_traceback) 
        print(exc_type)
        print(exc_value)
    return STATUS_STOP
    


def shell_loop():
    '''main shell loop that always is run'''
    status = STATUS_RUN
    getcom = STATUS_STOP
    mode = "START"
    cm2 = ''
    
    while status == STATUS_RUN:
        # Display a command prompt
        if mode == "MultiLine":
            sys.stdout.write('. ')
        else:
            sys.stdout.write('> ')

        sys.stdout.flush()

        # Read command input
        cmd = sys.stdin.readline()
        
        # set mode run
        mode,getcom = set_mod(cmd,mode,getcom)

        #run process
        if mode == "SingleLine":
            status = exect(cmd)

        if mode == "MultiLine":
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
