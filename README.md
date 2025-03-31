# Baby Faces Anonymizer

An end to end project for ingesting, annotating, training and deploying a model for anonymizing baby faces 

## 0. Setup

### Google Search Engine

0. rename `.env.example` to `.env`
1. Create a new search engine at [Search Engine Control Panel](https://programmablesearchengine.google.com/controlpanel/all)
2. Copy the Search Engine ID and place it on the `SEARCH_ENGINE_ID` line inside the `.env` file
3. Generate a Google Cloud API key, copy it and paste on the `G_API_KEY` line inside the `.env` file