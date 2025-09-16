import streamlit as st
import streamlit_authenticator as stauth
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xgboost as xgb
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from textblob import TextBlob
import requests
from datetime import datetime
from PIL import Image

# --- Authentication Setup ---
users = {
    "usernames": ["user1"],
    "names": ["User  One"],
    "passwords": ["$2b$12$KIXQ6q6q6q6q6q6q6q6q6u6q6q6q6q6q6q6q6q6q6q6q6q6q6q6q6"]  # bcrypt hashed password for 'password'
}

authenticator = stauth.Authenticate(
    users['names'], users['usernames'], users['passwords'],
    'some_cookie_name', 'some_signature_key', cookie_expiry_days=30
)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    st.write(f"Welcome *{name}*")
    authenticator.logout('Logout', 'sidebar')

    # --- Helper Functions for Technical Indicators ---
    def compute_macd(df, fast=12, slow=26, signal=9):
        macd_line = df['Close'].ewm(span=fast, adjust=False).mean() - df['Close'].ewm(span=slow, adjust=False).mean()
        signal_line = macd_line.ewm(span=signal, adjust=False).mean()
        return macd_line, signal_line

    def compute_rsi(df, window=14):
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def compute_stochastic(df, window=14):
        low_min = df['Low'].rolling(window=window).min()
        high_max = df['High'].rolling(window=window).max()
        stochastic = 100 * (df['Close'] - low_min) / (high_max - low_min)
        return stochastic

    def compute_bollinger_bands(df, window=20):
        df['Middle_BB'] = df['Close'].rolling(window=window).mean()
        df['Std_Dev'] = df['Close'].rolling(window=window).std()
        df['Upper_BB'] = df['Middle_BB'] + (df['Std_Dev'] * 2)
        df['Lower_BB'] = df['Middle_BB'] - (df['Std_Dev'] * 2)
        return df

    # --- News Sentiment Analysis ---
    def fetch_news_headlines(stock_symbol):
        # Replace YOUR_API_KEY with your actual NewsAPI key
        api_key = "YOUR_API_KEY"
        url = f"https://newsapi.org/v2/everything?q={stock_symbol}&language=en&sortBy=publishedAt&apiKey={api_key}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            articles = response.json().get('articles', [])
            headlines = [article['title'] for article in articles]
            return headlines
        except Exception as e:
            st.warning(f"News API error: {e}")
            return []

    def compute_sentiment_score(headlines):
        if not headlines:
            return 0
        scores = [TextBlob(headline).sentiment.polarity for headline in headlines]
        return np.mean(scores)

    # --- Fetch Stock Data ---
    def get_stock_data(stock_symbol, start_date, end_date):
        try:
            df = yf.download(stock_symbol, start=start_date, end=end_date)
            if 'Adj Close' in df.columns:
                df.drop(columns=['Adj Close'], inplace=True)
            return df
        except Exception as e:
            st.error(f"Error fetching stock data: {e}")
            return pd.DataFrame()

    # --- Streamlit UI ---
    st.title("MarketMantra - Stock Trend Predictor with Authentication & News Sentiment")

    stock_symbol = st.text_input("Enter Stock Symbol (e.g., AAPL, MSFT, ^BSESN)", value="^BSESN").upper()
    start_date = st.date_input("Start Date", pd.to_datetime("2023-01-01"))
    end_date = st.date_input("End Date", datetime.now().date())

    if start_date >= end_date:
        st.error("Start date must be before end date.")
        st.stop()

    df = get_stock_data(stock_symbol, start_date, end_date)
    if df.empty:
        st.warning("No data found for the selected stock or date range.")
        st.stop()

    # --- Feature Engineering ---
    df['Previous Close'] = df['Close'].shift(1)
    df['Daily Return'] = df['Close'].pct_change()
    df['MACD'], df['MACD_Signal'] = compute_macd(df)
    df['RSI'] = compute_rsi(df)
    df['Stochastic'] = compute_stochastic(df)
    df = compute_bollinger_bands(df)
    df['Target'] = np.where(df['Close'].shift(-1) > df['Close'], 1, 0)
    df.dropna(inplace=True)

    # --- News Sentiment Feature ---
    headlines = fetch_news_headlines(stock_symbol)
    sentiment_score = compute_sentiment_score(headlines)
    # Add sentiment score as a constant feature for all rows (or just latest row)
    df['News_Sentiment'] = sentiment_score

    # --- Prepare Features and Target ---
    feature_cols = ['Previous Close', 'Daily Return', 'MACD', 'MACD_Signal', 'RSI', 'Stochastic', 'Upper_BB', 'Lower_BB', 'News_Sentiment']
    features = df[feature_cols]
    target = df['Target']

    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)

    X_train, X_valid, Y_train, Y_valid = train_test_split(features_scaled, target, test_size=0.1, random_state=42)

    # --- Models ---
    models = {
        "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=20, random_state=50),
        "Gradient Boosting": GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=50),
        "XGBoost": xgb.XGBClassifier(n_estimators=100, max_depth=5, learning_rate=0.1, random_state=50, use_label_encoder=False, eval_metric='logloss'),
        "Decision Tree": DecisionTreeClassifier(random_state=50)
    }

    model_predictions = []
    for model_name, model in models.items():
        model.fit(X_train, Y_train)
        preds = model.predict(X_valid)
        model_predictions.append(preds)

    model_predictions = np.array(model_predictions)
    avg_preds = np.mean(model_predictions, axis=0)
    final_preds = np.round(avg_preds)

    # --- Confusion Matrix ---
    cm = confusion_matrix(Y_valid, final_preds)
    st.subheader("Confusion Matrix (Ensemble Prediction)")
    fig, ax = plt.subplots(figsize=(5, 5))
    cax = ax.matshow(cm, cmap=plt.cm.Blues)
    plt.title('Confusion Matrix')
    fig.colorbar(cax)
    ax.set_xticklabels([''] + ['Down', 'Up'])
    ax.set_yticklabels([''] + ['Down', 'Up'])
    plt.xlabel('Predicted')
    plt.ylabel('True')
    for (i, j), val in np.ndenumerate(cm):
        ax.text(j, i, val, ha='center', va='center')
    st.pyplot(fig)

    # --- Model Accuracy Display ---
    st.subheader("Model Accuracies")
    accuracies = {}
    for model_name, model in models.items():
        y_pred = model.predict(X_valid)
        acc = accuracy_score(Y_valid, y_pred) * 100
        accuracies[model_name] = acc
        st.write(f"{model_name}: {acc:.2f}%")

    selected_model_name = st.selectbox("Select Model for Prediction", list(models.keys()))
    selected_model = models[selected_model_name]

    # --- Predict Next Day Trend ---
    latest_features = df[feature_cols].iloc[-1].values.reshape(1, -1)
    latest_features_scaled = scaler.transform(latest_features)
    pred_prob = selected_model.predict_proba(latest_features_scaled)[0]
    pred_class = selected_model.predict(latest_features_scaled)[0]

    st.subheader("Next Day Prediction")
    if pred_class == 1:
        st.success(f"The stock {stock_symbol} is likely to go UP tomorrow with probability {pred_prob[1]*100:.2f}%")
    else:
        st.error(f"The stock {stock_symbol} is likely to go DOWN tomorrow with probability {pred_prob[0]*100:.2f}%")

    # --- Display News Sentiment ---
    st.subheader("Latest News Sentiment")
    st.write(f"Sentiment score based on recent news headlines: {sentiment_score:.3f} (Range: -1 negative to +1 positive)")
    if headlines:
        st.write("Sample Headlines:")
        for headline in headlines[:5]:
            st.write(f"- {headline}")
    else:
        st.write("No recent news headlines found or API error.")

else:
    if authentication_status is False:
        st.error("Username/password is incorrect")
    elif authentication_status is None:
        st.warning("Please enter your username and password")


st.markdown(response_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
