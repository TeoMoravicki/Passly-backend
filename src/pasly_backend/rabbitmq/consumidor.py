import pika
import json


def procesar(ch, method, properties, body):
    datos = json.loads(body)

    print("Compra confirmada:")
    print(datos)

    ch.basic_ack(
        delivery_tag=method.delivery_tag
    )


conexion = pika.BlockingConnection(
    pika.ConnectionParameters("localhost")
)

canal = conexion.channel()

canal.queue_declare(
    queue="compra_confirmada",
    durable=True
)

canal.basic_consume(
    queue="compra_confirmada",
    on_message_callback=procesar
)

print("Esperando compras confirmadas...")

canal.start_consuming()