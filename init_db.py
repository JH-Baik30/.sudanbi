# init_db.py
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, synonym
from app.models import Base, Word

DATABASE_URL = 'sqlite:///wordbook.db'
EXCEL_PATH = 'data/00_수단비 통합_위의파일컬럼_색출중.xlsx'

def load_excel_to_db():
    df = pd.read_excel(EXCEL_PATH)

    # 필요한 컬럼만 추출 및 이름 매핑
    df = df[[
        '카테고리', '카테고리_보조',
        '영어', '발음기호', '품사', '단어 편집_최종',
        '유의어_최종', '반의어_최종', 'YK 예문', 'YK 번역'
    ]].rename(columns={
        '카테고리': 'category',
        '카테고리_보조': 'subcategory',
        '영어': 'english',
        '발음기호': 'pronunciation',
        '품사': 'part_of_speech',
        '단어 편집_최종': 'meaning',
        '유의어_최종': 'synonym',
        '반의어_최종': 'antonym',
        'YK 예문': 'example_sentence',
        'YK 번역': 'example_translation',
    })

    engine = create_engine(DATABASE_URL)
    Base.metadata.drop_all(engine)  # 🔁 테이블 재생성 전 제거
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    for _, row in df.iterrows():
        word = Word(
            category = row['category'],
            subcategory = row['subcategory'],
            english=row['english'],
            pronunciation=row['pronunciation'],
            part_of_speech=row['part_of_speech'],
            meaning=row['meaning'],
            synonym=row['synonym'],
            antonym=row['antonym'],
            example_sentence=row['example_sentence'],
            example_translation=row['example_translation'],
        )
        session.add(word)

    session.commit()
    session.close()
    print("✅ 데이터베이스 초기화 및 삽입 완료!")

if __name__ == '__main__':
    load_excel_to_db()
