from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit

# 翻訳系
from googletrans import Translator
translator = Translator()

# 形態素解析　分かち書き用
from janome.tokenizer import Tokenizer
t = Tokenizer()

# Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hogefuga'
socketio = SocketIO(app, async_mode=None)

class SiteInfo:
    title = 'ページタイトル'


# 音声入力を受け取る
@app.route('/websocket',methods=['GET','POST'])
def websocket():
    
    return render_template('socket.html',
                           async_mode = socketio.async_mode,
                           title = SiteInfo.title,
                           )

# scketioの設定
@socketio.on('receive_content', namespace='/demo') # scket.html側の/demoからreceive_contentに対して送られてきた場合
def send_content(sent_data):
    
    # 分かち書きを実行して入力が2つ以上の単語の時に英訳して発生させる
    #print(t.tokenize(sent_data['data']).surface)
    for token in t.tokenize(sent_data['data']):
        print(token.surface)
    token_list = [tmp for tmp in t.tokenize(sent_data['data'])]

    if len(token_list) > 1:

        trans_en = translator.translate(sent_data['data'])

        content = '%s' % trans_en.text # socket.html側で{data:content}としているのでこうなる。
        
        # データをsocket.htmlのmy_contentに送信
        emit('my_content', {'data': content}, broadcast=False)

if __name__ == "__main__":
    socketio.run(app, host='127.0.0.1', port=5000, debug=True) # debug=Trueはサーバー起動中の修正もすぐに反映されるので、運用時にはFalseにすること