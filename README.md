# Welcome to the Lisan Arab Team Project

This project is dedicated to developing and evaluating language models specifically tailored for Arabic dialects and Modern Standard Arabic (MSA). We aim to provide advanced NLP tools that understand and process Arabic with high accuracy and nuance.

## Project Structure

### 📂 Data
All datasets are organized and stored in the `Data` folder. This directory contains the raw and processed data used throughout the project for training, fine-tuning, and evaluation of the models.

### 📂 Evaluation
The evaluation scripts and results can be found in the `Evaluation` folder. Within it, there’s a subdirectory called `Modeltest` that contains scripts for connecting with external models for comparative evaluation. We conduct evaluation through multiple language models, including:

- **GPT-4** and **GPT-3.5**
- **ALLaM**
- **Lisan ALLaM** (our custom model tailored for Arabic dialects)

### 📂 Preprocessing
The `Preprocessing` folder holds scripts used to clean, preprocess, and format the data before feeding it into models. This includes tokenization, dialect tagging, and other essential steps for optimal model training and evaluation.

## Running the Project

### Step 1: Start the Flask Server
To enable connectivity with IBM resources and access specific model APIs, start the Flask server by running:

```bash
python app.py
```

### Step 2: Launch the Project
Once the server is running, you can start the application with:

```bash
flutter run
```

This command initiates the Flutter application, setting up the project’s interface and features.

---

Happy coding! 🚀
