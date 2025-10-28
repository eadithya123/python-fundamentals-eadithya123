import sqlalchemy
from sqlalchemy import create_engine, String, Boolean, TIMESTAMP
from sqlalchemy.orm import sessionmaker, declarative_base, Mapped, mapped_column
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from typing import List, Union
import time

DB_USER = "my_app_user"
DB_PASSWORD = "my_secure_app_pass"
DB_HOST = "localhost" 
DB_PORT = "3306"
DB_NAME = "appdb"

DATABASE_URL = f"mariadb+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(
    DATABASE_URL,
    pool_size=10, 
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=3600,
    echo=False
)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=True, default=None)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[sqlalchemy.DateTime] = mapped_column(TIMESTAMP, default=sqlalchemy.func.current_timestamp())

    def __repr__(self):
        return f"User(id={self.id}, username='{self.username}', email='{self.email}')"

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def retrieve_all_users() -> List[User]:
    print("\n--- Listing All Users ---")
    for session in get_db_session():
        try:
            users: List[User] = session.scalars(sqlalchemy.select(User)).all()
            for user in users:
                print(user)
            return users
        except SQLAlchemyError as e:
            print(f"DB Error on retrieval: {e}")
            return []

def find_user_by_username(username: str) -> Union[User, None]:
    print(f"\n--- Searching for User: '{username}' ---")
    for session in get_db_session():
        try:
            user = session.scalars(
                sqlalchemy.select(User).where(User.username == username)
            ).one_or_none()
            
            if user:
                print(f"Found: {user.full_name}")
            else:
                print(f"User '{username}' not in records.")
            return user
        except SQLAlchemyError as e:
            print(f"DB Error on search: {e}")
            return None

def insert_new_user(username: str, email: str, full_name: str, password: str) -> Union[User, None]:
    print(f"\n--- Inserting User: '{username}' ---")
    for session in get_db_session():
        try:
            new_user = User(
                username=username,
                email=email,
                full_name=full_name,
                hashed_password=password
            )
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            print(f"Insertion successful for {new_user.full_name}.")
            return new_user
        except IntegrityError:
            session.rollback()
            print(f"Error: User '{username}' or email '{email}' already exists (Integrity constraint failed).")
            return None
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Database error during insertion: {e}")
            return None

def update_user_info(username: str, new_email: str) -> Union[User, None]:
    print(f"\n--- Updating Email for User: '{username}' to '{new_email}' ---")
    for session in get_db_session():
        try:
            
            stmt = (
                sqlalchemy.update(User)
                .where(User.username == username)
                .values(email=new_email)
            )

            result = session.execute(stmt)
            session.commit()

            if result.rowcount > 0:
                print(f"Update succeeded. Rows modified: {result.rowcount}")
                
                return find_user_by_username(username)
            else:
                print(f"User '{username}' not found. Update skipped.")
                return None
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Database error during update: {e}")
            return None

if __name__ == "__main__":
    print("Initializing. Waiting 5 seconds for the Docker DB container to fully start...")
    time.sleep(5) 
    print("Starting database operations.")

    retrieve_all_users()

    find_user_by_username('Adithya')

    find_user_by_username('Vikram')

    insert_new_user('Kiran', 'kiran.rao@corp.in', 'Kiran Rao', 'k_secret123')

    insert_new_user('Harsha', 'Harsha@email.com', 'Duplicate Harsha', 'fail_pass')

    update_user_info('Kiran', 'kiran.updated@corp.in')
    
    retrieve_all_users()