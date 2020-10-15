A simple SMS application which uses Africastalking as a SMS Gateway
Following are some of the features that the application supports
1. A Gateway model to configure SMS providers dynamically
2. A full fledged Message Table to store message data
3. A utils function which can be used independently to send sms
4. A route /message/file/upload to upload bulk sms data
5. Sample Bulk SMS upload document SMS/static/media/bulk_sms.csv
6. Parses file and display bad rows once upload is completed.

What can be improved
1. Bulk Sms sending can be pushed to a celery process to free up the frontend

![file_upload_demo](https://user-images.githubusercontent.com/67738912/96155401-921df280-0f18-11eb-91bf-986baabb5490.png)
File Format- Should follow the following format for Bulk SMS
![file_format](https://user-images.githubusercontent.com/67738912/96155558-bc6fb000-0f18-11eb-9e67-ccf191fa108f.png)
