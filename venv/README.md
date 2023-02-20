# Meduzzen Intership

---

First you must clone this repository
```
git clone https://github.com/Nyuzer/Meduzzen_Intership.git
```
Next, you should go into the venv directory and install all requirements
```
cd venv && pip install -r requirements.txt
```
After that you need to go to the project directory and start the server
```
cd .. && cd project && uvicorn main:app --reload
```


---
# Tests
To run tests you can enter this command in the tests directory
```
python -m pytest
```