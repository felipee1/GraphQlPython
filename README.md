-=fast tutorial install=-
pip install "graphene>=2.0"
pip install fastapi
pip install uvicorn

-=START API=-
uvicorn index:app --reload

-=Open on ip http://127.0.0.1:8000 =-

mutation soma {
soma(somaData: {number1:17, number2: 22}) {
soma {
result,
}
}
},

mutation mult {
multiplicar(multData: {number1:17, number2: 22}) {
mult {
result,
}
}
}
