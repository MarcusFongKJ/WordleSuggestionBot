# Wordle Suggestion Bot

This is my version of the popular game [*Wordle*](https://www.nytimes.com/games/wordle/index.html) built using Pygame. The game is similar to the original but with the addition of a list of word suggestions (up to 114) to help guide the player towards the answer. The suggestion list of 15,918 words was obtained by taking all the 5 letter words from [words_alpha.txt](https://github.com/dwyl/english-words/blob/master/words.txt). This list is updated using the information gained every time a new guess is entered.<br>
<br>

### 3 possible outcomes for each letter when a guess is entered:  
- Grey: Letter is not in answer<br>
- Yellow: Letter is in answer but incorrect position<br>
- Green: Letter is in answer and in correct position<br>
<br>

### How the suggestion list is updated after each guess:
The outcomes for the letters are stored in a list for grey letters, and a dictionary for yellow or green letters. The dictionary for yellow and green letters has a key of the particular letter and its corresponding value would be its position on the guess.<br>
- Words containing any grey letters is removed from the suggestion list.<br>
- Words with yellow letters at the exact position of the guess are removed from the suggestion list.<br>
- Word with green letters at the exact position of the guess are kept, all other words are removed from the suggestion list.<br>
<br>

## References when building this:
[3Blue1Brown](https://www.youtube.com/watch?v=v68zYyaEmEA&ab_channel=3Blue1Brown)<br>
[LeMaster Tech](https://www.youtube.com/watch?v=D8mqgW0DiKk&ab_channel=LeMasterTech)<br>
<br>

## Additional Information
The list of words allowed as a guess from the [website](https://www.nytimes.com/games/wordle/index.html) was different from where I had [referenced from](https://github.com/3b1b/videos/blob/master/_2022/wordle/data/possible_words.txt). The reason for this discrepancy is that when The New York Times bought Wordle and migrated it to its hosted site, certain words that were deemed too difficult, rude or offensive were removed (article [here](https://edition.cnn.com/2022/02/15/media/wordle-241-answers-new-york-times/index.html)). The video made by 3Blue1Brown shows that the data he used was from the original site at powerlanguage.co.uk/wordle/.