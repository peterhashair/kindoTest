import {
  Stack,
  StackProps,
  aws_ec2 as ec2,
  aws_rds as rds,
  aws_ecs as ecs,
  aws_ecs_patterns as ecsPatterns,
  aws_ecr_assets as ecrAssets,
  aws_iam as iam,
  RemovalPolicy,
} from "aws-cdk-lib";
import { Construct } from "constructs";

export class KindoTestStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    // VPC
    const vpc = new ec2.Vpc(this, "KindoVpc", { maxAzs: 2 });

    // RDS Postgres
    const db = new rds.DatabaseInstance(this, "KindoPostgres", {
      engine: rds.DatabaseInstanceEngine.postgres({
        version: rds.PostgresEngineVersion.VER_15_3,
      }),
      vpc,
      instanceType: ec2.InstanceType.of(
        ec2.InstanceClass.BURSTABLE2,
        ec2.InstanceSize.SMALL,
      ),
      credentials: rds.Credentials.fromGeneratedSecret("kindo"),
      databaseName: "kindotest",
      multiAz: false,
      allocatedStorage: 20,
      maxAllocatedStorage: 100,
      publiclyAccessible: false,
      vpcSubnets: { subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS },
      removalPolicy: RemovalPolicy.DESTROY,
      deletionProtection: false,
    });

    // ECS Cluster
    const cluster = new ecs.Cluster(this, "KindoCluster", { vpc });

    // Fargate Service for backend (placeholder, image must be built and pushed to ECR)
    const backendTaskImage = ecs.ContainerImage.fromRegistry(
      "amazon/amazon-ecs-sample",
    );
    new ecsPatterns.ApplicationLoadBalancedFargateService(
      this,
      "BackendService",
      {
        cluster,
        taskImageOptions: {
          image: backendTaskImage,
          containerPort: 8000,
          environment: {
            DATABASE_URL:
              "postgres://kindo:<password>@" +
              db.dbInstanceEndpointAddress +
              ":5432/kindotest",
          },
        },
        publicLoadBalancer: true,
      },
    );

    // Fargate Service for frontend (placeholder, image must be built and pushed to ECR)
    const frontendTaskImage = ecs.ContainerImage.fromRegistry("nginx");
    new ecsPatterns.ApplicationLoadBalancedFargateService(
      this,
      "FrontendService",
      {
        cluster,
        taskImageOptions: {
          image: frontendTaskImage,
          containerPort: 80,
        },
        publicLoadBalancer: true,
      },
    );
  }
}
