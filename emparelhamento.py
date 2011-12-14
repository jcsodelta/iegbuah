# -*- coding: utf-8 -*-
import networkx
import pydot

#O pydot esta sendo utilizado para manipular o subgrafo representado em DOT
#O networkx esta sendo usado para manipulacao geral sobre o grafo



class Hungaro:

	def texto(self):
		return "Algoritmo Hungaro"
	
	def lerGrafoDoArquivoMatrizAdjacente(self, caminho):
		print "Lendo matriz adjacente: "+caminho
		arquivo = open(caminho, 'r')
		self.grafo = pydot.Dot('Grafo', graph_type='graph' )
		#obter numero de no em primeira linha
		lista = arquivo.readline().split('\t')
		no_count = 0
		for coluna in range(0,len(lista)):
			self.grafo.add_node(pydot.Node(str(coluna)))
			if lista[coluna]=="1":
				self.grafo.add_edge(pydot.Edge(str(coluna), "1"))
				print ' add edge:'+str(coluna)+" - 1"
				no_count+=1
		print "numero no: "+str(no_count)
		#loop de toda linha, 2 ate no_count inclusive
		for i in range(2, no_count+1):
			linha = arquivo.readline()
			if linha != "":
				lista = linha.split('\t')
				j = 1
				for cell in lista:
					if cell == '1' and j>i:
						self.grafo.add_edge( pydot.Edge(str(j+i), str(i)) )
						print 'add Edge: ' + str(j+i) + ' - ' + str(i)
					j+=1
			else:
				print "Erro de leitura na Matriz de adjacencia"
				break
		self.criarParticao()
		return
	
	def lerGrafoDoArquivoDot(self, caminho):
		#self.grafo = networkx.read_dot(caminho) # network não lê subgrafos
		self.grafo = pydot.graph_from_dot_file(caminho)
		return
	
	def geraImagemGrafoInicial(self):
		self.grafo.write_gif("grafo.gif")
		return
	
	def aplicaHungaro(self): # grafo, X, emparelhamento
		
		self.grafoEmp = self.grafo
		
		# busca subgrafos
		lista = self.grafoEmp.get_subgraph_list()
		for i in lista:
			if i.get_name() == "X":
				sgX = i
			elif i.get_name() == "Y":
				sgY = i
			elif i.get_name() == "M":
				sgM = i
		
		arvore = networkx.Graph()
		pesos = {}
		sgMx = networkx.from_pydot(sgM)
		sgMx = sgMx.to_undirected()
		sgXx = networkx.from_pydot(sgX)
		sgXx = sgXx.to_undirected()
		grafoEmpx = networkx.from_pydot(self.grafoEmp)
		grafoEmpx = grafoEmpx.to_undirected()
		
		S = []
		T = []
		
		# segue os passo do algoritmo
		passo = 1
		
		while passo != 0:
			#
			# PASSO O1
			#
			if passo == 1:
				print "\tPasso 1"
				
				if sgMx.edges().__len__() == 0 :
					print "O conjunto M está vazio"
					e = self.grafoEmp.get_edges()[0]
					sgMx.add_edge( e.get_source(), e.get_destination() )
					print "A aresta " + self.imprimeVertice(e) + " foi adicionada a M"
					
				
				self.imprimeEstado(sgX, sgY, sgMx, arvore )
				raw_input("1")
				
				passo = 2
				
			#
			# PASSO O2
			#
			elif passo == 2:
				print "\tPasso 2"
				
				# existe algum vértice não saturado?
				
				i = 0
				encontrouNaoSaturado = False
				S = []
				T = []
				while not encontrouNaoSaturado and i < sgX.get_nodes().__len__():
					print "loop"
					v = sgX.get_nodes()[i]
					if not sgMx.has_node( v.get_name() ):
						print "Vértice não-saturado encontrado em X: "+ v.get_name()
						encontrouNaoSaturado = True
						S.append(v.get_name())
					i +=1
				
				if not encontrouNaoSaturado:
					print "Todos os vértices de X já estão saturados"
					passo = 0
				else:
					arvore = networkx.Graph()
					arvore.add_node( v.get_name() )
					pesos[v.get_name()] = 0
					
					passo = 3
					
				self.imprimeEstado(sgX, sgY, sgMx, arvore )
				raw_input("2")
				
			#
			# PASSO O3
			#
			elif passo == 3:
				print "\tPasso 3"
				
				# verifica se a vizinhança tem o mesmo tamanho de T
				


				T = arvore.nodes()
				
				sgXx = networkx.from_pydot(sgX)
				#print "arvore noses: "
				#print arvore.nodes()
				#print "T:"
				#maximo = T.__len__()
				#print maximo
				#print T
				i = T.__len__() - 1;
				while i >= 0:
					#print "i"
					print "T[i] Vale: "
					print T[i]
					#print "avaliando " + T[i]
					if sgXx.has_node( T[i] ):
						#print "removeu" + T[i]
						T.remove(T[i])
					i -= 1
				
				print "T:"
				print T
				
				#T.sort()
				#print "T = " + T.__str__()
				
				#S = arvore.nodes()
				#for n in T:
					#if not sgXx.has_node( n ):
						#S.remove(n)
				
				S.sort()
				print "S = " + S.__str__()
				
				NS = []
				
				for n in S:
					lista = grafoEmpx.neighbors(n)
					for n2 in lista:
						if n2 not in NS:
							NS.append(n2)
							
				NS.sort()
				print "NS = " + NS.__str__()
				
				if NS == T:
					print "PROBLEMA: O algoritmo não satisfaz o Teorema do Casamento"
					passo = 0
				else:
					
					# busca um y em NS que não está em T
					candidatos = []
					for n in NS:
						if n not in T:
							candidatos.append(n)
					
					y = candidatos[0];
					print "Escolheu "+ y +" entre NS - T: "+ candidatos.__str__()
					
					passo = 4
				
				self.imprimeEstado(sgX, sgY, sgMx, arvore )
				raw_input("3")
				
			#
			# PASSO O4
			#
			elif passo == 4:
				print "\tPasso 4"
				
				# verifica se y é M-saturado
				
				if sgMx.has_node( y ):
					print y + " é M-saturado"
					
					# adiciona novas arestas a arvore
					
					# busca um no na arvore que seja vizinho a y
					lista = arvore.nodes()
					i = 0
					encontrou = False
					while not encontrou and i < lista.__len__():
						if grafoEmpx.has_edge(y, lista[i]):
							arvore.add_edge( y, lista[i] )
							pesos[y] = pesos[lista[i]] + 1
						i +=1
					
					#vizin = sgMx.neighbors( y )
					#for n in sgMx.predecessors( y ):
					#	if not vizin.__contains__(n):
					#		vizin.append(n)
					#z = vizin[0]
					z = sgMx.neighbors( y )[0]
						
					arvore.add_edge( y, z )
					pesos[z] = pesos[y] + 1
					
					T.append(y)
					S.append(z)
					
					passo = 3
					
				else:
					print y + " é M-não-saturado"
					
					atual = y
					print "Atual = "+atual
					vizin = grafoEmpx.neighbors( atual )
					print "Vizinhos de y"
					print vizin
					
					encontrado = False
					i = 0
					while not encontrado and i < vizin.__len__():
						if vizin[i] in arvore.nodes():
							encontrado = True
							prox = vizin[i]
						i += 1
						
					print "Proximo = " + prox
					
					
					if sgMx.has_edge( y, prox ):
						print "Removendo de M: ("+ y +", "+prox+")"
						sgMx.remove_edge( y, prox)
					else:
						print "Adicionando a M: ("+ y +", "+prox+")"
						sgMx.add_edge( y, prox)
					
					anterior = y
					atual = prox
					print "Atual = "+atual
					print "Prox = "+prox
					print "Anterior = "+anterior
					
					#networkx.to_pydot(arvore).write_gif("arvore.gif")
					
					while atual != v.get_name():
						vizin = arvore.neighbors( atual )
						print vizin
						for n in vizin:
							if pesos[n] < pesos[atual]:
								prox = n
						#if vizin[0] != anterior:
							#prox = vizin[0]
						#else:
							#prox = vizin[1]
						
						if sgMx.has_edge( atual, prox ):
							print "Removendo de M: ("+ atual +", "+prox+")"
							sgMx.remove_edge( atual, prox)
						else:
							print "Adicionando a M: ("+ atual +", "+prox+")"
							sgMx.add_edge( atual, prox)
						
						anterior = atual
						atual = prox
						print "Atual = "+atual
						print "Prox = "+prox
						print "Anterior = "+anterior
						#networkx.to_pydot(arvore).write_gif("arvore.gif")
					
					passo = 2
					
				print "Emparelhamento:"
				print sgMx.nodes()
				print sgMx.edges()
				
				print "Arvore:"
				print arvore.nodes()
				print arvore.edges()
				
				self.imprimeEstado(sgX, sgY, sgMx, arvore )
				raw_input("4")
				
		
		# formata arestas de sgXx em grafoEmp
		
		lista = self.grafoEmp.get_edges()
		for e in lista:
			if sgMx.has_edge( e.get_source(), e.get_destination() ):
				e.set_style("dotted")
		
		#sgM = novoM
		
		return
		
	def imprimeVertice(self, e):
		return "("+e.get_source()+", "+e.get_destination()+")"
	
	def imprimeEstado(self, sgX, sgY, sgMx, arvore ):
		sgXx = networkx.from_pydot(sgX)
		print "X: "
		print sgXx.nodes()
		
		sgYx = networkx.from_pydot(sgY)
		print "Y: "
		print sgYx.nodes()
		
		print "M: "
		print sgMx.nodes()
		print sgMx.edges()
		
		print "Arvore: "
		print arvore.nodes()
		print arvore.edges()
		
		return
	
	def geraImagemGrafoEmparelhado(self):
		
		
		
		self.grafoEmp.write_gif('grafoEmparelhado.gif')
		
		return
		
	#recebe listas de no e aresta
	def lerGrafoBipartidoDaLista(self, particaoX, particaoY, arestas):
		self.grafo = pydot.Dot(graph_type='graph')
		subX = pydot.subgraph('X')
		subY = pydot.subgraph('Y')
		for no in particaoX:
			subX.add_node(str(no))
		for no in particaoY:
			subY.add_node(str(no))
		self.grafo.add_subgraph(subX)
		self.grafo.add_subgraph(subY)
		for aresta in arestas:
			self.grafo.add_edge(str(aresta))
		return self.grafo
		
	
	def exportarParaMatrizAdj(self, grafoDot, nome):
		print('criando arquivo com matriz de adjacencia: '+nome+'.txt')
		arquivo = open(str(nome)+'.txt', 'w')
		grafox = networkx.from_pydot(grafoDot)
		grafox = grafox.to_undirected()
		listaNo = grafox.nodes()
		for i in range(0, len(listaNo)):
			vizinhos = grafox.neighbors(listaNo[i])
			linha = ""
			for j in range(0, len(listaNo)):
				if listaNo[j] in vizinhos:
					linha+="1\t"
					print listaNo[i]+"("+str(i)+") -- " + listaNo[j]+"("+str(j)+")"
				else:
					linha+="0\t"
			linha = linha[0:-1]+"\n"
			arquivo.write(linha)

	def criarParticao(self):
		listaSubg = self.grafo.get_subgraph_list()
		temM=False
		for subg in listaSubg:
			if subg.get_name=='X' or subg.get_name=='Y':
				return
			if subg.get_name=='M':
				temM = True
		grafox = networkx.from_pydot(self.grafo)
		listaNo = grafox.nodes()
		X=[listaNo[0]]
		Y=[]
		for i in range(0,len(listaNo)):
			vizinhos = grafox.neighbors(listaNo[i])
			for j in vizinhos:
				if i in X and i not in Y:
					Y.append(j)
				elif i not in X:
					X.append(j)
		subX = pydot.subgraph(graph_name='X', directed=False)
		for no in X:
			subX.add_node(no)
		subY = pydot.subgraph(graph_name='Y', directed=False)
		for no in Y:
			subY.add_node(no)
		self.grafo.add_subgraph(subX)
		self.grafo.add_subgraph(subY)
		
		subM = pydot.subgraph(graph_name='M', directed=False)
		if len(self.grafo.get_edge_list())>0:
			subM.add_edge(self.grafo.get_edge_list()[0])























