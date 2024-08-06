# education3.0

Fun RAG app to pull problems from math textbooks and generate lesson plans from them!

# Installation Steps:

1. For now, you will need to clone the repo on your computer:

* `$ cd /path/to/desired/install/directory`

* `$ git clone https://github.com/ng4567/education3.0.git`

1. Then, create a groq API key here: [link](https://console.groq.com/keys)

Then, set the `GROQ_API_KEY` environment variable or create a `.env` file and load it using the `python-dotenv` library (you will need to modify my code if you don't take this option to avoid import errors).

3. Finally, you'll need to setup your python environment. I have provided a requirements.txt file that contains all needed libraries.

After creating a new conda or pyenv, run `pip install -r app/requirements.txt`


# Run the Application

Once you have setup your environment and obtained a groq API key, run the app:

* `$ cd app`
* `streamlit run 1-home.py` 
