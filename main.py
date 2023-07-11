import sqlite3
from flask import Flask, jsonify, request
from yorum import comment_main,comment_add,comment_delete,comment_read,comment_update

app = Flask(__name__)

@app.route('/')
def main():
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM blog')
    rows = cursor.fetchall()
    blog= []
    for row in rows:
        blog.append({
            'id':row[0],
            'başlık':[1],
            'özet':row[2]
        }
    )
    conn.close()
    return jsonify(blog)


@app.route('/add', methods=['POST'])
def  add():
    blog_baslık = request.values['baslik']
    blog_ozet = request.values['ozet']
    blog_icerik = request.values['icerik']
    
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO blog (baslik,ozet,icerik) VALUES (?,?,?)', (blog_baslık,blog_ozet,blog_icerik))
    blog_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return jsonify({'id': blog_id})

@app.route('/read')
def read():
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM blog' )
    rows = cursor.fetchall()
    blog = []
    for row in rows:    
        blog.append({
            'id': row[0],
            'başlık': row[1],
            'özet': row[2],
            'içerik': row[3]
           
        })
    conn.close()
    return jsonify(blog)
     
@app.route('/delete/<int:id>',methods = ['DELETE'])
def delete(id):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM blog WHERE id=?', (id,))
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


@app.route('/update/<id>',methods=['PATCH'])
def update(id):
    blog_baslık = request.values['baslik']
    blog_ozet = request.values['ozet']
    blog_icerik = request.values['icerik']

    conn=sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE blog SET baslik=?, ozet=?, icerik=? WHERE id=?', (blog_baslık, blog_ozet, blog_icerik, id))
    conn.commit()
    conn.close()
    
    return jsonify({'id': id})
    

@app.route('/read/<int:id>')
def readid(id):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM blog WHERE id=?',(id,) )
    row = cursor.fetchone()
    blog = {
   
            'id': row[0],
            'başlık': row[1],
            'özet': row[2],
            'içerik': row[3]
      }
    conn.close()
    return jsonify(blog)

@app.route('/comment')
def comment():
    return comment_main

@app.route('/comment/read/<int:id>')
def commentread():
    return comment_read


@app.route('/comment/update/<int:id>',methods=['PATCH'])
def commentupdate(id):
    return comment_update

@app.route('/commnet/delete/<int:id>', methods=['DELETE'])
def commentdelete(id):
    return comment_delete

@app.route('/comment/add/<int:id>', methods=['POST'])
def commentadd(id):
    return comment_add

app.run()