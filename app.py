from flask import Flask , jsonify, request, send_file

app  = Flask(__name__)

from videogames import videogames

#GET
@app.route('/')
def welcome():
    return jsonify({"message": "Inventory Application"})

@app.route('/videogames')
def getvideogames():
    return jsonify({        
        "videogames": videogames,
        "total": len(videogames)
        })
    
@app.route('/videoGamesOutOfStock')
def videoGamesOutOfStock():
    videoGame = [videogame for videogame in videogames if videogame['stocks'] == 0]
    return jsonify({        
        "videogames": videoGame,
        "total": len(videoGame)
        })
    
@app.route('/videoGamesName/<string:name>')
def videoGamesName(name: str):
    videoGame = [videogame for videogame in videogames if videogame['name'].upper() == name.upper()]
    return jsonify({        
        "videogames": videoGame,
        "total": len(videoGame)
        })
    
@app.route('/videoGamesConsole/<string:console>')
def videoGamesConsole(console: str):
    videoGame = [videogame for videogame in videogames if videogame['console'].upper() == console.upper()]
    return jsonify({        
        "videogames": videoGame,
        "total": len(videoGame)
        })

@app.route('/videogame/<string:name>/<string:console>')
def getvideogame(name: str,console: str):
    videoGame = [videogame for videogame in videogames if videogame['name'].upper() == name.upper() and videogame['console'].upper() == console.upper()]
    if len(videoGame) == 0:
        return jsonify({        
            "message": "No results with "+ name +" and" + console
        })
    else:       
        return jsonify({        
            "videogame": videoGame
        })


##POST

@app.route('/videogame',methods=['POST'])
def addVideoGame():
    newVideoGame = {
        "name": request.json['name'],
        "console": request.json['console'],
        "price":request.json['price'],
        "stocks":request.json['stocks'],
    }
    videogames.append(newVideoGame )
    return jsonify({        
            "newVideoGame": newVideoGame,
            "message" : "New videogame"
        })

##PUT
@app.route('/videogameAddStock/<string:name>/<string:console>',methods=['PUT'])
def videogameAddStock(name: str,console: str):
    videoGame = [videogame for videogame in videogames if videogame['name'].upper() == name.upper() and videogame['console'] == console.upper()]
    if len(videoGame) > 0:
        videoGame[0]['stocks'] += request.json['stocks']
        return jsonify({        
                "updateVideoGame": videoGame[0],
                "message" : "Update stock videogame"
            })
    return jsonify({
                "message": "No results with "+ name +" and " + console.upper()
            })
    
@app.route('/videogameDeleteStock/<string:name>/<string:console>',methods=['PUT'])
def videogameDeleteStock(name: str,console: str):
    videoGame = [videogame for videogame in videogames if videogame['name'].upper() == name.upper() and videogame['console'] == console.upper()]
    if len(videoGame) > 0:
        videoGame[0]['stocks'] -= request.json['stocks']
        if videoGame[0]['stocks'] < 0:
            videoGame[0]['stocks'] = 0
        return jsonify({        
                "updateVideoGame": videoGame[0],
                "message" : "Update stock videogame"
            })
    return jsonify({
                "message": "No results with "+ name +" and " + console.upper()
            })

@app.route('/videogame/<string:name>/<string:console>',methods=['PUT'])
def updateVideoGame(name: str,console: str):
    videoGame = [videogame for videogame in videogames if videogame['name'].upper() == name.upper() and videogame['console'].upper() == console.upper()]
    if len(videoGame) > 0:
        videoGame[0]['name'] = request.json['name']
        videoGame[0]['console'] = request.json['console']
        videoGame[0]['price'] = request.json['price']
        videoGame[0]['stocks'] = request.json['stocks']  
        return jsonify({        
                "updateVideoGame": videoGame[0],
                "message" : "Update videogame"
            })
    return jsonify({
                "message": "No results with "+ name +" and " + console.upper()
            })
 
##DELETE   
@app.route('/videogame/<string:name>/<string:console>',methods=['DELETE'])
def deleteVideoGame(name: str,console: str):
    videoGame = [videogame for videogame in videogames if videogame['name'].upper() == name.upper() and videogame['console'].upper() == console.upper()]
    if len(videoGame) > 0:
        videogames.remove(videoGame[0])
        return jsonify({
                "message" : "Deleted video game with "+ name +" and " + console.upper()
            })
    return jsonify({
                "message": "No results with "+ name +" and " + console.upper()
            })
    
    
##filtros
@app.route('/videogameFilterPrice/<int:minPrice>/<int:maxPrice>')
def videogameFilterPrice(minPrice,maxPrice):
    filterVideoGame = []
    for videogame in videogames:
        if videogame["price"] >= minPrice and videogame["price"] <= maxPrice:
            filterVideoGame.append(videogame)
    if len(filterVideoGame) != 0:
        return {
                    "Total": len(filterVideoGame),
                    "Video games": filterVideoGame
                }
    else:
        return {
                    "message": "No search results" 
                }

@app.route('/videogameFilterStocks/<int:minStocks>/<int:maxStocks>')
def videogameFilterStocks(minStocks,maxStocks):
    filterVideoGame = []
    for videogame in videogames:
        if videogame["stocks"] >= minStocks and videogame["stocks"] <= maxStocks:
            filterVideoGame.append(videogame)
    if len(filterVideoGame) != 0:
        return {
                    "Total stocks": len(filterVideoGame),
                    "Video games": filterVideoGame
                }
    else:
        return {
                    "message": "No search results" 
                }

##ficheros
@app.route("/downloadReportConsole")
def downloadReportConsole():
    orderVideoGames = sorted(videogames, key=lambda videogame: videogame['console'])
    with open("report.txt", "w") as archivo:
        for game in orderVideoGames:
            archivo.write(f"Name: {game['name']}, Console: {game['console']}, Price: {game['price']} €, Stocks: {game['stocks']}\n")
    return send_file("report.txt", as_attachment=True, download_name="report.txt")

@app.route("/downloadReportPrice")
def downloadReportPrice():
    orderVideoGames = sorted(videogames, key=lambda videogame: videogame['price'])
    with open("report.txt", "w") as archivo:
        for game in orderVideoGames:
            archivo.write(f"Name: {game['name']}, Console: {game['console']}, Price: {game['price']} €, Stocks: {game['stocks']}\n")
    return send_file("report.txt", as_attachment=True, download_name="report.txt")

@app.route("/downloadReportStock")
def downloadReportStock():
    orderVideoGames = sorted(videogames, key=lambda videogame: videogame['stocks'])
    with open("report.txt", "w") as archivo:
        for game in orderVideoGames:
            archivo.write(f"Name: {game['name']}, Console: {game['console']}, Price: {game['price']} €, Stocks: {game['stocks']}\n")
    return send_file("report.txt", as_attachment=True, download_name="report.txt")

@app.route("/downloadReportName")
def downloadReportName():
    orderVideoGames = sorted(videogames, key=lambda videogame: videogame['name'])
    with open("report.txt", "w") as archivo:
        for game in orderVideoGames:
            archivo.write(f"Name: {game['name']}, Console: {game['console']}, Price: {game['price']} €, Stocks: {game['stocks']}\n")
    return send_file("report.txt", as_attachment=True, download_name="report.txt")

@app.route("/downloadReportStock_0")
def downloadReportStock_0():
    orderVideoGames = sorted(videogames, key=lambda videogame: videogame['console'])
    with open("report.txt", "w") as archivo:
        for game in orderVideoGames:
            if game['stocks'] == 0:
                archivo.write(f"Name: {game['name']}, Console: {game['console']}, Price: {game['price']} €, Stocks: {game['stocks']}\n")
    return send_file("report.txt", as_attachment=True, download_name="report.txt")

#Esto va al final
if __name__ == '__main__':
    app.run(debug=True , port=4000)