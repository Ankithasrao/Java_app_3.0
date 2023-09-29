import requests

# Artifactory configuration
artifactory_url = 'http://54.241.235.243:8082/artifactory/example-repo-local/kubernetes-configmap-reload-0.0.1-SNAPSHOT.jar'   # Replace with your Artifactory base URL
file_path = '/home/ubuntu/Java_app_3.0/target/kubernetes-configmap-reload-0.0.1-SNAPSHOT.jar'
username = 'admin'
password = 'Password@123'

# Upload JAR file to Artifactory
def upload_jar():
    
    try:
        with open(file_path, 'rb') as jar_file:
            response = requests.put(artifactory_url, data=jar_file, auth=(username, password))

        if response.status_code == 201:
            print(f'Artifact uploaded successfully')
        else:
            print(f'Failed to upload artifact: {response.status_code} - {response.text}')
    except Exception as e:
        print(f'Error uploading artifact: {e}')

if __name__ == "__main__":
    upload_jar()
