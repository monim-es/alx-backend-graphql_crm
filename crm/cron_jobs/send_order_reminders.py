import datetime
import requests
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

LOG_FILE = '/tmp/order_reminders_log.txt'  # You can change this if you want

def log_message(message):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, 'a') as f:
        f.write(f"{timestamp} - {message}\n")

def main():
    transport = RequestsHTTPTransport(
        url='http://localhost:8000/graphql',
        verify=True,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=False)

    query = gql('''
        query($days: Int!) {
            orders(days: $days) {
                id
                customer {
                    name
                }
                orderDate
            }
        }
    ''')

    params = {"days": 7}

    try:
        result = client.execute(query, variable_values=params)
        orders = result['orders']
        for order in orders:
            order_id = order['id']
            customer_name = order['customer']['name']
            order_date = order['orderDate']
            log_message(f"Reminder: Order {order_id} for customer {customer_name} (orderDate: {order_date})")
        print("Order reminders processed!")
    except Exception as e:
        log_message(f"Error querying GraphQL: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
