import Clases

Reservadas = ['let', 'var','const','if','while','foreach','in','switch','case','break','default']

#=========================#
#AUTOMATA LECTOR DE SCRIPT#
#=========================#
def readScript(document, Tokens):
    numberLine = 0
    tokenLine = 0
    column = 0
    estado = 0
    content = ''

    for line in document:
        numberLine+=1
        i = 0
        while i < len(line):
            
            if estado == 0:
                content = ''
                tokenLine = numberLine
                column = i

                if line[i] == '/':
                    estado = 1
                    content = '/'
                elif str(line[i]).isalpha():
                    estado = 5
                    content = content + line[i]
                elif line[i] == '_':
                    estado = 5
                    content = content + '_'
                elif line[i] == '+':
                    estado = 6
                    content = content + '+'
                elif line[i] == '-':
                    estado = 6
                    content = content + '-'
                elif str(line[i]).isdigit():
                    estado = 6
                    content = content + line[i]
                elif line[i] == '=':
                    estado = 9
                    content = '='
                elif line[i] == '(':
                    Tokens.append(Clases.Token('tk_openPar','(','apertura de parentesis que almacenan parametros o condiciones',tokenLine,column))
                elif line[i] == ')':
                    Tokens.append(Clases.Token('tk_closePar',')','cierre de parentesis que almacenan parametros o condiciones',tokenLine,column))
                elif line[i] == '{':
                    Tokens.append(Clases.Token('tk_openBrack','{','llave de apertura',tokenLine,column))
                elif line[i] == '}':
                    Tokens.append(Clases.Token('tk_closeBrack','}','llave de cierre',tokenLine,column))
                elif line[i] == ';':
                    Tokens.append(Clases.Token('tk_semicolon',';','se coloca al final de ciertas instrucciones',tokenLine,column))
                elif line[i] == ':':
                    Tokens.append(Clases.Token('tk_points',':','se utiliza despues de un case o default',tokenLine,column))
                elif line[i] == ' ' or line[i] == '\n':
                    pass
                elif line[i] == '"':
                    estado = 12
                    content = content + '"'
                else:
                    estado = 11
                    content = content + line[i]
            elif estado == 1:
                if line[i] == '*':
                    estado = 2
                    content = content + '*'
                else:
                    estado = 11
                    content = content + '*'
            elif estado == 2:
                if line[i] == '*':
                    estado = 3
                    content = content + '*'
                else:
                    content = content + line[i]
            elif estado == 3:
                if line[i] == '/':
                    content = content + line[i]
                    estado = 4
                else:
                    estado = 2
                    content = content + line[i]
            elif estado == 4:
                Tokens.append(Clases.Token('tk_comment', content, 'los comentarios son bloques que se ignoran al momento de leer el codigo',tokenLine,column))
                content = ''
                estado = 0
                continue
            elif estado == 5:
                if line[i] == '_' or str(line[i]).isalpha() or str(line[i]).isdigit():
                    content = content + line[i]
                elif line[i] == ' ' or line[i] == '\n':
                    Tokens.append(selectWord(content,tokenLine,column))
                    estado = 0
                    content = ''
                elif line[i] == ';' or line[i] == '(' or line[i] == ')' or line[i] == '{' or line[i] == '}' or line[i] == ',' or line[i] == ':':
                    Tokens.append(selectWord(content,tokenLine,column))
                    estado = 0
                    content = ''
                    Tokens.append(selectSeparator(line[i],numberLine,i))
            elif estado == 6:
                if str(line[i]).isdigit():
                    content = content + line[i]
                elif line[i] == '.':
                    content = content + line[i]
                    estado = 7
                elif line[i] == ';' or line[i] == '(' or line[i] == ')' or line[i] == '{' or line[i] == '}' or line[i] == ',' or line[i] == ':':
                    Tokens.append(Clases.Token('tk_number', content, r'numeros, pueden ser enteros o decimales y cumplir con la estructura [(+|-)?D(D)*(\.D*)?]', tokenLine, column))
                    estado = 0
                    content = ''
                    Tokens.append(selectSeparator(line[i],numberLine,i))
                elif line[i] == ' ' or line[i] == '\n':
                    Tokens.append(Clases.Token('tk_number', content, r'numeros, pueden ser enteros o decimales y cumplir con la estructura [(+|-)?D(D)*(\.D*)?]', tokenLine, column))
                    content = ''
                    estado = 0
                else:
                    estado = 11
                    content = content + line[i]
            elif estado == 7:
                if str(line[i]).isdigit():
                    content = content + line[i]
                    estado = 8
                elif line[i] == ' ' or line[i] == '\n':
                    Tokens.append(Clases.Token('error', content, 'Se detecto error', tokenLine, column))
                    estado = 0
                    content = ''
                else:
                    estado = 11
                    content = content + line[i]
            elif estado == 8:
                if str(line[i]).isdigit():
                    content = content + line[i]
                elif line[i] == ';' or line[i] == '(' or line[i] == ')' or line[i] == '{' or line[i] == '}' or line[i] == ',' or line[i] == ':':
                    Tokens.append(Clases.Token('tk_number', content, r'numeros, pueden ser enteros o decimales y cumplir con la estructura [(+|-)?D(D)*(\.D*)?]', tokenLine, column))
                    estado = 0
                    content = ''
                    Tokens.append(selectSeparator(line[i],numberLine,i))
                elif line[i] == ' ' or line[i] == '\n':
                    Tokens.append(Clases.Token('tk_number', content, r'numeros, pueden ser enteros o decimales y cumplir con la estructura [(+|-)?D(D)*(\.D*)?]', tokenLine, column))
                    content = ''
                    estado = 0
                else:
                    estado = 11
                    content = content + line[i]
            elif estado == 9:
                if line[i] == '>':
                    estado = 10
                    content = content + line[i]
                elif line[i] == ' ' or line[i] == '\n':
                    Tokens.append(Clases.Token('tk_equal', '=', 'Signo utilizado para asignar un valor',tokenLine,column))    
                    estado = 0
                    content = ''
                else:
                    estado = 0
                    Tokens.append(Clases.Token('tk_equal', '=', 'Signo utilizado para asignar un valor',tokenLine,column))    
                    continue
            elif estado == 10:
                Tokens.append(Clases.Token('tk_arrow', '=>','utilizado al crear una funcion',tokenLine,column))
                estado = 0
                continue
            elif estado == 11:
                if line[i] == ' ' or line[i] == '\n':
                    Tokens.append(Clases.Token('error', content, 'Se detecto error', tokenLine, column))
                    estado = 0
                elif line[i] == ';' or line[i] == '(' or line[i] == ')' or line[i] == '{' or line[i] == '}' or line[i] == ',' or line[i] == ':':
                    Tokens.append(Clases.Token('error', content, 'Se detecto error', tokenLine, column))
                    Tokens.append(selectSeparator(line[i], numberLine, i))
                    content = ''
                    estado = 0
                else:
                    content = content + line[i]
            elif estado == 12:
                if line[i] == '"':
                    estado = 0
                    content = content + '"'
                    Tokens.append(Clases.Token('tk_string',content,'es una cadena de caracteres, inicia y termina con comillas dobles (")',tokenLine,column))
                    content = ''
                else:
                    content = content + line[i]
            i+=1
    
    #GENERANDO REPORTES DE TOKENS Y ERRORES
    iT = 1
    iE = 1
    headE = '<!DOCTYPE html><html><head><title>Errores lexicos</title><link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" integrity="sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z" crossorigin="anonymous"></head><body><table class="table"><thead><tr><th scope="col">#</th><th scope="col">Error</th><th scope="col">Fila</th><th scope="col">Columna</th></tr></thead><tbody>'
    footer = '</tbody></table></body></html>'
    contentE = ''
    headT = '<!DOCTYPE html><html><head><title>TOKENS</title><link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" integrity="sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z" crossorigin="anonymous"></head><body><table class="table"><thead class="thead-dark"><tr><th scope="col">#</th><th scope="col">TOKEN</th><th scope="col">CONTENIDO</th><th scope="col">DESCRIPCION</th><th scope="col">FILA</th><th scope="col">COLUMNA</th></tr></thead><tbody>'
    contentT = ''
    for token in Tokens:
        if token.token == 'error':
            contentE = contentE + '<tr><th scope="row">'+str(iE)+'</th><td>'+token.content+'</td><td>'+str(token.line)+'</td><td>'+str(token.column)+'</td></tr>'
            iE += 1
        else:
            contentT = contentT + '<tr><th scope="row">'+str(iT)+'</th><td>'+str(token.token)+'</td><td>'+token.content+'</td><td>'+token.description+'</td><td>'+str(token.line)+'</td><td>'+str(token.column)+'</td></tr>'
            iT += 1

    with open('REPORTE_ERRORES_LEXICOS.html', "w") as report:
        report.write(headE+contentE+footer)

    with open('REPORTE_TOKENS.html', "w") as report:
        report.write(headT+contentT+footer)

#=======================================#
#AQUI INICIAN FUNCIONES ASOCIADAS AL AFD#
#=======================================#

def selectWord(content, tokenLine, column):
    if isWord(content):
        return Clases.Token('tk_'+content, content, 'palabras reservadas, son palabras pertenecientes al lenguaje', tokenLine, column)
    elif isBool(content):
        return Clases.Token('tk_boolean', content, 'almacena valores de verdad, es decir, verdadero o falso', tokenLine, column)
    else:
        return Clases.Token('tk_id', content, 'identificadores de variables, funciones y parametros. Debe cumplir con la estructura [(_|L)(_|L|D)*]', tokenLine, column)

def selectSeparator(value, tokenLine, column):
    if value == '(':
        return Clases.Token('tk_openPar','(','apertura de parentesis que almacenan parametros o condiciones',tokenLine,column)
    elif value == ')':
        return Clases.Token('tk_closePar',')','cierre de parentesis que almacenan parametros o condiciones',tokenLine,column)
    elif value == '{':
        return Clases.Token('tk_openBrack','{','llave de apertura',tokenLine,column)
    elif value == '}':
        return Clases.Token('tk_closeBrack','}','llave de cierre',tokenLine,column)
    elif value == ';':
        return Clases.Token('tk_semicolon',';','se coloca al final de ciertas instrucciones',tokenLine,column)
    elif value == ',':
        return Clases.Token('tk_comma',',','se utiliza para separar parametros',tokenLine,column)
    elif value == ':':
        return Clases.Token('tk_points',':','se utiliza luego de un case o un default',tokenLine,column)
    

def isWord(word):
    for i in Reservadas:
        if word == i:
            return True

    return False

def isBool(word):
    if word == 'false' or word == 'true':
        return True
    else:
        return False

#=========================================================================#
#AQUI INICIA EL AUTOMATA DE PILA ENCARGADO DE REALIZAR ANALISIS SINTACTICO#
#=========================================================================#

#DEFINIMOS SIMBOLOS TERMINALES Y SIMBOLOS NO TERMINALES#
Terminals = ['tk_id','tk_arrow','tk_semicolon','tk_openPar',
'tk_closePar','tk_openBrack','tk_closeBrack','tk_number','tk_boolean',
'tk_string','tk_equal','tk_comma','tk_points','tk_let','tk_var','tk_const',
'tk_if','tk_while','tk_foreach','tk_in','tk_switch','tk_case','tk_break','tk_default']
NoTerminals = ['INSTRUCTION','VALUE','CASES','DECLARER','ID_PARAMETERS','PARAMETERS','DATA','BREAK']

def syntacticAnalysis(Tokens, stop):
    stack = ['λ']
    counter = 0
    state = 'i'
    iState = ''
    fState = ''
    i = 0
    j = 1
    error = False
    cicle = True
    out = ''
    intro = ''

    text1 = '<!DOCTYPE html><html><head><title>AUTOMATA CON PILA</title><link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" integrity="sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z" crossorigin="anonymous"></head><body><table class="table"><thead class="thead-dark"><tr><th scope="col">PILA</th><th scope="col">ENTRADA</th><th scope="col">TRANSICION</th></tr></thead><tbody>'
    text2 = ''
    text3 = '</tbody></table></body></html>'

    pila = ''
    entrada = ''
    transicion = ''

    for element in Tokens:
        counter += 1
    
    while cicle:
        pila = ''
        entrada = ''
        intro = ''
        transicion = ''
        aux = []
        if error:
            print('----- SE HA ENCONTRADO UN ERROR SINTACTICO -----')
            break

        if stop:
            input()

        #pasando pila a string#
        pila = ''
        stack.reverse()
        for element in stack:
            pila = pila + ' ' + element
        stack.reverse()
        #pasando entrada a string#
        try:
            for token in Tokens:
                entrada = entrada + ' ' + token.token
        except:
            print('NO SE PUDO ITERAR')

        iState = state
        if Tokens == []: 
            transicion = '(' + iState + ', λ, '
        else:
            if isTerminal(Tokens[i]):
                transicion = '(' + iState + ', ' + Tokens[i].token + ', '
            else:
                transicion = '(' + iState + ', λ, '
        
        if state == 'i':
            out = stack.pop()
            j -= 1
            stack.append('#')
            intro = '#'
            j += 1
            state = 'p'
        elif state == 'p':
            stack.append('INSTRUCTION')
            intro = 'INSTRUCTION'
            j += 1
            state = 'q'
        elif state == 'q':
            if stack[j-1] == '#':
                out = stack.pop()
                state = 'f'
                fState = state
        
                if intro == '':
                    intro = 'λ'
                transicion = transicion + out + '; ' + fState + ', ' + intro +')'

                print('--PILA-- '+pila)
                print('--ENTRADA-- '+entrada)
                print('--TRANSICION-- '+transicion)
                text2 = text2 + '<tr><th scope="row">'+pila+'</th><td>'+entrada+'</td><td>'+transicion+'</td></tr>'
                continue
            if not isTerminal(stack[j-1]):
                if stack[j-1] == 'INSTRUCTION':
                    if j <= 2 and Tokens == []:
                        entrada = 'λ'
                        fState = state
                        out = stack.pop()
                        j-=1
                        if intro == '':
                            intro = 'λ'
                        transicion = transicion + out + '; ' + fState + ', ' + intro +')'

                        print('--PILA-- '+pila)
                        print('--ENTRADA-- '+entrada)
                        print('--TRANSICION-- '+transicion)
                        text2 = text2 + '<tr><th scope="row">'+pila+'</th><td>'+entrada+'</td><td>'+transicion+'</td></tr>'
                        continue
                    out = stack.pop()
                    j -= 1
                    if Tokens[i].token == 'tk_if':
                        aux = ['tk_if','tk_openPar','VALUE','tk_closePar','tk_openBrack','INSTRUCTION','tk_closeBrack','INSTRUCTION']
                        aux.reverse()
                        stack = stack + aux
                        intro = 'tk_if tk_openPar VALUE tk_closePar tk_openBrack INSTRUCTION tk_closeBrack INSTRUCTION'
                        j += 8
                    elif Tokens[i].token == 'tk_while':
                        aux = ['tk_while','tk_openPar','VALUE','tk_closePar','tk_openBrack',
                        'INSTRUCTION','tk_closeBrack','INSTRUCTION']
                        aux.reverse()
                        stack = stack + aux
                        intro = 'tk_while tk_openPar VALUE tk_closePar tk_openBrack INSTRUCTION tk_closeBrack INSTRUCTION'
                        j += 8
                    elif Tokens[i].token == 'tk_foreach':
                        aux = ['tk_foreach','tk_openPar','tk_id','tk_in','tk_id','tk_closePar','tk_openBrack',
                        'INSTRUCTION','tk_closeBrack','INSTRUCTION']
                        aux.reverse()
                        stack = stack + aux
                        intro = 'tk_foreach tk_openPar tk_id tk_in tk_id tk_closePar tk_openBrack INSTRUCTION tk_closeBrack INSTRUCTION'
                        j += 10
                    elif Tokens[i].token == 'tk_switch':
                        aux = ['tk_switch','tk_openPar','tk_id','tk_closePar','tk_openBrack',
                        'CASES','tk_closeBrack','INSTRUCTION']
                        aux.reverse()
                        stack = stack + aux
                        intro = 'tk_switch tk_openPar tk_id tk_closePar tk_openBrack CASES tk_closeBrack INSTRUCTION'
                        j+=8
                    elif isDeclarer(Tokens[i].token):
                        aux = ['DECLARER', 'tk_id', 'tk_equal', 'COMPLEMENT', 'INSTRUCTION']
                        aux.reverse()
                        stack = stack + aux
                        intro = 'DECLARER tk_id tk_equal COMPLEMENT INSTRUCTION'
                        j+=5
                    elif Tokens[i].token == 'tk_id':
                        aux = ['tk_id','tk_openPar','PARAMETERS','tk_closePar','tk_semicolon','INSTRUCTION']
                        aux.reverse()
                        stack = stack + aux
                        intro = 'tk_id tk_openPar PARAMETERS tk_closePar tk_semicolon INSTRUCTION'
                        j += 6
                    else:
                        pass
                elif stack[j-1] == 'VALUE':
                    if Tokens[i].token == 'tk_id':
                        out = stack.pop()
                        stack.append('tk_id')
                    elif Tokens[i].token == 'tk_boolean':
                        out = stack.pop()
                        stack.append('tk_boolean')
                    else:
                        error = True
                elif stack[j-1] == 'CASES':
                    out = stack.pop()
                    j -= 1
                    if Tokens[i].token == 'tk_case':
                        aux = ['tk_case', 'DATA','tk_points','INSTRUCTION', 'BREAK', 'CASES']
                        aux.reverse()
                        stack = stack + aux
                        intro = 'tk_case DATA tk_points INSTRUCTION BREAK CASES'
                        j += 6
                    elif Tokens[i].token == 'tk_default':
                        aux = ['tk_default','tk_points','INSTRUCTION','BREAK','CASES']
                        aux.reverse()
                        stack = stack + aux
                        intro = 'tk_default tk_points INSTRUCTION BREAK CASES'
                        j+=5
                    else:
                        pass
                elif stack[j-1] == 'DECLARER':
                    if Tokens[i].token == 'tk_var':
                        out = stack.pop()
                        stack.append('tk_var')
                        intro = 'tk_var'
                    elif Tokens[i].token == 'tk_let':
                        out = stack.pop()
                        stack.append('tk_let')
                        intro = 'tk_let'
                    elif Tokens[i].token == 'tk_const':
                        out = stack.pop()
                        stack.append('tk_const')
                        intro = 'tk_const'
                    else:
                        error = True
                elif stack[j-1] == 'ID_PARAMETERS':
                    out = stack.pop()
                    j-=1
                    if Tokens[i].token == 'tk_id':
                        aux = ['tk_id','ID_PARAMETERS']
                        aux.reverse()
                        stack = stack + aux
                        intro = 'tk_id ID_PARAMETERS'
                        j+=2
                    elif Tokens[i].token == 'tk_comma':
                        aux = ['tk_comma','ID_PARAMETERS']
                        aux.reverse()
                        stack = stack + aux
                        intro = 'tk_comma ID_PARAMETERS'
                        j+=2 
                    else:
                        pass
                elif stack[j-1] == 'PARAMETERS':
                    out = stack.pop()
                    j-=1
                    if isData(Tokens[i].token):
                        aux = ['DATA', 'PARAMETERS']
                        aux.reverse()
                        stack = stack + aux
                        intro = 'DATA PARAMETERS'
                        j+=2
                    elif Tokens[i].token == 'tk_comma':
                        aux = ['tk_comma', 'PARAMETERS']
                        aux.reverse()
                        stack = stack + aux
                        intro = 'tk_comma PARAMETERS'
                        j+=2
                    else:
                        pass
                elif stack[j-1] == 'DATA':
                    if Tokens[i].token == 'tk_number':
                        out = stack.pop()
                        stack.append('tk_number')
                        intro = 'tk_number'
                    elif Tokens[i].token == 'tk_string':
                        out = stack.pop()
                        stack.append('tk_string')
                        intro = 'tk_string'
                    elif Tokens[i].token == 'tk_boolean':
                        out = stack.pop()
                        stack.append('tk_boolean')
                        intro = 'tk_boolean'
                    elif Tokens[i].token == 'tk_id':
                        out = stack.pop()
                        stack.append('tk_id')
                        intro = 'tk_id'
                    else:
                        out = stack.pop()
                        j-=1
                elif stack[j-1] == 'BREAK':
                    out = stack.pop()
                    j-=1
                    if Tokens[i].token == 'tk_break':
                        aux = ['tk_break', 'tk_semicolon']
                        aux.reverse()
                        stack= stack + aux
                        intro = 'tk_break tk_semicolon'
                        j+=2
                    else:
                        pass
                elif stack[j-1] == 'COMPLEMENT':
                    if Tokens[i].token == 'tk_openPar':
                        out = stack.pop()
                        j-=1
                        aux = ['tk_openPar','ID_PARAMETERS','tk_closePar','tk_arrow','tk_openBrack',
                        'INSTRUCTION','tk_closeBrack']
                        aux.reverse()
                        stack = stack + aux
                        intro = 'tk_openPar ID_PARAMETERS tk_closePar tk_arrow tk_openBrack INSTRUCTION tk_closeBrack'
                        j+=7
                    elif isData(Tokens[i].token):
                        out = stack.pop()
                        j-=1
                        aux = ['DATA', 'tk_semicolon']
                        aux.reverse()
                        stack = stack + aux
                        intro = 'DATA tk_semicolon'
                        j+=2
                    
                    else:
                        error = True  
            else:
                
                if Tokens[i].token == stack[j-1]:
                    out = stack.pop()
                    Tokens.remove(Tokens[0])
                    j-=1
                else:
                    error = True
        else:
            cicle = False
        fState = state
        
        if intro == '':
            intro = 'λ'
        if cicle:
            transicion = transicion + out + '; ' + fState + ', ' + intro +')'
        else:
            transicion = 'ACEPTACION'

        print('--PILA-- '+pila)
        print('--ENTRADA-- '+entrada)
        print('--TRANSICION-- '+transicion)
        text2 = text2 + '<tr><th scope="row">'+pila+'</th><td>'+entrada+'</td><td>'+transicion+'</td></tr>'
    
    with open('REPORTE_AUTOMATA_PILA.html', "w") as report:
        report.write(text1 + text2.replace('λ', 'None') +text3)


def isTerminal(token):
    for i in Terminals:
        if token == i:
            return True
    return False

def isDeclarer(token):
    if token == 'tk_var':
        return True
    elif token == 'tk_const':
        return True
    elif token == 'tk_let':
        return True
    else:
        return False

def isData(token):
    if token == 'tk_number':
        return True
    elif token == 'tk_boolean':
        return True
    elif token == 'tk_string':
        return True
    elif token == 'tk_id':
        return True
    else:
        return False