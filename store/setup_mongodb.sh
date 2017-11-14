sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
echo "deb http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list
sudo apt-get update
sudo apt-get install -y mongodb-org

#fix for MongoDB dbpath (\data\db\) does not exist after service mongod start
sudo killall -15 mongod
sudo mkdir -p /data/db/

#/!\ replace nom_utilisateur /!\
sudo chown -R nom_utilisateur:nom_utilisateur /data/db
sudo mongod

#src : https://doc.ubuntu-fr.org/mongodb 
#tested on ubuntu 17.10
