"""Quick script to check targets in database"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings
from init_database import BotTarget

engine = create_engine(settings.DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

targets = session.query(BotTarget).filter_by(enabled=True).all()
print(f'Total targets enabled: {len(targets)}')
for i, t in enumerate(targets, 1):
    print(f'  {i}. {t.url} - {t.target_pageviews} views')

session.close()
