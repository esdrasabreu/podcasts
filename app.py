from flask import Flask, request, jsonify, make_response
from flask import render_template
import sqlite3
import datetime

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
DATABASE = 'podcasts.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db


@app.route('/podcasts', methods=['GET'])
def get_podcasts():
    
    db = get_db()

    podcasts = db.execute('SELECT * FROM podcast').fetchall()
    
    db.close()
    
    return render_template('podcasts.html', podcasts=podcasts)

    
@app.route('/podcasts/episodio/<string:episodio>', methods=['GET'])
def get_podcast_by_episodio(episodio):
    db = get_db()
    podcasts = db.execute("SELECT * FROM podcast WHERE episodio LIKE '%' || ? || '%'", (episodio,)).fetchall()
    db.close()
    if podcasts:
            return make_response(jsonify([dict(podcast) for podcast in podcasts]), 200)
    else:
        return make_response(jsonify({'message': 'Podcast not found'}), 404)


@app.route('/podcasts/data/<string:data>', methods=['GET'])
def get_podcast_by_data(data):
    db = get_db()
    podcasts = db.execute("SELECT * FROM podcast WHERE data LIKE '%' || ? || '%'", (data,)).fetchall()
    db.close()
    if podcasts:
            return make_response(jsonify([dict(podcast) for podcast in podcasts]), 200)
    else:
        return make_response(jsonify({'message': 'Podcast not found'}), 404)


@app.route('/podcasts/duracao/<string:duracao>', methods=['GET'])
def get_podcast_by_duracao(duracao):
    db = get_db()
    podcasts = db.execute("SELECT * FROM podcast WHERE duracao LIKE '%' || ? || '%'", (duracao,)).fetchall()
    db.close()
    if podcasts:
        return make_response(jsonify([dict(podcast) for podcast in podcasts]), 200)
    else:
        return make_response(jsonify({'message': 'Podcast not found'}), 404)


@app.route('/podcasts/descricao/<string:descricao>', methods=['GET'])
def get_podcast_by_descricao(descricao):
    db = get_db()
    podcasts = db.execute("SELECT * FROM podcast WHERE descricao LIKE '%' || ? || '%'", (descricao,)).fetchall()
    db.close()
    if podcasts:
        return make_response(jsonify([dict(podcast) for podcast in podcasts]), 200)
    else:
        return make_response(jsonify({'message': 'Podcast not found'}), 404)


@app.route('/podcasts', methods=['POST'])
def create_podcast():
    data = request.get_json()
    if not data or not all(key in data for key in ('episodio', 'duracao', 'data', 'link', 'descricao')):
        return jsonify({'message': 'Data not provided or invalid'}), 400
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO podcast (episodio, duracao, data, link, descricao) VALUES (?, ?, ?, ?, ?)',
                   (data['episodio'], data['duracao'], data['data'], data['link'], data['descricao']))
    db.commit()
    new_id = cursor.lastrowid
    db.close()
    return jsonify({'id': new_id, 'message': 'Podcast created'}), 201

@app.route('/podcasts/<int:id>', methods=['PUT'])
def update_podcast(id):
    data = request.get_json()
    if not data or not all(key in data for key in ('episodio', 'duracao', 'data', 'link', 'descricao')):
        return jsonify({'message': 'Data not provided or invalid'}), 400
    db = get_db()
    cursor = db.cursor()
    cursor.execute('UPDATE podcast SET episodio = ?, duracao = ?, data = ?, link = ?, descricao = ? WHERE id = ?',
                   (data['episodio'], data['duracao'], data['data'], data['link'], data['descricao'], id))
    db.commit()
    db.close()
    return jsonify({'message': 'Podcast updated'}), 200

@app.route('/podcasts/<int:id>', methods=['DELETE'])
def delete_podcast(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM podcast WHERE id = ?', (id,))
    db.commit()
    db.close()
    return jsonify({'message': 'Podcast deleted'}), 200

if __name__ == '__main__':
    app.run(port=8080, debug=True)
