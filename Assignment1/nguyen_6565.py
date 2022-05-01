# Samson Nguyen
# 1001496565
# 6 February 2022
# CSE 4381 Assignment 1

import random

# 1. “Security is often important”
message = "Security is often important"


# rot-13 cypher
def rot13(msg):
    new_msg = ''
    # r0 = alphabet
    r0 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # r14 = alphabet rotated by 13
    r13 = 'NOPQRSTUVWXYZABCDEFGHIJKLM'
    # for each letter, if it is in the alphabet, rotate by 13
    for letter in msg:
        if not letter.isalpha():
            new_msg += letter
        elif letter.islower():
            new_msg += r13[r0.find(letter.upper())].lower()
        else:
            new_msg += r13[r0.find(letter)]
    return new_msg


# rot-N cypher
# given a message and N, do a rot-N encryption on message.
# if N not given, assume rot-13
def rot_n(msg, n=13):
    new_msg = ''
    r0 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    rn = r0[:]
    # rotate rn according to n
    if n >= 0:
        for i in range(n):
            rn = rn[1:] + rn[0]
    else:
        for i in range(0, abs(n)):
            rn = rn[-1] + rn[:-1]
    # for letter in message, replace with rot-N letter
    for letter in msg:
        if letter == ' ':
            new_msg += ' '
        elif letter.islower():
            new_msg += rn[r0.find(letter.upper())].lower()
        else:
            new_msg += rn[r0.find(letter)]
    return new_msg


print("\n--- PART 1 ---\n")
print("rot13")
print(rot13(message))
print(rot13(rot13(message)))
# print(rot_n(message, -6))
# print(rot_n(rot_n(message, -6), 6))
print("rot-N")
for n in range(27):
    print(rot_n(message, n), n)
    print(rot_n(message, -26 + n), -26 + n)

# 2. Letter by letter substitution cipher.
story = '''CHAPTER I

In the morning of life came a good fairy with her basket, and said:

     "Here are gifts. Take one, leave the others. And be wary, chose wisely; oh, choose wisely! for only one of them is valuable."

     The gifts were five: Fame, Love, Riches, Pleasure, Death. The youth said, eagerly:

     "There is no need to consider"; and he chose Pleasure.

     He went out into the world and sought out the pleasures that youth delights in. But each in its turn was short-lived and disappointing, vain and empty; and each, departing, mocked him. In the end he said: "These years I have wasted. If I could but choose again, I would choose wisely.

CHAPTER II

The fairy appeared, and said:

     "Four of the gifts remain. Choose once more; and oh, remember-time is flying, and only one of them is precious."

     The man considered long, then chose Love; and did not mark the tears that rose in the fairy's eyes.

     After many, many years the man sat by a coffin, in an empty home. And he communed with himself, saying: "One by one they have gone away and left me; and now she lies here, the dearest and the last. Desolation after desolation has swept over me; for each hour of happiness the treacherous trader, Love, as sold me I have paid a thousand hours of grief. Out of my heart of hearts I curse him."

CHAPTER III

"Choose again." It was the fairy speaking.

     "The years have taught you wisdom -- surely it must be so. Three gifts remain. Only one of them has any worth -- remember it, and choose warily."

     The man reflected long, then chose Fame; and the fairy, sighing, went her way.

     Years went by and she came again, and stood behind the man where he sat solitary in the fading day, thinking. And she knew his thought:

     "My name filled the world, and its praises were on every tongue, and it seemed well with me for a little while. How little a while it was! Then came envy; then detraction; then calumny; then hate; then persecution. Then derision, which is the beginning of the end. And last of all came pity, which is the funeral of fame. Oh, the bitterness and misery of renown! target for mud in its prime, for contempt and compassion in its decay."

CHAPTER IV

"Chose yet again." It was the fairy's voice.

     "Two gifts remain. And do not despair. In the beginning there was but one that was precious, and it is still here."

     "Wealth -- which is power! How blind I was!" said the man. "Now, at last, life will be worth the living. I will spend, squander, dazzle. These mockers and despisers will crawl in the dirt before me, and I will feed my hungry heart with their envy. I will have all luxuries, all joys, all enchantments of the spirit, all contentments of the body that man holds dear. I will buy, buy, buy! deference, respect, esteem, worship -- every pinchbeck grace of life the market of a trivial world can furnish forth. I have lost much time, and chosen badly heretofore, but let that pass; I was ignorant then, and could but take for best what seemed so."

     Three short years went by, and a day came when the man sat shivering in a mean garret; and he was gaunt and wan and hollow-eyed, and clothed in rags; and he was gnawing a dry crust and mumbling:

     "Curse all the world's gifts, for mockeries and gilded lies! And miscalled, every one. They are not gifts, but merely lendings. Pleasure, Love, Fame, Riches: they are but temporary disguises for lasting realities -- Pain, Grief, Shame, Poverty. The fairy said true; in all her store there was but one gift which was precious, only one that was not valueless. How poor and cheap and mean I know those others now to be, compared with that inestimable one, that dear and sweet and kindly one, that steeps in dreamless and enduring sleep the pains that persecute the body, and the shames and griefs that eat the mind and heart. Bring it! I am weary, I would rest."

CHAPTER V

The fairy came, bringing again four of the gifts, but Death was wanting. She said:
     "I gave it to a mother's pet, a little child. It was ignorant, but trusted me, asking me to choose for it. You did not ask me to choose."

     "Oh, miserable me! What is left for me?"

     "What not even you have deserved: the wanton insult of Old Age."'''
key = 'XPBDCRJTQEGHZLFWOAYUISVKMN'


# given message and key, do substitution cypher
def substitution(msg, k):
    alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    new_msg = ''
    # for each letter in message,
    #   new_msg += value in key at the same index as letter in alpha
    for letter in msg:
        if letter.upper() not in alpha:
            new_msg += letter
        elif letter.islower():
            new_msg += k[alpha.find(letter.upper())].lower()
        else:
            new_msg += k[alpha.find(letter)]
    return new_msg


print("\n--- PART 2 ---\n")
print(substitution(story, key))


# 3. Show letter frequencies for the plaintext

# count letter frequencies in msg
def letter_frequencies(msg):
    alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    total_letters = 0
    frequencies = {'A': 0}
    for letter in alpha:
        count = msg.count(letter) + msg.count(letter.lower())
        frequencies[letter] = count
        total_letters += count
    return frequencies


print("\n--- PART 3 ---\n")
print(letter_frequencies(story))

# 4. Homophonic substitution
# Define a cypher key that has multiple values per letter.
# Each letter in the alphabet will have a unique set of replacements.
# More frequently appearing letters have more possible replacements so it's harder to detect a pattern.
homophonic_key = {
    'A': ['38', '18'],
    'B': ['01'],
    'C': ['07'],
    'D': ['40'],
    'E': ['21', '09', '19', '33'],
    'F': ['37'],
    'G': ['29'],
    'H': ['11', '23'],
    'I': ['05', '30'],
    'J': ['15'],
    'K': ['02'],
    'L': ['22'],
    'M': ['35'],
    'N': ['20', '13'],
    'O': ['38'],
    'P': ['16'],
    'Q': ['25'],
    'R': ['24'],
    'S': ['10', '31'],
    'T': ['12', '28'],
    'U': ['03'],
    'V': ['32'],
    'W': ['08'],
    'X': ['26'],
    'Y': ['27'],
    'Z': ['36']
}


# given message and key, do homophonic cypher
def homophonic_cypher(msg, key):
    new_msg = ''
    for letter in msg:
        if not letter.isalpha():
            new_msg += letter
        else:
            new_msg += random.choice(key[letter.upper()])
    return new_msg


print("\n--- PART 4 ---\n")
print(homophonic_cypher(story, homophonic_key))

# 5. How would you use part 3 (above) to crack a cypher?
'''By knowing the statistically average letter frequencies for the language a cypher is written in
    as well as the letter frequencies in the encrypted message, I can replace the letters in the
    encrypted message with the ones in the alphabet with similar frequencies. For example, I know
    the most frequently appearing letter is probably E if the message is in English.'''
