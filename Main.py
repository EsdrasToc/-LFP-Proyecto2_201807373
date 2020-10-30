import Automatas
#DECLARACION DE VARIABLES#
document = []
cicle = True
option = ''
path = ''
tokens = []

while cicle:

    #IMPRESION DE MENU#
    print('========================================================')
    print('[1] - Cargar Script')
    print('[2] - Manejo AFD')
    print('[3] - Pila Interactiva')
    print('[4] - Diagrama de Bloques de Codigo')
    print('[5] - Salir')

    print('Ingrese el numeral de la instruccion que desea ejecutar:')
    option = input('$')

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
        for token in tokens:
            if token.token != 'error' and token.token != 'tk_comment':
                aux.append(token)
        Automatas.syntacticAnalysis(aux)
    elif option == '4':
        print('diagrama de bloques de codigo')
    elif option == '5':
        print('HASTA PRONTO')
        cicle = False
    else:
        print('POR FAVOR INGRESE UNA OPCION VALIDA')