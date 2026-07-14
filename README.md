# 馃搱 News-Based Trading Signal Bot (Telegram) 鈥� Professional Edition

Yeh bot free, real-time RSS news feeds scan karta hai (results, elections,
RBI policy, smart money moves), stock ka naam aur sentiment nikalta hai,
**live price se target/stoploss calculate karta hai**, aur sirf
**high-probability + high risk-reward** signals Telegram pe bhejta hai 鈥�
24x7, automatically, bina kisi laptop/mobile ko chalu rakhe.

> 鈿狅笍 **Disclaimer:** Yeh tool ek rule-based news + volatility filtering
> system hai. Koi bhi signal 100% guaranteed profit nahi deta. Stock
> market me risk hamesha rehta hai. Yeh financial advice nahi hai 鈥� apna
> research aur risk management khud karo. Pehle **paper trading** (bina
> asli paise ke) se test karo.

---

## 馃 Yeh kaam kaise karta hai

```
[RSS News Feeds] --> [Stock naam pehchano] --> [Sentiment check karo]
                                                        |
                                        Confidence >= 75? ---- NO ---> Skip
                                                        |
                                                       YES
                                                        |
                                        [Live price se ATR/target/stoploss nikalo]
                                                        |
                                        Risk:Reward >= 1.5? ---- NO ---> Skip
                                                        |
                                                       YES
                                                        |
                                              [Telegram Signal bhejo]
```

1. **`news_fetcher.py`** 鈥� Moneycontrol, LiveMint, Economic Times, Business
   Standard ke free RSS feeds se har 3 minute me latest news uthata hai.
2. **`stock_mapper.py`** 鈥� news text me se company ka naam dhundh kar uska
   NSE symbol nikalta hai (152 F&O stocks, `data/stock_symbols.json` me).
3. **`sentiment_analyzer.py`** 鈥� financial keywords ka weight-based score
   nikal kar BUY/SELL/NEUTRAL + category (Results/Smart Money/Election-Macro
   /Corporate Action/Regulatory) decide karta hai.
4. **`price_fetcher.py`** 鈥� Yahoo Finance se free live/recent price data laata hai.
5. **`risk_calculator.py`** 鈥� ATR (volatility) ke basis pe Entry, Stoploss,
   Target1, Target2 aur Risk:Reward ratio calculate karta hai.
6. **`signal_generator.py`** 鈥� sabko jodta hai, sirf tabhi signal deta hai
   jab: stock + direction clear ho + confidence high ho + risk-reward achha ho.
7. **`telegram_bot.py`** 鈥� professional formatted message Telegram pe bhejta hai.
8. **`main.py`** 鈥� Flask web-service + background scheduler; Render pe 24x7 chalta hai.

---

## 馃洜锔� Local Setup (test karne ke liye)

### 1. Telegram Bot banao
1. Telegram me **@BotFather** ko message karo
2. `/newbot` command bhejo, naam aur username do
3. Woh tumhe ek **token** dega 鈥� usse copy kar lo
4. Apne bot ko ek message bhejo (ya jis group/channel me signal chahiye
   wahan add karo)
5. Apna **Chat ID** nikalne ke liye **@userinfobot** ko message karo
   (ya group ke liye group me add karke `@RawDataBot` use karo)

### 2. Project setup
```bash
git clone <tumhari-repo-url>
cd news-trading-signals-bot
python3 -m venv venv
source venv/bin/activate      # Windows pe: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. `.env` file banao
```bash
cp .env.example .env
```
Fir `.env` file kholo aur apna `TELEGRAM_BOT_TOKEN` aur `TELEGRAM_CHAT_ID` daal do.

### 4. Bot chalao
```bash
python3 main.py
```
Bot chalte hi ek "started" message aayega Telegram pe. Yeh ek chhota web
server bhi start karega (`http://localhost:8080/ping`) 鈥� Render pe deploy
karte waqt yehi zaroori hai.

---

## 鈿� Option 0: GitHub Actions (SABSE AASAN, bilkul free, no extra signup)

Agar tumhare TELEGRAM_BOT_TOKEN aur TELEGRAM_CHAT_ID **GitHub Secrets** me
already save hain, to yeh sabse simple tareeka hai 鈥� koi Render/UptimeRobot
setup nahi chahiye, sab kuch GitHub ke andar hi ho jaata hai.

### Manual signal check (jab chaho button dabao)
1. GitHub pe apni repo kholo
2. **"Actions"** tab pe click karo
3. Left side me **"News Trading Signal Check"** workflow select karo
4. **"Run workflow"** button dabao (dropdown se "main" branch select rahega)
5. 30-60 second me run complete ho jaayega, agar signal mila to Telegram
   pe aa jaayega

### Automatic (har 10 minute, market hours me, khud chalega)
`.github/workflows/news-signals.yml` file me pehle se ek **schedule** set
hai 鈥� Mon-Fri, market hours (9 AM - 3:35 PM IST ke aas-paas), har 10
minute me automatically chalega. Kuch alag se karne ki zaroorat nahi,
bas ek baar code push karne ke baad ye khud-ba-khud shuru ho jaayega.

### GitHub Secrets check kar lo
Settings 鈫� Secrets and variables 鈫� Actions me yeh dono hone chahiye:
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

### 鈿狅笍 Is method ki limitations
- GitHub free tier me **private repo** ke liye 2000 minutes/month milte
  hain (public repo unlimited hai) 鈥� har run ~1 minute leta hai, to
  ~2000 checks/month tak free hai, jo kaafi zyada hai
- GitHub scheduled workflows kabhi-kabhi 5-15 minute tak **delay** ho
  sakte hain jab GitHub ke servers busy hon (yeh Render se zyada common
  hai, kyunki GitHub scheduled jobs ki koi timing guarantee nahi deta)
- Agar repo me **60 din tak koi activity na ho**, GitHub automatically
  scheduled workflows **disable** kar deta hai (manual trigger se wapas
  activate ho jaata hai)
- Isliye agar tumhe **zyada reliable, low-latency** chahiye, Option A
  (Render) better hai. GitHub Actions casual/backup use ke liye best hai.

---

## 馃殌 GitHub Repository Banane Ka Poora Process

### Option A: GitHub website se (sabse aasan)
1. [github.com](https://github.com) pe login karo (account nahi hai to free
   sign up kar lo)
2. Top-right corner me **"+"** icon pe click karo 鈫� **"New repository"**
3. **Repository name** do: `news-trading-signals-bot`
4. **Description** (optional): "News-based trading signal bot for Telegram"
5. **Public** ya **Private** choose karo (Private better hai agar apni
   strategy secret rakhni ho)
6. 鈿狅笍 **"Add a README file"** ko **UNCHECK** rakho (kyunki apna README already
   hai)
7. **"Create repository"** button dabao
8. Ab tumhe ek URL milega jaise: `https://github.com/tumhara-username/news-trading-signals-bot.git`

### Option B: Command line se code push karna
Terminal me project folder ke andar jaake ye commands chalao:

```bash
git init
git add .
git commit -m "Initial commit: professional news-based trading signal bot"
git branch -M main
git remote add origin https://github.com/tumhara-username/news-trading-signals-bot.git
git push -u origin main
```

Agar pehli baar push kar rahe ho to GitHub tumse login maangega:
- **Username**: apna GitHub username
- **Password**: yahan normal password kaam nahi karega 鈥� GitHub ab
  **Personal Access Token (PAT)** maangta hai:
  1. GitHub pe Settings 鈫� Developer settings 鈫� Personal access tokens 鈫�
     Tokens (classic)
  2. "Generate new token" 鈫� scopes me `repo` select karo
  3. Token copy kar lo aur password ki jagah use karo

### Baad me changes push karne ke liye
```bash
git add .
git commit -m "yaha likho kya change kiya"
git push
```

### 鈿狅笍 Zaroori: `.env` file kabhi GitHub pe mat daalna
`.gitignore` file already `.env` ko exclude kar rahi hai. Double-check
zaroor karna, kyunki usme tumhara Telegram bot token hota hai.

---

## 馃寪 Option A: Render.com pe FREE 24x7 Deployment (zyada reliable)

Render ka free web-service tier use karenge. Limitation: 15 minute tak
request na aaye to service so jaati hai. Isko fix karne ke liye ek free
"ping" service (UptimeRobot) use karenge jo har 5 minute me bot ko
jagata rahega 鈥� result: **free, 24x7 running bot**.

### Step 1: Render pe account banao aur deploy karo
1. [render.com](https://render.com) pe GitHub se free sign up karo
2. Dashboard me **"New +"** 鈫� **"Web Service"**
3. Apni GitHub repository connect karo (`news-trading-signals-bot`)
4. Settings:
   - **Name**: `news-trading-signals-bot`
   - **Region**: Singapore (India ke sabse paas)
   - **Branch**: `main`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
   - **Instance Type**: **Free**
5. **"Advanced"** 鈫� Environment Variables daalo:
   - `TELEGRAM_BOT_TOKEN` = apna bot token
   - `TELEGRAM_CHAT_ID` = apna chat ID
   - `POLL_INTERVAL_MINUTES` = `3`
   - `MIN_CONFIDENCE_SCORE` = `75`
   - `MIN_RISK_REWARD_RATIO` = `1.5`
6. **"Create Web Service"** dabao 鈥� 2-5 minute me deploy ho jaayega
7. Deploy hone ke baad URL milega: `https://news-trading-signals-bot.onrender.com`

### Step 2: Bot ko 24x7 jagaye rakhne ke liye (FREE keep-alive)
1. [uptimerobot.com](https://uptimerobot.com) pe free account banao
2. **"Add New Monitor"**:
   - **Monitor Type**: HTTP(s)
   - **Friendly Name**: News Trading Bot
   - **URL**: apna Render URL + `/ping` (jaise
     `https://news-trading-signals-bot.onrender.com/ping`)
   - **Monitoring Interval**: 5 minutes
3. Save kar do

Bas! UptimeRobot har 5 minute me bot ko ping karega, woh kabhi sleep nahi
karega, aur bot khud har 3 minute me news check karke signals bhejta
rahega 鈥� **24x7, bina kisi device ko chalu rakhe**.

### Step 3: Verify karo
- Render URL browser me kholo 鈥� `{"status": "alive", ...}` JSON dikhna chahiye
- Telegram pe "Bot start ho gaya hai" message aana chahiye
- Render dashboard ke "Logs" tab me news-check activity dikhegi

### Code update karne pe kya hoga?
`git push` karne pe Render automatically naya deploy start kar dega
(auto-deploy default on hota hai).

### 鈿狅笍 Free tier ki limitations (啶堗ぎ啶距え啶︵ぞ啶班 啶膏)
- Yeh ek widely-used workaround hai, 100% guarantee nahi ki Render kabhi
  policy change na kare
- Agar signals miss hone lagen, Render ka **Starter plan ($7/month)**
  permanently fix kar deta hai (koi spin-down nahi)
- Free tier pe monthly 750 hours milte hain 鈥� single service 24x7 ke
  liye kaafi hai

---

## 鈿欙笍 Customize kaise karo

- **Aur stocks add karo**: `data/stock_symbols.json` me naya entry daalo:
  `"company name": "SYMBOL"`
- **Naye keywords add karo**: `data/sentiment_lexicon.json` me bullish/bearish
  section me `"keyword": weight` add karo (weight 10-40 ke beech rakho),
  aur `data/keyword_categories.json` me uski category bhi add kar dena
- **Confidence threshold badlo**: Render env var `MIN_CONFIDENCE_SCORE`
  change karo (zyada strict ke liye 80+, zyada signals ke liye 65-70)
- **Risk-reward threshold badlo**: `MIN_RISK_REWARD_RATIO` change karo
  (zyada aggressive ke liye 1.2, zyada conservative ke liye 2.0+)
- **US stocks / Crypto ke liye**: `data/stock_symbols.json` replace karo,
  aur `price_fetcher.py` me `.NS` suffix hata/badal do

---

## 馃搨 Project Structure
```
news-trading-signals-bot/
鈹溾攢鈹€ .github/
鈹�   鈹斺攢鈹€ workflows/
鈹�       鈹斺攢鈹€ news-signals.yml    # GitHub Actions (manual button + auto schedule)
鈹溾攢鈹€ main.py                     # Flask app + scheduler - Render ke liye entry point
鈹溾攢鈹€ check_signals.py            # Ek-baar-chalne wala script - GitHub Actions ke liye
鈹溾攢鈹€ config.py                   # Saari settings
鈹溾攢鈹€ news_fetcher.py             # RSS news fetching
鈹溾攢鈹€ stock_mapper.py             # Company name -> NSE F&O symbol
鈹溾攢鈹€ sentiment_analyzer.py       # Bullish/Bearish scoring + category
鈹溾攢鈹€ price_fetcher.py            # Live price (Yahoo Finance)
鈹溾攢鈹€ risk_calculator.py          # ATR-based target/stoploss/risk-reward
鈹溾攢鈹€ signal_generator.py         # Poora high-probability filter logic
鈹溾攢鈹€ telegram_bot.py             # Telegram message formatting + sending
鈹溾攢鈹€ requirements.txt
鈹溾攢鈹€ Procfile                    # Render start command
鈹溾攢鈹€ runtime.txt                 # Python version
鈹溾攢鈹€ render.yaml                 # Render Blueprint (one-click deploy)
鈹溾攢鈹€ .env.example
鈹溾攢鈹€ .gitignore
鈹斺攢鈹€ data/
    鈹溾攢鈹€ stock_symbols.json      # 152 F&O stocks
    鈹溾攢鈹€ sentiment_lexicon.json  # Bullish/bearish keywords + weights
    鈹斺攢鈹€ keyword_categories.json # Keywords -> category mapping
```

---

## 馃搳 High-Probability, High Risk-Reward Filter

| Check | Kya verify hota hai |
|---|---|
| Stock identification | Company ka naam news me clearly mention ho (152 F&O stocks covered) |
| Sentiment direction | BUY ya SELL clear ho, mixed/confusing na ho |
| News confidence | Keywords ka combined weight >= 75/100 (strict, "solid" trades ke liye) |
| Live price available | Entry/stoploss/target calculate ho sake, warna signal skip |
| Risk:Reward ratio | Kam se kam 1:1.5, warna skip (sirf achhe risk-reward trades) |
| Duplicate check | Same news dobara signal na bhej de |

### News Categories jo cover hoti hain
| Category | Kya cover karta hai |
|---|---|
| 馃搳 **RESULTS** | Quarterly results - profit beat/miss, revenue growth/decline |
| 馃悑 **SMART_MONEY** | FII/DII buying-selling, bulk/block deals, promoter stake change |
| 馃彌锔� **ELECTION_MACRO** | Elections, exit polls, RBI repo rate, GST, tariffs, geopolitics |
| 馃 **CORPORATE_ACTION** | M&A, order wins, upgrades, buyback, dividend, rating changes |
| 鈿栵笍 **REGULATORY_RISK** | Fraud, SEBI probe, resignations, bans, lawsuits, penalties |

### Signal format jo Telegram pe aayega
```
馃煝 BUY SIGNAL 鈥� RELIANCE 馃煝
鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹�
馃搱 Stock: Reliance Industries (RELIANCE)
馃彿锔� Category: 馃搳 Quarterly Results Impact
馃幆 News Confidence: 95/100

馃挵 TRADE PLAN
   Entry: 鈧�2,847.50
   馃洃 Stoploss: 鈧�2,812.30
   馃幆 Target 1: 鈧�2,900.30
   馃幆 Target 2: 鈧�2,935.50
   鈿栵笍 Risk:Reward: 1:1.5

馃摪 Reason: beats estimates, record profit, upgrade
馃敆 News: Reliance posts record Q3 profit, beats street estimates
馃摗 Source: Moneycontrol
馃憠 Full news padho
鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹�
鈿狅笍 Automated news-based signal hai, financial advice nahi. Stoploss/target
ATR (volatility) se calculate hue hain, guarantee nahi. Apna risk khud
manage karo, 1-2% se zyada capital ek trade me mat lagana.
```

---

## 鈿狅笍 Important Notes (poori imandari se)
- News-based trading me **latency** ek badi problem hai 鈥� jab tak news
  public RSS pe aati hai, tab tak price kaafi move ho chuka hota hai. Isse
  faster karne ke liye paid low-latency news APIs (Bloomberg, Benzinga)
  better hote hain.
- Yeh system **backtested nahi hai**. Live use se pehle kam se kam 2-4
  hafte paper trading karke dekh lo ki signals kitne accurate aa rahe hain.
- ATR-based stoploss/target ek statistical estimate hai 鈥� market ka actual
  move news ki severity, overall market mood, aur liquidity pe depend
  karta hai, guarantee kabhi nahi hota.
- Kabhi bhi ek signal ke bharose apni poori capital mat lagana. Position
  sizing rule: kisi ek trade me apni total capital ka 1-2% se zyada risk
  mat lo.
- F&O stocks list NSE ki quarterly-updated list hoti hai 鈥� periodically
  [nseindia.com](https://www.nseindia.com) pe current list verify kar
  lena aur `data/stock_symbols.json` update kar lena.
