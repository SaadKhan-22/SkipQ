import boto3


class CloudWatchPutMetric:
    def __init__(self):
        self.client = boto3.client('cloudwatch')
        #https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html

    def put_data(self, namespace, metricName, dimensions, value):
        
        response = self.client.put_metric_data(Namespace = namespace,
        

        MetricData=[
            {
            'MetricName': metricName,
            'Dimensions': [dimensions],
                 'Value': value

                                }
                                ]
                                                )   
