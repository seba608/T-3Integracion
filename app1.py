from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
import requests
import json

app = Flask(__name__)
Bootstrap(app)


def make_query(query):
    request = requests.post('https://swapi-graphql-integracion-t3.herokuapp.com', json={'query': query})
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Failed {}. {}".format(request.status_code, query))


@app.route("/")
def index():
    query = """query {
                  allFilms {
                        films{
                              id
                              title
                              releaseDate
                              director
                              producers
                              episodeID
                              openingCrawl
                        }
                  }
                }
                """
    r = make_query(query)
    data = r["data"]["allFilms"]
    print(data)
    return render_template("index.html", films=data["films"])


@app.route('/pelicula/<film_id>')
def mostrar_pelicula(film_id):
    query = """query {
                  film(id: "%s") {
                        title
                        releaseDate
                        director
                        producers
                        episodeID
                        openingCrawl
                        characterConnection{
                            characters{
                                name
                                id
                            }
                        }
                        planetConnection{
                            planets{
                                name
                                id
                            }
                        }
                        starshipConnection{
                            starships{
                                name
                                id
                            }
                        }
                    }
                }""" % film_id
    r = make_query(query)
    data = r["data"]
    personajes = data["film"]["characterConnection"]["characters"]
    planetas = data["film"]["planetConnection"]["planets"]
    naves = data["film"]["starshipConnection"]["starships"]
    return render_template("pelicula.html", pelicula=data["film"], personajes=personajes,
                           planetas=planetas, naves=naves)


@app.route('/personaje/<personaje_id>')
def mostrar_personaje(personaje_id):
    query = """query {
                person(id: "%s") {
                    name
                    birthYear
                    eyeColor
                    gender
                    hairColor
                    height
                    mass
                    skinColor
                    skinColor
                    starshipConnection{
                        starships{
                            name
                            id
                            }
                        }
                    filmConnection{
                        films{
                            title
                            id
                            }
                        }
                        homeworld{
                            id
                            name
                        }
                    }
                }""" % personaje_id

    r = make_query(query)
    data = r["data"]
    character = data["person"]
    planeta = data["person"]["homeworld"]
    peliculas = data["person"]["filmConnection"]["films"]
    naves = character["starshipConnection"]["starships"]
    return render_template("personaje.html", personaje=character, peliculas=peliculas,
                           planeta=planeta, naves=naves)


@app.route('/nave/<nave_id>')
def mostrar_nave(nave_id):
    query = """query {
        starship(id: "%s") {
            MGLT
            cargoCapacity
            consumables
            costInCredits
            crew
            hyperdriveRating
            length
            manufacturers
            maxAtmospheringSpeed
            model
            name
            passengers
            filmConnection{
                films{
                    title
                    id
                }
            }
            pilotConnection{
                pilots{
                    name
                    id
                }
            }
            starshipClass
        }
    }""" % nave_id

    r = make_query(query)
    data = r["data"]
    nave = data["starship"]
    pilots = nave["pilotConnection"]["pilots"]
    peliculas = nave["filmConnection"]["films"]
    return render_template("nave.html", variable=nave, peliculas=peliculas,
                           pilotos=pilots)


@app.route('/planeta/<planeta_id>')
def mostrar_planeta(planeta_id):
    query = """query {
                planet(id: "%s") {
                    name
                    climates
                    diameter
                    filmConnection{
                        films{
                            title
                            id
                        }
                    }
                    gravity
                    orbitalPeriod
                    population
                    residentConnection{
                        residents{
                            name
                            id
                        }
                    }
                    rotationPeriod
                    surfaceWater
                    terrains				
                    }
                }""" % planeta_id

    r = make_query(query)
    data = r["data"]
    planeta = data["planet"]
    residents = data["planet"]["residentConnection"]["residents"]
    peliculas = data["planet"]["filmConnection"]["films"]

    return render_template("planeta.html", variable=planeta, peliculas=peliculas,
                           pilotos=residents)


if __name__ == '__main__':
    app.run(debug=True)
