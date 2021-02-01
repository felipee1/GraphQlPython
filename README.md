This is my first fastAPI graphql API, is an API base with jwt login, register and product register

-=fast tutorial install=-
pip install "graphene>=2.0"
pip install fastapi
pip install uvicorn
pip install pyjwt
pip install sqlalchemy
pip install alembic

-=POSTGRES SCRIPT INSTALL BEGIN=-

sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt \$(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get -y install postgresql

sudo -u postgres psql postgres

CREATE DATABASE postgres

ALTER USER postgres WITH PASSWORD 'root';

-=Rodando Migrations=-
alembic upgrade head

-=POSTGRES SCRIPT INSTALL END=-

-=START API=-
uvicorn index:app --reload

-=Open on ip http://127.0.0.1:8000 =-

mutation Login {
Login(username: "opica", password: "123456") {
token
}
}

query products {
allProducts{
id
productName
description
code
price
}
}

mutation register {
Register(userData: {email: "opica@gmail.com", username: "opica", password: "123456", fullName: "o pica da silva sauro"}) {
ok
user {
email
username
password
fullName
}
}
}

mutation new_product($token: String!) {
  NewProduct(productData: {productName: "chinelão de dedo", code: "151sa5d15sa", price: "15.96", description: "num tem", token:$token ,}) {
ok
product {
id
productName
description
code
price
}
}
}
