import boto3

ec2 = boto3.client("ec2")

def get_instances():
    response = ec2.describe_instances(
        Filters=[
            {
                "Name": "tag:AutoStartStop",
                "Values": ["true"]
            },
            {
                "Name": "instance-state-name",
                "Values": ["running", "stopped"]
            }
        ]
    )

    instance_ids = []

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instance_ids.append(instance["InstanceId"])

    return instance_ids


def lambda_handler(event, context):
    action = event.get("action")

    instance_ids = get_instances()

    if not instance_ids:
        return {
            "status": "No instances found with tag AutoStartStop=true"
        }

    if action == "start":
        ec2.start_instances(InstanceIds=instance_ids)
        return {
            "status": "Started instances",
            "instances": instance_ids
        }

    elif action == "stop":
        ec2.stop_instances(InstanceIds=instance_ids)
        return {
            "status": "Stopped instances",
            "instances": instance_ids
        }

    else:
        return {
            "status": "Invalid action. Use start or stop."
        }
