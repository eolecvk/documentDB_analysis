sudo apt-get update
sudo apt-get install software-properties-common -y

#ubuntu < 17.10
#sudo add-apt-repository ppa:couchdb/stable -y

#ubuntu >=17.10
sudo add-apt-repository ppa:jderose/couchdb-1.7.0

sudo apt-get update
sudo apt-get remove couchdb couchdb-bin couchdb-common -yf
sudo apt-get install couchdb -y
curl localhost:5984
