import praw
import re
import nltk
import os
nltk.download('cmudict')

reddit = praw.Reddit(client_id=os.environ['CLIENT_ID'],
                     client_secret=os.environ['CLIENT_SECRET'],
                     username=os.environ['USERNAME'],
                     password=os.environ['PASSWORD'],
                     user_agent=os.environ['USER_AGENT'],)


def get_phonemes(word):
    entries = nltk.corpus.cmudict.entries()
    for entry in entries:
        if entry[0] == word.lower():
            return entry[1]
    return None


def do_words_rhyme(word1, word2):
    if word1.lower() == word2.lower():
        return False
    phonemes1 = get_phonemes(word1)
    phonemes2 = get_phonemes(word2)
    return phonemes1 and phonemes2 and phonemes1[-2:] == phonemes2[-2:]


subreddit = reddit.subreddit('funny')

output_file = open('poem-output.txt', 'a')

commentsRhymed = 0

for comment in subreddit.stream.comments(skip_existing=True):
    sentences = re.split(r'[.!?]+', comment.body.strip())
    if len(sentences) == 2:
        words1 = sentences[0].split()
        words2 = sentences[1].split()
        if len(words1) > 0 and len(words2) > 0 and do_words_rhyme(words1[-1], words2[-1]):
            if commentsRhymed < 10:
                print(comment.body)
                output_file.write(comment.body + '\n')
                commentsRhymed = commentsRhymed + 1

output_file.close()