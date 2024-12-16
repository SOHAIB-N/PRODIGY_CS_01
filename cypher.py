import pyfiglet

class CaesarCipher:
    def __init__(self, text, shift=None, key=None, mode=None):
        self.text = text
        self.shift = shift
        self.key = key
        self.mode = mode
        self.processed_text = ""
        self.key_index = 0
        self.key_length = len(key) if key else 0
        self.shift_base = {True: 65, False: 97}
        self.alphabet_size = 26
    
    def _shift_character(self, char, shift_val, decrypt=False):
        shift_base = self.shift_base[char.isupper()]
        adjusted_shift = -shift_val if decrypt else shift_val
        return chr(((ord(char) - shift_base + adjusted_shift) % self.alphabet_size) + shift_base)

    def _process_with_shift(self, text, shift_val, decrypt=False):
        return ''.join([self._shift_character(c, shift_val, decrypt) if c.isalpha() else c for c in text])
    
    def _process_with_key(self, text, decrypt=False):
        key_process = lambda i: ord(self.key[i % self.key_length].lower()) - 97
        processed_text = []
        for char in text:
            if char.isalpha():
                shift_val = key_process(self.key_index) if not decrypt else -key_process(self.key_index)
                processed_text.append(self._shift_character(char, shift_val, decrypt))
                self.key_index += 1
            else:
                processed_text.append(char)
        return ''.join(processed_text)
    
    def encrypt(self):
        if self.key:
            return self._process_with_key(self.text)
        return self._process_with_shift(self.text, self.shift)
    
    def decrypt(self):
        if self.key:
            return self._process_with_key(self.text, decrypt=True)
        return self._process_with_shift(self.text, self.shift, decrypt=True)

def user_input_interaction():
    _ = lambda s: input(s)
    cipher_config = {
        '1': lambda text, shift: CaesarCipher(text, shift=shift).encrypt(),
        '2': lambda text, shift: CaesarCipher(text, shift=shift).decrypt(),
        '3': lambda text, key: CaesarCipher(text, key=key, mode='encrypt').encrypt(),
        '4': lambda text, key: CaesarCipher(text, key=key, mode='decrypt').decrypt()
    }

    while True:
        option = _("\nSelect an operation:\n1. Encrypt\n2. Decrypt\n3. Encrypt with Keyword\n4. Decrypt with Keyword\n5. Exit\n> ").strip()
        
        if option in cipher_config:
            message = _("Enter the message: ")
            if option in ('1', '2'):
                shift = int(_("Enter the shift value: "))
                result = cipher_config[option](message, shift)
            else:
                key = _("Enter the keyword: ")
                result = cipher_config[option](message, key)
            
            print(f"Result: {result}")
        
        elif option == '5':
            print("Shutting down. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

def main():
    ascii_art = pyfiglet.figlet_format("Caesar Cipher")
    print(ascii_art)

    try:
        user_input_interaction()
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
