##This script calculates the average dependency flux for each class level and graphs the result

import sys, io, csv
import pickle
import spacy
from matplotlib import pyplot

#Load CSV file containing corpus
corpus = io.open('CORPUS_050718.csv', encoding = 'utf-8')

#Load Spanish Spacy model
nlp =  spacy.load('es_core_news_md')

#Open dependency parsed essays
essays_famous = pickle.load(open('essays_famous_parsed.pickle', 'rb'))
essays_vacation = pickle.load(open('essays_vacation_parsed.pickle', 'rb'))

#Create dictionarys to retain flux scores by student class level
scores = dict()
scores_famous = dict()
scores_vacation = dict()

#essay lists contain tuples (student_level, spacy_document_object)
for essay in essays_famous:
  max_dist = 0
  essay_text = essay[1]
  level = essay[0]
  flux_list = list() #create list to keep flux score of each sentence
  num_sents = 0
  start_pos = 1 #increment to keep up with the appropriate index in Spacy

  for sent in essay_text.sents:
    num_words = 0
    num_sents += 1
    dep_spans = list() #list to keep track of dependency spans in each sentence
    tot_split = 0 #the total number of dependencies split in each sentence
    for word in sent:
      #if word.pos_ != "PUNCT":
      num_words += 1
      if not word.is_punct: #leave out punctuation so long final punc dependency is not included
        span = (word.head.i, word.i) # the span is a tuple if the head index and the word index
        dep_spans.append(span) #add each span to the spans list

    splits = range(start_pos, num_words + start_pos - 1) #the number of splits in each sentence

    for i in splits: #for each of the splits in the sentence
      split = 0 #keep track of how many dependency spans it splits
      for span in dep_spans: #for each span, check if it is split by one or more
        if (i <= span[0] and i > span[1]) or (i > span[0] and i <= span[1]):
          split += 1 #if split, add 1 to the split counter
      tot_split += split #add the count for that split to the total splits for the sentence

    if len(splits) > 0: #prevent div by 0
      flux = tot_split / len(splits) #get average for the sentence
      flux_list.append(flux) #add the average for the sentence to the essays list

    start_pos += num_words #update the starting position for the next sentence

  avg_flux = sum(flux_list) / float(num_sents) #calc the average flux for the essay

  if level not in scores_famous: #prevent key error
    scores_famous[level] = list()

  scores_famous[level].append(avg_flux) #add the average for essay to the score list for the level


for essay in essays_vacation: #see comments above
  max_dist = 0
  essay_text = essay[1]
  level = essay[0]
  flux_list = list()
  num_sents = 0
  start_pos = 1

  for sent in essay_text.sents:
    num_words = 0
    num_sents += 1
    dep_spans = list()
    tot_split = 0
    for word in sent:
      #if word.pos_ != "PUNCT":
      num_words += 1
      if not word.is_punct:
        # if word.i == word.head.i:
        #   continue
        span = (word.head.i, word.i)
        dep_spans.append(span)

    splits = range(start_pos, num_words + start_pos - 1)

    for i in splits:
      split = 0
      for span in dep_spans:
        if (i <= span[0] and i > span[1]) or (i > span[0] and i <= span[1]):
          split += 1
      tot_split += split

    if len(splits) > 0:
      flux = tot_split / len(splits)
      flux_list.append(flux)

    start_pos += num_words

  avg_flux = sum(flux_list) / float(num_sents)

  if level not in scores_vacation:
    scores_vacation[level] = list()

  scores_vacation[level].append(avg_flux)


scores_all = {**scores_famous, **scores_vacation} #combine the vacation and famous dicts to get the entire corpus

levels = scores_all.keys()

essays_avg = dict() #level is key, average score is value
famous_avg = dict()
vacation_avg = dict()

for level in levels: #calculate average flux score for each level
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
pyplot.title("Average Dependency Flux by Course")
pyplot.ylabel("Average Dependency Flux")
pyplot.xlabel("Course Number")
pyplot.plot(y, x, 'bo-') #this is a scatterplat, using green(g) triangles(^)
pyplot.plot(z, w, 'r+-')
#pyplot.plot(y, a, 'bo-', label = "Famous prompt") #this is a scatterplat, using green(g) triangles(^)
#pyplot.plot(y, c, 'r+-', label = "Vacation prompt")
#pyplot.plot(z, b, 'bo-')
#pyplot.plot(z, d, 'r+-')
#pyplot.legend()
pyplot.show() #display graph
