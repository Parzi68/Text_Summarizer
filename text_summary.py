from cgitb import text
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import  punctuation
from heapq import nlargest
# text="""One-Piece is a Japanese manga series written and illustrated by Eiichiro Oda. It has been serialized in Shueisha's shōnen manga magazine Weekly Shōnen Jump since July 1997, with its individual chapters compiled into 103 tankōbon volumes as of August 2022. The story follows the adventures of Monkey D. Luffy, a boy whose body gained the properties of rubber after unintentionally eating a Devil Fruit. With his pirate crew, the Straw Hat Pirates, Luffy explores the Grand Line in search of the deceased King of the Pirates Gol D. Roger's ultimate treasure known as the "One Piece" in order to become the next King of the Pirates.

# The manga spawned a media franchise, having been adapted into a festival film produced by Production I.G, and an anime series produced by Toei Animation, which began broadcasting in Japan in 1999. Additionally, Toei has developed fourteen animated feature films, one original video animation, and thirteen television specials. Several companies have developed various types of merchandising and media, such as a trading card game and numerous video games. The manga series was licensed for an English language release in North America and the United Kingdom by Viz Media and in Australia by Madman Entertainment. The anime series was licensed by 4Kids Entertainment for an English-language release in North America in 2004, before the license was dropped and subsequently acquired by Funimation in 2007.

# One Piece has received praise for its storytelling, art, characterization, and humor. It has received many awards and is ranked by critics, reviewers, and readers as one of the best manga of all time. Several volumes of the manga have broken publishing records, including the highest initial print run of any book in Japan. In 2015 and 2022, One Piece set the Guinness World Record for "the most copies published for the same comic book series by a single author". It was the best-selling manga for eleven consecutive years from 2008 to 2018, and is the only manga that had an initial print of volumes of above 3 million continuously for more than 10 years, as well as the only that had achieved more than 1 million copies sold in all of its over 100 published tankōbon volumes. One Piece is the only manga whose volumes have ranked first every year in Oricon's weekly comic chart existence since 2008."""

def summarizer(rawdocs):
    #printing lists of stop_words(not important words) 
    stopwords = list(STOP_WORDS)
    #print(stopwords)

    #loading spaCy library's module
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(rawdocs)
    #print(doc)

    #considering every words and punctuations as a token in text
    tokens = [token.text for token in doc]
    #print(tokens)

    #counting every word tokens in text and storing them in word_freq dictionary
    word_freq = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text] = 1
            else:
                word_freq[word.text] += 1
    #print(word_freq)

    #Maximum number of words used in text
    max_freq = max(word_freq.values())
    #print(max_freq)

    #average frequency of each word tokens
    for word in word_freq.keys():
        word_freq[word] = word_freq[word]/max_freq
    #print(word_freq)

    sent_tokens = [sent for sent in doc.sents]
    #print(sent_tokens)

    #counting word frequency in every sentence and putting it in sent_score dictionary 
    sent_scores={}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent] = word_freq[word.text]
                else:
                    sent_scores[sent] += word_freq[word.text]
    #print(sent_scores)

    #Selecting length of summary
    select_len = int(len(sent_tokens) * 0.3)
    #print(select_len)

    #prints sentences with highest frequency with the selectedd number of length given as a list
    summary = nlargest(select_len, sent_scores, key=sent_scores.get)
    #print(summary)

    #prints summary as a text
    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)
    # print(text)
    # print(summary)
    # print("Length of Original Text",len(text.split(' ')))
    # print("Length of Summary",len(summary.split(' ')))

    return summary, doc, len(rawdocs.split(' ')), len(summary.split(' '))