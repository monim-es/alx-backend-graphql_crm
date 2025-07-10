import datetime
import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def log_crm_heartbeat():
    timestamp = datetime.datetime.now().strftime('%d/%m/%Y-%H:%M:%S')
    with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
        f.write(f"{timestamp} CRM is alive\n")




def update_low_stock():
    LOG_FILE = '/tmp/low_stock_updates_log.txt'
    def log(message):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(LOG_FILE, 'a') as f:
            f.write(f"{timestamp} - {message}\n")

    transport = RequestsHTTPTransport(
        url='http://localhost:8000/graphql',
        verify=True,
        retries=3
    )
    client = Client(transport=transport, fetch_schema_from_transport=False)

    mutation = gql('''
        mutation {
            updateLowStockProducts {
                success
                message
                updatedProducts
            }
        }
    ''')

    try:
        result = client.execute(mutation)
        data = result['updateLowStockProducts']
        log(f"{data['message']} | Products: {', '.join(data['updatedProducts'])}")
        print("Low stock update successful.")
    except Exception as e:
        log(f"Error: {e}")
        print(f"Error: {e}")
