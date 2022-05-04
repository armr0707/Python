# Unidade de Controle - ControlUnit
# Interpretador de comandos em assembly
# Autor: Antonio Rogerio Machado Ramos
# E-mails: armr0707@gmail.com; armr0707@hotmail.com; armr0707@icloud.com
# 16/10/2020 - v1.0
# Programa:ControlUnit.py
# Documeto:ControlUnit.pdf
# Código: code.asm

# Registradores
# reg[0]: operando 0
# reg[1]: operando 1
# reg[2]: operando 2
# psw[0]: F(Fim do código) T(início do código)
# psw[1]: F(operador invalido) T(operador valido)
# psw[2]: F(operando invalido) T(operando válido)
# psw[3]: F(normal) T(overflow(>99))
# psw[4]: F(normal) T(underflow(<00))
# psw[5]: F(cmp diferente) T(cmp igual)

# Operadores
# opcode    mnemonico   exemplo     significado
# 01        beg/end     01 01 01    inicio
#                       01 02 02    fim
# 02        add         02 01 02    rg[0]=rg[1]+rg[2]
# 03        sub         03 02 00    rg[0]=rg[2]-rg[0]
# 04        mov         04 01 20    rg[1]=20
#                       04 02 30    rg[2]=30
# 05        mvr         05 00 02    rg[0]=rg[2]
#                       05 02 01    rg[2]=rg[1]
#                       05 01 00    rg[1]=rg[0]
# 06        jmp         06 00 22    salta para linha 22
#                       06 01 22    se psw[5]==T salta para linha 22
#                       06 02 22    se psw[5]==F salta para linha 22
# 07        dsp         07 01 00    display rg[1] e nenhum espaço (max 5)
#                       07 00 03    display rg[0] e 3 espaços (max 5)
#                       07 02 10    display rg[2], nl e 0 lb (max 5)
#                       07 00 12    display rg[0], nl e 2 lb (max 5)
#                       07 10 00    display psw[0] e nenhum espaço
#                       07 11 01    display psw[1] e 1 espaço (max 5)
#                       07 20 00    display pc e nova linha
# 08        cmp         08 01 02    se rg[1]==rg[2] psw[5]=T senão psw[5]=F

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

class ClasContUnit:
 # Atributos
 def __init__(self):
  self.pc=0 # contador de programa
  self.ri=0 # registrador de instrução
  self.rg=[0,0,0] # registradores de dados
  self.psw=[True,True,True,False,False,False] # registrador de status
  self.mem=[] # memória para o código
 # Lê arquivo e guarda na memoria
 def OpeArq(self):
  arq=open("code.asm","r")
  self.mem=(arq.readlines())
  arq.close()
 # Display Begin/End
 def DisB_E(self,Ope1,Ope2):
  if int(Ope1)==1: return ("B_E","Begin","-----")
  else: return ("B_E","-----","End  ")
 # Display Add
 def DisADD(self,Ope1,Ope2):
  return ("ADD","rg["+str(int(Ope1))+"]","rg["+str(int(Ope2))+"]")
 # Display Sub
 def DisSUB(self,Ope1,Ope2):
  return ("SUB","rg["+str(int(Ope1))+"]","rg["+str(int(Ope2))+"]")
 # Display Mov
 def DisMOV(self,Ope1,Ope2):
  return ("MOV","rg["+str(int(Ope1))+"]",str(int(Ope2)).zfill(2)+"   ")
 # Display Mvr
 def DisMVR(self,Ope1,Ope2):
  return ("MVR","rg["+str(int(Ope1))+"]","rg["+str(int(Ope2))+"]")
 # Display Jmp
 def DisJMP(self,Ope1,Ope2):
  if int(Ope1)==0: return ("JMP","-----",str(int(Ope2)).zfill(2)+"   ")
  if int(Ope1)==1: return ("JMP","True ",str(int(Ope2)).zfill(2)+"   ")
  if int(Ope1)==2: return ("JMP","False",str(int(Ope2)).zfill(2)+"   ")
 # Display Dsp
 def DisDSP(self,Ope1,Ope2):
  if int(Ope2)>=0 and int(Ope2)<=5:
   return ("DSP","rg["+str(int(Ope1))+"]",str(int(Ope2))+" esp")
  if int(Ope2)>=10 and int(Ope2)<=15:
   return ("DSP","rg["+str(int(Ope1))+"]",str(int(Ope2)-10)+" lin")
 # Display Cmp
 def DisCMP(self,Ope1,Ope2):
    return ("CMP","rg["+str(int(Ope1))+"]","rg["+str(int(Ope2))+"]")
 # Display do código na memória
 # c: objeto das cores do texto
 def DspCod(self,c):
  print("\nPrograma -----------------------")
  LinCod=0
  for LinCod in range(len(self.mem)):
   if not LinCod%3:
    Oper=str(int(self.mem[LinCod])).zfill(2)+" "
    Ope1=str(int(self.mem[LinCod+1])).zfill(2)+" "
    Ope2=str(int(self.mem[LinCod+2])).zfill(2)+"    "
    LnCd=str(LinCod).zfill(2)+": "
    switcher={
     1: self.DisB_E,
     2: self.DisADD,
     3: self.DisSUB,
     4: self.DisMOV,
     5: self.DisMVR,
     6: self.DisJMP,
     7: self.DisDSP,
     8: self.DisCMP,
    }
    FunDis=switcher.get(int(self.mem[LinCod]))
    MneOper,MneOpe1,MneOpe2=FunDis(Ope1,Ope2)
    print(end=c.EndCol+LnCd+c.VrmCla+Oper+c.AmaCla+Ope1+Ope2)
    print(c.VrmCla+MneOper+c.AmaCla+" "+MneOpe1+" "+MneOpe2)
  print(c.EndCol)
 # Operador que define o inicio  e fim do codigo
 def BegEnd(self):
  self.psw[0]=False; self.psw[2]=False
  self.pc+=1; op1=int(self.mem[self.pc])
  self.pc+=1; op2=int(self.mem[self.pc])
  if op1==1 and op2==1: self.psw[0]=True; self.psw[2]=True
  if op1==2 and op2==2: self.psw[0]=False; self.psw[2]=True
 # Operador que soma duas constantes e guarda em rg[0]
 def Add(self):
  self.psw[2]=False; self.psw[3]=False
  self.pc+=1; op1=int(self.mem[self.pc])
  self.pc+=1; op2=int(self.mem[self.pc])
  if op1>=0 and op1<=2 and op2>=0 and op2<=2:
   self.rg[0]=self.rg[op1]+self.rg[op2]; self.psw[2]=True
   if self.rg[0]>99: self.rg[0]=99; self.psw[3]=True
 # Operador que subtrai duas constrantes e guarda em rg[0]
 def Sub(self):
  self.psw[2]=False; self.psw[4]=False
  self.pc+=1; op1=int(self.mem[self.pc])
  self.pc+=1; op2=int(self.mem[self.pc])
  if op1>=0 and op1<=2 and op2>=0 and op2<=2:
   self.rg[0]=rg[op1]-rg[op2]; self.psw[2]=True
   if self.rg[0]<0: self.rg[0]=0; self.psw[4]=True
 # Operador que move uma constante para rg[0](00), rg[1](01), rg[2](02)
 def Mov(self):
  self.psw[2]=False
  self.pc+=1; op1=int(self.mem[self.pc])
  self.pc+=1; op2=int(self.mem[self.pc])
  if op1>=0 and op1<=2: self.rg[op1]=op2; self.psw[2]=True
 # Operador rg[X](0X)=rg[Y](0Y) para rg[0], rg[1], rg[2]
 def Mvr(self):
  self.psw[2]=False
  self.pc+=1; op1=int(self.mem[self.pc])
  self.pc+=1; op2=int(self.mem[self.pc])
  if op1>=0 and op1<=2 and op2>=0 and op2<=2: rg[op1]=rg[op2]; self.psw[2]=True
 # Operador de salto para endereço - 00(sempre) 01(rg0==0) 02(rg0!=0)
 def Jmp(self):
  self.psw[2]=False
  self.pc+=1; op1=int(self.mem[self.pc])
  self.pc+=1; op2=int(self.mem[self.pc])
  if op2>=0 and op2<len(self.mem) and op1>=0 and op1<=2:
   if op1==0: self.pc=op2
   if op1==1 and self.psw[5]: self.pc=op2-1
   if op1==2 and not self.psw[5]: self.pc=op2-1
   self.psw[2]=True
 # Operador que exibe na tela rg[X](0X) (00)nova linha (0Y) Y espaços (max 10)
 def Dsp(self):
  self.psw[2]=False
  self.pc+=1; op1=int(self.mem[self.pc])
  self.pc+=1; op2=int(self.mem[self.pc])
  if op1>=0 and op1<=2: # registradores
   print(end="rg["+str(op1)+"]:"+str(self.rg[op1]).zfill(2))
   self.psw[2]=True
  if op1>=10 and op1<=15: # psw
   print(end="pwd["+str(op1-10)+"]:"+str(self.psw[op1-10])[0])
   self.psw[2]=True
  if op1==20: # pc
   print(end="pc:"+str(self.pc).zfill(3))
   self.psw[2]=True
  if self.psw[2]==True:
   self.psw[2]=False
   if op2>=0 and op2<=5: print(end=" "*op2); self.psw[2]=True
   if op2>=10 and op2<=15: print("\n"*(op2-10)); self.psw[2]=True
 # Operador de comparação entre registradores F(diferente) T(igual)
 def Cmp(self):
  self.psw[2]=False
  self.pc+=1; op1=int(self.mem[self.pc])
  self.pc+=1; op2=int(self.mem[self.pc])
  if op1>=0 and op1<=2 and op2>=0 and op2<=2:
   if self.rg[op1]==self.rg[op2]: self.psw[5]=True
   else: self.psw[5]=False
   self.psw[2]=True
 # Display dos registradores
 def DspReg(self):
  print("MEM["+str(self.pc)+"]:"+self.mem[self.pc])
 # Trap - alertas sobre operações - status do psw
 def FunTrap(self):
  VarTrap=False
  if not self.psw[1]: print("\n*** Operador inválido ***"); VarTrap=True
  if not self.psw[2]: print("\n*** Operando inválido ***"); VarTrap=True
  return VarTrap
 # Unidade de controle
 def UniCon(self):
  print("Processo -----------------------")
  while self.pc<len(self.mem):
   self.ri=int(self.mem[self.pc])
   if self.FunTrap(): break
   switcher={
    1: self.BegEnd,
    2: self.Add,
    3: self.Sub,
    4: self.Mov,
    5: self.Mvr,
    6: self.Jmp,
    7: self.Dsp,
    8: self.Cmp,
   }
   FunOpe=switcher.get(self.ri,lambda:"Invalido")
   FunOpe()
   self.pc+=1
  print()
   
o=ClasContUnit() # instancia objeto da classe unidade de controle
c=ClasClrs() # instancia objeto da classe de cores do texto
o.OpeArq() # abre arquivo com o código e armazena na memória
o.DspCod(c) # display da memória com o código
o.UniCon() # unidade de controle

   

