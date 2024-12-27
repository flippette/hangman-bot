# Filter words by length
def filter_length(wordlist: list, length: int):
  # Length must be a positive integer
  if length < 1:
    raise ValueError()

  # Simple matching
  ret = []
  for word in wordlist:
    if len(word) == length:
      ret.append(word)
  return ret

# Filter words through whitelisted characters
def filter_whitelist(wordlist: list, whitelist: list):
  import re

  # Assemble regex for filtering
  pattern = ''
  for chr in whitelist:
    pattern = pattern + '(?=.*' + chr + ')'
  
  # Simple matching
  ret = []
  for word in wordlist:
    if re.match(pattern, word):
      ret.append(word)
  return ret

# Filter words through blacklisted characters
def filter_blacklist(wordlist: list, blacklist: list):
  import re

  # Assemble regex for filtering
  pattern = '^[^'
  for chr in blacklist:
    pattern = pattern + chr
  pattern = pattern + ']+$'

  if pattern == '^[^]+$':
    return wordlist
  
  # Simple matching
  ret = []
  for word in wordlist:
    if re.match(pattern, word):
      ret.append(word)
  return ret

# Prune duplicates in list
def prune(lst: list):
  ret = []
  for item in lst:
    if item not in ret:
      ret.append(item)
  return ret

# Get character frequency map
def get_freq_map(wordlist: list):
  freq_map = {}
  for word in wordlist:
    for char in word:
      if char not in freq_map:
        freq_map[char] = 1
        continue
      freq_map[char] = freq_map[char] + 1
  ret = sorted(freq_map.items(), key=lambda item: item[1], reverse=True)
  for index, item in enumerate(ret):
    ret[index] = item[0]
  return ret

# Guessing function
def guess(fmap: list, whitelist: list, blacklist: list):
  import re

  # Get most frequent unlisted char
  for chr in fmap:
    if chr not in whitelist and chr not in blacklist:
      if re.match('^[yY]', input('Is there a "' + chr + '"? ')):
        whitelist.append(chr)
        break
      blacklist.append(chr)
      break
  
  # Return most frequent character in filtered list
  return get_freq_map(filter_blacklist(filter_whitelist(words, whitelist), blacklist))[0]


# Query the user for target length
try:
  word_length = int(input('Word length: '))
except ValueError:
  print('Invalid word length! Exiting...')
  exit(1)

# Read words.txt
words = filter_length(open('words.txt', 'r').read().split('\n'), word_length)

# Main guessing routine
whitelist = []
blacklist = []
while True:
  import re

  current_fmap = get_freq_map(words)

  guess(current_fmap, whitelist, blacklist)

  # Braking condition: if len(filter_whitelist(words, whitelist)) == len(words)
  buffer = filter_blacklist(filter_whitelist(words, whitelist), blacklist)
  if len(buffer) == len(words):
    break
  words = buffer

is_correct = False  # Flag to track if the correct word was found

for index, word in enumerate(words):
    if index < 5:
          if re.match('^[yY]', input('Is it "' + word + '"? ')):
            print('yay ig')
            is_correct = True
            break
      
# If no correct word was found, ask if the user is lying
if not is_correct:
    guessed_word = input('Okay, what is it then: ').strip()
    if guessed_word in words:
        print('yea makes sense')
    else:
        print('stop lying')
