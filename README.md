# python-ports-adapters

## ustawienie środowiska
jeżeli nie korzystasz z vscode tylko uruchamiasz bezpośrednio z lini komend ustaw zmienną środowiskową
``` sh
. .venv\bin\activate
export PYTHONPATH=./src:$PYTHONPATH
```
``` powershell
& .venv\Scripts\Activate.ps1  
$env:PYTHONPATH="./src;$env:PYTHONPATH"
```
można też uruchomić odpowiednie skrypty przygotowane do tego celu
``` sh
activate.sh
```
``` powershell
activate.ps1
```

# run fastapi
``` sh
uvicorn main:app --reload
```
# alternatywnie mozna pobrac au add -dev "fastapi[standard]"
``` sh
fastapi dev
```