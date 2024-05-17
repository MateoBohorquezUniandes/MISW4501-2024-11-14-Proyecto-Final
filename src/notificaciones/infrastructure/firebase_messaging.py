from firebase_admin import credentials, messaging


class MessageAdmin:
    def subscribe_topic(self, tokens, topic):  # tokens is a list of registration tokens

        response = messaging.subscribe_to_topic(tokens, topic)
        if response.failure_count > 0:
            print(
                f"Failed to subscribe to topic {topic} due to {list(map(lambda e: e.reason,response.errors))}"
            )
        print(response.success_count, "tokens were subscribed successfully")

    def send_topic_push(self, title, body, topic):
        message = messaging.Message(
            notification=messaging.Notification(title=title, body=body), topic=topic
        )
        # Send a message to the devices subscribed to the provided topic.
        response = messaging.send(message)
        # Response is a message ID string.
        print("Successfully sent message:", response)
