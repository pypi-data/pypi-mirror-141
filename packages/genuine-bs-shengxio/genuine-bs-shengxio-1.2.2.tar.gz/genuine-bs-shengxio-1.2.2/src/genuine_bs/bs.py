from random import choices, randint
from genuine_bs import vocab

vocabulary = vocab.vocab

def rand_username(k = randint(3,10)):
    return ''.join(choices(vocabulary,k=k))

def rand_version(k = randint(2,10)):
    return '.'.join([str(randint(1,10)) for _ in range(k)])

def rand_url():
    return 'http://'+'.'.join(choices(vocabulary,k=2))+'.com'

def rand_ip():
    return '.'.join([str(randint(1,255)) for i in range(4)])

def rand_list(separator = ",",k = randint(2,10)):
    return f"[{separator.join(choices(vocabulary,k=k))}]"

def rand_words(k = randint(2,5)):
    return ' '.join(choices(vocabulary,k=k))
    
def rand_sentence(k = randint(2,20)):
    sen = ' '.join(choices(vocabulary,k=k))+"."
    sen = sen[0].upper()+sen[1:]
    return sen
    
def rand_paragraph(size = randint(4,10)):
    return '  '.join([rand_sentence() for _ in range(size)])
    
def rand_article(size = randint(7,100)):
    title = rand_words()+"\n\n"
    return title + "\n\n".join([rand_paragraph() for _ in range(size)])
    
if __name__ == "__main__":
    print(rand_username())
    print(rand_version())
    print(rand_url())
    print(rand_ip())
    print(rand_list())
    print(rand_words())
    print(rand_sentence())
    print(rand_paragraph())
    print(rand_article())