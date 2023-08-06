import dis


class ClientVerifier(type):
    def __init__(self, clsname, bases, clsdict):
        methods = []
        for key in clsdict:
            try:
                instruction = dis.get_instructions(clsdict[key])
            except TypeError:
                pass
            else:
                for i in instruction:
                    if i.opname == 'LOAD_GLOBAL':
                        if i.argval not in methods:
                            methods.append(i.argval)
        for command in ('accept', 'listen', 'socket'):
            if command in methods:
                raise TypeError(f'Использование метода {command} недопустимо в клиентском классе')
        if not ('get_message' in methods or 'send_message' in methods):
            raise TypeError('Отсутствуют вызовы функций, работающих с сокетами.')
        super().__init__(clsname, bases, clsdict)


class ServerVerifier(type):
    def __init__(self, clsname, bases, clsdict):
        methods = []
        attrs = []
        for key in clsdict:
            try:
                instruction = dis.get_instructions(clsdict[key])
            except TypeError:
                pass
            else:
                for i in instruction:
                    if i.opname == 'LOAD_GLOBAL':
                        if i.argval not in methods:
                            methods.append(i.argval)
                    elif i.opname == 'LOAD_ATTR':
                        if i.argval not in attrs:
                            attrs.append(i.argval)
        if 'connect' in methods:
            raise TypeError('Использование метода connect недопустимо в серверном классе')
        if not ('SOCK_STREAM' in attrs and 'AF_INET' in attrs):
            raise TypeError('Некорректная инициализация сокета.')
        super().__init__(clsname, bases, clsdict)
