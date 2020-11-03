from graphviz import Digraph
import Automatas

def createDiagram(Tokens, dot, char, edges, first, iChar, subExpression):
    if subExpression:
        edges.append(chr(char-1)+chr(char))
    else:
        if not first:
            edges.append(chr(iChar)+chr(char))
    cicle = True
    elements = 0
    for element in Tokens:
        elements+=1
    i = 0
    while cicle:
        if Tokens[i].token == 'tk_if':
            iChar = char
            dot.node(chr(char), 'Sentencia if')
            char += 1
            dot.node(chr(char), 'Condicion: '+Tokens[i+2].content)
            edges.append(chr(char-1)+chr(char))
            char += 1
            i += 4
            if SubExpression(i,Tokens) != []:
                char = createDiagram(SubExpression(i, Tokens),dot,char,edges,False,iChar, True)
                #edges.append(chr(char)+chr(createDiagram(SubExpression(i, Tokens),dot,char,edges,False,iChar, True)))
                #edges.append(chr(iChar)+chr(char))
                i+=2
                for element in SubExpression(i-2,Tokens):
                    i+=1
            else:
                i+=2
        elif Tokens[i].token == 'tk_while':
            iChar = char
            dot.node(chr(char), 'Sentencia while')
            char += 1
            dot.node(chr(char), 'Condicion: '+Tokens[i+2].content)
            edges.append(chr(char-1)+chr(char))
            char += 1
            i += 4
            if SubExpression(i,Tokens) != []:
                char = createDiagram(SubExpression(i, Tokens),dot,char,edges,False,iChar, True)
                #edges.append(chr(char)+chr(createDiagram(SubExpression(i, Tokens),dot,char,edges,False,iChar, True)))
                #edges.append(chr(iChar)+chr(char))
                i+=2
                for element in SubExpression(i-2,Tokens):
                    i+=1
            else:
                i+=2
        elif Tokens[i].token == 'tk_foreach':
            iChar = char
            dot.node(chr(char), 'Sentencia foreach')
            char+=1
            dot.node(chr(char), 'Elementos a evaluar: '+Tokens[i+2].content+' en '+Tokens[i+4].content)
            edges.append(chr(char-1)+chr(char))
            char+=1
            i+=6
            if SubExpression(i,Tokens) != []:
                char = createDiagram(SubExpression(i, Tokens),dot,char,edges,False,iChar, True)
                #edges.append(chr(iChar)+chr(char))
                #edges.append(chr(char)+chr(createDiagram(SubExpression(i, Tokens),dot,char,edges,False,iChar, True)))
                i+=2
                for element in SubExpression(i-2,Tokens):
                    i+=1
            else:
                i+=2
        elif Automatas.isDeclarer(Tokens[i].token):
            iChar = char
            if Automatas.isData(Tokens[i+3].token):
                dot.node(chr(char), 'Asignacion: '+Tokens[i+1].content)
                char+=1
                i+=5
            else:
                dot.node(chr(char), 'Definicion: '+Tokens[i+1].content)
                char+=1
                dot.node(chr(char), 'Parametros: ('+Parameters(i+4,Tokens)+')')
                edges.append(chr(char-1)+chr(char))
                char+=1

                while Tokens[i].token != 'tk_arrow':
                    i+=1
                i+=1
                if SubExpression(i,Tokens) != []:
                    char = createDiagram(SubExpression(i, Tokens),dot,char,edges,False,iChar, True)
                    #edges.append(chr(char)+chr(createDiagram(SubExpression(i, Tokens),dot,char,edges,False,iChar, True)))
                    #edges.append(chr(iChar)+chr(char))
                    i+=2
                    for element in SubExpression(i-2,Tokens):
                        i+=1
                else:
                    i+=2                
        elif Tokens[i].token == 'tk_id':
            iChar = char
            dot.node(chr(char), 'Llamada a funcion: '+Tokens[i].content)
            char+=1
            dot.node(chr(char), 'Parametros: ('+Parameters((i+1),Tokens)+')')
            edges.append(chr(char-1)+chr(char))
            char+=1

            while Tokens[i].token != 'tk_semicolon':
                i+=1
            i+=1

        print(str(i)+'------------------'+str(elements-1))
        if i >= elements-1:
            cicle=False
        else:
         edges.append(chr(iChar)+chr(char))
    return char
    
                
def SubExpression(i, Tokens):
    subExpression = True
    iteration = 0
    aux = []
    counter = 0
    while subExpression:
        iteration += 1
        aux.append(Tokens[i])
        if Tokens[i].token == 'tk_openBrack':
            counter += 1
        elif Tokens[i].token == 'tk_closeBrack':
            counter -= 1
        
        if counter == 0:
            subExpression = False
        
        i+=1

    if iteration == 2:
        return []
    else:
        aux.remove(aux[0])
        aux.remove(aux[iteration-2])
        return aux

def Parameters(i, Tokens):
    aux = ''
    cicle = True
    while cicle:
        if Tokens[i].token == 'tk_closePar':
            cicle = False
        elif Tokens[i].token == 'tk_comma':
            aux = aux+' , '
        else:
            aux = aux+Tokens[i].content
        i+=1
    return aux