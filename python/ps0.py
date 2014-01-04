#qpy:console
def run():
  lastName = raw_input('Enter your last name\n**')
  firstName = raw_input('Enter your date of birth:\n**')
  print lastName + ' ' + firstName
  return
def root(num):
  return rootrec(num/(num/2),num)
  
def rootrec(guess,num):
  guessRes = guess * guess
  print "guess " + str(guess) + " " + str(guessRes)
  if((guessRes - num)<0.1):
    return guess
  else: 
    return rootrec((guess+(guessRes/guess))/2,num)

print root(25)