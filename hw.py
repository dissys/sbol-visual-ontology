
import re

def Find(string): 
    # findall() has been used  
    # with valid conditions for urls in string 
    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string) 
    return url 
      
# Driver Code 
string = 'My Profile: https://auth.geeksforgeeks.org / user / Chinmoy % 20Lenka / articles in the portal of http://www.geeksforgeeks.org/' 
print("Urls: ", Find(string)) 


line= "Complex: http://www.biopax.org/release/biopax-level3.owl#Complex fgdfg"
#items=re.findall('(www|http|https)+[^\s]+[\w]', line)
items=re.findall(r'http[.]*', line)

print (items)
for item in items:
  # do something with each found email string
  print (item)

items = re.findall(r'(?<=-)\w+', 'spam-egg sdf-milk')
for item in items:
  # do something with each found email string
  print (item)


## Suppose we have a text with many email addresses
str = 'purple alice@google.com, blah monkey bob@abc.com blah dishwasher'

## Here re.findall() returns a list of all the found email strings
emails = re.findall(r'[\w\.-]+@[\w\.-]+', str) ## ['alice@google.com', 'bob@abc.com']
for email in emails:
  # do something with each found email string
  print (email)
  
    
line="da SO:0001955, SO:0001546 (Protein Stability Element)"
#line=" SO:0001546 (Protein Stability Element)"

items=re.findall('a[A-Z]+:[0-9]+', line)
for item in items:
  # do something with each found email string
  print (item)
  

    
line ="df ![glyph specification](aptamer-specification.png)dvg"
#p=re.compile('\((.)*.png\)') 
p=re.compile('\((.)*.png\)') 
#p=re.compile(r'glyph(.)*png') 
#p=re.compile('(.)*!\[(.*?)\]\((.*?)\)')
items=re.findall('!\[(.*?)\]\((.*?)\)',line)
for item in items:
  # do something with each found email string
  print (item[1])
  



 