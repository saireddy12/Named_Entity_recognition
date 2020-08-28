#python files to import
from libraries import *
from preprocessing import *
from  encrypting import *
@app.route('/app/v1/test',methods =['GET','POST'])
@auth.login_required
def test(model_path='model'):
    if (request.method=='POST'):
        text = request.json['text']
        query=text
        doc = prdnlp(query)
        l=[]
        for ent in doc.ents:
            d={}
            d['text']=ent.text
            d['start']=ent.start_char
            d['end']=ent.end_char
            d['value']=ent.label_
            l.append(d)
            d={}
            #print(ent.text, ent.start_char,ent.end_char,ent.label_)
        js=json.dumps(l)
        #print(js)
        return js
    else:
        pass
    return "ok"
    #return jsonify({ 'data': 'Hello, %s!' % g.user.username })


@app.route('/app/v1/train', methods=['GET'])
@auth.login_required
def train():
    #function for training the model
    def train_spacy(input_file_path,iterations):
        with open(input_file_path) as json_file:
            data = json.load(json_file)
        TRAIN_DATA = data
        nlp = spacy.blank('en')  # create blank Language class
        # create the built-in pipeline components and add them to the pipeline
        # nlp.create_pipe works for built-ins that are registered with spaCy
        if 'ner' not in nlp.pipe_names:
            ner = nlp.create_pipe('ner')
            nlp.add_pipe(ner, last=True)

        # add labels
        for _, annotations in TRAIN_DATA:
             for ent in annotations.get('entities'):
                ner.add_label(ent[2])

        # get names of other pipes to disable them during training
        print("Started Training")
        other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
        with nlp.disable_pipes(*other_pipes):  # only train NER
            optimizer = nlp.begin_training()
            for itn in range(iterations):
        
                print("Statring iteration " + str(itn+1))
                #random.shuffle(TRAIN_DATA)
                losses = {}
                for text, annotations in TRAIN_DATA:
                    nlp.update(
                        [text],  # batch of texts
                        [annotations],  # batch of annotations
                        drop=0.2,  # dropout - make it harder to memorise data
                        sgd=optimizer,losses=losses)
                print(losses)
        return nlp

    start_time = time.time()
    prdnlp = train_spacy('utterances.json',2)
    print("--- Timem taken for training %s seconds ---" % (time.time() - start_time))
    # Save our trained Model
    model_name='user1'+'model'
    prdnlp.to_disk(model_name)
    return 'Model Trained'
if __name__ == '__main__':
    app.debug = True
    prdnlp=spacy.load("model")
    app.run(host='0.0.0.0', port=5000)
