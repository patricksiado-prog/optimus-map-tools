import os, sys
from datetime import datetime

VERSION = "5.18"

try:
    import gspread
    from google.oauth2.service_account import Credentials
except ImportError:
    print("Install: pip install gspread google-auth")
    input("Press Enter to close...")
    sys.exit(1)

CREDS_FILE = "google_creds.json"
SHEET_ID = "12PIIplhqUuZWAfEUdJMP3J04nAyrsFsFB07bDDDV2Ag"
SOURCE_TAB = "Hunter Leads"
OUTPUT_TAB = "v5_18_PROPOSED_CHANGES"

RES_SUFFIXES = {
    'lane','ln','court','ct','cove','cv','way','place','pl','circle','cir','trail','trl',
    'crossing','xing','run','hollow','glen','meadow','terrace','ter','path','pass',
    'walk','loop','bend','point','pt','ridge','crest','springs'
}
COMM_SUFFIXES = {'boulevard','blvd','highway','hwy','freeway','fwy','parkway','pkwy','expressway','expy','turnpike','plaza','square','sq'}
COMM_KEYWORDS = {'llc','inc','corp','company','restaurant','hospital','clinic','pharmacy','school','church','store','shop','office','plaza','mall','center','centre','hotel','motel','bank','salon','studio','cafe','bar','market','bakery','dental','medical','law','realty','automotive','garage'}
KNOWN_COMMERCIAL_ZIPS = {'77002','77010','77046','77056','78701','73102'}

def normalize_zip(z):
    return str(z or "").strip().split(".")[0].zfill(5)

def smart_classify_v518(address, biz='', zip_code=''):
    if not address:
        return 'RESIDENTIAL', 'HIGH'
    a = address.lower().strip()
    if '(no #)' in a or '(no number)' in a:
        return 'DROP', 'HIGH'

    score = 0
    for tok in a.split()[-2:]:
        clean = tok.strip('.,#0123456789')
        if clean in RES_SUFFIXES:
            score -= 3
            break
        if clean in COMM_SUFFIXES:
            score += 3
            break

    if biz and biz.lower() not in ('','none','no biz','google maps (no biz)'):
        b = biz.lower()
        score += 4 if any(kw in b for kw in COMM_KEYWORDS) else 1

    if normalize_zip(zip_code) in KNOWN_COMMERCIAL_ZIPS:
        score += 1

    cls = 'COMMERCIAL' if score > 0 else 'RESIDENTIAL'
    conf = 'HIGH' if abs(score) >= 3 else ('MED' if abs(score) >= 1 else 'LOW')
    return cls, conf

def connect():
    if not os.path.exists(CREDS_FILE):
        print(f"ERROR: missing {CREDS_FILE} in current directory")
        input("Press Enter to close...")
        return None
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file(CREDS_FILE, scopes=scopes)
    return gspread.authorize(creds).open_by_key(SHEET_ID)

def main():
    print("HUNTER v5.18 RECLASSIFIER - SAFE / NON-DESTRUCTIVE")
    print("=" * 60)
    ss = connect()
    if not ss:
        return

    src = ss.worksheet(SOURCE_TAB)
    rows = src.get_all_records()
    print(f"Read {len(rows):,} rows from {SOURCE_TAB}")

    proposals = []
    stats = {'keep':0, 'to_RES':0, 'to_COMM':0, 'drop':0}

    for row in rows:
        addr = str(row.get('Address') or '').strip()
        biz  = str(row.get('Business Name') or '')
        old  = str(row.get('Property Type') or '').upper()
        zip_ = normalize_zip(row.get('Zip') or '')

        if old not in ('COMMERCIAL','RESIDENTIAL'):
            continue

        new, conf = smart_classify_v518(addr, biz, zip_)

        if new == 'DROP':
            stats['drop'] += 1
            proposals.append([addr, biz, row.get('City',''), zip_, old, 'DROP', conf, 'DELETE'])
        elif new == old:
            stats['keep'] += 1
        elif old == 'COMMERCIAL' and new == 'RESIDENTIAL':
            stats['to_RES'] += 1
            proposals.append([addr, biz, row.get('City',''), zip_, old, new, conf, 'MOVE_TO_RES'])
        elif old == 'RESIDENTIAL' and new == 'COMMERCIAL':
            stats['to_COMM'] += 1
            proposals.append([addr, biz, row.get('City',''), zip_, old, new, conf, 'MOVE_TO_COMM'])

    print(f"\nClassification summary:")
    print(f"  Unchanged:           {stats['keep']:>6,}")
    print(f"  COMM -> RES:         {stats['to_RES']:>6,}")
    print(f"  RES -> COMM:         {stats['to_COMM']:>6,}")
    print(f"  DROP no number:      {stats['drop']:>6,}")
    print(f"  TOTAL CHANGES:       {len(proposals):>6,}")

    tab_name = f"{OUTPUT_TAB}_{datetime.now().strftime('%Y%m%d_%H%M')}"
    try:
        out_ws = ss.add_worksheet(tab_name, rows=len(proposals)+10, cols=10)
    except Exception as e:
        print(f"Could not create new tab {tab_name}: {e}")
        input("Press Enter to close...")
        return

    header = ['Address','Business Name','City','Zip','Old Class','New Class','Confidence','Action']
    out_ws.update([header] + proposals)
    print(f"\nWrote {len(proposals):,} proposed changes to NEW tab: {tab_name}")
    print("Nothing existing has been modified.")
    input("Press Enter to close...")

if __name__ == "__main__":
    main()
