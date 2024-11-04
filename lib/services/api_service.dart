
import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import '../models/models_model.dart';
class ApiService {
  // IBM Watsonx AI service URL
  static const String IAM_URL = 'https://iam.cloud.ibm.com/identity/token';

  static const String SERVICE_URL = 'https://eu-de.ml.cloud.ibm.com';
  // Your API key (keep it secure)
  static const String API_KEY = 'A7fCX7J8EARR85DLvSAyrMoKNCD13ICvnmHbpvNENZNR';
  static const String PROJECT_ID = 'b5976110-fe74-4388-b42f-ec08a9fad675';
  static const String MODEL_ID = 'sdaia/allam-1-13b-instruct';
  static Future<String> getIamToken() async {
    final Map<String, String> headers = {
      'Content-Type': 'application/x-www-form-urlencoded',
    };

    final String data =
        'grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey=$API_KEY';

    final http.Response response = await http.post(
      Uri.parse(IAM_URL),
      headers: headers,
      body: data,
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body)['access_token'];
    } else {
      throw Exception('Failed to obtain IAM token: ${response.body}');
    }
  }
  
   // Your model ID
    
static Future<String> sendMessage({required String message}) async {
  try {
    // Obtain IAM Token
    String iamToken = await getIamToken();

    // Construct the full URL
    final String url = '$SERVICE_URL/ml/v1-beta/generation/text?version=2023-05-18';

    // Set up the request headers
    final Map<String, String> headers = {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer $iamToken',
      'Accept': 'application/json',
    };

    // Set up the request body
    final Map<String, dynamic> parameters = {
      "decoding_method": "greedy",
      "max_new_tokens": 900,
      "repetition_penalty": 1.05,
    };

    final Map<String, dynamic> body = {
      'model_id': MODEL_ID,
      'input': message,
      'parameters': parameters,
      'project_id': PROJECT_ID, // Add project_id to the request body
    };

    // Make the POST request
    final http.Response response = await http.post(
      Uri.parse(url),
      headers: headers,
      body: jsonEncode(body),
    );

    // Handle the response
    if (response.statusCode == 200) {
      final Map<String, dynamic> jsonResponse = jsonDecode(utf8.decode(response.bodyBytes));
      String generatedText = jsonResponse['results'][0]['generated_text'];
      return generatedText;
      
    } else {
      // Log the response body for debugging
      print('Status Code: ${response.statusCode}');
      print('Response Body: ${response.body}');

      // Handle errors
      final Map<String, dynamic> errorResponse = jsonDecode(response.body);
      String errorMessage = errorResponse['errors'] != null
          ? errorResponse['errors'][0]['message']
          : response.reasonPhrase ?? 'Unknown error';
      throw Exception('Failed to generate text: $errorMessage');
    }
  } catch (error) {
    print('Error in sendMessage: $error');
    rethrow;
  }
}


  // Optional: Implement getModels if needed
   static Future<List<ModelsModel>> getModels() async {
    try {
      final String url = '$SERVICE_URL/v1/projects/$PROJECT_ID/models';
      final Map<String, String> headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $API_KEY',
        'Accept': 'application/json',
      };

      final http.Response response = await http.get(
        Uri.parse(url),
        headers: headers,
      );

      if (response.statusCode == 200) {
        final Map<String, dynamic> jsonResponse = jsonDecode(response.body);

        // Adjust the parsing according to the actual API response
        final List<dynamic> modelsData = jsonResponse['resources'] ?? [];

        List<ModelsModel> models = modelsData.map((modelData) {
          return ModelsModel.fromJson(modelData);
        }).toList();

        return models;
      } else {
        // Handle errors
        final Map<String, dynamic> errorResponse = jsonDecode(response.body);
        String errorMessage = errorResponse['errors'] != null
            ? errorResponse['errors'][0]['message']
            : response.reasonPhrase ?? 'Unknown error';
        throw HttpException('Failed to retrieve models: $errorMessage');
      }
    } catch (error) {
      print('Error in getModels: $error');
      rethrow;
    }
  }
}
