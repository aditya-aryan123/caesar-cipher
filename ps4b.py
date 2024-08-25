# Problem Set 4B
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string
import re

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

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
    word = re.sub('[^A-Za-z0-9]+', ' ', word)
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        word_list = load_words(WORDLIST_FILENAME)
        self.message_text = text
        self.valid_words = is_word(word_list, text)

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        return self.valid_words

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
        cipher_dict = {}

        upper_case = string.ascii_uppercase
        lower_case = string.ascii_lowercase

        for letter in upper_case:
            index = (ord(letter) - ord("A") + shift) % 26
            shifted_char = chr(ord("A") + index)
            cipher_dict[letter] = shifted_char

        for letter in lower_case:
            index = (ord(letter) - ord("a") + shift) % 26
            shifted_char = chr(ord("a") + index)
            cipher_dict[letter] = shifted_char

        return cipher_dict

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
        message = self.message_text
        text = ""
        shifted_characters = self.build_shift_dict(shift)
        for char in message:
            if char.isalpha():
                text += shifted_characters[char]
            else:
                text += char

        return text
    

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
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        super().__init__(text)
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class
        
        Returns: a COPY of self.encryption_dict
        '''
        return self.encryption_dict

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift.        
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)


class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        super().__init__(text)
        self.message_text = text
        self.valid_words = self.get_valid_words

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        word_list = load_words(WORDLIST_FILENAME)
        best_shift = 0
        max_number_words = 0
        best_decrypted_text = ''

        for shift in range(1, 26):
            decrypted_text = self.apply_shift(26 - shift)
            words = re.sub("[^A-Za-z0-9]+", " ", decrypted_text)
            words = words.split()
            valid_words = sum(1 for word in words if is_word(word_list, word))

            if valid_words > max_number_words:
                max_number_words = valid_words
                best_shift = shift
                best_decrypted_text = decrypted_text 
            
        return (26 - best_shift, best_decrypted_text)

        

if __name__ == '__main__':

    #Example test case (PlaintextMessage)
    plaintext = PlaintextMessage('hello', 2)
    print('Expected Output: jgnnq')
    print('Actual Output:', plaintext.get_message_text_encrypted())

    #Example test case (CiphertextMessage)
    ciphertext = CiphertextMessage('jgnnq')
    print('Expected Output:', (24, 'hello'))
    print('Actual Output:', ciphertext.decrypt_message())

    # Test case 1: Simple shift
    plaintext1 = PlaintextMessage('hello', 2)
    print('Test case 1:')
    print('Expected Output: jgnnq')
    print('Actual Output:', plaintext1.get_message_text_encrypted())
    
    # Test case 2: Wrap around alphabet
    plaintext2 = PlaintextMessage('zebra', 3)
    print('\nTest case 2:')
    print('Expected Output: cheud')
    print('Actual Output:', plaintext2.get_message_text_encrypted())
    
    # Test case 3: Maintain case and punctuation
    plaintext3 = PlaintextMessage('Hello, World!', 4)
    print('\nTest case 3:')
    print('Expected Output: Lipps, Asvph!')
    print('Actual Output:', plaintext3.get_message_text_encrypted())
    
    # Test case 4: Decrypt simple message
    ciphertext1 = CiphertextMessage('jgnnq')
    print('\nTest case 4:')
    print('Expected Output:', (24, 'hello'))
    print('Actual Output:', ciphertext1.decrypt_message())
    
    # Test case 5: Decrypt message with punctuation
    ciphertext2 = CiphertextMessage('Lipps, Asvph!')
    print('\nTest case 5:')
    print('Expected Output:', (22, 'Hello, World!'))
    print('Actual Output:', ciphertext2.decrypt_message())
    
    # Test case 6: Decrypt longer message
    story = get_story_string()
    ciphertext3 = CiphertextMessage(story)
    print('\nTest case 6:')
    print('Decrypted story:', ciphertext3.decrypt_message())

    # Test case 7: Change shift
    plaintext4 = PlaintextMessage('hello', 2)
    print('\nTest case 7:')
    print('Original shift: 2')
    print('Encrypted text:', plaintext4.get_message_text_encrypted())
    plaintext4.change_shift(3)
    print('New shift: 3')
    print('New encrypted text:', plaintext4.get_message_text_encrypted())

    #TODO: best shift value and unencrypted story 
    
