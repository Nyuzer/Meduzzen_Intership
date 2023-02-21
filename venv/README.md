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

___

# Docker

To create an image you have to enter this command
```
docker build -t myimage .
```

Run a container based on your image
```
docker run -d --name mycontainer -p 80:80 myimage
```
Tests are run when you start the container. However, to do the tests when the container is running, enter this command.
```
docker exec mycontainer pytest
```
