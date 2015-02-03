#!/bin/bash

export JENKINS_HOME=$(mktemp -d)
JENKINS_WAR=/usr/share/jenkins/jenkins.war

cd ${JENKINS_HOME}
java -jar ${JENKINS_WAR} --httpPort=8181 &

## Can have smarter logic. This could work but didnt tested.
#while ! grep 'INFO: Jenkins is fully up and running' jenkins.out
#do
#  echo "Waiting for Jenkins to start..."
#  sleep 5
#done

sleep 45

echo "Jenkins is running, now get plugins.."

# Update updateCenter so we have a valid list of plugins
wget -q -O- http://updates.jenkins-ci.org/update-center.json | sed '1d;$d' > default.json
curl -s -X POST -H "Accept: application/json" -d @default.json http://127.0.0.1:8181/updateCenter/byId/default/postBack


while [ ! -f ${JENKINS_HOME}/jenkins-cli.jar ]
do
  wget -q -O ${JENKINS_HOME}/jenkins-cli.jar http://127.0.0.1:8181/jnlpJars/jenkins-cli.jar
done

# Since JENKINS_HOME in this docker image is a volume,
# we want to make sure that the plugins are available when
# volume is mounted
mkdir -p /var/lib/jenkins/downloaded_plugins

for p in $(cat /var/lib/jenkins/plugins_script/plugins.txt)
do
    echo "Adding Jenkins Plugin ${p}..."
    java -jar  ${JENKINS_HOME}/jenkins-cli.jar -s http://127.0.0.1:8181/ install-plugin ${p}
done

cp -r ${JENKINS_HOME}/plugins/* /var/lib/jenkins/downloaded_plugins/

java -jar ${JENKINS_HOME}/jenkins-cli.jar -s http://127.0.0.1:8181/ safe-shutdown

rm -rf ${JENKINS_HOME}
