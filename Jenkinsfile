pipeline {
    agent any
    
    environment {
        FEISHU_WEBHOOK = 'https://open.feishu.cn/open-apis/bot/v2/hook/1c2e5968-071c-4a69-b88d-c881b55754cc'
    }
    
    triggers {
        githubPush()
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code...'
                checkout scm
            }
        }
        
        stage('Quality Check') {
            steps {
                echo '检查核心关键字...'
                script {
                    def htmlContent = readFile 'index.html'
                    
                    if (!htmlContent.contains('红烧肉面')) {
                        error('质检失败：缺少核心菜品 - 红烧肉面')
                    }
                    if (!htmlContent.contains('清炒时蔬')) {
                        error('质检失败：缺少核心菜品 - 清炒时蔬')
                    }
                    
                    echo '✓ 核心关键字检查通过'
                }
            }
        }
        
        stage('Deploy') {
            steps {
                echo '部署到生产环境...'
                sh '''
                    echo "部署完成: $(date)"
                '''
            }
        }
        
        stage('Notify') {
            steps {
                echo '发送飞书通知...'
                sh """
                    curl -X POST \
                        -H 'Content-Type: application/json' \
                        -d '{
                            "msg_type": "text",
                            "content": {
                                "text": "质检通过，准备出餐 ✅\\n无人面馆已更新上线"
                            }
                        }' \
                        ${FEISHU_WEBHOOK}
                """
            }
        }
    }
    
    post {
        success {
            echo 'Pipeline 执行成功！'
        }
        failure {
            echo 'Pipeline 执行失败！'
            sh """
                curl -X POST \
                    -H 'Content-Type: application/json' \
                    -d '{
                        "msg_type": "text",
                        "content": {
                            "text": "❌ 无人面馆部署失败，请检查代码"
                        }
                    }' \
                    ${FEISHU_WEBHOOK}
            """
        }
    }
}
