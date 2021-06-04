from selenium import webdriver
import os, sys, csv, time

#################################################################################################################################
# Código para fazer a consulta dos filmes, encontrados dentro do arquivo .csv, e obter o id, no sistema do imdb, utilizando 	#
# o chromedriver e o google para realizar a busca, que possui resultados melhores que o método de busca da api do imdb.			#
#################################################################################################################################

##Para atualizar o selenium, acesse:
#https://chromedriver.chromium.org/downloads

#Contador de falhas no acesso
cont = 0

#Varíaveis para acesso
obj_orig = 'files/Filmes.csv' #Arquivo com a lista de filmes original
obj_dest = 'files/Filmes_com_id.csv' #Arquivo com a lista de filmes com id
chromedriver = 'files/chromedriver' #Localização do chromedriver

def timeme(method):
    def wrapper(*args, **kw):
        startTime = int(round(time.time() * 1000))
        result = method(*args, **kw)
        endTime = int(round(time.time() * 1000))
        print((endTime - startTime)/1000, 's')
        return result
    return wrapper

class movie:
	nome = None
	
	def __init__(self, nome):
		self.nome = nome

	def url_busca(self):
		valor = ''
		nome = self.nome.split(' ')
		for i in range(0,len(nome)):
			valor += '+' + nome[i]
		return 'https://www.google.com.br/search?as_sitesearch=imdb.com&q=' + valor

	def obter_id(self):
		global cont #defino a variável cont como global
		try:
			link = driver.find_elements_by_xpath('//*[@id="rso"]/div[1]/div/div[1]/a')[0].get_attribute('href')
			link = link.split('/')
			id_final = link[4][2:] #Retorno do terceiro caracter em diante
			cont = 0
			return id_final
		except:
			cont+=1
		

if __name__ == '__main__':

	os.chdir(sys.path[0]) #seleciono o caminho atual como padrão

	#Verifico se existe a pasta files. Se não existir, eu crio.
	if not os.path.isdir("files"):
		os.mkdir("files")

	#Abro o Chrome
	driver = webdriver.Chrome(chromedriver)

	#Crio os objetos para fazer as escritas e leituras dos .csv
	read_obj = open(obj_orig,'r')
	write_obj = open(obj_dest,'w', newline = '')
	csv_reader = csv.reader(read_obj)
	csv_writer = csv.writer(write_obj)

	for lin in csv_reader:
		filme = movie(lin[0]) #Pego nome do filme

		driver.get(filme.url_busca()) #Obtenho a url
		time.sleep(2)
		
		lin.append(filme.obter_id()) #Adiciono o novo id ao csv
		if cont == 3:
			break #Saio do loop caso tenha 3 falhas consecutivas
		csv_writer.writerow(lin) #Escrevo a linha no .csv

	#Fecho as conexões
	driver.close()
	read_obj.close()
	write_obj.close()