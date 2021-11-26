# Mystify
WordNet and Rhyming for Sublime Text

## Usage

Right click a highlighted word.


![mystify](https://user-images.githubusercontent.com/43641857/143511014-88f510c4-8e17-4884-8ea2-0de925460fb0.png)


## Installation
Navigate to the packages folder for sublime text:

  `git clone https://github.com/M49ICKPIxi3/mystify.git`

From the [wn library](https://github.com/goodmami/wn) installation instructions:

  ```
  pip install wn
  python -m wn download oewn:2021
  ```

Next, find the 'site-packages' directory of your local python installation. For example: `~/.pyenv/versions/3.8.0/lib/python3.8/site-packages`

Export the site-packages path to ST_USER_SITE_PACKAGES. This allows Sublime to add the site-packages to sys.path at runtime. Also works with the [Fountain](https://github.com/M49ICKPIxi3/Fountain) text generation plugin too.

  `export ST_USER_SITE_PACKAGES="path/to/your/site-packages"`

Restart Sublime Text and that's it!

Note: If you are running Sublime Text from a terminal don't forget to run `source .zshrc` for the shell you're using.

