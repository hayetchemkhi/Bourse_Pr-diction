pipeline {
    agent any
    stages {
        stage('Installer les Dépendances') {
            steps {
                script {
                    echo "Création de l'environnement virtuel et installation des dépendances"
                    sh '''
                    if [ ! -d venv ]; then
                        python3 -m venv venv || { echo "Erreur : Échec de la création de venv"; exit 1; }
                    fi
                    source venv/bin/activate
                    pip install -r requirements.txt
                    '''
                }
            }
        }
    }
}
