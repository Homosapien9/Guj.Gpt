# =========================
# IMPORTS 
# =========================
import numpy as np
import pandas as pd
import xgboost as xgb
import yfinance as yf
import streamlit as st
from datetime import datetime
import matplotlib.pyplot as plt
from PIL import Image
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
import copy

# =========================
# MODEL DEFINITIONS (global)
# =========================
MODELS = {
    "Random Forest": RandomForestClassifier(
        n_estimators=500,
        max_depth=6,
        min_samples_leaf=20,
        max_features='sqrt',
        class_weight='balanced',
        random_state=50,
        n_jobs=-1
    ),
    "Gradient Boosting": GradientBoostingClassifier(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=5,
        random_state=50
    ),
    "XGBoost": xgb.XGBClassifier(
        n_estimators=300,
        max_depth=4,
        learning_rate=0.03,
        subsample=0.8,
        colsample_bytree=0.8,
        min_child_weight=10,
        eval_metric='logloss',
        random_state=50
    ),
    "Decision Tree": DecisionTreeClassifier(
        max_depth=6,
        class_weight='balanced',
        random_state=50
    )
}

# =========================
# SESSION STATE
# =========================
if 'portfolio' not in st.session_state:
    st.session_state['portfolio'] = []

if 'watchlist' not in st.session_state:
    st.session_state['watchlist'] = []

# =========================
# DATA FETCH (cached)
# =========================
@st.cache_data(ttl=300)
def get_stock_data(stock_symbol, start_date, end_date):
    """Download stock data with error handling (5-min cache)."""
    try:
        df = yf.download(stock_symbol, start=start_date, end=end_date, auto_adjust=True)
        if 'Adj Close' in df.columns:
            df.drop(columns=['Adj Close'], inplace=True)
        return df
    except Exception as e:
        st.error(f"Error fetching stock data: {e}")
        return pd.DataFrame()

# Safe close price extractor for yfinance multi-level columns
def get_close_series(data):
    close = data['Close']
    if isinstance(close, pd.Series):
        return close.dropna()
    if isinstance(close, pd.DataFrame):
        return close.squeeze().dropna()
    return pd.Series(close).dropna()

# =========================
# INDICATOR FUNCTIONS
# =========================
def compute_rsi(df, window=14):
    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0.0).rolling(window).mean()
    loss = (-delta.where(delta < 0, 0.0)).rolling(window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def plot_rsi(df, window=14):
    df_plot = df.copy()
    df_plot['RSI'] = compute_rsi(df_plot, window)
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df_plot.index, df_plot['RSI'], label="RSI", color="blue")
    ax.axhline(70, color='red', linestyle='--', label="Overbought (70)")
    ax.axhline(30, color='green', linestyle='--', label="Oversold (30)")
    ax.set_title('Relative Strength Index (RSI)', fontsize=15)
    ax.set_xlabel('Date')
    ax.set_ylabel('RSI Value')
    ax.legend(loc="upper left")
    st.pyplot(fig)

def compute_macd(df, fast=12, slow=26, signal=9):
    macd_line = df['Close'].ewm(span=fast, adjust=False).mean() - \
                df['Close'].ewm(span=slow, adjust=False).mean()
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    return macd_line, signal_line

def compute_stochastic(df, window=14):
    low_min = df['Low'].rolling(window=window).min()
    high_max = df['High'].rolling(window=window).max()
    stochastic = 100 * (df['Close'] - low_min) / (high_max - low_min)
    return stochastic

def compute_bollinger_bands(df, window=20):
    df = df.copy()
    df['Middle_BB'] = df['Close'].rolling(window=window).mean()
    df['Std_Dev'] = df['Close'].rolling(window=window).std()
    df['Upper_BB'] = df['Middle_BB'] + (df['Std_Dev'] * 2)
    df['Lower_BB'] = df['Middle_BB'] - (df['Std_Dev'] * 2)
    return df

def plot_bollinger_bands(df, window=20):
    df_plot = compute_bollinger_bands(df, window)
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df_plot.index, df_plot['Close'], label='Close Price', color='blue')
    ax.plot(df_plot.index, df_plot['Upper_BB'], label='Upper Bollinger Band', color='red', linestyle='--')
    ax.plot(df_plot.index, df_plot['Middle_BB'], label='Middle Bollinger Band (SMA)', color='orange', linestyle='--')
    ax.plot(df_plot.index, df_plot['Lower_BB'], label='Lower Bollinger Band', color='green', linestyle='--')
    ax.fill_between(df_plot.index, df_plot['Upper_BB'], df_plot['Lower_BB'], color='gray', alpha=0.2)
    ax.set_title('Bollinger Bands', fontsize=15)
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.legend(loc='upper left')
    st.pyplot(fig)

def compute_volumetric_data(df):
    df = df.copy()
    df['Buy_Volume'] = df['Volume'].where(df['Close'] > df['Open'], 0)
    df['Sell_Volume'] = df['Volume'].where(df['Close'] <= df['Open'], 0)
    return df

def plot_volumetric_chart(df):
    st.write("Volume chart tracks the number of shares/contracts traded.")
    st.write("High volume: Confirms price trends (up or down).")
    st.write("Low volume: Signals lack of interest or indecision.")
    df_vol = compute_volumetric_data(df)
    fig, ax = plt.subplots(figsize=(15, 7))
    ax.bar(df_vol.index, df_vol['Buy_Volume'], color='green', alpha=0.6, label='Buying Pressure')
    ax.bar(df_vol.index, df_vol['Sell_Volume'], color='red', alpha=0.6, label='Selling Pressure')
    ax.set_title('Volumetric Chart: Buying vs Selling Pressure', fontsize=15)
    ax.set_xlabel('Date')
    ax.set_ylabel('Volume')
    ax.legend(loc='upper left')
    st.pyplot(fig)

# =========================
# SIGNAL SUMMARY CARD
# =========================
def get_signal_summary(df):
    signals = {}
    # RSI
    rsi_val = compute_rsi(df).iloc[-1]
    signals['RSI'] = 'Buy' if rsi_val < 30 else ('Sell' if rsi_val > 70 else 'Neutral')
    # MACD
    macd_line, signal_line = compute_macd(df)
    signals['MACD'] = 'Buy' if macd_line.iloc[-1] > signal_line.iloc[-1] else 'Sell'
    # Bollinger Bands
    bb = compute_bollinger_bands(df)
    price = df['Close'].iloc[-1]
    signals['Bollinger'] = 'Buy' if price < bb['Lower_BB'].iloc[-1] else \
                           ('Sell' if price > bb['Upper_BB'].iloc[-1] else 'Neutral')
    # Stochastic
    stoch_val = compute_stochastic(df).iloc[-1]
    signals['Stoch'] = 'Buy' if stoch_val < 20 else ('Sell' if stoch_val > 80 else 'Neutral')

    buys = sum(1 for v in signals.values() if v == 'Buy')
    sells = sum(1 for v in signals.values() if v == 'Sell')
    if buys >= 3:
        overall = 'BULLISH 🟢'
    elif sells >= 3:
        overall = 'BEARISH 🔴'
    else:
        overall = 'NEUTRAL 🟡'
    return signals, overall

# =========================
# FEATURE ENGINEERING
# =========================
def add_features(df):
    """Add technical features and target for the model (ML‑ready)."""
    df = df.copy()
    df['Return']     = df['Close'].pct_change()
    df['SMA_10']     = df['Close'].rolling(10).mean()
    df['SMA_50']     = df['Close'].rolling(50).mean()
    df['EMA_10']     = df['Close'].ewm(span=10).mean()
    df['Volatility'] = df['Close'].rolling(10).std()
    df['Momentum']   = df['Close'] - df['Close'].shift(5)
    df['Lag1']       = df['Close'].shift(1)
    df['Lag2']       = df['Close'].shift(2)
    df['Lag3']       = df['Close'].shift(3)

    # RSI
    delta = df['Close'].diff()
    gain  = delta.where(delta > 0, 0.0).rolling(14).mean()
    loss  = (-delta.where(delta < 0, 0.0)).rolling(14).mean()
    df['RSI'] = 100 - (100 / (1 + gain / loss))

    # MACD gap
    macd   = df['Close'].ewm(span=12).mean() - df['Close'].ewm(span=26).mean()
    signal = macd.ewm(span=9).mean()
    df['MACD_gap'] = macd - signal

    # Bollinger Band position
    mid = df['Close'].rolling(20).mean()
    std = df['Close'].rolling(20).std()
    df['BB_position'] = (df['Close'] - (mid - 2*std)) / (4 * std)

    # Stochastic
    low14  = df['Low'].rolling(14).min()
    high14 = df['High'].rolling(14).max()
    df['Stoch'] = 100 * (df['Close'] - low14) / (high14 - low14)

    # SMA crossover
    df['SMA_cross'] = df['SMA_10'] - df['SMA_50']

    df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
    df.dropna(inplace=True)
    return df

# =========================
# ROI CALCULATOR
# =========================
def calculate_advanced_roi(ticker, start_date, investment):
    df = get_stock_data(ticker, start_date, datetime.now().date().strftime('%Y-%m-%d'))
    benchmark = get_stock_data("^BSESN", start_date, datetime.now().date().strftime('%Y-%m-%d'))

    if df.empty or benchmark.empty:
        return None

    close_prices = get_close_series(df)
    bench_close = get_close_series(benchmark)

    start_price = float(close_prices.iloc[0])
    current_price = float(close_prices.iloc[-1])

    shares = investment / start_price
    final_value = shares * current_price
    total_return_pct = (final_value - investment) / investment * 100

    days = (close_prices.index[-1] - close_prices.index[0]).days
    years = days / 365
    cagr = ((final_value / investment) ** (1 / years) - 1) * 100

    returns = close_prices.pct_change().dropna()
    volatility = returns.std() * np.sqrt(252) * 100

    risk_free_rate = 0.06
    sharpe = (cagr/100 - risk_free_rate) / (volatility/100)

    bench_return = (bench_close.iloc[-1] - bench_close.iloc[0]) / bench_close.iloc[0] * 100

    return {
        "Final Value": float(final_value),
        "Total Return %": float(total_return_pct),
        "CAGR %": float(cagr),
        "Volatility %": float(volatility),
        "Sharpe Ratio": float(sharpe),
        "Sensex Return %": float(bench_return)
    }

# =========================
# STREAMLIT UI
# =========================
qr_image = Image.open("Website qr.png")
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<h1 style="color: white; font-size: 29.7px;">MarketMantra - Stock Trend Predictor</h1>', unsafe_allow_html=True)
    st.subheader("~ Developed By Jatan Shah")
with col2:
    st.image(qr_image, caption="scan for website", width=100)

with st.expander("Select Stock And Data Range (Minimum 5 Days Gap)"):
    st.header("Stock Selection")
    stock_symbol = st.text_input("Select Stock Symbol", value="^BSESN").upper()
    start_date = st.date_input("Start Date", pd.to_datetime("2024-01-01"))
    end_date = st.date_input("End Date", datetime.now().date())

with st.expander("Select Technical Indicators"):
    st.header("Technical Indicators")
    indicator_options = [
        "50-Day Simple Moving Average (SMA)",
        "200-Day Simple Moving Average (SMA)",
        "MACD (Moving Average Convergence Divergence)",
        "Stochastic Oscillator",
        "Bollinger Bands",
        "Relative Strength Index (RSI)",
        "Volume Chart"
    ]
    selected_indicators = st.multiselect(
        "Select Technical Indicators to Display",
        indicator_options,
        default=["50-Day Simple Moving Average (SMA)",
                 "200-Day Simple Moving Average (SMA)"]
    )

sma_50 = "50-Day Simple Moving Average (SMA)" in selected_indicators
sma_200 = "200-Day Simple Moving Average (SMA)" in selected_indicators
macd_ind = "MACD (Moving Average Convergence Divergence)" in selected_indicators
stochastic_ind = "Stochastic Oscillator" in selected_indicators
bollinger_ind = "Bollinger Bands" in selected_indicators
rsi_ind = "Relative Strength Index (RSI)" in selected_indicators
volume_ind = "Volume Chart" in selected_indicators

# ---- Fetch data ----
df_raw = get_stock_data(stock_symbol, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
if df_raw.empty:
    st.warning("No data found for the selected stock or date range. Model needs at least 5 days to predict results.")
    st.stop()

# ---- Data Visualization ----
with st.expander("Data Visualization"):
    st.subheader(f"Stock Data for {stock_symbol}")
    st.write(f"Historical data for {stock_symbol} from {start_date} to {end_date}, in its listed currency")
    st.dataframe(df_raw.tail())

    st.subheader("Closing Price Over Time")
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df_raw['Close'], label='Close Price', color='blue')
    ax.set_title(f"{stock_symbol} - Closing Price History", fontsize=15)
    ax.set_ylabel('Price', fontsize=12)
    ax.set_xlabel('Date', fontsize=12)
    ax.grid(True)
    plt.legend()
    st.pyplot(fig)

# ---- Portfolio & Watchlist buttons ----
st.header("Portfolio & Watchlist")
col_btn1, col_btn2, _, _ = st.columns(4)
with col_btn1:
    portfolio_add = st.button("Add to Portfolio")
with col_btn2:
    watchlist_add = st.button("Add to Watchlist")

if portfolio_add:
    if stock_symbol not in st.session_state['portfolio']:
        st.session_state['portfolio'].append(stock_symbol)
        st.success(f"{stock_symbol} added to Portfolio.")
    else:
        st.warning(f"{stock_symbol} is already in your Portfolio.")

if watchlist_add:
    if stock_symbol not in st.session_state['watchlist']:
        st.session_state['watchlist'].append(stock_symbol)
        st.success(f"{stock_symbol} added to Watchlist.")
    else:
        st.warning(f"{stock_symbol} is already in your Watchlist.")

# ---- Feature engineering for ML ----
df_ml = add_features(df_raw)

# ---- Tabs ----
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Portfolio", "Watchlist", "Technical Indicators", "Predictions", "Calculate ROI"])

# ---------- Tab 1: Portfolio ----------
with tab1:
    st.subheader("Manage Your Portfolio")
    if st.session_state['portfolio']:
        for stock in st.session_state['portfolio']:
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.write(f"**{stock}**")
            with col_b:
                if st.button(f"Remove {stock}", key=f"remove_port_{stock}"):
                    st.session_state['portfolio'].remove(stock)
                    st.rerun()
    else:
        st.write("No Stocks in your portfolio yet.")

# ---------- Tab 2: Watchlist ----------
with tab2:
    st.subheader("Manage Your Watchlist")
    if st.session_state['watchlist']:
        for stock in st.session_state['watchlist']:
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.write(f"**{stock}**")
            with col_b:
                if st.button(f"Remove {stock}", key=f"remove_watch_{stock}"):
                    st.session_state['watchlist'].remove(stock)
                    st.rerun()
    else:
        st.write("No Stocks in your watchlist yet.")

# ---------- Tab 3: Technical Indicators ----------
with tab3:
    st.subheader("Technical Indicators")
    # Signal summary card
    signals, overall = get_signal_summary(df_raw)
    st.subheader(f"Overall Signal: {overall}")
    cols = st.columns(4)
    for i, (ind, sig) in enumerate(signals.items()):
        color = 'green' if sig == 'Buy' else ('red' if sig == 'Sell' else 'orange')
        cols[i].markdown(f"**{ind}** \n:{color}[{sig}]")

    # Trend regime
    sma50_vals = df_raw['Close'].rolling(50).mean()
    sma200_vals = df_raw['Close'].rolling(200).mean()
    sma50_val = sma50_vals.iloc[-1]
    sma200_val = sma200_vals.iloc[-1]
    curr_price = float(df_raw['Close'].iloc[-1])
    if curr_price > sma50_val and curr_price > sma200_val:
        regime = "📈 UPTREND — price above both SMA-50 and SMA-200"
        regime_color = "success"
    elif curr_price < sma50_val and curr_price < sma200_val:
        regime = "📉 DOWNTREND — price below both SMA-50 and SMA-200"
        regime_color = "error"
    else:
        regime = "↔️ SIDEWAYS — mixed signals from SMA-50 and SMA-200"
        regime_color = "warning"
    getattr(st, regime_color)(f"Current regime: {regime}")

    if sma_50:
        st.header("Simple Moving Average (SMA) of 50 Days")
        st.write("The **50-day** SMA looks at the average price over the last 50 days (last 50 days shown).")
        # Work on a copy to avoid mutating df_raw
        df_plot = df_raw.copy()
        df_plot['SMA_50'] = df_plot['Close'].rolling(window=50).mean()
        sma50_plot = df_plot['SMA_50'].dropna().iloc[-50:]
        fig, ax = plt.subplots(figsize=(15, 5))
        ax.plot(df_plot['Close'], label='Close Price', color='blue', alpha=0.4)
        ax.plot(sma50_plot, label="50-Day SMA", color='orange')
        ax.set_title(f"{stock_symbol} - 50-Day Simple Moving Average", fontsize=15)
        ax.set_ylabel('Price', fontsize=12)
        ax.set_xlabel('Date', fontsize=12)
        ax.legend(loc='best')
        st.pyplot(fig)

    if sma_200:
        st.header("Simple Moving Average (SMA) of 200 Days")
        st.write("The **200-day** SMA looks at the average price over the last 200 days (last 200 days shown).")
        df_plot = df_raw.copy()
        df_plot['SMA_200'] = df_plot['Close'].rolling(window=200).mean()
        sma200_plot = df_plot['SMA_200'].dropna().iloc[-200:]
        fig, ax = plt.subplots(figsize=(15, 5))
        ax.plot(df_plot['Close'], label='Close Price', color='blue', alpha=0.4)
        ax.plot(sma200_plot, label="200-Day SMA", color='green')
        ax.set_title(f"{stock_symbol} - 200-Day Simple Moving Average", fontsize=15)
        ax.set_ylabel('Price', fontsize=12)
        ax.set_xlabel('Date', fontsize=12)
        ax.legend(loc='best')
        st.pyplot(fig)

    if macd_ind:
        st.header("MACD (Moving Average Convergence Divergence)")
        st.write("If the **MACD line** is higher than the **signal line**, the asset price could go **up**.")
        st.write("If the **MACD line** is lower than the **signal line**, the asset price could go **down**.")
        macd_line, signal_line = compute_macd(df_raw)
        fig, ax = plt.subplots(figsize=(15, 5))
        ax.plot(macd_line, label="MACD", color='blue')
        ax.plot(signal_line, label="Signal Line", color='orange')
        ax.set_title(f"{stock_symbol} - MACD", fontsize=15)
        ax.set_ylabel('Value', fontsize=12)
        ax.set_xlabel('Date', fontsize=12)
        ax.legend(loc='best')
        st.pyplot(fig)

    if stochastic_ind:
        st.header("Stochastic Oscillator")
        st.write("Above **80** → might be overbought (could come down). Below **20** → might be oversold (could go up).")
        stochastic_oscillator = compute_stochastic(df_raw)
        fig, ax = plt.subplots(figsize=(15, 5))
        ax.plot(stochastic_oscillator, label="Stochastic Oscillator", color='green')
        ax.axhline(80, linestyle='--', color='red')
        ax.axhline(20, linestyle='--', color='blue')
        ax.set_title(f"{stock_symbol} - Stochastic Oscillator", fontsize=15)
        ax.set_ylabel('Stochastic Value', fontsize=12)
        ax.set_xlabel('Date', fontsize=12)
        ax.legend(loc='best')
        st.pyplot(fig)

    if bollinger_ind:
        st.subheader("Bollinger Bands")
        st.write("If price hits/exceeds the **upper band**, potential **sell**. If it drops below the **lower band**, potential **buy**.")
        plot_bollinger_bands(df_raw)

    if rsi_ind:
        st.subheader("Relative Strength Index (RSI)")
        st.write("RSI above **70** → overbought (sell). RSI below **30** → oversold (buy).")
        plot_rsi(df_raw)

    if volume_ind:
        st.subheader("Volume Chart")
        plot_volumetric_chart(df_raw)

# ---------- Tab 4: Predictions ----------
with tab4:
    st.subheader("Predictions For Next Day's Trading")
    if df_ml.empty:
        st.error("Not enough data after feature engineering. Select a larger date range.")
    else:
        features = df_ml[[
            'Return', 'SMA_10', 'SMA_50', 'EMA_10', 'Volatility', 'Momentum',
            'Lag1', 'Lag2', 'Lag3',
            'RSI', 'MACD_gap', 'BB_position', 'Stoch', 'SMA_cross'
        ]]
        target = df_ml['Target']

        # Deepcopy fresh models for each run
        models = copy.deepcopy(MODELS)

        # Time-series cross-validation
        tscv = TimeSeriesSplit(n_splits=5)
        cv_scores = {name: [] for name in models}

        with st.spinner("Training models and computing predictions..."):
            for train_idx, test_idx in tscv.split(features):
                X_tr, X_te = features.iloc[train_idx], features.iloc[test_idx]
                y_tr, y_te = target.iloc[train_idx], target.iloc[test_idx]

                scaler = StandardScaler()
                X_tr_s = scaler.fit_transform(X_tr)
                X_te_s = scaler.transform(X_te)

                for name, model in models.items():
                    model.fit(X_tr_s, y_tr)
                    score = accuracy_score(y_te, model.predict(X_te_s))
                    cv_scores[name].append(score)

        st.subheader("Cross‑Validation Results (5‑fold)")
        for name, scores in cv_scores.items():
            mean = np.mean(scores) * 100
            std  = np.std(scores) * 100
            st.write(f"{name}: {mean:.1f}% ± {std:.1f}%")

        # Retrain on full data for evaluation & ensemble
        split = int(len(features) * 0.7)
        X_train, X_test = features[:split], features[split:]
        y_train, y_test = target[:split], target[split:]

        scaler_full = StandardScaler()
        X_train_scaled = scaler_full.fit_transform(X_train)
        X_test_scaled = scaler_full.transform(X_test)

        for name, model in models.items():
            model.fit(X_train_scaled, y_train)

        probs = []
        model_accuracies = {}
        for name, model in models.items():
            y_pred = model.predict(X_test_scaled)
            acc = accuracy_score(y_test, y_pred) * 100
            model_accuracies[name] = acc
            probs.append(model.predict_proba(X_test_scaled)[:, 1])

        avg_prob = np.mean(probs, axis=0)
        final_preds = (avg_prob > 0.5).astype(int)
        ensemble_acc = accuracy_score(y_test, final_preds) * 100

        # Baseline comparison
        baseline = target.mean() * 100
        baseline = max(baseline, 100 - baseline)

        col1, col2, col3 = st.columns(3)
        col1.metric("Ensemble Accuracy", f"{ensemble_acc:.1f}%")
        col2.metric("Baseline (always guess majority)", f"{baseline:.1f}%")

        beat = ensemble_acc - baseline
        if beat > 3:
            col3.metric("Edge over baseline", f"+{beat:.1f}%", delta="Model is learning")
        elif beat > 0:
            col3.metric("Edge over baseline", f"+{beat:.1f}%", delta="Marginal edge")
        else:
            col3.metric("Edge over baseline", f"{beat:.1f}%", delta="No edge — check features",
                        delta_color="inverse")

        up_pct = target.mean() * 100
        if up_pct > 65 or up_pct < 35:
            st.warning(f"⚠️ Imbalanced data: stock went UP {up_pct:.0f}% of days. "
                       f"Models already use class_weight='balanced' where applicable.")

        # Confusion matrix
        cm = confusion_matrix(y_test, final_preds)
        fig, ax = plt.subplots(figsize=(6, 5))
        cax = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
        fig.colorbar(cax)
        classes = ['Down', 'Up']
        ax.set(xticks=np.arange(len(classes)), yticks=np.arange(len(classes)),
               xticklabels=classes, yticklabels=classes,
               title="Confusion Matrix", ylabel="True Value", xlabel="Predicted Value")
        for i in range(2):
            for j in range(2):
                ax.text(j, i, format(cm[i, j], 'd'), ha="center", va="center", color="black")
        st.pyplot(fig)

        # Rolling accuracy chart
        st.subheader("Model Consistency Over Time")
        results_df = pd.DataFrame({'Actual': y_test.values, 'Predicted': final_preds})
        results_df['Correct'] = (results_df['Actual'] == results_df['Predicted'])
        results_df['Correct_int'] = results_df['Correct'].astype(int)
        rolling_acc = results_df['Correct_int'].rolling(30).mean() * 100
        fig, ax = plt.subplots(figsize=(15, 3))
        ax.plot(rolling_acc, color='steelblue', label='30-day rolling accuracy')
        ax.axhline(50, color='red', linestyle='--', alpha=0.5, label='Random (50%)')
        ax.axhline(baseline, color='orange', linestyle='--', alpha=0.5, label=f'Baseline ({baseline:.0f}%)')
        ax.set_ylabel('Accuracy %'); ax.set_ylim(30, 80)
        ax.legend(); ax.set_title("Rolling 30-day model accuracy")
        st.pyplot(fig)

        # Individual model accuracies
        st.subheader("Individual Model Accuracies")
        selected_model_name = st.selectbox("Select Model", list(models.keys()))
        st.write(f"{selected_model_name} Accuracy: {model_accuracies[selected_model_name]:.2f}%")

        # Feature importance
        st.subheader("What the model actually learned")
        rf_model = models["Random Forest"]
        importances = pd.Series(
            rf_model.feature_importances_,
            index=features.columns
        ).sort_values(ascending=False)

        fig, ax = plt.subplots(figsize=(10, 4))
        importances.head(8).plot(kind='bar', ax=ax, color='steelblue')
        ax.set_title("Top 8 features driving predictions (Random Forest)", fontsize=13)
        ax.set_ylabel("Importance score")
        ax.set_xlabel("")
        plt.xticks(rotation=30, ha='right')
        st.pyplot(fig)

        # Next day prediction with confidence threshold
        latest_features = scaler_full.transform(features.iloc[-1:].values)
        latest_probs = [m.predict_proba(latest_features)[0][1] for m in models.values()]
        final_up_prob = np.mean(latest_probs)

        st.subheader("Next Day Prediction")
        CONFIDENCE_THRESHOLD = 0.60
        if final_up_prob >= CONFIDENCE_THRESHOLD:
            st.success(f"📈 UP — {final_up_prob*100:.1f}% confidence")
        elif final_up_prob <= (1 - CONFIDENCE_THRESHOLD):
            st.error(f"📉 DOWN — {(1-final_up_prob)*100:.1f}% confidence")
        else:
            st.warning(f"⚠️ No clear signal — model is {final_up_prob*100:.1f}% towards UP. "
                       f"Wait for a stronger signal before acting.")
        st.progress(int(final_up_prob * 100))

        # Disclaimer
        st.markdown("---")
        st.caption(
            "⚠️ DISCLAIMER: These predictions are generated by machine learning models "
            "trained on historical price data. They do not constitute financial advice. "
            "Past performance does not guarantee future results. Always do your own "
            "research before making investment decisions. MarketMantra is a decision "
            "support tool, not a trading system."
        )

# ---------- Tab 5: ROI Calculator ----------
with tab5:
    st.subheader("Advanced Investment Analytics")

    roi_start_date = st.date_input(
        "Investment Start Date",
        pd.to_datetime("2016-01-01"),
        key="roi_start"
    )
    investment_amount = st.number_input(
        "Investment Amount (₹)",
        min_value=1000,
        value=100000,
        step=1000
    )

    if st.button("Calculate Advanced ROI"):
        with st.spinner("Fetching market data and computing ROI..."):
            result = calculate_advanced_roi(stock_symbol, roi_start_date, investment_amount)

        if result:
            col1, col2, col3 = st.columns(3)
            col1.metric("Final Value", f"₹{result['Final Value']:,.0f}")
            col2.metric("Total Return", f"{result['Total Return %']:.2f}%")
            col3.metric("CAGR", f"{result['CAGR %']:.2f}%")

            col4, col5 = st.columns(2)
            col4.metric("Volatility", f"{result['Volatility %']:.2f}%")
            col5.metric("Sharpe Ratio", f"{result['Sharpe Ratio']:.2f}")

            st.subheader("Investment Growth Over Time")
            stock_df = get_stock_data(
                stock_symbol,
                roi_start_date.strftime('%Y-%m-%d'),
                datetime.now().date().strftime('%Y-%m-%d')
            )
            if stock_df.empty:
                st.error("Could not fetch data. Check ticker symbol.")
            else:
                close_series = get_close_series(stock_df)
                normalized = close_series / close_series.iloc[0]
                investment_growth = normalized * investment_amount

                fig, ax = plt.subplots(figsize=(12,5))
                ax.plot(investment_growth, label=f"{stock_symbol} Investment Value")
                ax.set_ylabel("Portfolio Value (₹)")
                ax.set_xlabel("Date")
                ax.legend()
                st.pyplot(fig)

# ---- Footer ----
st.markdown("---")
st.caption("MarketMantra – combining technical analysis with machine learning for smarter trading decisions.")
