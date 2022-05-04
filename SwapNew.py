# Gerenciador de memória
# Páginas: 10 lógicas, 5 físicas e 5 virtuais
# Emprega swap in/out
# Autor: Antonio Rogerio Machado Ramos
# E-mails: armr0707@gmail.com; armr0707@hotmail.com; armr0707@icloud.com
# 04/10/2020 - v1.0
# Programa:SwapNew.py
# Documeto:SwapNew.pdf

from random import randint # Importar randint de random

class ClasClrs:
    VrmEsc= "\033[31m"
    VrmCla = "\033[91m"
    VrdEsc = "\033[32m"
    VrdCla = "\033[92m"
    AmaEsc = "\033[33m"
    AmaCla = "\033[93m"
    AzuEsc = "\033[34m"
    AzuCla = "\033[94m"
    MagEsc = "\033[35m"
    MagCla = "\033[95m"
    CiaEsc = "\033[36m"
    CiaCla = "\033[96m"
    CinEsc = "\033[37m"
    CinCla = "\033[90m"
    Header = "\033[95m"
    OkBlue = "\033[94m"
    OkGren = "\033[92m"
    Warnin = "\033[93m"
    Failur = "\033[91m"
    EndCol = "\033[0m"
    BolCol = "\033[1m"
    UndCol = "\033[4m"

class ClasPlog: # Atributos da página lógica  (pl)
 def __init__(self):
  self.PlBitExe=False # Executando (F)não (T)sim
  self.PlBitInv=True # Tipo da página correspondente (F)física (T)virtual
  self.PlEndPag=0 # Endereço da página correspondente

class ClasPfis: # Atributos da página física (pf)
 def __init__(self):
  self.PfBitRef=False # Página usada (F)não (T)sim
  self.PfBitDir=False # Página alterada (F)não (T)sim
  self.PfEndPlg=-1 # Endereço da página lógica correspondente (não canonico)
  self.PfDatPag="" # Dados da página
  
class ClasPvir: # Atributos da página virtual (pv)
 def __init__(self):
  self.PvDatPag="" # Dados da página

def FunCriTab(): # Cria tabelas pl, pf, pv e cores
 OPl=[0]*10 # lista para 10 páginas pl
 OPf=[0]*5 # lista para 5 páginas pf
 OPv=[0]*10 # lista para 10 páginas pv
 OPp=[0]*5 # lista para 5 páginas pp
 for ConPag in range(5): # Instancia objetos - 10 pl e 10 pv
  OPl[ConPag]=ClasPlog() # Instancia objeto pl [0-4]
  OPl[ConPag].PlEndPag=ConPag # Atribui endereço pv correspondente [0-4]
  OPl[ConPag].PlBitInv=True # True porque o correspondente é pv
  OPl[ConPag+5]=ClasPlog() # Instancia objeto pl [5-9]
  OPl[ConPag+5].PlEndPag=ConPag+5 # Atribui endereço pv correspondente [5-9]
  OPl[ConPag+5].PlBitInv=True # True porque o correspondente é pv
  OPf[ConPag]=ClasPfis() # Instancia objeto pf [0-4]
  OPf[ConPag].PfDatPag="....." # Preenche com dados
  OPv[ConPag]=ClasPvir() # Instancia objeto pv [0-4]
  OPv[ConPag].PvDatPag=chr(randint(97,122))*5 # Preenche com dados
  OPv[ConPag+5]=ClasPvir() # Instancia objeto pv [5-9]
  OPv[ConPag+5].PvDatPag=chr(randint(97,122))*5 # Preenche com dados
 OCl=ClasClrs() # Instancia objeto cl (cores)
 return (OPl,OPf,OPv,OCl)

def FunExiPag(OPl,OPf,OPv,OCl): # Exibe as páginas tabuladas e coloridas
 print(" Lógicas -----------    Física -------------------    Virtuais -")
 print(" End  Status     EPR    End  RBit  DBit  EPL Dados    End  Dados")
 for ConPag in range(10): # exibe atributos das paginas lógicas, físicas e virtuais
  print("["+OCl.VrmCla+str(ConPag).zfill(3)+OCl.CiaCla,end="  ") # páginas lógicas
  if OPl[ConPag].PlBitExe: print(end="Executando ")
  else: print(end="Não execut ")
  if OPl[ConPag].PlBitInv: print(OCl.VrdCla+str(OPl[ConPag].PlEndPag).zfill(3)+OCl.EndCol,end="]  ")
  else: print(OCl.AmaCla+str(OPl[ConPag].PlEndPag).zfill(3)+OCl.EndCol,end="]  ")
  if ConPag<5: # se o numero de paginas for no intervalo [0-4]
   print("["+OCl.AmaCla+str(ConPag).zfill(3),end="  ") # páginas físicas e virtuais
   print(OCl.MagCla+str(OPf[ConPag].PfBitRef),end=" ")
   if (OPf[ConPag].PfBitRef): print(end=" ")
   print(str(OPf[ConPag].PfBitDir),end=" ")
   if (OPf[ConPag].PfBitDir): print(end=" ")
   print(OCl.VrmCla+str(OPf[ConPag].PfEndPlg).zfill(3),end=" ")
   print(OCl.AzuCla+OPf[ConPag].PfDatPag,end=" ")
   print(OCl.EndCol,end="]  ")
  print(end=OCl.CinCla)
  if ConPag==5: print(end="                               ")
  if ConPag==6: print(end=" RBit: pf usada                ")
  if ConPag==7: print(end=" DBit: pf alterada             ")
  if ConPag==8: print(end=" EPR : endereço pag referencia ")
  if ConPag==9: print(end=" EPL : endereço pag lógica     ")
  print("["+OCl.VrdCla+str(ConPag).zfill(3),end="  ")
  print(OCl.AzuCla+OPv[ConPag].PvDatPag+OCl.EndCol,end="]")
  print(OCl.EndCol)
 
def FunExePag(OPl): # define aleatoriamente página lógica executando
 for ConPag in range(10): # passa pelas pl e seta todas como não executando
  OPl[ConPag].PlBitExe=False
 PagLog=randint(0,9) # endereço da página logica executando
 OPl[PagLog].PlBitExe=True # seta bit para executando
 return PagLog # retorna endereço da pl executando
 
def FunVerPlg(OPl,OPf,PagLog): # verifica se pl tem pf - se tiver T(executando), senão F(page fault)
 PagFlt=False # default - pl tem pf
 if (not OPl[PagLog].PlBitInv): # se pl tem pf
  OPf[OPl[PagLog].PlEndPag].PfBitRef=True # seta pf como usada
 else: PagFlt=True # pl não tem pf - page fault
 return PagFlt

def FunEscFis(OPl,OPf,OPv,PagLog): # escolhe pf que tem end pl -1 (não vinculada com pl)
 PagFlt=True # default - não tem pf livre
 for ConPag in range(5): # passa por todas as pf
  if OPf[ConPag].PfEndPlg==-1: # se tem pf com endereço pl -1
   OPf[ConPag].PfBitRef=True # seta pf como usada
   OPf[ConPag].PfEndPlg=PagLog # seta end pl e pv (mesmo)
   OPf[ConPag].PfDatPag=OPv[PagLog].PvDatPag # copia dados de pv para pf
   OPl[PagLog].PlBitInv=False # seta pl com pf
   OPl[PagLog].PlEndPag=ConPag # seta end pf na pl
   PagFlt=False # swap realizado
   break
 return PagFlt
 
def FunSecCha(OPl,OPf): # escolhe pf vitima e segunda chance pras outras
 PagVit=-1 # seta pagvit com endereço inválido
 for ConPag in range(5): # passa por todas as pf
  if (not OPf[ConPag].PfBitRef): PagVit=ConPag; break # pega primeira pagvit e sai do loop
 if PagVit<0:
  for ConPag in range(5): # passa por todas as pf
   if (not OPl[OPf[ConPag].PfEndPlg].PlBitExe): # se pf não executando
    OPf[ConPag].PfBitRef=False # seta pf como não usada
    if PagVit<0: PagVit=ConPag # pega a primeira não usada
 return PagVit # retorna end pf pagina vitima

def FunSwaPag(OPl,OPf,OPv,PagLog,PagVit): # rotina de swap para pl sem pf
 OPl[OPf[PagVit].PfEndPlg].PlEndPag=OPf[PagVit].PfEndPlg # pl (da pagvit) recebe o endpag do pv (mesmo end)
 OPl[OPf[PagVit].PfEndPlg].PlBitInv=True # setar pl (da pagvit) não tem mais pf
 OPl[OPf[PagVit].PfEndPlg].PlBitExe=False # setar pl (da pagvit) não está executando
 if OPf[PagVit].PfBitDir: # se pf vitima foi alterada
  OPv[OPf[PagVit].PfEndPlg].PvDatPag=OPf[PagVit].PfDatPag # pv relacionada recebe dados de pf vitima
 OPf[PagVit].PfBitRef=True # setar pf como usada
 OPf[PagVit].PfBitDir=False # setar pf como não alterada
 OPf[PagVit].PfEndPlg=PagLog # vincular pf com pl (executando)
 OPf[PagVit].PfDatPag=OPv[PagLog].PvDatPag # pf recebe os dados de pv (pl executando)
 OPl[PagLog].PlBitInv=False # setar pl (executando) para página física (pf)
 OPl[PagLog].PlEndPag=PagVit # seta pl endpag para pagina física (pf) (página vítima)
 
def FunDirBit(OPl,OPf): # altera os dados na pf executando (50% chance)
 for ConPag in range(10):
  if OPl[ConPag].PlBitExe and (not OPf[OPl[ConPag].PlEndPag].PfBitDir):
   OPf[OPl[ConPag].PlEndPag].PfBitRef=True
   if (not randint(0,1)):
    OPf[OPl[ConPag].PlEndPag].PfDatPag=chr(randint(97,122))*5 # altera dados da pf
    OPf[OPl[ConPag].PlEndPag].PfBitDir=True

def FunTesPro(): # Função para testar o processo
 print("="*66)
 print("Gerenciador de memória v1.0")
 print("Páginas: 10 lógicas, 5 físicas e 5 virtuais")
 print("Emprega swap in/out")
 print("-"*66)
 Continua=True; Ite=0
 OPl,OPf,OPv,OCl=FunCriTab()
 while Continua: # repete rotinas
  # rotinas de testes
  Ite+=1
  PagLog=FunExePag(OPl)
  PagFlt=FunVerPlg(OPl,OPv,PagLog)
  if PagFlt: PagFlt=FunEscFis(OPl,OPf,OPv,PagLog)
  if PagFlt: PagVit=FunSecCha(OPl,OPf); FunSwaPag(OPl,OPf,OPv,PagLog,PagVit)
  FunDirBit(OPl,OPf)
  FunExiPag(OPl,OPf,OPv,OCl)
  # rotina para continuar ou abortar
  tecla="*"
  while tecla.upper()!="F" and tecla.upper()!="":
   tecla=input(" ITERAÇÃO["+str(Ite).zfill(4)+"]         ENTER:PRÓXIMA ITERAÇÃO    F+ENTER:FIM   ")
  if tecla=="": Continua=True # se ENTER digitado, retorna falso
  else: Continua=False # se tecla digitado, retorna verdadeiro
 print("="*66)
  
FunTesPro()

