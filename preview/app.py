from flask import Flask, render_template, request, redirect
import pymysql
from recommendersystem import RecommenderSystem

app = Flask(__name__)

con = pymysql.connect(host='localhost', user='kopi', password='kopi', db='mp_recomsys')
cursor = con.cursor(pymysql.cursors.DictCursor)

query = "SELECT * FROM product"
recsys = RecommenderSystem(data=query)
recsys.fit()

@app.template_filter()
def currencyFormat(value):
    value = int(value)
    return "Rp. {:,d}".format(value)


@app.template_filter()
def scoreFormat(value):
    return "{:.2f}".format(value)

@app.route('/')
def index():
    return render_template('index.html', active_page='index')

@app.route('/data', methods=['POST', 'GET'])
def data():

    keyword = ['thinkpad x230', 'ssd 240gb', 'minna no nihongo', 'ps4', 'gitar akustik']
    count = 1
    price_input = 0
    topk_input = 20

    if request.method == 'POST':
        keyword_select = request.form['keyword']

        if request.form['keyword'] == keyword[2]:
            price_input = 80000

        if request.form['keyword'] == keyword[4]:
            price_input = 20000

        if request.form['price']:
            price_input = int(request.form['price'])

        if request.form['topk']:
            topk_input = int(request.form['topk'])

        data_entry = recsys.recommend_demo(keyword=keyword_select, prices=price_input, topk=topk_input)
        return render_template('data.html', active_page='data', data_entry=data_entry, keywords=keyword, count=count)
    else:
        data_entry = recsys.recommend_demo(keyword="thinkpad x230")
        return render_template('data.html', active_page='data', data_entry=data_entry, keywords=keyword, count=count)

@app.route('/recommendation', methods=['POST', 'GET'])
def recommendation():

    keyword = ['thinkpad x230', 'ssd 240gb', 'minna no nihongo', 'ps4', 'gitar akustik']
    price_input = 0
    topk_input = 18

    if request.method == 'POST':
        keyword_select = request.form['keyword']
        
        if request.form['keyword'] == keyword[2]:
            price_input = 80000
        
        if request.form['keyword'] == keyword[4]:
            price_input = 20000

        if request.form['price']:
            price_input = int(request.form['price'])

        if request.form['topk']:
            topk_input = int(request.form['topk'])

        data_entry = recsys.recommend_demo(keyword=keyword_select, prices=price_input, topk=topk_input)
        return render_template('recommendation.html', active_page='recommendation', data_entry=data_entry, keywords=keyword)
    else:
        data_entry = recsys.recommend_demo(keyword="thinkpad x230", topk=topk_input)
        return render_template('recommendation.html', active_page='recommendation', data_entry=data_entry, keywords=keyword)

@app.route('/detail', methods=['POST', 'GET'])
def detail():

    id_product = request.args.get('idp')
    index = int(request.args.get('idx'))

    query = 'SELECT * FROM product WHERE id_product=' + id_product
    cursor.execute(query)
    results = cursor.fetchall()

    cb_data = recsys.recommend_cb(idx=index)
                   
    return render_template('detail.html', active_page='recommendation', results=results, cb_data=cb_data)

@app.route('/graph', methods=['POST', 'GET'])
def graph():
    
    keyword = [{1:'thinkpad x230', 2:'ssd 240gb', 3:'minna no nihongo', 4:'ps4', 5:'gitar akustik'}]
    keyword_is = "All"
    
    if request.method == 'POST':
        keyword_is = keyword[0][int(request.form['keyword'])]
        keyword_select = str(request.form['keyword'])
        sql = """SELECT 
                'All' AS marketplace, 
                COUNT(*) AS total_product,
                SUM(product.review) AS total_sold 
                FROM store
                LEFT JOIN product ON store.id_store = product.id_product

                UNION

                SELECT 
                marketplace.marketplace,
                COUNT(store.id_marketplace) AS total_product,
                SUM(product.review) AS total_sold 
                FROM ((store
                LEFT JOIN marketplace ON store.id_marketplace = marketplace.id_marketplace)
                LEFT JOIN product ON store.id_store = product.id_store)
                WHERE store.id_keyword= """ + keyword_select + " GROUP BY marketplace.marketplace;"
        cursor.execute(sql)
        results = cursor.fetchall()
    else:
        sql = """SELECT 
                'All' AS marketplace, 
                COUNT(*) AS total_product,
                SUM(product.review) AS total_sold  
                FROM store
                LEFT JOIN product ON store.id_store = product.id_product

                UNION

                SELECT 
                marketplace.marketplace AS marketplace,
                COUNT(store.id_marketplace) AS total_product,
                SUM(product.review) AS total_sold
                FROM ((store
                LEFT JOIN marketplace ON store.id_marketplace = marketplace.id_marketplace)
                LEFT JOIN product ON store.id_store = product.id_product)
                GROUP BY marketplace.marketplace;"""
        cursor.execute(sql)
        results = cursor.fetchall()

    return render_template('graph.html', active_page='graph', keywords=keyword, results=results, keyword_is=keyword_is)
