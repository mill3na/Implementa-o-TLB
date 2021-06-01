
import argparse, random, re
contador_falsos_positivos = 0

"""comando de teste: python main.py --total_cache 4 --tipo_mapeamento=AS --arquivo_acesso=enderecosInteiros.txt --debug 1 --politica_substituicao LRU"""
def existe_posicao_vazia(memoria_cache, qtd_conjuntos, posicao_memoria):
    """Verifica se existe na cache uma posição de memória que ainda não foi utilizada,
    se existir, essa posição é retornada.
    Arguments:
      memoria_cache {list} -- memória cache
      qtd_conjuntos {int} -- número de conjuntos da cache
      posicao_memoria {int} -- posição de memória que se quer armazenar na cache
    Returns:
      [int] -- com a primeira posição de memória vazia do conjunto
    """
    num_conjunto = get_num_conjuno_posicao_memoria(posicao_memoria, qtd_conjuntos)
    lista_posicoes = get_lista_posicoes_cache_conjunto(memoria_cache, num_conjunto, qtd_conjuntos)

    # verifica se alguma das posições daquele conjunto está vazia
    for x in lista_posicoes:
        if memoria_cache[x] == -1:
            return x
    return -1


def get_num_conjuno_posicao_memoria(posicao_memoria, qtd_conjuntos):
    """Retorna o número do conjunto onde essa posição de memória é sempre mapeada
    Arguments:
      posicao_memoria {int} -- posição de memória que se quer acessar
      qtd_conjuntos {int} -- número de conjuntos que a cache possui
    """
    return int(posicao_memoria) % int(qtd_conjuntos)


def print_cache_associativo(cache):
    """Imprime o estado da memória cache no modelo de mapeamento associativo.
    """
    print("+-------------------------------+")
    print("|Tamanho Cache: {:>16}| ".format(len(cache)))
    print("+-------------+-----------------+")
    print("|        Cache Associativo      |")
    print("+-------------+-----------------+")
    print("|Posição Cache | Posição Memória|")
    print("+-------------+-----------------+")
    for posicao, valor in cache.items():
        print("|{:>14}|{:>16}|".format(hex(posicao), hex(valor)))
    print("+-------------+-----------------+")


def print_cache_associativo_conjunto(cache, qtd_conjuntos):
    """Imprime o estado da memória cache no modelo de mapeamento associativo por conjunto.
    """
    print("+------------------------------+")
    print("|Tamanho: {:>21}|\n|Conjuntos: {:>19}|".format(len(cache), qtd_conjuntos))
    print("+------------------------------+")
    print("+  Cache Associativo Conjunto  +")
    print("+-------+-------+--------------+")
    print("|#\t| Cnj\t|   Pos Memória|")
    print("+-------+-------+--------------+")
    for posicao, valor in cache.items():
        num_conjunto = get_num_conjuno_posicao_memoria(posicao, qtd_conjuntos)
        print("|{} \t|{:4}\t|\t   {:>4}|".format(posicao, num_conjunto, valor))
    print("+-------+-------+--------------+")


def inicializar_cache(total_cache):
    """Cria uma memória cache zerada utilizando dicionários (chave, valor) e com
    valor padrão igual a '-1'
    Arguments:
      total_cache {int} -- tamanho total de palavras da cache
    Returns:
      [list] -- [dicionário]
    """
    # zera total a memória cache
    memoria_cache = {}

    # popula a memória cache com o valor -1, isso indica que a posição não foi usada
    for x in range(0, total_cache):
        memoria_cache[x] = -1

    return memoria_cache


def verifica_posicao_em_cache_associativo_conjunto(memoria_cache, qtd_conjuntos, posicao_memoria, ):
    """Verifica se uma determinada posição de memória está na cache no modo associativo / associativo por conjunto
    Arguments:
      memoria_cache {list} -- memória cache
      qtd_conjuntos {int} -- número de conjuntos do cache
      posicao_memoria {int} -- posição que se deseja acessar
    """
    num_conjunto = int(posicao_memoria) % int(qtd_conjuntos)

    while num_conjunto < len(memoria_cache):
        if memoria_cache[num_conjunto] == posicao_memoria:
            return num_conjunto

        num_conjunto += qtd_conjuntos

    # não achou a posição de memória na cache
    return -1


def get_lista_posicoes_cache_conjunto(memoria_cache, num_conjunto, qtd_conjuntos):
    """Retorna uma lista com todas as posições da memória cache que fazem parte de um determinado conjunto.
    Arguments:
      memoria_cache {list} -- memória cache
      num_conjunto {int} -- número do conjunto que se quer saber quais são os endereçamentos associados com aquele conjunto
      qtd_conjuntos {int} -- quantidade total de conjuntos possíveis na memória
    Returns:
      [list] -- lista de posições de memória associada com um conjunto em particular
    """
    lista_posicoes = []
    posicao_inicial = num_conjunto
    while posicao_inicial < len(memoria_cache):
        lista_posicoes.append(posicao_inicial)
        posicao_inicial += qtd_conjuntos
    return lista_posicoes

def politica_substituicao_LRU_miss(memoria_cache, qtd_conjuntos, posicao_memoria):
    """Nessa politica de substituição quando ocorre um HIT a posição vai para o topo da fila,
    se ocorrer um MISS remove o elemento 0 e a posição da cache onde a memória foi alocada é
    colocada no topo da fila
    Arguments:
      memoria_cache {list} -- memóiria cache
      qtd_conjuntos {int} -- quantidade de conjuntos
      posicao_memoria {int} -- posição de memória que será acessada
    """
    num_conjunto = get_num_conjuno_posicao_memoria(posicao_memoria, qtd_conjuntos)
    lista_posicoes = get_lista_posicoes_cache_conjunto(memoria_cache, num_conjunto, qtd_conjuntos)

    # copiar os valores de cada posição da cache do conjunto em questão uma posição para traz
    for posicao_cache in lista_posicoes:
        proxima_posicao = posicao_cache + qtd_conjuntos
        if proxima_posicao < len(memoria_cache):
            memoria_cache[posicao_cache] = memoria_cache[proxima_posicao]
    # coloca a posição que acabou de ser lida na topo da lista, assim, ela nesse momento é a última que será removida
        verificar_falsos_positivos(memoria_cache, contador_falsos_positivos)

    memoria_cache[lista_posicoes[-1]] = posicao_memoria

    if debug:
        print('Posição Memória: {}'.format(posicao_memoria))
        print('Conjunto: {}'.format(num_conjunto))
        print('Lista posições: {}'.format(lista_posicoes))

def politica_substituicao_LRU_hit(memoria_cache, qtd_conjuntos, posicao_memoria, posicao_cache_hit):
    """Nessa politica de substituição quando ocorre um HIT a posição vai para o topo da fila,
    se ocorrer um MISS remove o elemento 0 e a posição da cache onde a memória foi alocada é
    colocada no topo da fila
    Arguments:
      memoria_cache {list} -- memóiria cache
      qtd_conjuntos {int} -- quantidade de conjuntos
      posicao_memoria {int} -- posição de memória que será acessada
      posicao_cache_hit {int} -- posição de memória cache onde o dados da memória principal está
    """
    num_conjunto = get_num_conjuno_posicao_memoria(posicao_memoria, qtd_conjuntos)
    lista_posicoes = get_lista_posicoes_cache_conjunto(memoria_cache, num_conjunto, qtd_conjuntos)

    # copiar os valores de cada posição da cache do conjunto em questão uma posição para traz
    for posicao_cache in lista_posicoes:
        if posicao_cache_hit <= posicao_cache:
            # em uma cache com 4 conjuntos e 20 posições, as posições do 'conjunto 0' são:
            # [0, 4, 8, 12, 16], se o hit for na posição 4, então, então, será necessário copiar os dados da posição
            # 0 não faz nada
            # 4 <- 8
            # 8 <- 12
            # 12 <- 16
            # 16 <- 4
            proxima_posicao = posicao_cache + qtd_conjuntos
            if proxima_posicao < len(memoria_cache):
                memoria_cache[posicao_cache] = memoria_cache[proxima_posicao]

        verificar_falsos_positivos(memoria_cache, contador_falsos_positivos)

    # coloca no topo da pilha a posição de memória que acabou de ser lida
    memoria_cache[lista_posicoes[-1]] = posicao_memoria

    if debug:
        print('Posição Memória: {}'.format(posicao_memoria))
        print('Conjunto: {}'.format(num_conjunto))
        print('Lista posições: {}'.format(lista_posicoes))


def executar_mapeamento_associativo_conjunto(total_cache, qtd_conjuntos, posicoes_memoria_para_acessar,
                                             politica_substituicao='RANDOM'):
    """Executa a operação de mapeamento associativo, ou seja, não existe uma posição específica
    para o mapemento de uma posição de memória.
    Arguments:
      total_cache {int} -- tamanho total de palavras da cache
      qtd_conjuntos {int} -- quantidade de conjuntos na cache
      posicoes_memoria_para_acessar {list} -- quais são as posições de memória que devem ser acessadas
      politica_substituicao {str} -- Qual é a política para substituição caso a posição de memória desejada não esteja na cache E não exista espaço vazio
    """

    memoria_cache = inicializar_cache(total_cache)

    # se o número de conjuntos for igual a zero, então estamos simulando
    # com a cache associativo!
    nome_mapeamento = 'Associativo'
    if qtd_conjuntos == 1:
        print_cache_associativo(memoria_cache)
    else:
        nome_mapeamento = 'Associativo Por Conjunto'
        print_cache_associativo_conjunto(memoria_cache, qtd_conjuntos)

    num_hit = 0
    num_miss = 0

    # se a política for fifo então inicializa a lista de controle

  # if politica_substituicao == 'FIFO':
  #     inicializar_contador_fifo()

    # se a política for fifo então inicializa a lista de controle
  #  if politica_substituicao == 'LFU':
#     inicializar_contador_lfu()

    # percorre cada uma das posições de memória que estavam no arquivo
    for index, posicao_memoria in enumerate(posicoes_memoria_para_acessar):
        print('\n\n\nInteração número: {}'.format(index + 1))
        # verificar se existe ou não a posição de memória desejada na cache
        inserir_memoria_na_posicao_cache = verifica_posicao_em_cache_associativo_conjunto(memoria_cache, qtd_conjuntos, posicao_memoria)

        # a posição desejada já está na memória
        if inserir_memoria_na_posicao_cache >= 0:
            num_hit += 1
            print('Cache HIT: posiçao de memória {}, posição cache {}'.format(posicao_memoria,
                                                                              inserir_memoria_na_posicao_cache))

          # se for LFU então toda vez que der um HIT será incrementado o contador daquela posição
            """if politica_substituicao == 'LFU':
                contador_lfu[inserir_memoria_na_posicao_cache] += 1
                imprimir_contador_lfu()"""

            # se for LRU então toda vez que der um HIT será incrementado o contador daquela posição
            if politica_substituicao == 'LRU':
                politica_substituicao_LRU_hit(memoria_cache, qtd_conjuntos, posicao_memoria,
                                              inserir_memoria_na_posicao_cache)

        else:
            num_miss += 1
            print('Cache MISS: posiçao de memória {}'.format(posicao_memoria))

            # verifica se existe uma posição vazia na cache, se sim aloca nela a posição de memória
            posicao_vazia = existe_posicao_vazia(memoria_cache, qtd_conjuntos, posicao_memoria)

            if debug:
                print('Posição da cache ainda não utilizada: {}'.format(posicao_vazia))
                print('\nLeitura linha {}, posição de memória {}.'.format(index, posicao_memoria))

            ########
            # se posicao_vazia for < 0 então devemos executar as políticas de substituição
            ########
            if posicao_vazia >= 0:
                memoria_cache[posicao_vazia] = posicao_memoria
                '''
            elif politica_substituicao == 'RANDOM':
                politica_substituicao_RANDOM(memoria_cache, qtd_conjuntos, posicao_memoria)
            elif politica_substituicao == 'FIFO':
                politica_substituicao_FIFO(memoria_cache, qtd_conjuntos, posicao_memoria)
            elif politica_substituicao == 'LFU':
                politica_substituicao_LFU(memoria_cache, qtd_conjuntos, posicao_memoria)'''
            elif politica_substituicao == 'LRU':
                politica_substituicao_LRU_miss(memoria_cache, qtd_conjuntos, posicao_memoria)

        if qtd_conjuntos == 1:
            print_cache_associativo(memoria_cache)
        else:
            print_cache_associativo_conjunto(memoria_cache, qtd_conjuntos)

        if step:
            print('Tecle ENTER para processar o próximo passo:')
            input()

    print('\n\n-----------------')
    print('Resumo Mapeamento {}'.format(nome_mapeamento))
    print('-----------------')
    print('Política de Substituição: {}'.format(politica_substituicao))
    print('-----------------')
    print('Total de memórias acessadas: {}'.format(len(posicoes_memoria_para_acessar)))
    print('Total HIT {}'.format(num_hit))
    print('Total MISS {}'.format(num_miss))
    taxa_cache_hit = (num_hit / len(posicoes_memoria_para_acessar)) * 100
    print('Taxa de Cache HIT {number:.{digits}f}%'.format(number=taxa_cache_hit, digits=2))


def executar_mapeamento_associativo(total_cache, posicoes_memoria_para_acessar, politica_substituicao):
    """O mapeamento associativo é um tipo de mapeamento associativo por conjunto
    ou o número de conjunto é igual a 1
    Arguments:
      total_cache {int} -- tamanho total de palavras da cache
      posicoes_memoria_para_acessar {list} - quais são as posições de memória que devem ser acessadas
      politica_substituicao {str} -- qual será a política de subistituição
    """
    # o número 1 indica que haverá apenas um único conjunto no modo associativo por conjunto
    # que é igual ao modo associativo padrão! :) SHAZAM
    executar_mapeamento_associativo_conjunto(total_cache, 1, posicoes_memoria_para_acessar, politica_substituicao)

def conversao_hexa_inteiro(origem, destino):
    try:
        a = open(origem, 'rt')
    except:
        print("Erro ao abrir o arquivo de endereços!")
    else:
        dado = []
        for linha in a:
            aux = linha
            aux = linha.replace("\n", '')
            integer = (int(aux, 0))

            with open(destino, 'at') as b:
                b.write(f'{integer}\n')

def criar_arquivo (nome):
    try:
        a = open(nome, '+wt')
        a.close()
    except:
        print("Houve um erro na criação do arquivo.")



def verificar_falsos_positivos (memoria_cache, contador_falsos_positivos):

    for posicao, valor in memoria_cache.items():
        for posicao2, valor2 in memoria_cache.items():
            #print(f'Valor for externo: {j}\nValor for interno: {l}.')
            if (valor == valor2) and (posicao != posicao2):
                contador_falsos_positivos += 1
                #print("Houve um falso positivo!\n")
    return contador_falsos_positivos



##########################
# O programa começa aqui!
##########################

# parse dos parâmetros passados no comando
parser = argparse.ArgumentParser(prog='Simulador de Cache')
parser.add_argument('--total_cache', required=True, type=int, help='Número total de posições da memória cache.')
parser.add_argument('--tipo_mapeamento', required=True,
                    help='Tipo do mapeamento desejado. Os valores aceitos para esse parâmetro são: DI / AS / AC.')
parser.add_argument('--politica_substituicao', default='ALL',
                    help='Qual será a política de substituição da cache que será utilizada. Os valores aceitos para esse parâmetro são: RANDOM / FIFO / LRU / LFU.')
parser.add_argument('--qtd_conjuntos', type=int, default=2,
                    help='Quando for escolhido o tipo de mapeamento AC deve-se informar quantos conjuntos devem ser criados dentro da memória cache.')
parser.add_argument('--arquivo_acesso', required=True, default='',
                    help='Nome do arquivo que possui as posições da memória principal que serão acessadas. Para cada linha do arquivo deve-se informar um número inteiro.')
parser.add_argument('--debug', default=0,
                    help='Por padrão vem setado como 0, caso queira exibir as mensagens de debugs basta passar --debug 1.')
parser.add_argument('--step', default=0,
                    help='Solicita a interação do usuário após cada linha processada do arquivo --step 1.')

args = parser.parse_args()

# recuperar toos os parâmetros passados
total_cache = args.total_cache
tipo_mapeamento = args.tipo_mapeamento
arquivo_acesso = args.arquivo_acesso
qtd_conjuntos = args.qtd_conjuntos
politica_substituicao = args.politica_substituicao.upper()
debug = args.debug
step = args.step

if qtd_conjuntos <= 0:
    print('\n\n------------------------------')
    print('ERRO: O número de conjuntos não pode ser 0.')
    print('------------------------------')
    exit()

if arquivo_acesso == '':
    print('\n\n------------------------------')
    print(
        'ERRO: É necesário informar o nome do arquivo que será processado, o parâmetro esperado é --arquivo_acesso seguido do nome do arquivo.')
    print('------------------------------')
    exit()

# lê o arquivo e armazena cada uma das posições de memória que será lida em uma lista
try:
    f = open(arquivo_acesso, "r")
    posicoes_memoria_para_acessar = []
    for posicao_memoria in f:
        posicoes_memoria_para_acessar.append(int(re.sub(r"\r?\n?$", "", posicao_memoria, 1)))
    f.close()
except IOError as identifier:
    print('\n\n------------------------------')
    print('ERRO: Arquivo \'{}\'não encontrado.'.format(arquivo_acesso))
    print('------------------------------')
    exit()

if len(posicoes_memoria_para_acessar) == 0:
    print('\n\n------------------------------')
    print('ERRO: o arquivo {} não possui nenhuma linha com números inteiros.'.format(arquivo_acesso))
    print('------------------------------')
    exit()

print('+====================+')
print('| SIMULADOR DE CACHE |')
print('+====================+')
print('+ Setando parâmetros iniciais da cache+')

if tipo_mapeamento != 'DI':
    if politica_substituicao != 'RANDOM' and politica_substituicao != 'FIFO' and politica_substituicao != 'LRU' and politica_substituicao != 'LFU' and politica_substituicao != 'ALL':
        print('\n\n------------------------------')
        print('ERRO: A política de substituição {} não existe.'.format(politica_substituicao))
        print('------------------------------')
        exit()


if tipo_mapeamento == 'AS':
    if (politica_substituicao == 'ALL'):
        executar_mapeamento_associativo(total_cache, posicoes_memoria_para_acessar, 'RANDOM')
        executar_mapeamento_associativo(total_cache, posicoes_memoria_para_acessar, 'FIFO')
        executar_mapeamento_associativo(total_cache, posicoes_memoria_para_acessar, 'LRU')
        executar_mapeamento_associativo(total_cache, posicoes_memoria_para_acessar, 'LFU')
    else:
        executar_mapeamento_associativo(total_cache, posicoes_memoria_para_acessar, politica_substituicao)

elif tipo_mapeamento == 'AC':
    # o número de conjuntos deve ser um divisor do total da memória
    if total_cache % qtd_conjuntos != 0:
        print('\n\n------------------------------')
        print(
            'ERRO: O número de conjuntos {} deve ser obrigatoriamente um divisor do total de memória cache disponível {}.'.format(
                qtd_conjuntos, total_cache))
        print('------------------------------')
        exit()

    if (politica_substituicao == 'ALL'):
        executar_mapeamento_associativo_conjunto(total_cache, qtd_conjuntos, posicoes_memoria_para_acessar, 'RANDOM')
        executar_mapeamento_associativo_conjunto(total_cache, qtd_conjuntos, posicoes_memoria_para_acessar, 'FIFO')
        executar_mapeamento_associativo_conjunto(total_cache, qtd_conjuntos, posicoes_memoria_para_acessar, 'LRU')
        executar_mapeamento_associativo_conjunto(total_cache, qtd_conjuntos, posicoes_memoria_para_acessar, 'LFU')
    else:
        executar_mapeamento_associativo_conjunto(total_cache, qtd_conjuntos, posicoes_memoria_para_acessar,
                                                 politica_substituicao)
else:
    print('\n\n------------------------------')
    print(
        'ERRO: O tipo de mapeamento \'{}\'não foi encontrado. \nOs valores possíveis para o parâmetro --tipo_mapeamento são: DI / AS / AC'.format(
            tipo_mapeamento))
    print('------------------------------')
    exit()

if debug:
    print('\n')
    print('-' * 80)
    print('Parâmetros da Simulação')
    print('-' * 80)
    print("Arquivo com as posições de memória: {}".format(arquivo_acesso))
    print('Número de posições de memória: {}'.format(len(posicoes_memoria_para_acessar)))
    print('As posições são: {}'.format(posicoes_memoria_para_acessar))
    print('Tamanho total da cache: {}'.format(total_cache))
    print("Tipo Mapeamento: {}".format(tipo_mapeamento))
    if tipo_mapeamento != 'AS':
        print("Quantidade de Conjuntos: {}".format(qtd_conjuntos))
    print("Política de Substituição: {}".format(politica_substituicao))
    print("Debug: {}".format(debug))
    print("Step: {}".format(step))
    print('-' * 80)

criar_arquivo("enderecosInteiros.txt")
arq = "enderecosInteiros.txt"
conversao_hexa_inteiro("enderecosHexadecimal.txt", arq)
#memoria_cache = inicializar_cache(total_cache)
#contador_falsos_positivos = verificar_falsos_positivos(memoria_cache, contador_falsos_positivos)
#print(f'\n\nForam encontrados \033[31m{contador_falsos_positivos}\033[m falsos positivos na implementação.')
