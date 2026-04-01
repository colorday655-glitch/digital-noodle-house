pipeline {
    agent any
    
    environment {
        VM_HOST = '173.254.206.13'
        VM_USER = 'root'
        VM_PATH = '/var/www/html'
        FEISHU_WEBHOOK = credentials('feishu-webhook')
    }
    
    stages {
        stage('Clone') {
            steps {
                echo '📥 从 GitHub 拉取代码...'
                sh 'git clone https://github.com/colorday655-glitch/digital-noodle-house.git ${WORKSPACE}/repo'
            }
        }
        
        stage('质检 - 关键字检查') {
            steps {
                echo '🔍 执行关键字质检...'
                script {
                    def content = readFile("${WORKSPACE}/repo/index.html")
                    
                    if (!content.contains('红烧肉面')) {
                        error '❌ 质检失败：index.html 必须包含“红烧肉面”'
                    }
                    if (!content.contains('清炒时蔬')) {
                        error '❌ 质检失败：index.html 必须包含“清炒时蔬”'
                    }
                    
                    echo '✅ 关键字质检通过'
                }
            }
        }
        
        stage('部署') {
            steps {
                echo '🚀 部署到 VM...'
                sh '''
                    scp -o StrictHostKeyChecking=no ${WORKSPACE}/repo/index.html ${VM_USER}@${VM_HOST}:${VM_PATH}/index.html
                '''
                echo '✅ 部署成功'
            }
        }
        
        stage('通知') {
            steps {
                echo '📢 发送飞书通知...'
                sh """
                    curl -X POST '${FEISHU_WEBHOOK}' \
                        -H 'Content-Type: application/json' \
                        -d '{
                            "msg_type": "text",
                            "content": {
                                "text": "🎉 质检通过，招牌菜品已自动上架正式环境，准备营业！"
                            }
                        }'
                """
            }
        }
    }
    
    post {
        success {
            echo '✅ 流水线执行成功'
        }
        failure {
            echo '❌ 流水线执行失败'
        }
    }
}
