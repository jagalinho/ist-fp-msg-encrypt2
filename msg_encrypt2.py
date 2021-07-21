#FP 2016-17 Projeto 2
#TP - 87667 - Joao Andre de Franca Ferreira Galinho

#--------------------------------TIPO POSICAO------------------------------------------------------------------
#Construtores:
def faz_pos(linha,coluna):
    """Funcao que dada uma linha e uma coluna, retorna uma posicao com a linha e coluna correspondentes."""
    if not all((isinstance(cord,int) and cord>=0) for cord in (linha,coluna)):                                      #Testa se tanto a linha como a coluna dadas sao numeros inteiros maiores que 0
        raise ValueError("faz_pos: argumentos errados")
    return (linha,coluna)

#Seletores:
def linha_pos(pos):
    """Funcao que dada uma posicao, retorna a coordenada correspondente a sua linha."""
    return pos[0]

def coluna_pos(pos):
    """Funcao que dada uma posicao, retorna a coordenada correspondente a sua coluna."""
    return pos[1]

#Reconhecedores:
def e_pos(arg):
    """Funcao que dado um argumento, testa se e uma posicao."""
    return (isinstance(arg,tuple)
            and len(arg)==2
            and all((isinstance(cord,int) and cord>=0) for cord in arg))                                            #Testa se ambas as coordenadas do argumento sao numeros inteiros maiores que 0

#Testes:
def pos_iguais(pos1,pos2):
    """Funcao que dadas duas posicoes, testa se sao iguais."""
    return pos1==pos2

#---------------------------------TIPO CHAVE-------------------------------------------------------------------
#Construtores:
def gera_chave_linhas(letras,mgc):
    """Funcao que dado um tuplo com 25 carcateres maiusculos diferentes e uma mensagem apenas com caracteres maiusculos e espacos, retorna uma chave com os elementos presentes na mensagem seguidos do resto dos elementos presentes no tuplo."""
    if not (isinstance(letras,tuple)
            and len(set(letras))==25                                                                                #Testa se letras tem 25 elementos diferentes
            and all((isinstance(e,str) and len(e)==1 and ord(e[0]) in range(65,91)) for e in letras)                #Testa se todos os elementos de letras sao strings com apenas 1 caracter maiusculo
            and isinstance(mgc,str)
            and all(ord(e) in [32]+list(range(65,91)) for e in mgc)):                                               #Testa se todos os caracteres da mensagem sao caracteres maiusculos ou espacos
        raise ValueError("gera_chave_linhas: argumentos errados")
    chave,elementos_chave=[],[]
    for e in mgc.replace(" ",""):                                                                                   #Ciclo que corre para todos os caracteres da mensagem, a excecao dos espacos
        if e not in elementos_chave and e in letras: elementos_chave+=[e]
    for e in letras:
        if e not in elementos_chave: elementos_chave+=[e]
    for i in range(0,25,5):                                                                                         #A partir dos elementos da chave cria uma chave que consiste em uma lista com 5 listas de 5 elementos
        chave+=[elementos_chave[i:i+5]]
    return chave

def gera_chave_espiral(letras,mgc,sentido,pos):
    """Funcao que dado um tuplo com 25 caracteres maiusculos diferentes, uma mensagem apenas com caracteres maiusculos e espacos, um sentido ("r"->Sentido dos ponteiros do relogio; "c"->Sentido contrario ao dos ponteiros do relogio) e uma posicao,
    retorna uma chave com os elementos presentes na mensagem seguidos do resto dos elementos presentes no tuplo dispostos em espiral com inicio na posicao e com o sentido dado."""
    if not (isinstance(letras,tuple)
            and len(set(letras))==25                                                                                #Testa se letras tem 25 elementos diferentes
            and all((isinstance(e,str) and len(e)==1 and ord(e[0]) in range(65,91)) for e in letras)                #Testa se todos os elementos de letras sao strings com apenas 1 caracter maiusculo
            and isinstance(mgc,str)
            and all(ord(e) in [32]+list(range(65,91)) for e in mgc)                                                 #Testa se todos os caracteres da mensagem sao caracteres maiusculos ou espacos
            and sentido in ("r","c")
            and e_pos(pos)
            and all(cord in (0,4) for cord in pos)):                                                                #Testa se a posicao dada corresponde a um dos cantos
        raise ValueError("gera_chave_espiral: argumentos errados")
    def prox_pos(pos,direcao):
        """Funcao que dada a posicao atual e a direcao atual, retorna a proxima posicao a preencher/testar. Se a nova posicao nao existir, a funcao retorna novamente a posicao atual."""
        linha,coluna=linha_pos(pos)+direcao[0],coluna_pos(pos)+direcao[1]
        if not all(cord in range(5) for cord in (linha,coluna)): return pos                                         #Testa se a nova posicao existe, isto e, se ambas as suas coordenadas estao entre 0 e 4
        return faz_pos(linha,coluna)
    chave=[[" " for coluna in range(5)] for linha in range(5)]
    direcao={"r":{faz_pos(0,0):(0,1),faz_pos(0,4):(1,0),faz_pos(4,4):(0,-1),faz_pos(4,0):(-1,0)},
             "c":{faz_pos(0,0):(1,0),faz_pos(4,0):(0,1),faz_pos(4,4):(-1,0),faz_pos(0,4):(0,-1)}}[sentido][pos]     #Dicionario que consoante o sentido e a posicao inicial devolve a direcao inicial
    prox_dir={"r":{(0,1):(1,0),(1,0):(0,-1),(0,-1):(-1,0),(-1,0):(0,1)},
              "c":{(0,1):(-1,0),(1,0):(0,1),(0,-1):(1,0),(-1,0):(0,-1)}}                                            #Dicionario que consoante o sentido e a direcao atual devolve a proxima direcao
    for e in mgc.replace(" ",""):                                                                                   #Ciclo que corre para todos os caracteres da mensagem a excecao dos espacos
        if e not in sum(chave,[]) and e in letras:
            chave=muda_chave(chave,pos,e)                                                                           #Insere o elemento na posicao atual da chave
            if not ref_chave(chave,prox_pos(pos,direcao))==" ": direcao=prox_dir[sentido][direcao]                  #Testa se a proxima posicao da chave esta vazia; Se nao estiver passa para a proxima direcao
            pos=prox_pos(pos,direcao)                                                                               #Atualiza a posicao atual para a proxima posicao
    for e in letras:
        if e not in sum(chave,[]):
            chave=muda_chave(chave,pos,e)                                                                           #Insere o elemento na posicao atual da chave
            if not ref_chave(chave,prox_pos(pos,direcao))==" ": direcao=prox_dir[sentido][direcao]                  #Testa se a proxima posicao da chave esta vazia; Se nao estiver passa para a proxima direcao
            pos=prox_pos(pos,direcao)                                                                               #Atualiza a posicao atual para a proxima posicao
    return chave

#Seletores:
def ref_chave(chave,pos):
    """Funcao que dada uma chave e uma posicao, retorna o elemento correspondente a posicao na chave."""
    return chave[linha_pos(pos)][coluna_pos(pos)]

def diz_pos_chave(chave,elemento):
    """Funcao que dada uma chave e um elemento, retorna a posicao que corresponde ao elemento na chave."""
    for linha in range(5):
        for coluna in range(5):
            if chave[linha][coluna]==elemento:                                                                      #Testa para todas as coordenadas possiveis na chave se o elemento correspondente a estas e igual ao elemento dado
                return faz_pos(linha,coluna)

#Modificadores:
def muda_chave(chave,pos,elemento):
    """Funcao que dada uma chave, uma posicao e um elemento, retorna a chave com o elemento na posicao dada."""
    chave[linha_pos(pos)][coluna_pos(pos)]=elemento
    return chave

def circula(cord):
    """[Funcao Auxiliar]\nFuncao que dada uma coordenada, torna possivel a sua incrementacao de forma circular."""
    return {-1:4,5:0}.get(cord,cord)                                                                                #Se o valor for -1 a funcao retorna 4; Se o valor for 5 a funcao retorna 0; Se nao for nenhum dos dois a funcao retorna o mesmo valor

#Reconhecedores:
def e_chave(arg):
    """Funcao que dado um argumento, testa se e uma chave."""
    return (isinstance(arg,list)
            and len(arg)==5
            and all(len(linha)==5 for linha in arg)                                                                 #Testa se todas as linhas do argumento tem 5 elementos
            and len(sum(arg,[]))==len(set(sum(arg,[])))                                                             #Testa se o argumento tem elementos repetidos
            and all((isinstance(e,str) and len(e)==1 and ord(e[0]) in range(65,91)) for e in sum(arg,[])))          #Testa se todos os elementos do argumento sao strings com apenas 1 caracter maiusculo

#Transformadores:
def string_chave(chave):
    """Funcao que dada uma chave, retorna uma string com os elementos da chave com a formatacao necessaria para serem impressos em forma de matriz."""
    string=""
    for linha in chave:
        for e in linha:
            string+=e+" "
        string+="\n"                                                                                                #No final de cada linha (sublista da chave) adiciona uma mudanca de linha
    return string

#--------------------------ENCRIPTACAO/DESENCRIPTACAO----------------------------------------------------------
def digramas(mens):
    """Funcao que dada uma mensagem, retorna essa mensagem em forma de conjunto de digramas validos."""
    mens=mens.replace(" ","")                                                                                       #Retira os espacos da mensagem
    if not len(mens)%2==0: mens+="X"                                                                                #Adiciona um X caso o numero de caracteres nao seja par
    while not all(mens[i]!=mens[i+1] for i in range(0,len(mens),2)):                                                #Testa se a mensagem ja e um conjunto valido de digramas e repete a funcao se ainda nao o for
        for i in range(0,len(mens),2):
            if mens[i]==mens[i+1]: mens=mens[:i+1]+"X"+mens[i+1:]                                                   #Se os dois elementos do digrama forem iguais adiciona um X entre eles
        if not len(mens)%2==0:
            if mens[-1]=="X": mens=mens[:-1]                                                                        #Remove o ultimo caracter caso este seja X e o numero de caracteres nao for par
            else: mens+="X"                                                                                         #Adiciona um X caso o ultimo caracter nao seja X e o numero de caracteres nao for par
    return mens

def figura(digrm,chave):
    """Funcao que dado um digrama e uma chave, retorna um tuplo com as posicoes correspondentes aos caracteres do digrama na chave e com a figura que estes desenham ("l"->Linha; "c"->Coluna; "r"->Retangulo)."""
    pos1,pos2=diz_pos_chave(chave,digrm[0]),diz_pos_chave(chave,digrm[1])
    if linha_pos(pos1)==linha_pos(pos2): return ("l",pos1,pos2)                                                     #Se as linhas forem iguais significa que as posicoes dos elementos do digrama na chave formam uma linha
    if coluna_pos(pos1)==coluna_pos(pos2): return ("c",pos1,pos2)                                                   #Se as colunas forem iguais significa que as posicoes dos elementos do digrama na chave formam uma coluna
    return ("r",pos1,pos2)                                                                                          #Se nenhuma coordenada for igual significa que as posicoes dos elementos do digrama na chave formam um retangulo

def codifica_l(pos1,pos2,inc):
    """Funcao que dadas duas posicoes com linhas iguais e um valor (1->Codifica ou -1->Descodifica), retorna um tuplo com as duas novas posicoes correspondentes aos elementos codificados/descodificados."""
    return (faz_pos(linha_pos(pos1),circula(coluna_pos(pos1)+inc)),                                                 #Incrementa o valor das colunas das posicoes por 1(encriptar) ou -1(desencriptar), estando estas sempre a rodar pelos valores entre 0 e 4
            faz_pos(linha_pos(pos2),circula(coluna_pos(pos2)+inc)))

def codifica_c(pos1,pos2,inc):
    """Funcao que dadas duas posicoes com colunas iguais e um valor (1->Codifica ou -1->Descodifica), retorna um tuplo com as duas novas posicoes correspondentes aos elementos codificados/descodificados."""
    return (faz_pos(circula(linha_pos(pos1)+inc),coluna_pos(pos1)),                                                 #Incrementa o valor das linhas das posicoes por 1(encriptar) ou -1(desencriptar), estando estas sempre a rodar pelos valores entre 0 e 4
            faz_pos(circula(linha_pos(pos2)+inc),coluna_pos(pos2)))

def codifica_r(pos1,pos2):
    """Funcao que dadas duas posicoes com linhas e colunas diferentes e um valor (1->Codifica ou -1->Descodifica), retorna um tuplo com as duas novas posicoes correspondentes aos elementos codificados/descodificados."""
    return (faz_pos(linha_pos(pos1),coluna_pos(pos2)),                                                              #As posicoes trocam de colunas entre si, a primeira fica com a coluna da segunda e a segunda com a coluna da primeira
            faz_pos(linha_pos(pos2),coluna_pos(pos1)))

def codifica_digrama(digrm,chave,inc):
    """Funcao que dado um digrama, uma chave e um valor (1->Codifica ou -1->Descodifica), retorna o digrama codificado/descodificado consoante a posicao dos seus caracteres na chave."""
    fig=figura(digrm,chave)
    if fig[0]=="l": pos_cod=codifica_l(fig[1],fig[2],inc)
    elif fig[0]=="c": pos_cod=codifica_c(fig[1],fig[2],inc)
    else: pos_cod=codifica_r(fig[1],fig[2])
    return ref_chave(chave,pos_cod[0])+ref_chave(chave,pos_cod[1])                                                  #Junta os caracteres correspondentes as duas posicoes codificadas para formar o digrama codificado

def codifica(mens,chave,inc):
    """Funcao que dada uma mensagem, uma chave e um valor (1->Codifica ou -1->Descodifica), retorna a mensagem codificada/descodificada consoante a posicao dos seus caracteres na chave."""
    mens,mens_cod=digramas(mens),""
    for i in range(0,len(mens),2):                                                                                  #Ciclo que corre para todos os digramas da mensagem
        mens_cod+=codifica_digrama(mens[i]+mens[i+1],chave,inc)
    return mens_cod
