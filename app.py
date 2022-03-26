from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit
from googletrans import Translator
from janome.tokenizer import Tokenizer


# 翻訳系
#translator = Translator()
translator = Translator(service_urls=['translate.googleapis.com'])

# 形態素解析　分かち書き用
t = Tokenizer()

# Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hogefuga'
socketio = SocketIO(app, async_mode=None)

class SiteInfo:
    title = '音声翻訳'


# 音声入力を受け取る
@app.route('/',methods=['GET','POST'])
def websocket():
    
    return render_template('socket.html',
                           #async_mode = socketio.async_mode, v1.2では不要
                           title = SiteInfo.title,
                           )

# scketioの設定
@socketio.on('receive_content', namespace='/demo') # scket.html側の/demoからreceive_contentに対して送られてきた場合
def send_content(sent_data):

    get_text = sent_data['data'].encode('latin1').decode('utf-8')
    print(get_text)
    
    # 分かち書きを実行して入力が2つ以上の単語の時に英訳して発生させる
    #for token in t.tokenize(get_text):
    #    print(token.surface)
    token_list = [tmp for tmp in t.tokenize(get_text)]

    if len(token_list) > 1:
        trans_en = translator.translate(get_text)
        content = trans_en.text 
        # データをsocket.htmlのmy_contentに送信
        emit('my_content', {'data': content}, broadcast=False)

if __name__ == "__main__":
    socketio.run(app, host='127.0.0.1', port=5000, debug=True) # debug=Trueはサーバー起動中の修正もすぐに反映されるので、運用時にはFalseにすること