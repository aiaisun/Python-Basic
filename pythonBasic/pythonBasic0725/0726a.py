import random_words
import random

rw=random_words.RandomWords()
word=rw.random_word()
print(word)

wordN =random.randint(0, len(word)-1)
print(wordN)

ans = word[wordN]
print(ans)

print("Test: ", word[:wordN], "_", word[wordN+1: len(word)])

player = input("please answer: ")

if player == ans:
    print("yes")

else:
    print("Wrong.")
    print("Right answer is ", ans)
