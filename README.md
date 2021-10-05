# browserbench

```bash
sudo apt-get update
sudo apt-get install -y python-is-python3 python3-selenium python3-numpy firefox git
git clone https://github.com/fintelia/browserbench.git && cd browserbench
wget https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz
tar -xzf geckodriver-v0.30.0-linux64.tar.gz
sudo mv geckodriver /usr/local/bin/
```

```bash
sudo apt-get install -y libtbb-dev m4
wget http://parsec.cs.princeton.edu/download/3.0/parsec-3.0-core.tar.gz && tar -xzf parsec-3.0-core.tar.gz && cd parsec-3.0
source env.sh
parsecmgmt -a build -p parsec.swaptions
parsecmgmt -a run -p parsec.swaptions -i native -s "time -p"
```

parsec.blackscholes
parsec.canneal
parsec.cmake
