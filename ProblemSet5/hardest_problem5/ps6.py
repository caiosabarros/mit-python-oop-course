import string

### DO NOT MODIFY THIS FUNCTION ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print('Loading word list from file...')
    # inFile: file
    in_file = open(file_name, 'r')
    # line: string
    line = in_file.readline()
    # word_list: list of strings
    word_list = line.split()
    print('  ', len(word_list), 'words loaded.')
    in_file.close()
    return word_list

### DO NOT MODIFY THIS FUNCTION ###
def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

### DO NOT MODIFY THIS FUNCTION ###
def get_story_string():
    """
    Returns: a joke in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    ### DO NOT MODIFY THIS METHOD ###
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    ### DO NOT MODIFY THIS METHOD ###
    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    ### DO NOT MODIFY THIS METHOD ###
    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class
        
        Returns: a COPY of self.valid_words
        '''
        return self.valid_words[:]
        
    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        lower = list(string.ascii_lowercase) + list(string.ascii_lowercase)
        upper = list(string.ascii_uppercase) + list(string.ascii_uppercase)

        mappingLower = {}
        for letter in lower:
            mappingLower[letter] = lower[lower.index(letter)+shift]
            if letter == 'z':
                break
        mappingUpper = {}
        for letter in upper:
            mappingUpper[letter] = upper[upper.index(letter)+shift]
            if letter == 'Z':
                break
                
        final_answer = {**mappingLower, **mappingUpper}
        return final_answer

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        ciphermessage = ""
        shifted_letters = self.build_shift_dict(shift)
        for letter in self.message_text:
            ciphermessage = ciphermessage + shifted_letters.get(letter,letter)
        return ciphermessage
            


class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encrypting_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        Hint: consider using the parent class constructor so less 
        code is repeated
        '''
        self.shift = shift
        self.text = Message(text)

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift
    def get_encrypting_dict(self):
        '''
        Used to safely access a copy self.encrypting_dict outside of the class
        
        Returns: a COPY of self.encrypting_dict
        '''
        self.encrypting_dict = self.text.build_shift_dict(self.shift)
        return self.encrypting_dict.copy()

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        self.message_text_encrypted = self.text.apply_shift(self.shift)
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift (ie. self.encrypting_dict and 
        message_text_encrypted).
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.shift = shift

class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text =  Message(text) 
        self.valid_words = load_words(WORDLIST_FILENAME)

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are  equally good such that they all create 
        the maximum number of you may choose any of those shifts (and their
        corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        #Count = how many words of the English language are in the decrypted message for a specific shift

        #Creates a tuple who will indicate a count number, the shift number and the decrypted message.
        indicators = ()

        #To each shift, add the message to the tuple and a counter, who will help us.
        for number in range(0,26):
            count = 0
            mensagem = self.message_text.apply_shift(number)
            mensagem_copy = mensagem.split(" ")
            for word in mensagem_copy:
                if is_word(self.valid_words, word):
                    count = count + 1
                else:
                    pass
            indicators = indicators + (count, number, mensagem)

        #This array shows how many of the words in each shift actually are in the English language.
        array = []
        for i in range(0,78,3):
            counters = indicators[i]
            array.append(counters)
        array.sort()

        #After sorting, better shows how many words are in the English language for the best shift
        better = array[-1]
        
        #Create an array that gets the indexes multiple of three 
        important_array = []
        for i in range(0,len(indicators),3):
            important_array.append(i)

        #Find the index from which the count is the greatest. It needs to be a multiple of three
        starting = 0
        for i in important_array:      
            if indicators.index(better, starting) in important_array:
                correct_index = indicators.index(better,starting) 
            elif starting <= len(indicators):
                starting = starting + 3    

        #Gets the shift and the decrypted message which are found right after the best count index.
        (x,y) = (indicators[correct_index+1],indicators[correct_index+2])
        return (x,y)

    def decrypt_story():
        '''
        This functions decrypts the message stored in the file story.txt
        using the helper functions
        '''
        ciphertext_story = CiphertextMessage(get_story_string())
        return ciphertext_story.decrypt_message()


#Example test case (PlaintextMessage)
plaintext = PlaintextMessage('hello', 2)
print('Expected Output: jgnnq')
print('Actual Output:', plaintext.get_message_text_encrypted())
    
#Example test case (CiphertextMessage)
ciphertext = CiphertextMessage('jgnnq')
print('Expected Output:', (24, 'hello'))
print('Actual Output:', ciphertext.decrypt_message())

ciphertext1 = CiphertextMessage(get_story_string())
print('Actual Output:', ciphertext1.decrypt_message())