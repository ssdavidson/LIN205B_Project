import sys, io, csv
import pickle
import spacy
from matplotlib import pyplot

#load corpus CSV file
corpus = io.open('CORPUS_050718.csv', encoding = 'utf-8')

#load Spacy Spanish model
nlp =  spacy.load('es_core_news_md')

#load previously saved dependency parsed essays
essays_famous = pickle.load(open('essays_famous_parsed.pickle', 'rb'))
essays_vacation = pickle.load(open('essays_vacation_parsed.pickle', 'rb'))

#dict to keep track of scores
scores = dict()
scores_famous = dict()
scores_vacation = dict()

#essay lists contain tuples (student_level, spacy_document_object)
for essay in essays_famous:
  essay_text = essay[1]
  level = essay[0]
  max_dist_list = list() #list to keep max dep dist of each sentence
  num_sents = 0

  for sent in essay_text.sents: #sents from Spacy object
    max_dist = 0
    num_sents += 1 #iterate num sentences
    for word in sent:
      if word.pos_ != "PUNCT": #omit punctuation dependency lengths
        if abs(word.i - word.head.i) > max_dist: #calc current dep dist and compare to max so far
          max_dist = abs(word.i - word.head.i) #update max if current is greater
    max_dist_list.append(max_dist) #add max dep for sent to the list for essay

  avg_max_dist = sum(max_dist_list) / float(num_sents) #average max dep for the essay

  if level not in scores_famous: #prevent key error
    scores_famous[level] = list()

  scores_famous[level].append(avg_max_dist) #add avg max dep for essay to list for appropriate level


for essay in essays_vacation: #see comments above
  max_dist = 0
  essay_text = essay[1]
  level = essay[0]
  max_dist_list = list()
  num_sents = 0

  for sent in essay_text.sents:
    max_dist = 0
    num_sents += 1
    for word in sent:
      if word.pos_ != "PUNCT":
        if abs(word.i - word.head.i) > max_dist:
          max_dist = abs(word.i - word.head.i)
    max_dist_list.append(max_dist)

  avg_max_dist = sum(max_dist_list) / float(num_sents)

  if level not in scores_vacation:
    scores_vacation[level] = list()

  scores_vacation[level].append(avg_max_dist)


scores_all = {**scores_famous, **scores_vacation} #combine famous and vacation to create dict for all essays

levels = scores_all.keys()

essays_avg = dict() #key is level, value is overall average max dep dist for that level
famous_avg = dict()
vacation_avg = dict()

for level in levels: #calculate overall avg max dep dist for the levels
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
pyplot.title("Maximum Dependency Length by Course")
pyplot.ylabel("Maximum Dependency Length")
pyplot.xlabel("Course Number")
pyplot.plot(y, x, 'bo-') #this is a scatterplat, using green(g) triangles(^)
pyplot.plot(z, w, 'r+-')
#pyplot.plot(y, a, 'bo-', label = "Famous prompt") #this is a scatterplat, using green(g) triangles(^)
#pyplot.plot(y, c, 'r+-', label = "Vacation prompt")
#pyplot.plot(z, b, 'bo-')
#pyplot.plot(z, d, 'r+-')
pyplot.legend()
pyplot.show() #display graph
