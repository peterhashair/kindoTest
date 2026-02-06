#!/usr/bin/env node
import "source-map-support/register";
import * as cdk from "aws-cdk-lib";
import { KindoTestStack } from "../kindo-test-stack";
const app = new cdk.App();
new KindoTestStack(app, "KindoTestStack");
