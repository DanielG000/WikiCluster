from Wiki import app
from Wiki.Users import Users
from Wiki.Escritores import Escritores
from Wiki.Mangas import Mangas
from Wiki.Generos import Generos
from Wiki.Animes import Animes
from Wiki.Episodios import Episodios
from Wiki.Personajes import Personajes
from Wiki.Seiyuus import Seiyuus
from Wiki.Productores import Productores
#from Wiki.UpFromFile import UpFromFile

app.register_blueprint(Users)
app.register_blueprint(Escritores)
app.register_blueprint(Mangas)
app.register_blueprint(Generos)
app.register_blueprint(Animes)
app.register_blueprint(Episodios)
app.register_blueprint(Personajes)
app.register_blueprint(Seiyuus)
app.register_blueprint(Productores)
#app.register_blueprint(UpFromFile)
