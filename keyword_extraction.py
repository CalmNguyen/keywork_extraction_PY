def splitFile(filename):
    f=open(filename,'r',encoding='UTF-8')
    results=f.read()
    out=results.split('\n')
    return out
def tokenizer(text, dict, is_show=False):
    input=text.split(" ")
    words=[]
    s=0
    while True:
        #Số kí tự đã tách
        e=len(input)
        while e>s:
            tmp_word=input[s:e]
            is_word=""
            for item in tmp_word:
                is_word+=item+" "
            is_word=is_word[:-1]
            e-=1
            if is_word.lower() in dict:
                words.append(is_word)
                break
            if e==s:
                words.append(is_word)
                break
        if e>=len(input):
            break
        if is_show:
            print("s = ",s)
            print("e = ",e)
            print(words[len(words)-1])
            print(" "*100)
        s=e+1
    result_list=[]
    result_string=""
    for item in words:
        result_list.append(item.replace(" ", "_"))
    for item in words:
        result_string+=(item.replace(" ", "_"))
        result_string+=" "
    return result_string
#Xóa ký tự dư thừa như .:,?/
def default(texts):
    texts = texts.replace('.',"")
    texts = texts.replace(',',"")
    texts = texts.replace(':',"")
    texts = texts.replace('|',"")
    texts = texts.replace('/',"")
    texts = texts.replace('?',"")
    texts = texts.replace(';',"")
    texts = texts.replace('!',"")
    return texts
#trả về list nhiều đoạn với dạng chữ_chữ thành từ
def Main(filename, texts):
    with open(filename, 'r', encoding='UTF-8') as f:
        l_strip = [s.strip() for s in f.readlines()]
    test1=tokenizer(default(texts), l_strip)
    return test1
def start(filein,fileout,filedict):
    ex=splitFile(filein)
    texts=[]
    for i in range(len(ex)):
        texts.append(Main(filedict, ex[i]))
    # Importing the Tf-idf vectorizer from sklearn
    from sklearn.feature_extraction.text import TfidfVectorizer

    # Defining the vectorizer
    vectorizer = TfidfVectorizer(stop_words='english', max_features= 1000,  max_df = 0.5, smooth_idf=True)

    # Transforming the tokens into the matrix form through .fit_transform()
    matrix= vectorizer.fit_transform(texts)

    # SVD represent documents and terms in vectors
    from sklearn.decomposition import TruncatedSVD
    SVD_model = TruncatedSVD(n_components=10, algorithm='randomized', n_iter=100, random_state=122)
    SVD_model.fit(matrix)

    # Getting the terms 
    terms = vectorizer.get_feature_names()
    # Iterating through each topic
    alltopic=""
    for i, comp in enumerate(SVD_model.components_):
        terms_comp = zip(terms, comp)
        # sorting the 7 most important terms
        sorted_terms = sorted(terms_comp, key= lambda x:x[1], reverse=True)[:7]
        alltopic+="Topic "+str(i)+": \n"
        # printing the terms of a topic
        for t in sorted_terms:
            alltopic+=t[0]+" "
        alltopic+=" \n"

    f=open(fileout,'w', encoding= "UTF-8")
    f.write(alltopic)


import sys
if __name__ == "__main__":
    start(str(sys.argv[1]),str(sys.argv[2]),'copydict.txt')

    


