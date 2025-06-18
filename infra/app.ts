import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';

export class ConstructionInfraStack extends cdk.Stack {
    constructor(scope: Construct, id: string, props?: cdk.StackProps) {
        super(scope, id, props);

        new lambda.Function(this, 'ConstructionLambda', {
            runtime: lambda.Runtime.PYTHON_3_10,
            handler: 'main.handler',
            code: lambda.Code.fromAsset('../lambda'),
        });
    }
}

const app = new cdk.App();
new ConstructionInfraStack(app, 'ConstructionInfraStack');
