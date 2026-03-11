import requests
from bs4 import BeautifulSoup
from database import SessionLocal, engine, Base
from models import Book

# Létrehozzuk az adatbázis táblákat, ha még nem léteznek
Base.metadata.create_all(bind=engine)

BASE_URL = "http://books.toscrape.com/catalogue/"

def get_rating_from_class(class_list):
    """A HTML class-ok alapján (pl. ['star-rating', 'Three']) visszaad egy számot."""
    ratings = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    for item in class_list:
        if item in ratings:
            return ratings[item]
    return 0

def run_scraper():
    # Megnyitunk egy adatbázis session-t
    db = SessionLocal()
    page_num = 1
    
    try:
        while True:
            print(f"Adatok gyűjtése a(z) {page_num}. oldalról...")
            url = f"{BASE_URL}page-{page_num}.html"
            
            response = requests.get(url)
            response.encoding = 'utf-8' 
            
            # Ha az oldal nem található (404), akkor elértünk a lista végére
            if response.status_code == 404:
                print("Elértük az utolsó oldalt. Scraping befejezve.")
                break
                
            soup = BeautifulSoup(response.text, "html.parser")
            # Kikeressük az összes könyvet az adott oldalon
            books_on_page = soup.find_all("article", class_="product_pod")
            
            for book_html in books_on_page:
                # 1. Alapadatok a listázó oldalról
                title = book_html.find("h3").find("a")["title"]
                price_text = book_html.find("p", class_="price_color").text
                
                clean_price = price_text.replace("£", "").replace("Â", "").strip()
                price = float(clean_price) 
                
                rating_classes = book_html.find("p", class_="star-rating")["class"]
                rating = get_rating_from_class(rating_classes)
                
                # 2. Részletes adatok (kategória, készlet) miatt be kell lépni a könyv saját oldalára
                book_link = book_html.find("h3").find("a")["href"]
                detail_url = BASE_URL + book_link
                
                detail_response = requests.get(detail_url)
                detail_response.encoding = 'utf-8' # <-- JAVÍTÁS 3: Itt is beállítjuk a kódolást
                detail_soup = BeautifulSoup(detail_response.text, "html.parser")
                
                # Készlet ellenőrzése
                availability_text = detail_soup.find("p", class_="instock availability").text.strip()
                in_stock = "In stock" in availability_text
                
                # Kategória kinyerése a morzsamenüből (breadcrumb)
                category = detail_soup.find("ul", class_="breadcrumb").find_all("li")[2].text.strip()
                
                # 3. Adatbázis rekord létrehozása
                db_book = Book(
                    title=title,
                    price=price,
                    in_stock=in_stock,
                    rating=rating,
                    category=category
                )
                db.add(db_book)
                
            # Oldalanként mentjük (commit) az adatokat az adatbázisba
            db.commit()
            page_num += 1
            
    finally:
        # Biztosítjuk, hogy a kapcsolat lezáruljon
        db.close()

if __name__ == "__main__":
    run_scraper()