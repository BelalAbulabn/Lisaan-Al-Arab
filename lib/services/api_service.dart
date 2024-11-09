import 'package:http/http.dart' as http;
import 'dart:convert';

class ApiService {
  static const String apiUrl = 'http://192.168.8.140:3021/generate-text'; // Update based on your setup

  static Future<String> sendMessage(String userInput) async {
    try {
      print("Sending POST request to $apiUrl with input: $userInput"); // Debug log

      final response = await http.post(
        Uri.parse(apiUrl),
        headers: {
          'Content-Type': 'application/json',
        },
        body: jsonEncode({"input": userInput}),
      );

       if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        print("Received response: ${data['response']}"); // Debug log
        return data['response'] ?? 'No response';
      } else {
        print("Error: Status code ${response.statusCode}"); // Debug log
        return 'Error: ${response.statusCode}';
      }
    } catch (e) {
      print("Error sending request: $e"); // Debug log
      return 'Error: $e';
    }
  }
}
