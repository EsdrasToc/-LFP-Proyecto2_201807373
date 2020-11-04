from graphviz import Digraph
import Automatas

def createDiagram(Tokens, dot, char, edges, first, iChar, subExpression):
    if subExpression:
        edges.append(chr(charM(char))+chr(char))
    else:
        if not first:
            edges.append(chr(iChar)+chr(char))
        
    cicle = True
    elements = 0
    elements = len(Tokens)
    i = 0
    while cicle:
        if Tokens[i].token == 'tk_if':
            iChar = char
            dot.node(chr(char), 'Sentencia if')
            char = charP(char)
            dot.node(chr(char), 'Condicion: '+Tokens[i+2].content)
            edges.append(chr(charM(char))+chr(char))
            char = charP(char)
            i += 4
            if SubExpression(i,Tokens) != []:
                char = createDiagram(SubExpression(i, Tokens),dot,char,edges,False,iChar, True)
                i+=2
                i += len(SubExpression(i-2,Tokens))
            else:
                i+=2
        elif Tokens[i].token == 'tk_while':
            iChar = char
            dot.node(chr(char), 'Sentencia while')
            char = charP(char)
            dot.node(chr(char), 'Condicion: '+Tokens[i+2].content)
            edges.append(chr(charM(char))+chr(char))
            char = charP(char)
            i += 4
            if SubExpression(i,Tokens) != []:
                char = createDiagram(SubExpression(i, Tokens),dot,char,edges,False,iChar, True)
                i+=2
                i += len(SubExpression(i-2,Tokens))
            else:
                i+=2
        elif Tokens[i].token == 'tk_foreach':
            iChar = char
            dot.node(chr(char), 'Sentencia foreach')
            char = charP(char)
            dot.node(chr(char), 'Elementos a evaluar: '+Tokens[i+2].content+' en '+Tokens[i+4].content)
            edges.append(chr(charM(char))+chr(char))
            char = charP(char)
            i+=6
            if SubExpression(i,Tokens) != []:
                char = createDiagram(SubExpression(i, Tokens),dot,char,edges,False,iChar, True)
                i+=2
                """for element in SubExpression(i-2,Tokens):
                    i+=1"""
                i += len(SubExpression(i-2,Tokens))
            else:
                i+=2
        elif Automatas.isDeclarer(Tokens[i].token):
            iChar = char
            if Automatas.isData(Tokens[i+3].token):
                dot.node(chr(char), 'Asignacion: '+Tokens[i+1].content)
                char = charP(char)
                i+=5
            else:
                dot.node(chr(char), 'Definicion: '+Tokens[i+1].content)
                char = charP(char)
                dot.node(chr(char), 'Parametros: ('+Parameters(i+4,Tokens)+')')
                edges.append(chr(charM(char))+chr(char))
                char = charP(char)

                while Tokens[i].token != 'tk_arrow':
                    i+=1
                i+=1
                if SubExpression(i,Tokens) != []:
                    char = createDiagram(SubExpression(i, Tokens),dot,char,edges,False,iChar, True)
                    i+=2
                    i += len(SubExpression(i-2,Tokens))
                else:
                    i+=2                
        elif Tokens[i].token == 'tk_id':
            iChar = char
            dot.node(chr(char), 'Llamada a funcion: '+Tokens[i].content)
            char = charP(char)
            dot.node(chr(char), 'Parametros: ('+Parameters((i+1),Tokens)+')')
            edges.append(chr(charM(char))+chr(char))
            char = charP(char)

            while Tokens[i].token != 'tk_semicolon':
                i+=1
            i+=1
        elif Tokens[i].token == 'tk_switch':
            print('ENTRO EN SWITCH')
            iChar = char
            dot.node(chr(char), 'Sentencia switch, condicion: '+Tokens[i+2].content)
            char = charP(char)
            i+=4
            if SubExpression(i,Tokens) != []:
                print('LLEGO HASTA ACA')
                for instruction in SwitchCases(SubExpression(i,Tokens)):
                    if instruction[0].token == 'tk_case':
                        dot.node(chr(char), 'Caso: '+instruction[1].content)
                    else:
                        dot.node(chr(char), 'Caso: por default')
                    edges.append(chr(iChar)+chr(char))
                    char = charP(char)
                    if instruction[0].token == 'tk_case':
                        instruction.remove(instruction[0])
                        instruction.remove(instruction[0])
                        instruction.remove(instruction[0])
                    else:
                        instruction.remove(instruction[0])
                        instruction.remove(instruction[0])
                    if len(instruction) != 0:    
                        char = createDiagram(instruction, dot, char, edges, False, iChar, True)
                
                i += len(SubExpression(i,Tokens))
                i +=2
            else:
                print('O HASTA ACA')
                i+=2
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
        if Tokens[i].token == 'tk_openPar':
            i+=1
            continue
        if Tokens[i].token == 'tk_closePar':
            cicle = False
        elif Tokens[i].token == 'tk_comma':
            aux = aux+' , '
        else:
            aux = aux+Tokens[i].content
        i+=1
    return aux
    
def SwitchCases(Tokens):
    cicle = True
    aux = []
    instructions = []
    i = 0
    while cicle:
        if i > len(Tokens)-1:
            instructions.append(aux)
            instructions.remove(instructions[0])
            break
            
        if Tokens[i].token == 'tk_case' or Tokens[i].token == 'tk_default':
            instructions.append(aux)
            aux = None
            aux = []
            aux.append(Tokens[i])
        elif Tokens[i].token == 'tk_break':
            i+=2
            continue
        elif i == len(Tokens)-1:
            aux.append(Tokens[i])
            instructions.append(aux)
            cicle = False
            instructions.remove(instructions[0])
        else:
            aux.append(Tokens[i])
        i+=1
    
    return instructions

def charM(char):
    if char == 97:
        return 90
    else:
        return char - 1

def charP(char):
    if char == 90:
        return 97
    else:
        return char + 1