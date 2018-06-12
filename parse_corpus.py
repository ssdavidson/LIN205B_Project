#This script creates constitency trees using FreeLing parser and save to file

#@inproceedings{padro12,
#author="Lluís Padró and Evgeny Stanilovsky",
#title="FreeLing 3.0: Towards Wider Multilinguality",
#ooktitle="Proceedings of the Language Resources and Evaluation Conference (LREC 2012)",
#organization="ELRA",
#address="Istanbul, Turkey",
#year="2012",
#month="May"}

import freeling
import sys
import string
import pickle
from student_class import Student #student class definition
import io, csv
from io import StringIO

#list to hold essays by prompt
essays_vacation = list()
essays_famous = list()

#list to hold essays by prompt once constituency parsed
essays_vacation_parsed = list()
essays_famous_parsed = list()

## -----------------------------------------------
## Print consituency trees
## Redirect to string; print and return
## Code from: https://talp-upc.gitbooks.io/freeling-tutorial/content/code/example03.py.html
## -----------------------------------------------
def ProcessSentences(ls):
    result_list = list() #list to keep parsed sentences for essay
    old_stdout = sys.stdout #save stdout location before redirect
    result = StringIO() #create redirect object

    sys.stdout = result #redirect stdout
    # for each sentence in list
    for s in ls :
        # for each word in sentence
        printTree(s.get_parse_tree(), 0) #print constitency tree
        print()
#        printDepTree(s.get_dep_tree(), 0)
#        print()
#        for w in s :
#            if w.get_lemma() not in string.punctuation:
#                word_tuple = (w.get_form().lower(), w.get_lemma(), w.get_tag())
#                result_list.append(word_tuple)
        # sentence separator
    sys.stdout = old_stdout #restore stdout
    print(result.getvalue())
    return result.getvalue() #return string containing parse trees


## -----------------------------------------------
## Set desired options for morphological analyzer
## -----------------------------------------------
def my_maco_options(lang,lpath) :

    # create options holder
    opt = freeling.maco_options(lang);

    # Provide files for morphological submodules. Note that it is not
    # necessary to set file for modules that will not be used.
    opt.UserMapFile = "";
    opt.LocutionsFile = lpath + "locucions.dat";
    opt.AffixFile = lpath + "afixos.dat";
    opt.ProbabilityFile = lpath + "probabilitats.dat";
    opt.DictionaryFile = lpath + "dicc.src";
    opt.NPdataFile = lpath + "np.dat";
    opt.PunctuationFile = lpath + "../common/punct.dat";
    return opt;

## ------------  output a parse tree ------------
def printTree(ptree, depth):

    node = ptree.begin();

    print(''.rjust(depth*2),end='');
    info = node.get_info();
    if (info.is_head()): print('+',end='');

    nch = node.num_children();
    if (nch == 0) :
        w = info.get_word();
        print ('({0} {1} {2})'.format(w.get_form(), w.get_lemma(), w.get_tag()),end='');

    else :
        print('{0}_['.format(info.get_label()));

        for i in range(nch) :
            child = node.nth_child_ref(i);
            printTree(child, depth+1);

        print(''.rjust(depth*2),end='');
        print(']',end='');

    print('');

## ------------  output a parse tree ------------
def printDepTree(dtree, depth):

    node = dtree.begin()

    print(''.rjust(depth*2),end='');

    info = node.get_info();
    link = info.get_link();
    linfo = link.get_info();
    print ('{0}/{1}/'.format(link.get_info().get_label(), info.get_label()),end='');

    w = node.get_info().get_word();
    print ('({0} {1} {2})'.format(w.get_form(), w.get_lemma(), w.get_tag()),end='');

    nch = node.num_children();
    if (nch > 0) :
        print(' [');

        for i in range(nch) :
            d = node.nth_child_ref(i);
            if (not d.begin().get_info().is_chunk()) :
                printDepTree(d, depth+1);

        ch = {};
        for i in range(nch) :
            d = node.nth_child_ref(i);
            if (d.begin().get_info().is_chunk()) :
                ch[d.begin().get_info().get_chunk_ord()] = d;

        for i in sorted(ch.keys()) :
            printDepTree(ch[i], depth + 1);

        print(''.rjust(depth*2),end='');
        print(']',end='');

    print('');

## ----------------------------------------------
## -------------    MAIN PROGRAM  ---------------
## ----------------------------------------------

# set locale to an UTF8 compatible locale
freeling.util_init_locale("default");

# get requested language from arg1, or English if not provided
lang = "es"
if len(sys.argv)>1 : lang=sys.argv[1]

# get installation path to use from arg2, or use /usr/local if not provided
ipath = "/usr/local/Cellar/freeling/4.0_4";
if len(sys.argv)>2 : ipath=sys.argv[2]

# path to language data
lpath = ipath + "/share/freeling/" + lang + "/"

# create analyzers
tk=freeling.tokenizer(lpath+"tokenizer.dat");
sp=freeling.splitter(lpath+"splitter.dat");

# create the analyzer with the required set of maco_options
morfo=freeling.maco(my_maco_options(lang,lpath));
#  then, (de)activate required modules
morfo.set_active_options (False,  # UserMap
                          True,  # NumbersDetection,
                          True,  # PunctuationDetection,
                          True,  # DatesDetection,
                          True,  # DictionarySearch,
                          True,  # AffixAnalysis,
                          False, # CompoundAnalysis,
                          True,  # RetokContractions,
                          True,  # MultiwordsDetection,
                          True,  # NERecognition,
                          False, # QuantitiesDetection,
                          True); # ProbabilityAssignment

# create tagger
tagger = freeling.hmm_tagger(lpath+"tagger.dat",True,2)

#Process the student essay lists to create lists containing parsed essays
def process_list(student_list, prompt):
    for essay in student_list:
        # create tagger
        level = essay[0]
        text = essay[1]

        tagger = freeling.hmm_tagger(lpath+"tagger.dat",True,2)

        # create sense annotator
        sen = freeling.senses(lpath+"senses.dat");

        # create sense disambiguator
        wsd = freeling.ukb(lpath+"ukb.dat");

        # create dependency parser
        parser = freeling.chart_parser(lpath+"/chunker/grammar-chunk.dat");
        dep = freeling.dep_txala(lpath+"/dep_txala/dependences.dat", parser.get_start_symbol())

        # tokenize input line into a list of words
        lw = tk.tokenize(text)
        # split list of words in sentences, return list of sentences
        ls = sp.split(lw)

        # perform morphosyntactic analysis and disambiguation
        ls = morfo.analyze(ls)
        ls = tagger.analyze(ls)

        # annotate and disambiguate senses
        ls = sen.analyze(ls);
        ls = wsd.analyze(ls);
        # parse sentences
        ls = parser.analyze(ls);
        ls = dep.analyze(ls);

        # get the parsed essay text
        essay_parse = ProcessSentences(ls)

        #append tuple with level and parsed text to appropriate essay list
        if prompt == "V":
          essays_vacation_parsed.append((level, essay_parse))

        elif prompt == "F":
          essays_famous_parsed.append((level, essay_parse))

#Load and process the corpus CSV file
#Save tuples of (level, essay_text) to the appropriate essay list
with io.open('CORPUS_050718.csv', encoding = 'utf-8') as wb:
  csvreader = csv.reader(wb)
  for row in csvreader:
    if (row[16] != '' and row[16] != "S18_Famous"):
      if (row[3] != ''):
        text = row[16]
        level = int(row[3][4:])
        if len(text) >= 50:
          essays_famous.append((level, text))
    if (row[30] != '' and row[30] != "W18_Famous"):
      if (row[17] != ''):
        text = row[30]
        level = int(row[17][4:])
        if len(text) >= 50:
          essays_famous.append((level, text))
    if (row[31] != '' and row[31] != "W18_Vacation"):
      if (row[17] != ''):
        text = row[31]
        level = int(row[17][4:])
        if len(text) >= 50:
          essays_vacation.append((level,text))
    if (row[46] != '' and row[46] != "F17_Famous"):
      if (row[32] != ''):
        text = row[46]
        level = int(row[32][4:])
        if len(text) >= 50:
          essays_famous.append((level, text))
    if (row[47] != '' and row[47] != "F17_Vacation"):
      if (row[32] != ''):
        text = row[47]
        level = int(row[32][4:])
        if len(text) >= 50:
          essays_vacation.append((level,text))
    if (row[60] != '' and row[60] != "S17_Famous"):
      if (row[48] != ''):
        text = row[60]
        level = int(row[48][4:])
        if len(text) >= 50:
          essays_famous.append((level, text))
    if (row[61] != '' and row[61] != "S17_Vacation"):
      if (row[48] != ''):
        text = row[61]
        level = int(row[48][4:])
        if len(text) >= 50:
          essays_vacation.append((level,text))
    if (row[76] != '' and row[76] != "SU17_Famous"):
      if (row[62] != ''):
        text = row[76]
        level = int(row[62][4:])
        if len(text) >= 50:
          essays_famous.append((level, text))
    if (row[77] != '' and row[77] != "SU17_Vacation"):
      if (row[62] != ''):
        text = row[77]
        level = int(row[62][4:])
        if len(text) >= 50:
          essays_vacation.append((level,text))

#create the parsed essay lists
process_list(essays_vacation, "V")
process_list(essays_famous, "F")

#save the data sets to file for futher use
pickle.dump(essays_vacation, open('essays_vacation.pickle', 'wb'))
pickle.dump(essays_famous, open('essays_famous.pickle', 'wb'))
pickle.dump(essays_vacation_parsed, open('essays_vacation_parsed.pickle', 'wb'))
pickle.dump(essays_famous_parsed, open('essays_famous_parsed.pickle', 'wb'))
