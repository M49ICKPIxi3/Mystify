# Mystify
WordNet Thesaurus and Rhyming for Sublime Text

## Usage

Highlight a word and right click. You can either view Definitions or select a word in one of the submenus to use as a replacement.


![mystify](https://user-images.githubusercontent.com/43641857/143511014-88f510c4-8e17-4884-8ea2-0de925460fb0.png)


## Installation
Navigate to the Packages folder for Sublime Text:

  `cd ~/Library/Application\ Support/Sublime\ Text\ 3/Packages`

Clone the repository.

  `git clone https://github.com/M49ICKPIxi3/mystify.git`

From the [wn library](https://github.com/goodmami/wn) installation instructions:

  ```
  pip install wn
  python -m wn download oewn:2021
  ```

Restart Sublime Text.

Deployment on Package Control is upcoming. Until then, you have to download the repo into the Packages directory. 
The version of python used to download the WordNet data doesn't matter, you just need to have the data on
your machine for Mystify to be able to use it. Interface for additional WordNets also upcoming.

#### Credits:
WordNet's integration uses [wn](https://github.com/goodmami/wn).

Rhyming feature makes use of [pronouncing](https://github.com/aparrish/pronouncingpy).
