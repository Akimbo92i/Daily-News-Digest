#!/usr/bin/env python3
"""
🌍 DAILY NEWS DIGEST v2.1
Résumé quotidien des actualités mondiales avec scoring émotionnel
Version avec titres complets
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from collections import Counter
import re
import os
import textwrap
import warnings
warnings.filterwarnings("ignore")

# ═══════════════════════════════════════════════════════════════════════════════
# 🎨 CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

# Largeur d'affichage (ajustable selon votre terminal)
DISPLAY_WIDTH = 90

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'
    ORANGE = '\033[38;5;208m'
    PURPLE = '\033[38;5;141m'
    ITALIC = '\033[3m'

# ═══════════════════════════════════════════════════════════════════════════════
# 📊 DICTIONNAIRES DE SENTIMENT
# ═══════════════════════════════════════════════════════════════════════════════

MOTS_NEGATIFS = {
    # Conflits & Violence
    'guerre': -3, 'war': -3, 'mort': -3, 'dead': -3, 'killed': -3, 'tué': -3,
    'attaque': -2, 'attack': -2, 'bombe': -3, 'bomb': -3, 'terrorisme': -3,
    'terrorism': -3, 'massacre': -3, 'genocide': -3, 'génocide': -3,
    'conflit': -2, 'conflict': -2, 'combat': -2, 'violence': -2, 'violent': -2,
    'missile': -2, 'missiles': -2, 'frappe': -2, 'strike': -2, 'strikes': -2,
    'drone': -1, 'drones': -1, 'shooting': -3, 'shooter': -3, 'gunman': -3,
    
    # Catastrophes
    'catastrophe': -3, 'disaster': -3, 'tsunami': -3, 'séisme': -2, 
    'earthquake': -2, 'ouragan': -2, 'hurricane': -2, 'incendie': -2,
    'fire': -1, 'inondation': -2, 'flood': -2, 'tempête': -2, 'storm': -1,
    'explosion': -2, 'crash': -2, 'accident': -1, 'accidents': -1,
    'wildfire': -2, 'wildfires': -2, 'devastation': -3, 'devastating': -2,
    
    # Économie négative
    'crise': -2, 'crisis': -2, 'récession': -2, 'recession': -2,
    'inflation': -1, 'chômage': -2, 'unemployment': -2, 'faillite': -2,
    'bankruptcy': -2, 'effondrement': -2, 'collapse': -2, 'dette': -1, 'debt': -1,
    'layoffs': -2, 'layoff': -2, 'licenciement': -2,
    
    # Santé
    'pandémie': -2, 'pandemic': -2, 'épidémie': -2, 'epidemic': -2,
    'virus': -1, 'maladie': -1, 'disease': -1, 'décès': -2, 'deaths': -2,
    'dies': -2, 'died': -2, 'die': -2, 'death': -2,
    
    # Autres négatifs
    'scandale': -2, 'scandal': -2, 'corruption': -2, 'fraude': -2,
    'fraud': -2, 'arrestation': -1, 'arrest': -1, 'arrested': -1, 'prison': -1,
    'condamné': -1, 'sentenced': -1, 'victime': -2, 'victim': -2, 'victims': -2,
    'tragédie': -3, 'tragedy': -3, 'tragic': -2, 'menace': -2, 'threat': -2,
    'threatens': -2, 'threatening': -2,
    'peur': -1, 'fear': -1, 'fears': -1, 'danger': -2, 'dangerous': -2,
    'alerte': -1, 'alert': -1, 'warning': -1, 'warns': -1,
    'échec': -1, 'failure': -1, 'failed': -1, 'fails': -1,
    'protest': -1, 'protests': -1, 'manifestation': -1, 'riot': -2, 'riots': -2,
    'sanctions': -1, 'sanction': -1, 'emergency': -1,
    'wounded': -2, 'blessé': -2, 'injured': -1, 'injuries': -1,
    'torn': -1, 'war-torn': -2, 'bloody': -2, 'bloodshed': -3,
    'hostage': -2, 'hostages': -2, 'kidnapped': -2, 'abducted': -2,
    'refugees': -1, 'refugee': -1, 'displaced': -1, 'flee': -1, 'fled': -1,
    'destroyed': -2, 'destruction': -2, 'ruins': -2,
}

MOTS_POSITIFS = {
    # Paix & Accord
    'paix': 3, 'peace': 3, 'accord': 2, 'agreement': 2, 'traité': 2,
    'treaty': 2, 'réconciliation': 3, 'reconciliation': 3, 'deal': 1,
    'ceasefire': 3, 'cessez-le-feu': 3, 'truce': 2,
    
    # Victoires & Succès
    'victoire': 2, 'victory': 2, 'succès': 2, 'success': 2, 'successful': 2,
    'gagner': 2, 'win': 2, 'wins': 2, 'winner': 2, 'won': 2,
    'champion': 2, 'champions': 2, 'record': 1, 'exploit': 2,
    'achievement': 2, 'achieves': 2, 'historic': 1, 'historique': 1,
    'triumph': 2, 'triumphant': 2,
    
    # Économie positive
    'croissance': 2, 'growth': 2, 'grows': 1, 'emploi': 2, 'jobs': 2,
    'investissement': 1, 'investment': 1, 'profit': 1, 'profits': 1,
    'hausse': 1, 'rise': 1, 'rises': 1, 'boom': 2, 'surges': 1, 'surge': 1,
    'recovery': 2, 'reprise': 2, 'boost': 1, 'boosts': 1,
    'hiring': 1, 'hired': 1,
    
    # Innovation & Progrès
    'découverte': 2, 'discovery': 2, 'discovers': 2, 'innovation': 2,
    'breakthrough': 3, 'avancée': 2, 'progrès': 2, 'progress': 2,
    'révolution': 2, 'revolution': 2, 'revolutionary': 2,
    'guérison': 3, 'cure': 3, 'vaccin': 2, 'vaccine': 2,
    'launch': 1, 'launches': 1, 'lancement': 1, 'unveiled': 1,
    
    # Autres positifs
    'célébration': 2, 'celebration': 2, 'celebrates': 2, 'fête': 1,
    'festival': 1, 'héros': 2, 'hero': 2, 'heroes': 2, 'heroic': 2,
    'sauvetage': 2, 'rescue': 2, 'rescued': 2, 'sauvé': 2, 'saved': 2,
    'espoir': 2, 'hope': 2, 'hopes': 1, 'hopeful': 2,
    'optimisme': 2, 'optimism': 2, 'optimistic': 2,
    'libération': 2, 'liberation': 2, 'freed': 2, 'liberté': 2, 'freedom': 2,
    'amélioration': 1, 'improvement': 1, 'improves': 1, 'solution': 1,
    'resolved': 2, 'résolu': 2, 'support': 1, 'supports': 1,
    'awarded': 1, 'award': 1, 'prix': 1, 'prize': 1,
    'love': 1, 'joy': 2, 'happy': 1, 'happiness': 2,
    'united': 1, 'unity': 2, 'together': 1,
}

CATEGORIES_EMOJI = {
    'politique': '🏛️',
    'économie': '💰',
    'technologie': '💻',
    'science': '🔬',
    'santé': '🏥',
    'sport': '⚽',
    'environnement': '🌍',
    'culture': '🎭',
    'conflit': '⚔️',
    'catastrophe': '🌋',
    'société': '👥',
}

# ═══════════════════════════════════════════════════════════════════════════════
# 📡 SOURCES RSS FIABLES
# ═══════════════════════════════════════════════════════════════════════════════

RSS_SOURCES = [
    # 🇫🇷 Sources Françaises
    {"url": "https://www.lemonde.fr/rss/une.xml", "name": "Le Monde", "flag": "🇫🇷", "lang": "fr"},
    {"url": "https://www.francetvinfo.fr/titres.rss", "name": "France Info", "flag": "🇫🇷", "lang": "fr"},
    
    # 🇬🇧 Sources UK
    {"url": "https://feeds.bbci.co.uk/news/world/rss.xml", "name": "BBC World", "flag": "🇬🇧", "lang": "en"},
    {"url": "https://www.theguardian.com/world/rss", "name": "The Guardian", "flag": "🇬🇧", "lang": "en"},
    
    # 🇺🇸 Sources US
    {"url": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml", "name": "NY Times", "flag": "🇺🇸", "lang": "en"},
    {"url": "https://feeds.npr.org/1001/rss.xml", "name": "NPR News", "flag": "🇺🇸", "lang": "en"},
    
    # 🌐 Sources Internationales
    {"url": "https://www.aljazeera.com/xml/rss/all.xml", "name": "Al Jazeera", "flag": "🌐", "lang": "en"},
    {"url": "https://www.euronews.com/rss?level=theme&name=news", "name": "Euronews", "flag": "🇪🇺", "lang": "en"},
    
    # 💻 Tech
    {"url": "https://techcrunch.com/feed/", "name": "TechCrunch", "flag": "💻", "lang": "en"},
]

# ═══════════════════════════════════════════════════════════════════════════════
# 🔧 FONCTIONS UTILITAIRES
# ═══════════════════════════════════════════════════════════════════════════════

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_terminal_width():
    """Récupère la largeur du terminal"""
    try:
        return os.get_terminal_size().columns
    except:
        return DISPLAY_WIDTH

def clean_html(text):
    """Nettoie le HTML d'un texte"""
    if not text:
        return ""
    clean = re.sub(r'<[^>]+>', '', text)
    clean = re.sub(r'&[a-zA-Z]+;', ' ', clean)
    clean = re.sub(r'&#\d+;', ' ', clean)
    clean = re.sub(r'\s+', ' ', clean)
    return clean.strip()

def wrap_text(text, width, indent=0):
    """Coupe le texte proprement avec indentation"""
    wrapper = textwrap.TextWrapper(
        width=width,
        initial_indent=' ' * indent,
        subsequent_indent=' ' * indent,
        break_long_words=False,
        break_on_hyphens=True
    )
    return wrapper.fill(text)

def print_header():
    """Affiche l'en-tête stylisé"""
    width = min(get_terminal_width() - 4, DISPLAY_WIDTH)
    date_now = datetime.now().strftime("%A %d %B %Y • %H:%M")
    
    print(f"\n{Colors.CYAN}{Colors.BOLD}")
    print(f"  ╔{'═' * (width - 4)}╗")
    print(f"  ║{' ' * ((width - 50) // 2)}🌍  D A I L Y   G L O B A L   N E W S   D I G E S T  🌍{' ' * ((width - 50) // 2)}║")
    print(f"  ╚{'═' * (width - 4)}╝")
    print(f"{Colors.RESET}")
    print(f"  {Colors.DIM}📅 {date_now}{Colors.RESET}\n")

def print_separator(char="─", length=None, color=Colors.DIM):
    """Affiche un séparateur"""
    if length is None:
        length = min(get_terminal_width() - 4, DISPLAY_WIDTH)
    print(f"  {color}{char * length}{Colors.RESET}")

def get_emoji_score(score):
    """Retourne l'emoji approprié selon le score"""
    if score >= 15:
        return "🌟", "EXCELLENTE", Colors.GREEN
    elif score >= 8:
        return "😊", "BONNE", Colors.GREEN
    elif score >= 2:
        return "🙂", "PLUTÔT BONNE", Colors.CYAN
    elif score >= -2:
        return "😐", "NEUTRE", Colors.YELLOW
    elif score >= -8:
        return "😟", "MITIGÉE", Colors.ORANGE
    elif score >= -15:
        return "😢", "DIFFICILE", Colors.RED
    else:
        return "💔", "TRÈS DIFFICILE", Colors.RED

# ═══════════════════════════════════════════════════════════════════════════════
# 🌐 SCRAPING DES ACTUALITÉS
# ═══════════════════════════════════════════════════════════════════════════════

def fetch_rss_feed(source):
    """Récupère et parse un flux RSS"""
    articles = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/rss+xml, application/xml, text/xml, */*',
    }
    
    try:
        response = requests.get(source['url'], headers=headers, timeout=8, verify=True)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item') or soup.find_all('entry')
        
        for item in items[:8]:
            title = item.find('title')
            if not title:
                continue
            title_text = clean_html(title.get_text())
            
            description = item.find('description') or item.find('summary') or item.find('content')
            desc_text = clean_html(description.get_text()) if description else ""
            
            pub_date = item.find('pubDate') or item.find('published') or item.find('updated')
            date_text = pub_date.get_text() if pub_date else ""
            
            if title_text and len(title_text) > 10:
                articles.append({
                    'title': title_text,
                    'description': desc_text[:300],
                    'source': f"{source['name']} {source['flag']}",
                    'source_name': source['name'],
                    'date': date_text,
                    'lang': source.get('lang', 'en')
                })
                
    except requests.exceptions.Timeout:
        return None, "Timeout"
    except requests.exceptions.ConnectionError:
        return None, "Connexion impossible"
    except requests.exceptions.HTTPError as e:
        return None, f"HTTP {e.response.status_code}"
    except Exception as e:
        return None, str(e)[:25]
    
    return articles, None

def fetch_all_news():
    """Récupère les actualités de toutes les sources"""
    all_articles = []
    successful_sources = 0
    failed_sources = []
    
    print(f"  {Colors.CYAN}📡 Connexion aux sources d'actualités...{Colors.RESET}\n")
    
    for source in RSS_SOURCES:
        source_display = f"{source['name']} {source['flag']}"
        articles, error = fetch_rss_feed(source)
        
        if articles:
            all_articles.extend(articles)
            successful_sources += 1
            print(f"  {Colors.GREEN}✓{Colors.RESET} {source_display:22} │ {Colors.WHITE}{len(articles):2} articles{Colors.RESET}")
        else:
            failed_sources.append(source['name'])
            print(f"  {Colors.RED}✗{Colors.RESET} {source_display:22} │ {Colors.DIM}{error}{Colors.RESET}")
    
    print()
    print_separator("─")
    total = len(RSS_SOURCES)
    print(f"  {Colors.BOLD}📊 Bilan:{Colors.RESET} {Colors.GREEN}{successful_sources}/{total}{Colors.RESET} sources OK • {Colors.WHITE}{len(all_articles)}{Colors.RESET} articles récupérés")
    
    return all_articles

# ═══════════════════════════════════════════════════════════════════════════════
# 📈 ANALYSE DE SENTIMENT
# ═══════════════════════════════════════════════════════════════════════════════

def analyze_sentiment(text):
    """Analyse le sentiment d'un texte"""
    if not text:
        return 0, []
    
    text_lower = text.lower()
    score = 0
    found_words = []
    
    for word, value in MOTS_NEGATIFS.items():
        pattern = r'\b' + re.escape(word) + r'\b'
        matches = re.findall(pattern, text_lower)
        if matches:
            score += value * len(matches)
            found_words.append((word, value * len(matches), 'neg'))
    
    for word, value in MOTS_POSITIFS.items():
        pattern = r'\b' + re.escape(word) + r'\b'
        matches = re.findall(pattern, text_lower)
        if matches:
            score += value * len(matches)
            found_words.append((word, value * len(matches), 'pos'))
    
    return score, found_words

def categorize_article(text):
    """Catégorise un article"""
    if not text:
        return 'société'
    
    text_lower = text.lower()
    
    categories = {
        'conflit': ['guerre', 'war', 'conflit', 'conflict', 'militaire', 'military',
                   'armée', 'army', 'troops', 'missile', 'strike', 'frappe', 'combat',
                   'offensive', 'défense', 'defense', 'otan', 'nato', 'ukraine', 'gaza',
                   'israël', 'israel', 'hamas', 'russia', 'russie', 'weapons', 'armes',
                   'drone', 'bombing', 'airstrike', 'soldier', 'soldiers', 'sudan'],
        
        'politique': ['président', 'president', 'gouvernement', 'government', 'élection',
                     'election', 'vote', 'loi', 'law', 'parlement', 'parliament', 'sénat',
                     'senate', 'congress', 'ministre', 'minister', 'macron', 'biden', 
                     'trump', 'politique', 'political', 'parti', 'party', 'réforme',
                     'diplomat', 'diplomacy', 'embassy', 'ambassador'],
        
        'économie': ['économie', 'economy', 'economic', 'bourse', 'stock', 'marché',
                    'market', 'euro', 'dollar', 'banque', 'bank', 'inflation', 'pib',
                    'gdp', 'croissance', 'growth', 'entreprise', 'business', 'trade',
                    'commerce', 'emploi', 'job', 'chômage', 'unemployment', 'dette'],
        
        'technologie': ['tech', 'technology', 'ia', 'ai', 'artificial', 'robot', 
                       'numérique', 'digital', 'apple', 'google', 'meta', 'microsoft',
                       'amazon', 'startup', 'cyber', 'software', 'app', 'smartphone',
                       'openai', 'chatgpt', 'tesla', 'elon', 'musk', 'spacex'],
        
        'science': ['science', 'scientific', 'recherche', 'research', 'découverte',
                   'discovery', 'espace', 'space', 'nasa', 'étude', 'study',
                   'laboratory', 'experiment', 'scientist'],
        
        'santé': ['santé', 'health', 'hôpital', 'hospital', 'médecin', 'doctor',
                 'maladie', 'disease', 'vaccin', 'vaccine', 'covid', 'virus',
                 'cancer', 'patient', 'médical', 'medical', 'oms', 'who', 'drug'],
        
        'sport': ['football', 'soccer', 'sport', 'match', 'champion', 'championship',
                 'olympics', 'olympique', 'coupe', 'cup', 'fifa', 'nba', 'tennis',
                 'rugby', 'tour de france', 'league', 'ligue', 'goal', 'team'],
        
        'environnement': ['climat', 'climate', 'environnement', 'environment', 
                         'pollution', 'écologie', 'ecology', 'carbone', 'carbon',
                         'renouvelable', 'renewable', 'vert', 'green', 'nature',
                         'biodiversité', 'biodiversity', 'réchauffement', 'warming'],
        
        'catastrophe': ['séisme', 'earthquake', 'ouragan', 'hurricane', 'typhon',
                       'inondation', 'flood', 'incendie', 'fire', 'wildfire',
                       'catastrophe', 'disaster', 'tsunami', 'tornade', 'tornado',
                       'tempête', 'storm', 'explosion', 'crash', 'accident'],
        
        'culture': ['film', 'movie', 'cinema', 'musique', 'music', 'art', 'culture',
                   'festival', 'concert', 'exposition', 'exhibition', 'livre', 'book',
                   'théâtre', 'theater', 'série', 'series', 'netflix', 'cannes'],
    }
    
    scores = {cat: 0 for cat in categories}
    
    for category, keywords in categories.items():
        for kw in keywords:
            if kw in text_lower:
                scores[category] += 1
    
    best_category = max(scores, key=scores.get)
    return best_category if scores[best_category] > 0 else 'société'

# ═══════════════════════════════════════════════════════════════════════════════
# 🎨 AFFICHAGE DES RÉSULTATS
# ═══════════════════════════════════════════════════════════════════════════════

def display_top_news(articles, limit=12):
    """Affiche les actualités principales avec titres COMPLETS"""
    
    width = min(get_terminal_width() - 4, DISPLAY_WIDTH)
    
    print(f"\n\n  {Colors.BOLD}{Colors.CYAN}📰 FAITS MARQUANTS DU JOUR{Colors.RESET}")
    print_separator("═")
    
    # Analyser et trier par impact
    analyzed = []
    seen_titles = set()
    
    for article in articles:
        title_key = article['title'][:50].lower()
        if title_key in seen_titles:
            continue
        seen_titles.add(title_key)
        
        score, found_words = analyze_sentiment(article['title'] + " " + article.get('description', ''))
        category = categorize_article(article['title'] + " " + article.get('description', ''))
        analyzed.append((article, score, category, found_words))
    
    analyzed.sort(key=lambda x: abs(x[1]), reverse=True)
    
    for i, (article, score, category, words) in enumerate(analyzed[:limit], 1):
        emoji = CATEGORIES_EMOJI.get(category, '📌')
        
        # Couleur et indicateur selon le score
        if score > 2:
            score_color = Colors.GREEN
            indicator = "▲"
            score_bg = ""
        elif score < -2:
            score_color = Colors.RED
            indicator = "▼"
            score_bg = ""
        else:
            score_color = Colors.YELLOW
            indicator = "●"
            score_bg = ""
        
        # ═══ AFFICHAGE DU TITRE COMPLET ═══
        title = article['title']
        
        # Première ligne avec numéro et emoji
        prefix = f"  {emoji} {i:2}. "
        prefix_len = 8  # Longueur visuelle du préfixe
        
        # Calcul de la largeur disponible pour le titre
        title_width = width - prefix_len - 2
        
        # Découper le titre en lignes si nécessaire
        if len(title) <= title_width:
            # Titre court : une seule ligne
            print(f"\n{prefix}{Colors.BOLD}{Colors.WHITE}{title}{Colors.RESET}")
        else:
            # Titre long : multi-lignes
            lines = textwrap.wrap(title, width=title_width)
            print(f"\n{prefix}{Colors.BOLD}{Colors.WHITE}{lines[0]}{Colors.RESET}")
            for line in lines[1:]:
                print(f"         {Colors.WHITE}{line}{Colors.RESET}")
        
        # Ligne de métadonnées
        source_info = article['source']
        score_display = f"{indicator} {score:+d}"
        
        print(f"         {Colors.DIM}└─{Colors.RESET} {Colors.DIM}{source_info}{Colors.RESET}  {score_color}{score_display}{Colors.RESET}")
        
        # Afficher les mots-clés détectés (optionnel, pour les gros scores)
        if abs(score) >= 5 and words:
            key_words = [w[0] for w in sorted(words, key=lambda x: abs(x[1]), reverse=True)[:3]]
            print(f"         {Colors.DIM}   🏷️  {', '.join(key_words)}{Colors.RESET}")

def display_day_score(total_score, article_count, stats):
    """Affiche le score de la journée"""
    emoji, label, color = get_emoji_score(total_score)
    width = min(get_terminal_width() - 4, DISPLAY_WIDTH)
    
    # Calcul du pourcentage
    max_possible = article_count * 2.5
    percentage = ((total_score + max_possible) / (2 * max_possible)) * 100 if max_possible > 0 else 50
    percentage = max(0, min(100, percentage))
    
    # Barre de progression
    bar_length = 40
    filled = int(bar_length * percentage / 100)
    
    bar = ""
    for i in range(bar_length):
        if i < filled:
            if i < bar_length * 0.3:
                bar += f"{Colors.RED}█"
            elif i < bar_length * 0.5:
                bar += f"{Colors.ORANGE}█"
            elif i < bar_length * 0.7:
                bar += f"{Colors.YELLOW}█"
            else:
                bar += f"{Colors.GREEN}█"
        else:
            bar += f"{Colors.DIM}░"
    bar += Colors.RESET
    
    inner_width = width - 6
    
    print(f"\n\n")
    print(f"  {Colors.BOLD}{Colors.CYAN}╔{'═' * inner_width}╗{Colors.RESET}")
    print(f"  {Colors.BOLD}{Colors.CYAN}║{Colors.RESET}{' ' * ((inner_width - 26) // 2)}📊  SCORE DE LA JOURNÉE  📊{' ' * ((inner_width - 26) // 2)}{Colors.BOLD}{Colors.CYAN}║{Colors.RESET}")
    print(f"  {Colors.BOLD}{Colors.CYAN}╠{'═' * inner_width}╣{Colors.RESET}")
    print(f"  {Colors.BOLD}{Colors.CYAN}║{Colors.RESET}{' ' * inner_width}{Colors.BOLD}{Colors.CYAN}║{Colors.RESET}")
    
    # Ligne du verdict
    verdict = f"{emoji}   Journée  {color}{Colors.BOLD}{label}{Colors.RESET}   {emoji}"
    verdict_clean_len = len(f"{emoji}   Journée  {label}   {emoji}")
    padding = (inner_width - verdict_clean_len) // 2
    print(f"  {Colors.BOLD}{Colors.CYAN}║{Colors.RESET}{' ' * padding}{verdict}{' ' * (inner_width - padding - verdict_clean_len)}{Colors.BOLD}{Colors.CYAN}║{Colors.RESET}")
    
    print(f"  {Colors.BOLD}{Colors.CYAN}║{Colors.RESET}{' ' * inner_width}{Colors.BOLD}{Colors.CYAN}║{Colors.RESET}")
    
    # Score total
    score_line = f"Score Total: {color}{Colors.BOLD}{total_score:+4d}{Colors.RESET} points"
    score_clean_len = len(f"Score Total: {total_score:+4d} points")
    padding = (inner_width - score_clean_len) // 2
    print(f"  {Colors.BOLD}{Colors.CYAN}║{Colors.RESET}{' ' * padding}{score_line}{' ' * (inner_width - padding - score_clean_len)}{Colors.BOLD}{Colors.CYAN}║{Colors.RESET}")
    
    print(f"  {Colors.BOLD}{Colors.CYAN}║{Colors.RESET}{' ' * inner_width}{Colors.BOLD}{Colors.CYAN}║{Colors.RESET}")
    
    # Barre de progression
    bar_line = f"😢  [{bar}]  😊"
    bar_clean_len = 4 + bar_length + 6  # emojis + crochets + espaces
    padding = (inner_width - bar_clean_len) // 2
    print(f"  {Colors.BOLD}{Colors.CYAN}║{Colors.RESET}{' ' * padding}{bar_line}{' ' * (inner_width - padding - bar_clean_len)}{Colors.BOLD}{Colors.CYAN}║{Colors.RESET}")
    
    # Pourcentage
    pct_line = f"{percentage:5.1f}%"
    padding = (inner_width - len(pct_line)) // 2
    print(f"  {Colors.BOLD}{Colors.CYAN}║{Colors.RESET}{' ' * padding}{pct_line}{' ' * (inner_width - padding - len(pct_line))}{Colors.BOLD}{Colors.CYAN}║{Colors.RESET}")
    
    print(f"  {Colors.BOLD}{Colors.CYAN}║{Colors.RESET}{' ' * inner_width}{Colors.BOLD}{Colors.CYAN}║{Colors.RESET}")
    print(f"  {Colors.BOLD}{Colors.CYAN}╠{'═' * inner_width}╣{Colors.RESET}")
    
    # Stats résumées
    stats_line = f"📰 {stats['total_articles']:3} articles  │  😊 {stats['positif']:2} positifs  │  😐 {stats['neutre']:2} neutres  │  😢 {stats['negatif']:2} négatifs"
    stats_padding = (inner_width - len(stats_line)) // 2
    print(f"  {Colors.BOLD}{Colors.CYAN}║{Colors.RESET}{' ' * stats_padding}{stats_line}{' ' * (inner_width - stats_padding - len(stats_line))}{Colors.BOLD}{Colors.CYAN}║{Colors.RESET}")
    
    print(f"  {Colors.BOLD}{Colors.CYAN}╚{'═' * inner_width}╝{Colors.RESET}")

def display_statistics(articles):
    """Affiche les statistiques détaillées"""
    
    categories = Counter()
    sentiments = {'positif': 0, 'neutre': 0, 'negatif': 0}
    sources = Counter()
    total_score = 0
    all_keywords = Counter()
    scores_list = []
    
    for article in articles:
        full_text = article['title'] + " " + article.get('description', '')
        score, found_words = analyze_sentiment(full_text)
        category = categorize_article(full_text)
        
        categories[category] += 1
        sources[article['source_name']] += 1
        total_score += score
        scores_list.append(score)
        
        if score > 2:
            sentiments['positif'] += 1
        elif score < -2:
            sentiments['negatif'] += 1
        else:
            sentiments['neutre'] += 1
        
        for word, val, _ in found_words:
            all_keywords[word] += 1
    
    print(f"\n\n  {Colors.BOLD}{Colors.CYAN}📊 STATISTIQUES & ANALYSE{Colors.RESET}")
    print_separator("═")
    
    # Répartition par thème
    print(f"\n  {Colors.BOLD}📂 Répartition thématique:{Colors.RESET}\n")
    
    total = sum(categories.values())
    max_count = max(categories.values()) if categories else 1
    
    for category, count in categories.most_common(8):
        emoji = CATEGORIES_EMOJI.get(category, '📌')
        percentage = (count / total) * 100
        bar_len = int((count / max_count) * 30)
        bar = "█" * bar_len
        
        if category in ['conflit', 'catastrophe']:
            bar_color = Colors.RED
        elif category in ['science', 'technologie', 'culture']:
            bar_color = Colors.GREEN
        else:
            bar_color = Colors.CYAN
        
        print(f"     {emoji} {category.capitalize():15} {bar_color}{bar:30}{Colors.RESET} {count:3} ({percentage:4.1f}%)")
    
    # Tonalité
    print(f"\n  {Colors.BOLD}💭 Tonalité globale:{Colors.RESET}\n")
    
    total_sent = sum(sentiments.values())
    sentiment_data = [
        ('positif', sentiments['positif'], '😊', Colors.GREEN),
        ('neutre', sentiments['neutre'], '😐', Colors.YELLOW),
        ('négatif', sentiments['negatif'], '😢', Colors.RED),
    ]
    
    for label, count, emoji, color in sentiment_data:
        percentage = (count / total_sent) * 100 if total_sent > 0 else 0
        bar_len = int(percentage / 2.5)
        bar = "█" * bar_len
        print(f"     {emoji} {label.capitalize():12} {color}{bar:40}{Colors.RESET} {count:3} ({percentage:4.1f}%)")
    
    # Mots-clés
    if all_keywords:
        print(f"\n  {Colors.BOLD}🏷️  Mots-clés dominants:{Colors.RESET}\n")
        
        neg_words = [f"#{w}" for w, _ in all_keywords.most_common(20) if w in MOTS_NEGATIFS][:10]
        pos_words = [f"#{w}" for w, _ in all_keywords.most_common(20) if w in MOTS_POSITIFS][:10]
        
        if neg_words:
            print(f"     {Colors.RED}▼ Négatifs: {' '.join(neg_words)}{Colors.RESET}")
        if pos_words:
            print(f"     {Colors.GREEN}▲ Positifs: {' '.join(pos_words)}{Colors.RESET}")
    
    # Chiffres clés
    print(f"\n  {Colors.BOLD}📈 Chiffres clés:{Colors.RESET}\n")
    
    avg_score = total_score / len(articles) if articles else 0
    
    print(f"     📰 Articles analysés     : {Colors.WHITE}{Colors.BOLD}{len(articles)}{Colors.RESET}")
    print(f"     🎯 Score total           : {Colors.CYAN}{Colors.BOLD}{total_score:+d}{Colors.RESET} points")
    print(f"     📊 Score moyen/article   : {Colors.CYAN}{avg_score:+.2f}{Colors.RESET}")
    print(f"     📡 Sources actives       : {Colors.WHITE}{len(sources)}{Colors.RESET}")
    
    if scores_list:
        print(f"     ⬆️  Article le + positif : {Colors.GREEN}{max(scores_list):+d}{Colors.RESET}")
        print(f"     ⬇️  Article le + négatif : {Colors.RED}{min(scores_list):+d}{Colors.RESET}")
    
    return {
        'total_score': total_score,
        'total_articles': len(articles),
        'positif': sentiments['positif'],
        'neutre': sentiments['neutre'],
        'negatif': sentiments['negatif'],
        'categories': categories
    }

def display_mood_advice(score, stats):
    """Affiche un conseil personnalisé"""
    
    print(f"\n\n  {Colors.BOLD}{Colors.CYAN}💡 PERSPECTIVE DU JOUR{Colors.RESET}")
    print_separator("═")
    
    if score >= 10:
        emoji = "🌟"
        title = "Excellente journée !"
        message = [
            "Les nouvelles positives dominent largement aujourd'hui.",
            "Profitez de cette énergie pour entreprendre !",
        ]
    elif score >= 3:
        emoji = "☀️"
        title = "Bonne journée globalement"
        message = [
            "Plus de bonnes nouvelles que de mauvaises.",
            "Un climat propice à l'optimisme raisonné.",
        ]
    elif score >= -3:
        emoji = "⛅"
        title = "Journée équilibrée"
        message = [
            "Mix de positif et négatif dans l'actualité.",
            "Gardez du recul sur les gros titres sensationnels.",
        ]
    elif score >= -10:
        emoji = "🌧️"
        title = "Journée chargée"
        message = [
            "Plusieurs actualités difficiles aujourd'hui.",
            "Rappel : les bonnes nouvelles font moins de clics.",
            "Beaucoup de gens œuvrent pour des solutions.",
        ]
    else:
        emoji = "🌪️"
        title = "Journée lourde"
        message = [
            "Beaucoup d'actualités préoccupantes.",
            "Prenez soin de vous : pause écran si besoin.",
            "L'humanité a toujours su traverser les tempêtes. 💙",
        ]
    
    print(f"\n  {emoji} {Colors.BOLD}{title}{Colors.RESET}\n")
    for line in message:
        print(f"     {Colors.WHITE}• {line}{Colors.RESET}")
    
    # Top catégorie
    if stats['categories']:
        top_cat = stats['categories'].most_common(1)[0]
        cat_emoji = CATEGORIES_EMOJI.get(top_cat[0], '📌')
        print(f"\n  {Colors.DIM}📌 Thème dominant : {cat_emoji} {top_cat[0].capitalize()} ({top_cat[1]} articles){Colors.RESET}")

def display_footer():
    """Affiche le pied de page"""
    print(f"\n")
    print_separator("═", color=Colors.CYAN)
    print(f"  {Colors.DIM}📡 Sources : Le Monde, BBC, NYT, Guardian, Al Jazeera, France Info...")
    print(f"  🤖 Analyse de sentiment par détection de mots-clés")
    print(f"  📅 Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}{Colors.RESET}")
    print_separator("═", color=Colors.CYAN)
    print()

# ═══════════════════════════════════════════════════════════════════════════════
# 🚀 PROGRAMME PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Fonction principale"""
    clear_screen()
    print_header()
    
    articles = fetch_all_news()
    
    if not articles:
        print(f"\n  {Colors.RED}❌ Impossible de récupérer les actualités.{Colors.RESET}")
        print(f"  {Colors.DIM}Vérifiez votre connexion internet.{Colors.RESET}\n")
        return
    
    print_separator("═", color=Colors.CYAN)
    
    # Actualités principales
    display_top_news(articles)
    
    # Statistiques
    stats = display_statistics(articles)
    
    # Score de la journée
    display_day_score(stats['total_score'], stats['total_articles'], stats)
    
    # Conseil
    display_mood_advice(stats['total_score'], stats)
    
    # Footer
    display_footer()

if __name__ == "__main__":
    try:
        import requests
        from bs4 import BeautifulSoup
    except ImportError:
        print("📦 Installation des dépendances...")
        import subprocess
        import sys
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
                              'requests', 'beautifulsoup4', 'lxml', '-q'])
        import requests
        from bs4 import BeautifulSoup
    
    main()