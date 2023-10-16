# AuthoWrite Back-End

*Created for the COMP30022 IT Project subject*

### <u>Members</u>

[`Adrian Podiono`](https://www.linkedin.com/in/adrian-podiono-787367246)  [`Hanizam Zaharyudin`](https://www.linkedin.com/in/hanizam-zaharyudin-1a5124198)  [`Jia Jie Zheng`](https://www.linkedin.com/in/thomas-zheng-7622a2190/)  [`Lin Xin Xie`](https://www.linkedin.com/in/linxx/)  [`Saaiq Ahmed`](https://www.linkedin.com/in/saaiq-ahmed-364b5a219/)

## Description

This is the Flask Web API repository which is used to input and process strings, `.txt`, `.pdf` and `.docx` files to output an estimated Authorship score. 

- *A score on the likelihood percentage chance that an unknown text was written by the author of the known texts, assuming all the known texts were written by the same individual*

All files are converted into strings and pipelined into the **Authorship Algorithm** supplied to us by our client [Eduardo Oliveira](https://www.eduoliveira.com/).

- *The given algorithm was simplified as the model used isn't being trained and only used*
- *The algorithm was also improved upon after errors were noticed which was done with the permission of our client*

#### Algorithm Changes Made:
1. Edited `get_vectors()` to output text style information
2. Fixed `calculate_style_vector()` to not divide `avg_sentence_length` and `ttr` by `word_count`
   1. Edited to output `word_count` as well
3. Fixed `analyze_sentence_lengths()` to properly obtain a list of sentence lengths

Alongside the score, the algorithm also outputs extra data about the unknown and known texts which is used by the algorithm in determining Authorship score. The extra data is supplied for the user's insight as to why the model may have given the score it did.

## How To Use 

Documentation of the deployed API is available with the link here: [AuthoWrite Back-End API Documentation](http://3.26.213.177:5000/docs)

There is only 1 main function under `/compare` as a `POST` request which takes in a multi-part form and outputs a JSON response. The multi-part form is ensured to include the headers:

- `"known_texts"` *(Required)* : `List` of known texts (of type `str`) to compare against
- `"unknown_text"` : an unknown text (of type `str`) to compare against
- `"known_files"` *(Required)* : `List` of known files (of type `file`) to compare against
- `"unknown_file"` : unknown file (of type `file`) to compare against

    - Where `"unknown_file"` takes priority over `"unknown_text"`

## Deployment Method

The deployment was done as an **EC2 Instance** on AWS.
The server was setup manually at the start to install both `git` and `python3`. So that the repository could then be cloned to the EC2 Instance and run.

To ensure CI/CD, a script was setup to check for any changes to the main branch of the github and then rerun the process.

The code used for the deployment after the initial setup was:

    git pull
    pip install -r requirements.txt
    python -c 'import nltk; nltk. download(["punkt", "stopwords","wordnet"])'
    export FLASK_APP=application.py
    nohup flask run --host=0.0.0.0

Where `nohup` allows for the application to run in the EC2 instance continuously even when the terminal is closed. The command in line 3 is also only needed once as attempting to redownload is unneccessary computing. 