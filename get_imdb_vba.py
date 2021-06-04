# import our libraries
import pythoncom
import imdb

ia = imdb.IMDb()

class PythonObjectLibrary:
    # This will create a GUID to register it with Windows, it is unique.
    _reg_clsid_ = pythoncom.CreateGuid()

    # Register the object as an EXE file, the alternative is an DLL file (INPROC_SERVER)
    _reg_clsctx_ = pythoncom.CLSCTX_LOCAL_SERVER

    # the program ID, this is the name of the object library that users will use to create the object.
    _reg_progid_ = "Python.ObjectLibrary"

    # this is a description of our object library.
    _reg_desc_ = "This is our Python object library."

    # a list of strings that indicate the public methods for the object. If they aren't listed they are conisdered private.
    _public_methods_ = ['obter_id', 'obter_nome_pt','obter_nome_en','obter_ano','obter_genero','obter_nota']

    
    nome = None
    id = 0
    def obter_id(self,nome):
        filme_id = ia.search_movie(nome)
        if len(filme_id) != 0:
            return filme_id[0].movieID

    def obter_nome_pt(self, id):
        i = 0
        titulo_pt = None
        try:
            raw_akas = ia.get_movie_release_dates(id)['data']['raw akas']
            for i in range(0,len(raw_akas)):
                if 'Brazil' == raw_akas[i]['countries']:
                    titulo_pt = raw_akas[i]['title']
                    break
            if titulo_pt == None:
                #Se eu não achar o país 'Brazil', eu procuro pelo idioma original
                if ' (original title)' == raw_akas[0].get('countries'): 
                    return raw_akas[0].get('title')
            else:
                return titulo_pt
        except:
            return ia.get_movie(id).get('title')

    def obter_nome_en(self, id):
        titulo_en = ia.get_movie(id).get('title')
        return titulo_en

    def obter_ano(self, id):
        filme_data = ia.get_movie_release_dates(id)['data']['raw release dates'][0]['date']
        ano = filme_data.split(' ')
        ano = ano[len(ano) - 1]
        return ano

    def obter_genero(self, id):
        generos = ia.get_movie(id).get('genres')
        return ', '.join(generos)

    def obter_nota(self, id):
        nota = ia.get_movie(id).get('rating')
        return nota 

if __name__ == '__main__':
    import win32com.server.register
    win32com.server.register.UseCommandLine(PythonObjectLibrary)