{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyOHTkE/txaNxuigz/5KPJC7",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/Mtiwari27/Virality-Prediction-Model/blob/main/Viralityapp.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "shub6a0rGoWb"
      },
      "outputs": [],
      "source": [
        "import streamlit as st\n",
        "import pickle\n",
        "import re\n",
        "import pandas as pd\n",
        "from nltk.corpus import stopwords\n",
        "from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer\n",
        "\n",
        "# Load the trained model\n",
        "with open(\"virality_model.pkl\", \"rb\") as file:\n",
        "    model = pickle.load(file)\n",
        "\n",
        "# Function to preprocess text\n",
        "def clean_text(text):\n",
        "    text = re.sub(r\"http\\S+|www\\S+|https\\S+\", '', text)  # Remove URLs\n",
        "    text = re.sub(r'\\@\\w+|\\#','', text)  # Remove mentions & hashtags\n",
        "    text = re.sub(r'\\d+', '', text)  # Remove numbers\n",
        "    text = text.lower()  # Convert to lowercase\n",
        "    text = ' '.join([word for word in text.split() if word not in stopwords.words('english')])  # Remove stopwords\n",
        "    return text\n",
        "\n",
        "# Function to extract features\n",
        "def extract_features(post_text, likes, shares, comments, followers, post_hour):\n",
        "    sia = SentimentIntensityAnalyzer()\n",
        "    sentiment = sia.polarity_scores(post_text)['compound']\n",
        "    hashtag_count = len(re.findall(r\"#\\w+\", post_text))\n",
        "    engagement_rate = (likes + shares + comments) / max(followers, 1)  # Avoid division by zero\n",
        "\n",
        "    time_of_day = [0, 0, 0, 0]  # [Night, Morning, Afternoon, Evening]\n",
        "    if 0 <= post_hour < 6:\n",
        "        time_of_day[0] = 1\n",
        "    elif 6 <= post_hour < 12:\n",
        "        time_of_day[1] = 1\n",
        "    elif 12 <= post_hour < 18:\n",
        "        time_of_day[2] = 1\n",
        "    else:\n",
        "        time_of_day[3] = 1\n",
        "\n",
        "    return [hashtag_count, sentiment, engagement_rate] + time_of_day\n",
        "\n",
        "# Streamlit UI\n",
        "st.title(\"Social Media Virality Predictor\")\n",
        "st.write(\"Enter the details of your post to predict if it will go viral.\")\n",
        "\n",
        "# User input\n",
        "post_text = st.text_area(\"Enter your post text:\")\n",
        "likes = st.number_input(\"Number of Likes:\", min_value=0, value=100)\n",
        "shares = st.number_input(\"Number of Shares:\", min_value=0, value=50)\n",
        "comments = st.number_input(\"Number of Comments:\", min_value=0, value=20)\n",
        "followers = st.number_input(\"Total Followers:\", min_value=1, value=1000)\n",
        "post_hour = st.slider(\"Hour of Post (0-23):\", min_value=0, max_value=23, value=12)\n",
        "\n",
        "if st.button(\"Predict\"):\n",
        "    features = extract_features(post_text, likes, shares, comments, followers, post_hour)\n",
        "    prediction = model.predict([features])[0]\n",
        "\n",
        "    if prediction == 1:\n",
        "        st.success(\"This post is likely to go VIRAL! 🚀\")\n",
        "    else:\n",
        "        st.warning(\"This post may not go viral. Try optimizing hashtags and engagement.\")"
      ]
    }
  ]
}