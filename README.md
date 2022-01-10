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

```bash
sudo apt-add-repository multiverse
sudo apt-get install vagrant virtualbox
sudo usermod -a -G kvm ubuntu
```

# PARSEC
Download the PARSEC benchmarks:
```bash
wget http://parsec.cs.princeton.edu/download/2.1/parsec-2.1.tar.gz && \
wget http://parsec.cs.princeton.edu/download/2.1/binaries/parsec-2.1-amd64-linux.tar.gz && \
tar -xzf parsec-2.1-amd64-linux.tar.gz && \
tar -xzf parsec-2.1.tar.gz -C parsec-2.1 --strip-components=1
mv parsec-2.1/pkgs/apps/facesim/inst/amd64-linux.gcc.pre parsec-2.1/pkgs/apps/facesim/inst/amd64-linux.gcc && \
mv parsec-2.1/pkgs/apps/swaptions/inst/amd64-linux.gcc.pre parsec-2.1/pkgs/apps/swaptions/inst/amd64-linux.gcc && \
mv parsec-2.1/pkgs/apps/bodytrack/inst/amd64-linux.gcc.pre parsec-2.1/pkgs/apps/bodytrack/inst/amd64-linux.gcc 
```
Then `cd` into the parsec-2.1 directory and run each of them:
```bash
./bin/parsecmgmt -a run -p swaptions -i native -s "time -p"
```
```bash
./bin/parsecmgmt -a run -p facesim -i native -s "time -p"
```
```bash
./bin/parsecmgmt -a run -p bodytrack -i native -s "time -p"
```
