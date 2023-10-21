
![NeuralNotes](/engine/static/logo_idea_01.png)

## 1. Backgrounds 

The project is carried out during the completion of the bachelor thesis at Vietnam-Germany University. This project aims to investigate ability of generating music by an AI. Whether it creates a "melodic" product is a matter of debate, however, if we don't try it we won't know anything. Furthermore, the author develops a friendly-user interface which allows users can interact with the agent. 

## 2. Acknowledgement

The author expressed his sincere thanks to the warm guidance of Dr. Dinh Quang Vinh and Dr. Ngoc Tran Hong. At the same time, the author also thanked Mr. Nguyen Hoang Huy Bao's companion with specific and clear instructions.

## 3. Usage

### Install environment

```
    # Clone this repository. The terminal should be directed to the directory containing this project.
    # If you do not use conda, you can substitute 2 follows line by those appropriate to your machine

    # Create environment and access to it
    conda create --name neuralnotes
    conda activate neuralnotes

    # Install requirements
    pip install -r requirements.txt
```

Users can train the model from the beginning or use pretrained model [here](https://drive.google.com/file/d/12fZpF1GxpWzrC7bhQx0T8BLOBfIoJn1C/view?usp=share_link). 

The link for dataset is [here](https://zenodo.org/record/4782721/files/remi_dataset.tar.gz?download=1). I have prepared several samples for the processing. Also, there are processed pieces at /data/examples, users can give it a try. 

### Run Application

```
    # Run the project
    python main.py
```

## 4. Contributors. 

1. Dr. Dinh Quang Vinh. 
2. Dr. Ngoc Tran Hong. 
3. Le Duc Minh. 

## 5. Contact

Gmail: 16669@student.vgu.edu.vn

Linkedin: https://www.linkedin.com/in/minh-le-duc-a62863172/

## 6. Note

+ There are many variations to suit your environment. For example, the tokens for using Google's OAuth2 need to be updated to suit your needs. The data system I use is MongoDB, which you can change to suit your settings.

+ There are many soundfonts that I have collected in /engine/soundfonts, you guys can change to suit your settings. 

+ For those who want to interact directly to model so that you guys can play with it. There are notebooks in /notebook, having implementations for data representation, REMI representation, training model and generating function of the model. 
