from libraries import *
from database import *
def preprocessing():
    change_tags={}
    for i in tag_intent.keys():
       change_tags[i]=i
    change_tags['AggregationColumn']=change_tags['ComparisonColumnOne']=change_tags['ComparisonColumnTwo']=change_tags['ComparisonColumnThree']=change_tags['ColumnNumberOne']=change_tags['ColumnNumberTwo']=change_tags['ColumnNumberThree']='column_name'
    change_tags['GroupByColumn']=change_tags['OrderByColumn']='column_name'       
    change_tags['ColumnValueOne']=change_tags['ColumnValueTwo']=change_tags['ColumnValueThree']='column_value'       
    change_tags['ComparatorOne']=change_tags['ComparatorTwo']=change_tags['ComparatorThree']='comparators'
    change_tags['binary_logic_operator2']='binary_logic_operator'

    tag_intent['AggregationColumn']=tag_intent['ComparisonColumnOne']=tag_intent['ComparisonColumnTwo']=tag_intent['ComparisonColumnThree']=tag_intent['ColumnNumberOne']=tag_intent['ColumnNumberTwo']=tag_intent['ColumnNumberThree']=tag_intent['GroupByColumn']=tag_intent['OrderByColumn']=tag_intent['column_name']       

    tag_intent['ColumnValueOne']=tag_intent['ColumnValueTwo']=tag_intent['ColumnValueThree']=tag_intent['column_value']       
     
    tag_intent['ComparatorOne']=tag_intent['ComparatorTwo']=tag_intent['ComparatorThree']=tag_intent['comparators']       
        
    tag_intent['binary_logic_operator2']=tag_intent['binary_logic_operator']

    #function for extracting intents and coressponding value(tag)
    def extract_phrases(s,d=[]):
        start = s.find('{')
        if start == -1: # No opening bracket found stops the function
            return ''
        start += 1
        end = s.find('}', start)
        w= s[start:end] #getting intent(word) using the start and end index
        d.append(w)
        extract_phrases(s[end+1:],d)   #recalling
        return d



    #function for creating json file from md or txt file 
    sents=[]
    def create_md(path_of_text_file):
        f = open(path_of_text_file, "r")  
        z=f.readline()
        sents=[]
        while z:
            l=extract_phrases(z,d=[])
            for i in l:
                z=z.replace('{','(').replace('}',')')
                w='('+i+')'
                r=random.choice(tag_intent[i])
                k='['+r+']'+w
                z=z.replace(w,k)
            sents.append(z)
            z=f.readline()
        #print(len(sents))
        return sents


    prefinal_list=[]
    for i in range(5):
        sents=create_md(path_of_text_file='/home/saireddy/Music/entity_recognition/required_sayings.txt')
        prefinal_list+=sents
    final_list=[]
    #with open('utter.txt', 'w') as f:
    for line in prefinal_list:
        df=extract_phrases(line,d=[])
        for w in df:
            line=line.replace('{','(').replace('}',')')
            #line=str(line)
            line=line.replace(w,change_tags[w])
        final_list.append(line.replace('\n',''))
    def extract(s,d={}):
        start = s.find('[')
        s2 = s.find('(')
        if start == -1: # No opening bracket found stops the function
            return ''
        start += 1
        s2+=1# skip the bracket, move to the next character
        end = s.find(']', start)
        e2=s.find(')',s2)
        w= s[start:end] #getting intent(word) using the start and end index
        intent=s[s2:e2] #getting value(tag) using the start and end index extracted using find function
        d[w]=intent     #storing in the dictionary
        extract(s[e2+1:],d)   #recalling till no brackets are found
        return d


    #function for creating json file from md or txt file 

    def create_json(utter_list,path_of_jsonfile):
        #f = open(path_of_md_file, "r")
        end_list=[]
        dictn={}
        #z=f.readline()
        fn=[]
        for line in final_list:
            di={}
            di=extract(line,d={})
            dictn={}
            word=[]
            word=[x for x in di]
            inter_list=[]
            x=re.sub("\(.*?\)", "", line)
            x=x.replace('[','').replace(']','')
            x=re.sub(' +',' ',x)
            for w in word:
                try:
                    n=x.count(w)
                    if n>1:
                        r_string = r"\b({})\b".format(w)
                        start_indices=[(g.start(), g.group()) for g in re.finditer(r_string,x)]
                        for i in start_indices:
                            s_endindex=i+len(w)
                            inter_list.append((i,s_endindex,di[w]))
                    else:
                        re_string = r"\b({})\b".format(w)
                        s_sindex=re.search(re_string,x).start()
                        #s_sindex=re.find(w)
                        s_endindex=s_sindex+len(w)
                        inter_list.append((s_sindex,s_endindex,di[w]))
                except:
                    pass
            dictn['entities']=inter_list
            fn=[x.replace('\n',''),dictn]
            tp=tuple(fn)
            end_list.append(tp)
            #z=f.readline()
        with open(path_of_jsonfile, 'w') as outfile:
            json.dump(end_list, outfile)
        #print(len(end_list))
        #return end_list

    create_json(utter_list=final_list,path_of_jsonfile='utterances.json')

preprocessing()
