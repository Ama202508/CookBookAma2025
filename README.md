# Django Cookbook (Proiect final)

## Descriere
O aplicație web dezvoltată cu Django unde utilizatorii pot crea, edita și vizualiza rețete culinare.  
Proiectul include autentificare utilizatori și operații CRUD pentru rețete.

## Dezvoltare si rulare
1. Creare mediul virtual:
 .venv\Scripts\activate

2. Instalarea dependentelor:
pip install -r requirements.txt

3. Creare baza de date:
python manage.py migrate

4. Creeaza un utilizator administrator:
python manage.py createsuperuser

5. Ruleaza serverul:
python manage.py runserver


Acceseaza aplicatia la: Starting development server at http://127.0.0.1:8000/

Pagini incluse:
/ – listă rețete (alfabetic)
/date/ – listă rețete după dată
/recipe/add/ – adaugă rețetă
/recipe/<id>/edit/ – editează rețetă
/recipe/<id>/delete/ – șterge rețetă
/recipe/<id>/ – detalii rețetă
/login/ – autentificare
/logout/ – delogare


Teste:
Proiectul include teste unitare scrise cu framework-ul de testare Django. 
Acestea verifică:
- funcționarea autentificării (login și acces la pagini),
- restricționarea accesului la crearea rețetelor pentru utilizatori neautentificați,
- crearea corectă a unei rețete și asocierea cu utilizatorul proprietar,
- sortarea rețetelor alfabetic și după data de creare,
- permisiunile: doar proprietarul poate edita o rețetă,
- validarea câmpului date_added_str (obligatoriu).

Pentru a rula testele: python manage.py test


