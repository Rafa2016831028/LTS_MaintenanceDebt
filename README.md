# Apache Long Term Support (LTS) Maintenance Debt

The core intent of the project is to identify the maintenance trend of LTS support, to pinpoint when and why Technical debt manifests in the targeted release. 
The dataset available at \data_code_stable folder.

The pipeline of analysis is described in the following picture:


![git_flow](https://github.com/joydeba/InconsistentLinking/blob/main/Image/methodology.png)

# Clone it by - 
    - git clone https://github.com/Rafa2016831028/LTS_MaintenanceDebt.git
     - If password is not working, use PAT

# Execution Insturuction & Reproducability:
 This study examines the technical debt involved in fixing 105,396 commits derived from 31,076 backports. These backports were collected from 87 repositories across three major ecosystems: Apache, Eclipse, and Python.
     - The \Ecosystem folder contains the backports and commit information required to trace and reproduce the experiment.
     - The \data_code_stable folder contains the previous and current states of committed backport changes, from which software metrics (CC, MP, Workload) were calculated.
     - The \stats folder provides the statistical demographics of the tagged backports considered for project analysis.


# Virtual environment (Set up instruction)
    - python3 -m venv . venvINCON
    - source bin/activate [for locations]

# Required packages
    - pip/pip3 install PyGithub
    - pip install numpy
    - pip install matplotlib
    - pip3 install pytz
    - pip3 install GitPython 
    - brew install gh
    - sudo apt-get install python3-tk

# Reproducability (run the code on SonarQube)
1. Install SonarScanner - Make sure you have the SonarScanner installed.
2. Create sonar-project.properties and set up your SonarQube key with

At the root of your repo, create a file named sonar-project.properties:
```
sonar.projectKey=my-python-project
sonar.projectName=My Python Project
sonar.projectVersion=1.0
sonar.sources=Analyzer/try.py
sonar.language=py
sonar.sourceEncoding=UTF-8
```
3. Run the Scanner : From each project root, execute:
```
sonar-scanner \
  -Dsonar.projectBaseDir=. \
  -Dsonar.sources=Analyzer/try.py
```
As we are working with a cluster of software projects to run them together, you need to configure your Jenkins pipeline

```bash
stages {
  stage('SonarQube Analysis') {
    steps {
      script {
        def projects = ["apache//accumulo", 
        "apache//activemq-artemis",
         "apache//ambari", "apache//arrow", 
         "apache//arrow-datafusion", 
         "apache//avro", 
         "apache//beam", 
         "apache//brooklyn-server", 
         "apache//camel",
          "apache//camel-quarkus", 
          "apache//cassandra",
           "apache//cloudstack", 
           "apache//cxf", 
           "apache//doris",
            "apache//dubbo", 
            "apache//fineract",
            "apache//groovy", 
            "apache//ignite", 
            "apache//incubator-celeborn",
            "apache//jackrabbit-oak",
            "apache//james-project", 
            "apache//kyuubi", 
            "apache//maven", 
            "apache//netbeans",
            "apache//nifi", 
            "apache//ozone", 
            "apache//phoenix", 
            "apache//pulsar", 
            "apache//solr", 
            "apache//storm", 
            "apache//tomcat", 
            "apache//zeppelin", 
            "apache//zookeeper"]

        projects.each { p ->
          dir(p) {
            sh "sonar-scanner -Dsonar.projectKey=${p} -Dsonar.sources=src"
          }
        }
      }
    }
  }
}
```

4.To view Results: Open your SonarQube dashboard in the browser. Navigate to your project key. You’ll see issues such as bugs, vulnerabilities, code smells, and maintainability indexes for try.py
5. To visualize the metrics output 
# Research Question
1. Are the effort of safeguarding the releases prone to introducing quality debt to the target release?
2. How does quality debt evolve in release lifecycle?
3. When and why do developers induce new technical debt in LTS support?

# Links

# Install
 [gh api](https://cli.github.com/manual/gh_api)
 
 # Data retrieve
 - gh repo list eclipse -L 300 > eclipse.csv

 # Get the list of projects inside apache dir
 
 - ls -l apache | grep "^d" | wc -l

# Diagram

[Backport Workflow Diagram](https://drive.google.com/file/d/1Ihp0vFnOlCfWVOWmG3WEYZAFupf9f5--/view?usp=sharing)
