import json
# Impor library lain yang Anda butuhkan untuk prediksi
# from your_model_library import load_model, predict

def handler(event, context):
    """
    Menangani request ke /api/predict.
    """
    # Jika Anda menerima data melalui POST request
    # body = json.loads(event['body'])
    # input_data = body['data']

    # --- Logika Prediksi Anda di Sini ---
    # model = load_model('model.pkl')
    # result = predict(input_data)
    
    # Contoh hasil
    prediction_result = {"prediction": "hasil_prediksi_anda"}

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*' # Penting untuk mengizinkan request dari frontend
        },
        'body': json.dumps(prediction_result)
    }