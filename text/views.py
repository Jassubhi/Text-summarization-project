import math
import operator
import os
import re
import string

import PyPDF2 as pdf
import gensim
import nltk
import textract as tt
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from gensim import corpora
from gtts import gTTS
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize

from text.forms import DocumentForm
from text.models import Document

name = ""
topics = ""
Questions = ""
Answer = ""
phrases = ""
ans = ""
doc = ""
documentary = ""


def home(request):
    context = {}
    ques = {}
    # doc = ''
    if request.POST.get('uploadFile'):
        uploaded_file = request.FILES['documents']
        print(uploaded_file.name)
        fs = FileSystemStorage()
        print(fs)
        global name
        name = fs.save(uploaded_file.name, uploaded_file)
        d = "\\"
        global doc
        doc = settings.MEDIA_ROOT + d + name
        print(doc)
        context['context'] = fs.url(name)
        global topics
        topics = topic_modelling(doc)
        context['topics'] = topics
        return render(request, 'text/home.html', context)

    if request.POST.get('submittedTopic'):
        x1 = "soil"
        x1 = request.POST['selectedTopic']
        print(x1)
        x2 = doc
        global Questions
        global Answer
        global phrases
        Questions, Answer, phrases = generate_question_answer(x1, x2)
        context['context'] = doc
        context['topics'] = topics
        return render(request, 'text/home.html', context)

    if request.POST.get('generateQuestion'):
        context['context'] = doc
        context['topics'] = topics
        context['Questions'] = Questions
        # print('Questions',Questions)
        return render(request, 'text/home.html', context)

    if request.POST.get('selectedQuestion'):
        global sq
        sq = request.POST['QuestionsList']
        print("**************", sq)
        context['context'] = doc
        context['topics'] = topics
        context['Questions'] = Questions
        return render(request, 'text/home.html', context)

    if request.POST.get('generateAnswer'):
        context['context'] = doc
        context['topics'] = topics
        context['Questions'] = Questions
        global ans
        ans = generate_relevant_answer(sq, Answer, phrases)
        context['Answer'] = ans
        print('ans', Answer)
        print(phrases)
        print(sq)
        return render(request, 'text/home.html', context)

    if request.POST.get('SpeechAnswer'):
        context['context'] = doc
        context['topics'] = topics
        context['Questions'] = Questions
        context['Answer'] = ans
        language = 'en'
        mytext = ans
        myobj = gTTS(text=mytext, lang=language, slow=False)
        myobj.save("%s.mp3" % os.path.join(settings.MEDIA_ROOT, "answer"))
        os.system("%s.mp3" % os.path.join(settings.MEDIA_ROOT, "answer"))
        print("%s.mp3" % os.path.join(settings.MEDIA_ROOT, "answer"))
        return render(request, 'text/home.html', context)

    if request.POST.get('generateSummary'):
        global text_input
        text_input = ans
        print("text_input is assigned in IF ------ ", len(text_input))
        summarized_answer = summary_of_selected(text_input)
        context['context'] = doc
        context['topics'] = topics
        context['Questions'] = Questions
        context['Answer'] = ans
        context['Summarized_Answer'] = summarized_answer
        return render(request, 'text/home.html', context)

    return render(request, 'text/home.html', context)


def text_pre_processing(x):
    from nltk.corpus import stopwords
    text = x
    compileddoc = sent_tokenize(text)
    stopwords = set(stopwords.words('english'))
    exclude = set(string.punctuation)
    return compileddoc, stopwords, exclude


def pdf_to_text(x):
    doc = x
    global pdfFileObj
    pdfFileObj = open(doc, 'rb')
    pdfReader = pdf.PdfFileReader(pdfFileObj)
    num_pages = pdfReader.numPages
    global text
    text = ''
    for i in range(11, 20):
        p = pdfReader.getPage(i)
        text += p.extractText()

    if text != "":
        text = text
    else:
        text = tt.process(fileurl, method='tesseract', language='eng')
    # text Cleaning
    text = text.replace("\n", " ")
    return text


def topic_modelling(x):
    doc = x
    global text
    text = pdf_to_text(doc)
    # Topic Identification using LDA
    compileddoc, stopwords, exclude = text_pre_processing(text)

    lemma = WordNetLemmatizer()

    def clean(document):
        stopwordremoval = " ".join([i for i in document.lower().split() if i not in stopwords])
        punctuationremoval = ''.join(ch for ch in stopwordremoval if ch not in exclude)
        normalized = " ".join(lemma.lemmatize(word) for word in punctuationremoval.split())
        return normalized

    final_doc = [clean(document).split() for document in compileddoc]

    dictionary = corpora.Dictionary(final_doc)

    DT_matrix = [dictionary.doc2bow(doc) for doc in final_doc]

    Lda_object = gensim.models.ldamodel.LdaModel

    numberoftopics = 9

    lda_model_1 = Lda_object(DT_matrix, num_topics=numberoftopics, id2word=dictionary)

    print(lda_model_1.print_topics(num_topics=3, num_words=6))

    def convert_to_list(number_of_topics=2):
        topics = []
        number_of_topics
        for i in range(number_of_topics):
            s = lda_model_1.show_topic(topicid=i)
            for j in range(len(s)):
                # print(j)
                if s[j][0] not in stopwords:
                    topics.append(s[j][0])
        d = nltk.pos_tag(topics)
        topics_NN = []
        for i in range(len(d)):
            if d[i][1] == 'NN' and d[i][0] not in topics_NN:
                topics_NN.append(d[i][0])
        return topics_NN

    topics = convert_to_list(numberoftopics)

    return topics


def generate_question_answer(x1, x2):
    selected_topic = x1
    Sentences_of_topic = []
    doc = x2
    text = pdf_to_text(doc)
    compileddoc, stopwords, exclude = text_pre_processing(text)

    for i in range(len(compileddoc)):
        if selected_topic in compileddoc[i].lower():
            Sentences_of_topic.append(compileddoc[i])

    s = ' '.join(Sentences_of_topic).lower()
    tokenized = word_tokenize(s)

    def before_after_of_selected(tokenized):
        tokenized
        before = []
        after = []
        for i in range(len(tokenized)):
            if tokenized[i] == selected_topic:
                if tokenized[i - 1].lower() not in stopwords and tokenized[i - 1] not in exclude and tokenized[
                    i - 1] not in before:
                    before.append(tokenized[i - 1])
                if tokenized[i + 1].lower() not in stopwords and tokenized[i + 1] not in exclude and tokenized[
                    i + 1] not in after:
                    after.append(tokenized[i + 1])
                else:
                    continue
        return before, after

    before, after = before_after_of_selected(tokenized)
    print("Before: ", before)
    print("--------------------------")
    print("After: ", after)

    tagged = nltk.pos_tag(tokenized)
    tagged_dict = dict(tagged)
    pos_before = nltk.pos_tag(before)
    pos_after = nltk.pos_tag(after)

    Adj_Question_Template = ["From the text describe somethings about "]
    # Verb_Question_Template = ["According to article how is "]
    phrases = []
    for i in range(len(pos_before)):
        if pos_before[i][1] == 'NN' or pos_before[i][1] == 'JJ':
            p = pos_before[i][0] + ' ' + selected_topic
            phrases.append(p)
    for i in range(len(pos_after)):
        if pos_after[i][1] == 'NN' or pos_after[i][1] == 'JJ':
            p = selected_topic + ' ' + pos_after[i][0]
            phrases.append(p)
    Questions = ['All Questions']
    for i in phrases:
        Questions.append(Adj_Question_Template[0] + ' ' + i + '?')
    print(Questions)
    # Question = Adj_Question_Template[0]+phrases[0]+"?"
    Answer = ' '.join(Sentences_of_topic)
    return Questions, Answer, phrases


def generate_relevant_answer(x1, x2, x3):
    sq = x1
    Answer = x2
    phrases = x3
    relevant_Answer = []
    compileddoc, stopwords, exclude = text_pre_processing(text)
    found_index = 0
    if sq not in 'All Questions':
        for i in range(len(phrases)):
            if phrases[i] in sq:
                found_index = i

    for i in range(len(compileddoc)):
        if found_index == 0:
            return Answer
        elif phrases[found_index] in compileddoc[i].lower():
            relevant_Answer.append(compileddoc[i])

    print(relevant_Answer)
    ans = ' '.join(relevant_Answer)
    return ans


# The summarization of the words

def summary_of_selected(text_input):
    from nltk.corpus import stopwords
    Stopwords = set(stopwords.words('english'))
    wordlemmatizer = WordNetLemmatizer()
    print("Inside function -------- assigned ", len(text_input))

    def lemmatize_words(words):
        print("Words are ", len(words))
        print(words)
        lemmatized_words = []
        for word in words:
            # print(word)
            lemmatized_words.append(wordlemmatizer.lemmatize(word))
        return lemmatized_words

    def stem_words(words):
        stemmed_words = []
        for word in words:
            stemmed_words.append(stemmer.stem(word))
        return stemmed_words

    def remove_special_characters(text_input):
        regex = r'[^a-zA-Z0-9\s]'
        text_input = re.sub(regex, '', text_input)
        return text_input

    def freq(words):
        words = [word.lower() for word in words]
        dict_freq = {}
        words_unique = []
        for word in words:
            if word not in words_unique:
                words_unique.append(word)
        for word in words_unique:
            dict_freq[word] = words.count(word)
        return dict_freq

    def pos_tagging(text_input):
        pos_tag = nltk.pos_tag(text_input.split())
        pos_tagged_noun_verb = []
        for word, tag in pos_tag:
            if tag == "NN" or tag == "NNP" or tag == "NNS" or tag == "VB" or tag == "VBD" or tag == "VBG" or tag == "VBN" or tag == "VBP" or tag == "VBZ":
                pos_tagged_noun_verb.append(word)
        return pos_tagged_noun_verb

    def tf_score(word, sentence):
        freq_sum = 0
        word_frequency_in_sentence = 0
        len_sentence = len(sentence)
        for word_in_sentence in sentence.split():
            if word == word_in_sentence:
                word_frequency_in_sentence = word_frequency_in_sentence + 1
        tf = word_frequency_in_sentence / len_sentence
        return tf

    def idf_score(no_of_sentences, word, sentences):
        no_of_sentence_containing_word = 0
        for sentence in sentences:
            sentence = remove_special_characters(str(sentence))
            sentence = re.sub(r'\d+', '', sentence)
            sentence = sentence.split()
            sentence = [word for word in sentence if word.lower() not in Stopwords and len(word) > 1]
            sentence = [word.lower() for word in sentence]
            sentence = [wordlemmatizer.lemmatize(word) for word in sentence]
            if word in sentence:
                no_of_sentence_containing_word = no_of_sentence_containing_word + 1
        idf = math.log10(no_of_sentences / no_of_sentence_containing_word)
        return idf

    def tf_idf_score(tf, idf):
        return tf * idf

    def word_tfidf(dict_freq, word, sentences, sentence):
        word_tfidf = []
        tf = tf_score(word, sentence)
        idf = idf_score(len(sentences), word, sentences)
        tf_idf = tf_idf_score(tf, idf)
        return tf_idf

    def sentence_importance(sentence, dict_freq, sentences):
        sentence_score = 0
        sentence = remove_special_characters(str(sentence))
        sentence = re.sub(r'\d+', '', sentence)
        pos_tagged_sentence = []
        no_of_sentences = len(sentences)
        pos_tagged_sentence = pos_tagging(sentence)
        for word in pos_tagged_sentence:
            if word.lower() not in Stopwords and word not in Stopwords and len(word) > 1:
                word = word.lower()
                word = wordlemmatizer.lemmatize(word)
                sentence_score = sentence_score + word_tfidf(dict_freq, word, sentences, sentence)
        return sentence_score

    tokenized_sentence = sent_tokenize(text_input)
    text_input = remove_special_characters(str(text_input))
    tokenized_words_with_stopwords = word_tokenize(text_input)
    tokenized_words = [word for word in tokenized_words_with_stopwords if word not in Stopwords]
    tokenized_words = [word for word in tokenized_words if len(word) > 1]
    tokenized_words = [word.lower() for word in tokenized_words]
    print("-------- tokenized_words are ", len(tokenized_words))
    tokenized_words = lemmatize_words(tokenized_words)
    word_freq = freq(tokenized_words)
    input_user = 3
    no_of_sentences = int((input_user * len(tokenized_sentence)) / 15)
    print(tokenized_sentence)
    print("This is in summarization +++++++######*****", no_of_sentences)
    c = 1
    sentence_with_importance = {}
    for sent in tokenized_sentence:
        sentenceimp = sentence_importance(sent, word_freq, tokenized_sentence)
        sentence_with_importance[c] = sentenceimp
        c = c + 1
    sentence_with_importance = sorted(sentence_with_importance.items(), key=operator.itemgetter(1), reverse=True)
    cnt = 0
    summary = []
    sentence_no = []

    for word_prob in sentence_with_importance:
        if cnt < no_of_sentences:
            sentence_no.append(word_prob[0])
            cnt = cnt + 1
        else:
            break
    print(sentence_with_importance)
    sentence_no.sort()
    cnt = 1
    for sentence in tokenized_sentence:
        if cnt in sentence_no:
            summary.append(sentence)
        cnt = cnt + 1

    summary = " ".join(summary)
    print("\n")
    print(summary)
    return summary


def welcome(request):
    return render(request, 'text/welcome.html')


def reload(request):
    if request.method == 'POST':
        doc = request.POST['doc']
        topics = request.POST['topics']
        Questions = request.POST['Questions']
        ans = request.POST['ans']
        summarized_answer = request.POST['summarized_answer']

    return render(request, 'text/welcome.html')
