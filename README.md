-=fast tutorial install=-
pip install "graphene>=2.0"
pip install fastapi
pip install uvicorn
pip install pyjwt
pip install sqlalchemy

-=POSTGRES SCRIPT INSTALL BEGIN=-

sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt \$(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get -y install postgresql

-=POSTGRES SCRIPT INSTALL END=-

-=START API=-
uvicorn index:app --reload

-=Open on ip http://127.0.0.1:8000 =-

mutation Login {
Login(username:"teste",password:"teste") {
token
}
}

query person($token: String!) {
  person(token: $token) {
name
age
}
}
