pipeline {
    agent any
    
    environment {
        VM_HOST = '173.254.206.13'
        VM_USER = 'root'
        TARGET_PATH = '/var/www/html/digital-noodle-house/index.html'
    }
    
    stages {
        stage('Clone') {
            steps {
                echo '📥 从 GitHub 拉取代码...'
                git branch: 'main', credentialsId: 'github', url: 'https://github.com/colorday655-glitch/digital-noodle-house.git'
            }
        }
        
        stage('质检') {
            steps {
                echo '🔍 执行关键字质检...'
                script {
                    def content = readFile 'index.html'
                    
                    // 检查红烧肉面
                    if (!content.contains('红烧肉面')) {
                        error '❌ 质检失败：index.html 必须包含“红烧肉面”'
                    }
                    
                    // 检查清炒时蔬
                    if (!content.contains('清炒时蔬')) {
                        error '❌ 质检失败：index.html 必须包含“清炒时蔬”'
                    }
                    
                    echo '✅ 关键字质检通过'
                }
            }
        }
        
        stage('Deploy') {
            steps {
                echo '🚀 部署到 VM...'
                script {
                    sh '''
                        ssh -o StrictHostKeyChecking=no ${VM_USER}@${VM_HOST} "curl -s https://raw.githubusercontent.com/colorday655-glitch/digital-noodle-house/main/index.html -o ${TARGET_PATH}"
                    '''
                }
                echo '✅ 部署成功'
            }
        }
        
        stage('Notify') {
            steps {
                echo '📢 发送飞书通知...'
                script {
                    def webhook = 'https://open.feishu.cn/open-apis/bot/v2/hook/1c2e5968-071c-4a69-b88d-c881b55754cc'
                    def message = '''
                    {
                        "msg_type": "text",
                        "content": {
                            "text": "✅ 质检通过，招牌菜品已自动上架正式环境，准备营业！\\n🍜 红烧肉面\\n🥬 清炒时蔬\\n📍 http://jackbaba.cn/digital-noodle-house/"
                        }
                    }
                    '''
                    sh "curl -s -X POST '${webhook}' -H 'Content-Type: application/json' -d '${message}'"
                }
            }
        }
    }
    
    post {
        success {
            echo '🎉 流水线执行成功！'
        }
        failure {
            echo '❌ 流水线执行失败'
        }
    }
}
