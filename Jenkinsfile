pipeline {
    agent any
    
    environment {
        VM_HOST = '173.254.206.13'
        VM_USER = 'root'
        VM_PWD = 'Xq87WaE9vMfW20l3hQ'
        TARGET_DIR = '/var/www/html/digital-noodle-house'
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
                sh 'grep -q "红烧肉面" index.html && grep -q "清炒时蔬" index.html && echo "质检通过：红烧肉面, 清炒时蔬" || exit 1'
            }
        }
        
        stage('部署到VM') {
            steps {
                sh 'sshpass -p "${VM_PWD}" ssh -o StrictHostKeyChecking=no ${VM_USER}@${VM_HOST} "mkdir -p ${TARGET_DIR}"'
                sh 'sshpass -p "${VM_PWD}" scp -o StrictHostKeyChecking=no index.html ${VM_USER}@${VM_HOST}:${TARGET_DIR}/'
                echo '部署完成'
            }
        }
        
        stage('飞书通知') {
            steps {
                sh 'curl -X POST -H "Content-Type: application/json" -d "{\\"msg_type\\":\\"text\\",\\"content\\":{\\"text\\":\\"✅ 质检通过，招牌菜品已自动上架正式环境，准备营业！\\"}}" "${FEISHU_WEBHOOK}"'
            }
        }
    }
    
    post {
        success { echo '部署成功' }
        failure { echo '部署失败' }
    }
}
