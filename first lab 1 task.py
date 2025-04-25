def word_count(text):
    words = text.split()
    word_dict = {}
    for word in words:
        word = word.lower()  # Перетворюємо слово в мале
        if word in word_dict:
            word_dict[word] += 1
        else:
            word_dict[word] = 1
    return word_dict

text = "this is a test text and this test is simple test text test texxxxt text text "
word_dict = word_count(text)

# Створюємо список слів, що зустрічаються більше ніж 3 рази
common_words = [word for word, count in word_dict.items() if count > 3]
print(common_words)