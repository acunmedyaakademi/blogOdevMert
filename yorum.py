import sqlite3
from flask import Flask, jsonify, request

app= Flask(__name__)

@app.route('/comment')
def comment_main():
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM comment')
    rows = cursor.fetchall()
    comment = []
    for row in rows:
        comment.append({
            'id':row[0],
            'isim':row[1],
            'soy isim':row[2],
            'yorum':row[3],
            'bağlı olduğu post':row[4]
        }
    )
    conn.close()
    return jsonify(comment)

@app.route('/comment/add/<int:id>', methods=['POST'])
def comment_add(id):
    commnet_name = request.values['name']
    comment_surname = request.values['surname']
    comment_comment = request.values['comment']
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO comment (name,surname,comment,post_id) VALUES (?,?,?,?)', (commnet_name,comment_surname,comment_comment,id))
    comment_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return jsonify({'id': comment_id})

@app.route('/comment/delete/<int:id>', methods=['DELETE'])
def comment_delete(id):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM comment WHERE id=?', (id,))
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    if rows_affected > 0:
        return jsonify(
           {
                'Durum': True
            }
        )
    else:
        return jsonify(
            {
                'Durum': False,
                'Uyarı': 'Yanlış id'
            }
        )

@app.route('/comment/update/<int:id>',methods=['PATCH'])
def comment_update(id):
    commnet_name = request.values['name']
    commnet_surname = request.values['surname']
    comment_comment = request.values['comment']

    conn=sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE comment SET name=?, surname=?, comment=? WHERE id=?', (commnet_name, commnet_surname, comment_comment, id))
    conn.commit()
    conn.close()
    
    return jsonify({'id': id})
        
@app.route('/comment/read/<int:id>')
def comment_read(id):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM comment WHERE id=?', (id,) )
    rows = cursor.fetchall()
    blog = []
    for row in rows:    
        blog.append({
            'id': row[0],
            'name': row[1],
            'surname': row[2],
            'comment': row[3],
            'post_id': row[4]
           
        })
    conn.close()
    return jsonify(blog)

app.run()