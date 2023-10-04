@Library('my-shared-library') _

pipeline{

    agent any

    parameters{

        choice(name: 'action', choices: 'create\ndelete', description: 'Choose create/Destroy')
        string(name: 'ImageName', description: "name of the docker build", defaultValue: 'javapp')
        string(name: 'ImageTag', description: "tag of the docker build", defaultValue: 'v1')
        string(name: 'DockerHubUser', description: "name of the Application", defaultValue: 'ankitharao')
    }

    stages{
         
        stage('Git Checkout'){
                    when { expression {  params.action == 'create' } }
            steps{
            gitCheckout(
                branch: "main",
                url: "https://github.com/Ankithasrao/Java_app_3.0.git"
            )
            }
        }
         stage('Unit Test maven'){
         
         when { expression {  params.action == 'create' } }

            steps{
               script{
                   
                   mvnTest()
               }
            }
        }
         stage('Integration Test maven'){
         when { expression {  params.action == 'create' } }
            steps{
               script{
                   
                   mvnIntegrationTest()
               }
            }
        }
       //  stage('Static code analysis: Sonarqube'){
       //   when { expression {  params.action == 'create' } }
       //      steps{
       //         script{
                   
       //             def SonarQubecredentialsId = 'sonarqube-api'
       //             statiCodeAnalysis(SonarQubecredentialsId)
       //         }
       //      }
       // }
       // stage('Quality Gate Status Check : Sonarqube'){
       //   when { expression {  params.action == 'create' } }
       //      steps{
       //         script{
                   
       //             def SonarQubecredentialsId = 'sonarqube-api'
       //             QualityGateStatus(SonarQubecredentialsId)
       //         }
       //      }
       // }
        stage('Maven Build : maven'){
         when { expression {  params.action == 'create' } }
            steps{
               script{
                   
                   mvnBuild()
               }
            }
        }
        stage('Build and Add Artifact to the repo : JFrog') {
            steps {
                script {
                    // Artifactory configuration
                    def artifactoryUrl = 'http://18.204.16.85:8081/artifactory'
                    def repoName = 'example-repo-local'
                    def targetPath = 'http://18.204.16.85:8082/artifactory/example-repo-local/kubernetes-configmap-reload-0.0.1-SNAPSHOT.jar'
                    def localArtifactPath = 'kubernetes-configmap-reload-0.0.1-SNAPSHOT.jar'
                    def apiKeyOrUsername = 'admin'
                    def apiKeyOrPassword = 'Password@123'

                       // Extract the filename from the localArtifactPath
                    def fileName = localArtifactPath.split('/').last()

                    // Construct the full URL to upload the artifact
                    def uploadUrl = "${artifactoryUrl}/${repoName}/${targetPath}/$(basename ${localArtifactPath})"

                    // Upload the artifact using curl
                    def uploadCommand = """
                        curl -X PUT -u ${apiKeyOrUsername}:${apiKeyOrPassword} -T ${localArtifactPath} ${uploadUrl}
                    """
                    def uploadResult = sh(script: uploadCommand, returnStatus: true)

                    if (uploadResult == 0) {
                        echo "Artifact successfully uploaded to Artifactory."
                    } else {
                        error "Failed to upload artifact to Artifactory. Exit code: ${uploadResult}"
                    }
                }
            }
        }
        stage('Docker Image Build'){
         when { expression {  params.action == 'create' } }
            steps{
               script{
                   
                   dockerBuild("${params.ImageName}","${params.ImageTag}","${params.DockerHubUser}")
               }
            }
        }
         stage('Docker Image Scan: trivy '){
         when { expression {  params.action == 'create' } }
            steps{
               script{
                   
                   dockerImageScan("${params.ImageName}","${params.ImageTag}","${params.DockerHubUser}")
               }
            }
        }
        stage('Docker Image Push : DockerHub '){
         when { expression {  params.action == 'create' } }
            steps{
               script{
                   
                   dockerImagePush("${params.ImageName}","${params.ImageTag}","${params.DockerHubUser}")
               }
            }
        }   
        stage('Docker Image Cleanup : DockerHub '){
         when { expression {  params.action == 'create' } }
            steps{
               script{
                   
                   dockerImageCleanup("${params.ImageName}","${params.ImageTag}","${params.DockerHubUser}")
               }
            }
        }      
    }
}
