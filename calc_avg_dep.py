import sys, io, csv
import pickle
import spacy
from matplotlib import pyplot

#load the CSV containing corpus data
corpus = io.open('CORPUS_050718.csv', encoding = 'utf-8')

#load Spacy Spanish model
nlp =  spacy.load('es_core_news_md')

essays_famous = [] #lists to hold essays by genre
essays_vacation = []

#load the CSV into csvreader
csvreader = csv.reader(corpus)

#iterate thru the rows of the corpus CSV
for row in csvreader:
  if (row[16] != '' and row[16] != "S18_Famous"):
    if (row[3] != ''):
      text = row[16]
      if len(text.split()) >= 50:
        essays_famous.append((int(row[3][4:]), nlp(text))) #for each essay, add to the correct list a tuple of level and text
  if (row[30] != '' and row[30] != "W18_Famous"):
    if (row[17] != ''):
      text = row[30]
      if len(text.split()) >= 50:
        essays_famous.append((int(row[17][4:]), nlp(text)))
  if (row[31] != '' and row[31] != "W18_Vacation"):
    if (row[17] != ''):
      text = row[31]
      if len(text.split()) >= 50:
        essays_vacation.append((int(row[17][4:]), nlp(text)))
  if (row[46] != '' and row[46] != "F17_Famous"):
    if (row[32] != ''):
      text = row[46]
      if len(text.split()) >= 50:
        essays_famous.append((int(row[32][4:]), nlp(text)))
  if (row[47] != '' and row[47] != "F17_Vacation"):
    if (row[32] != ''):
      text = row[47]
      if len(text.split()) >= 50:
        essays_vacation.append((int(row[32][4:]), nlp(text)))
  if (row[60] != '' and row[60] != "S17_Famous"):
    if (row[48] != ''):
      text = row[60]
      if len(text.split()) >= 50:
        essays_famous.append((int(row[48][4:]), nlp(text)))
  if (row[61] != '' and row[61] != "S17_Vacation"):
    if (row[48] != ''):
      text = row[61]
      if len(text.split()) >= 50:
        essays_vacation.append((int(row[48][4:]), nlp(text)))
  if (row[76] != '' and row[76] != "SU17_Famous"):
    if (row[62] != ''):
      text = row[76]
      if len(text.split()) >= 50:
        essays_famous.append((int(row[62][4:]), nlp(text)))
  if (row[77] != '' and row[77] != "SU17_Vacation"):
    if (row[62] != ''):
      text = row[77]
      if len(text.split()) >= 50:
        essays_vacation.append((int(row[62][4:]), nlp(text)))

pickle.dump(essays_famous, open('essays_famous_parsed.pickle', 'wb')) #dump the two essay lists to pickle for later use
pickle.dump(essays_vacation, open('essays_vacation_parsed.pickle', 'wb'))

scores = dict() #dict to track scores by level
scores_famous = dict()
scores_vacation = dict()

#essay lists contain tuples (student_level, spacy_document_object)
for essay in essays_famous:
  dist_count = 0 #total distance
  total = 0 #total words
  essay_text = essay[1]
  level = essay[0]

  for word in essay_text: #calc dep len for each word and add to total
    if word.pos_ != "PUNCT": #omit punctuation dependencies
      total += 1 #iterate the word count
      dist_count += abs(word.i - word.head.i) #add dep dist to the count

  avg_dep_dist = dist_count / total #calc avg dep distance

  if level not in scores_famous: #prevent key error
    scores_famous[level] = list()

  scores_famous[level].append(avg_dep_dist) #add avg dep dist to appropriate level score list


for essay in essays_vacation: #see comments above
  dist_count = 0
  total = 0
  essay_text = essay[1]
  level = essay[0]

  for word in essay_text:
    if word.pos_ != "PUNCT":
      total += 1
      dist_count += abs(word.i - word.head.i)

  avg_dep_dist = dist_count / total

  if level not in scores_vacation:
    scores_vacation[level] = list()

  scores_vacation[level].append(avg_dep_dist)

scores_all = {**scores_famous, **scores_vacation} #combine both lists to create list for all essays

levels = scores_all.keys()

essays_avg = dict() #key is level, value is avg dependency length for that level
famous_avg = dict()
vacation_avg = dict()

for level in levels: #calculate average dependency lengths for each level
    essays_avg[level] = sum(scores_all[level]) / len(scores_all[level])
    famous_avg[level] = sum(scores_famous[level]) / len(scores_famous[level])
    vacation_avg[level] = sum(scores_vacation[level]) / len(scores_vacation[level])

#create list for graphing
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
pyplot.title("Average Dependency Length by Course")
pyplot.ylabel("Average Dependency Length")
pyplot.xlabel("Course Number")
pyplot.plot(y, x, 'bo-') #this is a scatterplat, using green(g) triangles(^)
pyplot.plot(z, w, 'r+-')
#pyplot.plot(y, a, 'bo-', label = "Famous prompt") #this is a scatterplat, using green(g) triangles(^)
#pyplot.plot(y, c, 'r+-', label = "Vacation prompt")
#pyplot.plot(z, b, 'bo-')
#pyplot.plot(z, d, 'r+-')
pyplot.legend()
pyplot.show() #display graph
