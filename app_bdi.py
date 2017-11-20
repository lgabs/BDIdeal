# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 17:07:22 2017

@author: Luan
"""
#import tkinter
#from functools import partial
from tkinter import *
import numpy as np
import scipy as sp

import matplotlib.pylab as mpl
import matplotlib 

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure


import scipy.optimize as opt




#matplotlib.use("TkAgg")
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
#from matplotlib.figure import Figure


class Obra:
    def __init__(self,
                 nome,
                 cd,
                 classe,
                 tipoobra,
                 tipocontrato, 
                 tiporegime,
                 local,
                 tributos, 
                 prazo,
                 regressao):
        self.nome         = nome
        self.cd           = cd
        self.classe       = classe
        self.tipoobra     = tipoobra
        self.tipocontrato = tipocontrato
        self.tiporegime   = tiporegime
        self.local        = local
        self.tributos     = tributos
        self.prazo        = prazo
        self.regressao    = regressao


class Application:
    
    
        
    def close_frame(self, otherFrame):
        #otherFrame.destroy()
        otherFrame.withdraw()


    def objective_p(self, bdi_prop):
        def p_w(bdi_prop):
            p_w = 1/np.sqrt(2*np.pi*self.rmse**2)*sp.integrate.quad(lambda w: np.exp(-(w-self.BDI_medio)**2/(2*self.rmse**2)), bdi_prop, np.inf)[0]
            return float(p_w)
        
        def p_n(bdi_prop):
            p_n = 1/np.sqrt(2*np.pi*self.sigma_n**2)*sp.integrate.quad(lambda w: np.exp(-(w-self.r_o_medio)**2/(2*self.sigma_n**2)), -1*np.inf, bdi_prop)[0]
            return float(p_n)
            
        def p_o():
            if self.perspectiva.get() == "ruim":
                return 0.25
            elif self.perspectiva.get() == "média":
                return 0.50
            elif self.perspectiva.get() == "ótima":
                return 0.75
            else:
                print("erro: perspectiva de mercado errada!")  
                
        p = p_w(bdi_prop)*p_n(bdi_prop) + (1 - p_w(bdi_prop))*p_o()
        return float(p)
    
    def risco(self, bdi_prop):
        r = 1-self.objective_p(bdi_prop)
        return r
    
    def calcularBDI(self):    
        
        self.BDI_medio = 0
        self.rmse = 0
        self.rmse_ro = float(0.02741)
        self.sigma_n = 0
        self.r_o_medio = 0
        self.coeficientes = []
        # REGRESSÃO GERAL
        if self.novaobra.regressao == self.regressoes[0]:
            self.rmse = 0.0363
            coef_lncd = 2.87
            
            coefs_classes =[
                        0,
                        0,
                        -26.77,
                        0,
                        0
                    ]
            coefs_tiposobra = [
                        31.17,
                        0,
                        67.14,
                        0,
                        0,
                        0,
                        0,
                        27.02,
                        19.13,
                        0,
                        0
                    ]
            coefs_contratos=[
                        0,
                        20.57,
                        0,
                        0
                    ]
            coefs_regimes=[
                        0,
                        0,
                        0
                    ]
            coefs_locais=[
                        0,
                        0
                    ]
            coef_tributos = 382
            coef_prazo = 0
            coef_indep = -221.63
            
            self.coeficientes.append(coef_lncd)
            self.coeficientes.append(coefs_classes[self.classes.index(self.novaobra.classe)])
            self.coeficientes.append(coefs_tiposobra[self.tiposobra.index(self.novaobra.tipoobra)])
            self.coeficientes.append(coefs_contratos[self.tiposcontratos.index(self.novaobra.tipocontrato)])
            self.coeficientes.append(coefs_regimes[self.tiposregimes.index(self.novaobra.tiporegime)])
            self.coeficientes.append(coefs_locais[self.locais.index(self.novaobra.local)])
            self.coeficientes.append(coef_tributos)
            self.coeficientes.append(coef_prazo)
            self.coeficientes.append(coef_indep)             
        
        # FILTRO CONTRATO ADMINISTRATIVO
        
        elif self.novaobra.regressao == self.regressoes[1]:
            self.rmse = 0.03473
            coef_lncd = 2.69
            
            coefs_classes =[
                        0,
                        0,
                        0,
                        0,
                        0
                    ]
            coefs_tiposobra = [
                        29.61,
                        32.15,
                        95.57,
                        16.31,
                        25.32,
                        54.38,
                        0,
                        29.38,
                        0,
                        45.51,
                        0
                    ]
            coefs_contratos=[
                        0,
                        0,
                        0,
                        0
                    ]
            coefs_regimes=[
                        0,
                        0,
                        0
                    ]
            coefs_locais=[
                        0,
                        0
                    ]
            coef_tributos = 532.31
            coef_prazo = 0
            coef_indep = -409.12
            
            self.coeficientes.append(coef_lncd)
            self.coeficientes.append(coefs_classes[self.classes.index(self.novaobra.classe)])
            self.coeficientes.append(coefs_tiposobra[self.tiposobra.index(self.novaobra.tipoobra)])
            self.coeficientes.append(coefs_contratos[self.tiposcontratos.index(self.novaobra.tipocontrato)])
            self.coeficientes.append(coefs_regimes[self.tiposregimes.index(self.novaobra.tiporegime)])
            self.coeficientes.append(coefs_locais[self.locais.index(self.novaobra.local)])
            self.coeficientes.append(coef_tributos)
            self.coeficientes.append(coef_prazo)
            self.coeficientes.append(coef_indep)
            
        # FILTRO REGIME EPU
        elif self.novaobra.regressao == self.regressoes[2]:
            self.rmse = 0.03451
            coef_lncd = 2.89
            
            coefs_classes =[
                        0,
                        0,
                        0,
                        0,
                        0
                    ]
            coefs_tiposobra = [
                        30.48,
                        26.68,
                        91.44,
                        0,
                        0,
                        51.33,
                        18.70,
                        25.24,
                        0,
                        0,
                        0
                    ]
            coefs_contratos=[
                        0,
                        45.54,
                        0,
                        0
                    ]
            coefs_regimes=[
                        0,
                        0,
                        0
                    ]
            coefs_locais=[
                        0,
                        0
                    ]
            coef_tributos = 412.75
            coef_prazo = 0
            coef_indep = -280.44
            
            self.coeficientes.append(coef_lncd)
            self.coeficientes.append(coefs_classes[self.classes.index(self.novaobra.classe)])
            self.coeficientes.append(coefs_tiposobra[self.tiposobra.index(self.novaobra.tipoobra)])
            self.coeficientes.append(coefs_contratos[self.tiposcontratos.index(self.novaobra.tipocontrato)])
            self.coeficientes.append(coefs_regimes[self.tiposregimes.index(self.novaobra.tiporegime)])
            self.coeficientes.append(coefs_locais[self.locais.index(self.novaobra.local)])
            self.coeficientes.append(coef_tributos)
            self.coeficientes.append(coef_prazo)
            self.coeficientes.append(coef_indep)
        
        # fim da definição dos coeficientes da regressão!
        #print ('\n'.join("%s" % item for item in self.coeficientes))
        t = 1/(1-float(self.novaobra.tributos)/100)
        self.atributos = [
                    float(np.log(float(self.novaobra.cd))),
                    1,
                    1,
                    1,
                    1,
                    1,
                    t,
                    float(self.novaobra.prazo),
                    1
                ]
        #print ('\n'.join("%s" % item for item in self.atributos))
        self.BDI_medio = float(0.001*sum(np.multiply(self.atributos,self.coeficientes)))
        #print('\nBDI médio: '+str(float(self.BDI_medio*100))+'%')
        
        # r_o_medio
        L = 0
        if self.perspectiva.get() == "ruim":
            L = 0.0616
        elif self.perspectiva.get() == "média":
            L = 0.0740
        elif self.perspectiva.get() == "ótima":
            L = 0.0896
        self.r_o_medio = float((self.BDI_medio - L)/(1 + L))
        
        # sigma_cd
        self.sigma_n = np.sqrt(1/(self.novaobra.cd**2)*(self.novaobra.cd**2*self.rmse_ro**2+(1+self.r_o_medio)**2*(float(self.sigmacd.get())/100*self.novaobra.cd)**2+(float(self.sigmacd.get())/100*self.novaobra.cd)**2*self.rmse_ro**2))
        #print('\n'+'r_o_medio: '+str(self.r_o_medio))
        #print('\n'+'sigma_n: '+str(self.sigma_n))
        # Optimization of BDI_prop = x
        self.BDI_prop = 0
        self.faixax = np.linspace(0, 0.5, 100)
        
        
        self.prob_faixax = []
        for item in self.faixax:
            self.prob_faixax.append(self.objective_p(item))
            
        #mpl.plot(self.faixax, self.prob_faixax)
        
        self.result = opt.minimize_scalar(self.risco, 0.15, method="bounded", bounds=[0, 1])

        self.prob_max = self.objective_p(self.result.x)
        #mpl.plot(self.result.x, self.prob_max,'ro')
        #print('\nBDI ideal: '+str(self.result.x))
        #print('\nProb(BDI ideal): '+str(self.prob_max))
        
        self.page_graph()

        # 1. probability P is a non-convex function of BDI_prop
        # 2. P is smooth
     
    def atribuir_inputs(self):    
        
        self.novaobra = Obra(
                        self.nomeobra.get(),
                        float(self.cd.get()),
                        self.classe_obra.get(),
                        self.tipo_obra.get(),
                        self.tipo_contrato.get(),
                        self.tipo_regime.get(),
                        self.local.get(),
                        float(self.tributos.get()),
                        float(self.prazo.get()),
                        self.reg.get()
                    ) 
        #print(self.novaobra.__dict__, sep=', ')
        #print ('\n'.join("%s: %s" % item for item in vars(self.novaobra).items()))
        #print('\n'+str(self.sigmacd.get()))
    
    def page_graph(self):
        
        #if self.pgraph is None:
            self.pgraph = Tk()
            self.pgraph.title('BDIdeal')
            #self.pgraph.iconbitmap('trucking.ico')
            lb_title   = Label(self.pgraph, text="Resultados")
            lb_title["font"] = ("Arial", "20")
            lb_title.pack(pady = 10, padx= 10)
            
            container = Frame(self.pgraph)
            container.pack(pady = 10, padx= 10)
            textfinal = '\n'.join("%s: %s" % item for item in vars(self.novaobra).items())+'\nPerspectiva de Mercado: '+str(self.perspectiva.get()+'\nDesv. Padrão dos custos diretos (CD): '+ str(self.sigmacd.get())+' % de CD''\n\nBDI ideal: '+str(self.result.x)+'\nP(BDI ideal): '+str(self.prob_max))

            result1 = Label(container, text=textfinal, justify=LEFT)
            result1.pack(side=LEFT)
            
#            result2 = Label(container, text = '\nPerspectiva de Mercado: '+str(self.perspectiva.get()), justify=LEFT)
#            result2.pack(side=LEFT)
#            result3 = Label(container, text = '\nDesv. Padrão dos custos diretos: '+ str(self.sigmacd), justify=LEFT)
#            result3.pack(side=LEFT)
            
            #button1 = Button(self.pgraph, text="Back to Home",
            #                   command=lambda: controller.show_frame(self.jan))
            #button1.pack()
            
            f = Figure(figsize=(3,3), dpi=100)
            a = f.add_subplot(111)
            a.plot(self.faixax, self.prob_faixax)
            a.scatter(self.result.x, self.prob_max)
    
    
            canvas = FigureCanvasTkAgg(f, self.pgraph)
            canvas.show()
            canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)
    
            toolbar = NavigationToolbar2TkAgg(canvas, self.pgraph)
            toolbar.update()
            canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)            

            
        #else:
            # Se já foi, basta colocá-la na frente
            #self.pgraph.lift()
    
    
    
    def page_suporte(self):
        
        self.suporte = Tk()
        #self.suporte.iconbitmap('trucking.ico')
        self.suporte.title('BDIdeal')
        
        container1 = Frame(self.suporte)
        container1.pack(pady = 10, padx= 10)
        container2 = Frame(self.suporte)
        container2.pack(pady = 5, padx= 5)
        container3 = Frame(self.suporte)
        container3.pack(pady = 5, padx= 5)
        
        lb_title = Label(container1, text="Suporte e Metodologia")
        lb_title["font"] = ("Arial", "14")
        lb_title.pack()
        
        lb_suporte = Label(container2, text="Este programa determina o valor de BDI ideal a ser utilizado em orçamentos de obras, com base na maximização \nda probabilidade da licitante não incorrer em perdas financeiras. Essa metodologia foi defendida como\nTrabalho de Graduação do aluno Luan Fernandes, no Instituto Tecnológico de Aeronáutica\nsob o tema 'Abordagem Probabilística do cálculo de BDI de Obras Públicas', no dia 9 de novembro de 2017.\n\nPara ver detalhes, hipóteses e limitações, este trabalho pode ser consultado no site da Biblioteca do ITA:\n\
                                            <http://www.sophia.bibl.ita.br/biblioteca/index.html>.", justify=LEFT)
        lb_suporte["font"] = self.fontepadrao
        #lb_suport["width"] = 7
        lb_suporte.pack()
        
        lb_email = Label(container3, text="Para dúvidas e sugestões, o autor pode ser consultado pelo email luangabriel70@gmail.com.\nÚltima atualização: 20/11/2017\n\nIcon made by Freepik from www.flaticon.com ")
        lb_email["font"] = self.fontepadrao
        lb_email.pack()
    
        
    
    def page_inputs(self): # JANELA DE VALORES DE ENTRADA

        # Verifica se já foi criada
        if self.jan is None:
            self.jan = Tk()
            #self.jan.iconbitmap('trucking.ico')
            self.jan.title('BDIdeal')
            self.jan.protocol("WM_DELETE_WINDOW", self.fecha_pageinputs)
            self.lb_titleinput  = Label(self.jan, text='Insira dados de entrada da obra nos campos:')
            self.lb_nomeobra    = Label(self.jan, text="Nome: ")
            self.lb_cd          = Label(self.jan, text="Custo Direto (R$): ")
            self.lb_cnae        = Label(self.jan, text="Classificação CNAE 2.0: ")
            self.lb_tipoobra    = Label(self.jan, text="Tipo da Obra (CNAE 2.0): ")
            self.lb_contrato    = Label(self.jan, text="Tipo de Contrato: ")
            self.lb_regime      = Label(self.jan, text="Regime de Contrato: ")
            self.lb_local       = Label(self.jan, text="Localidade: ")
            self.lb_tributos    = Label(self.jan, text="Tributos efetivos (%)\n(com deduções aplicáveis): ")
            self.lb_prazo       = Label(self.jan, text="Prazo da obra (dias): ")
            self.lb_perspectiva       = Label(self.jan, text="Perspectiva de Mercado\n(ruim/média/ótima):")
            self.lb_sigmacd     = Label(self.jan, text="Desvio padrão dos custos diretos (CD)\ncomo % de CD (default: 5.00%)")
            self.lb_reg         = Label(self.jan, text="Escolha a regressão desejada: ")
            
            self.lb_titleinput.grid(row = 0, column = 0, columnspan=2, sticky=W+E)
            self.lb_nomeobra.grid(row = 1, column = 0)
            self.lb_cd.grid(row = 2 ,column = 0)
            self.lb_cnae.grid(row = 3 ,column = 0)
            self.lb_tipoobra.grid(row = 4 ,column = 0)
            self.lb_contrato.grid(row = 5 ,column = 0)
            self.lb_regime.grid(row =  6,column = 0)
            self.lb_local.grid(row =  7,column = 0)
            self.lb_tributos.grid(row = 8 ,column = 0)
            self.lb_prazo.grid(row =  9,column = 0)
            self.lb_reg.grid(row = 10, column = 0)
            self.lb_perspectiva.grid(row = 11, column=0)
            self.lb_sigmacd.grid(row = 12, column=0)
            
            self.classes = [
                     "Construção De Edifícios",
                     "Construção De Redes De Abastecimento De Água, Coleta De Esgoto E Construções Correlatas",
                     "Construção De Rodovias E Ferrovias",
                     "Obras De Geração E Distribuição De Energia",
                     "Obras Portuárias, Marítimas E Fluviais"
                   ]
            self.tiposobra = [
                     "Obras Aeroportuárias - Pátio E Pista",
                     "Obras Aeroportuárias - Terminais",
                     "Obras De Derrocamento E Dragagem",
                     "Obras De Edificação - Construção",
                     "Obras De Edificação - Reforma",
                     "Obras De Linha De Transmissão/Distribuição De Energia",
                     "Obras De Saneamento Ambiental",
                     "Obras Ferroviárias",
                     "Obras Hídricas - Irrigação, Barragens E Canais",
                     "Obras Portuárias - Estruturas",
                     "Obras Rodoviárias"
                    ]
            self.tiposcontratos = [
                    "Contrato Administrativo",
                    "Contrato de Repasse",
                    "Convênio",
                    "Termo de Compromisso "
                    ]
            self.tiposregimes = [
                     "Empreitada Integral (EI)",
                     "Empreitada por Preço Global (EPG)",
                     "Empreitada por Preço Unitário (EPU) "
                    ]
            self.locais = [  
                    "Interior",
                    "Centros Urbanos"
                    ]
            self.regressoes = [
                    "Geral                           (R2 aj.= 0.2646, RMSE = 0.0363)",
                    "Filtro: Contrato Administrativo (R2 aj.= 0.3326, RMSE = 0.03473)",
                    "Filtro: Regime por EPU          (R2 aj.= 0.3694, RMSE = 0.03451)"
                    ]
         
            self.nomeobra = Entry(self.jan)
            self.nomeobra.insert(0, 'Obra 1')
            self.nomeobra["width"] = 30
            self.nomeobra["font"] = self.fontepadrao
            self.nomeobra.grid(row = 1, column = 1, sticky = W)

            self.cd = Entry(self.jan)
            self.cd.insert(0, '1000000.00')
            self.cd["width"] = 30
            self.cd["font"] = self.fontepadrao
            self.cd.grid(row = 2, column = 1, sticky = W)

            self.classe_obra = StringVar(self.jan)
            self.classe_obra.set(self.classes[0])  # default
            lista_classe = OptionMenu(self.jan, self.classe_obra, *self.classes)           
            lista_classe.grid(row = 3, column = 1, sticky = W)

            self.tipo_obra = StringVar(self.jan)
            self.tipo_obra.set(self.tiposobra[0])  # default
            lista_tipoobra = OptionMenu(self.jan, self.tipo_obra, *self.tiposobra) 
            lista_tipoobra.grid(row = 4, column = 1, sticky = W)

            self.tipo_contrato = StringVar(self.jan)
            self.tipo_contrato.set(self.tiposcontratos[0])  # default
            lista_tipocontrato = OptionMenu(self.jan, self.tipo_contrato, *self.tiposcontratos) 
            lista_tipocontrato.grid(row = 5, column = 1, sticky = W)

            self.tipo_regime = StringVar(self.jan)
            self.tipo_regime.set(self.tiposregimes[0])  # default
            lista_tiporegime = OptionMenu(self.jan, self.tipo_regime, *self.tiposregimes) 
            lista_tiporegime.grid(row = 6, column = 1, sticky = W)

            self.local = StringVar(self.jan)
            self.local.set(self.locais[0])  # default
            lista_local = OptionMenu(self.jan, self.local, *self.locais) 
            lista_local.grid(row = 7, column = 1, sticky = W)

            self.tributos = Entry(self.jan)
            self.tributos.insert(0, '10.00')
            self.tributos["width"] = 30
            self.tributos["font"] = self.fontepadrao
            self.tributos.grid(row = 8, column = 1, sticky = W)

            self.prazo = Entry(self.jan)
            self.prazo.insert(0, '360')
            self.prazo["width"] = 30
            self.prazo["font"] = self.fontepadrao
            self.prazo.grid(row = 9, column = 1, sticky = W)
            
            self.reg = StringVar(self.jan)
            self.reg.set(self.regressoes[0])
            lista_reg = OptionMenu(self.jan, self.reg, *self.regressoes)
            lista_reg.grid(row = 10, column = 1, sticky = W)
            
            self.perspectiva = Entry(self.jan)
            self.perspectiva.insert(0, 'ruim')
            self.perspectiva["width"] = 30
            self.perspectiva["font"] = self.fontepadrao
            self.perspectiva.grid(row = 11, column=1)
            
            self.sigmacd = Entry(self.jan)
            self.sigmacd.insert(0, '5.00')
            self.sigmacd["width"] = 30
            self.sigmacd["font"] = self.fontepadrao
            self.sigmacd.grid(row = 12, column=1)


            # BOTÕES
            
            container1_input = Frame(self.jan)
            container1_input["pady"] = 5
            container1_input.grid(row = 13, column = 0, columnspan = 2)                            
            botao_confirma = Button(container1_input)
            botao_confirma["text"] = "Atribuir valores"
            botao_confirma["width"] = 20
            botao_confirma["command"] = self.atribuir_inputs
            botao_confirma.pack()
            
            botao_voltar = Button(self.jan)
            botao_voltar["text"] = "Voltar"
            botao_voltar["pady"] = 5
            botao_voltar["command"] = lambda: self.close_frame(self.jan)
            #botao_voltar.grid(row = 11, column = 1)
        
            # Calcular BDI ideal
            container2_input = Frame(self.jan)
            container2_input["pady"] = 5
            container2_input.grid(row = 14, column = 0, columnspan = 2)                            
            calculoBDI = Button(container2_input)
            calculoBDI["text"] = "Calcular BDI Ideal"
            calculoBDI["font"] = self.fontepadrao
            calculoBDI["width"] = 20          
            #calculoBDI["command"] = lambda: controller.show_frame()
            calculoBDI["command"] = self.calcularBDI
            calculoBDI.pack()
            
            #self.jan.geometry('300x200')
        else:
            # Se já foi, basta colocá-la na frente
            self.jan.lift()
      


    def fecha_pageinputs(self):
        # Seta de novo em None para recriar quando abrir
        self.jan.destroy()
        self.jan = None
    
    def __init__(self, master=None):
        self.jan = None
        self.fontepadrao = ("Arial", "10")
        self.primeiroContainer = Frame(master)
        self.primeiroContainer["pady"] = 30
        self.primeiroContainer.pack()
       
        self.segundoContainer = Frame(master) 
        self.segundoContainer["padx"] = 20
        self.segundoContainer.pack()
        
        self.terceiroContainer = Frame(master) 
        self.terceiroContainer["padx"] = 20
        self.terceiroContainer["pady"] = 10
        self.terceiroContainer.pack()
        
        self.titulo = Label(self.primeiroContainer, text = "Bem vindo ao Programa de BDI ideal\nversão 1.0")
        self.titulo["font"] = ("Arial", "10", "bold")
        self.titulo.pack()
        
        # Cadastro da Obra
        self.cadastroButton = Button(self.segundoContainer)
        self.cadastroButton["text"]  = "Calcular BDI ideal"
        self.cadastroButton["font"]  = self.fontepadrao
        self.cadastroButton["width"] = 20
        self.cadastroButton["command"] = self.page_inputs
        self.cadastroButton.pack()
        
        self.suporteButton = Button(self.terceiroContainer)
        self.suporteButton["text"] = "Suporte e Metodologia"
        self.suporteButton["font"] = self.fontepadrao
        self.suporteButton["width"] = 20
        self.suporteButton["command"] = self.page_suporte
        self.suporteButton.pack()                   
   
                       
root = Tk()
root.title('BDIdeal')
#root.iconbitmap('trucking.ico')
Application(root)

#root.geometry()
root.mainloop()