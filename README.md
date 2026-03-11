# Books Scraper & API Challenge

Ez a tároló a "Books Scraper & API Challenge" tesztfeladat teljes megoldását tartalmazza. A projekt egy teljes adatfeldolgozási folyamatot (data pipeline) mutat be: könyvek adatainak webes gyűjtését (scraping) , adatbázisban történő tárolását , egy RESTful API-n keresztüli publikálását , valamint a teljes infrastruktúra automatizált, felhőbe történő telepítését (CI/CD).

## 1. Élő API Elérés (Live API)

Az alkalmazás jelenleg az AWS (Amazon Web Services) felhőben fut. [Az élő API-t és annak interaktív Swagger/OpenAPI dokumentációját az alábbi linken próbálhatod ki:

**http://3.68.246.89:8000/docs**

*(Megjegyzés: A szerver indulásakor az adatgyűjtő a háttérben folyamatosan tölti fel az adatbázist az 1000 könyv adataival, így az elemek száma percről percre nőheti el a végleges mennyiséget.)*

## 2. Architektúra és Technikai Döntések

A funkcionális és nem funkcionális követelmények maximális teljesítése érdekében a következő technológiai stacket választottam:

* **Programozási nyelv:** `Python 3` - Ipari standard mind a webes adatgyűjtés, mind a modern API-k építése terén.
* **Web Scraper:** `requests` & `BeautifulSoup4` - Gyors és hatékony eszközök a statikus HTML oldalak feldolgozására. Célzottan gyűjti be a könyvek címét, árát, készletinformációit, értékelését és kategóriáját , kezelve a lapozást is.
* **API Keretrendszer:** `FastAPI` - Kivételes teljesítménye és a beépített, automatikus Swagger (OpenAPI) dokumentáció generálása miatt esett rá a választás. Az adatvalidációt a `Pydantic` végzi.
* **Adatbázis:** `SQLite` kiegészítve `SQLAlchemy` ORM-mel. Az ORM használata biztosítja, hogy a kód hordozható legyen, és a jövőben akár egy relációs PostgreSQL adatbázisra is át lehessen állni minimális kódmódosítással.
* **Felhőszolgáltató:** `AWS (Amazon Web Services)` - Egy EC2 példány (virtuális szerver) felel az API és a scraper futtatásáért.
* **Infrastruktúra mint Kód (IaC):** `Terraform` - A teljes felhős infrastruktúra (EC2 szerver, Security Group tűzfalszabályok) kódból van definiálva a reprodukálhatóság érdekében.
* **CI/CD és Automatizáció:** `GitHub Actions` - Egy automatizált pipeline, amely minden új `main` ágra történő *commit* esetén lefut, felépíti az AWS környezetet a Terraform segítségével, és elindítja az alkalmazást.

## 3. Megvalósított API Végpontok

* `GET /books/`: Visszaadja az összes lekapart könyvet, támogatva a lapozást (`skip` és `limit` query paraméterekkel).
* `GET /books/statistics/most-expensive`: Statisztikai végpont, amely visszaadja az adatbázisban szereplő legdrágább könyvet.
* `GET /books/statistics/least-expensive`: Statisztikai végpont, amely visszaadja az adatbázisban szereplő legolcsóbb könyvet.

## 4. Kihívások és Megoldások

A fejlesztés és a felhős telepítés (DevOps) során az alábbi kihívásokkal szembesültem és oldottam meg:

1. **Karakterkódolási anomáliák (Scraping):** A céloldal bizonyos árak esetében hibás karaktereket (pl. egy rejtett `Â` karaktert a `£` jel előtt) adott vissza, ami megakasztotta a `float` konverziót. Ezt a `requests` kódolásának explicit UTF-8-ra állításával és string tisztítással oldottam meg.
2. **AWS Free Tier korlátozások (IaC):** A Terraform konfiguráció kezdetben `t2.micro` példányt kért, de az újonnan regisztrált fiókoknál a frankfurti régióban az AWS már a `t3.micro` típust biztosítja a Free Tier keretében. A Terraform konfiguráció dinamikus módosítása orvosolta a hibaüzenetet.
3. **CI/CD Tűzfal Ütközések:** A GitHub Actions többszöri futtatásakor az AWS jelezte, hogy a megadott Security Group (tűzfal) már létezik. A megoldás a Terraform kód módosítása (erőforrás átnevezése) volt a tiszta állapot (state) biztosítása érdekében.
4. **Blokkoló Scraper Folyamat:** Kezdetben a szerver telepítő szkriptje (user_data) megvárta az 1000 könyv lekaparását, mielőtt elindította volna a FastAPI szervert, ami `Connection Refused` hibát eredményezett a telepítés után. Ezt a folyamatok aszinkron, háttérben történő futtatásával (`nohup ... &`) küszöböltem ki, így az API azonnal elérhetővé válik, míg az adatok a háttérben töltődnek fel.

## 5. Útmutató a Helyi Futtatáshoz (Local Setup) 

Ha saját gépeden szeretnéd tesztelni a projektet, kövesd az alábbi lépéseket:

**Előfeltételek:**
- Python 3.9+
- Git

**1. A tároló klónozása:**
```bash
git clone [https://github.com/spawn187/books-scraper-api.git](https://github.com/spawn187/books-scraper-api.git)
cd books-scraper-api