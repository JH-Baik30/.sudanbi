# init_db.py
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Word

DATABASE_URL = 'sqlite:///wordbook.db'
EXCEL_PATH = 'data/00_수단비 통합_0326_수정(0507)_발음기호수정_B.xlsx'

def load_excel_to_db():
    df = pd.read_excel(EXCEL_PATH)

    # 필요한 컬럼만 추출 및 이름 매핑
    df = df[[
        '영어', '발음기호', '품사', '단어 뜻', 'YK 예문', 'YK 번역'
    ]].rename(columns={
        '영어': 'english',
        '발음기호': 'pronunciation',
        '품사': 'part_of_speech',
        '단어 뜻': 'meaning',
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
            english=row['english'],
            pronunciation=row['pronunciation'],
            part_of_speech=row['part_of_speech'],
            meaning=row['meaning'],
            example_sentence=row['example_sentence'],
            example_translation=row['example_translation'],
        )
        session.add(word)

    session.commit()
    session.close()
    print("✅ 데이터베이스 초기화 및 삽입 완료!")

if __name__ == '__main__':
    load_excel_to_db()
