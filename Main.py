import Automatas
import outputFunctions
from graphviz import Digraph

#DECLARACION DE VARIABLES#
document = []
cicle = True
option = ''
path = ''
tokens = []
dot = None
edges = []
while cicle:

    #IMPRESION DE MENU#
    print('========================================================')
    print('[1] - Cargar Script')
    print('[2] - Manejo AFD')
    print('[3] - Pila Interactiva')
    print('[4] - Diagrama de Bloques de Codigo')
    print('[5] - Salir')

    print('Ingrese el numeral de la instruccion que desea ejecutar:')
    option = input()
    #LECTURA DE INSTRUCCION#
    if option == '1':
        print('--- INGRESE LA RUTA DEL SCRIPT QUE DESEA CARGAR ---')
        path = input('RUTA: ')
        try:
            with open(path, "r") as f:
                document = []
                for line in f:
                    document.append(line)
        except:
            print('--- OCURRIO UN ERROR AL LEER: '+path+' ---')
    elif option == '2':
        tokens = []
        Automatas.readScript(document, tokens)
    elif option == '3':
        aux = []
        tokens = []
        try:
            Automatas.readScript(document, tokens)
            for token in tokens:
                if token.token != 'error' and token.token != 'tk_comment':
                    aux.append(token)
        except:
            print('OCURRIO UN ERROR EN EL AFD')
        
        try:
            Automatas.syntacticAnalysis(aux, True)
        except:
            print('OCURRIO UN ERROR EN EL AUTOMATA DE PILA')
    elif option == '4':
        aux = []
        tokens = []
        edges = []
        dot = Digraph(comment='flujo de script')
        try:
            Automatas.readScript(document, tokens)
            for token in tokens:
                if token.token != 'error' and token.token != 'tk_comment':
                    aux.append(token)
        except:
            print('OCURRIO UN ERROR EN EL AFD')
        try:
            outputFunctions.createDiagram(aux,dot,65,edges,True,65, False)
            dot.edges(edges)
            print(dot.source)
            try:
                dot.render('test-output/instrucciones.gv', view=True)
            except:
                with open('instrucciones.gv', "w") as report:
                    report.write(dot.source)
                print('SE CREO UN ARCHIVO CON EXTENSION .gv')
        except:
            print('NO SE PUDO DIAGRAMAR CORRECTAMENTE')
    elif option == '5':
        print('HASTA PRONTO')
        cicle = False
    else:
        print('POR FAVOR INGRESE UNA OPCION VALIDA')