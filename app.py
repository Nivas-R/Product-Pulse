{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyPv4BQwWTaOmj6Nfl6aErFZ",
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
        "<a href=\"https://colab.research.google.com/github/Nivas-R/Product-Pulse/blob/main/app.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# ===============================\n",
        "# 1. Imports\n",
        "# ===============================\n",
        "import pandas as pd\n",
        "import nltk\n",
        "from nltk.sentiment import SentimentIntensityAnalyzer\n",
        "\n",
        "# ===============================\n",
        "# 2. Download VADER lexicon (safe check)\n",
        "# ===============================\n",
        "try:\n",
        "    nltk.data.find('sentiment/vader_lexicon')\n",
        "except LookupError:\n",
        "    nltk.download('vader_lexicon')\n",
        "\n",
        "# ===============================\n",
        "# 3. Load Data\n",
        "# ===============================\n",
        "df = pd.read_csv(\"final_merged_dataset.csv\")  # make sure filename matches\n",
        "\n",
        "# ===============================\n",
        "# 4. Text Preprocessing (safe & clean)\n",
        "# ===============================\n",
        "df['review_text'] = (\n",
        "    df['review_text']\n",
        "    .fillna(\"\")          # safety for missing text\n",
        "    .str.lower()         # normalize casing\n",
        "    .str.strip()         # remove extra spaces\n",
        ")\n",
        "\n",
        "# ===============================\n",
        "# 5. Sentiment Analysis\n",
        "# ===============================\n",
        "sia = SentimentIntensityAnalyzer()\n",
        "\n",
        "df['sentiment_score'] = df['review_text'].apply(\n",
        "    lambda x: sia.polarity_scores(x)['compound']\n",
        ")\n",
        "\n",
        "# ===============================\n",
        "# 6. Sentiment Labeling\n",
        "# ===============================\n",
        "def label_sentiment(score):\n",
        "    if score >= 0.05:\n",
        "        return \"Positive\"\n",
        "    elif score <= -0.05:\n",
        "        return \"Negative\"\n",
        "    else:\n",
        "        return \"Neutral\"\n",
        "\n",
        "df['sentiment_label'] = df['sentiment_score'].apply(label_sentiment)\n",
        "\n",
        "# ===============================\n",
        "# 7. KPI Creation\n",
        "# ===============================\n",
        "product_kpis = df.groupby('product_name').agg(\n",
        "    avg_price=('price', 'mean'),\n",
        "    total_stock=('stock', 'sum'),\n",
        "    avg_sentiment=('sentiment_score', 'mean'),\n",
        "    review_count=('review_text', 'count')\n",
        ").reset_index()\n",
        "\n",
        "category_kpis = df.groupby('category').agg(\n",
        "    avg_sentiment=('sentiment_score', 'mean'),\n",
        "    review_count=('review_text', 'count')\n",
        ").reset_index()\n",
        "\n",
        "low_stock_alert = df[df['stock'] < 20][\n",
        "    ['product_name', 'category', 'stock', 'sentiment_label']\n",
        "]\n",
        "\n",
        "# ===============================\n",
        "# 8. Save Outputs\n",
        "# ===============================\n",
        "df.to_csv(\"merged_with_sentiment.csv\", index=False)\n",
        "product_kpis.to_csv(\"product_kpis.csv\", index=False)\n",
        "category_kpis.to_csv(\"category_kpis.csv\", index=False)\n",
        "low_stock_alert.to_csv(\"low_stock_alert.csv\", index=False)\n",
        "\n",
        "print(\"Pipeline executed successfully.\")\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "ZwbxFxAxOYzs",
        "outputId": "034c8ffd-1429-4224-e088-9438f56232ed"
      },
      "execution_count": 5,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Pipeline executed successfully.\n"
          ]
        },
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "[nltk_data] Downloading package vader_lexicon to /root/nltk_data...\n",
            "[nltk_data]   Package vader_lexicon is already up-to-date!\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "LVvzg5uMOKo4"
      },
      "outputs": [],
      "source": []
    }
  ]
}