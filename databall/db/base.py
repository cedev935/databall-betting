import re

from sqlalchemy.orm import as_declarative, declared_attr

from databall.db.session import Session


@as_declarative()
class Base:
    @declared_attr
    def __tablename__(cls):
        return re.sub(r'([a-z\d])([A-Z])', r'\1_\2', cls.__name__).lower()

    @classmethod
    def save_df(cls, df):
        columns = {column.upper() for column in cls.__table__.columns.keys()}
        columns_to_drop = set(df.columns) - columns
        df_save = df.drop(columns_to_drop, axis=1)

        with Session() as session:
            engine = session.get_bind()
            df_save.to_sql(cls.__tablename__, engine, if_exists='append', index=False)
