import sys, io, csv
import pickle
import spacy
from matplotlib import pyplot
import numpy

#load corpus CSV file
corpus = io.open('CORPUS_050718.csv', encoding = 'utf-8')

#load Spacy Spanish models
nlp =  spacy.load('es_core_news_md')

#load dependency parsed essays from Pickle
essays_famous = pickle.load(open('essays_famous_parsed.pickle', 'rb'))
essays_vacation = pickle.load(open('essays_vacation_parsed.pickle', 'rb'))

scores = dict() #dict to track sent len by level
scores_famous = dict()
scores_vacation = dict()

#essay lists contain tuples (student_level, spacy_document_object)
for essay in essays_famous:
  essay_text = essay[1]
  level = essay[0]
  sent_len_list = list() #list to keep sent len for each sent in essay
  num_sents = 0

  for sent in essay_text.sents: #dep parsed essay text from Spacy object
    sent_len = 0
    num_sents += 1 #iterate number of sentences
    for word in sent:
      sent_len += 1 #iterate number of words in sent
    sent_len_list.append(sent_len) #add sent len to list for essay

  avg_sent_len = sum(sent_len_list) / float(num_sents) #calc avg sent len for essay

  if level not in scores_famous: #prevent key error
    scores_famous[level] = list()

  scores_famous[level].append(avg_sent_len) #add sent len for essay to list for approp level


for essay in essays_vacation: #see comments above
  essay_text = essay[1]
  level = essay[0]
  sent_len_list = list()
  num_sents = 0

  for sent in essay_text.sents:
    sent_len = 0
    num_sents += 1
    for word in sent:
      sent_len += 1
    sent_len_list.append(sent_len)

  avg_sent_len = sum(sent_len_list) / float(num_sents)

  if level not in scores_vacation:
    scores_vacation[level] = list()

  scores_vacation[level].append(avg_sent_len)


scores_all = {**scores_famous, **scores_vacation} #combine two essay score dicts to create a single dict for corpus

levels = scores_all.keys()

essays_avg = dict() #key is level, value is avg sent len
famous_avg = dict()
vacation_avg = dict()

for level in levels: #calculate averages for each level
    essays_avg[level] = sum(scores_all[level]) / len(scores_all[level])
    famous_avg[level] = sum(scores_famous[level]) / len(scores_famous[level])
    vacation_avg[level] = sum(scores_vacation[level]) / len(scores_vacation[level])

#create lists for graphing
x = [essays_avg[1],essays_avg[2],essays_avg[3],essays_avg[21],essays_avg[22],essays_avg[23],essays_avg[24]]
w = [essays_avg[31],essays_avg[32],essays_avg[33]]
a = [famous_avg[1],famous_avg[2],famous_avg[3],famous_avg[21],famous_avg[22],famous_avg[23],famous_avg[24]]
b = [famous_avg[31],famous_avg[32],famous_avg[33]]
c = [vacation_avg[1],vacation_avg[2],vacation_avg[3],vacation_avg[21],vacation_avg[22],vacation_avg[23],vacation_avg[24]]
d = [vacation_avg[31],vacation_avg[32],vacation_avg[33]]

#create labels
y = ["SPA1", "SPA2", "SPA3", "SPA21", "SPA22", "SPA23", "SPA24"]
z = ["SPA31","SPA32","SPA33"]

#graph it
pyplot.title("Average Sentence Length by Course")
pyplot.ylabel("Average Sentence Length")
pyplot.xlabel("Course Number")
#pyplot.plot(y, x, 'bo-') #this is a scatterplat, using green(g) triangles(^)
#pyplot.plot(z, w, 'r+-')
pyplot.plot(y, a, 'bo-', label = "Famous prompt") #this is a scatterplat, using green(g) triangles(^)
pyplot.plot(y, c, 'r+-', label = "Vacation prompt")
pyplot.plot(z, b, 'bo-')
pyplot.plot(z, d, 'r+-')
pyplot.legend()
pyplot.show() #display graph
