pipeline {
    agent any
    
    environment {
        VM_HOST = '173.254.206.13'
        VM_USER = 'root'
        VM_PWD = 'Xq87WaE9vMfW20l3hQ'
        TARGET_DIR = '/var/www/html/digital-noodle-house'
        GIT_REPO = 'https://github.com/colorday655-glitch/digital-noodle-house.git'
        FEISHU_WEBHOOK = 'https://open.feishu.cn/open-apis/bot/v2/hook/1c2e5968-071c-4a69-b88d-c881b55754cc'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo '从 GitHub 拉取代码...'
                checkout scm
            }
        }
        
        stage('质量检查') {
            steps {
                echo '执行关键字质检...'
                script {
                    def content = readFile 'index.html'
                    def checks = [
                        '红烧肉面': content.contains('红烧肉面'),
                        '清炒时蔬': content.contains('清炒时蔬')
                    ]
                    
                    def failed = checks.findAll { !it.value }
                    if (failed) {
                        error "质检失败：缺少关键字 ${failed.keySet().join(', ')}"
                    }
                    echo "✓ 质检通过：${checks.keySet().join(', ')} 均已包含"
                }
            }
        }
        
        stage('部署到VM') {
            steps {
                echo '通过 SSH 部署到 VM...'
                sh """
                    sshpass -p '${env.VM_PWD}' ssh -o StrictHostKeyChecking=no ${env.VM_USER}@${env.VM_HOST} "mkdir -p ${env.TARGET_DIR}"
                    sshpass -p '${env.VM_PWD}' scp -o StrictHostKeyChecking=no index.html ${env.VM_USER}@${env.VM_HOST}:${env.TARGET_DIR}/
                """
                echo '✓ 部署完成'
            }
        }
        
        stage('飞书通知') {
            steps {
                echo '发送飞书通知...'
                sh """
                    curl -X POST -H 'Content-Type: application/json' \
                    -d '{"msg_type":"text","content":{"text":"✅ 质检通过，招牌菜品已自动上架正式环境，准备营业！"}}' \
                    ${env.FEISHU_WEBHOOK}
                """
            }
        }
    }
    
    post {
        success {
            echo '🎉 部署成功！'
        }
        failure {
            echo '❌ 部署失败，请检查日志'
        }
    }
}
