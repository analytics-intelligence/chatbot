import os
import wikipedia
from flask_cors import CORS
from bert import QA
from flask import Flask, request, jsonify, abort
from werkzeug.utils import secure_filename
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from chatterbot import ChatBot 
from twilio.twiml.messaging_response import MessagingResponse
from middleware.helper import training_list, question_list, greeting_list

app = Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER'] = 'dataset'
app.config['ALLOWED_EXTENSIONS'] = ['.csv', '.txt']

Bot = ChatBot('Anthony', read_only=True)
trainer = ListTrainer(Bot)
corpus_trainer = ChatterBotCorpusTrainer(Bot)
corpus_trainer.train('chatterbot.corpus.english.greetings')
trainer.train(training_list)

model = QA("model")

@app.route("/",methods=['POST'])
def predict():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    if incoming_msg in greeting_list:
        corpus_response = Bot.get_response(incoming_msg)
        msg.body(str(corpus_response))
        return str(resp)
    else:
        for item in question_list:
            if incoming_msg in item.lower():
                chatterbot_response = Bot.get_response(incoming_msg)
                msg.body(str(chatterbot_response))
                return str(resp)
            else:
                pass
        wiki_response = wikipedia.summary(incoming_msg, sentences=4)
        try:
            out = model.predict(wiki_response, incoming_msg)
            msg.body(out["answer"])
            return str(resp)
        except Exception as e:
            print(e)
            return jsonify({"result":"Model Failed"})


@app.route('/upload', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['ALLOWED_EXTENSIONS']:
            abort(400)
        uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'response': 'File successfully uploaded and saved'})



if __name__ == "__main__":
    app.run()

