
![NeuralNotes](/engine/static/logo_idea_01.png)

## 1. Backgrounds 

The project is carried out during the completion of the bachelor thesis at Vietnam-Germany University. This project aims to investigate ability of generating music by an AI. Whether it creates a "melodic" product is a matter of debate, however, if we don't try it we won't know anything. Furthermore, the author develops a friendly-user interface which allows users can interact with the agent. 

## 2. Acknowledgement

The author expressed his sincere thanks to the warm guidance of Dr. Dinh Quang Vinh and Dr. Ngoc Tran Hong. At the same time, the author also thanked Mr. Nguyen Hoang Huy Bao's companion with specific and clear instructions.

## 3, Usage

### Install environment 

```
    # Clone this repository. The terminal should be directed to the directory containing this project.
    # If you do not use conda, you can substitute 2 follows line by those appropriate to your machine

    # Create environment and access to it
    conda create --name musicgen
    conda activate musicgen

    # Install requirements
    pip install -r requirements.txt
```

### Usage

```
    # Run the project
    python main.py
```

### For developers

For those who want to interact directly to model so that you guys can play with it. There are notebooks in /notebook, having implementations for data representation, REMI representation, training model and generating function of the model. 


## 4. Contributors. 

1. Dr. Dinh Quang Vinh. 
2. Dr. Ngoc Tran Hong. 
3. Le Duc Minh. 


## Note

There are many variations to suit your environment. For example, the tokens for using Google's OAuth2 need to be updated to suit your needs. The data system I use is MongoDB, which you can change to suit your settings.

There are many soundfonts that I have collected in /engine/soundfonts, you guyes can change to suit your settings. 
