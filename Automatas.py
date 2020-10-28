import Clases

Reservadas = ['let', 'var','const','if','while','foreach','in','switch','case','break','default', 'print']

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
                    Tokens.append(Clases.Token('tk_semiColon',';','se coloca al final de ciertas instrucciones',tokenLine,column))
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
                elif line[i] == ';' or line[i] == '(' or line[i] == ')' or line[i] == '{' or line[i] == '}' or line[i] == ',':
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
                elif line[i] == ';' or line[i] == '(' or line[i] == ')' or line[i] == '{' or line[i] == '}' or line[i] == ',':
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
                elif line[i] == ';' or line[i] == '(' or line[i] == ')' or line[i] == '{' or line[i] == '}' or line[i] == ',':
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
                elif line[i] == ';' or line[i] == '(' or line[i] == ')' or line[i] == '{' or line[i] == '}' or line[i] == ',':
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
            contentT = contentT + '<tr><th scope="row">'+str(iT)+'</th><td>'+token.token+'</td><td>'+token.content+'</td><td>'+token.description+'</td><td>'+str(token.line)+'</td><td>'+str(token.column)+'</td></tr>'
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
        return Clases.Token('tk_word', content, 'palabras reservadas, son palabras pertenecientes al lenguaje', tokenLine, column)
    elif isBool(content):
        return Clases.Token('tk_boolean', content, 'almacena valores de verdad, es decir, verdadero o falso', tokenLine, column)
    else:
        #return Clases.Token('error', content, 'Se detecto error', tokenLine, column)
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
        return Clases.Token('tk_semiColon',';','se coloca al final de ciertas instrucciones',tokenLine,column)
    elif value == ',':
        return Clases.Token('tk_comma',',','se utiliza para separar parametros',tokenLine,column)
    

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