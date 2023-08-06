from random import choices, randint
import vocab

vocabulary = vocab.vocab
    
def phrase(length = randint(2,5)):
    return ' '.join(choices(vocabulary,k=length))
    
def slogan(length = randint(3,10)):
    return ' '.join(choices(vocabulary,k=length))
    
def sentence(length = randint(2,20)):
    sen = ' '.join(choices(vocabulary,k=length))+"."
    sen = sen[0].upper()+sen[1:]
    return sen
    
def paragraph(size = randint(4,10)):
    return '  '.join([sentence() for i in range(size)])
    
def article(size = randint(7,100)):
    title = phrase()+"\n\n"
    return title + "\n\n".join([paragraph for i in range(size)])
    
if __name__ == "__main__":
    print(paragraph())