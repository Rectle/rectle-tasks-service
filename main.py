import os
import pika
import sys
from flask import Flask, request, jsonify, make_response
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

credentials = pika.PlainCredentials(os.getenv('RABBITMQ_USER'), os.getenv('RABBITMQ_PASS'))

@app.route("/", methods=["POST"])
def add_task():
    try:
        task_id = request.json['task']

        connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv('RABBITMQ_HOST'), port=os.getenv('RABBITMQ_PORT'), credentials=credentials))
        channel = connection.channel()
        channel.queue_declare(queue='task_queue', durable=True)

        channel.basic_publish(
            exchange='',
            routing_key='task_queue',
            body=task_id,
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )

        connection.close()
        
        response = make_response(
            jsonify(
                {"status": "ok"}
            ),
            201,
        )
        response.headers["Content-Type"] = "application/json"
        return response
    except:
        response = make_response(
            jsonify(
                {"status": "error"}
            ),
            503,
        )
        response.headers["Content-Type"] = "application/json"
        return response

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))