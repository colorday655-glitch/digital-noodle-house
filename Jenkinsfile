pipeline {
    agent any
    
    environment {
        GIT_REPO = 'https://github.com/colorday655-glitch/digital-noodle-house.git'
        BRANCH = 'main'
        VM_HOST = '173.254.206.13'
        VM_USER = 'root'
        DEPLOY_PATH = '/var/www/digital-noodle-house'
        FEISHU_WEBHOOK = 'https://open.feishu.cn/open-apis/bot/v2/hook/1c2e5968-071c-4a69-b88d-c881b55754cc'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo '📥 从 GitHub 拉取代码...'
                checkout scm
            }
        }
        
        stage('Quality Check') {
            steps {
                echo '🔍 执行关键字质检...'
                
                script {
                    def content = readFile 'index.html'
                    
                    def checks = [
                        '红烧肉面': content.contains('红烧肉面'),
                        '清炒时蔬': content.contains('清炒时蔬')
                    ]
                    
                    def failedChecks = checks.findAll { !it.value }
                    
                    if (failedChecks) {
                        error "❌ 质检失败：缺少关键字 ${failedChecks.key.join(', ')}"
                    }
                    
                    echo "✅ 质检通过：${checks.key.join(', ')} 均已包含"
                }
            }
        }
        
        stage('Deploy to VM') {
            steps {
                echo "🚀 部署到 ${VM_HOST}..."
                
                script {
                    sh """
                        ssh -o StrictHostKeyChecking=no ${VM_USER}@${VM_HOST} "
                            mkdir -p ${DEPLOY_PATH}
                            cd ${DEPLOY_PATH}
                            rm -rf index.html || true
                        "
                        
                        scp -o StrictHostKeyChecking=no index.html ${VM_USER}@${VM_HOST}:${DEPLOY_PATH}/
                        
                        ssh -o StrictHostKeyChecking=no ${VM_USER}@${VM_HOST} "
                            echo '✅ 文件部署成功'
                            ls -la ${DEPLOY_PATH}
                        "
                    """
                }
            }
        }
        
        stage('Notify Feishu') {
            steps {
                echo '📢 发送飞书通知...'
                
                script {
                    def message = '''
                    {
                        "msg_type": "post",
                        "content": {
                            "post": {
                                "zh_cn": {
                                    "title": "🎉 面馆部署成功",
                                    "content": [
                                        {
                                            "tag": "text",
                                            "text": "质检通过，招牌菜品已自动上架正式环境，准备营业！"
                                        },
                                        {
                                            "tag": "text", 
                                            "text": "\\n📍 地址：jackbaba.cn/digital-noodle-house"
                                        },
                                        {
                                            "tag": "at",
                                            "at_all": true
                                        }
                                    ]
                                }
                            }
                        }
                    }
                    '''
                    
                    def response = sh(
                        script: "curl -s -X POST -H 'Content-Type: application/json' -d '${message}' ${FEISHU_WEBHOOK}",
                        returnStdout: true
                    )
                    
                    echo "飞书通知响应: ${response}"
                }
            }
        }
    }
    
    post {
        success {
            echo '✅ Pipeline 执行成功'
        }
        failure {
            echo '❌ Pipeline 执行失败'
        }
    }
}
