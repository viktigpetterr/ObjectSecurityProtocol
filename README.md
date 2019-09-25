# ObjectSecurityProtocol
Application level security proof of concept communication. Provides integrity, confidentiality, and replay protection. Based on the principles of object security and perfect forward secrecy.

### Installing 
```
python3 -m venv ./venv
```
```
source ./venv/bin/activate
```
```
pip install -r requirements.txt
```

### Start
Open two terminals

#### terminal 1
```
source ./venv/bin/activate
```
```
python3 Server.py
```
#### Terminal 2
```
source ./venv/bin/activate
```
```
python3 Client.py
```
