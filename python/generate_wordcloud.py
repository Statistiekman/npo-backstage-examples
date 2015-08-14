import codecs
import glob
import math
import os
import pkg_resources
import re
import sys

# Check if the nltk and weighwords dependencies are installed
dependencies = ['nltk', 'weighwords']
try:
    pkg_resources.require(dependencies)
except pkg_resources.DistributionNotFound:
    sys.exit(
        'generate_wordcloud.py requires two extra dependencies: nltk and '
        'weighwords. These might take some time to install (weighwords also'
        'depends on numpy)\nPlease install them, e.g.: '
        'sudo pip install nltk weighwords')

from weighwords import ParsimoniousLM
import nltk

# This program will generate a wordcloud for each of the specified
# programs. To achieve this we use Parsimonious Language Models, which
# can will find the most distinctive words for each supplied body of
# text when comparing them to each other. It uses NLTK to tokenize the
# text. The results are printed on screen and saved to files.

data_dir = 'npo_backstage_subtitles/'

# The programs for which we have downloaded subtitles and will generate
# worldclouds
programs = ['EenVandaag', 'Nieuwsuur']

# Number of most distinctive words for each program
top_words = 100

# This list will store a tuple for each program containing its title and
# a list of all its words.
# E.g., [('EenVandaag'), ['all', 'words']), ('Nieuwsuur', ['words'])].
documents = []

# The weight parameter used to create the Parsimonious Language Models.
# The lower the weight the distinctive words will be selected, but a
# too low weight will select words which are only used once in a text
# resulting in a bad characterization of the text. So play around with
# this value.
weight = 0.01

for program in programs:
    print 'Loading data for: %s' % (program)

    # Store all words for this program in this list
    words = []

    program_dir = data_dir + program

    if not os.path.exists(program_dir):
        sys.exit(
            'Subtitle directory does not exist: %s\nRun '
            'download_filtered_subtitles.py first\n' % (program_dir)
        )

    loaded_documents_count = 0
    for filename in glob.glob('%s/*.srt' % (program_dir)):
        with codecs.open(filename, 'r', 'utf-8') as IN:
            subtitle = IN.readlines()
        # Use only the text line and filter out the metadata lines
        # containing timestamps etc.
        subtitle = subtitle[4::4]
        # Tokenize the text using NLTK
        tokens = nltk.tokenize.word_tokenize(
            ' '.join(subtitle),
            language='dutch'
        )
        # Change all characters to lowercase
        tokens = [i.lower() for i in tokens]
        for token in [token for token in tokens if re.match('\w+', token)]:
            words.append(token)

        loaded_documents_count += 1

    print 'Loaded %d documents\n' % (loaded_documents_count)
    # Add the list with all collected words for this program to
    # documents
    documents.append((program, words))

# Create the Parsimonious Language Model for the documents
model = ParsimoniousLM([words for program, words in documents], w=weight)
for program, words in documents:
    print "\nTop %d words for %s:" % (top_words, program)
    with codecs.open('wordcloud_%s.txt' % (program), 'w', 'utf-8') as OUT:
        # Generate the top words for a program
        for word, score in model.top(top_words, words):
            result_line = "%s:%.6f" % (word, math.exp(score))
            print result_line
            OUT.write('%s\n' % (result_line))
