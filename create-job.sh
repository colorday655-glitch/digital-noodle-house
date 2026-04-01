#!/bin/bash
JENKINS_URL="http://173.254.206.13:8080"
JOB_NAME="digital-noodle-house"
GIT_REPO="https://github.com/colorday655-glitch/digital-noodle-house.git"
GIT_BRANCH="*/main"
FEISHU_WEBHOOK="https://open.feishu.cn/open-apis/bot/v2/hook/1c2e5968-071c-4a69-b88d-c881b55754cc"

JOB_CONFIG="<?xml version='1.1' encoding='UTF-8'?>
<flow-definition plugin='workflow-job@1333'>
  <description>无人面馆 CI/CD 流水线</description>
  <keepDependencies>false</keepDependencies>
  <properties/>
  <definition class='org.jenkinsci.plugins.workflow.cps.CpsScmFlowDefinition' plugin='workflow-cps@3903'>
    <scriptPath>Jenkinsfile</scriptPath>
    <lightweight>true</lightweight>
    <scm class='hudson.plugins.git.GitSCMSource'>
      <remote>${GIT_REPO}</remote>
      <credentialsId>-1</credentialsId>
      <traits>
        <hudson.plugins.git.traits.BranchDiscoveryTrait>
          <strategyId>1</strategyId>
        </hudson.plugins.git.traits.BranchDiscoveryTrait>
      </traits>
      <includes>${GIT_BRANCH}</includes>
      <excludes></excludes>
    </scm>
  </definition>
  <disabled>false</disabled>
</flow-definition>"

echo "创建 Jenkins Job: ${JOB_NAME}"
curl -X POST "${JENKINS_URL}/job/${JOB_NAME}/config.xml" \
  -u "admin:$(cat /tmp/jenkins_token 2>/dev/null || echo '')" \
  -H "Content-Type: text/xml" \
  --data "${JOB_CONFIG}" \
  -w "\nHTTP Status: %{http_code}\n"

echo ""
echo "Job 创建完成！访问 http://173.254.206.13:8080/job/${JOB_NAME} 查看"