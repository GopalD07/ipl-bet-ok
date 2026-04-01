# IPL-Bet — Hosting Guide
# Stack: Supabase → Render → Vercel (all free)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 1 — SUPABASE (Database)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Go to https://supabase.com → sign up with GitHub
2. Click "New project" → name it: IPL-Bet
3. Set a password, pick region → Create project (wait 2 min)
4. Click "SQL Editor" in sidebar → "New query" → paste and run:

-------- PASTE THIS SQL --------
CREATE TABLE match_configs (
  match_no    INTEGER PRIMARY KEY,
  home_wallet NUMERIC(10,4) DEFAULT 0,
  away_wallet NUMERIC(10,4) DEFAULT 0,
  result      TEXT DEFAULT 'pending',
  updated_at  TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE bets (
  id         BIGSERIAL PRIMARY KEY,
  match_no   INTEGER NOT NULL REFERENCES match_configs(match_no) ON DELETE CASCADE,
  side       TEXT NOT NULL CHECK (side IN ('home','away')),
  placed     NUMERIC(10,4) NOT NULL,
  win        NUMERIC(10,4) NOT NULL DEFAULT 0,
  odd        NUMERIC(10,4) DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_bets_match ON bets(match_no);
CREATE INDEX idx_bets_side  ON bets(match_no, side);
---------------------------------

5. Go to Settings → API → copy and save these 2 values:
   - Project URL  →  https://xxxxxxxx.supabase.co
   - anon/public key  →  eyJhbGci...long string


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 2 — GITHUB (Code Storage)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Go to https://github.com → sign in
2. Click "+" → "New repository"
   - Name: IPL-Bet
   - Public
   - DO NOT tick "Add README"
   - Click "Create repository"

3. Open terminal in your project folder and run:

-------- PASTE THESE COMMANDS ONE BY ONE --------
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/IPL-Bet.git
git push -u origin main
--------------------------------------------------

   Replace YOUR_USERNAME with your GitHub username.
   When prompted: enter GitHub username + password
   (if password fails, use a GitHub Personal Access Token)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 3 — RENDER (Backend API)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Go to https://render.com → sign up with GitHub
2. Click "New +" → "Web Service"
3. Click "Connect" next to IPL-Bet repo
4. Fill in:
   - Name:            ipl-bet-api
   - Region:          Singapore
   - Branch:          main
   - Runtime:         Python 3
   - Build Command:   pip install -r requirements.txt
   - Start Command:   gunicorn app:app --bind 0.0.0.0:$PORT --workers 2
   - Instance Type:   Free

5. Scroll to "Environment Variables" → Add these 3:

   Key: SUPABASE_URL     Value: https://xxxxxxxx.supabase.co
   Key: SUPABASE_KEY     Value: eyJhbGci...your anon key
   Key: FLASK_ENV        Value: production

6. Click "Create Web Service" → wait 3-5 min for build

7. Test it — open in browser:
   https://ipl-bet-api.onrender.com/schedule
   → Should show JSON list of IPL matches ✅

   NOTE: First request after 15min sleep takes ~30 sec. Normal.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 4 — VERCEL (Frontend)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Go to https://vercel.com → sign up with GitHub (same account)
2. Click "Add New..." → "Project"
3. Find IPL-Bet in the list → click "Import"
4. Settings:
   - Framework Preset: Other
   - Root Directory:   . (leave empty/dot)
   - Build Command:    (leave empty)
   - Output Directory: . (leave empty/dot)
5. Click "Deploy"
6. Wait 60 seconds → click "Visit"

Your live URL: https://ipl-bet.vercel.app  ✅


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
UPDATING CODE LATER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Whenever you make any changes, just run:

git add .
git commit -m "describe your change"
git push

Both Render and Vercel auto-redeploy within 2 minutes. Done.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RUNNING LOCALLY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

pip install flask flask-cors supabase gunicorn
export SUPABASE_URL="https://xxxxxxxx.supabase.co"
export SUPABASE_KEY="eyJhbGci..."
python app.py

Then open index.html in browser (or use Live Server in VS Code)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FILES IN THIS REPO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

index.html        → Frontend (deployed on Vercel)
app.py            → Backend Flask API (deployed on Render)
requirements.txt  → Python packages
Procfile          → Tells Render how to start the server
DEPLOY.md         → This file


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TROUBLESHOOTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Website shows "Cannot connect to backend"
→ Render is sleeping. Refresh after 30 seconds.

git push fails with "authentication failed"
→ Go to GitHub → Settings → Developer Settings
  → Personal Access Tokens → Tokens (classic) → Generate new
  → Give it "repo" scope → use that token as your password

Vercel shows 404 or blank page
→ Settings → Git → Disconnect → reconnect GitHub
→ Make sure "All repositories" is selected

Render build fails
→ Check build logs on Render dashboard
→ Most likely: requirements.txt missing a package

Supabase "permission denied" error
→ Supabase → Table Editor → each table → Authentication → disable RLS
