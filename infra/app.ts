import { App, Stack, StackProps, Duration } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { DockerImageFunction, Architecture, DockerImageCode, ApplicationLogLevel, SystemLogLevel, LogFormat } from 'aws-cdk-lib/aws-lambda';
import { PolicyStatement } from 'aws-cdk-lib/aws-iam';
export class ConstructionInfraStack extends Stack {
    constructor(scope: Construct, id: string, props?: StackProps) {
        super(scope, id, props);
        const { account, region } = Stack.of(this);
        new DockerImageFunction(this, 'ConstructionLambda', {
            architecture: Architecture.ARM_64,
            code: DockerImageCode.fromImageAsset('../lambda'),
            memorySize: 1000,
            timeout: Duration.seconds(30),
            logFormat: LogFormat.JSON,
            applicationLogLevelV2: ApplicationLogLevel.INFO,
            systemLogLevelV2: SystemLogLevel.WARN,
            initialPolicy: [
                new PolicyStatement({
                    actions: ['secretsmanager:GetSecretValue'],
                    resources: [
                        `arn:aws:secretsmanager:${region}:${account}:secret:construction/google-service-account-ENfRVk`
                    ]
                })
            ]
        });
    }
}

const app = new App();
new ConstructionInfraStack(app, 'ConstructionInfraStack');
