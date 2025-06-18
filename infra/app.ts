import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';

export class ConstructionInfraStack extends cdk.Stack {
    constructor(scope: Construct, id: string, props?: cdk.StackProps) {
        super(scope, id, props);

        new lambda.DockerImageFunction(this, 'ConstructionLambda', {
            code: lambda.DockerImageCode.fromImageAsset('../lambda/src'),
        });
    }
}

const app = new cdk.App();
new ConstructionInfraStack(app, 'ConstructionInfraStack');
