# Sample Streamlit App on CO2-GDP Dataset
This is a sample Streamlit app that uses the CO2-GDP dataset to visualize the relationship between CO2 emissions and GDP.

`conda.yml` file is provided for setting up a local development environment using Anaconda. Streamlit currently does not properly support conda environments on Streamlit Cloud, so the `requirements.txt` file is provided for deploying the app on Streamlit Cloud.

Setup conda environment:
```bash
conda env create -f conda.yml
conda activate streamlit-co2-gdp
```

Run the app locally:
```bash
streamlit run co2-gdp_db_plotly_streamlit.py
```

The app is deployed on Streamlit Cloud at `https://co2-gdp-db.streamlit.app

Deploy your own app on Streamlit Cloud:
1. Push the code to a public GitHub repository of yours.
1. Create a new app on Streamlit Cloud.
2. Connect your GitHub repository containing the app code.
3. Select the branch and file path of the app.
4. Select python version 3.10
4. Click "Deploy" to deploy the app.
5. Once the app is deployed, you can access it using the provided URL.

Documentation:
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit Cloud Documentation](https://docs.streamlit.io/streamlit-cloud)