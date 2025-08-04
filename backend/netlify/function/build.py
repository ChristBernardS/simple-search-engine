import json
# Impor library yang dibutuhkan untuk proses build

def handler(event, context):
    """
    Menangani request ke /api/build.
    """
    # --- Logika Build Anda di Sini ---
    # misal: build_some_data()
    
    build_status = {"status": "Build successful"}

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(build_status)
    }