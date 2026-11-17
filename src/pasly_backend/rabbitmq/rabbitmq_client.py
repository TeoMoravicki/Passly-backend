import pika
import json


def publicar_compra_confirmada(datos):
    conexion = pika.BlockingConnection(
        pika.ConnectionParameters("localhost")
    )

    canal = conexion.channel()

    canal.queue_declare(
        queue="compra_confirmada",
        durable=True
    )

    canal.basic_publish(
        exchange="",
        routing_key="compra_confirmada",
        body=json.dumps(datos),
        properties=pika.BasicProperties(
            delivery_mode=2
        )
    )

    conexion.close()