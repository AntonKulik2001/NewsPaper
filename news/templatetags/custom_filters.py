import string

from django import template

register = template.Library()

BAD_WORDS = ['сука','тварь','пидорас','говно','блять','гандон',]

@register.filter()
def censor(text):
    text_list = text.split()
    censored_list = []

    for word in text_list:
        clean_word = ''.join(c for c in word if c not in string.punctuation)
        if clean_word.lower() in BAD_WORDS:
            censored_word = clean_word[0] + (len(clean_word) - 1) * '*'
            censored_list.append(word.replace(clean_word, censored_word))
        else:
            censored_list.append(word)
    return ' '.join(censored_list)