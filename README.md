<h1>Stock-Prediction</h1>
    <p>
        This is an innovative and user-friendly stock prediction web application developed in Python. 
        By harnessing the power of <strong>Streamlit</strong>, <strong>Alpha Vantage API</strong>, and <strong>Facebook Prophet</strong>, 
        this app empowers users to make informed investment decisions. With just a few clicks, users can select their preferred stock, 
        specify the desired prediction period, and gain valuable insights by visualizing accurate and reliable forecasted stock prices. 
        Stay ahead of the market trends and maximize your investment potential with this cutting-edge stock prediction app.
    </p>
    <p>Check out the live demo of this stock prediction web application at 
        <a href="https://stock-prediction-ue99dmds3q.streamlit.app/" target="_blank">Streamlit App Link</a>.
    </p>

<h2>Features</h2>
    <ul>
        <li>Enter a stock symbol or ticker (e.g., <code>AAPL</code>, <code>GOOG</code>) to select the desired stock for prediction.</li>
        <li>Choose the number of years for prediction.</li>
        <li>View raw stock data, interactive time series plots, forecast data, forecast chart, and forecast components.</li>
        <li>Interactive and responsive web interface.</li>
        <li>Fetches data from <strong>Alpha Vantage</strong> and forecasts using <strong>Facebook Prophet</strong>.</li>
    </ul>

<h2>Installation</h2>
    <ol>
        <li>Clone or download this repository to your local machine.</li>
        <li>Install the required dependencies:
            <pre><code>pip install -r requirements.txt</code></pre>
        </li>
        <li>Run the app:
            <pre><code>streamlit run app.py</code></pre>
        </li>
        <li>Open the web app in your browser: <a href="http://localhost:8501" target="_blank">http://localhost:8501</a></li>
    </ol>

<h2>Getting Your Alpha Vantage API Key</h2>
    <ol>
        <li>Go to the <a href="https://www.alphavantage.co/support/#api-key" target="_blank">Alpha Vantage website</a> and sign up for a free account.</li>
        <li>After signing up, you will receive a free API key.</li>
        <li>Add your API key to the app by creating a <code>.streamlit/secrets.toml</code> file in your project folder with the following content:
            <pre><code>alpha_vantage_api_key = "YOUR_API_KEY_HERE"</code></pre>
        </li>
        <li>Save the file and restart the app.</li>
    </ol>
    <p><em>The app will automatically use this API key instead of the default key.</em></p>

<h2>Technologies Used</h2>
    <ul>
        <li>Python</li>
        <li>Streamlit</li>
        <li>Alpha Vantage API</li>
        <li>Facebook Prophet</li>
        <li>Plotly</li>
        <li>Pandas</li>
    </ul>

<h2>Contributions</h2>
    <p>
        Contributions are welcome! We value your input and encourage you to actively participate in the project. 
        If you have any ideas, suggestions, bug reports, or feature requests, please don't hesitate to open an issue on GitHub. 
        Additionally, we appreciate any code contributions you may have. If you'd like to contribute code, please submit a pull request, 
        and we will review it as soon as possible. Thank you for your support!
    </p>
