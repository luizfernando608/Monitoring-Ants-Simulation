from colorama import Fore
p=Fore.GREEN+'oi'
NFormigas = 1
NFCarregando = 2
NFProcurando = 3

NFormigueiro = 5
NCenario = 6
NComida = 7
NCFonte = 8
NCFormigueiro = 9
NCTransito = 10

IDMaxTempo, MaxTempo = 'n',11
MaxTempo = round(MaxTempo,3)
IDMinTempo, MinTempo = 'i',12
MinTempo = round(MinTempo,3)
MediaTempo = round(13,3)
MaxCarregado = round(14,3)
MediaCarregado = round(15,3)

def retorna_linha(valores):
    tamanho=0
    for a in valores:
        tamanho += len(str(a))
    return '|'+str(valores[0])+(73-tamanho)*' '+str(valores[1])+'|'

n='\n'
b='|'

#Limpar Código
import os
os.system('cls') 

#printar
print(Fore.MAGENTA+(75*'-'+n+
                    retorna_linha(['Valores:',''])+n+
                    retorna_linha([' Total Cenários', NCenario])+n+
                    retorna_linha([' Total Formigueiro',NFormigueiro])+n+
                    retorna_linha([' Total Formiga',NFormigas])+n+
                    retorna_linha(['  % Carregando',str(round(NFCarregando/NFormigas*100,2))+'%'])+n+
                    retorna_linha(['  % Procurando',str(round(NFProcurando/NFormigas*100,2))+'%'])+n+
                    retorna_linha([' Total Comida',NComida])+n+
                    retorna_linha(['  % Fonte',str(round(NCFonte/NComida*100,2))+'%'])+n+
                    retorna_linha(['  % Formigueiro',str(round(NCFormigueiro/NComida*100,2))+'%'])+n+
                    retorna_linha(['  % Transito',str(round(NCTransito/NComida*100,2))+'%'])+n+
                    b + 73*'-'+b+n+
                    retorna_linha(['Tempo Cenários:',''])+n+
                    retorna_linha([' Máximo',MaxTempo])+n+
                    retorna_linha(['  Quem',IDMaxTempo])+n+
                    retorna_linha([' Mínimo',MinTempo])+n+
                    retorna_linha(['  Quem',IDMinTempo])+n+
                    retorna_linha([' Média',MediaTempo])+n+
                    retorna_linha(['Comida Carregada por Formiga:',''])+n+
                    retorna_linha([' Máximo',MaxCarregado])+n+
                    retorna_linha([' Média', MediaCarregado])+n+
                    75*'-'))
