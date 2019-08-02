import random_words
import random

rw= random_words.RandomWords()
word=rw.random_word()

print(word)

ans = random.randint(0 , len(word)-1 )
print(ans)

print(word[0:ans] , "_" , word[ans+1 : len(word)] )
playerAnswer = input("please answer: ")

ans1 = word[ans]
if playerAnswer == ans1:
    print( "Correct." )
else:
    print("Wrong.")
