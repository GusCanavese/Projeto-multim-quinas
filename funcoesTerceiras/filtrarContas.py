import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from consultas.select import Buscas 
from componentes import criaLabel, criaBotao
from telas.telaVercontasApagar import telaVercontasApagar
#! PARA A BUSCA COM DATAS FUNCIONAR, 
# É NECESSÁRIO CADASTRAR A CONTAARECEBER 
# E PAGAR COM O FORMATO DATETIME SEM A 
# HORA, SOMENTE COM A DATA
